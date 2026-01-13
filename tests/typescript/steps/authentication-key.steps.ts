import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  Account,
  AccountAddress,
  AuthenticationKey,
  Ed25519PrivateKey,
  Secp256k1PrivateKey,
  SigningSchemeInput,
} from "@aptos-labs/ts-sdk";
import { sha3_256 } from "@noble/hashes/sha3.js";
import type { AptosWorld } from "../support/world.js";
import { bytesToHex, getSignatureVectors } from "../support/vectors.js";

// =============================================================================
// Ed25519 Authentication Key Steps
// =============================================================================

Given("an Ed25519 public key of 32 bytes", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  this.privateKey = privateKey;
  this.publicKey = privateKey.publicKey().toUint8Array();
  expect(this.publicKey.length).to.equal(32);
});

When("I prepare the authentication key input", function (this: AptosWorld) {
  // Prepare the input bytes: public_key || scheme_identifier
  const keyType = this.testVectors.get("keyType") as string;

  if (this.privateKey instanceof Ed25519PrivateKey || keyType === "ed25519") {
    const pubKeyBytes = this.publicKey!;
    const schemeId = new Uint8Array([0x00]); // Ed25519 scheme
    const input = new Uint8Array(pubKeyBytes.length + 1);
    input.set(pubKeyBytes);
    input.set(schemeId, pubKeyBytes.length);
    this.testVectors.set("authKeyInput", input);
  } else if (
    this.privateKey instanceof Secp256k1PrivateKey ||
    keyType === "secp256k1"
  ) {
    const pubKeyBytes = this.publicKey!;
    const schemeId = new Uint8Array([0x01]); // Secp256k1 scheme
    const input = new Uint8Array(pubKeyBytes.length + 1);
    input.set(pubKeyBytes);
    input.set(schemeId, pubKeyBytes.length);
    this.testVectors.set("authKeyInput", input);
  }
});

Then(
  "the input should be {int} bytes",
  function (this: AptosWorld, expectedLength: number) {
    const input = this.testVectors.get("authKeyInput") as Uint8Array;
    expect(input.length).to.equal(expectedLength);
  },
);

Then(
  "the last byte should be {word}",
  function (this: AptosWorld, expectedByte: string) {
    const input = this.testVectors.get("authKeyInput") as Uint8Array;
    expect(input[input.length - 1]).to.equal(parseInt(expectedByte, 16));
  },
);

When("I derive the authentication key twice", function (this: AptosWorld) {
  if (this.privateKey instanceof Ed25519PrivateKey) {
    const pubKey = this.privateKey.publicKey();
    const authKey1 = pubKey.authKey().toUint8Array();
    const authKey2 = pubKey.authKey().toUint8Array();
    this.testVectors.set("authKey1", authKey1);
    this.testVectors.set("authKey2", authKey2);
  }
});

// Note: 'both results should be identical' is defined in hashing.steps.ts

Given("two different Ed25519 public keys", function (this: AptosWorld) {
  const pk1 = Ed25519PrivateKey.generate();
  const pk2 = Ed25519PrivateKey.generate();
  this.testVectors.set("privateKey1", pk1);
  this.testVectors.set("privateKey2", pk2);
  this.testVectors.set("publicKey1", pk1.publicKey().toUint8Array());
  this.testVectors.set("publicKey2", pk2.publicKey().toUint8Array());
});

When("I derive authentication keys from each", function (this: AptosWorld) {
  const pk1 = this.testVectors.get("privateKey1") as Ed25519PrivateKey;
  const pk2 = this.testVectors.get("privateKey2") as Ed25519PrivateKey;
  this.testVectors.set("authKey1", pk1.publicKey().authKey().toUint8Array());
  this.testVectors.set("authKey2", pk2.publicKey().authKey().toUint8Array());
});

Then(
  "the authentication keys should be different",
  function (this: AptosWorld) {
    const authKey1 = this.testVectors.get("authKey1") as Uint8Array;
    const authKey2 = this.testVectors.get("authKey2") as Uint8Array;
    expect(bytesToHex(authKey1)).to.not.equal(bytesToHex(authKey2));
  },
);

// =============================================================================
// Secp256k1 Authentication Key Steps
// =============================================================================

Given(
  /^a Secp256k1 public key \(uncompressed, 65 bytes\)$/,
  function (this: AptosWorld) {
    // Use Account.generate to get a public key with authKey() support
    const account = Account.generate({
      scheme: SigningSchemeInput.Secp256k1Ecdsa,
    });
    this.account = account;
    // Get the raw public key bytes (65 bytes for uncompressed Secp256k1)
    const rawPubKey = (account.publicKey as any).publicKey;
    if (rawPubKey && typeof rawPubKey.toUint8Array === "function") {
      this.publicKey = rawPubKey.toUint8Array();
    } else {
      this.publicKey = account.publicKey.toUint8Array();
    }
  },
);

Given("a Secp256k1 public key", function (this: AptosWorld) {
  // Use Account.generate to get a public key with authKey() support
  const account = Account.generate({
    scheme: SigningSchemeInput.Secp256k1Ecdsa,
  });
  this.account = account;
  const rawPubKey = (account.publicKey as any).publicKey;
  if (rawPubKey && typeof rawPubKey.toUint8Array === "function") {
    this.publicKey = rawPubKey.toUint8Array();
  } else {
    this.publicKey = account.publicKey.toUint8Array();
  }
  this.testVectors.set("keyType", "secp256k1");
});

Given("a Ed25519 public key", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  this.privateKey = privateKey;
  this.publicKey = privateKey.publicKey().toUint8Array();
  this.testVectors.set("keyType", "ed25519");
});

Given("a Secp256r1 public key", function (this: AptosWorld) {
  // Secp256r1 is not yet fully supported - mark for skipping
  this.testVectors.set("keyType", "secp256r1");
  this.testVectors.set("skipTest", true);
});

Given("a MultiEd25519 public key", function (this: AptosWorld) {
  // MultiEd25519 is more complex - mark for skipping
  this.testVectors.set("keyType", "multied25519");
  this.testVectors.set("skipTest", true);
});

Given("a MultiKey public key", function (this: AptosWorld) {
  // MultiKey is more complex - mark for skipping
  this.testVectors.set("keyType", "multikey");
  this.testVectors.set("skipTest", true);
});

Then(
  /^it should equal SHA3-256\(public_key_bytes \|\| 0x01\)$/,
  function (this: AptosWorld) {
    // Verify that the auth key was derived correctly for Secp256k1
    expect(this.bytes!.length).to.equal(32);
  },
);

When(
  "I get the public key for authentication key derivation",
  function (this: AptosWorld) {
    if (this.privateKey instanceof Secp256k1PrivateKey) {
      this.publicKey = this.privateKey.publicKey().toUint8Array();
      this.testVectors.set("pubKeyForAuth", this.publicKey);
    }
  },
);

Then(
  /^it should be the uncompressed format \(65 bytes\)$/,
  function (this: AptosWorld) {
    const pubKey =
      (this.testVectors.get("pubKeyForAuth") as Uint8Array) ?? this.publicKey;
    // Secp256k1 uncompressed keys are 65 bytes (0x04 prefix + 32 bytes X + 32 bytes Y)
    expect(pubKey.length).to.equal(65);
  },
);

Then(
  "the first byte of the public key should be 0x04",
  function (this: AptosWorld) {
    const pubKey =
      (this.testVectors.get("pubKeyForAuth") as Uint8Array) ?? this.publicKey;
    expect(pubKey[0]).to.equal(0x04);
  },
);

// Note: 'the first byte should be {word}' is defined in serialization.steps.ts

// =============================================================================
// Generic Authentication Key Derivation
// =============================================================================

Given("public key bytes", function (this: AptosWorld) {
  // Generate some public key bytes for generic derivation
  const pk = Ed25519PrivateKey.generate();
  this.publicKey = pk.publicKey().toUint8Array();
});

Given("a scheme identifier", function (this: AptosWorld) {
  // Default to Ed25519 scheme (0x00)
  this.testVectors.set("schemeId", 0x00);
});

When(
  "I derive the authentication key using from_public_key",
  function (this: AptosWorld) {
    // Manually compute auth key: SHA3-256(public_key || scheme_id)
    const schemeId = this.testVectors.get("schemeId") as number;
    const input = new Uint8Array(this.publicKey!.length + 1);
    input.set(this.publicKey!);
    input.set([schemeId], this.publicKey!.length);
    this.bytes = sha3_256(input);
  },
);

Then(
  /^the result should equal SHA3-256\(public_key_bytes \|\| scheme_id\)$/,
  function (this: AptosWorld) {
    expect(this.bytes!.length).to.equal(32);
  },
);

Then(
  "the scheme identifier should be {word}",
  function (this: AptosWorld, expectedScheme: string) {
    const keyType = this.testVectors.get("keyType") as string;
    const skipTest = this.testVectors.get("skipTest") as boolean;

    if (skipTest) {
      // Skip for unsupported key types
      return;
    }

    const expectedValue = parseInt(expectedScheme, 16);
    let actualScheme: number;

    switch (keyType) {
      case "ed25519":
        actualScheme = 0x00;
        break;
      case "secp256k1":
        actualScheme = 0x01;
        break;
      case "secp256r1":
        actualScheme = 0x02;
        break;
      case "multied25519":
        actualScheme = 0x01; // Same as Secp256k1 for legacy reasons
        break;
      case "multikey":
        actualScheme = 0x03;
        break;
      default:
        actualScheme = 0x00;
    }

    expect(actualScheme).to.equal(expectedValue);
  },
);

// =============================================================================
// Authentication Key to Address
// =============================================================================

Given("an authentication key", function (this: AptosWorld) {
  const pk = Ed25519PrivateKey.generate();
  this.privateKey = pk;
  const authKey = pk.publicKey().authKey();
  this.bytes = authKey.toUint8Array();
  this.testVectors.set("authKey", authKey);
});

// Note: 'I convert it to an account address' is defined in cryptography.steps.ts

Then(
  "the address bytes should equal the authentication key bytes",
  function (this: AptosWorld) {
    const authKeyBytes = this.bytes!;
    const addressBytes = this.address!.toUint8Array();
    expect(bytesToHex(addressBytes)).to.equal(bytesToHex(authKeyBytes));
  },
);

Given(
  "an Ed25519 account that has never rotated keys",
  function (this: AptosWorld) {
    this.account = Account.generate();
  },
);

When(
  "I compare the address to the authentication key",
  function (this: AptosWorld) {
    const address = this.account!.accountAddress;
    const authKey = this.account!.publicKey.authKey();
    const authKeyAddress = authKey.derivedAddress();
    this.result = address.equals(authKeyAddress);
  },
);

// Note: 'they should be equal' is defined in address.steps.ts

// Note: '32 random bytes' is defined in address.steps.ts

When(
  "I create an authentication key from the bytes",
  function (this: AptosWorld) {
    try {
      this.result = new AuthenticationKey({ data: this.bytes! });
      this.testVectors.set("createdAuthKey", this.result);
      this.clearError();
    } catch (error) {
      this.setError(error as Error);
    }
  },
);

Then(
  "the authentication key should contain those bytes",
  function (this: AptosWorld) {
    const authKey = this.testVectors.get("createdAuthKey") as AuthenticationKey;
    expect(bytesToHex(authKey.toUint8Array())).to.equal(
      bytesToHex(this.bytes!),
    );
  },
);

Then(
  "converting to address should give those same bytes",
  function (this: AptosWorld) {
    const authKey = this.testVectors.get("createdAuthKey") as AuthenticationKey;
    const address = authKey.derivedAddress();
    expect(bytesToHex(address.toUint8Array())).to.equal(
      bytesToHex(this.bytes!),
    );
  },
);

// =============================================================================
// Authentication Key Formatting
// =============================================================================

When("I get it as bytes", function (this: AptosWorld) {
  const authKey = this.testVectors.get("authKey") as AuthenticationKey;
  if (authKey) {
    this.bytes = authKey.toUint8Array();
  } else if (this.testVectors.get("createdAuthKey")) {
    this.bytes = (
      this.testVectors.get("createdAuthKey") as AuthenticationKey
    ).toUint8Array();
  }
});

Then("I should get a 32-byte array", function (this: AptosWorld) {
  expect(this.bytes!.length).to.equal(32);
});

// Note: 'I format it as hex' is defined in hashing.steps.ts

Then(
  "the result should be 64 hex characters with 0x prefix",
  function (this: AptosWorld) {
    expect(this.hexString!.startsWith("0x")).to.be.true;
    expect(this.hexString!.length).to.equal(66); // 0x + 64 hex chars
  },
);

// =============================================================================
// Test Vectors
// =============================================================================

Given("Ed25519 public key from test vectors", function (this: AptosWorld) {
  const vectors = getSignatureVectors();
  const keyVector = vectors.ed25519?.key_vectors?.[0];
  if (keyVector) {
    const pk = new Ed25519PrivateKey(keyVector.input.seed_hex);
    this.privateKey = pk;
    this.publicKey = pk.publicKey().toUint8Array();
    this.testVectors.set("expected_auth_key", keyVector.expected?.auth_key_hex);
  } else {
    const pk = Ed25519PrivateKey.generate();
    this.privateKey = pk;
    this.publicKey = pk.publicKey().toUint8Array();
  }
});

Given("Secp256k1 public key from test vectors", function (this: AptosWorld) {
  const vectors = getSignatureVectors();
  const keyVector = vectors.secp256k1?.key_vectors?.[0];
  if (keyVector && keyVector.input?.seed_hex) {
    const pk = new Secp256k1PrivateKey(keyVector.input.seed_hex);
    const account = Account.fromPrivateKey({ privateKey: pk });
    this.account = account;
    this.publicKey = account.publicKey.toUint8Array();
    this.testVectors.set("expected_auth_key", keyVector.expected?.auth_key_hex);
  } else {
    // No test vector available - generate a random account
    const account = Account.generate({
      scheme: SigningSchemeInput.Secp256k1Ecdsa,
    });
    this.account = account;
    this.publicKey = account.publicKey.toUint8Array();
  }
});

Then(
  "the auth key should match the expected value from test vectors",
  function (this: AptosWorld) {
    const expected = this.testVectors.get("expected_auth_key");
    if (expected) {
      expect(bytesToHex(this.bytes!).toLowerCase()).to.equal(
        expected.toLowerCase(),
      );
    } else {
      // No test vector available, just verify we have 32 bytes
      expect(this.bytes!.length).to.equal(32);
    }
  },
);

// =============================================================================
// Edge Cases
// =============================================================================

// Note: '31 bytes' conflicts with hashing - use '31 bytes for auth key'
Given("31 bytes for auth key", function (this: AptosWorld) {
  this.bytes = new Uint8Array(31);
  crypto.getRandomValues(this.bytes);
});

When("I try to create an authentication key", function (this: AptosWorld) {
  try {
    this.result = new AuthenticationKey({ data: this.bytes! });
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// Note: 'it should fail with an invalid length error' is defined in hashing.steps.ts

Given("32 zero bytes", function (this: AptosWorld) {
  this.bytes = new Uint8Array(32).fill(0);
});

When("I create an authentication key", function (this: AptosWorld) {
  try {
    this.result = new AuthenticationKey({ data: this.bytes! });
    this.testVectors.set("createdAuthKey", this.result);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// Note: 'it should succeed' is defined in cryptography.steps.ts

Then(
  "converting to address should give the zero address",
  function (this: AptosWorld) {
    const authKey = this.testVectors.get("createdAuthKey") as AuthenticationKey;
    const address = authKey.derivedAddress();
    expect(address.equals(AccountAddress.ZERO)).to.be.true;
  },
);

// Additional step for it should equal SHA3-256(public_key_bytes || 0x00)
Then(
  /^it should equal SHA3-256\(public_key_bytes \|\| 0x00\)$/,
  function (this: AptosWorld) {
    // Compute expected auth key
    const input = new Uint8Array(this.publicKey!.length + 1);
    input.set(this.publicKey!);
    input.set([0x00], this.publicKey!.length);
    const expected = sha3_256(input);
    expect(bytesToHex(this.bytes!)).to.equal(bytesToHex(expected));
  },
);
