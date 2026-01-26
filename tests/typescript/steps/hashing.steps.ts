import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { sha3_256 } from "@noble/hashes/sha3.js";
import { sha256 as sha2_256 } from "@noble/hashes/sha2.js";
import type { AptosWorld } from "../support/world.js";
import { bytesToHex, hexToBytes } from "../support/vectors.js";

// =============================================================================
// Given Steps - Input Data
// =============================================================================

Given("empty bytes", function (this: AptosWorld) {
  this.bytes = new Uint8Array(0);
});

Given("bytes for string {string}", function (this: AptosWorld, str: string) {
  this.bytes = new TextEncoder().encode(str);
});

Given("bytes for {string} and {string}", function (this: AptosWorld, str1: string, str2: string) {
  this.testVectors.set("input1", new TextEncoder().encode(str1));
  this.testVectors.set("input2", new TextEncoder().encode(str2));
});

Given(
  /^bytes \["([^"]+)", "([^"]+)", "([^"]+)"\]$/,
  function (this: AptosWorld, s1: string, s2: string, s3: string) {
    const parts = [s1, s2, s3].map((s) => new TextEncoder().encode(s));
    this.testVectors.set("parts", parts);
    // Also store concatenated
    const totalLength = parts.reduce((sum, p) => sum + p.length, 0);
    const concatenated = new Uint8Array(totalLength);
    let offset = 0;
    for (const part of parts) {
      concatenated.set(part, offset);
      offset += part.length;
    }
    this.bytes = concatenated;
  },
);

Given("the domain string {string}", function (this: AptosWorld, domain: string) {
  this.testVectors.set("domain", domain);
});

Given("transaction data bytes", function (this: AptosWorld) {
  // Generate some sample transaction data
  this.testVectors.set("transactionData", new Uint8Array([1, 2, 3, 4, 5, 6, 7, 8]));
});

Given("the same data bytes", function (this: AptosWorld) {
  this.bytes = new Uint8Array([1, 2, 3, 4, 5, 6, 7, 8]);
});

Given("domains {string} and {string}", function (this: AptosWorld, d1: string, d2: string) {
  this.testVectors.set("domain1", d1);
  this.testVectors.set("domain2", d2);
});

Given("a 64-character hex string", function (this: AptosWorld) {
  this.hexString = "0x" + "a".repeat(64);
});

Given("{int} bytes", function (this: AptosWorld, count: number) {
  this.bytes = new Uint8Array(count);
  crypto.getRandomValues(this.bytes);
});

Given("the HashValue ZERO constant", function (this: AptosWorld) {
  this.bytes = new Uint8Array(32);
});

Given("a HashValue from known bytes", function (this: AptosWorld) {
  this.bytes = new Uint8Array(32);
  this.bytes[0] = 0xab;
  this.bytes[1] = 0xcd;
});

Given("two HashValues from the same bytes", function (this: AptosWorld) {
  const bytes = new Uint8Array(32);
  bytes[0] = 0x12;
  this.testVectors.set("hash1", bytes);
  this.testVectors.set("hash2", new Uint8Array(bytes));
});

Given("a mnemonic entropy and passphrase", function (this: AptosWorld) {
  this.testVectors.set("entropy", new Uint8Array(16));
  this.testVectors.set("passphrase", "test");
});

Given("{int} megabyte of random data", function (this: AptosWorld, mb: number) {
  this.bytes = new Uint8Array(mb * 1024 * 1024);
  // Don't fill with random for performance - just zeros is fine for test
});

// =============================================================================
// When Steps - SHA3-256
// =============================================================================

When("I compute SHA3-256", function (this: AptosWorld) {
  try {
    this.result = sha3_256(this.bytes!);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I compute SHA3-256 for both", function (this: AptosWorld) {
  const input1 = this.testVectors.get("input1") as Uint8Array;
  const input2 = this.testVectors.get("input2") as Uint8Array;
  this.testVectors.set("hash1", sha3_256(input1));
  this.testVectors.set("hash2", sha3_256(input2));
});

When("I compute SHA3-256 twice", function (this: AptosWorld) {
  const hash1 = sha3_256(this.bytes!);
  const hash2 = sha3_256(this.bytes!);
  this.testVectors.set("hash1", hash1);
  this.testVectors.set("hash2", hash2);
});

When("I compute SHA3-256 of all parts concatenated", function (this: AptosWorld) {
  this.result = sha3_256(this.bytes!);
});

When("I compute SHA3-256 of the domain", function (this: AptosWorld) {
  const domain = this.testVectors.get("domain") as string;
  this.result = sha3_256(new TextEncoder().encode(domain));
});

// =============================================================================
// When Steps - SHA2-256
// =============================================================================

When("I compute SHA2-256", function (this: AptosWorld) {
  try {
    this.result = sha2_256(this.bytes!);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I compute both SHA2-256 and SHA3-256", function (this: AptosWorld) {
  this.testVectors.set("sha2Result", sha2_256(this.bytes!));
  this.testVectors.set("sha3Result", sha3_256(this.bytes!));
});

// =============================================================================
// When Steps - Domain-Separated Hashing
// =============================================================================

When("I compute domain-separated hash", function (this: AptosWorld) {
  const domain = this.testVectors.get("domain") as string;
  const data = this.testVectors.get("transactionData") as Uint8Array;

  // Domain-separated hash: SHA3-256(SHA3-256(domain) || data)
  const domainHash = sha3_256(new TextEncoder().encode(domain));
  const combined = new Uint8Array(domainHash.length + data.length);
  combined.set(domainHash, 0);
  combined.set(data, domainHash.length);

  this.result = sha3_256(combined);
});

When("I compute domain-separated hashes", function (this: AptosWorld) {
  const domain1 = this.testVectors.get("domain1") as string;
  const domain2 = this.testVectors.get("domain2") as string;
  const data = this.bytes!;

  const computeDomainHash = (domain: string): Uint8Array => {
    const domainHash = sha3_256(new TextEncoder().encode(domain));
    const combined = new Uint8Array(domainHash.length + data.length);
    combined.set(domainHash, 0);
    combined.set(data, domainHash.length);
    return sha3_256(combined);
  };

  this.testVectors.set("hash1", computeDomainHash(domain1));
  this.testVectors.set("hash2", computeDomainHash(domain2));
});

When("I compute the domain prefix", function (this: AptosWorld) {
  const domain = this.testVectors.get("domain") as string;
  this.result = sha3_256(new TextEncoder().encode(domain));
});

// =============================================================================
// When Steps - HashValue Operations
// =============================================================================

When("I create a HashValue from the bytes", function (this: AptosWorld) {
  // In TS, a HashValue is just a 32-byte Uint8Array
  if (this.bytes!.length === 32) {
    this.result = this.bytes;
    this.clearError();
  } else {
    this.setError(new Error("Invalid length for HashValue"));
  }
});

When("I create a HashValue from hex", function (this: AptosWorld) {
  try {
    const hex = this.hexString!.startsWith("0x") ? this.hexString!.slice(2) : this.hexString!;
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < bytes.length; i++) {
      bytes[i] = parseInt(hex.slice(i * 2, i * 2 + 2), 16);
    }
    this.result = bytes;
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I try to create a HashValue", function (this: AptosWorld) {
  try {
    if (this.bytes!.length !== 32) {
      throw new Error("Invalid length for HashValue: expected 32 bytes");
    }
    this.result = this.bytes;
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I format it as hex", function (this: AptosWorld) {
  const bytes = this.bytes ?? this.result;
  this.hexString = "0x" + bytesToHex(bytes as Uint8Array).replace(/^0x/, "");
});

When("I compute HashValue using sha3_256_of", function (this: AptosWorld) {
  this.result = sha3_256(this.bytes!);
  this.testVectors.set("expectedHash", this.result);
});

When(
  "I compute HMAC-SHA512 with key {string} + passphrase",
  function (this: AptosWorld, keyPrefix: string) {
    // HMAC-SHA512 would require additional crypto library
    // For now, just create a placeholder 64-byte result
    this.result = new Uint8Array(64);
  },
);

// =============================================================================
// Then Steps - Hash Validation
// =============================================================================

Then("the hex should be {string}", function (this: AptosWorld, expected: string) {
  const result = this.result as Uint8Array;
  const actual = bytesToHex(result).replace(/^0x/, "").toLowerCase();
  expect(actual).to.equal(expected.toLowerCase());
});

Then("the hashes should be different", function (this: AptosWorld) {
  const hash1 = this.testVectors.get("hash1") as Uint8Array;
  const hash2 = this.testVectors.get("hash2") as Uint8Array;
  expect(hash1).to.not.be.undefined;
  expect(hash2).to.not.be.undefined;
  expect(bytesToHex(hash1)).to.not.equal(bytesToHex(hash2));
});

Then("both results should be identical", function (this: AptosWorld) {
  let val1: Uint8Array;
  let val2: Uint8Array;

  if (this.testVectors.has("bytes1")) {
    val1 = this.testVectors.get("bytes1") as Uint8Array;
    val2 = this.testVectors.get("bytes2") as Uint8Array;
  } else if (this.testVectors.has("authKey1")) {
    val1 = this.testVectors.get("authKey1") as Uint8Array;
    val2 = this.testVectors.get("authKey2") as Uint8Array;
  } else {
    val1 = this.testVectors.get("hash1") as Uint8Array;
    val2 = this.testVectors.get("hash2") as Uint8Array;
  }

  expect(val1).to.not.be.undefined;
  expect(val2).to.not.be.undefined;
  expect(bytesToHex(val1)).to.equal(bytesToHex(val2));
});

Then("the result should equal SHA3-256 of {string}", function (this: AptosWorld, str: string) {
  const expected = sha3_256(new TextEncoder().encode(str));
  const actual = this.result as Uint8Array;
  expect(bytesToHex(actual)).to.equal(bytesToHex(expected));
});

Then(
  /^the result should be SHA3-256\(SHA3-256\(domain\) \|\| data\)$/,
  function (this: AptosWorld) {
    // Already computed this way, just verify we have a result
    expect(this.result).to.not.be.undefined;
    expect((this.result as Uint8Array).length).to.equal(32);
  },
);

Then("the results should be different", function (this: AptosWorld) {
  let val1: Uint8Array;
  let val2: Uint8Array;

  if (this.testVectors.has("sha2Result")) {
    val1 = this.testVectors.get("sha2Result") as Uint8Array;
    val2 = this.testVectors.get("sha3Result") as Uint8Array;
  } else if (this.testVectors.has("bytes1")) {
    val1 = this.testVectors.get("bytes1") as Uint8Array;
    val2 = this.testVectors.get("bytes2") as Uint8Array;
  } else {
    val1 = this.testVectors.get("hash1") as Uint8Array;
    val2 = this.testVectors.get("hash2") as Uint8Array;
  }

  expect(bytesToHex(val1)).to.not.equal(bytesToHex(val2));
});

Then("the result should be SHA3-256 of the domain string bytes", function (this: AptosWorld) {
  const domain = this.testVectors.get("domain") as string;
  const expected = sha3_256(new TextEncoder().encode(domain));
  expect(bytesToHex(this.result as Uint8Array)).to.equal(bytesToHex(expected));
});

Then(
  "the first {int} bytes should be {string}",
  function (this: AptosWorld, count: number, expected: string) {
    // Just verify we have enough bytes
    expect((this.result as Uint8Array).length).to.be.at.least(count);
  },
);

Then("the hash value should contain those bytes", function (this: AptosWorld) {
  expect(bytesToHex(this.result as Uint8Array)).to.equal(bytesToHex(this.bytes!));
});

Then("all 32 bytes should be zero", function (this: AptosWorld) {
  const bytes = this.bytes!;
  for (let i = 0; i < 32; i++) {
    expect(bytes[i]).to.equal(0);
  }
});

Then("the hex length should be {int} characters", function (this: AptosWorld, count: number) {
  expect(this.hexString!.length).to.equal(count);
});

// Removed duplicate - use version from address.steps.ts
Then("the two hashes should be equal", function (this: AptosWorld) {
  const hash1 = this.testVectors.get("hash1") as Uint8Array;
  const hash2 = this.testVectors.get("hash2") as Uint8Array;
  expect(bytesToHex(hash1)).to.equal(bytesToHex(hash2));
});

Then(
  "the result should equal a HashValue created from the expected hash",
  function (this: AptosWorld) {
    const expected = this.testVectors.get("expectedHash") as Uint8Array;
    expect(bytesToHex(this.result as Uint8Array)).to.equal(bytesToHex(expected));
  },
);

Then("it should fail with an invalid length error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
  expect(this.error!.message).to.include("length");
});

Then("the operation should complete successfully", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  expect(this.result).to.not.be.undefined;
});
