# Kotlin SDK Test Status

> **Last Updated:** 2026-02-23  
> **Last Verified:** Not yet verified (SDK integration just completed)

---

## 1. SDK Information

| Property             | Value                                          |
| -------------------- | ---------------------------------------------- |
| **Package**          | `com.aptos:core`                               |
| **Version Tested**   | 0.1.0                                          |
| **Publisher**        | aptos-labs (official)                          |
| **Repository**       | https://github.com/aptos-labs/aptos-kotlin-sdk |
| **Package Registry** | Maven Central / Maven Local                    |
| **Test Framework**   | Cucumber-JVM + Kotlin                          |

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
> - Official aptos-labs SDK replaces community kaptos SDK
> - Step definitions updated to use new SDK API

---

## 3. Feature Availability

### ✅ Available in SDK

| Feature             | Notes                                      |
| ------------------- | ------------------------------------------ |
| address             | AccountAddress.fromHex/fromHexRelaxed      |
| ed25519             | Ed25519.PrivateKey, PublicKey, Signature   |
| secp256k1           | Secp256k1.PrivateKey, PublicKey, Signature |
| hashing             | SHA3-256, SHA2-256 via JVM/BouncyCastle    |
| serialization       | BcsSerializer, BcsDeserializer             |
| authentication-key  | AuthenticationKey.fromEd25519/Secp256k1    |
| mnemonic-derivation | Mnemonic, SLIP-0010, BIP-32                |
| type-tags           | TypeTag parsing and formatting             |
| transactions        | RawTransaction, SignedTransaction          |
| accounts            | Ed25519Account, Secp256k1Account           |
| keyless             | KeylessAccount (via SDK)                   |
| multi-key           | MultiKey, MultiEd25519                     |

### 🟡 Partially Available

| Feature         | Reason                       | Impact                  |
| --------------- | ---------------------------- | ----------------------- |
| entry-function  | Step definitions need update | Needs test verification |
| raw-transaction | Step definitions need update | Needs test verification |
| signing         | Step definitions need update | Needs test verification |

### ➖ Not Yet Tested

| Feature                | Reason                  | Tracking Issue |
| ---------------------- | ----------------------- | -------------- |
| fullnode-api           | Needs network access    | -              |
| transaction-submission | Needs network access    | -              |
| simulation             | Step definitions needed | -              |
| multi-agent            | Step definitions needed | -              |
| fee-payer              | Step definitions needed | -              |

---

## 4. Known Issues

| Scenario       | Issue                           | Workaround       |
| -------------- | ------------------------------- | ---------------- |
| SDK publishing | SDK may not be on Maven Central | Use mavenLocal() |
| Test run       | Not yet verified in CI          | Run locally      |

---

## 5. SDK-Specific Notes

- **Official SDK** — Maintained by aptos-labs
- **JVM-focused** with Android support (API 26+)
- **Modular architecture**: core, client, sdk, indexer modules
- **Kotlin 2.1.10** with JVM target 11
- Uses **Bouncy Castle** for cryptographic operations
- Uses **kotlinx.serialization** for JSON parsing
- Full **BCS serialization** support
- **Ed25519 and Secp256k1** key generation, signing, verification
- **BIP-39 mnemonic** and **SLIP-0010/BIP-32** key derivation

---

## 6. How to Run Tests

```bash
cd tests/kotlin

# Run all tests
./gradlew test

# Run with info output
./gradlew test --info

# Run only required (P0) tests
./gradlew testRequired

# Generate HTML report
./gradlew test
# Report at: build/reports/cucumber/cucumber.html
```

---

## 7. Contributing

To add or update tests for this SDK:

1. Add step definitions in `src/test/kotlin/com/aptos/specs/steps/*.kt`
2. Run `./gradlew test` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Submit PR with test results

### Step Definition Pattern (Kotlin)

```kotlin
@Given("a hex string {string}")
fun givenAHexString(hexString: String) {
    world.hexString = hexString
}
```

---

## 8. References

- [Aptos Kotlin SDK](https://github.com/aptos-labs/aptos-kotlin-sdk)
- [Cucumber-JVM Documentation](https://cucumber.io/docs/cucumber/)
- [Kotest Assertions](https://kotest.io/docs/assertions/assertions.html)
- [Feature Specifications](../../features/)
- [Test Vectors](../../test-vectors/)
