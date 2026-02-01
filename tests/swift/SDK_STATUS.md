# Swift SDK Test Status

> **Last Updated:** 2026-01-28  
> **Last Verified:** 2026-01-28 via `swift test`

---

## 1. SDK Information

| Property             | Value                                         |
| -------------------- | --------------------------------------------- |
| **Package**          | `aptos-swift-sdk`                             |
| **Version Tested**   | main                                          |
| **Publisher**        | ALCOVE-LAB (community)                        |
| **Repository**       | https://github.com/ALCOVE-LAB/aptos-swift-sdk |
| **Package Registry** | Swift Package Manager                         |
| **Test Framework**   | XCTest                                        |

---

## 2. Coverage Summary

| Priority       | Passing | Total   | Percentage | Status |
| -------------- | ------- | ------- | ---------- | ------ |
| Required (P0)  | 286     | 370     | 77%        | 🟡     |
| Preferred (P1) | 0       | 183     | 0%         | ❌     |
| Optional (P2)  | 0       | 250     | 0%         | ❌     |
| **Total**      | **286** | **826** | **35%**    | 🟡     |

> **Notes:**
>
> - XCTest-based tests: 286 tests passed (0 failures)
> - Test duration: ~2.6 seconds
> - Community SDK from ALCOVE-LAB
> - Requires Xcode (not just Command Line Tools)
> - CucumberSwift step definitions prepared for future BDD integration

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature             | Tests | Notes                               |
| ------------------- | ----- | ----------------------------------- |
| address             | 32    | Full address parsing and formatting |
| serialization       | 23    | Complete BCS serialization          |
| type-tags           | 32    | Full TypeTag parsing                |
| ed25519             | 18    | Complete Ed25519 support            |
| secp256k1           | 18    | Full Secp256k1 support              |
| hashing             | 9     | SHA3-256 and SHA2-256               |
| authentication-key  | 8     | Auth key derivation                 |
| mnemonic-derivation | 9     | BIP-39/BIP-44 support               |
| single-key          | 22    | SingleKey account support           |

### 🟡 Partially Available

| Feature         | Reason                       | Impact                    |
| --------------- | ---------------------------- | ------------------------- |
| entry-function  | Step definitions not written | Needs test implementation |
| raw-transaction | Step definitions not written | Needs test implementation |
| signing         | Basic tests only             | Needs more coverage       |
| fullnode-api    | Step definitions not written | Needs test implementation |

### ➖ Not Available in SDK

| Feature     | Reason          | Tracking Issue |
| ----------- | --------------- | -------------- |
| secp256r1   | Not implemented | -              |
| bls12381    | Not implemented | -              |
| keyless     | Not implemented | -              |
| codegen     | Not implemented | -              |
| simulation  | Not implemented | -              |
| multi-agent | Not implemented | -              |
| fee-payer   | Not implemented | -              |

---

## 4. Known Issues

All implemented tests pass. No known issues.

### SDK-Specific Behaviors

| Behavior           | Description                                              |
| ------------------ | -------------------------------------------------------- |
| Address formatting | `toString()` only shortens "special" addresses (0x0-0xf) |
| Secp256k1 signing  | Uses SHA3-256 hashing internally                         |
| BIP-44 Ed25519     | Hardened path: `m/44'/637'/0'/0'/0'`                     |
| BIP-44 Secp256k1   | Standard path: `m/44'/637'/0'/0/0`                       |

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature                | Scenarios     | Notes                          |
| ---------------------- | ------------- | ------------------------------ |
| entry-function         | All           | Step definitions needed        |
| raw-transaction        | All           | Step definitions needed        |
| signing                | Most advanced | Need transaction signing tests |
| fullnode-api           | All           | Step definitions needed        |
| transaction-submission | All           | Step definitions needed        |
| error-handling         | All           | Step definitions needed        |

### Preferred (P1) - Medium Priority

| Feature        | Scenarios | Notes           |
| -------------- | --------- | --------------- |
| faucet         | All 23    | Not implemented |
| gas-estimation | All 26    | Not implemented |
| view-functions | All 28    | Not implemented |
| retry          | All 31    | Not implemented |

### Optional (P2) - Low Priority

All optional features need step definitions.

---

## 6. SDK-Specific Notes

- **Community SDK** from ALCOVE-LAB, not official aptos-labs
- Swift 6.2+ required
- Requires **Xcode** (not just Command Line Tools) for XCTest
- Uses XCTest for testing (CucumberSwift has SPM issues)
- Strong typing with Swift's type system
- Good for iOS/macOS applications

---

## 7. How to Run Tests

```bash
cd tests/swift

# Run all tests
swift test

# Run with verbose output
swift test --verbose

# Run specific test (if needed)
swift test --filter "AptosSpecsTests"
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add test methods to `Tests/AptosSpecsTests/AptosSpecsTests.swift`
2. Follow the naming pattern `test_<Feature>_<Scenario>()`
3. Run `swift test` to verify tests pass
4. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
5. Update this file's coverage summary
6. Submit PR with test results

---

## 9. Test Results Matrix

> Last run: 2026-01-22

### By Feature Category

| Category          | Tests | Status      |
| ----------------- | ----- | ----------- |
| AccountAddress    | 32    | ✅ All pass |
| Ed25519           | 18    | ✅ All pass |
| Secp256k1         | 18    | ✅ All pass |
| Mnemonic/BIP-44   | 9     | ✅ All pass |
| BCS Serialization | 23    | ✅ All pass |
| TypeTag           | 32    | ✅ All pass |
| Hashing           | 9     | ✅ All pass |
| AuthenticationKey | 8     | ✅ All pass |
| Account           | 22    | ✅ All pass |
| Hex Utilities     | 18    | ✅ All pass |
| Identifier        | 6     | ✅ All pass |
| ModuleId          | 6     | ✅ All pass |
| ChainId           | 9     | ✅ All pass |
| Move Primitives   | 12    | ✅ All pass |
| MoveString        | 5     | ✅ All pass |
| MoveVector        | 6     | ✅ All pass |
| MoveOption        | 12    | ✅ All pass |
| Network Config    | 19    | ✅ All pass |
| AptosConfig       | 6     | ✅ All pass |
| Signatures        | 7     | ✅ All pass |
| PublicKeys        | 9     | ✅ All pass |

### Test Run Summary

```
Total tests: 286
Passed: 286
Failed: 0
```

### Implemented Test Details

#### Address Tests (32)

- Parse hex with/without prefix
- Parse full 64-char hex, uppercase/mixed case
- Reject invalid inputs
- Format to full/short hex
- Standard constants (ZERO, ONE, THREE, FOUR)
- Equality comparisons
- BCS serialize/deserialize/round-trip
- IsSpecial detection

#### Cryptography Tests (36)

- Ed25519: key generation, sign/verify, export, derive auth key
- Secp256k1: key generation, sign/verify, export, uncompressed format

#### Account Tests (22)

- Generate random accounts
- Create from private key
- Sign and verify messages
- Signature schemes (Ed25519, SingleKey)

#### Mnemonic Tests (9)

- Ed25519/Secp256k1 derivation paths
- Account from derivation path
- Reject invalid paths

### Community SDK Notes

This is a community-maintained SDK from ALCOVE-LAB. It may have:

- Different API patterns than official SDKs
- Features that differ from official releases

Check the [aptos-swift-sdk repository](https://github.com/ALCOVE-LAB/aptos-swift-sdk) for updates.
