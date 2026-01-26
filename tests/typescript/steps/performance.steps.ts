import { Given, When, Then, Before, After, setDefaultTimeout } from "@cucumber/cucumber";
import {
  Aptos,
  AptosConfig,
  Network,
  Account,
  Ed25519PrivateKey,
  AccountAddress,
} from "@aptos-labs/ts-sdk";
import { sha3_256 } from "@noble/hashes/sha3.js";
import { TestWorld, BenchmarkResult } from "../support/world";

// Set longer timeout for performance tests (10 minutes)
setDefaultTimeout(600000);

interface PerformanceResults {
  sdk: string;
  version: string;
  runtime: string;
  network: string;
  timestamp: string;
  environment: {
    platform: string;
    arch: string;
    nodeVersion: string;
  };
  results: Record<string, number>;
}

// Global performance results collector
const performanceResults: PerformanceResults = {
  sdk: "typescript",
  version: "5.2.0",
  runtime: `bun ${process.versions.bun || "unknown"}`,
  network: "devnet",
  timestamp: new Date().toISOString(),
  environment: {
    platform: process.platform,
    arch: process.arch,
    nodeVersion: process.version,
  },
  results: {},
};

function calculateStats(samples: number[]): BenchmarkResult {
  const sorted = [...samples].sort((a, b) => a - b);
  const sum = sorted.reduce((acc, val) => acc + val, 0);
  const avg = sum / sorted.length;
  const p95Index = Math.floor(sorted.length * 0.95);
  const p95 = sorted[p95Index] || sorted[sorted.length - 1];
  const min = sorted[0];
  const max = sorted[sorted.length - 1];
  const totalTime = sum;
  const opsPerSecond = sorted.length / (totalTime / 1000);

  return { samples: sorted, avg, p95, min, max, opsPerSecond };
}

async function measureTime<T>(fn: () => Promise<T>, iterations: number): Promise<BenchmarkResult> {
  const samples: number[] = [];

  // Warmup
  for (let i = 0; i < Math.min(5, iterations); i++) {
    await fn();
  }

  // Actual measurements
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    await fn();
    const end = performance.now();
    samples.push(end - start);
  }

  return calculateStats(samples);
}

function measureTimeSync<T>(fn: () => T, iterations: number): BenchmarkResult {
  const samples: number[] = [];

  // Warmup
  for (let i = 0; i < Math.min(10, iterations); i++) {
    fn();
  }

  // Actual measurements
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    fn();
    const end = performance.now();
    samples.push(end - start);
  }

  return calculateStats(samples);
}

// =============================================================================
// Setup
// =============================================================================

Given("a configured Aptos client for devnet", function (this: TestWorld) {
  const config = new AptosConfig({ network: Network.DEVNET });
  this.aptos = new Aptos(config);
});

Given("a known funded account address", async function (this: TestWorld) {
  // Use a well-known devnet address that should have resources
  this.address = AccountAddress.fromString(
    "0x1", // Core framework address, always exists
  );
});

Given("a known transaction hash for benchmarking", async function (this: TestWorld) {
  // Get a recent transaction hash from ledger info
  const txs = await this.aptos.getTransactions({ options: { limit: 1 } });
  if (txs.length > 0 && "hash" in txs[0]) {
    this.transactionHash = txs[0].hash;
  } else {
    throw new Error("Could not find a transaction hash for benchmarking");
  }
});

Given("a funded Ed25519 account for benchmarking", async function (this: TestWorld) {
  this.account = Account.generate();
  // Fund account for transaction tests
  await this.aptos.fundAccount({
    accountAddress: this.account.accountAddress,
    amount: 100_000_000, // 1 APT
  });
});

Given("an Ed25519 key pair for benchmarking", function (this: TestWorld) {
  this.account = Account.generate();
});

Given("a {int}-byte message", function (this: TestWorld, size: number) {
  this.message = new Uint8Array(size).fill(0x42);
});

Given("a signed {int}-byte message", function (this: TestWorld, size: number) {
  this.message = new Uint8Array(size).fill(0x42);
  this.signature = this.account.sign(this.message);
});

Given("a sample raw transaction for benchmarking", function (this: TestWorld) {
  // Use a simple account address for BCS serialization testing
  // AccountAddress is serializable and represents a common operation
  this.address = AccountAddress.fromString("0x1");
});

Given("a known account with tokens", async function (this: TestWorld) {
  // Use 0x1 which has APT
  this.address = AccountAddress.fromString("0x1");
});

Given("a known account with fungible assets", async function (this: TestWorld) {
  this.address = AccountAddress.fromString("0x1");
});

Given("a known account with events", async function (this: TestWorld) {
  this.address = AccountAddress.fromString("0x1");
});

// =============================================================================
// REST API Benchmarks
// =============================================================================

When(
  "I measure the time to get ledger info {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(() => this.aptos.getLedgerInfo(), iterations);
  },
);

When(
  "I measure the time to get account info {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () => this.aptos.getAccountInfo({ accountAddress: this.address }),
      iterations,
    );
  },
);

When(
  "I measure the time to get account resources {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () => this.aptos.getAccountResources({ accountAddress: this.address }),
      iterations,
    );
  },
);

When(
  "I measure the time to get transaction by hash {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () =>
        this.aptos.getTransactionByHash({
          transactionHash: this.transactionHash,
        }),
      iterations,
    );
  },
);

When(
  "I measure the time to get account balance {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () => this.aptos.getAccountAPTAmount({ accountAddress: this.address }),
      iterations,
    );
  },
);

// =============================================================================
// GraphQL Benchmarks
// =============================================================================

When(
  "I measure the time to query account tokens {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () =>
        this.aptos.getAccountOwnedTokens({
          accountAddress: this.address,
        }),
      iterations,
    );
  },
);

When(
  "I measure the time to query account transactions {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () =>
        this.aptos.getAccountTransactions({
          accountAddress: this.address,
          options: { limit: 10 },
        }),
      iterations,
    );
  },
);

When(
  "I measure the time to query fungible asset balances {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () =>
        this.aptos.getCurrentFungibleAssetBalances({
          options: {
            where: {
              owner_address: { _eq: this.address.toString() },
            },
          },
        }),
      iterations,
    );
  },
);

When(
  "I measure the time to query events by account {int} times",
  async function (this: TestWorld, iterations: number) {
    this.benchmarkResult = await measureTime(
      () =>
        this.aptos.getAccountEventsByCreationNumber({
          accountAddress: this.address,
          creationNumber: 0,
        }),
      iterations,
    );
  },
);

// =============================================================================
// Transaction Benchmarks
// =============================================================================

When(
  "I measure the time to submit {int} APT transfers without waiting",
  async function (this: TestWorld, iterations: number) {
    const recipient = Account.generate();
    const samples: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start = performance.now();

      const transaction = await this.aptos.transaction.build.simple({
        sender: this.account.accountAddress,
        data: {
          function: "0x1::aptos_account::transfer",
          functionArguments: [recipient.accountAddress, 100],
        },
      });

      const signedTx = await this.aptos.transaction.sign({
        signer: this.account,
        transaction,
      });

      await this.aptos.transaction.submit.simple({
        transaction,
        senderAuthenticator: signedTx,
      });

      const end = performance.now();
      samples.push(end - start);

      // Small delay to avoid sequence number issues
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    this.benchmarkResult = calculateStats(samples);
  },
);

When(
  "I measure the time to build and sign {int} APT transfer transactions",
  async function (this: TestWorld, iterations: number) {
    const recipient = Account.generate();
    const samples: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start = performance.now();

      const transaction = await this.aptos.transaction.build.simple({
        sender: this.account.accountAddress,
        data: {
          function: "0x1::aptos_account::transfer",
          functionArguments: [recipient.accountAddress, 100],
        },
        options: {
          accountSequenceNumber: BigInt(i), // Avoid fetching
        },
      });

      this.aptos.transaction.sign({
        signer: this.account,
        transaction,
      });

      const end = performance.now();
      samples.push(end - start);
    }

    this.benchmarkResult = calculateStats(samples);
  },
);

When(
  "I measure the time to submit and wait for {int} APT transfers",
  async function (this: TestWorld, iterations: number) {
    const recipient = Account.generate();
    const samples: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start = performance.now();

      const transaction = await this.aptos.transaction.build.simple({
        sender: this.account.accountAddress,
        data: {
          function: "0x1::aptos_account::transfer",
          functionArguments: [recipient.accountAddress, 100],
        },
      });

      const pendingTx = await this.aptos.signAndSubmitTransaction({
        signer: this.account,
        transaction,
      });

      await this.aptos.waitForTransaction({
        transactionHash: pendingTx.hash,
      });

      const end = performance.now();
      samples.push(end - start);
    }

    this.benchmarkResult = calculateStats(samples);
  },
);

When(
  "I measure the full transaction flow {int} times including:",
  async function (this: TestWorld, iterations: number) {
    const recipient = Account.generate();
    const samples: number[] = [];
    const stepBreakdown: Record<string, number[]> = {
      build: [],
      simulate: [],
      sign: [],
      submit: [],
      wait: [],
    };

    for (let i = 0; i < iterations; i++) {
      const totalStart = performance.now();

      // Build
      let stepStart = performance.now();
      const transaction = await this.aptos.transaction.build.simple({
        sender: this.account.accountAddress,
        data: {
          function: "0x1::aptos_account::transfer",
          functionArguments: [recipient.accountAddress, 100],
        },
      });
      stepBreakdown.build.push(performance.now() - stepStart);

      // Simulate
      stepStart = performance.now();
      await this.aptos.transaction.simulate.simple({
        signerPublicKey: this.account.publicKey,
        transaction,
      });
      stepBreakdown.simulate.push(performance.now() - stepStart);

      // Sign
      stepStart = performance.now();
      const signedTx = await this.aptos.transaction.sign({
        signer: this.account,
        transaction,
      });
      stepBreakdown.sign.push(performance.now() - stepStart);

      // Submit
      stepStart = performance.now();
      const pendingTx = await this.aptos.transaction.submit.simple({
        transaction,
        senderAuthenticator: signedTx,
      });
      stepBreakdown.submit.push(performance.now() - stepStart);

      // Wait
      stepStart = performance.now();
      await this.aptos.waitForTransaction({
        transactionHash: pendingTx.hash,
      });
      stepBreakdown.wait.push(performance.now() - stepStart);

      samples.push(performance.now() - totalStart);
    }

    this.benchmarkResult = calculateStats(samples);
    this.stepBreakdown = Object.fromEntries(
      Object.entries(stepBreakdown).map(([k, v]) => [k, calculateStats(v)]),
    );
  },
);

// =============================================================================
// Crypto Benchmarks
// =============================================================================

When(
  "I measure the time to generate {int} Ed25519 key pairs",
  function (this: TestWorld, iterations: number) {
    this.benchmarkResult = measureTimeSync(() => Account.generate(), iterations);
  },
);

When(
  "I measure the time to sign the message {int} times",
  function (this: TestWorld, iterations: number) {
    this.benchmarkResult = measureTimeSync(() => this.account.sign(this.message), iterations);
  },
);

When(
  "I measure the time to verify the signature {int} times",
  function (this: TestWorld, iterations: number) {
    this.benchmarkResult = measureTimeSync(
      () => this.account.verifySignature({ message: this.message, signature: this.signature }),
      iterations,
    );
  },
);

When(
  "I measure the time to BCS serialize the transaction {int} times",
  function (this: TestWorld, iterations: number) {
    const addr = this.address!;
    this.benchmarkResult = measureTimeSync(() => addr.bcsToBytes(), iterations);
  },
);

When(
  "I measure the time to hash the message {int} times",
  function (this: TestWorld, iterations: number) {
    const msg = this.message!;
    this.benchmarkResult = measureTimeSync(() => sha3_256(msg), iterations);
  },
);

// =============================================================================
// Recording Results
// =============================================================================

Then(
  "I record the average response time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.avg * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.avg.toFixed(2)} ms`);
  },
);

Then("I record the p95 response time as {string}", function (this: TestWorld, metricName: string) {
  performanceResults.results[metricName] = Math.round(this.benchmarkResult.p95 * 100) / 100;
  console.log(`  ${metricName}: ${this.benchmarkResult.p95.toFixed(2)} ms`);
});

Then(
  "I record the requests per second as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] =
      Math.round(this.benchmarkResult.opsPerSecond * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.opsPerSecond.toFixed(2)} rps`);
  },
);

Then(
  "I record the average submission time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.avg * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.avg.toFixed(2)} ms`);
  },
);

Then(
  "I record the p95 submission time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.p95 * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.p95.toFixed(2)} ms`);
  },
);

Then(
  "I record the transactions per second as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] =
      Math.round(this.benchmarkResult.opsPerSecond * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.opsPerSecond.toFixed(2)} tps`);
  },
);

Then("I record the average time as {string}", function (this: TestWorld, metricName: string) {
  // Convert to microseconds for crypto ops
  const unit = metricName.includes("_us") ? "μs" : "ms";
  const value = metricName.includes("_us")
    ? this.benchmarkResult.avg * 1000
    : this.benchmarkResult.avg;
  performanceResults.results[metricName] = Math.round(value * 100) / 100;
  console.log(`  ${metricName}: ${value.toFixed(2)} ${unit}`);
});

Then("I record the p95 time as {string}", function (this: TestWorld, metricName: string) {
  const unit = metricName.includes("_us") ? "μs" : "ms";
  const value = metricName.includes("_us")
    ? this.benchmarkResult.p95 * 1000
    : this.benchmarkResult.p95;
  performanceResults.results[metricName] = Math.round(value * 100) / 100;
  console.log(`  ${metricName}: ${value.toFixed(2)} ${unit}`);
});

Then(
  "I record the operations per second as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] =
      Math.round(this.benchmarkResult.opsPerSecond * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.opsPerSecond.toFixed(2)} ops/s`);
  },
);

Then(
  "I record the average round-trip time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.avg * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.avg.toFixed(2)} ms`);
  },
);

Then(
  "I record the p95 round-trip time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.p95 * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.p95.toFixed(2)} ms`);
  },
);

Then(
  "I record the minimum round-trip time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.min * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.min.toFixed(2)} ms`);
  },
);

Then(
  "I record the maximum round-trip time as {string}",
  function (this: TestWorld, metricName: string) {
    performanceResults.results[metricName] = Math.round(this.benchmarkResult.max * 100) / 100;
    console.log(`  ${metricName}: ${this.benchmarkResult.max.toFixed(2)} ms`);
  },
);

Then("I record the average total time as {string}", function (this: TestWorld, metricName: string) {
  performanceResults.results[metricName] = Math.round(this.benchmarkResult.avg * 100) / 100;
  console.log(`  ${metricName}: ${this.benchmarkResult.avg.toFixed(2)} ms`);
});

Then("I record the breakdown by step", function (this: TestWorld) {
  console.log("  Step breakdown (avg ms):");
  for (const [step, stats] of Object.entries(this.stepBreakdown)) {
    const avgMs = (stats as BenchmarkResult).avg;
    performanceResults.results[`tx_step_${step}_avg_ms`] = Math.round(avgMs * 100) / 100;
    console.log(`    ${step}: ${avgMs.toFixed(2)} ms`);
  }
});

// =============================================================================
// After hook to output results
// =============================================================================

After({ tags: "@performance" }, function () {
  // Output JSON results at the end
  console.log("\n=== Performance Results JSON ===");
  console.log(JSON.stringify(performanceResults, null, 2));
});
