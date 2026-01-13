# Account Management Specification

## Overview

The account management module provides abstractions for Aptos accounts, including key management, address derivation, and signing capabilities. It wraps cryptographic primitives with a user-friendly interface.

## Goals

1. Provide unified Account interface for all account types
2. Support multiple signature schemes transparently
3. Enable easy account creation from various sources
4. Secure key handling with proper memory management

## Non-Goals

- Wallet UI functionality
- Key storage/persistence (users handle this)
- Account state management (handled by API clients)

---

## Account Interface

### Description

A common interface that all account types must implement, enabling polymorphic usage.

### Required Methods

| Method | Priority | Description |
|--------|----------|-------------|
| `address()` | P0 | Get the account's address |
| `public_key_bytes()` | P0 | Get public key as bytes |
| `signature_scheme()` | P0 | Get the signature scheme identifier |
| `sign(message)` | P0 | Sign arbitrary bytes |
| `authentication_key()` | P0 | Get the authentication key |

### Signature Schemes

| Scheme | Identifier | Priority |
|--------|------------|----------|
| Ed25519 | ed25519 | P0 |
| Secp256k1 | secp256k1_ecdsa | P1 |
| Secp256r1 | secp256r1_ecdsa | P2 |
| MultiEd25519 | multi_ed25519 | P2 |
| MultiKey | multi_key | P2 |

---

## Ed25519Account (Required - P0)

### Description

Single-key account using Ed25519 signature scheme. This is the primary account type for Aptos.

### Construction

| Method | Priority | Description |
|--------|----------|-------------|
| `generate()` | P0 | Generate new random account |
| `from_private_key(key)` | P0 | Create from Ed25519 private key |
| `from_private_key_hex(hex)` | P0 | Create from hex-encoded private key |
| `from_private_key_bytes(bytes)` | P0 | Create from private key bytes |
| `from_mnemonic(mnemonic)` | P1 | Create from BIP-39 mnemonic (default path) |
| `from_mnemonic_with_path(mnemonic, path)` | P1 | Create with custom derivation path |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| address | AccountAddress | The account's on-chain address |
| public_key | Ed25519PublicKey | The public key |
| private_key | Ed25519PrivateKey | The private key (not exposed in Debug) |

### Methods

| Method | Priority | Description |
|--------|----------|-------------|
| `address()` | P0 | Get account address |
| `public_key()` | P0 | Get public key reference |
| `sign(message)` | P0 | Sign arbitrary bytes |
| `sign_transaction(raw_txn)` | P0 | Sign a raw transaction |

### Address Derivation

For Ed25519 accounts:
```
authentication_key = SHA3-256(public_key || 0x00)
address = authentication_key
```

---

## Secp256k1Account (Preferred - P1)

### Description

Single-key account using Secp256k1 ECDSA signature scheme.

### Construction

| Method | Priority | Description |
|--------|----------|-------------|
| `generate()` | P1 | Generate new random account |
| `from_private_key(key)` | P1 | Create from Secp256k1 private key |
| `from_private_key_hex(hex)` | P1 | Create from hex-encoded private key |
| `from_mnemonic(mnemonic)` | P1 | Create from BIP-39 mnemonic |

### Address Derivation

For Secp256k1 accounts:
```
authentication_key = SHA3-256(uncompressed_public_key || 0x01)
address = authentication_key
```

---

## Mnemonic-Based Accounts (Preferred - P1)

### BIP-39 Mnemonics

| Method | Priority | Description |
|--------|----------|-------------|
| `generate(word_count)` | P1 | Generate random mnemonic (12, 15, 18, 21, 24) |
| `from_phrase(phrase)` | P1 | Parse existing mnemonic phrase |
| `validate()` | P1 | Validate checksum |
| `phrase()` | P1 | Get the mnemonic phrase as string |
| `to_seed(passphrase)` | P1 | Derive 64-byte seed |

### BIP-44 Derivation

Default Aptos derivation path:
```
m/44'/637'/0'/0'/0'
```

Path components:
- `44'` - BIP-44 purpose
- `637'` - Aptos coin type
- `0'` - Account index
- `0'` - Change (always 0 for Aptos)
- `0'` - Address index

### Deriving Multiple Accounts

```
Account 0: m/44'/637'/0'/0'/0'
Account 1: m/44'/637'/0'/0'/1'
Account 2: m/44'/637'/0'/0'/2'
```

---

## AnyAccount / Dynamic Account (Preferred - P1)

### Description

Type-erased account for runtime polymorphism when the account type isn't known at compile time.

### Variants

| Variant | Priority | Description |
|---------|----------|-------------|
| Ed25519 | P0 | Wraps Ed25519Account |
| Secp256k1 | P1 | Wraps Secp256k1Account |
| Secp256r1 | P2 | Wraps Secp256r1Account |
| MultiEd25519 | P2 | Wraps MultiEd25519Account |
| MultiKey | P2 | Wraps MultiKeyAccount |

### Usage Pattern

```
// Load account from config without knowing type at compile time
let account = match config.key_type {
    "ed25519" => AnyAccount::ed25519(Ed25519Account::from_hex(key)),
    "secp256k1" => AnyAccount::secp256k1(Secp256k1Account::from_hex(key)),
    _ => error,
};

// Use uniformly
let signature = account.sign(message);
```

---

## AuthenticationKey

### Description

32-byte value derived from public key, used to derive account addresses.

### Construction

| Method | Priority | Description |
|--------|----------|-------------|
| `from_ed25519(public_key)` | P0 | Derive from Ed25519 public key |
| `from_secp256k1(public_key)` | P1 | Derive from Secp256k1 public key |
| `from_public_key(bytes, scheme)` | P0 | Derive from any public key |
| `from_bytes(bytes)` | P0 | Create from raw 32 bytes |

### Methods

| Method | Priority | Description |
|--------|----------|-------------|
| `account_address()` | P0 | Convert to AccountAddress |
| `as_bytes()` | P0 | Get raw 32-byte array |

### Derivation Formula

```
auth_key = SHA3-256(public_key_bytes || scheme_identifier)
```

---

## Error Handling

### Required Error Cases

| Error | Cause | Priority |
|-------|-------|----------|
| InvalidPrivateKey | Malformed private key bytes | P0 |
| InvalidMnemonic | Bad mnemonic phrase | P1 |
| InvalidDerivationPath | Malformed BIP-44 path | P1 |
| KeyDerivationFailed | Path derivation error | P1 |
| UnsupportedScheme | Requested scheme not available | P1 |

---

## Security Considerations

### Private Key Handling

1. **Memory Zeroization**: Private keys must be zeroized when dropped
2. **No Display/Debug**: Private keys must not implement Display or expose in Debug
3. **No Default Serialize**: Private keys should not be easily serialized
4. **Explicit Clone**: Cloning requires explicit method call with security acknowledgment

### Mnemonic Security

1. **Entropy Quality**: Use CSPRNG for generation
2. **Checksum Validation**: Always validate checksum on parse
3. **Seed Zeroization**: Zeroize intermediate seed after derivation

### Account Security

1. **Address Validation**: Always verify addresses before use
2. **Signing Confirmation**: Clear indication when signing occurs
3. **Key Export Warnings**: Warn users when exporting private keys

---

## Cross-SDK Compatibility

All SDKs must produce identical:
1. Addresses from the same private key
2. Authentication keys from the same public key
3. Derived accounts from the same mnemonic and path
4. Signatures for the same transaction

Test vectors in `test-vectors/mnemonics.json` provide deterministic test cases.

