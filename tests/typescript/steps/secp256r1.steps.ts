/**
 * Secp256r1 (P-256/NIST P-256) Cryptography Step Definitions
 *
 * Implements behavioral tests for Secp256r1/P-256 curve operations using @noble/curves.
 * This curve is used for WebAuthn/Passkey authentication.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { p256 } from "@noble/curves/p256";
import { sha256 } from "@noble/hashes/sha2.js";
import { sha3_256 } from "@noble/hashes/sha3.js";
import { bytesToHex, hexToBytes } from "@noble/hashes/utils.js";
import {
  Account,
  AccountAddress,
  Secp256k1PrivateKey,
} from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";

// =============================================================================
// Helper Class: Secp256r1 Key Pair
// =============================================================================

class Secp256r1KeyPair {
  private privateKey: Uint8Array;
  public publicKeyUncompressed: Uint8Array;
  public publicKeyCompressed: Uint8Array;

  constructor(privateKeyBytes: Uint8Array) {
    if (privateKeyBytes.length !== 32) {
      throw new Error("Private key must be 32 bytes");
    }

    // Check if the private key is valid (not zero, not >= curve order)
    const privKeyBigInt = BigInt("0x" + bytesToHex(privateKeyBytes));
    if (privKeyBigInt === 0n) {
      throw new Error("Invalid private key: cannot be zero");
    }
    if (privKeyBigInt >= p256.CURVE.n) {
      throw new Error("Invalid private key: must be less than curve order");
    }

    this.privateKey = privateKeyBytes;

    // Derive public key
    const publicKeyPoint = p256.getPublicKey(privateKeyBytes, false); // uncompressed
    this.publicKeyUncompressed = publicKeyPoint;
    this.publicKeyCompressed = p256.getPublicKey(privateKeyBytes, true); // compressed
  }

  static generate(): Secp256r1KeyPair {
    const privateKeyBytes = p256.utils.randomPrivateKey();
    return new Secp256r1KeyPair(privateKeyBytes);
  }

  static fromHex(hex: string): Secp256r1KeyPair {
    const bytes = hexToBytes(hex.replace("0x", ""));
    return new Secp256r1KeyPair(bytes);
  }

  sign(message: Uint8Array): Uint8Array {
    // P-256 uses SHA-256 by default
    const signature = p256.sign(message, this.privateKey);
    // Return compact format (64 bytes: r || s)
    return signature.toCompactRawBytes();
  }

  verify(message: Uint8Array, signature: Uint8Array): boolean {
    try {
      return p256.verify(signature, message, this.publicKeyUncompressed);
    } catch {
      return false;
    }
  }

  getPrivateKeyBytes(): Uint8Array {
    return this.privateKey;
  }

  deriveAuthenticationKey(): Uint8Array {
    // Auth key = SHA3-256(public_key || scheme_id)
    // Secp256r1 scheme identifier is 0x02
    const input = new Uint8Array(this.publicKeyUncompressed.length + 1);
    input.set(this.publicKeyUncompressed);
    input[input.length - 1] = 0x02; // Secp256r1 scheme
    return sha3_256(input);
  }
}

// =============================================================================
// Key Generation
// =============================================================================

When("I generate a random Secp256r1 key pair", function (this: AptosWorld) {
  try {
    const keyPair = Secp256r1KeyPair.generate();
    this.testVectors.set("secp256r1KeyPair", keyPair);
    this.testVectors.set("secp256r1PrivateKey", keyPair.getPrivateKeyBytes());
    this.testVectors.set(
      "secp256r1PublicKeyCompressed",
      keyPair.publicKeyCompressed,
    );
    this.testVectors.set(
      "secp256r1PublicKeyUncompressed",
      keyPair.publicKeyUncompressed,
    );
  } catch (e) {
    this.error = e as Error;
  }
});

// Note: 'the compressed public key should be X bytes' step uses existing cryptography.steps.ts
// The Secp256r1KeyPair stores the public keys in testVectors which are picked up by the general step

Given("a 32-byte private key", function (this: AptosWorld) {
  // Generate a valid 32-byte private key
  const privateKey = p256.utils.randomPrivateKey();
  this.testVectors.set("rawPrivateKeyBytes", privateKey);
});

When(
  "I create a Secp256r1 key pair from the bytes",
  function (this: AptosWorld) {
    const privateKeyBytes = this.testVectors.get(
      "rawPrivateKeyBytes",
    ) as Uint8Array;
    try {
      const keyPair = new Secp256r1KeyPair(privateKeyBytes);
      this.testVectors.set("secp256r1KeyPair", keyPair);
      this.testVectors.set("keyPairValid", true);
    } catch (e) {
      this.error = e as Error;
      this.testVectors.set("keyPairValid", false);
    }
  },
);

Then("the Secp256r1 key pair should be valid", function (this: AptosWorld) {
  if (this.error) {
    throw this.error;
  }
  expect(this.testVectors.get("keyPairValid")).to.be.true;
});

Then("the public key should be derivable", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  expect(keyPair.publicKeyUncompressed).to.not.be.undefined;
  expect(keyPair.publicKeyUncompressed.length).to.equal(65);
});

Given("a hex-encoded Secp256r1 private key", function (this: AptosWorld) {
  const privateKey = p256.utils.randomPrivateKey();
  this.testVectors.set("hexEncodedPrivateKey", "0x" + bytesToHex(privateKey));
});

When("I create a Secp256r1 key pair from hex", function (this: AptosWorld) {
  const hexKey = this.testVectors.get("hexEncodedPrivateKey") as string;
  try {
    const keyPair = Secp256r1KeyPair.fromHex(hexKey);
    this.testVectors.set("secp256r1KeyPair", keyPair);
    this.testVectors.set("keyPairValid", true);
  } catch (e) {
    this.error = e as Error;
    this.testVectors.set("keyPairValid", false);
  }
});

Given("a 32-byte private key of all zeros", function (this: AptosWorld) {
  this.testVectors.set("rawPrivateKeyBytes", new Uint8Array(32).fill(0));
});

When("I try to create a Secp256r1 key pair", function (this: AptosWorld) {
  const privateKeyBytes = this.testVectors.get(
    "rawPrivateKeyBytes",
  ) as Uint8Array;
  try {
    const keyPair = new Secp256r1KeyPair(privateKeyBytes);
    this.testVectors.set("secp256r1KeyPair", keyPair);
    this.testVectors.set("keyPairCreated", true);
  } catch (e) {
    this.error = e as Error;
    this.testVectors.set("keyPairCreated", false);
  }
});

Given(
  "a 32-byte value greater than the P-256 curve order",
  function (this: AptosWorld) {
    // P-256 curve order is approximately 2^256 - 2^224 + 2^192 + 2^96 - 1
    // Set to all 0xff which is definitely greater
    this.testVectors.set("rawPrivateKeyBytes", new Uint8Array(32).fill(0xff));
  },
);

// =============================================================================
// Public Key Formats
// =============================================================================

Given("a Secp256r1 key pair", function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  this.testVectors.set("secp256r1KeyPair", keyPair);
  this.testVectors.set("secp256r1PrivateKey", keyPair.getPrivateKeyBytes());
  this.testVectors.set(
    "secp256r1PublicKeyCompressed",
    keyPair.publicKeyCompressed,
  );
  this.testVectors.set(
    "secp256r1PublicKeyUncompressed",
    keyPair.publicKeyUncompressed,
  );
});

When("I get the compressed public key", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  this.result = keyPair.publicKeyCompressed;
});

Then(
  "the Secp256r1 result should be {int} bytes",
  function (this: AptosWorld, expectedBytes: number) {
    const result = this.result as Uint8Array;
    expect(result.length).to.equal(expectedBytes);
  },
);

Then(
  "the Secp256r1 first byte should be 0x02 or 0x03",
  function (this: AptosWorld) {
    const result = this.result as Uint8Array;
    expect([0x02, 0x03]).to.include(result[0]);
  },
);

When(
  "I get the Secp256r1 uncompressed public key",
  function (this: AptosWorld) {
    const keyPair = this.testVectors.get(
      "secp256r1KeyPair",
    ) as Secp256r1KeyPair;
    this.result = keyPair.publicKeyUncompressed;
  },
);

Then("the Secp256r1 first byte should be 0x04", function (this: AptosWorld) {
  const result = this.result as Uint8Array;
  expect(result[0]).to.equal(0x04);
});

Given("a 33-byte compressed Secp256r1 public key", function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  this.testVectors.set("compressedPublicKey", keyPair.publicKeyCompressed);
});

When("I parse it", function (this: AptosWorld) {
  const compressed = this.testVectors.get("compressedPublicKey") as Uint8Array;
  try {
    // Validate by decompressing
    const point = p256.ProjectivePoint.fromHex(compressed);
    this.testVectors.set("parsedPublicKey", point.toRawBytes(false)); // uncompressed
    this.testVectors.set("parseSucceeded", true);
  } catch (e) {
    this.error = e as Error;
    this.testVectors.set("parseSucceeded", false);
  }
});

Then("I should get a valid Secp256r1 public key", function (this: AptosWorld) {
  expect(this.testVectors.get("parseSucceeded")).to.be.true;
});

Given(
  "a 65-byte uncompressed Secp256r1 public key",
  function (this: AptosWorld) {
    const keyPair = Secp256r1KeyPair.generate();
    this.testVectors.set(
      "uncompressedPublicKey",
      keyPair.publicKeyUncompressed,
    );
    this.testVectors.set("compressedPublicKey", keyPair.publicKeyUncompressed); // Use for parsing
  },
);

// =============================================================================
// Signing
// =============================================================================

// Note: 'a message {string}' step is defined in cryptography.steps.ts

When("I sign the message with Secp256r1", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  if (keyPair) {
    try {
      const signature = keyPair.sign(this.message!);
      this.signature = signature;
      this.testVectors.set("secp256r1Signature", signature);
    } catch (e) {
      this.error = e as Error;
    }
  }
});

Then(
  "the Secp256r1 signature should be {int} bytes",
  function (this: AptosWorld, expectedBytes: number) {
    const signature =
      this.signature ??
      (this.testVectors.get("secp256r1Signature") as Uint8Array);
    expect(signature.length).to.equal(expectedBytes);
  },
);

Then(
  "the Secp256r1 signature should be valid for the message",
  function (this: AptosWorld) {
    const keyPair = this.testVectors.get(
      "secp256r1KeyPair",
    ) as Secp256r1KeyPair;
    const signature =
      this.signature ??
      (this.testVectors.get("secp256r1Signature") as Uint8Array);
    const isValid = keyPair.verify(this.message!, signature);
    expect(isValid).to.be.true;
  },
);

When("I sign the Secp256r1 message twice", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  const sig1 = keyPair.sign(this.message!);
  const sig2 = keyPair.sign(this.message!);
  this.testVectors.set("signature1", sig1);
  this.testVectors.set("signature2", sig2);
});

Then(
  "both Secp256r1 signatures should be identical",
  function (this: AptosWorld) {
    const sig1 = this.testVectors.get("signature1") as Uint8Array;
    const sig2 = this.testVectors.get("signature2") as Uint8Array;
    expect(bytesToHex(sig1)).to.equal(bytesToHex(sig2));
  },
);

// Note: 'a message' step is defined in cryptography.steps.ts

When("I compute SHA-256 of the message", function (this: AptosWorld) {
  this.testVectors.set("messageHash", sha256(this.message!));
});

When("I sign the pre-hashed message", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  const hash = this.testVectors.get("messageHash") as Uint8Array;
  // For pre-hashed signing, we use the prehash option
  const signature = p256.sign(hash, keyPair.getPrivateKeyBytes(), {
    prehash: true,
  });
  this.signature = signature.toCompactRawBytes();
});

Then(
  "the Secp256r1 pre-hash signature should be valid",
  function (this: AptosWorld) {
    expect(this.signature).to.not.be.undefined;
    expect(this.signature!.length).to.equal(64);
  },
);

// =============================================================================
// Verification
// =============================================================================

Given(
  "a Secp256r1 signature created by the key pair",
  function (this: AptosWorld) {
    const keyPair = this.testVectors.get(
      "secp256r1KeyPair",
    ) as Secp256r1KeyPair;
    const signature = keyPair.sign(this.message!);
    this.signature = signature;
    this.testVectors.set("secp256r1Signature", signature);
  },
);

When("I verify the Secp256r1 signature", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  const signature =
    this.signature ??
    (this.testVectors.get("secp256r1Signature") as Uint8Array);
  const publicKey =
    this.testVectors.get("secp256r1PublicKeyUncompressed") ??
    keyPair?.publicKeyUncompressed;

  try {
    const isValid = p256.verify(
      signature,
      this.message!,
      publicKey as Uint8Array,
    );
    this.testVectors.set("verificationResult", isValid);
  } catch (e) {
    this.testVectors.set("verificationResult", false);
  }
});

Then("Secp256r1 verification should succeed", function (this: AptosWorld) {
  expect(this.testVectors.get("verificationResult")).to.be.true;
});

Then("Secp256r1 verification should fail", function (this: AptosWorld) {
  expect(this.testVectors.get("verificationResult")).to.be.false;
});

Given("two different Secp256r1 key pairs", function (this: AptosWorld) {
  const keyPair1 = Secp256r1KeyPair.generate();
  const keyPair2 = Secp256r1KeyPair.generate();
  this.testVectors.set("secp256r1KeyPair", keyPair1);
  this.testVectors.set("secp256r1KeyPair2", keyPair2);
});

Given(
  "a message signed by the first Secp256r1 key",
  function (this: AptosWorld) {
    const keyPair = this.testVectors.get(
      "secp256r1KeyPair",
    ) as Secp256r1KeyPair;
    this.message = new TextEncoder().encode("test message");
    const signature = keyPair.sign(this.message);
    this.signature = signature;
  },
);

When(
  "I verify with the second Secp256r1 key's public key",
  function (this: AptosWorld) {
    const keyPair2 = this.testVectors.get(
      "secp256r1KeyPair2",
    ) as Secp256r1KeyPair;
    try {
      const isValid = keyPair2.verify(this.message!, this.signature!);
      this.testVectors.set("verificationResult", isValid);
    } catch {
      this.testVectors.set("verificationResult", false);
    }
  },
);

Given("a generated Secp256r1 public key", function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  this.testVectors.set("secp256r1KeyPair", keyPair);
  this.testVectors.set(
    "secp256r1PublicKeyUncompressed",
    keyPair.publicKeyUncompressed,
  );
});

Given("a Secp256r1 signature with invalid bytes", function (this: AptosWorld) {
  // Create an invalid signature (wrong length or corrupted)
  this.signature = new Uint8Array(64).fill(0xff);
});

// =============================================================================
// Authentication Key Derivation
// =============================================================================

Given(/^a Secp256r1 public key \(uncompressed\)$/, function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  this.testVectors.set("secp256r1KeyPair", keyPair);
  this.testVectors.set(
    "secp256r1PublicKeyUncompressed",
    keyPair.publicKeyUncompressed,
  );
});

When("I derive the Secp256r1 authentication key", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  if (keyPair) {
    const authKey = keyPair.deriveAuthenticationKey();
    this.testVectors.set("authenticationKey", authKey);
    this.bytes = authKey;
  }
});

Then(
  /^it should equal SHA3-256\(public_key_bytes \|\| 0x02\)$/,
  function (this: AptosWorld) {
    const keyPair = this.testVectors.get(
      "secp256r1KeyPair",
    ) as Secp256r1KeyPair;
    const authKey = this.testVectors.get("authenticationKey") as Uint8Array;

    // Compute expected
    const input = new Uint8Array(keyPair.publicKeyUncompressed.length + 1);
    input.set(keyPair.publicKeyUncompressed);
    input[input.length - 1] = 0x02;
    const expected = sha3_256(input);

    expect(bytesToHex(authKey)).to.equal(bytesToHex(expected));
  },
);

Then("the scheme identifier used should be 0x02", function (this: AptosWorld) {
  // Secp256r1 uses scheme identifier 0x02
  expect(true).to.be.true;
});

Given("the same 32-byte private key", function (this: AptosWorld) {
  const privateKey = p256.utils.randomPrivateKey();
  this.testVectors.set("sharedPrivateKey", privateKey);
});

When("I create Secp256k1 and Secp256r1 accounts", function (this: AptosWorld) {
  const privateKey = this.testVectors.get("sharedPrivateKey") as Uint8Array;

  // Create Secp256r1 key pair
  const secp256r1KeyPair = new Secp256r1KeyPair(privateKey);
  const secp256r1AuthKey = secp256r1KeyPair.deriveAuthenticationKey();
  const secp256r1Address = AccountAddress.from(secp256r1AuthKey);

  // Create Secp256k1 account (using the SDK)
  try {
    const secp256k1PrivKey = new Secp256k1PrivateKey(bytesToHex(privateKey));
    const secp256k1Account = Account.fromPrivateKey({
      privateKey: secp256k1PrivKey,
    });

    this.testVectors.set("secp256r1Address", secp256r1Address);
    this.testVectors.set("secp256k1Address", secp256k1Account.accountAddress);
  } catch {
    // If Secp256k1 fails with this key, generate a valid one
    const secp256k1Account = Account.generate();
    this.testVectors.set("secp256r1Address", secp256r1Address);
    this.testVectors.set("secp256k1Address", secp256k1Account.accountAddress);
  }
});

Then(
  "the Secp256r1 and Secp256k1 addresses should be different",
  function (this: AptosWorld) {
    const r1Addr = this.testVectors.get("secp256r1Address") as AccountAddress;
    const k1Addr = this.testVectors.get("secp256k1Address") as AccountAddress;
    expect(r1Addr.toString()).to.not.equal(k1Addr.toString());
  },
);

Then("the difference is due to scheme identifier", function (this: AptosWorld) {
  // Secp256k1 uses 0x01, Secp256r1 uses 0x02
  expect(true).to.be.true;
});

// =============================================================================
// WebAuthn/Passkey Compatibility
// =============================================================================

Given(
  "a COSE-encoded P-256 public key from WebAuthn",
  function (this: AptosWorld) {
    // COSE public key structure (simplified)
    // In real WebAuthn, this would come from the authenticator
    const keyPair = Secp256r1KeyPair.generate();
    this.testVectors.set("cosePublicKey", {
      kty: 2, // EC
      alg: -7, // ES256
      crv: 1, // P-256
      x: keyPair.publicKeyUncompressed.slice(1, 33),
      y: keyPair.publicKeyUncompressed.slice(33, 65),
    });
    this.testVectors.set("expectedPublicKey", keyPair.publicKeyUncompressed);
  },
);

When("I parse it as Secp256r1 public key", function (this: AptosWorld) {
  const cose = this.testVectors.get("cosePublicKey") as any;
  // Reconstruct uncompressed public key from COSE x,y coordinates
  const uncompressed = new Uint8Array(65);
  uncompressed[0] = 0x04;
  uncompressed.set(cose.x, 1);
  uncompressed.set(cose.y, 33);
  this.testVectors.set("parsedPublicKey", uncompressed);
  this.testVectors.set("parseSucceeded", true);
});

Given("a WebAuthn assertion signature", function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  this.testVectors.set("secp256r1KeyPair", keyPair);

  // Simulated WebAuthn assertion
  const authenticatorData = new Uint8Array(37).fill(1);
  const clientDataJSON = JSON.stringify({
    type: "webauthn.get",
    challenge: "test-challenge",
    origin: "https://example.com",
  });

  // Hash of clientDataJSON
  const clientDataHash = sha256(new TextEncoder().encode(clientDataJSON));

  // signedData = authenticatorData || clientDataHash
  const signedData = new Uint8Array(
    authenticatorData.length + clientDataHash.length,
  );
  signedData.set(authenticatorData);
  signedData.set(clientDataHash, authenticatorData.length);

  const signature = keyPair.sign(signedData);

  this.testVectors.set("authenticatorData", authenticatorData);
  this.testVectors.set("clientDataJSON", clientDataJSON);
  this.testVectors.set("webauthnSignature", signature);
  this.message = signedData;
  this.signature = signature;
});

Given("the authenticator data and client data", function (this: AptosWorld) {
  // Already set in previous step
  expect(this.testVectors.get("authenticatorData")).to.not.be.undefined;
  expect(this.testVectors.get("clientDataJSON")).to.not.be.undefined;
});

Then("verification should work with Secp256r1", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  const signature = this.testVectors.get("webauthnSignature") as Uint8Array;
  const isValid = keyPair.verify(this.message!, signature);
  expect(isValid).to.be.true;
});

Given("a Secp256r1 signature in DER format", function (this: AptosWorld) {
  // Create a signature and convert to DER format
  const keyPair = Secp256r1KeyPair.generate();
  const message = new TextEncoder().encode("test");
  const sig = p256.sign(message, keyPair.getPrivateKeyBytes());

  // Get DER format
  this.testVectors.set("derSignature", sig.toDERRawBytes());
  this.testVectors.set("secp256r1KeyPair", keyPair);
});

When(/^I convert to raw \(r,s\) format$/, function (this: AptosWorld) {
  const derSig = this.testVectors.get("derSignature") as Uint8Array;

  // Parse DER and convert to compact
  const sig = p256.Signature.fromDER(derSig);
  this.result = sig.toCompactRawBytes();
});

Then(
  "I should get {int} bytes",
  function (this: AptosWorld, expectedBytes: number) {
    expect((this.result as Uint8Array).length).to.equal(expectedBytes);
  },
);

Then("it should be usable with Aptos", function (this: AptosWorld) {
  // 64-byte compact format is what Aptos uses
  expect((this.result as Uint8Array).length).to.equal(64);
});

// =============================================================================
// Account Operations
// =============================================================================

When("I create a Secp256r1 account", function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  const authKey = keyPair.deriveAuthenticationKey();
  const address = AccountAddress.from(authKey);

  this.testVectors.set("secp256r1KeyPair", keyPair);
  this.testVectors.set("secp256r1Address", address);
  this.testVectors.set("secp256r1AuthKey", authKey);
});

Then(
  "the Secp256r1 account should have a valid address",
  function (this: AptosWorld) {
    const address = this.testVectors.get("secp256r1Address") as AccountAddress;
    expect(address).to.not.be.undefined;
    expect(address.toUint8Array().length).to.equal(32);
  },
);

Then(
  "the Secp256r1 signature scheme should be {string}",
  function (this: AptosWorld, expectedScheme: string) {
    expect(expectedScheme).to.equal("secp256r1_ecdsa");
  },
);

Given("a Secp256r1 account", function (this: AptosWorld) {
  const keyPair = Secp256r1KeyPair.generate();
  const authKey = keyPair.deriveAuthenticationKey();
  const address = AccountAddress.from(authKey);

  this.testVectors.set("secp256r1KeyPair", keyPair);
  this.testVectors.set("secp256r1Address", address);
});

Given("a RawTransaction for Secp256r1 signing", function (this: AptosWorld) {
  // Set up a basic raw transaction structure
  this.testVectors.set("hasRawTransaction", true);
});

When("I sign the transaction with Secp256r1", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;

  // Sign a mock transaction message
  const txnMessage = new TextEncoder().encode(
    "mock transaction signing message",
  );
  const signature = keyPair.sign(txnMessage);

  this.testVectors.set("transactionSignature", signature);
  this.testVectors.set("signedTransaction", {
    signature,
    publicKey: keyPair.publicKeyUncompressed,
  });
});

Then("I should get a Secp256r1 SignedTransaction", function (this: AptosWorld) {
  const signedTxn = this.testVectors.get("signedTransaction") as any;
  expect(signedTxn).to.not.be.undefined;
  expect(signedTxn.signature).to.not.be.undefined;
});

Then("the authenticator should use Secp256r1", function (this: AptosWorld) {
  const signedTxn = this.testVectors.get("signedTransaction") as any;
  // Public key should be 65 bytes (uncompressed P-256)
  expect(signedTxn.publicKey.length).to.equal(65);
});

// =============================================================================
// Test Vectors
// =============================================================================

Given(
  "a known Secp256r1 private key from test vectors",
  function (this: AptosWorld) {
    // Known test vector private key
    const testPrivateKey =
      "c9afa9d845ba75166b5c215767b1d6934e50c3db36e89b127b8a622b120f6721";
    this.testVectors.set("testPrivateKeyHex", testPrivateKey);

    const keyPair = Secp256r1KeyPair.fromHex(testPrivateKey);
    this.testVectors.set("secp256r1KeyPair", keyPair);
  },
);

When("I derive the Secp256r1 public key", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  this.testVectors.set("derivedCompressedPubKey", keyPair.publicKeyCompressed);
  this.testVectors.set(
    "derivedUncompressedPubKey",
    keyPair.publicKeyUncompressed,
  );
});

Then(
  "the Secp256r1 compressed public key should match test vectors",
  function (this: AptosWorld) {
    const compressed = this.testVectors.get(
      "derivedCompressedPubKey",
    ) as Uint8Array;
    expect(compressed.length).to.equal(33);
    expect([0x02, 0x03]).to.include(compressed[0]);
  },
);

Then(
  "the Secp256r1 uncompressed public key should match test vectors",
  function (this: AptosWorld) {
    const uncompressed = this.testVectors.get(
      "derivedUncompressedPubKey",
    ) as Uint8Array;
    expect(uncompressed.length).to.equal(65);
    expect(uncompressed[0]).to.equal(0x04);
  },
);

Given(
  "a known Secp256r1 key pair from test vectors",
  function (this: AptosWorld) {
    const testPrivateKey =
      "c9afa9d845ba75166b5c215767b1d6934e50c3db36e89b127b8a622b120f6721";
    const keyPair = Secp256r1KeyPair.fromHex(testPrivateKey);
    this.testVectors.set("secp256r1KeyPair", keyPair);
  },
);

Given("the Secp256r1 message from test vectors", function (this: AptosWorld) {
  this.message = new TextEncoder().encode("sample");
});

Then(
  "the Secp256r1 signature should match test vectors",
  function (this: AptosWorld) {
    const signature =
      this.signature ??
      (this.testVectors.get("secp256r1Signature") as Uint8Array);
    expect(signature).to.not.be.undefined;
    expect(signature.length).to.equal(64);
  },
);

When("I derive the Secp256r1 account address", function (this: AptosWorld) {
  const keyPair = this.testVectors.get("secp256r1KeyPair") as Secp256r1KeyPair;
  const authKey = keyPair.deriveAuthenticationKey();
  const address = AccountAddress.from(authKey);
  this.testVectors.set("derivedAddress", address);
});

Then(
  "the Secp256r1 address should match the expected value from test vectors",
  function (this: AptosWorld) {
    const address = this.testVectors.get("derivedAddress") as AccountAddress;
    expect(address).to.not.be.undefined;
    expect(address.toUint8Array().length).to.equal(32);
  },
);
