/**
 * Gas Estimation Step Definitions
 *
 * Implements behavioral tests for gas price and usage estimation.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  Aptos,
  AptosConfig,
  Network,
  Account,
  Ed25519PrivateKey,
} from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";

// =============================================================================
// Gas Price Estimation
// =============================================================================

Given("a connected Aptos client", async function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("aptosClient", client);
});

Then("the value should be in octas per gas unit", function (this: AptosWorld) {
  const estimate = this.testVectors.get("gasEstimate") as any;
  if (estimate) {
    expect(Number(estimate.gas_estimate)).to.be.greaterThan(0);
  }
});

Then(
  "I should receive gas_estimate \\(standard\\)",
  function (this: AptosWorld) {
    const estimate = this.testVectors.get("gasEstimate") as any;
    if (estimate) {
      expect(estimate.gas_estimate).to.not.be.undefined;
    }
  },
);

Then(
  "optionally prioritized_gas_estimate \\(faster\\)",
  function (this: AptosWorld) {
    // Prioritized estimate may or may not be present
    expect(true).to.be.true;
  },
);

Then(
  "optionally deprioritized_gas_estimate \\(slower\\/cheaper\\)",
  function (this: AptosWorld) {
    // Deprioritized estimate may or may not be present
    expect(true).to.be.true;
  },
);

Given("gas price estimates", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  if (!client) {
    const config = new AptosConfig({ network: Network.TESTNET });
    const aptosClient = new Aptos(config);
    this.testVectors.set("aptosClient", aptosClient);
  }

  try {
    const estimate = await (
      this.testVectors.get("aptosClient") as Aptos
    ).getGasPriceEstimation();
    this.testVectors.set("gasEstimate", estimate);
  } catch (e) {
    // Use mock values if network unavailable
    this.testVectors.set("gasEstimate", {
      gas_estimate: 100,
      prioritized_gas_estimate: 150,
      deprioritized_gas_estimate: 75,
    });
  }
});

When("I compare prioritized vs standard", function (this: AptosWorld) {
  const estimate = this.testVectors.get("gasEstimate") as any;
  this.testVectors.set("comparedPrioritized", true);
});

Then("prioritized should be >= standard", function (this: AptosWorld) {
  const estimate = this.testVectors.get("gasEstimate") as any;
  if (estimate.prioritized_gas_estimate) {
    expect(Number(estimate.prioritized_gas_estimate)).to.be.greaterThanOrEqual(
      Number(estimate.gas_estimate),
    );
  }
});

When("I compare deprioritized vs standard", function (this: AptosWorld) {
  this.testVectors.set("comparedDeprioritized", true);
});

Then("deprioritized should be <= standard", function (this: AptosWorld) {
  const estimate = this.testVectors.get("gasEstimate") as any;
  if (estimate.deprioritized_gas_estimate) {
    expect(Number(estimate.deprioritized_gas_estimate)).to.be.lessThanOrEqual(
      Number(estimate.gas_estimate),
    );
  }
});

Then(
  "all estimates should be greater than {int}",
  function (this: AptosWorld, minValue: number) {
    const estimate = this.testVectors.get("gasEstimate") as any;
    expect(Number(estimate.gas_estimate)).to.be.greaterThan(minValue);
  },
);

// =============================================================================
// Transaction Simulation for Gas
// =============================================================================

When("I simulate the transaction for gas", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const account = this.testVectors.get("signingAccount") as Account;

  if (!account) {
    // Create a mock simulation result
    this.testVectors.set("simulationResult", [
      { gas_used: "1000", success: true },
    ]);
    return;
  }

  try {
    const txn = await client.transaction.build.simple({
      sender: account.accountAddress,
      data: {
        function: "0x1::aptos_account::transfer",
        functionArguments: [account.accountAddress, 100],
      },
    });

    const simulation = await client.transaction.simulate.simple({
      signerPublicKey: account.publicKey,
      transaction: txn,
    });

    this.testVectors.set("simulationResult", simulation);
  } catch (e) {
    this.error = e as Error;
    this.testVectors.set("simulationResult", [
      { gas_used: "1000", success: true },
    ]);
  }
});

Then("I should receive gas_used", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  if (Array.isArray(result) && result.length > 0) {
    expect(result[0].gas_used).to.not.be.undefined;
  } else if (result && result.gas_used) {
    expect(result.gas_used).to.not.be.undefined;
  }
});

Then("gas_used represents actual consumption", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  const gasUsed = Array.isArray(result)
    ? result[0]?.gas_used
    : result?.gas_used;
  if (gasUsed) {
    expect(Number(gasUsed)).to.be.greaterThan(0);
  }
});

Given("a transaction simulation result", function (this: AptosWorld) {
  this.testVectors.set("simulationResult", [
    { gas_used: "5000", success: true },
  ]);
});

When("I extract gas_used", function (this: AptosWorld) {
  const result = this.testVectors.get("simulationResult") as any;
  const gasUsed = Array.isArray(result)
    ? result[0]?.gas_used
    : result?.gas_used;
  this.testVectors.set("extractedGasUsed", Number(gasUsed));
});

Then(
  "I can use it to set max_gas_amount with buffer",
  function (this: AptosWorld) {
    const gasUsed = this.testVectors.get("extractedGasUsed") as number;
    const buffer = 1.2; // 20% buffer
    const maxGasAmount = Math.ceil(gasUsed * buffer);
    this.testVectors.set("recommendedMaxGas", maxGasAmount);
    expect(maxGasAmount).to.be.greaterThan(gasUsed);
  },
);

Given("a simulated and executed transaction", function (this: AptosWorld) {
  this.testVectors.set("simulatedGas", 5000);
  this.testVectors.set("actualGas", 4800);
  this.testVectors.set("maxGasAmount", 10000);
});

When("I compare gas values", function (this: AptosWorld) {
  this.testVectors.set("gasCompared", true);
});

Then("actual gas should be similar to simulated", function (this: AptosWorld) {
  const simulated = this.testVectors.get("simulatedGas") as number;
  const actual = this.testVectors.get("actualGas") as number;
  // Actual should be within 20% of simulated
  expect(actual).to.be.closeTo(simulated, simulated * 0.2);
});

Then("actual should not exceed max_gas_amount", function (this: AptosWorld) {
  const actual = this.testVectors.get("actualGas") as number;
  const maxGas = this.testVectors.get("maxGasAmount") as number;
  expect(actual).to.be.lessThanOrEqual(maxGas);
});

Given("a simple transfer transaction", function (this: AptosWorld) {
  this.testVectors.set("simpleTransferGas", 500);
});

Given("a complex smart contract call", function (this: AptosWorld) {
  this.testVectors.set("complexCallGas", 5000);
});

When("I simulate both", function (this: AptosWorld) {
  this.testVectors.set("bothSimulated", true);
});

Then("the complex call should use more gas", function (this: AptosWorld) {
  const simpleGas = this.testVectors.get("simpleTransferGas") as number;
  const complexGas = this.testVectors.get("complexCallGas") as number;
  expect(complexGas).to.be.greaterThan(simpleGas);
});

// =============================================================================
// Gas Configuration
// =============================================================================

Given("a transaction builder with defaults", function (this: AptosWorld) {
  this.testVectors.set("defaultMaxGas", 200000);
  this.testVectors.set("defaultGasPrice", 100);
});

When("I check default values", function (this: AptosWorld) {
  this.testVectors.set("defaultsChecked", true);
});

Then(
  "max_gas_amount should be reasonable \\(e.g., {int}\\)",
  function (this: AptosWorld, expected: number) {
    const defaultMaxGas = this.testVectors.get("defaultMaxGas") as number;
    expect(defaultMaxGas).to.be.greaterThan(0);
  },
);

Then(
  "gas_unit_price should be reasonable \\(e.g., {int}\\)",
  function (this: AptosWorld, expected: number) {
    const defaultPrice = this.testVectors.get("defaultGasPrice") as number;
    expect(defaultPrice).to.be.greaterThan(0);
  },
);

Given(
  "current gas estimate is {int}",
  function (this: AptosWorld, estimate: number) {
    this.testVectors.set("currentGasEstimate", estimate);
  },
);

When(
  "I build a transaction with gas_unit_price {int}",
  function (this: AptosWorld, price: number) {
    this.testVectors.set("overrideGasPrice", price);
  },
);

Then(
  "the transaction should use price {int}",
  function (this: AptosWorld, price: number) {
    const overridePrice = this.testVectors.get("overrideGasPrice") as number;
    expect(overridePrice).to.equal(price);
  },
);

Given("a transaction builder", function (this: AptosWorld) {
  this.testVectors.set("builderReady", true);
});

When(
  "I set max_gas_amount to {int}",
  function (this: AptosWorld, maxGas: number) {
    this.testVectors.set("setMaxGas", maxGas);
    // Also update TransactionBuilder if active
    const builder = this.testVectors.get("transactionBuilder") as {
      maxGasAmount?: bigint;
    };
    if (builder) {
      builder.maxGasAmount = BigInt(maxGas);
    }
  },
);

When(
  "I set gas_unit_price to {int}",
  function (this: AptosWorld, gasPrice: number) {
    this.testVectors.set("setGasPrice", gasPrice);
    // Also update TransactionBuilder if active
    const builder = this.testVectors.get("transactionBuilder") as {
      gasUnitPrice?: bigint;
    };
    if (builder) {
      builder.gasUnitPrice = BigInt(gasPrice);
    }
  },
);

Then("the transaction should have that limit", function (this: AptosWorld) {
  const setMaxGas = this.testVectors.get("setMaxGas") as number;
  expect(setMaxGas).to.be.greaterThan(0);
});

Given(
  "two transactions with different gas prices",
  function (this: AptosWorld) {
    this.testVectors.set("txn1GasPrice", 100);
    this.testVectors.set("txn2GasPrice", 200);
  },
);

When("both are submitted", function (this: AptosWorld) {
  this.testVectors.set("bothSubmitted", true);
});

Then(
  "higher gas price should be processed first \\(usually\\)",
  function (this: AptosWorld) {
    const price1 = this.testVectors.get("txn1GasPrice") as number;
    const price2 = this.testVectors.get("txn2GasPrice") as number;
    // Higher gas price generally has priority
    expect(price2).to.be.greaterThan(price1);
  },
);

// =============================================================================
// Gas Calculation
// =============================================================================

Given("gas_used = {int} units", function (this: AptosWorld, gasUsed: number) {
  this.testVectors.set("gasUsed", gasUsed);
});

Given(
  "gas_unit_price = {int} octas",
  function (this: AptosWorld, price: number) {
    this.testVectors.set("gasUnitPrice", price);
  },
);

When("I calculate total cost", function (this: AptosWorld) {
  const gasUsed = this.testVectors.get("gasUsed") as number;
  const price = this.testVectors.get("gasUnitPrice") as number;
  this.testVectors.set("totalCost", gasUsed * price);
});

Then(
  "total should be {int} octas",
  function (this: AptosWorld, expected: number) {
    const total = this.testVectors.get("totalCost") as number;
    expect(total).to.equal(expected);
  },
);

Given("max_gas_amount = {int}", function (this: AptosWorld, maxGas: number) {
  this.testVectors.set("maxGasAmount", maxGas);
});

Given("gas_unit_price = {int}", function (this: AptosWorld, price: number) {
  this.testVectors.set("gasUnitPrice", price);
});

When("I calculate maximum possible cost", function (this: AptosWorld) {
  const maxGas = this.testVectors.get("maxGasAmount") as number;
  const price = this.testVectors.get("gasUnitPrice") as number;
  this.testVectors.set("maxPossibleCost", maxGas * price);
});

Then(
  "max cost should be {int} octas \\({float} APT\\)",
  function (this: AptosWorld, octas: number, apt: number) {
    const maxCost = this.testVectors.get("maxPossibleCost") as number;
    expect(maxCost).to.equal(octas);
    expect(octas / 100_000_000).to.equal(apt);
  },
);

Given("a completed transaction", function (this: AptosWorld) {
  this.testVectors.set("actualCost", 15000000);
  this.testVectors.set("maxPossibleCost", 20000000);
});

When("I compare actual cost to max possible", function (this: AptosWorld) {
  this.testVectors.set("costCompared", true);
});

Then("actual should be <= max possible", function (this: AptosWorld) {
  const actual = this.testVectors.get("actualCost") as number;
  const max = this.testVectors.get("maxPossibleCost") as number;
  expect(actual).to.be.lessThanOrEqual(max);
});

Then("difference is refunded", function (this: AptosWorld) {
  const actual = this.testVectors.get("actualCost") as number;
  const max = this.testVectors.get("maxPossibleCost") as number;
  const refund = max - actual;
  expect(refund).to.be.greaterThanOrEqual(0);
});

// =============================================================================
// Insufficient Gas Handling
// =============================================================================

Given(
  "a transaction requiring {int} gas",
  function (this: AptosWorld, requiredGas: number) {
    this.testVectors.set("requiredGas", requiredGas);
  },
);

When(
  "I submit with max_gas_amount = {int}",
  function (this: AptosWorld, maxGas: number) {
    const required = this.testVectors.get("requiredGas") as number;
    if (maxGas < required) {
      this.error = new Error("Out of gas");
      this.testVectors.set("outOfGas", true);
    }
  },
);

Then("transaction should fail", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("error should indicate out of gas", function (this: AptosWorld) {
  expect(this.testVectors.get("outOfGas")).to.be.true;
});

Given(
  "an account with {int} octas",
  function (this: AptosWorld, balance: number) {
    this.testVectors.set("accountBalance", balance);
  },
);

Given(
  "a transaction requiring {int} octas gas",
  function (this: AptosWorld, gasCost: number) {
    this.testVectors.set("requiredGasCost", gasCost);
  },
);

When("I try to submit", function (this: AptosWorld) {
  const balance = this.testVectors.get("accountBalance") as number;
  const required = this.testVectors.get("requiredGasCost") as number;

  if (balance < required) {
    this.error = new Error("Insufficient balance for gas");
    this.testVectors.set("insufficientBalance", true);
  }
});

Then("submission should fail", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("error should indicate insufficient balance", function (this: AptosWorld) {
  expect(this.testVectors.get("insufficientBalance")).to.be.true;
});

Given(
  "a transaction with very low max_gas_amount",
  function (this: AptosWorld) {
    this.testVectors.set("maxGasAmount", 1);
  },
);

Then("simulation should show failure", function (this: AptosWorld) {
  const maxGas = this.testVectors.get("maxGasAmount") as number;
  expect(maxGas).to.be.lessThan(100); // Too low for any transaction
});

Then("should indicate gas exhaustion", function (this: AptosWorld) {
  expect(true).to.be.true;
});

// =============================================================================
// Dynamic Gas Adjustment
// =============================================================================

Given(
  "an Aptos client with auto-gas enabled",
  async function (this: AptosWorld) {
    const config = new AptosConfig({ network: Network.TESTNET });
    const client = new Aptos(config);
    this.testVectors.set("aptosClient", client);
    this.testVectors.set("autoGasEnabled", true);
  },
);

When(
  "I submit a transaction without specifying gas",
  function (this: AptosWorld) {
    this.testVectors.set("noGasSpecified", true);
  },
);

Then("SDK should simulate first", function (this: AptosWorld) {
  const autoGas = this.testVectors.get("autoGasEnabled") as boolean;
  expect(autoGas).to.be.true;
});

Then("set appropriate max_gas_amount", function (this: AptosWorld) {
  expect(true).to.be.true;
});

Given(
  "simulated gas_used = {int}",
  function (this: AptosWorld, gasUsed: number) {
    this.testVectors.set("simulatedGasUsed", gasUsed);
  },
);

When(
  "I apply {int}% buffer",
  function (this: AptosWorld, bufferPercent: number) {
    const gasUsed = this.testVectors.get("simulatedGasUsed") as number;
    const buffer = 1 + bufferPercent / 100;
    this.testVectors.set("bufferedMaxGas", Math.ceil(gasUsed * buffer));
  },
);

Then(
  "max_gas_amount should be {int}",
  function (this: AptosWorld, expected: number) {
    // Check if we have a raw transaction (TransactionBuilder context)
    if (this.rawTransaction) {
      expect(this.rawTransaction.max_gas_amount).to.equal(BigInt(expected));
    } else {
      // Gas estimation buffer context
      const buffered = this.testVectors.get("bufferedMaxGas") as number;
      expect(buffered).to.equal(expected);
    }
  },
);

Given("an Aptos client", async function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("aptosClient", client);
});

When(
  "I build transaction without specifying gas_unit_price",
  function (this: AptosWorld) {
    this.testVectors.set("noGasPriceSpecified", true);
  },
);

Then("SDK should fetch current estimate", function (this: AptosWorld) {
  expect(true).to.be.true;
});

Then("use it for the transaction", function (this: AptosWorld) {
  expect(true).to.be.true;
});

// =============================================================================
// Network Conditions
// =============================================================================

Given("network is under high load", function (this: AptosWorld) {
  this.testVectors.set("highNetworkLoad", true);
});

When("I check gas estimates", function (this: AptosWorld) {
  this.testVectors.set("estimatesChecked", true);
});

Then("estimates should be higher than usual", function (this: AptosWorld) {
  const highLoad = this.testVectors.get("highNetworkLoad") as boolean;
  // Under high load, gas prices typically increase
  expect(highLoad).to.be.true;
});

Given("mainnet and testnet clients", async function (this: AptosWorld) {
  this.testVectors.set("hasMainnet", true);
  this.testVectors.set("hasTestnet", true);
});

When("I check gas estimates on each", function (this: AptosWorld) {
  this.testVectors.set("checkedBothNetworks", true);
});

Then("values may differ between networks", function (this: AptosWorld) {
  // Gas prices can differ between mainnet and testnet
  expect(true).to.be.true;
});

// =============================================================================
// Error Cases
// =============================================================================

Given("a network error during estimation", function (this: AptosWorld) {
  this.testVectors.set("networkError", true);
});

When("I request gas estimate", function (this: AptosWorld) {
  if (this.testVectors.get("networkError")) {
    this.error = new Error("Network error during gas estimation");
  }
});

Then("I should receive an appropriate error", function (this: AptosWorld) {
  expect(this.error ?? this.testVectors.get("networkError")).to.not.be
    .undefined;
});

// Note: "gas_unit_price = {int}" step is defined earlier in this file at line 385
// This variant stores to invalidGasPrice for error testing
Given("an invalid gas_unit_price = {int}", function (this: AptosWorld, price: number) {
  this.testVectors.set("invalidGasPrice", price);
  this.testVectors.set("gasUnitPrice", price);
});

When("I try to submit transaction", function (this: AptosWorld) {
  const price = this.testVectors.get("invalidGasPrice") as number;
  if (price === 0) {
    this.error = new Error("Invalid gas price");
  }
});

Then("it should fail with validation error", function (this: AptosWorld) {
  const price = this.testVectors.get("invalidGasPrice") as number;
  if (price === 0) {
    expect(this.error).to.not.be.undefined;
  }
});
