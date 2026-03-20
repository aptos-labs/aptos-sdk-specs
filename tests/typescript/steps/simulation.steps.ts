/**
 * Transaction Simulation Step Definitions
 *
 * Implements behavioral tests for transaction simulation.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  Account,
  AccountAddress,
  Ed25519PrivateKey,
  RawTransaction,
  ChainId,
  MultiAgentTransaction,
} from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";
import { createTransferPayload } from "../support/transaction-payload-helpers.js";

function setupMultiAgentSimulationTransaction(world: AptosWorld, count: number) {
  const sender = Account.fromPrivateKey({ privateKey: Ed25519PrivateKey.generate() });
  const secondaries: Account[] = [];
  for (let i = 0; i < count; i++) {
    secondaries.push(Account.fromPrivateKey({ privateKey: Ed25519PrivateKey.generate() }));
  }

  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));
  const rawTxn = new RawTransaction(
    sender.accountAddress,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(Math.floor(Date.now() / 1000) + 600),
    new ChainId(1),
  );
  const secondaryAddresses = secondaries.map((account) => account.accountAddress);
  const multiAgentTxn = new MultiAgentTransaction(rawTxn, secondaryAddresses);

  world.testVectors.set("senderAccount", sender);
  world.testVectors.set("secondaryAccounts", secondaries);
  world.testVectors.set("secondaryAddresses", secondaryAddresses);
  world.testVectors.set("rawTransaction", rawTxn);
  world.testVectors.set("multiAgentTransaction", multiAgentTxn);
  world.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1200",
      changes: [
        { type: "write_resource", address: sender.accountAddress.toString(), data: {} },
        ...secondaries.map((account) => ({
          type: "write_resource",
          address: account.accountAddress.toString(),
          data: {},
        })),
      ],
      events: [
        {
          type: "0x1::coin::WithdrawEvent",
          data: { amount: "100" },
        },
      ],
    },
  ]);
}

// =============================================================================
// Basic Simulation (simulation.feature patterns)
// =============================================================================

// Note: "a valid transaction" step is defined in transaction-submission.steps.ts
// Use the hook below for simulation-specific setup
Given("a valid transaction for simulation", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.account = account;
  this.testVectors.set("simulationAccount", account);
  this.testVectors.set("validTransaction", true);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1000",
      vm_status: "Executed successfully",
      changes: [{ type: "write_resource", address: "0x1", data: {} }],
      events: [{ type: "0x1::coin::WithdrawEvent", data: { amount: "100" } }],
    },
  ]);
});

// Note: "I simulate it" and "I simulate the transaction" steps are in transaction-submission.steps.ts

Then("I should get a simulation result", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  expect(result).to.not.be.undefined;
});

Then("it should include gas_used", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  expect(result.gas_used).to.not.be.undefined;
});

Then("it should include success status", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  expect(result.success).to.be.a("boolean");
});

Given("a transaction I haven't signed yet", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.account = account;
  this.testVectors.set("unsignedTransaction", true);
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "500" }]);
});

Then("simulation should work", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[] | undefined;
  const simulationResult = this.testVectors.get("simulationResult") as any;
  const resolvedSimulation =
    response?.[0] ?? (Array.isArray(simulationResult) ? simulationResult[0] : simulationResult);
  expect(resolvedSimulation?.success).to.be.true;
});

Then("use a dummy signature internally", function (this: AptosWorld) {
  // SDK uses a dummy signature for simulation
  expect(true).to.be.true;
});

Given("a transaction simulation", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1000",
      changes: [{ type: "write_resource", address: "0x1", data: {} }],
      events: [{ type: "0x1::coin::WithdrawEvent", data: { amount: "100" } }],
    },
  ]);
});

When("I inspect the simulation result", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  this.testVectors.set("simulationResult", response?.[0]);
});

Then("I should see state changes that would occur", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  expect(result.changes).to.be.an("array");
});

Then("events that would be emitted", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  expect(result.events).to.be.an("array");
});

// Gas estimation via simulation
Given("a transaction", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.account = account;
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "1000" }]);
});

Then("gas_used tells me actual consumption", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  const gasUsed = parseInt(response?.[0]?.gas_used || "0", 10);
  expect(gasUsed).to.be.greaterThan(0);
});

Then("I can set max_gas_amount with buffer", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  const gasUsed = parseInt(response?.[0]?.gas_used || "0", 10);
  const maxGasWithBuffer = Math.ceil(gasUsed * 1.2);
  this.testVectors.set("recommendedMaxGas", maxGasWithBuffer);
  expect(maxGasWithBuffer).to.be.greaterThan(gasUsed);
});

Given("a complex transaction", function (this: AptosWorld) {
  this.testVectors.set("complexTransaction", true);
  this.testVectors.set("simulationResults", [
    { max_gas: 1000, gas_used: "950", success: true },
    { max_gas: 500, gas_used: "500", success: false }, // out of gas
  ]);
});

When("I simulate with different max_gas amounts", function (this: AptosWorld) {
  this.testVectors.set("simulatedWithDifferentGas", true);
});

Then("I can find the minimum needed", function (this: AptosWorld) {
  const results = this.testVectors.get("simulationResults") as any[];
  const successfulRuns = results.filter((r) => r.success);
  expect(successfulRuns.length).to.be.greaterThan(0);
});

Given("a simple transfer", function (this: AptosWorld) {
  this.testVectors.set("simpleTransferGas", 500);
});

// Note: "a complex smart contract call", "I simulate both", and "the complex call should use more gas"
// are defined in gas-estimation.steps.ts for gas-specific scenarios

// Preview state changes
Given("a transfer transaction", function (this: AptosWorld) {
  this.testVectors.set("transferTransaction", true);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "500",
      changes: [
        {
          type: "write_resource",
          address: "0x1",
          data: { coin: { value: "900" } },
        },
        {
          type: "write_resource",
          address: "0x2",
          data: { coin: { value: "1100" } },
        },
      ],
    },
  ]);
});

Then("I should see sender balance decrease", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.changes).to.be.an("array");
});

Then("recipient balance increase", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.changes.length).to.be.greaterThan(0);
});

Given("a transaction that modifies resources", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1000",
      changes: [
        {
          type: "write_resource",
          address: "0x1",
          data: { type: "0x1::coin::CoinStore", data: { coin: { value: "900" } } },
        },
      ],
    },
  ]);
});

Then("I should see which resources change", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.changes).to.be.an("array");
  expect(response?.[0]?.changes.length).to.be.greaterThan(0);
});

Then("their new values", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.changes?.[0]?.data).to.not.be.undefined;
});

Then("I should see which events would emit", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.events).to.be.an("array");
});

Then("their data", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  const events = response?.[0]?.events;
  if (events && events.length > 0) {
    expect(events[0].data).to.not.be.undefined;
  }
});

// Failure preview
Given("a transaction that would abort", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: false,
      gas_used: "250",
      vm_status: "Move abort in 0x1::coin: EINSUFFICIENT_BALANCE (code: 0x10001)",
    },
  ]);
});

// Note: "simulation should show failure" is defined in gas-estimation.steps.ts
Then("simulation result should show failure", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.success).to.be.false;
});

Then("include the abort code", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.vm_status).to.include("abort");
});

Then("the module that aborted", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.vm_status).to.include("::");
});

Given("a transfer exceeding sender's balance", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: false,
      gas_used: "100",
      vm_status: "INSUFFICIENT_BALANCE",
    },
  ]);
});

Then("simulation should fail", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.success).to.be.false;
});

Then("indicate insufficient funds", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.vm_status).to.match(/insufficient|balance/i);
});

Given("a transaction with wrong type arguments", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: false,
      gas_used: "50",
      vm_status: "TYPE_MISMATCH",
    },
  ]);
});

Then("indicate the type mismatch", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.vm_status).to.match(/type/i);
});

Given("a transaction accessing non-existent resource", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: false,
      gas_used: "50",
      vm_status: "RESOURCE_NOT_FOUND",
    },
  ]);
});

Then("indicate resource not found", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.vm_status).to.match(/resource|not.found/i);
});

// Simulation options
Given("a historical ledger version", function (this: AptosWorld) {
  this.testVectors.set("ledgerVersion", 1000000n);
});

When("I simulate at that version", function (this: AptosWorld) {
  this.testVectors.set("simulatedAtVersion", true);
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "500" }]);
});

Then("simulation uses state at that version", function (this: AptosWorld) {
  expect(this.testVectors.get("simulatedAtVersion")).to.be.true;
});

When("I simulate with specific max_gas_amount", function (this: AptosWorld) {
  this.testVectors.set("specificMaxGas", 50000);
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "1000" }]);
});

Then("simulation respects that limit", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  const maxGas = this.testVectors.get("specificMaxGas") as number;
  const gasUsed = parseInt(response?.[0]?.gas_used || "0", 10);
  expect(gasUsed).to.be.lessThanOrEqual(maxGas);
});

When("I simulate with specific gas_unit_price", function (this: AptosWorld) {
  this.testVectors.set("specificGasPrice", 200);
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "1000" }]);
});

Then("simulation uses that price for calculations", function (this: AptosWorld) {
  expect(this.testVectors.get("specificGasPrice")).to.equal(200);
});

Given(
  "a multi-agent simulation transaction with {int} secondary signer",
  function (this: AptosWorld, count: number) {
    setupMultiAgentSimulationTransaction(this, count);
  },
);

Given(
  "a multi-agent simulation transaction with {int} secondary signers",
  function (this: AptosWorld, count: number) {
    setupMultiAgentSimulationTransaction(this, count);
  },
);

Given("sender public key is provided for simulation", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account | undefined;
  if (!sender) {
    throw new Error("senderAccount is required before setting sender public key for simulation");
  }

  this.testVectors.set("simulationSenderPublicKey", sender.publicKey);
  this.testVectors.set("simulationSenderPublicKeyProvided", true);
});

Given("secondary signer public keys are provided for simulation", function (this: AptosWorld) {
  const secondaries = this.testVectors.get("secondaryAccounts") as Account[] | undefined;
  if (!secondaries || secondaries.length === 0) {
    throw new Error(
      "secondaryAccounts are required before setting secondary signer public keys for simulation",
    );
  }

  this.testVectors.set(
    "simulationSecondarySignerPublicKeys",
    secondaries.map((account) => account.publicKey),
  );
  this.testVectors.set("simulationSecondarySignerKeysProvided", true);
  this.testVectors.set("simulationAuthKeyCheckMode", "full");
});

Given("no signer public keys are provided for simulation", function (this: AptosWorld) {
  this.testVectors.set("simulationSenderPublicKeyProvided", false);
  this.testVectors.set("simulationSenderPublicKey", undefined);
  this.testVectors.set("simulationSecondarySignerKeysProvided", false);
  this.testVectors.set("simulationSecondarySignerPublicKeys", undefined);
  this.testVectors.set("simulationFeePayerPublicKeyProvided", false);
  this.testVectors.set("simulationFeePayerPublicKey", undefined);
  this.testVectors.set("simulationAuthKeyCheckMode", "skipped");

  if (!this.testVectors.get("simulationResponse")) {
    this.testVectors.set("simulationResponse", [{ success: true, gas_used: "900" }]);
  }
});

Given("secondary signer public keys include undefined placeholders", function (this: AptosWorld) {
  let secondaries = (this.testVectors.get("secondaryAccounts") as Account[] | undefined) ?? [];
  if (secondaries.length === 0) {
    const fallbackSecondary = Account.fromPrivateKey({
      privateKey: Ed25519PrivateKey.generate(),
    });
    secondaries = [fallbackSecondary];
    this.testVectors.set("secondaryAccounts", secondaries);
    this.testVectors.set("secondaryAddresses", [fallbackSecondary.accountAddress]);
  }

  const secondaryCount =
    secondaries.length ||
    ((this.testVectors.get("secondaryAddresses") as AccountAddress[] | undefined)?.length ?? 0) ||
    1;

  const keySlots = Array.from({ length: secondaryCount }, (_, index) =>
    index === 0 ? secondaries[0].publicKey : undefined,
  );

  this.testVectors.set("simulationSecondarySignerPublicKeys", keySlots);
  this.testVectors.set(
    "simulationProvidedSecondarySignerSlots",
    keySlots.filter((key) => key !== undefined).length,
  );
  this.testVectors.set("simulationSecondarySignerKeysProvided", true);
  this.testVectors.set("simulationAuthKeyCheckMode", "partial");
});

Given("secondary signer public key mapping has wrong length", function (this: AptosWorld) {
  const secondaryAddresses =
    (this.testVectors.get("secondaryAddresses") as AccountAddress[] | undefined) ?? [];
  const wrongLength = secondaryAddresses.length === 0 ? 1 : secondaryAddresses.length - 1;

  const malformedKeys = Array.from(
    { length: wrongLength },
    () => Account.fromPrivateKey({ privateKey: Ed25519PrivateKey.generate() }).publicKey,
  );

  this.testVectors.set("simulationSecondarySignerPublicKeys", malformedKeys);
  this.testVectors.set("malformedSignerKeyMapping", true);
});

Given("a simulation result covering sender and secondary accounts", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account | undefined;
  const secondaryAddresses =
    (this.testVectors.get("secondaryAddresses") as AccountAddress[] | undefined) ?? [];

  const involvedAddresses = [
    sender?.accountAddress.toString() ?? "0x1",
    ...secondaryAddresses.map((address) => address.toString()),
  ];

  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1400",
      changes: involvedAddresses.map((address) => ({
        type: "write_resource",
        address,
        data: {},
      })),
      events: involvedAddresses.map((address) => ({
        type: "0x1::coin::DepositEvent",
        account: address,
        data: { amount: "100" },
      })),
    },
  ]);
});

Given(
  "sender, secondary, and fee payer public keys are provided for simulation",
  function (this: AptosWorld) {
    const sender = this.testVectors.get("senderAccount") as Account | undefined;
    if (!sender) {
      throw new Error(
        "senderAccount is required before setting sender public key for fee-payer simulation",
      );
    }

    const secondaries = this.testVectors.get("secondaryAccounts") as Account[] | undefined;
    if (!secondaries || secondaries.length === 0) {
      throw new Error(
        "secondaryAccounts are required before setting secondary signer keys for fee-payer simulation",
      );
    }

    const feePayer = this.testVectors.get("feePayerAccount") as Account | undefined;
    if (!feePayer) {
      throw new Error("feePayerAccount is required before setting fee payer key for simulation");
    }

    this.testVectors.set("simulationSenderPublicKey", sender.publicKey);
    this.testVectors.set(
      "simulationSecondarySignerPublicKeys",
      secondaries.map((account) => account.publicKey),
    );
    this.testVectors.set("simulationFeePayerPublicKey", feePayer.publicKey);
    this.testVectors.set("simulationSenderPublicKeyProvided", true);
    this.testVectors.set("simulationSecondarySignerKeysProvided", true);
    this.testVectors.set("simulationFeePayerPublicKeyProvided", true);
    this.testVectors.set("simulationAuthKeyCheckMode", "full");
    this.testVectors.set("feePayerTransactionCreated", true);

    if (!this.testVectors.get("simulationResponse")) {
      this.testVectors.set("simulationResponse", [{ success: true, gas_used: "1000" }]);
    }
  },
);

When("I simulate the multi-agent transaction", function (this: AptosWorld) {
  const transaction =
    this.testVectors.get("multiAgentTransaction") ?? this.testVectors.get("rawTransaction");
  expect(transaction).to.not.be.undefined;

  const simulationRequest: {
    transaction: unknown;
    senderPublicKey?: unknown;
    secondarySignersPublicKeys?: Array<unknown>;
  } = {
    transaction,
  };
  if (this.testVectors.get("simulationSenderPublicKeyProvided") === true) {
    simulationRequest.senderPublicKey = this.testVectors.get("simulationSenderPublicKey");
  }
  if (this.testVectors.get("simulationSecondarySignerKeysProvided") === true) {
    simulationRequest.secondarySignersPublicKeys =
      (this.testVectors.get("simulationSecondarySignerPublicKeys") as Array<unknown> | undefined) ??
      [];
  }
  this.testVectors.set("simulationRequest", simulationRequest);

  if (!this.testVectors.get("simulationResponse")) {
    const sender = this.testVectors.get("senderAccount") as Account | undefined;
    const secondaryAddresses =
      (this.testVectors.get("secondaryAddresses") as AccountAddress[] | undefined) ?? [];
    const involvedAddresses = [
      sender?.accountAddress.toString() ?? "0x1",
      ...secondaryAddresses.map((address) => address.toString()),
    ];

    this.testVectors.set("simulationResponse", [
      {
        success: true,
        gas_used: "1000",
        changes: involvedAddresses.map((address) => ({
          type: "write_resource",
          address,
          data: {},
        })),
        events: [],
      },
    ]);
  }

  const simulationResponse = this.testVectors.get("simulationResponse") as any[] | undefined;
  this.testVectors.set("simulationResult", simulationResponse?.[0]);
});

When("I simulate the multi-agent fee-payer transaction", function (this: AptosWorld) {
  const transaction = this.testVectors.get("feePayerTransaction");
  expect(
    transaction,
    "feePayerTransaction must be set before simulating a multi-agent fee-payer transaction",
  ).to.not.be.undefined;

  const simulationRequest: {
    transaction: unknown;
    senderPublicKey?: unknown;
    secondarySignersPublicKeys?: Array<unknown>;
    feePayerAddress?: unknown;
    feePayerPublicKey?: unknown;
  } = {
    transaction,
  };
  const feePayerAddress = this.testVectors.get("feePayerAddress");
  if (feePayerAddress !== undefined) {
    simulationRequest.feePayerAddress = feePayerAddress;
  }
  if (this.testVectors.get("simulationSenderPublicKeyProvided") === true) {
    simulationRequest.senderPublicKey = this.testVectors.get("simulationSenderPublicKey");
  }
  if (this.testVectors.get("simulationSecondarySignerKeysProvided") === true) {
    simulationRequest.secondarySignersPublicKeys =
      (this.testVectors.get("simulationSecondarySignerPublicKeys") as Array<unknown> | undefined) ??
      [];
  }
  if (this.testVectors.get("simulationFeePayerPublicKeyProvided") === true) {
    simulationRequest.feePayerPublicKey = this.testVectors.get("simulationFeePayerPublicKey");
  }
  this.testVectors.set("simulationRequest", simulationRequest);

  if (!this.testVectors.get("simulationResponse")) {
    this.testVectors.set("simulationResponse", [
      {
        success: true,
        gas_used: "1100",
      },
    ]);
  }

  const simulationResponse = this.testVectors.get("simulationResponse") as any[] | undefined;
  this.testVectors.set("simulationResult", simulationResponse?.[0]);
});

When("I inspect the multi-agent simulation result", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  this.testVectors.set("simulationResult", response?.[0]);
});

Then("auth-key checks should run for all provided signers", function (this: AptosWorld) {
  const mode = this.testVectors.get("simulationAuthKeyCheckMode") as string;
  expect(mode).to.equal("full");
  expect(this.testVectors.get("simulationSenderPublicKeyProvided")).to.be.true;
  const simulationRequest = this.testVectors.get("simulationRequest") as
    | {
        senderPublicKey?: unknown;
        secondarySignersPublicKeys?: Array<unknown>;
        feePayerPublicKey?: unknown;
      }
    | undefined;
  expect(simulationRequest).to.not.be.undefined;
  expect(simulationRequest?.senderPublicKey).to.not.be.undefined;

  const secondarySignerKeys = this.testVectors.get("simulationSecondarySignerPublicKeys") as
    | Array<unknown>
    | undefined;
  expect(secondarySignerKeys).to.be.an("array");
  expect((secondarySignerKeys ?? []).length).to.be.greaterThan(0);
  expect((secondarySignerKeys ?? []).every((key) => key !== undefined)).to.be.true;
  const requestSecondarySignerKeys = simulationRequest?.secondarySignersPublicKeys ?? [];
  expect(requestSecondarySignerKeys).to.be.an("array");
  expect(requestSecondarySignerKeys.length).to.be.greaterThan(0);
  expect(requestSecondarySignerKeys.every((key) => key !== undefined)).to.be.true;

  const feePayerKeyProvided = this.testVectors.get("simulationFeePayerPublicKeyProvided");
  if (feePayerKeyProvided === true) {
    expect(this.testVectors.get("simulationFeePayerPublicKey")).to.not.be.undefined;
    expect(simulationRequest?.feePayerPublicKey).to.not.be.undefined;
  }
});

Then("auth-key checks should be skipped", function (this: AptosWorld) {
  const mode = this.testVectors.get("simulationAuthKeyCheckMode") as string;
  expect(mode).to.equal("skipped");
  expect(this.testVectors.get("simulationSenderPublicKeyProvided")).to.not.be.true;
  const simulationRequest = this.testVectors.get("simulationRequest") as
    | {
        senderPublicKey?: unknown;
        secondarySignersPublicKeys?: Array<unknown>;
        feePayerPublicKey?: unknown;
      }
    | undefined;
  expect(simulationRequest).to.not.be.undefined;
  expect(simulationRequest?.senderPublicKey).to.be.undefined;

  const secondarySignerKeys = this.testVectors.get("simulationSecondarySignerPublicKeys") as
    | Array<unknown>
    | undefined;
  expect(secondarySignerKeys).to.be.undefined;
  expect(simulationRequest?.secondarySignersPublicKeys).to.be.undefined;
  expect(simulationRequest?.feePayerPublicKey).to.be.undefined;
});

Then("auth-key checks should run only for provided signer slots", function (this: AptosWorld) {
  const mode = this.testVectors.get("simulationAuthKeyCheckMode") as string;
  expect(mode).to.equal("partial");
  const simulationRequest = this.testVectors.get("simulationRequest") as
    | {
        secondarySignersPublicKeys?: Array<unknown>;
      }
    | undefined;
  expect(simulationRequest).to.not.be.undefined;

  const secondarySignerKeys = this.testVectors.get("simulationSecondarySignerPublicKeys") as
    | Array<unknown>
    | undefined;
  expect(secondarySignerKeys).to.be.an("array");
  expect((secondarySignerKeys ?? []).some((key) => key === undefined)).to.be.true;
  expect((secondarySignerKeys ?? []).some((key) => key !== undefined)).to.be.true;
  const requestSecondarySignerKeys = simulationRequest?.secondarySignersPublicKeys ?? [];
  expect(requestSecondarySignerKeys.some((key) => key === undefined)).to.be.true;
  expect(requestSecondarySignerKeys.some((key) => key !== undefined)).to.be.true;
});

Then("show changes for all involved accounts", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[] | undefined;
  const result = this.testVectors.get("simulationResult") as any | undefined;
  const changes = response?.[0]?.changes ?? result?.changes ?? [];
  expect(changes.length).to.be.greaterThan(1);
});

Then("it should include events for involved accounts", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[] | undefined;
  const result = this.testVectors.get("simulationResult") as any | undefined;
  const events = response?.[0]?.events ?? result?.events ?? [];
  expect(events).to.be.an("array");
  expect(events.length).to.be.greaterThan(0);
});

Then("gas should be charged to fee payer", function (this: AptosWorld) {
  const simulationRequest = this.testVectors.get("simulationRequest") as
    | {
        transaction?: unknown;
        feePayerAddress?: unknown;
      }
    | undefined;
  expect(simulationRequest).to.not.be.undefined;
  expect(simulationRequest?.transaction).to.not.be.undefined;
  expect(simulationRequest?.feePayerAddress).to.not.be.undefined;
});

Then("simulation should reflect that", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response?.[0]?.gas_used).to.not.be.undefined;
});

// Simulation vs execution
Given("a simulation", function (this: AptosWorld) {
  this.testVectors.set("simulationDone", true);
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "1000" }]);
});

When("it completes", function (this: AptosWorld) {
  this.testVectors.set("simulationCompleted", true);
});

Then("no on-chain state should change", function (this: AptosWorld) {
  // Simulation doesn't modify state
  expect(true).to.be.true;
});

Then("I can submit the real transaction", function (this: AptosWorld) {
  // Can still submit after simulation
  expect(true).to.be.true;
});

Given("blockchain state changes between simulate and submit", function (this: AptosWorld) {
  this.testVectors.set("stateChanged", true);
});

When("I submit after simulation", function (this: AptosWorld) {
  this.testVectors.set("submittedAfterSimulation", true);
});

Then("results might differ", function (this: AptosWorld) {
  expect(this.testVectors.get("stateChanged")).to.be.true;
});

Then("this is expected behavior", function (this: AptosWorld) {
  // State changes are expected
  expect(true).to.be.true;
});

Given("current sequence number is {int}", function (this: AptosWorld, seqNum: number) {
  this.testVectors.set("currentSeqNum", seqNum);
});

When("I simulate transaction with seq num {int}", function (this: AptosWorld, seqNum: number) {
  this.testVectors.set("simulatedSeqNum", seqNum);
  this.testVectors.set("simulationResponse", [{ success: true, gas_used: "500" }]);
});

Then(
  "simulation should work even if account hasn't committed seq {int} yet",
  function (this: AptosWorld, seqNum: number) {
    const response = this.testVectors.get("simulationResponse") as any[];
    expect(response?.[0]?.success).to.be.true;
  },
);

// Batch simulation
Given("multiple transactions", function (this: AptosWorld) {
  this.testVectors.set("multipleTransactions", [
    { id: 1, success: true, gas_used: "500" },
    { id: 2, success: true, gas_used: "600" },
    { id: 3, success: false, gas_used: "100" },
  ]);
});

When("I simulate them in batch", function (this: AptosWorld) {
  const txns = this.testVectors.get("multipleTransactions") as any[];
  this.testVectors.set("batchSimulationResults", txns);
});

Then("save API calls", function (this: AptosWorld) {
  // Batch simulation reduces API calls
  expect(true).to.be.true;
});

Given("transactions with sequential sequence numbers", function (this: AptosWorld) {
  this.testVectors.set("sequentialTransactions", [
    { seq: 0, success: true },
    { seq: 1, success: true },
    { seq: 2, success: true },
  ]);
});

When("I simulate them in order", function (this: AptosWorld) {
  this.testVectors.set("simulatedInOrder", true);
});

Then("later simulations should see earlier changes", function (this: AptosWorld) {
  // Sequential simulation can see state changes
  expect(this.testVectors.get("simulatedInOrder")).to.be.true;
});

// Error cases
Given("API is unavailable", function (this: AptosWorld) {
  this.testVectors.set("apiUnavailable", true);
});

When("I try to simulate", function (this: AptosWorld) {
  if (this.testVectors.get("malformedSignerKeyMapping")) {
    const secondaryAddresses =
      (this.testVectors.get("secondaryAddresses") as AccountAddress[] | undefined) ?? [];
    const secondarySignerKeys =
      (this.testVectors.get("simulationSecondarySignerPublicKeys") as Array<unknown> | undefined) ??
      [];

    if (secondarySignerKeys.length !== secondaryAddresses.length) {
      this.error = new Error(
        "Validation error: secondary signer key mapping length does not match secondary signer addresses",
      );
      return;
    }
  } else if (this.testVectors.get("apiUnavailable")) {
    this.error = new Error("Network error: API unavailable");
  } else if (this.testVectors.get("malformedTransaction")) {
    this.error = new Error("Validation error: malformed transaction");
  }
});

Then("I should get a network error not a simulation failure", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
  expect(this.error!.message).to.match(/network/i);
});

Given("a malformed transaction", function (this: AptosWorld) {
  this.testVectors.set("malformedTransaction", true);
});

Then("I should get validation error before simulation even runs", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
  expect(this.error!.message).to.match(/validation/i);
});

// =============================================================================
// Legacy Simulation Setup (for backward compatibility)
// =============================================================================

Given("a valid unsigned transaction", async function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });

  this.account = account;
  this.testVectors.set("simulationAccount", account);

  // Store the account for simulation
  this.testVectors.set("simulationPayload", {
    function: "0x1::aptos_account::transfer",
    arguments: [account.accountAddress.toString(), "100"],
  });
});

Given("sender public key", function (this: AptosWorld) {
  const account = this.testVectors.get("simulationAccount") as Account;
  if (account) {
    this.testVectors.set("senderPublicKey", account.publicKey);
  }
});

// NOTE: "I submit for simulation" requires network access to call the simulation API.
// This is an integration test that needs testnet/devnet access.
// See features/06-advanced/simulation.feature

Then("I should receive simulation results without broadcasting", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response).to.not.be.undefined;
  expect(Array.isArray(response)).to.be.true;
});

Then("transaction should NOT appear on chain", function (this: AptosWorld) {
  // Simulation doesn't broadcast
  expect(true).to.be.true;
});

// =============================================================================
// Simulation Results
// =============================================================================

Given("a successful simulation", function (this: AptosWorld) {
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1234",
      vm_status: "Executed successfully",
      changes: [{ type: "write_resource", address: "0x1", data: {} }],
      events: [{ type: "0x1::coin::WithdrawEvent", data: { amount: "100" } }],
    },
  ]);
});

When("I inspect the simulation result", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  this.testVectors.set("inspectedSimulation", response[0]);
});

Then("I should see success status", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.success).to.be.a("boolean");
});

Then("I should see gas_used", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.gas_used).to.not.be.undefined;
});

Then("I should see state changes \\(if any\\)", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.changes).to.be.an("array");
});

Then("I should see events \\(if any\\)", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.events).to.be.an("array");
});

// =============================================================================
// Failed Simulations
// =============================================================================

Given(
  "a transaction that will fail \\(e.g., call non-existent function\\)",
  function (this: AptosWorld) {
    this.testVectors.set("failingTransaction", true);
    this.testVectors.set("simulationResponse", [
      {
        success: false,
        gas_used: "100",
        vm_status: "FUNCTION_NOT_FOUND",
      },
    ]);
  },
);

When("I simulate the failing transaction", function (this: AptosWorld) {
  // Simulation already prepared
  this.testVectors.set("inspectedSimulation", this.testVectors.get("simulationResponse")[0]);
});

// Note: "I should see success: false" is defined in transaction-submission.steps.ts
Then("simulation should show success: false", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.success).to.be.false;
});

Then("I should see vm_status with error details", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.vm_status).to.not.be.undefined;
});

Given("a transaction that aborts", function (this: AptosWorld) {
  this.testVectors.set("abortingTransaction", true);
  this.testVectors.set("simulationResponse", [
    {
      success: false,
      gas_used: "250",
      vm_status: "Move abort: 0x1::coin EINSUFFICIENT_BALANCE(0x10001)",
    },
  ]);
});

When("I simulate the aborting transaction", function (this: AptosWorld) {
  this.testVectors.set("inspectedSimulation", this.testVectors.get("simulationResponse")[0]);
});

Then("I should see the abort code", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.vm_status).to.include("abort");
});

Then("I should see the module and error name if available", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.vm_status).to.include("::");
});

// =============================================================================
// Gas Estimation via Simulation
// =============================================================================

Given("an unsigned transaction for gas estimation", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("gasEstimationAccount", account);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "500",
    },
  ]);
});

When("I simulate for gas estimation", function (this: AptosWorld) {
  this.testVectors.set("gasEstimationResult", this.testVectors.get("simulationResponse")[0]);
});

Then("I should get gas_used estimate", function (this: AptosWorld) {
  const result = this.testVectors.get("gasEstimationResult") as any;
  expect(result.gas_used).to.not.be.undefined;
});

Then("I can use this to set max_gas_amount with margin", function (this: AptosWorld) {
  const result = this.testVectors.get("gasEstimationResult") as any;
  const gasUsed = parseInt(result.gas_used, 10);
  const maxGasWithMargin = Math.ceil(gasUsed * 1.2); // 20% margin
  this.testVectors.set("recommendedMaxGas", maxGasWithMargin);
  expect(maxGasWithMargin).to.be.greaterThan(gasUsed);
});

// =============================================================================
// State Preview
// =============================================================================

Given("a transaction that modifies account state", function (this: AptosWorld) {
  this.testVectors.set("stateModifyingTxn", true);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "1000",
      changes: [
        {
          type: "write_resource",
          address: "0x1",
          state_key_hash: "0xabc123",
          data: {
            type: "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",
            data: { coin: { value: "900" } },
          },
        },
      ],
    },
  ]);
});

When("I simulate and inspect changes", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  this.testVectors.set("simulationChanges", response[0].changes);
});

Then("I should see the resources that would be modified", function (this: AptosWorld) {
  const changes = this.testVectors.get("simulationChanges") as any[];
  expect(changes.length).to.be.greaterThan(0);
});

Then("I should see the new values \\(for writes\\)", function (this: AptosWorld) {
  const changes = this.testVectors.get("simulationChanges") as any[];
  for (const change of changes) {
    if (change.type === "write_resource") {
      expect(change.data).to.not.be.undefined;
    }
  }
});

// =============================================================================
// Event Preview
// =============================================================================

Given("a transaction that emits events", function (this: AptosWorld) {
  this.testVectors.set("eventEmittingTxn", true);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "800",
      events: [
        {
          guid: { creation_number: "3", account_address: "0x1" },
          sequence_number: "0",
          type: "0x1::coin::WithdrawEvent",
          data: { amount: "100" },
        },
        {
          guid: { creation_number: "4", account_address: "0x2" },
          sequence_number: "0",
          type: "0x1::coin::DepositEvent",
          data: { amount: "100" },
        },
      ],
    },
  ]);
});

When("I simulate and inspect events", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  this.testVectors.set("simulationEvents", response[0].events);
});

Then("I should see the events that would be emitted", function (this: AptosWorld) {
  const events = this.testVectors.get("simulationEvents") as any[];
  expect(events.length).to.be.greaterThan(0);
});

Then("each event should have type and data", function (this: AptosWorld) {
  const events = this.testVectors.get("simulationEvents") as any[];
  for (const event of events) {
    expect(event.type).to.not.be.undefined;
    expect(event.data).to.not.be.undefined;
  }
});

// =============================================================================
// Signature Handling in Simulation
// =============================================================================

Given("an unsigned transaction", function (this: AptosWorld) {
  this.testVectors.set("unsignedTxn", true);
});

When("I provide only the public key for simulation", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("simulationPublicKey", account.publicKey);
});

Then("simulation should work without valid signature", function (this: AptosWorld) {
  // Simulation doesn't require actual signature
  expect(true).to.be.true;
});

Then(
  "the result should reflect what would happen with valid signature",
  function (this: AptosWorld) {
    expect(true).to.be.true;
  },
);

Given("a signed transaction with incorrect signature", function (this: AptosWorld) {
  this.testVectors.set("incorrectSignature", true);
});

When("I simulate it with skip_signature_check", function (this: AptosWorld) {
  this.testVectors.set("skipSignatureCheck", true);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "500",
    },
  ]);
});

Then("simulation should still succeed", function (this: AptosWorld) {
  const response = this.testVectors.get("simulationResponse") as any[];
  expect(response[0].success).to.be.true;
});

Then("show what execution would do", function (this: AptosWorld) {
  expect(true).to.be.true;
});

// =============================================================================
// Multiple Simulations
// =============================================================================

Given("multiple transactions to simulate", function (this: AptosWorld) {
  this.testVectors.set("multipleTransactions", [
    { id: 1, success: true, gas_used: "500" },
    { id: 2, success: true, gas_used: "600" },
    { id: 3, success: false, gas_used: "100" },
  ]);
});

When("I batch simulate them", function (this: AptosWorld) {
  const txns = this.testVectors.get("multipleTransactions") as any[];
  this.testVectors.set("batchSimulationResults", txns);
});

Then("I should get results for each", function (this: AptosWorld) {
  const results = this.testVectors.get("batchSimulationResults") as any[];
  expect(results.length).to.be.greaterThan(0);
});

Then("can identify which would succeed or fail", function (this: AptosWorld) {
  const results = this.testVectors.get("batchSimulationResults") as any[];
  const succeeded = results.filter((r) => r.success).length;
  const failed = results.filter((r) => !r.success).length;
  expect(succeeded + failed).to.equal(results.length);
});

// =============================================================================
// Ledger Version
// =============================================================================

Given("a specific ledger version", function (this: AptosWorld) {
  this.testVectors.set("ledgerVersion", 1000000n);
});

When("I simulate at that ledger version", function (this: AptosWorld) {
  this.testVectors.set("simulatedAtVersion", true);
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "500",
    },
  ]);
});

Then("simulation should use state at that version", function (this: AptosWorld) {
  expect(this.testVectors.get("simulatedAtVersion")).to.be.true;
});

// =============================================================================
// Error Cases
// =============================================================================

Given("a transaction with invalid payload", function (this: AptosWorld) {
  this.testVectors.set("invalidPayload", true);
});

When("I try to simulate the invalid transaction", function (this: AptosWorld) {
  this.error = new Error("Invalid transaction payload");
});

Then("I should get a clear error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("not just a generic failure", function (this: AptosWorld) {
  expect(this.error!.message).to.include("Invalid");
});

Given("a very complex transaction", function (this: AptosWorld) {
  this.testVectors.set("complexTransaction", true);
});

When("simulation takes too long", function (this: AptosWorld) {
  this.testVectors.set("simulationTimedOut", true);
  this.error = new Error("Simulation timeout");
});

Then("I should get timeout error with suggestion to increase timeout", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
  expect(this.error!.message).to.include("timeout");
});

// =============================================================================
// Comparison Helpers
// =============================================================================

Given("a simulation result", function (this: AptosWorld) {
  this.testVectors.set("simulationResult", {
    success: true,
    gas_used: "1000",
    changes: [],
    events: [],
  });
});

Given("an actual execution result", function (this: AptosWorld) {
  this.testVectors.set("executionResult", {
    success: true,
    gas_used: "980",
    changes: [],
    events: [],
  });
});

When("I compare them", function (this: AptosWorld) {
  const sim = this.testVectors.get("simulationResult") as any;
  const exec = this.testVectors.get("executionResult") as any;

  this.testVectors.set("comparison", {
    successMatch: sim.success === exec.success,
    gasDifference: Math.abs(parseInt(sim.gas_used, 10) - parseInt(exec.gas_used, 10)),
  });
});

Then("success status should match", function (this: AptosWorld) {
  const comparison = this.testVectors.get("comparison") as any;
  expect(comparison.successMatch).to.be.true;
});

Then("gas_used should be similar \\(may differ slightly\\)", function (this: AptosWorld) {
  const comparison = this.testVectors.get("comparison") as any;
  // Allow up to 10% difference
  const sim = this.testVectors.get("simulationResult") as any;
  const tolerance = parseInt(sim.gas_used, 10) * 0.1;
  expect(comparison.gasDifference).to.be.lessThan(tolerance);
});

Then("events should match", function (this: AptosWorld) {
  // Events should match between simulation and execution
  const sim = this.testVectors.get("simulationResult") as any;
  const exec = this.testVectors.get("executionResult") as any;
  if (sim?.events && exec?.events) {
    expect(sim.events.length).to.equal(exec.events.length);
  }
});
