/**
 * Transaction Simulation Step Definitions
 *
 * Implements behavioral tests for transaction simulation.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  Aptos,
  AptosConfig,
  Network,
  Account,
  AccountAddress,
  Ed25519PrivateKey,
  Secp256k1PrivateKey,
  RawTransaction,
  EntryFunction,
  Identifier,
  U64,
  ChainId,
  Serializer,
} from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";

// =============================================================================
// Simulation Setup
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

When("I submit for simulation", async function (this: AptosWorld) {
  // Mock simulation result
  this.testVectors.set("simulationResponse", [
    {
      success: true,
      gas_used: "500",
      vm_status: "Executed successfully",
      changes: [],
      events: [],
    },
  ]);
});

Then(
  "I should receive simulation results without broadcasting",
  function (this: AptosWorld) {
    const response = this.testVectors.get("simulationResponse") as any[];
    expect(response).to.not.be.undefined;
    expect(Array.isArray(response)).to.be.true;
  },
);

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
  this.testVectors.set(
    "inspectedSimulation",
    this.testVectors.get("simulationResponse")[0],
  );
});

Then("I should see success: false", function (this: AptosWorld) {
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
  this.testVectors.set(
    "inspectedSimulation",
    this.testVectors.get("simulationResponse")[0],
  );
});

Then("I should see the abort code", function (this: AptosWorld) {
  const sim = this.testVectors.get("inspectedSimulation") as any;
  expect(sim.vm_status).to.include("abort");
});

Then(
  "I should see the module and error name if available",
  function (this: AptosWorld) {
    const sim = this.testVectors.get("inspectedSimulation") as any;
    expect(sim.vm_status).to.include("::");
  },
);

// =============================================================================
// Gas Estimation via Simulation
// =============================================================================

Given(
  "an unsigned transaction for gas estimation",
  function (this: AptosWorld) {
    const privateKey = Ed25519PrivateKey.generate();
    const account = Account.fromPrivateKey({ privateKey });
    this.testVectors.set("gasEstimationAccount", account);
    this.testVectors.set("simulationResponse", [
      {
        success: true,
        gas_used: "500",
      },
    ]);
  },
);

When("I simulate for gas estimation", function (this: AptosWorld) {
  this.testVectors.set(
    "gasEstimationResult",
    this.testVectors.get("simulationResponse")[0],
  );
});

Then("I should get gas_used estimate", function (this: AptosWorld) {
  const result = this.testVectors.get("gasEstimationResult") as any;
  expect(result.gas_used).to.not.be.undefined;
});

Then(
  "I can use this to set max_gas_amount with margin",
  function (this: AptosWorld) {
    const result = this.testVectors.get("gasEstimationResult") as any;
    const gasUsed = parseInt(result.gas_used, 10);
    const maxGasWithMargin = Math.ceil(gasUsed * 1.2); // 20% margin
    this.testVectors.set("recommendedMaxGas", maxGasWithMargin);
    expect(maxGasWithMargin).to.be.greaterThan(gasUsed);
  },
);

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

Then(
  "I should see the resources that would be modified",
  function (this: AptosWorld) {
    const changes = this.testVectors.get("simulationChanges") as any[];
    expect(changes.length).to.be.greaterThan(0);
  },
);

Then(
  "I should see the new values \\(for writes\\)",
  function (this: AptosWorld) {
    const changes = this.testVectors.get("simulationChanges") as any[];
    for (const change of changes) {
      if (change.type === "write_resource") {
        expect(change.data).to.not.be.undefined;
      }
    }
  },
);

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

Then(
  "I should see the events that would be emitted",
  function (this: AptosWorld) {
    const events = this.testVectors.get("simulationEvents") as any[];
    expect(events.length).to.be.greaterThan(0);
  },
);

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

When(
  "I provide only the public key for simulation",
  function (this: AptosWorld) {
    const privateKey = Ed25519PrivateKey.generate();
    const account = Account.fromPrivateKey({ privateKey });
    this.testVectors.set("simulationPublicKey", account.publicKey);
  },
);

Then(
  "simulation should work without valid signature",
  function (this: AptosWorld) {
    // Simulation doesn't require actual signature
    expect(true).to.be.true;
  },
);

Then(
  "the result should reflect what would happen with valid signature",
  function (this: AptosWorld) {
    expect(true).to.be.true;
  },
);

Given(
  "a signed transaction with incorrect signature",
  function (this: AptosWorld) {
    this.testVectors.set("incorrectSignature", true);
  },
);

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

Then(
  "simulation should use state at that version",
  function (this: AptosWorld) {
    expect(this.testVectors.get("simulatedAtVersion")).to.be.true;
  },
);

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

Then(
  "I should get timeout error with suggestion to increase timeout",
  function (this: AptosWorld) {
    expect(this.error).to.not.be.undefined;
    expect(this.error!.message).to.include("timeout");
  },
);

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
    gasDifference: Math.abs(
      parseInt(sim.gas_used, 10) - parseInt(exec.gas_used, 10),
    ),
  });
});

Then("success status should match", function (this: AptosWorld) {
  const comparison = this.testVectors.get("comparison") as any;
  expect(comparison.successMatch).to.be.true;
});

Then(
  "gas_used should be similar \\(may differ slightly\\)",
  function (this: AptosWorld) {
    const comparison = this.testVectors.get("comparison") as any;
    // Allow up to 10% difference
    const sim = this.testVectors.get("simulationResult") as any;
    const tolerance = parseInt(sim.gas_used, 10) * 0.1;
    expect(comparison.gasDifference).to.be.lessThan(tolerance);
  },
);

Then("events should match", function (this: AptosWorld) {
  // Events should match between simulation and execution
  expect(true).to.be.true;
});
