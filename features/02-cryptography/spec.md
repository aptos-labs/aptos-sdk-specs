# Cryptography Specification

## Overview

The cryptography module provides cryptographic primitives for Aptos blockchain operations including
key generation, signing, verification, and hashing. Multiple signature schemes are supported with
Ed25519 being the primary required scheme.

## Goals

1. Provide secure key generation and management
2. Support multiple signature schemes used by Aptos
3. Enable proper authentication key derivation
4. Ensure cross-SDK cryptographic compatibility

## Non-Goals

- Key storage/persistence (user responsibility)
- Hardware wallet integration (optional feature)
- Key encryption at rest (user responsibility)

---

## Ed25519 (Required - P0)

### Description

Ed25519 is the primary signature scheme for Aptos accounts. It provides fast signing and
verification with 32-byte keys.

### Key Sizes

| Component              | Size                         |
| ---------------------- | ---------------------------- |
| Private Key (Seed)     | 32 bytes                     |
| Private Key (Extended) | 64 bytes (seed + public key) |
| Public Key             | 32 bytes                     |
| Signature              | 64 bytes                     |

### Requirements

#### Key Generation

| Method              | Priority | Description                               |
| ------------------- | -------- | ----------------------------------------- |
| `generate()`        | P0       | Generate random key pair using secure RNG |
| `from_seed(bytes)`  | P0       | Create from 32-byte seed                  |
| `from_bytes(bytes)` | P0       | Create from 64-byte private key           |
| `from_hex(string)`  | P0       | Create from hex-encoded private key       |

#### Signing

| Method                  | Priority | Description                |
| ----------------------- | -------- | -------------------------- |
| `sign(message)`         | P0       | Sign arbitrary bytes       |
| `sign_message(message)` | P0       | Sign with domain separator |

#### Verification

| Method                       | Priority | Description                         |
| ---------------------------- | -------- | ----------------------------------- |
| `verify(message, signature)` | P0       | Verify signature against public key |

#### Export

| Method                | Priority | Description                                   |
| --------------------- | -------- | --------------------------------------------- |
| `public_key_bytes()`  | P0       | Get 32-byte public key                        |
| `private_key_bytes()` | P0       | Get private key bytes (with security warning) |
| `to_hex()`            | P0       | Export as hex string                          |

### Security Requirements

1. Private keys must be zeroized on drop
2. Private keys should not implement Display/Debug
3. Use cryptographically secure RNG for generation
4. Constant-time comparison for verification

---

## Secp256k1 ECDSA (Preferred - P1)

### Description

Secp256k1 is used for compatibility with Ethereum-style wallets and hardware devices.

### Key Sizes

| Component                 | Size            |
| ------------------------- | --------------- |
| Private Key               | 32 bytes        |
| Public Key (Compressed)   | 33 bytes        |
| Public Key (Uncompressed) | 65 bytes        |
| Signature                 | 64 bytes (r, s) |

### Requirements

#### Key Generation

| Method              | Priority | Description                         |
| ------------------- | -------- | ----------------------------------- |
| `generate()`        | P1       | Generate random key pair            |
| `from_bytes(bytes)` | P1       | Create from 32-byte private key     |
| `from_hex(string)`  | P1       | Create from hex-encoded private key |

#### Public Key Formats

| Method              | Priority | Description                 |
| ------------------- | -------- | --------------------------- |
| `to_compressed()`   | P1       | 33-byte compressed format   |
| `to_uncompressed()` | P1       | 65-byte uncompressed format |

#### Signing

| Method                 | Priority | Description                     |
| ---------------------- | -------- | ------------------------------- |
| `sign(message)`        | P1       | Sign with recoverable signature |
| `sign_prehashed(hash)` | P1       | Sign pre-hashed message         |

### Authentication Key

Secp256k1 authentication key derivation:

```
auth_key = SHA3-256(public_key_uncompressed || 0x01)
```

Where `0x01` is the Secp256k1 scheme identifier.

---

## Secp256r1 / P-256 (Optional - P2)

### Description

Secp256r1 (NIST P-256) is used for WebAuthn/Passkey compatibility.

### Key Sizes

Same as Secp256k1.

### Authentication Key

```
auth_key = SHA3-256(public_key_uncompressed || 0x02)
```

Where `0x02` is the Secp256r1 scheme identifier.

---

## Hashing

### SHA3-256 (Required - P0)

| Method                     | Priority | Description                 |
| -------------------------- | -------- | --------------------------- |
| `sha3_256(data)`           | P0       | Compute SHA3-256 hash       |
| `sha3_256_of_parts(parts)` | P0       | Hash multiple data segments |

### SHA2-256 (Required - P0)

Required for BIP-39/BIP-44 key derivation.

| Method         | Priority | Description           |
| -------------- | -------- | --------------------- |
| `sha256(data)` | P0       | Compute SHA2-256 hash |

### Domain-Separated Hashing

Aptos uses domain-separated hashing for type safety:

```
hash = SHA3-256(SHA3-256(domain_string) || data)
```

Common domains:

- `APTOS::RawTransaction` - Single-signer transactions
- `APTOS::RawTransactionWithData` - Multi-agent/fee payer transactions

---

## Authentication Key

### Description

Authentication key is derived from public key and used to derive account addresses for new accounts.

### Derivation

```
auth_key = SHA3-256(public_key_bytes || scheme_identifier)
```

### Scheme Identifiers

| Scheme       | Identifier | Priority |
| ------------ | ---------- | -------- |
| Ed25519      | 0x00       | P0       |
| Secp256k1    | 0x01       | P1       |
| Secp256r1    | 0x02       | P2       |
| MultiEd25519 | 0x01       | P2       |
| MultiKey     | 0x03       | P2       |
| Keyless      | 0x05       | P2       |

### Address Derivation

For new accounts (not rotated):

```
account_address = authentication_key
```

### Requirements

| Method                         | Priority | Description               |
| ------------------------------ | -------- | ------------------------- |
| `from_public_key(key, scheme)` | P0       | Derive from public key    |
| `from_ed25519(public_key)`     | P0       | Derive from Ed25519 key   |
| `from_secp256k1(public_key)`   | P1       | Derive from Secp256k1 key |
| `to_account_address()`         | P0       | Convert to address        |
| `as_bytes()`                   | P0       | Get raw 32 bytes          |

---

## Key Derivation (Preferred - P1)

### BIP-39 Mnemonics

| Method                 | Priority | Description                                  |
| ---------------------- | -------- | -------------------------------------------- |
| `generate(word_count)` | P1       | Generate mnemonic (12, 15, 18, 21, 24 words) |
| `from_phrase(phrase)`  | P1       | Parse mnemonic phrase                        |
| `validate(phrase)`     | P1       | Validate mnemonic checksum                   |
| `to_seed(passphrase)`  | P1       | Derive 64-byte seed                          |

### BIP-44 Path Derivation

Aptos uses coin type 637:

```
m/44'/637'/account'/change'/address_index'
```

Default path: `m/44'/637'/0'/0'/0'`

| Method                         | Priority | Description          |
| ------------------------------ | -------- | -------------------- |
| `derive_ed25519(seed, path)`   | P1       | Derive Ed25519 key   |
| `derive_secp256k1(seed, path)` | P1       | Derive Secp256k1 key |

---

## Error Handling

### Required Error Cases

| Error                 | Trigger                     | Priority |
| --------------------- | --------------------------- | -------- |
| InvalidPrivateKey     | Malformed private key bytes | P0       |
| InvalidPublicKey      | Malformed public key bytes  | P0       |
| InvalidSignature      | Malformed signature bytes   | P0       |
| VerificationFailed    | Signature doesn't verify    | P0       |
| InvalidMnemonic       | Bad mnemonic phrase         | P1       |
| InvalidDerivationPath | Malformed BIP-44 path       | P1       |

---

## Security Considerations

### Key Generation

1. Use OS-provided CSPRNG (cryptographically secure pseudo-random number generator)
2. Never use predictable seeds in production
3. Validate entropy quality when possible

### Key Storage

1. Zeroize private key memory on drop
2. Avoid copying private keys unnecessarily
3. Don't log or display private keys
4. Consider memory-locking for sensitive operations

### Signing

1. Always use domain separation for different message types
2. Never sign arbitrary data without user consent
3. Validate transaction details before signing

---

## Cross-SDK Compatibility

All SDKs must produce identical:

1. Public keys from the same private key
2. Signatures for the same message and key
3. Authentication keys from the same public key
4. Derived keys from the same mnemonic and path

Test vectors in `test-vectors/signatures.json` and `test-vectors/mnemonics.json` provide
deterministic test cases.

---

## Related Gherkin Feature Files

| File                | Scenarios | Description                                   |
| ------------------- | --------- | --------------------------------------------- |
| `ed25519.feature`   | 23        | Ed25519 key generation, signing, verification |
| `secp256k1.feature` | 18        | Secp256k1 ECDSA operations                    |
| `secp256r1.feature` | 26        | Secp256r1/P-256 for WebAuthn/Passkey          |
| `hashing.feature`   | 21        | SHA3-256, SHA2-256, domain separation         |
