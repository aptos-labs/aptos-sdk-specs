# Swift SDK Test Status

> **Last Updated:** 2026-02-23  
> **Last Verified:** Not yet verified (SDK integration just completed)

---

## 1. SDK Information

| Property             | Value                                                 |
| -------------------- | ----------------------------------------------------- |
| **Package**          | `AptosSDK`                                            |
| **Version Tested**   | main                                                  |
| **Publisher**        | aptos-labs (official)                                 |
| **Repository**       | https://github.com/aptos-labs/aptos-swift-sdk         |
| **Package Registry** | Swift Package Manager                                 |
| **Test Framework**   | XCTest                                                |

---

## 2. Coverage Summary

| Priority       | Passing | Total | Percentage | Status |
| -------------- | ------- | ----- | ---------- | ------ |
| Required (P0)  | TBD     | TBD   | TBD        | 🔄     |
| Preferred (P1) | TBD     | TBD   | TBD        | 🔄     |
| Optional (P2)  | TBD     | TBD   | TBD        | 🔄     |
| **Total**      | **TBD** | TBD   | TBD        | 🔄     |

> **Notes:**
>
> - SDK integration just completed — test results pending verification
> - Official aptos-labs SDK replaces community ALCOVE-LAB SDK
> - Requires Xcode with Swift 6.0+ and macOS 14+
> - CucumberSwift step definitions prepared for future BDD integration

---

## 3. Feature Availability

### ✅ Available in SDK

| Feature             | Notes                                      |
| ------------------- | ------------------------------------------ |
| address             | AccountAddress with hex parsing/formatting |
| ed25519             | Ed25519PrivateKey, PublicKey, Signature     |
| secp256k1           | Secp256k1PrivateKey, PublicKey, Signature   |
| secp256r1           | Secp256r1PrivateKey, PublicKey (P-256)      |
| hashing             | AptosHashing (SHA3-256, SHA2-256)          |
| serialization       | BCS Serializer/Deserializer                |
| authentication-key  | AuthenticationKey derivation               |
| mnemonic-derivation | Mnemonic, HDKey, BIP-39/BIP-44/SLIP-0010  |
| type-tags           | TypeTag, StructTag parsing                 |
| transactions        | RawTransaction, SignedTransaction           |
| accounts            | Ed25519Account, SingleKeyAccount            |
| keyless             | KeylessAccount, PepperClient, ProverClient |
| multi-key           | MultiKeyAccount, MultiKey                   |
| multi-agent         | MultiAgentUtils                             |
| fee-payer           | FeePayerUtils                               |

### 🟡 Partially Available

| Feature         | Reason                       | Impact                    |
| --------------- | ---------------------------- | ------------------------- |
| entry-function  | Step definitions need update | Needs test verification   |
| raw-transaction | Step definitions need update | Needs test verification   |
| signing         | Step definitions need update | Needs test verification   |

---

## 4. Known Issues

| Scenario         | Issue                                 | Workaround                |
| ---------------- | ------------------------------------- | ------------------------- |
| CucumberSwift    | Upstream compilation bug              | Use XCTest-based tests    |
| Swift 6.0        | Requires latest Xcode                 | Install Xcode 16+        |
| Platform         | macOS 14+ required                    | Update macOS              |

---

## 5. SDK-Specific Notes

- **Official SDK** — Maintained by aptos-labs (Greg Nazario)
- **Swift 6.0** with strict concurrency
- **Actor-based HTTP client** with retry support
- **15 domain APIs**: Account, Transaction, View, Coin, Faucet, DigitalAsset, etc.
- Uses **CTweetNaCl** (embedded C) for deterministic Ed25519 signing
- Uses **CryptoKit** for SHA-256 and P-256 (Secp256r1)
- Uses **secp256k1.swift** (P256K) for Secp256k1
- **AIP-80** private key format support
- Supports iOS 17+, macOS 14+, tvOS 17+, watchOS 10+

---

## 6. How to Run Tests

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

## 7. Contributing

To add or update tests for this SDK:

1. Add test methods to `Tests/AptosSpecsTests/AptosSpecsTests.swift`
2. Follow the naming pattern `test_<Feature>_<Scenario>()`
3. Run `swift test` to verify tests pass
4. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
5. Update this file's coverage summary
6. Submit PR with test results

---

## 8. References

- [Aptos Swift SDK](https://github.com/aptos-labs/aptos-swift-sdk)
- [Feature Specifications](../../features/)
- [Test Vectors](../../test-vectors/)
