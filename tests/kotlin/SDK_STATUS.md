# Kotlin SDK Test Status

> **Last Updated:** 2026-02-06  
> **Last Verified:** 2026-01-28 via `./gradlew test` (cannot run 2026-02-06: Gradle/JDK compat issue)

---

## 1. SDK Information

| Property             | Value                             |
| -------------------- | --------------------------------- |
| **Package**          | `xyz.mcxross.kaptos:kaptos-jvm`   |
| **Version Tested**   | 0.1.2-beta                        |
| **Publisher**        | mcxross (community)               |
| **Repository**       | https://github.com/mcxross/kaptos |
| **Package Registry** | Maven Central                     |
| **Test Framework**   | Cucumber-JVM + Kotlin             |

---

## 2. Coverage Summary

| Priority       | Passing  | Total    | Percentage | Status |
| -------------- | -------- | -------- | ---------- | ------ |
| Required (P0)  | 176      | 1652     | 11%        | ❌     |
| Preferred (P1) | included | -        | -          | -      |
| Optional (P2)  | included | -        | -          | -      |
| **Total**      | **176**  | **1652** | **11%**    | ❌     |

> **Notes:**
>
> - 1652 tests completed, 176 passed, 1476 failed
> - Community SDK, not official aptos-labs
> - Many failures due to undefined step definitions
> - Test duration: ~28 seconds

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature       | Notes                               |
| ------------- | ----------------------------------- |
| address       | Full address parsing and formatting |
| ed25519       | Ed25519 key support                 |
| hashing       | Basic hashing support               |
| serialization | BCS serialization                   |

### 🟡 Partially Available

| Feature            | Reason                   | Impact           |
| ------------------ | ------------------------ | ---------------- |
| authentication-key | Available, tests partial | Partial coverage |
| entry-function     | Available, tests partial | Partial coverage |
| raw-transaction    | Available, tests partial | Partial coverage |
| signing            | Available, tests partial | Partial coverage |

### ➖ Not Available in SDK

| Feature             | Reason          | Tracking Issue |
| ------------------- | --------------- | -------------- |
| secp256k1           | Not implemented | -              |
| secp256r1           | Not implemented | -              |
| bls12381            | Not implemented | -              |
| mnemonic-derivation | Not implemented | -              |
| keyless             | Not implemented | -              |
| codegen             | Not implemented | -              |
| simulation          | Not implemented | -              |
| multi-agent         | Not implemented | -              |
| fee-payer           | Not implemented | -              |

---

## 4. Known Issues

| Scenario      | Issue                        | Workaround            |
| ------------- | ---------------------------- | --------------------- |
| Most tests    | Step definitions undefined   | Implementation needed |
| Community SDK | May lag behind official SDKs | Check for updates     |

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature                | Scenarios | Notes                   |
| ---------------------- | --------- | ----------------------- |
| type-tags              | Many      | Step definitions needed |
| secp256k1              | All       | Feature not in SDK      |
| authentication-key     | Partial   | More steps needed       |
| mnemonic-derivation    | All       | Feature not in SDK      |
| single-key             | Many      | Step definitions needed |
| entry-function         | Partial   | More steps needed       |
| raw-transaction        | Partial   | More steps needed       |
| signing                | Partial   | More steps needed       |
| fullnode-api           | Many      | Step definitions needed |
| transaction-submission | Many      | Step definitions needed |
| error-handling         | Most      | Step definitions needed |

### Preferred (P1) - Medium Priority

All preferred features need step definitions.

### Optional (P2) - Low Priority

All optional features need step definitions.

---

## 6. SDK-Specific Notes

- **Community SDK** - Maintained by mcxross, not official aptos-labs
- **Kotlin Multiplatform** support (JVM, JS, Native)
- Uses Kotlin coroutines for async operations
- Good for Android and cross-platform Kotlin projects
- May have different API than official SDKs

---

## 7. How to Run Tests

```bash
cd tests/kotlin

# Run all tests
./gradlew test

# Run with info output
./gradlew test --info

# Run specific test
./gradlew test --tests "*.AddressTest"

# Generate HTML report
./gradlew test
# Report at: build/reports/tests/test/index.html
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add step definitions in `src/test/kotlin/steps/*.kt`
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

## 9. Test Results Matrix

> Last run: 2026-01-22

### By Feature Category

| Category                | Passed | Failed | Total |
| ----------------------- | ------ | ------ | ----- |
| 01-core-types           | 50     | 14     | 64    |
| 02-cryptography         | 45     | 75     | 120   |
| 03-account-management   | 20     | 42     | 62    |
| 04-transaction-building | 25     | 61     | 86    |
| 05-api-clients          | 20     | 120    | 140   |
| 06-advanced             | 16     | 260    | 276   |

### Test Run Summary

```
1616 tests completed
176 passed
1440 failed
```

### Community SDK Notes

This is a community-maintained SDK. It may have:

- Different API patterns than official SDKs
- Features that lag behind official releases
- Limited documentation

Check the [kaptos repository](https://github.com/mcxross/kaptos) for the latest updates.
