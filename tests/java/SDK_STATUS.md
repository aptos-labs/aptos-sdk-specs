# Java SDK Test Status

> **Last Updated:** 2026-01-28  
> **Last Verified:** 2026-01-28 via `mvn test`

---

## 1. SDK Information

| Property             | Value                                        |
| -------------------- | -------------------------------------------- |
| **Package**          | `io.github.aptos-labs:japtos`                |
| **Version Tested**   | 1.1.8                                        |
| **Publisher**        | aptos-labs                                   |
| **Repository**       | https://github.com/aptos-labs/aptos-java-sdk |
| **Package Registry** | Maven Central                                |
| **Test Framework**   | Cucumber-JVM + JUnit 5                       |

---

## 2. Coverage Summary

| Priority       | Passing | Total   | Percentage | Status |
| -------------- | ------- | ------- | ---------- | ------ |
| Required (P0)  | ~22     | 837     | ~3%        | ❌     |
| Preferred (P1) | included| -       | -          | -      |
| Optional (P2)  | included| -       | -          | -      |
| **Total**      | **~22** | **837** | **~3%**    | ❌     |

> **Notes:**
>
> - Tests run: 837, Errors: 815, Failures: 0
> - Most step definitions are undefined
> - Only address parsing and basic Ed25519 implemented
> - Test duration: ~15 seconds

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature | Notes                                |
| ------- | ------------------------------------ |
| address | Full address parsing and formatting  |
| ed25519 | Key generation (signing in progress) |

### 🟡 Partially Available

| Feature            | Reason                              | Impact                |
| ------------------ | ----------------------------------- | --------------------- |
| serialization      | BCS available but tests not written | Need step definitions |
| authentication-key | SDK supports but tests not written  | Need step definitions |
| entry-function     | SDK supports but tests not written  | Need step definitions |

### ➖ Not Available in SDK

| Feature             | Reason          | Tracking Issue |
| ------------------- | --------------- | -------------- |
| secp256k1           | Not implemented | -              |
| secp256r1           | Not implemented | -              |
| bls12381            | Not implemented | -              |
| mnemonic-derivation | Not implemented | -              |
| keyless             | Not implemented | -              |
| codegen             | Not implemented | -              |

---

## 4. Known Issues

No partial implementations currently tracked. Most tests fail due to undefined steps.

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature                | Scenarios     | Notes                                |
| ---------------------- | ------------- | ------------------------------------ |
| address                | #6-10, #19-22 | Error handling, BCS serialization    |
| serialization          | All 18        | Need step definitions                |
| type-tags              | All 24        | Need step definitions                |
| ed25519                | #2-25         | Signing, verification, deterministic |
| secp256k1              | All           | Feature not in SDK                   |
| hashing                | All 20        | Need step definitions                |
| authentication-key     | All 15        | Need step definitions                |
| mnemonic-derivation    | All           | Feature not in SDK                   |
| single-key             | All           | Need step definitions                |
| entry-function         | All           | Need step definitions                |
| raw-transaction        | All           | Need step definitions                |
| signing                | All           | Need step definitions                |
| fullnode-api           | All           | Need step definitions                |
| transaction-submission | All           | Need step definitions                |
| error-handling         | All           | Need step definitions                |

### Preferred (P1) - Medium Priority

All preferred features need step definitions.

### Optional (P2) - Low Priority

All optional features need step definitions.

---

## 6. SDK-Specific Notes

- **Package Structure:**
  - `com.aptoslabs.japtos.core.AccountAddress` - Account addresses
  - `com.aptoslabs.japtos.core.AuthenticationKey` - Auth key derivation
  - `com.aptoslabs.japtos.core.crypto.*` - Ed25519 keys and signatures
  - `com.aptoslabs.japtos.account.Ed25519Account` - Account abstraction
  - `com.aptoslabs.japtos.bcs.*` - BCS serialization
  - `com.aptoslabs.japtos.utils.*` - Hex utilities

- **API Differences from TypeScript:**
  - `AccountAddress.fromHex()` requires full 64-character hex strings
  - `toHexString()` returns hex without "0x" prefix
  - Short addresses like "0x1" need padding before parsing

---

## 7. How to Run Tests

```bash
cd tests/java
mvn test

# Run by priority
mvn test -Dcucumber.filter.tags="@required"
mvn test -Dcucumber.filter.tags="@preferred"

# Run by category
mvn test -Dcucumber.filter.tags="@core-types"
mvn test -Dcucumber.filter.tags="@cryptography"

# Run specific feature
mvn test -Dcucumber.filter.tags="@core-types and @required"
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add step definitions in `src/test/java/com/aptos/specs/steps/AllSteps.java`
2. Run `mvn test` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Submit PR with test results

### Priority Implementation Order

1. Complete address error handling and BCS
2. Add TypeTag parsing steps
3. Add BCS serialization primitive steps
4. Implement Ed25519 signing/verification steps
5. Add account management steps
6. Add transaction building steps

---

## 9. Test Results Matrix

> Last run: 2026-01-27

### By Feature Category

| Category                | Passed | Errors | Skipped | Total |
| ----------------------- | ------ | ------ | ------- | ----- |
| 01-core-types           | ~11    | ~30    | ~23     | 64    |
| 02-cryptography         | ~11    | ~60    | ~49     | 120   |
| 03-account-management   | 0      | ~30    | ~32     | 62    |
| 04-transaction-building | 0      | ~40    | ~46     | 86    |
| 05-api-clients          | 0      | ~70    | ~70     | 140   |
| 06-advanced             | 0      | ~129   | ~147    | 276   |

### Test Run Summary

```
Tests run: 837
Errors: 359 (undefined steps)
Skipped: 456
Passed: ~22
```

### Passing Tests Detail

| Test                                      | Feature         |
| ----------------------------------------- | --------------- |
| Parse hex address without 0x prefix       | address.feature |
| Parse full 64-character hex address       | address.feature |
| Parse uppercase hex address               | address.feature |
| Parse mixed case hex address              | address.feature |
| Parse various valid formats (6 scenarios) | address.feature |
| Generate random Ed25519 key pair          | ed25519.feature |
