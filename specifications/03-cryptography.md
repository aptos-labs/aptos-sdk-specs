# Cryptography Specification

## Abstract

This document specifies the cryptographic primitives required for Aptos SDK implementations,
including key generation, signing, verification, and hashing. Ed25519 is the primary required
signature scheme, with additional schemes available for specific use cases.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Ed25519](#2-ed25519)
3. [Secp256k1 ECDSA](#3-secp256k1-ecdsa)
4. [Secp256r1 / P-256](#4-secp256r1--p-256)
5. [BLS12-381](#5-bls12-381)
6. [Hashing](#6-hashing)
7. [Authentication Key Derivation](#7-authentication-key-derivation)
8. [Key Derivation (BIP-39/BIP-44)](#8-key-derivation-bip-39bip-44)
9. [Test Vectors](#9-test-vectors)
10. [Security Considerations](#10-security-considerations)
11. [References](#11-references)

---

## 1. Introduction

### 1.1 Purpose

Cryptographic operations are fundamental to Aptos SDK functionality, enabling secure key management,
transaction signing, and identity verification. This specification ensures consistent cryptographic
behavior across all SDK implementations.

### 1.2 Scope

This specification covers:
- Ed25519 signature scheme (required)
- Secp256k1 ECDSA signature scheme (preferred)
- Secp256r1/P-256 for WebAuthn compatibility (optional)
- BLS12-381 for aggregatable signatures (optional)
- SHA3-256 and SHA2-256 hashing
- Authentication key derivation
- BIP-39/BIP-44 key derivation

### 1.3 Definitions

| Term              | Definition                                              |
| ----------------- | ------------------------------------------------------- |
| Private Key       | Secret key used for signing                             |
| Public Key        | Derived from private key, used for verification         |
| Signature         | Cryptographic proof of private key possession           |
| Authentication Key| Hash of public key with scheme identifier               |
| CSPRNG            | Cryptographically Secure Pseudo-Random Number Generator |

---

## 2. Ed25519

### 2.1 Overview

Ed25519 is the primary signature scheme for Aptos accounts. It uses the Edwards-curve Digital
Signature Algorithm with Curve25519.

**Priority: P0 (Required)**

### 2.2 Key Sizes

| Component              | Size     | Description                         |
| ---------------------- | -------- | ----------------------------------- |
| Private Key (Seed)     | 32 bytes | Random seed                         |
| Private Key (Extended) | 64 bytes | Seed concatenated with public key   |
| Public Key             | 32 bytes | Compressed Edwards point            |
| Signature              | 64 bytes | (R, s) pair                         |

### 2.3 Key Generation [P0]

#### 2.3.1 Random Generation

**Signature:**
```
generate() -> (PrivateKey, PublicKey)
```

**Requirements:**

1. Implementation **MUST** use a CSPRNG for seed generation
2. Implementation **MUST** generate a 32-byte random seed
3. Implementation **MUST** derive the public key from the seed

#### 2.3.2 From Seed

**Signature:**
```
from_seed(seed: [u8; 32]) -> (PrivateKey, PublicKey)
```

**Requirements:**

1. Implementation **MUST** accept exactly 32 bytes
2. Same seed **MUST** always produce the same key pair
3. Invalid seed length **MUST** cause an error

#### 2.3.3 From Bytes

**Signature:**
```
from_bytes(bytes: [u8; 64]) -> (PrivateKey, PublicKey)
```

**Requirements:**

1. Implementation **MUST** accept 64-byte extended private key
2. Bytes 0-31 are the seed, bytes 32-63 are the public key
3. Implementation **SHOULD** verify public key matches derived value

#### 2.3.4 From Hex

**Signature:**
```
from_hex(hex: string) -> Result<(PrivateKey, PublicKey), Error>
```

**Requirements:**

1. Implementation **MUST** accept hex with or without `0x` prefix
2. Implementation **MUST** support both 64-char (32-byte) and 128-char (64-byte) hex

### 2.4 Signing [P0]

#### 2.4.1 Sign Message

**Signature:**
```
sign(private_key: PrivateKey, message: bytes) -> Signature
```

**Requirements:**

1. Implementation **MUST** follow RFC 8032 Ed25519 signing
2. Same key and message **MUST** produce deterministic signature
3. Empty messages **MUST** be supported

#### 2.4.2 Sign with Domain Separator

**Signature:**
```
sign_with_domain(private_key: PrivateKey, domain: string, message: bytes) -> Signature
```

**Domain-Separated Message:**
```
signed_message = SHA3-256(SHA3-256(domain) || message)
```

### 2.5 Verification [P0]

**Signature:**
```
verify(public_key: PublicKey, message: bytes, signature: Signature) -> bool
```

**Requirements:**

1. Implementation **MUST** follow RFC 8032 Ed25519 verification
2. Implementation **MUST** return `false` for invalid signatures (not error)
3. Implementation **MUST** return `false` for malformed signatures
4. Verification **SHOULD** be constant-time

### 2.6 Key Export [P0]

| Method                | Output Size | Description                    |
| --------------------- | ----------- | ------------------------------ |
| `public_key_bytes()`  | 32 bytes    | Raw public key bytes           |
| `private_key_bytes()` | 32 or 64 bytes | Seed or extended key        |
| `to_hex()`            | 66 or 130 chars | Hex with 0x prefix         |

### 2.7 Scheme Identifier [P0]

```
Ed25519 Scheme Identifier: 0x00
```

---

## 3. Secp256k1 ECDSA

### 3.1 Overview

Secp256k1 ECDSA provides compatibility with Ethereum-style wallets and hardware devices.

**Priority: P1 (Preferred)**

### 3.2 Key Sizes

| Component                 | Size     | Description                    |
| ------------------------- | -------- | ------------------------------ |
| Private Key               | 32 bytes | Scalar value                   |
| Public Key (Compressed)   | 33 bytes | 0x02/0x03 prefix + x-coordinate|
| Public Key (Uncompressed) | 65 bytes | 0x04 prefix + x + y            |
| Signature                 | 64 bytes | (r, s) values                  |

### 3.3 Key Generation [P1]

**Signatures:**
```
generate() -> (PrivateKey, PublicKey)
from_bytes(bytes: [u8; 32]) -> Result<(PrivateKey, PublicKey), Error>
from_hex(hex: string) -> Result<(PrivateKey, PublicKey), Error>
```

**Requirements:**

1. Private key **MUST** be a valid scalar (1 <= k < n where n is curve order)
2. Implementation **MUST** reject zero and out-of-range values

### 3.4 Public Key Formats [P1]

**Signatures:**
```
to_compressed() -> [u8; 33]
to_uncompressed() -> [u8; 65]
```

**Compressed Format:**
```
0x02 || x  (if y is even)
0x03 || x  (if y is odd)
```

**Uncompressed Format:**
```
0x04 || x || y
```

### 3.5 Signing [P1]

**Signature:**
```
sign(private_key: PrivateKey, message_hash: [u8; 32]) -> Signature
```

**Requirements:**

1. Input **MUST** be the hash of the message (not raw message)
2. Implementation **MUST** use RFC 6979 deterministic k generation
3. Signature **MUST** use low-S normalization (s <= n/2)

### 3.6 Verification [P1]

**Signature:**
```
verify(public_key: PublicKey, message_hash: [u8; 32], signature: Signature) -> bool
```

### 3.7 Scheme Identifier [P1]

```
Secp256k1 Scheme Identifier: 0x01
```

---

## 4. Secp256r1 / P-256

### 4.1 Overview

Secp256r1 (NIST P-256) enables WebAuthn/Passkey compatibility for browser-based authentication.

**Priority: P2 (Optional)**

### 4.2 Key Sizes

Same as Secp256k1 (32-byte private key, 33/65-byte public key, 64-byte signature).

### 4.3 Key Generation [P2]

Same interface as Secp256k1.

### 4.4 Signing and Verification [P2]

Same interface as Secp256k1.

### 4.5 WebAuthn Integration [P2]

For WebAuthn compatibility:

1. Implementation **SHOULD** support parsing WebAuthn attestation
2. Implementation **SHOULD** handle clientDataJSON and authenticatorData
3. Implementation **SHOULD** verify WebAuthn signatures

### 4.6 Scheme Identifier [P2]

```
Secp256r1 Scheme Identifier: 0x02
```

---

## 5. BLS12-381

### 5.1 Overview

BLS12-381 enables signature aggregation for multi-signature schemes and efficient batch
verification.

**Priority: P2 (Optional)**

### 5.2 Key Sizes

| Component   | Size     | Description                    |
| ----------- | -------- | ------------------------------ |
| Private Key | 32 bytes | Scalar value                   |
| Public Key  | 48 bytes | G1 point (compressed)          |
| Signature   | 96 bytes | G2 point (compressed)          |

### 5.3 Key Generation [P2]

**Signature:**
```
generate() -> (PrivateKey, PublicKey)
from_bytes(bytes: [u8; 32]) -> Result<(PrivateKey, PublicKey), Error>
```

### 5.4 Signing [P2]

**Signature:**
```
sign(private_key: PrivateKey, message: bytes) -> Signature
```

### 5.5 Verification [P2]

**Signature:**
```
verify(public_key: PublicKey, message: bytes, signature: Signature) -> bool
```

### 5.6 Aggregation [P2]

**Signatures:**
```
aggregate_signatures(signatures: Vec<Signature>) -> Signature
aggregate_public_keys(public_keys: Vec<PublicKey>) -> PublicKey
```

**Requirements:**

1. Aggregated signature **MUST** verify against aggregated public key
2. Order of aggregation **MUST NOT** affect result

### 5.7 Proof of Possession [P2]

**Signature:**
```
proof_of_possession(private_key: PrivateKey) -> Signature
verify_proof_of_possession(public_key: PublicKey, proof: Signature) -> bool
```

Used to prevent rogue key attacks in multi-signature schemes.

---

## 6. Hashing

### 6.1 SHA3-256 [P0]

**Signature:**
```
sha3_256(data: bytes) -> [u8; 32]
```

**Requirements:**

1. Implementation **MUST** use Keccak-based SHA3-256 (FIPS 202)
2. Output **MUST** be exactly 32 bytes
3. Empty input **MUST** be supported

### 6.2 SHA2-256 [P0]

**Signature:**
```
sha256(data: bytes) -> [u8; 32]
```

**Requirements:**

1. Implementation **MUST** use SHA-256 (FIPS 180-4)
2. Required for BIP-39/BIP-44 key derivation

### 6.3 Domain-Separated Hashing [P0]

Aptos uses domain separation to prevent cross-protocol signature attacks.

**Formula:**
```
hash = SHA3-256(SHA3-256(domain_string) || data)
```

**Common Domains:**

| Domain                            | Usage                              |
| --------------------------------- | ---------------------------------- |
| `APTOS::RawTransaction`           | Single-signer transaction signing  |
| `APTOS::RawTransactionWithData`   | Multi-agent/fee payer transactions |

### 6.4 Hashing Multiple Parts [P1]

**Signature:**
```
sha3_256_of_parts(parts: Vec<bytes>) -> [u8; 32]
```

Concatenates parts and hashes the result.

---

## 7. Authentication Key Derivation

### 7.1 Overview

An authentication key is derived from a public key and used to derive the initial account address.

### 7.2 Derivation Formula [P0]

```
authentication_key = SHA3-256(public_key_bytes || scheme_identifier)
```

### 7.3 Scheme Identifiers [P0]

| Scheme       | Identifier | Priority |
| ------------ | ---------- | -------- |
| Ed25519      | 0x00       | P0       |
| Secp256k1    | 0x01       | P1       |
| Secp256r1    | 0x02       | P2       |
| MultiEd25519 | 0x01       | P2       |
| MultiKey     | 0x03       | P2       |
| Keyless      | 0x05       | P2       |

### 7.4 Ed25519 Authentication Key [P0]

**Signature:**
```
auth_key_from_ed25519(public_key: Ed25519PublicKey) -> AuthenticationKey
```

**Formula:**
```
auth_key = SHA3-256(public_key || 0x00)
```

Where `public_key` is the 32-byte Ed25519 public key.

### 7.5 Secp256k1 Authentication Key [P1]

**Signature:**
```
auth_key_from_secp256k1(public_key: Secp256k1PublicKey) -> AuthenticationKey
```

**Formula:**
```
auth_key = SHA3-256(uncompressed_public_key || 0x01)
```

Where `uncompressed_public_key` is the 65-byte uncompressed public key.

### 7.6 Address Derivation [P0]

For new accounts (authentication key has not been rotated):

```
account_address = authentication_key
```

The 32-byte authentication key **IS** the account address.

### 7.7 AuthenticationKey Type [P0]

**Methods:**

| Method              | Description                    |
| ------------------- | ------------------------------ |
| `from_bytes(bytes)` | Create from 32-byte array      |
| `account_address()` | Convert to AccountAddress      |
| `as_bytes()`        | Get raw 32-byte array          |

---

## 8. Key Derivation (BIP-39/BIP-44)

### 8.1 BIP-39 Mnemonics [P1]

#### 8.1.1 Generation

**Signature:**
```
generate_mnemonic(word_count: u8) -> Mnemonic
```

**Supported Word Counts:**

| Words | Entropy Bits | Checksum Bits |
| ----- | ------------ | ------------- |
| 12    | 128          | 4             |
| 15    | 160          | 5             |
| 18    | 192          | 6             |
| 21    | 224          | 7             |
| 24    | 256          | 8             |

**Requirements:**

1. Implementation **MUST** use CSPRNG for entropy
2. Implementation **MUST** use BIP-39 English wordlist
3. Checksum **MUST** be calculated per BIP-39

#### 8.1.2 Parsing

**Signature:**
```
from_phrase(phrase: string) -> Result<Mnemonic, Error>
```

**Requirements:**

1. Implementation **MUST** validate checksum
2. Implementation **MUST** reject invalid words
3. Implementation **SHOULD** be case-insensitive

#### 8.1.3 Seed Derivation

**Signature:**
```
to_seed(mnemonic: Mnemonic, passphrase: string) -> [u8; 64]
```

**Formula:**
```
seed = PBKDF2(
  password = mnemonic_phrase,
  salt = "mnemonic" || passphrase,
  iterations = 2048,
  key_length = 64,
  hash = HMAC-SHA512
)
```

### 8.2 BIP-44 Path Derivation [P1]

#### 8.2.1 Aptos Derivation Path

```
m / 44' / 637' / account' / change' / address_index'
```

**Components:**

| Level | Value | Description                    |
| ----- | ----- | ------------------------------ |
| 44'   | Fixed | BIP-44 purpose                 |
| 637'  | Fixed | Aptos coin type (registered)   |
| account' | Variable | Account index (default 0) |
| change'  | 0     | Always 0 for Aptos            |
| address_index' | Variable | Address index (default 0) |

**Default Path:** `m/44'/637'/0'/0'/0'`

#### 8.2.2 Deriving Multiple Accounts

```
Account 0: m/44'/637'/0'/0'/0'
Account 1: m/44'/637'/0'/0'/1'
Account 2: m/44'/637'/0'/0'/2'
```

#### 8.2.3 Ed25519 Derivation [P1]

**Signature:**
```
derive_ed25519(seed: [u8; 64], path: string) -> Ed25519PrivateKey
```

**Requirements:**

1. Implementation **MUST** use SLIP-0010 for Ed25519 derivation
2. All path components **MUST** be hardened (')

#### 8.2.4 Secp256k1 Derivation [P1]

**Signature:**
```
derive_secp256k1(seed: [u8; 64], path: string) -> Secp256k1PrivateKey
```

**Requirements:**

1. Implementation **MUST** use standard BIP-32 derivation
2. Hardened derivation **SHOULD** be used for security

---

## 9. Test Vectors

### 9.1 Ed25519 Signing

Test vectors in `test-vectors/signatures.json`:

```json
{
  "ed25519_vectors": [
    {
      "name": "basic_signature",
      "private_key_hex": "0x...",
      "public_key_hex": "0x...",
      "message_hex": "0x...",
      "signature_hex": "0x..."
    }
  ]
}
```

### 9.2 Key Derivation

Test vectors in `test-vectors/mnemonics.json`:

```json
{
  "derivation_vectors": [
    {
      "mnemonic": "abandon abandon ... about",
      "passphrase": "",
      "path": "m/44'/637'/0'/0'/0'",
      "expected_address": "0x..."
    }
  ]
}
```

### 9.3 Authentication Key

```json
{
  "auth_key_vectors": [
    {
      "public_key_hex": "0x...",
      "scheme": "ed25519",
      "expected_auth_key": "0x..."
    }
  ]
}
```

---

## 10. Security Considerations

### 10.1 Key Generation

1. Implementation **MUST** use OS-provided CSPRNG
2. Implementation **MUST NOT** use predictable seeds in production
3. Implementation **SHOULD** verify entropy source quality when possible

### 10.2 Key Storage

1. Private keys **MUST** be zeroized when no longer needed
2. Private keys **SHOULD** use memory protection when available
3. Private keys **MUST NOT** appear in logs or debug output
4. Private keys **MUST NOT** implement `Display` trait

### 10.3 Signing

1. Implementation **MUST** use domain separation for different message types
2. Implementation **SHOULD** require explicit user consent before signing
3. Implementation **SHOULD** display transaction details before signing

### 10.4 Side-Channel Resistance

1. Verification **SHOULD** use constant-time comparison
2. Private key operations **SHOULD** be constant-time
3. Implementation **SHOULD NOT** branch on secret data

### 10.5 Mnemonic Security

1. Mnemonics **MUST** be generated with CSPRNG entropy
2. Mnemonics **SHOULD** be zeroized after use
3. Seed derivation **MUST** use standard PBKDF2 parameters

---

## 11. References

### 11.1 Related Specifications

- [04-accounts.md](04-accounts.md) - Account types using these primitives
- [05-transactions.md](05-transactions.md) - Transaction signing

### 11.2 External Standards

- [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032) - Edwards-Curve Digital Signature Algorithm (EdDSA)
- [RFC 6979](https://datatracker.ietf.org/doc/html/rfc6979) - Deterministic ECDSA
- [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) - Mnemonic code
- [BIP-44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) - HD Wallets
- [SLIP-0010](https://github.com/satoshilabs/slips/blob/master/slip-0010.md) - Universal derivation
- [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) - SHA-3 Standard

### 11.3 Feature Files

- `features/02-cryptography/ed25519.feature` - 23 Ed25519 scenarios
- `features/02-cryptography/secp256k1.feature` - 18 Secp256k1 scenarios
- `features/02-cryptography/secp256r1.feature` - 26 Secp256r1 scenarios
- `features/02-cryptography/bls12381.feature` - 30 BLS12-381 scenarios
- `features/02-cryptography/hashing.feature` - 21 hashing scenarios

### 11.4 Test Vectors

- `test-vectors/signatures.json`
- `test-vectors/mnemonics.json`
