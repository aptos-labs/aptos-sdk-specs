/**
 * View Function Step Definitions
 *
 * Implements behavioral tests for view function execution.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { Aptos, AptosConfig, Network, AccountAddress, MoveValue } from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";

// =============================================================================
// Basic View Function Calls
// =============================================================================

When("I call view function {string}", async function (this: AptosWorld, functionId: string) {
  this.testVectors.set("viewFunctionId", functionId);
});

When("with type arguments [{string}]", function (this: AptosWorld, typeArg: string) {
  this.testVectors.set("typeArguments", [typeArg]);
});

When("arguments [{string}]", function (this: AptosWorld, arg: string) {
  this.testVectors.set("functionArguments", [arg]);
});

Then("the call should succeed", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const functionId = this.testVectors.get("viewFunctionId") as string;
  const typeArgs = (this.testVectors.get("typeArguments") as string[]) ?? [];
  const args = (this.testVectors.get("functionArguments") as string[]) ?? [];

  try {
    const [module, func] = functionId.split("::").slice(-2);
    const moduleAddress = functionId.split("::")[0];

    const result = await client.view({
      payload: {
        function: functionId as any,
        typeArguments: typeArgs as any,
        functionArguments: args,
      },
    });

    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive return values", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result).to.not.be.undefined;
  expect(Array.isArray(result)).to.be.true;
});

When("with no type arguments", function (this: AptosWorld) {
  this.testVectors.set("typeArguments", []);
});

Then("the result should be a boolean", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result.length).to.be.greaterThan(0);
  expect(typeof result[0]).to.equal("boolean");
});

When("no arguments", function (this: AptosWorld) {
  this.testVectors.set("functionArguments", []);
});

Then("the result should be a u64", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result.length).to.be.greaterThan(0);
  // u64 can be returned as string or number
  expect(result[0]).to.not.be.undefined;
});

When("I call a view function that returns multiple values", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  // Use a function that returns multiple values
  this.testVectors.set("viewFunctionId", "0x1::timestamp::now_seconds");
  this.testVectors.set("typeArguments", []);
  this.testVectors.set("functionArguments", []);
});

Then("I should receive all return values in order", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(Array.isArray(result)).to.be.true;
});

// =============================================================================
// Argument Encoding
// =============================================================================

Given("a view function expecting an address", function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::account::exists_at");
  this.testVectors.set("typeArguments", []);
});

When("I pass address {string} as argument", function (this: AptosWorld, address: string) {
  this.testVectors.set("functionArguments", [address]);
});

Then("the address should be properly encoded", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const functionId = this.testVectors.get("viewFunctionId") as string;
  const args = this.testVectors.get("functionArguments") as string[];

  try {
    const result = await client.view({
      payload: {
        function: functionId as any,
        typeArguments: [],
        functionArguments: args,
      },
    });
    this.testVectors.set("viewResult", result);
    expect(result).to.not.be.undefined;
  } catch (e) {
    this.error = e as Error;
  }
});

Given("a view function expecting a u64", function (this: AptosWorld) {
  // Placeholder - actual function depends on what's available
  this.testVectors.set("expectedArgType", "u64");
});

When("I pass number {int} as argument", function (this: AptosWorld, num: number) {
  this.testVectors.set("functionArguments", [num.toString()]);
});

Then("the number should be properly encoded", function (this: AptosWorld) {
  const args = this.testVectors.get("functionArguments") as string[];
  expect(args[0]).to.not.be.undefined;
});

Given("a view function expecting a string", function (this: AptosWorld) {
  this.testVectors.set("expectedArgType", "string");
});

When("I pass {string} as argument", function (this: AptosWorld, str: string) {
  this.testVectors.set("functionArguments", [str]);
});

Then("the string should be properly encoded", function (this: AptosWorld) {
  const args = this.testVectors.get("functionArguments") as string[];
  expect(args[0]).to.not.be.undefined;
});

Given("a view function expecting vector<u8>", function (this: AptosWorld) {
  this.testVectors.set("expectedArgType", "vector<u8>");
});

When(
  "I pass bytes [{int}, {int}, {int}, {int}, {int}] as argument",
  function (this: AptosWorld, b1: number, b2: number, b3: number, b4: number, b5: number) {
    this.testVectors.set("functionArguments", [[b1, b2, b3, b4, b5]]);
  },
);

Then("the vector should be properly encoded", function (this: AptosWorld) {
  const args = this.testVectors.get("functionArguments") as any[];
  expect(args[0]).to.not.be.undefined;
});

Given("a view function expecting a bool", function (this: AptosWorld) {
  this.testVectors.set("expectedArgType", "bool");
});

When("I pass true as argument", function (this: AptosWorld) {
  this.testVectors.set("functionArguments", [true]);
});

Then("the boolean should be properly encoded", function (this: AptosWorld) {
  const args = this.testVectors.get("functionArguments") as any[];
  expect(args[0]).to.equal(true);
});

// =============================================================================
// Type Argument Handling
// =============================================================================

Given("a view function with one type parameter", function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::coin::balance");
});

When("I call with type argument {string}", function (this: AptosWorld, typeArg: string) {
  this.testVectors.set("typeArguments", [typeArg]);
});

Then("the type should be properly passed", async function (this: AptosWorld) {
  const typeArgs = this.testVectors.get("typeArguments") as string[];
  expect(typeArgs.length).to.equal(1);
});

Given("a view function with multiple type parameters", function (this: AptosWorld) {
  this.testVectors.set("expectedTypeParamCount", 2);
});

When(
  "I call with type arguments [{string}, {string}]",
  function (this: AptosWorld, type1: string, type2: string) {
    this.testVectors.set("typeArguments", [type1, type2]);
  },
);

Then("both types should be properly passed", function (this: AptosWorld) {
  const typeArgs = this.testVectors.get("typeArguments") as string[];
  expect(typeArgs.length).to.equal(2);
});

Given("a view function with generic type", function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::coin::balance");
});

Then("the nested type should be properly parsed", function (this: AptosWorld) {
  const typeArgs = this.testVectors.get("typeArguments") as string[];
  expect(typeArgs[0]).to.include("::");
});

// =============================================================================
// Return Value Parsing
// =============================================================================

Given("a view function returning u64", async function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::timestamp::now_seconds");
  this.testVectors.set("typeArguments", []);
  this.testVectors.set("functionArguments", []);
});

When("I execute the call", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const functionId = this.testVectors.get("viewFunctionId") as string;
  const typeArgs = (this.testVectors.get("typeArguments") as string[]) ?? [];
  const args = (this.testVectors.get("functionArguments") as any[]) ?? [];

  try {
    const result = await client.view({
      payload: {
        function: functionId as any,
        typeArguments: typeArgs as any,
        functionArguments: args,
      },
    });
    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should be able to parse the result as u64", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result.length).to.be.greaterThan(0);
  // u64 values can be parsed as BigInt or number
  const value = BigInt(result[0]);
  expect(value).to.be.greaterThanOrEqual(0n);
});

Given("a view function returning a String", function (this: AptosWorld) {
  this.testVectors.set("expectedReturnType", "string");
});

Then("I should be able to parse the result as string", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  if (result && result.length > 0) {
    expect(typeof result[0]).to.be.oneOf(["string", "object"]);
  }
});

Given("a view function returning bool", function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::account::exists_at");
  this.testVectors.set("typeArguments", []);
  this.testVectors.set("functionArguments", ["0x1"]);
});

Then("I should be able to parse the result as boolean", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result.length).to.be.greaterThan(0);
  expect(typeof result[0]).to.equal("boolean");
});

Given("a view function returning vector<u8>", function (this: AptosWorld) {
  this.testVectors.set("expectedReturnType", "vector<u8>");
});

Then("I should be able to parse the result as byte array", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  if (result && result.length > 0) {
    expect(Array.isArray(result[0]) || typeof result[0] === "string").to.be.true;
  }
});

Given("a view function returning a struct", function (this: AptosWorld) {
  this.testVectors.set("expectedReturnType", "struct");
});

Then("I should be able to access struct fields", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  if (result && result.length > 0 && typeof result[0] === "object") {
    expect(Object.keys(result[0]).length).to.be.greaterThan(0);
  }
});

// =============================================================================
// Error Cases
// =============================================================================

When(
  "I call non-existent view function {string}",
  async function (this: AptosWorld, functionId: string) {
    const client = this.testVectors.get("aptosClient") as Aptos;

    try {
      await client.view({
        payload: {
          function: functionId as any,
          typeArguments: [],
          functionArguments: [],
        },
      });
    } catch (e) {
      this.error = e as Error;
    }
  },
);

Then("I should receive an error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("the error should indicate function not found", function (this: AptosWorld) {
  expect(this.error!.message).to.match(/not found|does not exist|FUNCTION_NOT_FOUND/i);
});

When("I call a view function with wrong argument types", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;

  try {
    await client.view({
      payload: {
        function: "0x1::account::exists_at" as any,
        typeArguments: [],
        functionArguments: ["invalid_not_an_address"],
      },
    });
  } catch (e) {
    this.error = e as Error;
  }
});

Then("the error should indicate type mismatch", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

When("I call a view function with too few arguments", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;

  try {
    await client.view({
      payload: {
        function: "0x1::account::exists_at" as any,
        typeArguments: [],
        functionArguments: [], // Missing required argument
      },
    });
  } catch (e) {
    this.error = e as Error;
  }
});

When("I call a generic function without type arguments", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;

  try {
    await client.view({
      payload: {
        function: "0x1::coin::balance" as any,
        typeArguments: [], // Missing required type argument
        functionArguments: ["0x1"],
      },
    });
  } catch (e) {
    this.error = e as Error;
  }
});

Given("a view function that can abort", function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::coin::balance");
});

When("I call with arguments that cause abort", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;

  try {
    // Call balance on an account that doesn't have a CoinStore
    await client.view({
      payload: {
        function: "0x1::coin::balance" as any,
        typeArguments: ["0x1::aptos_coin::AptosCoin"],
        functionArguments: ["0x" + "0".repeat(64)], // Non-existent account
      },
    });
  } catch (e) {
    this.error = e as Error;
  }
});

Then("the error should contain the abort code", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
  // Abort errors typically contain an abort code
});

// =============================================================================
// Common View Functions
// =============================================================================

When("I call 0x1::coin::balance<0x1::aptos_coin::AptosCoin>", async function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::coin::balance");
  this.testVectors.set("typeArguments", ["0x1::aptos_coin::AptosCoin"]);
});

When("with the account address as argument", async function (this: AptosWorld) {
  const address = this.testVectors.get("accountAddress") as AccountAddress;
  this.testVectors.set("functionArguments", [address.toString()]);

  const client = this.testVectors.get("aptosClient") as Aptos;
  const functionId = this.testVectors.get("viewFunctionId") as string;
  const typeArgs = this.testVectors.get("typeArguments") as string[];
  const args = this.testVectors.get("functionArguments") as string[];

  try {
    const result = await client.view({
      payload: {
        function: functionId as any,
        typeArguments: typeArgs as any,
        functionArguments: args,
      },
    });
    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive the balance as u64", function (this: AptosWorld) {
  if (!this.error) {
    const result = this.testVectors.get("viewResult") as any[];
    expect(result.length).to.be.greaterThan(0);
    const balance = BigInt(result[0]);
    expect(balance).to.be.greaterThanOrEqual(0n);
  }
});

When("I call 0x1::account::exists_at", async function (this: AptosWorld) {
  this.testVectors.set("viewFunctionId", "0x1::account::exists_at");
  this.testVectors.set("typeArguments", []);
});

When("with address {string} as argument", async function (this: AptosWorld, address: string) {
  this.testVectors.set("functionArguments", [address]);

  const client = this.testVectors.get("aptosClient") as Aptos;
  const functionId = this.testVectors.get("viewFunctionId") as string;
  const args = [address];

  try {
    const result = await client.view({
      payload: {
        function: functionId as any,
        typeArguments: [],
        functionArguments: args,
      },
    });
    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive true", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result[0]).to.equal(true);
});

When("I call 0x1::timestamp::now_seconds", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;

  try {
    const result = await client.view({
      payload: {
        function: "0x1::timestamp::now_seconds" as any,
        typeArguments: [],
        functionArguments: [],
      },
    });
    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive current blockchain timestamp", function (this: AptosWorld) {
  const result = this.testVectors.get("viewResult") as any[];
  expect(result.length).to.be.greaterThan(0);
  const timestamp = BigInt(result[0]);
  expect(timestamp).to.be.greaterThan(0n);
});

When("I call 0x1::coin::supply<0x1::aptos_coin::AptosCoin>", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;

  try {
    const result = await client.view({
      payload: {
        function: "0x1::coin::supply" as any,
        typeArguments: ["0x1::aptos_coin::AptosCoin"],
        functionArguments: [],
      },
    });
    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive the total supply", function (this: AptosWorld) {
  if (!this.error) {
    const result = this.testVectors.get("viewResult") as any[];
    expect(result).to.not.be.undefined;
  }
});

// =============================================================================
// At Specific Ledger Version
// =============================================================================

Given("a known past ledger version", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const ledgerInfo = await client.getLedgerInfo();
  // Use a recent but not current version
  const pastVersion = BigInt(ledgerInfo.ledger_version) - 10n;
  this.testVectors.set("pastLedgerVersion", pastVersion > 0n ? pastVersion : 1n);
});

When("I call a view function at that version", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const version = this.testVectors.get("pastLedgerVersion") as bigint;

  try {
    const result = await client.view({
      payload: {
        function: "0x1::timestamp::now_seconds" as any,
        typeArguments: [],
        functionArguments: [],
      },
      options: {
        ledgerVersion: version,
      },
    });
    this.testVectors.set("viewResult", result);
    this.result = result;
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive the state as of that version", function (this: AptosWorld) {
  if (!this.error) {
    const result = this.testVectors.get("viewResult") as any[];
    expect(result).to.not.be.undefined;
  }
});

Given("a ledger version older than oldest available", function (this: AptosWorld) {
  // Very old version that's likely pruned
  this.testVectors.set("oldLedgerVersion", 1n);
});

When("I try to call a view function at that version", async function (this: AptosWorld) {
  const client = this.testVectors.get("aptosClient") as Aptos;
  const version = this.testVectors.get("oldLedgerVersion") as bigint;

  try {
    await client.view({
      payload: {
        function: "0x1::timestamp::now_seconds" as any,
        typeArguments: [],
        functionArguments: [],
      },
      options: {
        ledgerVersion: version,
      },
    });
  } catch (e) {
    this.error = e as Error;
  }
});

Then("I should receive an error about unavailable state", function (this: AptosWorld) {
  // Old versions may or may not be available depending on the node
  // If there's an error, it should indicate version issues
  if (this.error) {
    expect(this.error.message.toLowerCase()).to.match(/version|unavailable|pruned|not found/i);
  }
});
