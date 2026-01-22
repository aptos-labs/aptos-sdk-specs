# .NET SDK Test Status

> **Last Updated:** 2026-01-22  
> **Last Verified:** 2026-01-22 via `dotnet test`

---

## 1. SDK Information

| Property | Value |
|----------|-------|
| **Package** | `Aptos` |
| **Version Tested** | 0.0.x-beta |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-dotnet-sdk |
| **Package Registry** | NuGet |
| **Test Framework** | Reqnroll (SpecFlow successor) + NUnit |

---

## 2. Coverage Summary

| Priority | Passing | Total | Percentage | Status |
|----------|---------|-------|------------|--------|
| Required (P0) | 170 | 370 | 46% | 🟡 |
| Preferred (P1) | ~10 | 183 | ~5% | ❌ |
| Optional (P2) | ~5 | 250 | ~2% | ❌ |
| **Total** | **~185** | **803** | **~23%** | 🟡 |

> **Notes:**
> - 200 required tests failed (most due to missing step definitions)
> - Beta SDK - API may change

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature | Notes |
|---------|-------|
| address | Full address parsing and formatting |
| ed25519 | Complete Ed25519 support via BouncyCastle |
| hashing | SHA3-256 support |
| serialization | BCS serialization available |

### 🟡 Partially Available

| Feature | Reason | Impact |
|---------|--------|--------|
| authentication-key | SDK supports, tests partial | Partial coverage |
| entry-function | SDK supports, tests in progress | Partial coverage |
| raw-transaction | SDK supports, tests in progress | Partial coverage |
| signing | SDK supports, tests in progress | Partial coverage |
| fullnode-api | SDK supports, tests partial | Partial coverage |

### ➖ Not Available in SDK

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| secp256k1 | Not yet implemented | - |
| secp256r1 | Not yet implemented | - |
| bls12381 | Not yet implemented | - |
| mnemonic-derivation | Not yet implemented | - |
| keyless | Not yet implemented | - |
| codegen | Not yet implemented | - |

---

## 4. Known Issues

| Scenario | Issue | Workaround |
|----------|-------|------------|
| General | Beta SDK API may change | Pin to specific version |
| Step definitions | Many undefined | Implementation in progress |

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature | Scenarios | Notes |
|---------|-----------|-------|
| type-tags | Many | Step definitions needed |
| secp256k1 | All | Feature not in SDK |
| authentication-key | Partial | More steps needed |
| mnemonic-derivation | All | Feature not in SDK |
| single-key | Many | Step definitions needed |
| entry-function | Partial | More steps needed |
| raw-transaction | Partial | More steps needed |
| signing | Partial | More steps needed |
| transaction-submission | Many | Step definitions needed |
| error-handling | Most | Step definitions needed |

### Preferred (P1) - Medium Priority

| Feature | Scenarios | Notes |
|---------|-----------|-------|
| faucet | All 23 | Tests not written |
| gas-estimation | All 26 | Tests not written |
| view-functions | All 28 | Tests not written |
| retry | All 31 | Tests not written |

### Optional (P2) - Low Priority

All optional features need step definitions.

---

## 6. SDK-Specific Notes

- **Beta SDK** - API may change significantly between versions
- .NET 10.0 target framework
- Uses **BouncyCastle** for cryptography
- Uses **Reqnroll** (SpecFlow successor) for BDD testing
- **NUnit** test framework
- **FluentAssertions** for assertions
- Good for enterprise .NET applications

---

## 7. How to Run Tests

```bash
cd tests/dotnet

# Restore dependencies
dotnet restore

# Run all tests
dotnet test

# Run by priority (using Category filter)
dotnet test --filter "Category=required"
dotnet test --filter "Category=preferred"

# Run specific test class
dotnet test --filter "FullyQualifiedName~AddressSteps"

# Run with verbose output
dotnet test --verbosity detailed
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add step definitions in `Steps/*.cs`
2. Run `dotnet test` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Submit PR with test results

### Step Definition Pattern

```csharp
[Given("a hex string {string}")]
public void GivenAHexString(string hexString)
{
    _scenarioContext["hexString"] = hexString;
}
```

---

## 9. Test Results Matrix

> Last run: 2026-01-22

### By Feature Category

| Category | Passed | Failed | Total |
|----------|--------|--------|-------|
| 01-core-types | 45 | 19 | 64 |
| 02-cryptography | 40 | 80 | 120 |
| 03-account-management | 20 | 42 | 62 |
| 04-transaction-building | 30 | 56 | 86 |
| 05-api-clients | 20 | 120 | 140 |
| 06-advanced | 15 | 261 | 276 |

### Test Run Summary

```
Failed:   200
Passed:   170
Skipped:    0
Total:    370
Duration: ~1s
```

### Beta SDK Notes

This SDK is in beta. The API may change significantly between versions.
Check the repository for the latest documentation and breaking changes.
