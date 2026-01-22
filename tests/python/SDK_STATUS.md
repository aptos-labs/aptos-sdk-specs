# Python SDK Test Status

> **Last Updated:** 2026-01-22  
> **Last Verified:** 2026-01-22 via `behave`

---

## 1. SDK Information

| Property | Value |
|----------|-------|
| **Package** | `aptos-sdk` |
| **Version Tested** | 0.11.0 |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-python-sdk |
| **Package Registry** | PyPI |
| **Test Framework** | Behave (Python BDD) |

---

## 2. Coverage Summary

| Priority | Passing | Total | Percentage | Status |
|----------|---------|-------|------------|--------|
| Required (P0) | 197 | 370 | 53% | 🟡 |
| Preferred (P1) | ~20 | 183 | ~11% | ❌ |
| Optional (P2) | ~10 | 250 | ~4% | ❌ |
| **Total** | **~227** | **803** | **~28%** | 🟡 |

> **Notes:**
> - 332 undefined step definitions
> - 148 scenarios with errors (missing steps)
> - 438 scenarios skipped (network tests or features not available)

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature | Notes |
|---------|-------|
| address | Full address parsing and formatting |
| ed25519 | Complete Ed25519 support via PyNaCl |
| hashing | SHA3-256 support |
| authentication-key | Auth key derivation |

### 🟡 Partially Available

| Feature | Reason | Impact |
|---------|--------|--------|
| serialization | BCS available, some tests not written | Partial coverage |
| type-tags | TypeTag parsing available, tests partial | Partial coverage |
| entry-function | SDK supports, tests in progress | Partial coverage |
| raw-transaction | SDK supports, tests in progress | Partial coverage |
| signing | SDK supports, tests in progress | Partial coverage |

### ➖ Not Available in SDK

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| secp256k1 | Not implemented | - |
| secp256r1 | Not implemented | - |
| bls12381 | Not implemented | - |
| keyless | Not implemented | - |
| codegen | Not implemented | - |

---

## 4. Known Issues

No partial implementations currently tracked. Most issues are undefined steps.

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature | Scenarios | Notes |
|---------|-----------|-------|
| type-tags | #23-24 | Error handling scenarios |
| secp256k1 | All | Feature not in SDK |
| authentication-key | Partial | Some scenarios undefined |
| mnemonic-derivation | All | Tests not written |
| single-key | Most | Tests not written |
| entry-function | Most | Tests in progress |
| raw-transaction | Most | Tests in progress |
| signing | Most | Tests in progress |
| fullnode-api | Most | Tests not written |
| transaction-submission | Most | Tests not written |
| error-handling | Most | Tests not written |

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

- Uses **Python asyncio** for async operations
- **PyNaCl** for Ed25519 cryptography
- Strong typing with type hints
- Python 3.8+ required
- Good for scripting and automation

---

## 7. How to Run Tests

```bash
cd tests/python

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
behave ../../features

# Run by priority
behave ../../features --tags=@required
behave ../../features --tags=@preferred

# Run by category
behave ../../features/01-core-types
behave ../../features/02-cryptography

# Dry run (check step definitions)
behave ../../features --dry-run
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add step definitions in `steps/*.py`
2. Run `behave ../../features` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Submit PR with test results

### Setup Notes

Behave requires symlinks in the features directory:
```bash
cd features
ln -sf ../tests/python/steps steps
ln -sf ../tests/python/environment.py environment.py
ln -sf ../tests/python/support support
```

---

## 9. Test Results Matrix

> Last run: 2026-01-22

### By Feature Category

| Category | Passed | Failed | Error | Skipped | Total |
|----------|--------|--------|-------|---------|-------|
| 01-core-types | 60 | 2 | 10 | 0 | 72 |
| 02-cryptography | 45 | 5 | 30 | 40 | 120 |
| 03-account-management | 25 | 3 | 20 | 14 | 62 |
| 04-transaction-building | 30 | 5 | 25 | 26 | 86 |
| 05-api-clients | 20 | 5 | 30 | 85 | 140 |
| 06-advanced | 17 | 5 | 33 | 273 | 328 |

### Test Run Summary

```
1 feature passed, 4 failed, 8 error, 16 skipped
197 scenarios passed, 25 failed, 148 error, 438 skipped
918 steps passed, 25 failed, 59 error, 1742 skipped, 332 undefined
```

### Well-Implemented Areas

- Address parsing and formatting
- Basic Ed25519 cryptography
- BCS serialization primitives
- Basic account operations

### Needs Work

- TypeTag parsing step definitions
- Entry function building steps
- Transaction signing steps
- API client steps
