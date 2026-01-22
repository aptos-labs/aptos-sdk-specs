# Swift SDK Test Status

> **Last Updated:** 2026-01-22

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `aptos-swift-sdk` |
| **Version Tested** | main (bf2aa06) |
| **Publisher** | ALCOVE-LAB |
| **Repository** | https://github.com/ALCOVE-LAB/aptos-swift-sdk |
| **Package Manager** | Swift Package Manager |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | 286 | 306 | 93% |
| Preferred (P1) | 0 | 183 | 0% |
| Optional (P2) | 0 | 250 | 0% |
| **Total** | 286 | 739 | 39% |

## Feature Availability

Features confirmed working:

| Feature | Status | Tests |
|---------|--------|-------|
| AccountAddress | ✅ | 32 |
| Ed25519 | ✅ | 18 |
| Secp256k1 | ✅ | 18 |
| Mnemonic/BIP-44 | ✅ | 9 |
| BCS Serialization | ✅ | 23 |
| TypeTag | ✅ | 32 |
| Hashing | ✅ | 9 |
| AuthenticationKey | ✅ | 8 |
| Account | ✅ | 22 |
| Hex Utilities | ✅ | 18 |
| Identifier | ✅ | 6 |
| ModuleId | ✅ | 6 |
| ChainId | ✅ | 9 |
| Move Primitives | ✅ | 12 |
| MoveString | ✅ | 5 |
| MoveVector | ✅ | 6 |
| MoveOption | ✅ | 12 |
| Network Config | ✅ | 19 |
| AptosConfig | ✅ | 6 |
| Signatures | ✅ | 7 |
| PublicKeys | ✅ | 9 |

## Tests Implemented (286 total)

### Address Tests (32 tests)
- [x] Parse hex with/without prefix
- [x] Parse full 64-char hex
- [x] Parse various formats
- [x] Parse uppercase/mixed case hex
- [x] Reject invalid inputs
- [x] Format to full/short hex
- [x] Standard constants (ZERO, ONE, THREE, FOUR)
- [x] Equality comparisons
- [x] BCS serialize/deserialize/round-trip
- [x] IsSpecial detection

### Ed25519 Tests (18 tests)
- [x] Key generation (random, from seed, from hex)
- [x] Sign message (normal, empty, deterministic)
- [x] Verify signature (valid, wrong key, wrong message)
- [x] Export keys (bytes, hex)
- [x] Derive auth key and address

### Secp256k1 Tests (18 tests)
- [x] Key generation (random, from seed, from hex)
- [x] Sign message (normal, empty)
- [x] Verify signature (valid, wrong key, wrong message)
- [x] Export keys (bytes, hex)
- [x] Uncompressed public key format (65 bytes)

### Account Tests (22 tests)
- [x] Generate random accounts
- [x] Create from private key
- [x] Sign and verify messages
- [x] Signature schemes (Ed25519, SingleKey)
- [x] SingleKey with Secp256k1

### Mnemonic/BIP-44 Tests (9 tests)
- [x] Ed25519 derivation path
- [x] Secp256k1 derivation path
- [x] Account from derivation path
- [x] Reject invalid paths

### TypeTag Tests (32 tests)
- [x] Parse primitives (bool, u8-u256, address, signer)
- [x] Parse vectors (simple, nested)
- [x] Parse structs (simple, with type args)
- [x] Format types
- [x] Reject invalid types
- [x] StructTag helpers (aptosCoin, string, option, object)
- [x] BCS serialization

### Hashing Tests (9 tests)
- [x] SHA3-256 (empty, hello, deterministic)
- [x] SHA2-256 (empty, hello)
- [x] Large data hashing

### AuthenticationKey Tests (8 tests)
- [x] Derive from Ed25519
- [x] Same/different public keys
- [x] Convert to address
- [x] Export (bytes, hex)

### BCS Serialization Tests (23 tests)
- [x] Bool, U8, U16, U32, U64, U128
- [x] Strings and bytes
- [x] ULEB128 encoding
- [x] AccountAddress

### Hex Utility Tests (18 tests)
- [x] Parse with/without prefix
- [x] Format (toString, without prefix)
- [x] From bytes/Data
- [x] Equality comparisons
- [x] Validation
- [x] Case normalization

### Identifier Tests (6 tests)
- [x] Create and equality
- [x] BCS serialization

### ModuleId Tests (6 tests)
- [x] Create and fromStr
- [x] BCS serialization
- [x] Reject invalid format

### ChainId Tests (9 tests)
- [x] Create for networks
- [x] BCS serialization

### Move Primitive Tests (12 tests)
- [x] Boolean, U8, U16, U32, U64
- [x] BCS round-trip

### MoveString Tests (5 tests)
- [x] Create and serialize
- [x] Unicode support

### MoveVector Tests (6 tests)
- [x] U8, U64, Boolean, String vectors
- [x] BCS serialization

### MoveOption Tests (12 tests)
- [x] Some/None values
- [x] BCS serialization

### Network Configuration Tests (19 tests)
- [x] Network names (mainnet, testnet, devnet, local)
- [x] Chain IDs
- [x] Full node URLs
- [x] Indexer URLs
- [x] Faucet URLs
- [x] Custom network configuration

### AptosConfig Tests (6 tests)
- [x] Preset configurations (mainnet, testnet, devnet, localnet)
- [x] Custom network

### Signature Tests (7 tests)
- [x] Ed25519 signature length and creation
- [x] Secp256k1 signature length and creation
- [x] Reject invalid lengths

### PublicKey Tests (9 tests)
- [x] Ed25519 public key (length, from bytes/hex)
- [x] Secp256k1 public key (length, uncompressed prefix)
- [x] Reject invalid lengths

## Known SDK Behaviors

### Address Formatting
- `toString()` only shortens "special" addresses (0x0 through 0xf)
- Non-special addresses return full 64-char format from `toString()`
- Use `toStringLong()` for consistent full format
- "Special" is defined as: last byte < 16 AND all other bytes are 0

### Signing
- Ed25519 signatures verify correctly
- Secp256k1 signatures use SHA3-256 hashing internally
- Account.sign() uses underlying key's signing

### BIP-44 Derivation
- Ed25519 uses hardened path: `m/44'/637'/0'/0'/0'`
- Secp256k1 uses standard path: `m/44'/637'/0'/0/0`

## Known Issues

None currently - all implemented tests pass.

## SDK-Specific Notes

- Uses XCTest for testing (CucumberSwift has SPM compatibility issues)
- Swift 6.2+ required
- Requires Xcode (not just Command Line Tools) for XCTest support
- SDK provides comprehensive type safety with Swift's strong typing

## How to Run Tests

```bash
cd tests/swift

# Run all tests
swift test

# Run with verbose output
swift test --verbose
```

## Contributing

To add tests for this SDK:

1. Add test methods to `Tests/AptosSpecsTests/AptosSpecsTests.swift`
2. Follow the naming pattern `test_<Feature>_<Scenario>()`
3. Update this file's coverage summary
4. Run `swift test` to verify
