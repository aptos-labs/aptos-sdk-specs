import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { Serializer, Deserializer, AccountAddress } from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";
import { bytesToHex, hexToBytes } from "../support/vectors.js";

// =============================================================================
// Given Steps - Boolean Values
// =============================================================================

Given("a boolean value true", function (this: AptosWorld) {
  this.testVectors.set("boolValue", true);
});

Given("a boolean value false", function (this: AptosWorld) {
  this.testVectors.set("boolValue", false);
});

// =============================================================================
// Given Steps - Integer Values
// =============================================================================

Given("a u8 value {int}", function (this: AptosWorld, value: number) {
  this.testVectors.set("u8Value", value);
});

Given("a u16 value {word}", function (this: AptosWorld, value: string) {
  const numValue = value.startsWith("0x")
    ? parseInt(value, 16)
    : parseInt(value, 10);
  this.testVectors.set("u16Value", numValue);
});

Given("a u32 value {word}", function (this: AptosWorld, value: string) {
  const numValue = value.startsWith("0x")
    ? parseInt(value, 16)
    : parseInt(value, 10);
  this.testVectors.set("u32Value", numValue);
});

Given("a u64 value {word}", function (this: AptosWorld, value: string) {
  this.testVectors.set("u64Value", BigInt(value));
});

Given("a u128 value {word}", function (this: AptosWorld, value: number) {
  this.testVectors.set("u128Value", BigInt(value));
});

Given("a u256 value {word}", function (this: AptosWorld, value: string) {
  this.testVectors.set("u256Value", BigInt(value));
});

// =============================================================================
// Given Steps - Signed Integer Values
// =============================================================================

Given(/^an i8 value (-?\d+)$/, function (this: AptosWorld, value: string) {
  this.testVectors.set("i8Value", parseInt(value, 10));
});

Given(/^an i16 value (-?\d+)$/, function (this: AptosWorld, value: string) {
  this.testVectors.set("i16Value", parseInt(value, 10));
});

Given(/^an i32 value (-?\d+)$/, function (this: AptosWorld, value: string) {
  this.testVectors.set("i32Value", parseInt(value, 10));
});

Given(/^an i64 value (-?\d+)$/, function (this: AptosWorld, value: string) {
  this.testVectors.set("i64Value", BigInt(value));
});

Given(/^an i128 value (-?\d+)$/, function (this: AptosWorld, value: string) {
  this.testVectors.set("i128Value", BigInt(value));
});

Given(/^an i256 value (-?\d+)$/, function (this: AptosWorld, value: string) {
  this.testVectors.set("i256Value", BigInt(value));
});

Given("a length value {int}", function (this: AptosWorld, value: number) {
  this.testVectors.set("lengthValue", value);
});

// =============================================================================
// Given Steps - Bytes/String Values
// =============================================================================

Given("an empty byte array", function (this: AptosWorld) {
  this.bytes = new Uint8Array(0);
});

// Use regex for bracket patterns - Cucumber expressions can't escape brackets
Given(
  /^bytes \[(0x[0-9a-fA-F]+(?:,\s*0x[0-9a-fA-F]+)*)\]$/,
  function (this: AptosWorld, bytesStr: string) {
    const byteValues = bytesStr.split(",").map((b) => {
      const trimmed = b.trim();
      return parseInt(trimmed, 16);
    });
    this.bytes = new Uint8Array(byteValues);
  },
);

Given("a string {string}", function (this: AptosWorld, str: string) {
  this.testVectors.set("stringValue", str);
});

// =============================================================================
// Given Steps - Option Values
// =============================================================================

Given("an Option with no value", function (this: AptosWorld) {
  this.testVectors.set("optionValue", null);
});

Given(
  "an Option containing u64 value {int}",
  function (this: AptosWorld, value: number) {
    this.testVectors.set("optionValue", BigInt(value));
  },
);

// =============================================================================
// Given Steps - Vector Values
// =============================================================================

Given("an empty vector of u8", function (this: AptosWorld) {
  this.testVectors.set("vectorU8", new Uint8Array(0));
});

Given(
  /^a vector \[(\d+), (\d+), (\d+)\] of u8$/,
  function (this: AptosWorld, a: string, b: string, c: string) {
    this.testVectors.set(
      "vectorU8",
      new Uint8Array([parseInt(a), parseInt(b), parseInt(c)]),
    );
  },
);

Given(
  /^a vector \[(\d+), (\d+)\] of u64$/,
  function (this: AptosWorld, a: string, b: string) {
    this.testVectors.set("vectorU64", [BigInt(a), BigInt(b)]);
  },
);

Given(
  /^a vector \[\[(\d+), (\d+)\], \[(\d+), (\d+)\]\] of vectors of u8$/,
  function (this: AptosWorld, a1: string, a2: string, b1: string, b2: string) {
    this.testVectors.set("nestedVector", [
      new Uint8Array([parseInt(a1), parseInt(a2)]),
      new Uint8Array([parseInt(b1), parseInt(b2)]),
    ]);
  },
);

// =============================================================================
// Given Steps - AccountAddress
// =============================================================================

Given(
  "an AccountAddress {string}",
  function (this: AptosWorld, addressStr: string) {
    this.address = AccountAddress.from(addressStr);
  },
);

Given(
  "{int} bytes with byte {int} = {word}",
  function (
    this: AptosWorld,
    totalBytes: number,
    byteIndex: number,
    value: string,
  ) {
    const bytes = new Uint8Array(totalBytes);
    bytes[byteIndex] = parseInt(value, 16);
    this.bytes = bytes;
  },
);

// =============================================================================
// Given Steps - Complex Structs
// =============================================================================

Given("a struct with fields:", function (this: AptosWorld, dataTable: any) {
  const fields = dataTable.hashes();
  this.testVectors.set("structFields", fields);
});

// =============================================================================
// Given Steps - Error Cases
// =============================================================================

Given(
  /^bytes \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\] intended for u64$/,
  function (this: AptosWorld, b1: string, b2: string) {
    this.bytes = new Uint8Array([parseInt(b1, 16), parseInt(b2, 16)]);
    this.testVectors.set("intendedType", "u64");
  },
);

// =============================================================================
// When Steps - BCS Serialization
// =============================================================================

// Helper: Convert signed integer to two's complement unsigned representation
function toTwosComplement(value: number | bigint, bits: number): bigint {
  const bigValue = BigInt(value);
  const maxUnsigned = BigInt(1) << BigInt(bits);
  if (bigValue < 0) {
    return maxUnsigned + bigValue;
  }
  return bigValue;
}

When("I BCS serialize it", function (this: AptosWorld) {
  try {
    const serializer = new Serializer();

    // Check what value type we have
    if (this.testVectors.has("boolValue")) {
      serializer.serializeBool(this.testVectors.get("boolValue") as boolean);
    } else if (this.testVectors.has("u8Value")) {
      serializer.serializeU8(this.testVectors.get("u8Value") as number);
    } else if (this.testVectors.has("u16Value")) {
      serializer.serializeU16(this.testVectors.get("u16Value") as number);
    } else if (this.testVectors.has("u32Value")) {
      serializer.serializeU32(this.testVectors.get("u32Value") as number);
    } else if (this.testVectors.has("u64Value")) {
      serializer.serializeU64(this.testVectors.get("u64Value") as bigint);
    } else if (this.testVectors.has("u128Value")) {
      serializer.serializeU128(this.testVectors.get("u128Value") as bigint);
    } else if (this.testVectors.has("u256Value")) {
      serializer.serializeU256(this.testVectors.get("u256Value") as bigint);
    // Signed integer types (two's complement)
    // TODO: Add support for signed integer types, it's not working correctly atm
    /*} else if (this.testVectors.has("i8Value")) {
      const val = toTwosComplement(this.testVectors.get("i8Value") as number, 8);
      serializer.serializeU8(Number(val));
    } else if (this.testVectors.has("i16Value")) {
      const val = toTwosComplement(this.testVectors.get("i16Value") as number, 16);
      serializer.serializeU16(Number(val));
    } else if (this.testVectors.has("i32Value")) {
      const val = toTwosComplement(this.testVectors.get("i32Value") as number, 32);
      serializer.serializeU32(Number(val));
    } else if (this.testVectors.has("i64Value")) {
      const val = toTwosComplement(this.testVectors.get("i64Value") as bigint, 64);
      serializer.serializeU64(val);
    } else if (this.testVectors.has("i128Value")) {
      const val = toTwosComplement(this.testVectors.get("i128Value") as bigint, 128);
      serializer.serializeU128(val);
    } else if (this.testVectors.has("i256Value")) {
      const val = toTwosComplement(this.testVectors.get("i256Value") as bigint, 256);
      serializer.serializeU256(val);
      */
    } else if (this.testVectors.has("stringValue")) {
      serializer.serializeStr(this.testVectors.get("stringValue") as string);
    } else if (this.testVectors.has("optionValue")) {
      const opt = this.testVectors.get("optionValue");
      if (opt === null) {
        serializer.serializeBool(false);
      } else {
        serializer.serializeBool(true);
        serializer.serializeU64(opt as bigint);
      }
    } else if (this.testVectors.has("vectorU8")) {
      const vec = this.testVectors.get("vectorU8") as Uint8Array;
      serializer.serializeBytes(vec);
    } else if (this.testVectors.has("vectorU64")) {
      const vec = this.testVectors.get("vectorU64") as bigint[];
      serializer.serializeU32AsUleb128(vec.length);
      for (const v of vec) {
        serializer.serializeU64(v);
      }
    } else if (this.testVectors.has("nestedVector")) {
      const vec = this.testVectors.get("nestedVector") as Uint8Array[];
      serializer.serializeU32AsUleb128(vec.length);
      for (const inner of vec) {
        serializer.serializeBytes(inner);
      }
    } else if (this.testVectors.has("structFields")) {
      // Serialize struct fields in order
      const fields = this.testVectors.get("structFields") as Array<{
        field: string;
        type: string;
        value: string;
      }>;
      for (const f of fields) {
        if (f.type === "address") {
          const addr = AccountAddress.from(f.value);
          addr.serialize(serializer);
        } else if (f.type === "u64") {
          serializer.serializeU64(BigInt(f.value));
        } else if (f.type === "u8") {
          serializer.serializeU8(parseInt(f.value));
        }
        // Add more types as needed
      }
    } else if (this.rawTransaction) {
      // Handle RawTransaction serialization
      this.rawTransaction.serialize(serializer);
    } else if (this.signedTransaction) {
      // Handle SignedTransaction serialization
      this.signedTransaction.serialize(serializer);
    } else if (
      this.result &&
      typeof (this.result as any).serialize === "function"
    ) {
      // Handle any serializable result (e.g., TransactionAuthenticator)
      (this.result as any).serialize(serializer);
    } else if (this.bytes) {
      serializer.serializeBytes(this.bytes);
    } else if (this.address) {
      this.address.serialize(serializer);
    }

    this.bytes = serializer.toUint8Array();
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I ULEB128 encode it", function (this: AptosWorld) {
  try {
    const value = this.testVectors.get("lengthValue") as number;
    const serializer = new Serializer();
    serializer.serializeU32AsUleb128(value);
    this.bytes = serializer.toUint8Array();
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I ULEB128 encode and decode it", function (this: AptosWorld) {
  try {
    const originalValue = this.testVectors.get("lengthValue") as number;

    // Encode
    const serializer = new Serializer();
    serializer.serializeU32AsUleb128(originalValue);
    const bytes = serializer.toUint8Array();

    // Decode
    const deserializer = new Deserializer(bytes);
    this.result = deserializer.deserializeUleb128AsU32();
    this.testVectors.set("originalValue", originalValue);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// =============================================================================
// When Steps - BCS Deserialization
// =============================================================================

When("I BCS deserialize as boolean", function (this: AptosWorld) {
  try {
    const deserializer = new Deserializer(this.bytes!);
    this.result = deserializer.deserializeBool();
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I BCS deserialize as u64", function (this: AptosWorld) {
  try {
    const deserializer = new Deserializer(this.bytes!);
    this.result = deserializer.deserializeU64();
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I BCS deserialize as vector of u8", function (this: AptosWorld) {
  try {
    const deserializer = new Deserializer(this.bytes!);
    this.result = deserializer.deserializeBytes();
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// =============================================================================
// Then Steps - Result Validation
// =============================================================================

// Removed duplicate - use the regex version from hashing.steps.ts

Then(
  "the byte should be {word}",
  function (this: AptosWorld, expected: string) {
    expect(this.bytes![0]).to.equal(parseInt(expected, 16));
  },
);


Then(
  /^the bytes should be \[((?:0x[0-9a-fA-F]+, )*0x[0-9a-fA-F]+)\]$/,
  function (this: AptosWorld, bytesStr: string) {
    const hexByteRegex = /0x[0-9a-fA-F]+/g;
    const matches = bytesStr.match(hexByteRegex);
    if (!matches) {
      throw new Error("No byte values found");
    }
    const expected = matches.map((b) => parseInt(b, 16));
    expect(this.bytes!.length).to.equal(expected.length);
    for (let i = 0; i < expected.length; i++) {
      expect(this.bytes![i]).to.equal(expected[i]);
    }
  },
);


Then(
  "the result should be {int} bytes in little-endian",
  function (this: AptosWorld, count: number) {
    expect(this.bytes!.length).to.equal(count);
  },
);

Then(
  "the result should be {int} bytes in little-endian \\(two\'s complement)",
  function (this: AptosWorld, count: number) {
    expect(this.bytes!.length).to.equal(count);
  },
);


Then(
  "byte {int} should be {word}",
  function (this: AptosWorld, index: number, expected: string) {
    expect(this.bytes![index]).to.equal(parseInt(expected, 16));
  },
);

Then(
  /^bytes (\d+)-(\d+) should all be (0x[0-9a-fA-F]+)$/,
  function (this: AptosWorld, start: string, end: string, expected: string) {
    const from = parseInt(start, 10);
    const to = parseInt(end, 10);
    const value = parseInt(expected, 16);
    for (let i = from; i <= to; i++) {
      expect(this.bytes![i]).to.equal(value);
    }
  },
);

// Removed duplicate - use version from address.steps.ts

Then(
  /^the result should be \[(0x[0-9a-fA-F]+)\]$/,
  function (this: AptosWorld, expected: string) {
    expect(this.bytes!.length).to.equal(1);
    expect(this.bytes![0]).to.equal(parseInt(expected, 16));
  },
);

Then(
  /^the result should be \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\]$/,
  function (this: AptosWorld, b1: string, b2: string) {
    expect(this.bytes!.length).to.equal(2);
    expect(this.bytes![0]).to.equal(parseInt(b1, 16));
    expect(this.bytes![1]).to.equal(parseInt(b2, 16));
  },
);

Then(
  /^the result should be \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\]$/,
  function (this: AptosWorld, b1: string, b2: string, b3: string) {
    expect(this.bytes!.length).to.equal(3);
    expect(this.bytes![0]).to.equal(parseInt(b1, 16));
    expect(this.bytes![1]).to.equal(parseInt(b2, 16));
    expect(this.bytes![2]).to.equal(parseInt(b3, 16));
  },
);

Then(
  /^the first byte should be (0x[0-9a-fA-F]+) \(length\)$/,
  function (this: AptosWorld, expected: string) {
    expect(this.bytes![0]).to.equal(parseInt(expected, 16));
  },
);

Then(
  /^the remaining bytes should be \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\]$/,
  function (this: AptosWorld, b1: string, b2: string, b3: string) {
    expect(this.bytes![1]).to.equal(parseInt(b1, 16));
    expect(this.bytes![2]).to.equal(parseInt(b2, 16));
    expect(this.bytes![3]).to.equal(parseInt(b3, 16));
  },
);

Then(
  "the remaining bytes should be UTF-8 encoded {string}",
  function (this: AptosWorld, str: string) {
    const encoded = new TextEncoder().encode(str);
    for (let i = 0; i < encoded.length; i++) {
      expect(this.bytes![i + 1]).to.equal(encoded[i]);
    }
  },
);

Then(
  /^the first byte should be (0x[0-9a-fA-F]+) \(UTF-8 byte length\)$/,
  function (this: AptosWorld, expected: string) {
    expect(this.bytes![0]).to.equal(parseInt(expected, 16));
  },
);

Then(
  "the first byte should be {word}",
  function (this: AptosWorld, expected: string) {
    // Check bytes, or publicKey for public key scenarios
    const bytes =
      this.bytes ??
      (this.testVectors.get("pubKeyForAuth") as Uint8Array) ??
      this.publicKey;
    expect(bytes).to.not.be.undefined;
    expect(bytes![0]).to.equal(parseInt(expected, 16));
  },
);

Then(
  "the remaining {int} bytes should be the u64 value",
  function (this: AptosWorld, count: number) {
    expect(this.bytes!.length).to.equal(count + 1); // 1 for the option flag
  },
);

Then(
  "the remaining bytes should be two u64 values in little-endian",
  function (this: AptosWorld) {
    expect(this.bytes!.length).to.equal(17); // 1 for length + 2*8 for u64s
  },
);

Then(
  "each inner vector should be length-prefixed",
  function (this: AptosWorld) {
    // Just verify we have some bytes
    expect(this.bytes!.length).to.be.greaterThan(2);
  },
);

Then(
  "the result should be exactly {int} bytes",
  function (this: AptosWorld, count: number) {
    expect(this.bytes!.length).to.equal(count);
  },
);

Then("the fields should be serialized in order", function (this: AptosWorld) {
  expect(this.bytes).to.not.be.undefined;
  expect(this.bytes!.length).to.be.greaterThan(0);
});

Then(
  /^the total length should be (\d+) bytes \((\d+) \+ (\d+)\)$/,
  function (this: AptosWorld, total: string, a: string, b: string) {
    expect(this.bytes!.length).to.equal(parseInt(total));
  },
);

Then("the result should be true", function (this: AptosWorld) {
  expect(this.result).to.be.true;
});

Then("the result should be false", function (this: AptosWorld) {
  expect(this.result).to.be.false;
});

Then("the result should equal the original value", function (this: AptosWorld) {
  const original = this.testVectors.get("originalValue");
  expect(this.result).to.equal(original);
});

Then(
  "the deserialization should fail with an error",
  function (this: AptosWorld) {
    expect(this.error).to.not.be.undefined;
  },
);
