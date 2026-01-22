# Feature Coverage Matrix

> **Last Updated:** 2026-01-21
>
> This file tracks implementation status of behavioral specifications across all SDK implementations.
> Check boxes indicate that step definitions exist and tests pass for that scenario.

## Summary

| SDK        | Required (P0) | Preferred (P1) | Optional (P2) | Total    |
| ---------- | ------------- | -------------- | ------------- | -------- |
| TypeScript | 280/306 (92%) | 150/183 (82%)  | 80/250 (32%)  | 510/739  |
| Go         | 90/306 (29%)  | 20/183 (11%)   | 0/250 (0%)    | 110/739  |
| Rust       | 200/306 (65%) | 60/183 (33%)   | 20/250 (8%)   | 280/739  |

## Legend

- `[x]` - Implemented and passing
- `[ ]` - Not yet implemented
- `[~]` - Partially implemented or known issues

---

## 01-core-types

### address.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Parse hex address with 0x prefix | [x] | [x] | [x] |
| 2 | Parse hex address without 0x prefix | [x] | [x] | [x] |
| 3 | Parse full 64-character hex address | [x] | [x] | [x] |
| 4 | Parse uppercase hex address | [x] | [x] | [x] |
| 5 | Parse mixed case hex address | [x] | [x] | [x] |
| 6 | Reject empty string | [x] | [x] | [~] |
| 7 | Reject just 0x prefix | [x] | [x] | [~] |
| 8 | Reject non-hex characters | [x] | [x] | [x] |
| 9 | Reject address too long | [x] | [x] | [x] |
| 10 | Reject address with spaces | [x] | [x] | [x] |
| 11 | Format address to full hex | [x] | [x] | [x] |
| 12 | Format address to short string | [x] | [x] | [x] |
| 13 | Format zero address | [x] | [x] | [x] |
| 14 | ZERO address constant | [x] | [x] | [x] |
| 15 | ONE address constant (framework) | [x] | [x] | [x] |
| 16 | THREE address constant (token) | [x] | [x] | [x] |
| 17 | FOUR address constant (objects) | [x] | [x] | [x] |
| 18 | Addresses parsed from equivalent inputs are equal | [x] | [x] | [x] |
| 19 | Different addresses are not equal | [x] | [x] | [x] |
| 20 | BCS serialize address | [x] | [x] | [x] |
| 21 | BCS deserialize address | [x] | [x] | [x] |
| 22 | BCS round-trip | [x] | [x] | [x] |

### serialization.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | ULEB128 round-trip | [x] | [ ] | [x] |
| 2 | Serialize empty bytes | [x] | [ ] | [x] |
| 3 | Serialize short bytes | [x] | [ ] | [x] |
| 4 | Serialize string | [x] | [ ] | [x] |
| 5 | Serialize empty string | [x] | [ ] | [x] |
| 6 | Serialize string with unicode | [x] | [ ] | [x] |
| 7 | Serialize None option | [x] | [ ] | [x] |
| 8 | Serialize Some option with u64 | [x] | [ ] | [x] |
| 9 | Serialize empty vector | [x] | [ ] | [x] |
| 10 | Serialize vector of u8 | [x] | [ ] | [x] |
| 11 | Serialize vector of u64 | [x] | [ ] | [x] |
| 12 | Serialize nested vector | [x] | [ ] | [x] |
| 13 | Serialize AccountAddress | [x] | [ ] | [x] |
| 14 | Deserialize AccountAddress | [x] | [ ] | [x] |
| 15 | Serialize struct with multiple fields | [x] | [ ] | [x] |
| 16 | Fail to deserialize truncated data | [x] | [ ] | [x] |
| 17 | Fail to deserialize invalid boolean | [x] | [ ] | [x] |
| 18 | Fail to deserialize sequence with invalid length | [x] | [ ] | [x] |

### type-tags.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Format primitive types | [x] | [ ] | [x] |
| 2 | Parse vector of u8 | [x] | [ ] | [x] |
| 3 | Parse nested vector | [x] | [ ] | [x] |
| 4 | Parse vector of struct | [x] | [ ] | [x] |
| 5 | Format vector type | [x] | [ ] | [x] |
| 6 | Parse simple struct type | [x] | [ ] | [x] |
| 7 | Parse struct with type argument | [x] | [ ] | [x] |
| 8 | Parse struct with multiple type arguments | [x] | [ ] | [x] |
| 9 | Parse struct with full address | [x] | [ ] | [x] |
| 10 | Format struct type without type args | [x] | [ ] | [x] |
| 11 | Format struct type with type args | [x] | [ ] | [x] |
| 12 | Reject empty type string | [x] | [ ] | [x] |
| 13 | Reject unknown primitive | [x] | [ ] | [x] |
| 14 | Reject malformed vector | [x] | [ ] | [x] |
| 15 | Reject unclosed vector bracket | [x] | [ ] | [x] |
| 16 | Reject invalid struct format | [x] | [ ] | [x] |
| 17 | Reject struct with invalid address | [x] | [ ] | [x] |
| 18 | Parse module ID | [x] | [ ] | [x] |
| 19 | Format module ID | [x] | [ ] | [x] |
| 20 | Reject invalid module ID | [x] | [ ] | [x] |
| 21 | Create MoveStructTag from components | [x] | [ ] | [x] |
| 22 | BCS serialize primitive TypeTag | [x] | [ ] | [x] |
| 23 | BCS serialize struct TypeTag | [x] | [ ] | [x] |
| 24 | BCS round-trip for complex TypeTag | [x] | [ ] | [x] |

---

## 02-cryptography

### ed25519.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate random Ed25519 key pair | [x] | [x] | [x] |
| 2 | Generate unique key pairs | [x] | [x] | [x] |
| 3 | Create key pair from 32-byte seed | [x] | [x] | [x] |
| 4 | Create key pair from 64-byte private key | [x] | [x] | [x] |
| 5 | Create key pair from hex string | [x] | [x] | [x] |
| 6 | Reject invalid private key length | [x] | [x] | [x] |
| 7 | Sign a message | [x] | [x] | [x] |
| 8 | Sign empty message | [x] | [x] | [x] |
| 9 | Sign produces deterministic signatures | [x] | [x] | [x] |
| 10 | Different messages produce different signatures | [x] | [x] | [x] |
| 11 | Different keys produce different signatures | [x] | [x] | [x] |
| 12 | Verify valid signature | [x] | [x] | [x] |
| 13 | Reject signature from wrong key | [x] | [x] | [x] |
| 14 | Reject signature for wrong message | [x] | [x] | [x] |
| 15 | Reject malformed signature | [x] | [x] | [x] |
| 16 | Reject truncated signature | [x] | [x] | [x] |
| 17 | Export public key bytes | [x] | [x] | [x] |
| 18 | Export private key bytes | [x] | [x] | [x] |
| 19 | Export keys as hex | [x] | [x] | [x] |
| 20 | Derive authentication key from Ed25519 public key | [x] | [x] | [x] |
| 21 | Derive account address from authentication key | [x] | [x] | [x] |
| 22 | Known test vector - key derivation | [x] | [x] | [x] |
| 23 | Known test vector - signing | [x] | [x] | [x] |
| 24 | Private key is zeroized on drop | [x] | [ ] | [x] |
| 25 | Private key does not appear in debug output | [x] | [ ] | [x] |

### hashing.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Compute SHA3-256 of empty data | [x] | [x] | [x] |
| 2 | Compute SHA3-256 of "hello" | [x] | [x] | [x] |
| 3 | SHA3-256 produces different hashes for different inputs | [x] | [x] | [x] |
| 4 | SHA3-256 is deterministic | [x] | [x] | [x] |
| 5 | Compute SHA3-256 of multiple parts | [x] | [x] | [x] |
| 6 | Compute SHA2-256 of empty data | [x] | [x] | [x] |
| 7 | Compute SHA2-256 of "hello" | [x] | [x] | [x] |
| 8 | SHA2-256 differs from SHA3-256 | [x] | [x] | [x] |
| 9 | Domain-separated hash for RawTransaction | [x] | [ ] | [x] |
| 10 | Different domains produce different hashes | [x] | [ ] | [x] |
| 11 | Domain hash prefix is computed correctly | [x] | [ ] | [x] |
| 12 | Create HashValue from bytes | [x] | [ ] | [x] |
| 13 | Create HashValue from hex | [x] | [ ] | [x] |
| 14 | Reject invalid HashValue length | [x] | [ ] | [x] |
| 15 | HashValue ZERO constant | [x] | [ ] | [x] |
| 16 | Format HashValue as hex | [x] | [ ] | [x] |
| 17 | HashValue equality | [x] | [ ] | [x] |
| 18 | HashValue from SHA3-256 | [x] | [ ] | [x] |
| 19 | Compute HMAC-SHA512 for BIP-39 seed derivation | [x] | [ ] | [x] |
| 20 | Hashing large data | [x] | [ ] | [x] |

### secp256k1.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate random Secp256k1 key pair | [x] | [ ] | [x] |
| 2 | Create key pair from 32-byte private key | [x] | [ ] | [x] |
| 3 | Create key pair from hex string | [x] | [ ] | [x] |
| 4 | Reject invalid private key (zero) | [x] | [ ] | [x] |
| 5 | Reject invalid private key (greater than curve order) | [x] | [ ] | [x] |
| 6 | Get compressed public key | [x] | [ ] | [x] |
| 7 | Get uncompressed public key | [x] | [ ] | [x] |
| 8 | Compressed and uncompressed represent same key | [x] | [ ] | [x] |
| 9 | Sign a message | [x] | [ ] | [x] |
| 10 | Sign produces deterministic signatures (RFC 6979) | [x] | [ ] | [x] |
| 11 | Sign pre-hashed message | [x] | [ ] | [x] |
| 12 | Verify valid signature | [x] | [ ] | [x] |
| 13 | Reject signature from wrong key | [x] | [ ] | [x] |
| 14 | Reject malformed signature | [x] | [ ] | [x] |
| 15 | Derive authentication key from Secp256k1 public key | [x] | [ ] | [x] |
| 16 | Authentication key uses scheme identifier 0x01 | [x] | [ ] | [x] |
| 17 | Known test vector - key derivation | [x] | [ ] | [x] |
| 18 | Known test vector - signing | [x] | [ ] | [x] |
| 19 | Known test vector - address derivation | [x] | [ ] | [x] |

### secp256r1.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate random Secp256r1 key pair | [x] | [ ] | [x] |
| 2 | Create key pair from 32-byte private key | [x] | [ ] | [x] |
| 3 | Create key pair from hex string | [x] | [ ] | [x] |
| 4 | Reject invalid private key (zero) | [x] | [ ] | [x] |
| 5 | Reject invalid private key (greater than curve order) | [x] | [ ] | [x] |
| 6 | Get compressed public key | [x] | [ ] | [x] |
| 7 | Get uncompressed public key | [x] | [ ] | [x] |
| 8 | Parse compressed public key | [x] | [ ] | [x] |
| 9 | Parse uncompressed public key | [x] | [ ] | [x] |
| 10 | Sign a message | [x] | [ ] | [x] |
| 11 | Sign produces deterministic signatures (RFC 6979) | [x] | [ ] | [x] |
| 12 | Sign with SHA-256 pre-hash | [x] | [ ] | [x] |
| 13 | Verify valid signature | [x] | [ ] | [x] |
| 14 | Reject signature from wrong key | [x] | [ ] | [x] |
| 15 | Reject malformed signature | [x] | [ ] | [x] |
| 16 | Derive authentication key from Secp256r1 public key | [x] | [ ] | [x] |
| 17 | Secp256r1 uses scheme identifier 0x02 | [x] | [ ] | [x] |
| 18 | Secp256r1 address differs from Secp256k1 | [x] | [ ] | [x] |
| 19 | Parse WebAuthn public key | [x] | [ ] | [ ] |
| 20 | Verify WebAuthn assertion signature | [x] | [ ] | [ ] |
| 21 | Signature format compatibility | [x] | [ ] | [ ] |
| 22 | Create Secp256r1 account | [x] | [ ] | [x] |
| 23 | Sign transaction with Secp256r1 account | [x] | [ ] | [x] |
| 24 | Known Secp256r1 key derivation test vector | [x] | [ ] | [x] |
| 25 | Known Secp256r1 signing test vector | [x] | [ ] | [x] |
| 26 | Known Secp256r1 address test vector | [x] | [ ] | [x] |

### bls12381.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate random BLS key pair | [ ] | [ ] | [ ] |
| 2 | Create key pair from 32-byte seed | [ ] | [ ] | [ ] |
| 3 | Create key pair from hex string | [ ] | [ ] | [ ] |
| 4 | Reject invalid private key | [ ] | [ ] | [ ] |
| 5 | BLS public key size | [ ] | [ ] | [ ] |
| 6 | BLS signature size | [ ] | [ ] | [ ] |
| 7 | Sign a message | [ ] | [ ] | [ ] |
| 8 | Signing is deterministic | [ ] | [ ] | [ ] |
| 9 | Different messages produce different signatures | [ ] | [ ] | [ ] |
| 10 | Different keys produce different signatures | [ ] | [ ] | [ ] |
| 11 | Verify valid signature | [ ] | [ ] | [ ] |
| 12 | Reject signature from wrong key | [ ] | [ ] | [ ] |
| 13 | Reject signature for wrong message | [ ] | [ ] | [ ] |
| 14 | Reject malformed signature | [ ] | [ ] | [ ] |
| 15 | Aggregate two signatures | [ ] | [ ] | [ ] |
| 16 | Aggregate multiple signatures | [ ] | [ ] | [ ] |
| 17 | Verify aggregated signature | [ ] | [ ] | [ ] |
| 18 | Aggregation is deterministic | [ ] | [ ] | [ ] |
| 19 | Cannot aggregate signatures for different messages | [ ] | [ ] | [ ] |
| 20 | Aggregate two public keys | [ ] | [ ] | [ ] |
| 21 | Aggregate multiple public keys | [ ] | [ ] | [ ] |
| 22 | Aggregated key verification | [ ] | [ ] | [ ] |
| 23 | Generate proof of possession | [ ] | [ ] | [ ] |
| 24 | Verify valid proof of possession | [ ] | [ ] | [ ] |
| 25 | Reject invalid proof of possession | [ ] | [ ] | [ ] |
| 26 | PoP prevents rogue key attacks | [ ] | [ ] | [ ] |
| 27 | Create BLS account | [ ] | [ ] | [ ] |
| 28 | BLS authentication key derivation | [ ] | [ ] | [ ] |
| 29 | Sign transaction with BLS account | [ ] | [ ] | [ ] |
| 30 | Reject invalid public key bytes | [ ] | [ ] | [ ] |
| 31 | Reject invalid signature bytes | [ ] | [ ] | [ ] |
| 32 | Reject point not on curve | [ ] | [ ] | [ ] |
| 33 | Known BLS key derivation test vector | [ ] | [ ] | [ ] |
| 34 | Known BLS signing test vector | [ ] | [ ] | [ ] |
| 35 | Known BLS aggregation test vector | [ ] | [ ] | [ ] |

---

## 03-account-management

### authentication-key.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Derive authentication key from Ed25519 public key | [x] | [x] | [x] |
| 2 | Authentication key uses Ed25519 scheme identifier | [x] | [x] | [x] |
| 3 | Same public key produces same authentication key | [x] | [x] | [x] |
| 4 | Different public keys produce different authentication keys | [x] | [x] | [x] |
| 5 | Derive authentication key from Secp256k1 public key | [x] | [ ] | [x] |
| 6 | Secp256k1 uses uncompressed public key | [x] | [ ] | [x] |
| 7 | Secp256k1 uses scheme identifier 0x01 | [x] | [ ] | [x] |
| 8 | Derive authentication key from arbitrary public key and scheme | [x] | [ ] | [x] |
| 9 | Convert authentication key to account address | [x] | [x] | [x] |
| 10 | New account address equals authentication key | [x] | [x] | [x] |
| 11 | Authentication key from_bytes | [x] | [x] | [x] |
| 12 | Authentication key as bytes | [x] | [x] | [x] |
| 13 | Authentication key to hex | [x] | [x] | [x] |
| 14 | Known Ed25519 authentication key test vector | [x] | [x] | [x] |
| 15 | Known Secp256k1 authentication key test vector | [x] | [ ] | [x] |
| 16 | Reject invalid authentication key length | [x] | [x] | [x] |
| 17 | Handle all-zero authentication key | [x] | [x] | [x] |

### single-key.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate random Ed25519 account | [x] | [x] | [x] |
| 2 | Generated accounts are unique | [x] | [x] | [x] |
| 3 | Create Ed25519 account from private key bytes | [x] | [x] | [x] |
| 4 | Create Ed25519 account from hex string | [x] | [x] | [x] |
| 5 | Create Ed25519 account from 64-byte expanded key | [x] | [x] | [x] |
| 6 | Load account from AIP-80 compliant string | [x] | [ ] | [x] |
| 7 | Export account to AIP-80 compliant string | [x] | [ ] | [x] |
| 8 | Ed25519 account public key | [x] | [x] | [x] |
| 9 | Ed25519 account authentication key | [x] | [x] | [x] |
| 10 | Ed25519 account address | [x] | [x] | [x] |
| 11 | Sign message with Ed25519 account | [x] | [x] | [x] |
| 12 | Sign transaction with Ed25519 account | [x] | [x] | [x] |
| 13 | Verify signature from Ed25519 account | [x] | [x] | [x] |
| 14 | Reject signature from different Ed25519 account | [x] | [x] | [x] |
| 15 | Generate random Secp256k1 account | [x] | [ ] | [x] |
| 16 | Create Secp256k1 account from private key | [x] | [ ] | [x] |
| 17 | Secp256k1 account address differs from Ed25519 | [x] | [ ] | [x] |
| 18 | Sign message with Secp256k1 account | [x] | [ ] | [x] |
| 19 | Sign transaction with Secp256k1 account | [x] | [ ] | [x] |
| 20 | Secp256k1 signature is recoverable | [x] | [ ] | [ ] |
| 21 | Known Ed25519 account test vector | [x] | [x] | [x] |
| 22 | Known Secp256k1 account test vector | [x] | [ ] | [x] |
| 23 | Reject invalid private key length | [x] | [x] | [x] |
| 24 | Reject invalid hex string | [x] | [x] | [x] |
| 25 | Account equality by address | [x] | [x] | [x] |
| 26 | Private key is not exposed accidentally | [x] | [ ] | [x] |
| 27 | Private key export requires explicit method | [x] | [ ] | [x] |
| 28 | AIP-80 format is ed25519-priv-... for Ed25519 | [x] | [ ] | [x] |

### mnemonic-derivation.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate 12-word mnemonic | [x] | [ ] | [x] |
| 2 | Generate 24-word mnemonic | [x] | [ ] | [x] |
| 3 | Generated mnemonics are unique | [x] | [ ] | [x] |
| 4 | Mnemonic words are from BIP-39 wordlist | [x] | [ ] | [x] |
| 5 | Parse valid mnemonic phrase | [x] | [ ] | [x] |
| 6 | Mnemonic parsing is case-insensitive | [x] | [ ] | [x] |
| 7 | Reject invalid mnemonic word | [x] | [ ] | [x] |
| 8 | Reject mnemonic with wrong word count | [x] | [ ] | [x] |
| 9 | Reject mnemonic with invalid checksum | [x] | [ ] | [x] |
| 10 | Derive Ed25519 account from mnemonic with default path | [x] | [ ] | [x] |
| 11 | Derive Ed25519 account with custom path | [x] | [ ] | [x] |
| 12 | Same mnemonic produces same account | [x] | [ ] | [x] |
| 13 | Different mnemonics produce different accounts | [x] | [ ] | [x] |
| 14 | Different paths produce different accounts | [x] | [ ] | [x] |
| 15 | Derive multiple accounts from one mnemonic | [x] | [ ] | [x] |
| 16 | Derive Secp256k1 account from mnemonic | [x] | [ ] | [x] |
| 17 | Ed25519 and Secp256k1 from same mnemonic have different addresses | [x] | [ ] | [x] |
| 18 | Derive account with passphrase | [x] | [ ] | [x] |
| 19 | Different passphrases produce different accounts | [x] | [ ] | [x] |
| 20 | No passphrase is same as empty passphrase | [x] | [ ] | [x] |
| 21 | Known test vector - 12 word mnemonic | [x] | [ ] | [x] |
| 22 | Known test vector - with passphrase | [x] | [ ] | [x] |
| 23 | Known test vector - multiple indices | [x] | [ ] | [x] |
| 24 | Valid derivation path formats | [x] | [ ] | [x] |
| 25 | Reject invalid derivation path - missing m | [x] | [ ] | [x] |
| 26 | Reject invalid derivation path - wrong coin type | [x] | [ ] | [x] |
| 27 | Reject invalid derivation path - non-hardened where required | [x] | [ ] | [x] |
| 28 | Mnemonic phrase can be retrieved | [x] | [ ] | [x] |
| 29 | Seed is zeroized after derivation | [x] | [ ] | [x] |

---

## 04-transaction-building

### entry-function.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create entry function payload with no arguments | [x] | [x] | [x] |
| 2 | Create entry function payload with u64 argument | [x] | [x] | [x] |
| 3 | Create entry function payload with address argument | [x] | [x] | [x] |
| 4 | Create entry function payload with string argument | [x] | [x] | [x] |
| 5 | Create entry function payload with vector argument | [x] | [x] | [x] |
| 6 | Create entry function payload with bool argument | [x] | [x] | [x] |
| 7 | Create entry function payload with multiple arguments | [x] | [x] | [x] |
| 8 | Create entry function with type arguments | [x] | [x] | [x] |
| 9 | Create entry function with multiple type arguments | [x] | [x] | [x] |
| 10 | BCS serialize entry function payload | [x] | [x] | [x] |
| 11 | BCS deserialize entry function payload | [x] | [x] | [x] |
| 12 | Entry function serialization is deterministic | [x] | [x] | [x] |
| 13 | Serialize u8 argument | [x] | [x] | [x] |
| 14 | Serialize u16 argument | [x] | [x] | [x] |
| 15 | Serialize u32 argument | [x] | [x] | [x] |
| 16 | Serialize u64 argument | [x] | [x] | [x] |
| 17 | Serialize u128 argument | [x] | [x] | [x] |
| 18 | Serialize u256 argument | [x] | [x] | [x] |
| 19 | Serialize nested vector argument | [x] | [x] | [x] |
| 20 | Serialize optional argument (Some) | [x] | [ ] | [x] |
| 21 | Serialize optional argument (None) | [x] | [ ] | [x] |
| 22 | Reject invalid module address | [x] | [x] | [x] |
| 23 | Reject empty function name | [x] | [x] | [x] |
| 24 | Known entry function test vector | [x] | [x] | [x] |

### raw-transaction.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create raw transaction with required fields | [x] | [x] | [x] |
| 2 | Raw transaction has correct sender | [x] | [x] | [x] |
| 3 | Raw transaction has correct sequence number | [x] | [x] | [x] |
| 4 | Raw transaction has correct max gas | [x] | [x] | [x] |
| 5 | Raw transaction has correct gas unit price | [x] | [x] | [x] |
| 6 | Raw transaction has correct expiration | [x] | [x] | [x] |
| 7 | Raw transaction has correct chain ID | [x] | [x] | [x] |
| 8 | BCS serialize raw transaction | [x] | [x] | [x] |
| 9 | BCS deserialize raw transaction | [x] | [x] | [x] |
| 10 | Raw transaction serialization is deterministic | [x] | [x] | [x] |
| 11 | Compute signing message from raw transaction | [x] | [x] | [x] |
| 12 | Signing message uses domain separation | [x] | [x] | [x] |
| 13 | Signing message is deterministic | [x] | [x] | [x] |
| 14 | Different transactions have different signing messages | [x] | [x] | [x] |
| 15 | Set expiration from duration | [x] | [ ] | [x] |
| 16 | Set expiration from timestamp | [x] | [ ] | [x] |
| 17 | Reject zero max gas | [x] | [x] | [x] |
| 18 | Reject zero gas unit price | [x] | [x] | [x] |
| 19 | Reject expired transaction | [x] | [ ] | [x] |
| 20 | Known raw transaction test vector | [x] | [x] | [x] |
| 21 | Known signing message test vector | [x] | [x] | [x] |

### signing.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Sign raw transaction with Ed25519 account | [x] | [x] | [x] |
| 2 | Signed transaction contains original raw transaction | [x] | [x] | [x] |
| 3 | Signed transaction contains authenticator | [x] | [x] | [x] |
| 4 | Ed25519 authenticator structure | [x] | [x] | [x] |
| 5 | BCS serialize signed transaction | [x] | [x] | [x] |
| 6 | BCS deserialize signed transaction | [x] | [x] | [x] |
| 7 | Signed transaction serialization is deterministic | [x] | [x] | [x] |
| 8 | Compute transaction hash | [x] | [x] | [x] |
| 9 | Transaction hash is deterministic | [x] | [x] | [x] |
| 10 | Transaction hash uses signed transaction bytes | [x] | [x] | [x] |
| 11 | Different signed transactions have different hashes | [x] | [x] | [x] |
| 12 | Verify signed transaction signature | [x] | [x] | [x] |
| 13 | Reject tampered transaction | [x] | [x] | [x] |
| 14 | Reject wrong signer | [x] | [x] | [x] |
| 15 | Sign with Secp256k1 account | [x] | [ ] | [x] |
| 16 | Secp256k1 authenticator structure | [x] | [ ] | [x] |
| 17 | Verify Secp256k1 signed transaction | [x] | [ ] | [x] |
| 18 | SingleKey authenticator wrapper | [x] | [ ] | [x] |
| 19 | Sign transaction twice produces same result | [x] | [x] | [x] |
| 20 | Cannot sign with wrong chain ID | [x] | [x] | [x] |
| 21 | Known Ed25519 signing test vector | [x] | [x] | [x] |
| 22 | Known transaction hash test vector | [x] | [x] | [x] |
| 23 | Known Secp256k1 signing test vector | [x] | [ ] | [x] |
| 24 | Known SingleKey authenticator test vector | [x] | [ ] | [x] |

### script.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create script payload from bytecode | [x] | [ ] | [ ] |
| 2 | Script payload with no arguments | [x] | [ ] | [ ] |
| 3 | Script payload with arguments | [x] | [ ] | [ ] |
| 4 | Script payload with type arguments | [x] | [ ] | [ ] |
| 5 | BCS serialize script payload | [x] | [ ] | [ ] |
| 6 | BCS deserialize script payload | [x] | [ ] | [ ] |
| 7 | Script serialization is deterministic | [x] | [ ] | [ ] |
| 8 | Compile Move script | [ ] | [ ] | [ ] |
| 9 | Compile script with dependencies | [ ] | [ ] | [ ] |
| 10 | Compile script with arguments | [ ] | [ ] | [ ] |
| 11 | Reject invalid Move script | [ ] | [ ] | [ ] |
| 12 | Load script from file | [ ] | [ ] | [ ] |
| 13 | Load script from hex string | [x] | [ ] | [ ] |
| 14 | Create raw transaction with script payload | [x] | [ ] | [ ] |
| 15 | Sign and submit script transaction | [x] | [ ] | [ ] |
| 16 | Script with signer argument | [x] | [ ] | [ ] |
| 17 | Script accesses sender | [x] | [ ] | [ ] |
| 18 | Script with multiple signers | [ ] | [ ] | [ ] |
| 19 | Script timeout and gas | [x] | [ ] | [ ] |
| 20 | Inline script in transaction | [x] | [ ] | [ ] |
| 21 | Complex script with loops | [ ] | [ ] | [ ] |
| 22 | Script calling module functions | [ ] | [ ] | [ ] |
| 23 | Script with abort | [x] | [ ] | [ ] |
| 24 | Script return values | [ ] | [ ] | [ ] |
| 25 | Known script payload test vector | [x] | [ ] | [ ] |

---

## 05-api-clients

### fullnode-api.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create API client with URL | [x] | [x] | [x] |
| 2 | API client URL normalization | [x] | [ ] | [x] |
| 3 | API client with custom headers | [x] | [ ] | [x] |
| 4 | Get ledger info | [x] | [x] | [x] |
| 5 | Ledger info contains chain ID | [x] | [x] | [x] |
| 6 | Ledger info contains epoch | [x] | [x] | [x] |
| 7 | Ledger info contains ledger version | [x] | [x] | [x] |
| 8 | Get account info | [x] | [x] | [x] |
| 9 | Account info contains sequence number | [x] | [x] | [x] |
| 10 | Account info contains authentication key | [x] | [x] | [x] |
| 11 | Get account not found | [x] | [x] | [x] |
| 12 | Get account resources | [x] | [x] | [x] |
| 13 | Get specific account resource | [x] | [x] | [x] |
| 14 | Get account modules | [x] | [ ] | [x] |
| 15 | Get transaction by hash | [x] | [x] | [x] |
| 16 | Get transaction by version | [x] | [x] | [x] |
| 17 | Get transactions | [x] | [x] | [x] |
| 18 | Get account transactions | [x] | [x] | [x] |
| 19 | Check transaction success | [x] | [x] | [x] |
| 20 | Check transaction failure | [x] | [x] | [x] |
| 21 | Get events by event key | [x] | [ ] | [x] |
| 22 | Get events by creation number | [x] | [ ] | [x] |
| 23 | Handle API 404 error | [x] | [x] | [x] |
| 24 | Handle API 400 error | [x] | [x] | [x] |
| 25 | Handle network error | [x] | [ ] | [x] |

### transaction-submission.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Submit valid signed transaction | [x] | [x] | [x] |
| 2 | Submit transaction with correct content type | [x] | [x] | [x] |
| 3 | Submit transaction returns hash | [x] | [x] | [x] |
| 4 | Reject invalid transaction format | [x] | [x] | [x] |
| 5 | Reject transaction with invalid signature | [x] | [x] | [x] |
| 6 | Reject transaction with wrong chain ID | [x] | [x] | [x] |
| 7 | Reject expired transaction | [x] | [ ] | [x] |
| 8 | Wait for transaction success | [x] | [x] | [x] |
| 9 | Wait for transaction timeout | [x] | [ ] | [x] |
| 10 | Wait returns success status | [x] | [x] | [x] |
| 11 | Wait returns failure status | [x] | [x] | [x] |
| 12 | Wait polls until completion | [x] | [ ] | [x] |
| 13 | Submit and wait for transaction | [x] | [x] | [x] |
| 14 | Sign, submit, and wait | [x] | [x] | [x] |
| 15 | Simulate transaction | [x] | [ ] | [x] |
| 16 | Simulate shows gas estimate | [x] | [ ] | [x] |
| 17 | Simulate shows VM error for failing tx | [~] | [ ] | [x] |
| 18 | Simulate with insufficient balance | [x] | [ ] | [x] |
| 19 | Simulate doesn't require valid signature | [x] | [ ] | [x] |
| 20 | Get gas price estimate | [x] | [ ] | [x] |
| 21 | Use gas estimate for transaction | [x] | [ ] | [x] |
| 22 | Get current sequence number | [x] | [x] | [x] |
| 23 | Submit with correct sequence number | [x] | [x] | [x] |
| 24 | Reject wrong sequence number | [x] | [x] | [x] |
| 25 | Submit multiple transactions in sequence | [x] | [ ] | [x] |
| 26 | Handle submission network error | [x] | [ ] | [x] |
| 27 | Handle VM error in response | [x] | [ ] | [x] |
| 28 | Transaction hash is predictable | [x] | [x] | [x] |

### faucet.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Fund account with default amount | [x] | [ ] | [ ] |
| 2 | Fund account with specific amount | [x] | [ ] | [ ] |
| 3 | Faucet returns transaction hashes | [x] | [ ] | [ ] |
| 4 | Fund creates account if not exists | [x] | [ ] | [ ] |
| 5 | Fund adds to existing balance | [x] | [ ] | [ ] |
| 6 | Configure faucet URL | [x] | [ ] | [ ] |
| 7 | Use devnet faucet | [x] | [ ] | [ ] |
| 8 | Use testnet faucet | [x] | [ ] | [ ] |
| 9 | Faucet not available on mainnet | [x] | [ ] | [ ] |
| 10 | Wait for faucet transaction | [x] | [ ] | [ ] |
| 11 | Fund and wait in one call | [x] | [ ] | [ ] |
| 12 | Handle faucet rate limiting | [x] | [ ] | [ ] |
| 13 | Handle faucet service unavailable | [x] | [ ] | [ ] |
| 14 | Faucet timeout | [x] | [ ] | [ ] |
| 15 | Fund multiple accounts | [x] | [ ] | [ ] |
| 16 | Fund with authentication | [x] | [ ] | [ ] |
| 17 | Balance after funding | [x] | [ ] | [ ] |
| 18 | New account with zero initial balance | [x] | [ ] | [ ] |
| 19 | Fund non-existent address format | [x] | [ ] | [ ] |
| 20 | Reject invalid faucet URL | [x] | [ ] | [ ] |
| 21 | Faucet transaction is coin transfer | [x] | [ ] | [ ] |
| 22 | Fund integration test accounts | [x] | [ ] | [ ] |
| 23 | Parallel funding | [x] | [ ] | [ ] |

### gas-estimation.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Get current gas price | [x] | [ ] | [ ] |
| 2 | Gas price is in octas | [x] | [ ] | [ ] |
| 3 | Gas price varies by network load | [x] | [ ] | [ ] |
| 4 | Estimate gas for simple transfer | [x] | [ ] | [ ] |
| 5 | Estimate gas for entry function call | [x] | [ ] | [ ] |
| 6 | Estimate gas for complex transaction | [x] | [ ] | [ ] |
| 7 | Gas estimate via simulation | [x] | [ ] | [ ] |
| 8 | Simulation returns gas_used | [x] | [ ] | [ ] |
| 9 | Add buffer to gas estimate | [x] | [ ] | [ ] |
| 10 | Calculate total fee from gas | [x] | [ ] | [ ] |
| 11 | Prioritized gas price | [x] | [ ] | [ ] |
| 12 | Deprioritized gas price | [x] | [ ] | [ ] |
| 13 | Auto-set gas unit price | [x] | [ ] | [ ] |
| 14 | Auto-set max gas amount | [x] | [ ] | [ ] |
| 15 | Override auto gas settings | [x] | [ ] | [ ] |
| 16 | Estimate fails for invalid transaction | [x] | [ ] | [ ] |
| 17 | Estimate for multi-agent transaction | [x] | [ ] | [ ] |
| 18 | Estimate for fee payer transaction | [x] | [ ] | [ ] |
| 19 | Historical gas prices | [ ] | [ ] | [ ] |
| 20 | Gas price percentiles | [ ] | [ ] | [ ] |
| 21 | Min and max gas price bounds | [x] | [ ] | [ ] |
| 22 | Gas estimation timeout | [x] | [ ] | [ ] |
| 23 | Estimate with specific account | [x] | [ ] | [ ] |
| 24 | Estimate without account (simulation only) | [x] | [ ] | [ ] |
| 25 | Gas varies by payload size | [x] | [ ] | [ ] |
| 26 | Storage gas costs | [x] | [ ] | [ ] |

### view-functions.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Execute simple view function | [x] | [ ] | [ ] |
| 2 | Execute view function without type arguments | [x] | [ ] | [ ] |
| 3 | Execute view function without arguments | [x] | [ ] | [ ] |
| 4 | Execute view function with multiple return values | [x] | [ ] | [ ] |
| 5 | Pass address argument | [x] | [ ] | [ ] |
| 6 | Pass u64 argument | [x] | [ ] | [ ] |
| 7 | Pass string argument | [x] | [ ] | [ ] |
| 8 | Pass vector argument | [x] | [ ] | [ ] |
| 9 | Pass bool argument | [x] | [ ] | [ ] |
| 10 | Single type argument | [x] | [ ] | [ ] |
| 11 | Multiple type arguments | [x] | [ ] | [ ] |
| 12 | Nested type argument | [x] | [ ] | [ ] |
| 13 | Parse u64 return value | [x] | [ ] | [ ] |
| 14 | Parse string return value | [x] | [ ] | [ ] |
| 15 | Parse bool return value | [x] | [ ] | [ ] |
| 16 | Parse vector return value | [x] | [ ] | [ ] |
| 17 | Parse struct return value | [x] | [ ] | [ ] |
| 18 | View function not found | [x] | [ ] | [ ] |
| 19 | Invalid arguments | [x] | [ ] | [ ] |
| 20 | Wrong number of arguments | [x] | [ ] | [ ] |
| 21 | Wrong number of type arguments | [x] | [ ] | [ ] |
| 22 | View function aborts | [x] | [ ] | [ ] |
| 23 | Get coin balance | [x] | [ ] | [ ] |
| 24 | Check account exists | [x] | [ ] | [ ] |
| 25 | Get current timestamp | [x] | [ ] | [ ] |
| 26 | Get coin supply | [x] | [ ] | [ ] |
| 27 | Execute view function at specific version | [x] | [ ] | [ ] |
| 28 | View function at too old version | [x] | [ ] | [ ] |

### retry.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Retry on network timeout | [x] | [ ] | [ ] |
| 2 | Retry on connection refused | [x] | [ ] | [ ] |
| 3 | Retry on 5xx server error | [x] | [ ] | [ ] |
| 4 | No retry on 4xx client error | [x] | [ ] | [ ] |
| 5 | Configure max retry attempts | [x] | [ ] | [ ] |
| 6 | Configure retry delay | [x] | [ ] | [ ] |
| 7 | Exponential backoff | [x] | [ ] | [ ] |
| 8 | Jitter in retry delay | [x] | [ ] | [ ] |
| 9 | Max retry delay cap | [x] | [ ] | [ ] |
| 10 | Retry callback/hook | [x] | [ ] | [ ] |
| 11 | Custom retry condition | [x] | [ ] | [ ] |
| 12 | Retry specific status codes | [x] | [ ] | [ ] |
| 13 | No retry by default | [x] | [ ] | [ ] |
| 14 | Retry preserves request | [x] | [ ] | [ ] |
| 15 | Total timeout across retries | [x] | [ ] | [ ] |
| 16 | Circuit breaker pattern | [ ] | [ ] | [ ] |
| 17 | Retry on rate limit (429) | [x] | [ ] | [ ] |
| 18 | Respect Retry-After header | [x] | [ ] | [ ] |
| 19 | Retry only idempotent operations | [x] | [ ] | [ ] |
| 20 | No retry on submit (non-idempotent) | [x] | [ ] | [ ] |
| 21 | Retry with fresh data | [x] | [ ] | [ ] |
| 22 | Log retry attempts | [x] | [ ] | [ ] |
| 23 | Retry statistics | [ ] | [ ] | [ ] |
| 24 | Abort retry on fatal error | [x] | [ ] | [ ] |
| 25 | Graceful degradation | [ ] | [ ] | [ ] |
| 26 | Retry for wait_for_transaction | [x] | [ ] | [ ] |
| 27 | Transaction not found during retry | [x] | [ ] | [ ] |
| 28 | Health check before retry | [ ] | [ ] | [ ] |
| 29 | Per-endpoint retry config | [ ] | [ ] | [ ] |
| 30 | Retry context propagation | [ ] | [ ] | [ ] |
| 31 | Retry metrics/telemetry | [ ] | [ ] | [ ] |
| 32 | Concurrent request retry | [x] | [ ] | [ ] |

### indexer.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create indexer client | [x] | [ ] | [ ] |
| 2 | Configure indexer URL | [x] | [ ] | [ ] |
| 3 | Query account tokens | [x] | [ ] | [ ] |
| 4 | Query token by ID | [x] | [ ] | [ ] |
| 5 | Query collection | [x] | [ ] | [ ] |
| 6 | Query account NFTs | [x] | [ ] | [ ] |
| 7 | Query fungible asset balances | [x] | [ ] | [ ] |
| 8 | Query fungible asset metadata | [x] | [ ] | [ ] |
| 9 | Query coin activities | [x] | [ ] | [ ] |
| 10 | Query token activities | [x] | [ ] | [ ] |
| 11 | Query events by type | [x] | [ ] | [ ] |
| 12 | Query events by account | [x] | [ ] | [ ] |
| 13 | Query transactions by account | [x] | [ ] | [ ] |
| 14 | Query transactions by function | [x] | [ ] | [ ] |
| 15 | Query with pagination | [x] | [ ] | [ ] |
| 16 | Query with limit | [x] | [ ] | [ ] |
| 17 | Query with offset | [x] | [ ] | [ ] |
| 18 | Query with ordering | [x] | [ ] | [ ] |
| 19 | Query with filtering | [x] | [ ] | [ ] |
| 20 | Query with multiple filters | [x] | [ ] | [ ] |
| 21 | Raw GraphQL query | [x] | [ ] | [ ] |
| 22 | GraphQL query variables | [x] | [ ] | [ ] |
| 23 | Handle indexer lag | [x] | [ ] | [ ] |
| 24 | Handle indexer unavailable | [x] | [ ] | [ ] |
| 25 | Handle invalid query | [x] | [ ] | [ ] |
| 26 | Account current holdings | [x] | [ ] | [ ] |
| 27 | Account transaction history | [x] | [ ] | [ ] |
| 28 | Get ANS name for address | [x] | [ ] | [ ] |
| 29 | Get address for ANS name | [x] | [ ] | [ ] |
| 30 | Query processor status | [x] | [ ] | [ ] |
| 31 | Query latest indexed version | [x] | [ ] | [ ] |

---

## 06-advanced

### error-handling.feature `@required`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Network errors are distinguishable | [x] | [ ] | [x] |
| 2 | API errors include status code | [x] | [ ] | [x] |
| 3 | Validation errors are informative | [x] | [ ] | [x] |
| 4 | Transaction errors include details | [x] | [ ] | [x] |
| 5 | Parse success status | [x] | [ ] | [x] |
| 6 | Parse execution failure | [x] | [ ] | [x] |
| 7 | Parse out of gas failure | [x] | [ ] | [x] |
| 8 | Parse sequence number error | [x] | [ ] | [x] |
| 9 | Parse insufficient balance error | [x] | [ ] | [x] |
| 10 | Recognize standard abort codes | [x] | [ ] | [x] |
| 11 | Custom module abort codes | [x] | [ ] | [x] |
| 12 | Errors include operation context | [x] | [ ] | [x] |
| 13 | Errors are chainable | [x] | [ ] | [x] |
| 14 | Errors include request ID | [x] | [ ] | [x] |
| 15 | TypeScript uses typed errors | [x] | [ ] | [ ] |
| 16 | Rust uses Result types | [ ] | [ ] | [x] |
| 17 | Python uses exceptions | [ ] | [ ] | [ ] |
| 18 | Go uses error interface | [ ] | [x] | [ ] |
| 19 | Identify retryable errors | [x] | [ ] | [x] |
| 20 | Identify permanent failures | [x] | [ ] | [x] |
| 21 | Simulation failure with details | [x] | [ ] | [x] |
| 22 | Simulation gas estimation | [x] | [ ] | [x] |
| 23 | Transaction not found during wait | [x] | [ ] | [x] |
| 24 | Transaction failed during wait | [x] | [ ] | [x] |
| 25 | Error messages are actionable | [x] | [ ] | [x] |
| 26 | No internal jargon in user-facing errors | [x] | [ ] | [x] |
| 27 | Errors are loggable | [x] | [ ] | [x] |
| 28 | Sequence number recovery | [x] | [ ] | [x] |
| 29 | Gas estimation recovery | [x] | [ ] | [x] |
| 30 | Rate limit recovery | [x] | [ ] | [x] |

### simulation.feature `@preferred`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Simulate valid transaction | [x] | [ ] | [ ] |
| 2 | Simulate without signing | [x] | [ ] | [ ] |
| 3 | Simulation result includes changes | [x] | [ ] | [ ] |
| 4 | Use simulation for gas estimation | [x] | [ ] | [ ] |
| 5 | Simulation shows max_gas_amount needed | [x] | [ ] | [ ] |
| 6 | Gas varies by transaction complexity | [x] | [ ] | [ ] |
| 7 | Preview balance changes | [x] | [ ] | [ ] |
| 8 | Preview resource changes | [x] | [ ] | [ ] |
| 9 | Preview events | [x] | [ ] | [ ] |
| 10 | Simulation shows abort | [x] | [ ] | [ ] |
| 11 | Simulation shows insufficient balance | [x] | [ ] | [ ] |
| 12 | Simulation shows type errors | [x] | [ ] | [ ] |
| 13 | Simulation catches access errors | [x] | [ ] | [ ] |
| 14 | Simulate at specific version | [x] | [ ] | [ ] |
| 15 | Simulate with gas override | [x] | [ ] | [ ] |
| 16 | Simulate with gas price override | [x] | [ ] | [ ] |
| 17 | Simulate multi-agent transaction | [x] | [ ] | [ ] |
| 18 | Simulate fee payer transaction | [x] | [ ] | [ ] |
| 19 | Simulation does not commit changes | [x] | [ ] | [ ] |
| 20 | Simulation results may differ from execution | [x] | [ ] | [ ] |
| 21 | Simulation with current sequence number | [x] | [ ] | [ ] |
| 22 | Simulate multiple transactions | [ ] | [ ] | [ ] |
| 23 | Simulate transaction sequence | [ ] | [ ] | [ ] |
| 24 | Simulation network error | [ ] | [ ] | [ ] |
| 25 | Invalid transaction for simulation | [ ] | [ ] | [ ] |
| 26 | Simulation timeout | [ ] | [ ] | [ ] |

### multi-agent.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create multi-agent transaction with one secondary signer | [x] | [ ] | [ ] |
| 2 | Create multi-agent transaction with multiple secondary signers | [x] | [ ] | [ ] |
| 3 | Secondary signer addresses are preserved | [x] | [ ] | [ ] |
| 4 | Multi-agent signing message differs from single signer | [x] | [ ] | [ ] |
| 5 | Multi-agent signing message includes secondary addresses | [x] | [ ] | [ ] |
| 6 | Multi-agent signing message uses correct domain | [x] | [ ] | [ ] |
| 7 | All parties sign the same message | [x] | [ ] | [ ] |
| 8 | Sign multi-agent transaction | [x] | [ ] | [ ] |
| 9 | Multi-agent authenticator structure | [x] | [ ] | [ ] |
| 10 | Multi-agent with mixed account types | [x] | [ ] | [ ] |
| 11 | Collect signatures from multiple parties | [x] | [ ] | [ ] |
| 12 | Signatures can be collected in any order | [x] | [ ] | [ ] |
| 13 | Reject incomplete signature collection | [x] | [ ] | [ ] |
| 14 | Reject mismatched secondary signer count | [x] | [ ] | [ ] |
| 15 | Reject empty secondary signers | [x] | [ ] | [ ] |
| 16 | Secondary signer address must match signature | [x] | [ ] | [ ] |
| 17 | Serialize multi-agent authenticator | [x] | [ ] | [ ] |
| 18 | Multi-agent transaction serialization is deterministic | [x] | [ ] | [ ] |
| 19 | Known multi-agent signing message test vector | [x] | [ ] | [ ] |
| 20 | Known multi-agent transaction test vector | [x] | [ ] | [ ] |

### fee-payer.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create fee payer transaction with sponsor | [x] | [ ] | [ ] |
| 2 | Create fee payer transaction with secondary signers | [x] | [ ] | [ ] |
| 3 | Fee payer address is preserved | [x] | [ ] | [ ] |
| 4 | Fee payer signing message differs from multi-agent | [x] | [ ] | [ ] |
| 5 | Fee payer signing message includes fee payer address | [x] | [ ] | [ ] |
| 6 | Fee payer signing message uses correct domain | [x] | [ ] | [ ] |
| 7 | All parties (including fee payer) sign the same message | [x] | [ ] | [ ] |
| 8 | Sign fee payer transaction | [x] | [ ] | [ ] |
| 9 | Fee payer authenticator structure | [x] | [ ] | [ ] |
| 10 | Fee payer with no secondary signers | [x] | [ ] | [ ] |
| 11 | Fee payer with mixed account types | [x] | [ ] | [ ] |
| 12 | Sender initiates sponsored transaction | [x] | [ ] | [ ] |
| 13 | Sponsor completes sponsored transaction | [x] | [ ] | [ ] |
| 14 | Signatures can be collected in any order | [x] | [ ] | [ ] |
| 15 | Fee payer pays gas regardless of sender gas fields | [x] | [ ] | [ ] |
| 16 | Transaction fails if fee payer has insufficient gas | [x] | [ ] | [ ] |
| 17 | Reject missing fee payer signature | [x] | [ ] | [ ] |
| 18 | Reject missing sender signature | [x] | [ ] | [ ] |
| 19 | Fee payer address must match signature | [x] | [ ] | [ ] |
| 20 | Serialize fee payer authenticator | [x] | [ ] | [ ] |
| 21 | Fee payer transaction serialization is deterministic | [x] | [ ] | [ ] |
| 22 | Known fee payer signing message test vector | [x] | [ ] | [ ] |
| 23 | Known fee payer transaction test vector | [x] | [ ] | [ ] |

### multi-signature.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Create 2-of-3 multi-sig account | [x] | [ ] | [ ] |
| 2 | Create 1-of-1 multi-sig account | [x] | [ ] | [ ] |
| 3 | Create multi-sig with all keys required | [x] | [ ] | [ ] |
| 4 | Reject threshold of 0 | [x] | [ ] | [ ] |
| 5 | Reject threshold greater than key count | [x] | [ ] | [ ] |
| 6 | Reject empty key list | [x] | [ ] | [ ] |
| 7 | Multi-sig authentication key derivation | [x] | [ ] | [ ] |
| 8 | Key order affects authentication key | [x] | [ ] | [ ] |
| 9 | Same keys same order produce same address | [x] | [ ] | [ ] |
| 10 | Sign with enough private keys | [x] | [ ] | [ ] |
| 11 | Cannot sign without enough keys | [x] | [ ] | [ ] |
| 12 | Collect signatures from multiple parties | [x] | [ ] | [ ] |
| 13 | Reject duplicate signer indices | [x] | [ ] | [ ] |
| 14 | Reject invalid signer index | [x] | [ ] | [ ] |
| 15 | Multi-sig signature contains indices | [x] | [ ] | [ ] |
| 16 | Signatures are ordered by index | [x] | [ ] | [ ] |
| 17 | Sign transaction with multi-sig account | [x] | [ ] | [ ] |
| 18 | Multi-sig transaction authenticator structure | [x] | [ ] | [ ] |
| 19 | Verify multi-sig signature | [x] | [ ] | [ ] |
| 20 | Reject signature with insufficient signers | [x] | [ ] | [ ] |
| 21 | Reject signature with wrong signers | [x] | [ ] | [ ] |
| 22 | Known multi-sig address test vector | [x] | [ ] | [ ] |
| 23 | Known multi-sig signature test vector | [x] | [ ] | [ ] |

### keyless.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Generate ephemeral key pair | [x] | [ ] | [ ] |
| 2 | Ephemeral key pair generates unique nonce | [x] | [ ] | [ ] |
| 3 | Check ephemeral key expiry | [x] | [ ] | [ ] |
| 4 | Fresh ephemeral key is not expired | [x] | [ ] | [ ] |
| 5 | Get ephemeral nonce for OIDC flow | [x] | [ ] | [ ] |
| 6 | Create keyless account from JWT | [x] | [ ] | [ ] |
| 7 | Keyless account has correct provider | [x] | [ ] | [ ] |
| 8 | Keyless account address is deterministic | [x] | [ ] | [ ] |
| 9 | Different users have different addresses | [x] | [ ] | [ ] |
| 10 | Keyless address derivation formula | [x] | [ ] | [ ] |
| 11 | Different issuers produce different addresses | [x] | [ ] | [ ] |
| 12 | Different audiences produce different addresses | [x] | [ ] | [ ] |
| 13 | Pepper affects address | [x] | [ ] | [ ] |
| 14 | Sign message with keyless account | [x] | [ ] | [ ] |
| 15 | Sign transaction with keyless account | [x] | [ ] | [ ] |
| 16 | Reject signing with expired ephemeral key | [x] | [ ] | [ ] |
| 17 | Check if keyless account is valid | [x] | [ ] | [ ] |
| 18 | Keyless account with expired proof | [x] | [ ] | [ ] |
| 19 | Refresh proof | [x] | [ ] | [ ] |
| 20 | Google provider configuration | [x] | [ ] | [ ] |
| 21 | Apple provider configuration | [x] | [ ] | [ ] |
| 22 | Custom OIDC provider | [x] | [ ] | [ ] |
| 23 | Get pepper for JWT | [x] | [ ] | [ ] |
| 24 | Same JWT produces same pepper | [x] | [ ] | [ ] |
| 25 | Handle pepper service error | [x] | [ ] | [ ] |
| 26 | Generate ZK proof | [x] | [ ] | [ ] |
| 27 | Handle prover service error | [x] | [ ] | [ ] |
| 28 | Reject invalid JWT format | [x] | [ ] | [ ] |
| 29 | Reject JWT with wrong nonce | [x] | [ ] | [ ] |
| 30 | Reject expired JWT | [x] | [ ] | [ ] |
| 31 | Ephemeral key expiry is enforced | [x] | [ ] | [ ] |
| 32 | Pepper is not exposed in account | [x] | [ ] | [ ] |
| 33 | Known keyless address test vector | [x] | [ ] | [ ] |

### codegen.feature `@optional`

| # | Scenario | TypeScript | Go | Rust |
|---|----------|------------|-----|------|
| 1 | Fetch module ABI from chain | [ ] | [ ] | [ ] |
| 2 | Fetch ABI for multiple modules | [ ] | [ ] | [ ] |
| 3 | Handle module not found | [ ] | [ ] | [ ] |
| 4 | Parse entry functions from ABI | [ ] | [ ] | [ ] |
| 5 | Parse view functions from ABI | [ ] | [ ] | [ ] |
| 6 | Parse struct definitions from ABI | [ ] | [ ] | [ ] |
| 7 | Parse generic types | [ ] | [ ] | [ ] |
| 8 | Generate TypeScript types for structs | [ ] | [ ] | [ ] |
| 9 | Generate TypeScript function wrappers | [ ] | [ ] | [ ] |
| 10 | Generate TypeScript view function wrappers | [ ] | [ ] | [ ] |
| 11 | Map Move types to TypeScript | [ ] | [ ] | [ ] |
| 12 | Generate Rust types for structs | [ ] | [ ] | [ ] |
| 13 | Generate Rust function wrappers | [ ] | [ ] | [ ] |
| 14 | Map Move types to Rust | [ ] | [ ] | [ ] |
| 15 | Generate Python types for structs | [ ] | [ ] | [ ] |
| 16 | Generate Python function wrappers | [ ] | [ ] | [ ] |
| 17 | Generate Go types for structs | [ ] | [ ] | [ ] |
| 18 | Generate Go function wrappers | [ ] | [ ] | [ ] |
| 19 | Generated code handles address encoding | [ ] | [ ] | [ ] |
| 20 | Generated code handles u64 encoding | [ ] | [ ] | [ ] |
| 21 | Generated code handles vector encoding | [ ] | [ ] | [ ] |
| 22 | Generated code handles struct encoding | [ ] | [ ] | [ ] |
| 23 | Compile-time type checking | [ ] | [ ] | [ ] |
| 24 | Type inference for generics | [ ] | [ ] | [ ] |
| 25 | Optional parameters handling | [ ] | [ ] | [ ] |
| 26 | Generate code via CLI | [ ] | [ ] | [ ] |
| 27 | CLI supports multiple output formats | [ ] | [ ] | [ ] |
| 28 | CLI from local ABI file | [ ] | [ ] | [ ] |
| 29 | Procedural macro for contract bindings | [ ] | [ ] | [ ] |
| 30 | Macro fetches ABI at build time | [ ] | [ ] | [ ] |
| 31 | Generated code surfaces Move errors | [ ] | [ ] | [ ] |
| 32 | Generated code validates arguments | [ ] | [ ] | [ ] |
| 33 | Generate documentation comments | [ ] | [ ] | [ ] |
| 34 | Include function signatures in docs | [ ] | [ ] | [ ] |

---

## Maintenance

This file should be updated when:

1. New step definitions are added to any SDK
2. Tests are verified to pass
3. New scenarios are added to feature files

To check current status, run:

```bash
# TypeScript
cd tests/typescript && bun run cucumber-js --dry-run --format summary

# Go
cd tests/go && go test -v ./...

# Rust
cd tests/rust && cargo test --test specs
```
