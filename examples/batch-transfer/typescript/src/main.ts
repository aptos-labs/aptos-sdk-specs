/**
 * Aptos Batch Transfer Example - TypeScript
 *
 * Demonstrates sending N APT transfers in parallel using:
 *   - Single sequence number fetch (not per-transaction)
 *   - Local build + sign before any submission
 *   - Promise.allSettled for parallel submit
 *   - Exponential backoff retry on confirmation
 *
 * Usage:
 *   bun src/main.ts [--count N] [--network devnet|testnet]
 */

import {
  Account,
  AccountAuthenticator,
  Aptos,
  AptosConfig,
  Network,
  SimpleTransaction,
} from "@aptos-labs/ts-sdk";

// ─── Constants ────────────────────────────────────────────────────────────────

const COIN_STORE = "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>";
const TRANSFER_AMOUNT_OCTAS = 100; // small amount per transfer
const FUND_AMOUNT_OCTAS = 100_000_000; // 1 APT
const MAX_GAS_AMOUNT = 10_000;

// ─── CLI Parsing ──────────────────────────────────────────────────────────────

function parseArgs(): { count: number; network: string } {
  const args = process.argv.slice(2);
  let count = 10;
  let network = "devnet";
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--count" && i + 1 < args.length) {
      count = parseInt(args[i + 1], 10);
      if (isNaN(count) || count < 1) {
        console.error("--count must be a positive integer");
        process.exit(1);
      }
    }
    if (args[i] === "--network" && i + 1 < args.length) {
      network = args[i + 1];
      if (network === "mainnet") {
        console.error(
          "Error: mainnet is not supported by this example because it funds a new account via faucet.",
        );
        console.error("To use mainnet, extend this example to accept a pre-funded sender key.");
        process.exit(1);
      }
      if (!["devnet", "testnet"].includes(network)) {
        console.error(`Error: unknown network "${network}". Allowed values: devnet, testnet`);
        process.exit(1);
      }
    }
  }
  return { count, network };
}

function toNetworkEnum(name: string): Network {
  return name === "testnet" ? Network.TESTNET : Network.DEVNET;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

async function getBalanceOctas(aptos: Aptos, address: Account["accountAddress"]): Promise<number> {
  try {
    const resource = await aptos.getAccountResource({
      accountAddress: address,
      resourceType: COIN_STORE as `${string}::${string}::${string}`,
    });
    return Number((resource as { coin: { value: string } }).coin.value);
  } catch {
    return 0;
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Waits for a submitted transaction to be confirmed, retrying with
 * exponential backoff if the wait times out.
 */
async function waitWithRetry(
  aptos: Aptos,
  hash: string,
  maxAttempts = 3,
  baseDelayMs = 2_000,
): Promise<{ hash: string }> {
  let lastError: unknown;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    if (attempt > 0) {
      const delay = baseDelayMs * Math.pow(2, attempt - 1);
      await sleep(delay);
    }
    try {
      const result = await aptos.waitForTransaction({
        transactionHash: hash,
        options: { timeoutSecs: 30, checkSuccess: true },
      });
      return { hash: result.hash };
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError ?? new Error(`Failed to confirm ${hash} after ${maxAttempts} attempts`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const { count, network: networkName } = parseArgs();
  const aptos = new Aptos(new AptosConfig({ network: toNetworkEnum(networkName) }));

  console.log(`\nAptos Batch Transfer Example (TypeScript)`);
  console.log(`==========================================`);
  console.log(`Network:      ${networkName}`);
  console.log(`Transactions: ${count}`);
  console.log();

  // ═══════════════════════════════════════════════════════════════════════════
  // Phase 1: Setup
  // ═══════════════════════════════════════════════════════════════════════════
  console.log(`[1/4] Setup`);

  const sender = Account.generate();
  console.log(`  ✓ Generated sender:  ${sender.accountAddress.toString()}`);

  const recipients: Account[] = Array.from({ length: count }, () => Account.generate());
  console.log(`  ✓ Generated ${count} recipient accounts`);

  // Fund the sender via the devnet/testnet faucet
  const fundResult = await aptos.fundAccount({
    accountAddress: sender.accountAddress,
    amount: FUND_AMOUNT_OCTAS,
  });
  await aptos.waitForTransaction({ transactionHash: fundResult.hash });
  console.log(`  ✓ Funded sender with 1 APT (tx: ${fundResult.hash})`);

  const initialBalance = await getBalanceOctas(aptos, sender.accountAddress);
  console.log(`  ✓ Sender balance: ${initialBalance.toLocaleString()} octas`);
  console.log();

  // ═══════════════════════════════════════════════════════════════════════════
  // Phase 2: Batch Submission
  // ═══════════════════════════════════════════════════════════════════════════
  console.log(`[2/4] Batch Submission (${count} transactions)`);

  // Estimate gas price once for all transactions
  const gasEstimate = await aptos.getGasPriceEstimation();
  const gasUnitPrice = gasEstimate.gas_estimate;
  console.log(`  ✓ Gas price estimate: ${gasUnitPrice} octas/gas`);

  // KEY INSIGHT: Fetch the sequence number ONCE, then increment locally.
  // Without this, each build.simple() would call the chain for the seq num,
  // causing N round-trips and making parallel submission impossible.
  const accountInfo = await aptos.getAccountInfo({ accountAddress: sender.accountAddress });
  const startSeqNum = BigInt(accountInfo.sequence_number);
  console.log(`  ✓ Starting sequence number: ${startSeqNum}`);

  // Build and sign all transactions locally (zero network calls per-transaction)
  const t0 = Date.now();
  const prepared: Array<{ txn: SimpleTransaction; auth: AccountAuthenticator }> = [];

  for (let i = 0; i < count; i++) {
    const txn = await aptos.transaction.build.simple({
      sender: sender.accountAddress,
      data: {
        function: "0x1::aptos_account::transfer",
        functionArguments: [recipients[i].accountAddress, TRANSFER_AMOUNT_OCTAS],
      },
      options: {
        accountSequenceNumber: startSeqNum + BigInt(i),
        gasUnitPrice,
        maxGasAmount: MAX_GAS_AMOUNT,
      },
    });
    const auth = aptos.transaction.sign({ signer: sender, transaction: txn });
    prepared.push({ txn, auth });
  }

  const buildMs = Date.now() - t0;
  console.log(`  ✓ Built & signed ${count} transactions locally in ${buildMs}ms`);

  // Submit all transactions in parallel
  const t1 = Date.now();
  const submitResults = await Promise.allSettled(
    prepared.map(({ txn, auth }) =>
      aptos.transaction.submit.simple({
        transaction: txn,
        senderAuthenticator: auth,
      }),
    ),
  );
  const submitMs = Date.now() - t1;

  const pendingHashes: string[] = [];
  const submitErrors: string[] = [];
  for (const result of submitResults) {
    if (result.status === "fulfilled") {
      pendingHashes.push(result.value.hash);
    } else {
      submitErrors.push(String(result.reason));
    }
  }

  console.log(`  ✓ Submitted ${pendingHashes.length}/${count} in ${submitMs}ms`);
  if (submitErrors.length > 0) {
    console.log(`  ⚠ ${submitErrors.length} submission failure(s)`);
    for (const e of submitErrors) console.log(`    - ${e}`);
  }
  console.log();

  // ═══════════════════════════════════════════════════════════════════════════
  // Phase 3: Track & Confirm
  // ═══════════════════════════════════════════════════════════════════════════
  console.log(`[3/4] Tracking Confirmations`);

  const confirmResults = await Promise.allSettled(
    pendingHashes.map((hash) => waitWithRetry(aptos, hash)),
  );

  const confirmed = confirmResults.filter((r) => r.status === "fulfilled").length;
  const confirmFailed = confirmResults.filter((r) => r.status === "rejected").length;

  console.log(`  ✓ Confirmed: ${confirmed}/${pendingHashes.length}`);
  if (confirmFailed > 0) {
    console.log(`  ✗ Failed to confirm: ${confirmFailed}`);
  }
  console.log();

  // ═══════════════════════════════════════════════════════════════════════════
  // Phase 4: Verify & Report
  // ═══════════════════════════════════════════════════════════════════════════
  console.log(`[4/4] Verify & Report`);

  const finalBalance = await getBalanceOctas(aptos, sender.accountAddress);
  const totalSpent = Math.max(0, initialBalance - finalBalance);
  const avgCostPerTx = confirmed > 0 ? Math.round(totalSpent / confirmed) : 0;

  console.log(`  ✓ Final balance: ${finalBalance.toLocaleString()} octas`);
  console.log(`  ✓ Total spent (transfers + gas): ${totalSpent.toLocaleString()} octas`);

  const report = {
    network: networkName,
    timestamp: new Date().toISOString(),
    transactions: {
      requested: count,
      submitted: pendingHashes.length,
      confirmed,
      failed: submitErrors.length + confirmFailed,
    },
    performance: {
      build_and_sign_ms: buildMs,
      submit_ms: submitMs,
    },
    economics: {
      initial_balance_octas: initialBalance,
      final_balance_octas: finalBalance,
      total_spent_octas: totalSpent,
      avg_cost_per_tx_octas: avgCostPerTx,
    },
  };

  console.log(`\n=== Summary ===`);
  console.log(JSON.stringify(report, null, 2));
}

main().catch((err: unknown) => {
  console.error("\nFatal error:", err instanceof Error ? err.message : err);
  process.exit(1);
});
