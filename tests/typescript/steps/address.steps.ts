import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { AccountAddress, Deserializer, Serializer } from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";
import {
  getAddressParsingVectors,
  getAddressConstants,
  getInvalidAddressInputs,
  hexToBytes,
  bytesToHex,
} from "../support/vectors.js";

// =============================================================================
// Given Steps - Address Input
// =============================================================================

// Primary step used in feature files
Given("a hex string {string}", function (this: AptosWorld, hex: string) {
  this.hexString = hex;
});

// Alternative phrasings for compatibility
Given(
  "a valid hex address string {string}",
  function (this: AptosWorld, hex: string) {
    this.hexString = hex;
  },
);

Given(
  "the address string {string}",
  function (this: AptosWorld, address: string) {
    this.hexString = address;
  },
);

Given("a short address {string}", function (this: AptosWorld, address: string) {
  this.hexString = address;
});

Given("a full 64-character hex address", function (this: AptosWorld) {
  this.hexString =
    "0x0000000000000000000000000000000000000000000000000000000000000001";
});

Given(
  "an invalid hex string {string}",
  function (this: AptosWorld, hex: string) {
    this.hexString = hex;
  },
);

Given("test vectors from addresses.json", function (this: AptosWorld) {
  const vectors = getAddressParsingVectors();
  this.testVectors.set("address_parsing", vectors);
});

// =============================================================================
// Given Steps - Address Creation from Value/Hex
// =============================================================================

Given(
  "an AccountAddress with value {int}",
  function (this: AptosWorld, value: number) {
    // Create address with specific byte value in last position
    const bytes = new Uint8Array(32);
    bytes[31] = value;
    this.address = AccountAddress.from(bytes);
  },
);

Given(
  "an AccountAddress from hex {string}",
  function (this: AptosWorld, hex: string) {
    this.address = AccountAddress.from(normalizeHexAddress(hex));
    // Store for comparison - initialize addresses array
    this.addresses = [this.address];
    this.testVectors.set("original_address", this.address);
  },
);

Given(
  "another AccountAddress from hex {string}",
  function (this: AptosWorld, hex: string) {
    const address2 = AccountAddress.from(normalizeHexAddress(hex));
    // Add second address for comparison
    if (!this.addresses || this.addresses.length === 0) {
      this.addresses = [this.address!];
    }
    this.addresses.push(address2);
  },
);

// =============================================================================
// Given Steps - Bytes
// =============================================================================

Given("32 random bytes", function (this: AptosWorld) {
  this.bytes = new Uint8Array(32);
  crypto.getRandomValues(this.bytes);
});

Given(
  "32 bytes with value {int} in the last byte",
  function (this: AptosWorld, value: number) {
    this.bytes = new Uint8Array(32);
    this.bytes[31] = value;
  },
);

// =============================================================================
// Given Steps - Address Constants
// =============================================================================

Given("the ZERO address constant", function (this: AptosWorld) {
  this.address = AccountAddress.ZERO;
});

Given("the zero address constant", function (this: AptosWorld) {
  this.address = AccountAddress.ZERO;
});

Given("the ONE address constant", function (this: AptosWorld) {
  this.address = AccountAddress.ONE;
});

Given("the framework address constant", function (this: AptosWorld) {
  this.address = AccountAddress.ONE;
});

Given("the THREE address constant", function (this: AptosWorld) {
  this.address = AccountAddress.THREE;
});

Given("the FOUR address constant", function (this: AptosWorld) {
  this.address = AccountAddress.FOUR;
});

// =============================================================================
// Given Steps - Address Pairs for Comparison
// =============================================================================

Given(
  "two addresses {string} and {string}",
  function (this: AptosWorld, addr1: string, addr2: string) {
    this.addresses = [AccountAddress.from(addr1), AccountAddress.from(addr2)];
  },
);

// =============================================================================
// When Steps - Parsing
// =============================================================================

// Helper to normalize short hex addresses for parsing
function normalizeHexAddress(hex: string): string {
  if (hex.startsWith("0x") || hex.startsWith("0X")) {
    const hexPart = hex.slice(2);
    if (hexPart.length < 64 && hexPart.length > 0) {
      return "0x" + hexPart.padStart(64, "0");
    }
    return hex;
  } else if (hex.length < 64 && hex.length > 0) {
    return "0x" + hex.padStart(64, "0");
  }
  return hex;
}

// Helper to get short string format (strip leading zeros)
// The TS SDK only provides short format for special addresses (0x1-0x4)
// So we implement our own for testing purposes
function toShortString(address: AccountAddress): string {
  const full = address.toStringLong();
  const hex = full.slice(2); // Remove 0x prefix
  const trimmed = hex.replace(/^0+/, ""); // Remove leading zeros
  return "0x" + (trimmed || "0"); // Ensure at least '0x0' for zero address
}

When("I parse the address", function (this: AptosWorld) {
  try {
    this.address = AccountAddress.from(normalizeHexAddress(this.hexString!));
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I parse the address string", function (this: AptosWorld) {
  try {
    this.address = AccountAddress.from(normalizeHexAddress(this.hexString!));
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I parse it as an AccountAddress", function (this: AptosWorld) {
  try {
    this.address = AccountAddress.from(normalizeHexAddress(this.hexString!));
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I create an AccountAddress from the bytes", function (this: AptosWorld) {
  try {
    this.address = AccountAddress.from(this.bytes!);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I try to parse it as an address", function (this: AptosWorld) {
  try {
    this.address = AccountAddress.from(this.hexString!);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// =============================================================================
// When Steps - Formatting
// =============================================================================

When("I format the address as a string", function (this: AptosWorld) {
  this.hexString = this.address!.toString();
});

When("I format it as full hex", function (this: AptosWorld) {
  this.result = this.address!.toStringLong();
});

When("I format it as a full hex string", function (this: AptosWorld) {
  this.hexString = this.address!.toStringLong();
});

When("I format it as short string", function (this: AptosWorld) {
  this.result = toShortString(this.address!);
});

When("I format it as a short string", function (this: AptosWorld) {
  this.hexString = toShortString(this.address!);
});

// =============================================================================
// When Steps - Bytes/Serialization
// =============================================================================

When("I get the raw bytes", function (this: AptosWorld) {
  this.bytes = this.address!.toUint8Array();
});

When("I BCS serialize the address", function (this: AptosWorld) {
  // BCS serialization of an address is just the 32 bytes
  this.bytes = this.address!.toUint8Array();
});

When("I BCS deserialize as AccountAddress", function (this: AptosWorld) {
  try {
    const deserializer = new Deserializer(this.bytes!);
    this.address = AccountAddress.deserialize(deserializer);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When(
  "I BCS deserialize the result as AccountAddress",
  function (this: AptosWorld) {
    try {
      const deserializer = new Deserializer(this.bytes!);
      this.result = AccountAddress.deserialize(deserializer);
      this.clearError();
    } catch (error) {
      this.setError(error as Error);
    }
  },
);

// =============================================================================
// When Steps - Comparison
// =============================================================================

When("I compare them for equality", function (this: AptosWorld) {
  this.result = this.addresses[0].equals(this.addresses[1]);
});

// =============================================================================
// When Steps - Test Vectors
// =============================================================================

When("I run all parsing test vectors", function (this: AptosWorld) {
  const vectors = this.testVectors.get("address_parsing");
  const results: Array<{ name: string; passed: boolean; error?: string }> = [];

  for (const vector of vectors) {
    try {
      const address = AccountAddress.from(vector.input);
      const fullHex = address.toStringLong();
      const shortString = address.toString();

      const passed =
        fullHex.toLowerCase() === vector.expected.full_hex.toLowerCase() &&
        shortString.toLowerCase() ===
          vector.expected.short_string.toLowerCase();

      results.push({ name: vector.name, passed });
    } catch (error) {
      results.push({
        name: vector.name,
        passed: false,
        error: (error as Error).message,
      });
    }
  }

  this.result = results;
});

// =============================================================================
// Then Steps - Parsing Success/Failure
// =============================================================================

Then("the parsing should succeed", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  // Check for either address or result (for TypeTags)
  expect(this.address ?? this.result).to.not.be.undefined;
});

Then("I should get a valid AccountAddress", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  expect(this.address).to.not.be.undefined;
});

Then("the address should be valid", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  expect(this.address).to.not.be.undefined;
});

Then("parsing should fail", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("parsing should fail with an error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then(
  "the parsing should fail with an invalid address error",
  function (this: AptosWorld) {
    expect(this.error).to.not.be.undefined;
  },
);

Then(
  "the parsing should fail with an invalid hex error",
  function (this: AptosWorld) {
    expect(this.error).to.not.be.undefined;
  },
);

Then(
  "the parsing should fail with an invalid length error",
  function (this: AptosWorld) {
    expect(this.error).to.not.be.undefined;
  },
);

Then(
  "it should fail with an InvalidAddress error",
  function (this: AptosWorld) {
    expect(this.error).to.not.be.undefined;
  },
);

// =============================================================================
// Then Steps - Address Byte Assertions
// =============================================================================

Then(
  "the address bytes should have length {int}",
  function (this: AptosWorld, length: number) {
    expect(this.address!.toUint8Array().length).to.equal(length);
  },
);

Then(
  "byte {int} should equal {int}",
  function (this: AptosWorld, index: number, value: number) {
    const bytes = this.address?.toUint8Array() ?? this.bytes;
    expect(bytes![index]).to.equal(value);
  },
);

Then(
  "bytes {int}-{int} should all be {int}",
  function (this: AptosWorld, start: number, end: number, value: number) {
    const bytes = this.address?.toUint8Array() ?? this.bytes;
    for (let i = start; i <= end; i++) {
      expect(bytes![i]).to.equal(value);
    }
  },
);

Then(
  "all 32 bytes should be {int}",
  function (this: AptosWorld, value: number) {
    const bytes = this.address!.toUint8Array();
    for (let i = 0; i < 32; i++) {
      expect(bytes[i]).to.equal(value);
    }
  },
);

Then("the byte length should be 32", function (this: AptosWorld) {
  expect(this.bytes!.length).to.equal(32);
});

Then("the bytes should be 32 bytes", function (this: AptosWorld) {
  expect(this.bytes!.length).to.equal(32);
});

// Removed duplicate - use regex version from hashing.steps.ts

Then("the first byte should be zero", function (this: AptosWorld) {
  expect(this.bytes![0]).to.equal(0);
});

Then(
  "the last byte should be {int}",
  function (this: AptosWorld, expected: number) {
    const bytes = this.address?.toUint8Array() ?? this.bytes;
    expect(bytes![31]).to.equal(expected);
  },
);

// =============================================================================
// Then Steps - String Format Assertions
// =============================================================================

Then(
  "the full hex should be {string}",
  function (this: AptosWorld, expected: string) {
    const actual = this.address!.toStringLong();
    expect(actual.toLowerCase()).to.equal(expected.toLowerCase());
  },
);

Then(
  "the full hex representation should be {string}",
  function (this: AptosWorld, expected: string) {
    const actual = this.address!.toStringLong();
    expect(actual.toLowerCase()).to.equal(expected.toLowerCase());
  },
);

Then(
  "the short string should be {string}",
  function (this: AptosWorld, expected: string) {
    const actual = toShortString(this.address!);
    expect(actual.toLowerCase()).to.equal(expected.toLowerCase());
  },
);

Then(
  "the address should equal {string}",
  function (this: AptosWorld, expected: string) {
    const actual = this.address!.toString();
    expect(actual.toLowerCase()).to.equal(expected.toLowerCase());
  },
);

Then(
  "the result should be {string}",
  function (this: AptosWorld, expected: string) {
    // Check testVectors.formattedString first, then this.result, then this.hexString
    const actual =
      this.testVectors.get("formattedString") ?? this.result ?? this.hexString;
    expect(String(actual).toLowerCase()).to.equal(expected.toLowerCase());
  },
);

// =============================================================================
// Then Steps - Address Equality
// =============================================================================

Then(
  "it should equal address {string}",
  function (this: AptosWorld, expected: string) {
    const expectedAddress = AccountAddress.from(expected);
    expect(this.address!.equals(expectedAddress)).to.be.true;
  },
);

Then("the two addresses should be equal", function (this: AptosWorld) {
  expect(this.addresses[0].equals(this.addresses[1])).to.be.true;
});

Then("the two addresses should not be equal", function (this: AptosWorld) {
  expect(this.addresses[0].equals(this.addresses[1])).to.be.false;
});

Then("they should be equal", function (this: AptosWorld) {
  // Handle both comparison result (boolean) and hash comparison (testVectors)
  if (this.testVectors.has("hash1") && this.testVectors.has("hash2")) {
    const hash1 = this.testVectors.get("hash1") as Uint8Array;
    const hash2 = this.testVectors.get("hash2") as Uint8Array;
    const hex1 = Array.from(hash1)
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
    const hex2 = Array.from(hash2)
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
    expect(hex1).to.equal(hex2);
  } else {
    expect(this.result).to.be.true;
  }
});

Then("they should not be equal", function (this: AptosWorld) {
  expect(this.result).to.be.false;
});

Then(
  "the result should equal the original address",
  function (this: AptosWorld) {
    const originalAddress = this.testVectors.get(
      "original_address",
    ) as AccountAddress;
    const resultAddress = this.result as AccountAddress;
    expect(resultAddress.equals(originalAddress)).to.be.true;
  },
);

// =============================================================================
// Then Steps - Test Vectors
// =============================================================================

Then("all test vectors should pass", function (this: AptosWorld) {
  const results = this.result as Array<{
    name: string;
    passed: boolean;
    error?: string;
  }>;
  const failures = results.filter((r) => !r.passed);

  if (failures.length > 0) {
    const failureMessages = failures
      .map((f) => `  - ${f.name}: ${f.error || "mismatch"}`)
      .join("\n");
    throw new Error(
      `${failures.length} test vectors failed:\n${failureMessages}`,
    );
  }
});
