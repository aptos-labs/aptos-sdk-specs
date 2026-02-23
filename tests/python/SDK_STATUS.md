# Python SDK Test Status

> **Last Updated:** 2026-02-23  
> **Last Verified:** 2026-02-23 via `behave` (full test suite)

---

## 1. SDK Information

| Property             | Value                                          |
| -------------------- | ---------------------------------------------- |
| **Package**          | `aptos-sdk`                                    |
| **Version Tested**   | >=0.11.0                                       |
| **Publisher**        | aptos-labs                                     |
| **Repository**       | https://github.com/aptos-labs/aptos-python-sdk |
| **Package Registry** | PyPI                                           |
| **Test Framework**   | Behave (Python BDD)                            |

---

## 2. Coverage Summary

| Priority       | Passing  | Total   | Percentage | Status |
| -------------- | -------- | ------- | ---------- | ------ |
| Required (P0)  | 459      | 791     | 58%        | 🟡     |
| Preferred (P1) | included | -       | -          | -      |
| Optional (P2)  | included | -       | -          | -      |
| **Total**      | **459**  | **791** | **58%**    | 🟡     |

> **Notes:**
>
> - 459 passed, 121 failed, 75 errors, 136 skipped
> - 2258 steps passed, 121 failed, 74 errors, 604 skipped, 1 undefined
> - Test duration: ~1.2 seconds
> - Significant improvement from previous run (272 -> 459 passing)

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature            | Notes                               |
| ------------------ | ----------------------------------- |
| address            | Full address parsing and formatting |
| ed25519            | Complete Ed25519 support via PyNaCl |
| hashing            | SHA3-256 support                    |
| authentication-key | Auth key derivation                 |

### 🟡 Partially Available

| Feature         | Reason                                   | Impact           |
| --------------- | ---------------------------------------- | ---------------- |
| serialization   | BCS available, some tests not written    | Partial coverage |
| type-tags       | TypeTag parsing available, tests partial | Partial coverage |
| entry-function  | SDK supports, tests in progress          | Partial coverage |
| raw-transaction | SDK supports, tests in progress          | Partial coverage |
| signing         | SDK supports, tests in progress          | Partial coverage |

### ➖ Not Available in SDK

| Feature   | Reason          | Tracking Issue |
| --------- | --------------- | -------------- |
| secp256k1 | Not implemented | -              |
| secp256r1 | Not implemented | -              |
| keyless   | Not implemented | -              |
| codegen   | Not implemented | -              |

---

## 4. Known Issues

No partial implementations currently tracked. Most issues are undefined steps.

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature                | Scenarios | Notes                    |
| ---------------------- | --------- | ------------------------ |
| type-tags              | #23-24    | Error handling scenarios |
| secp256k1              | All       | Feature not in SDK       |
| authentication-key     | Partial   | Some scenarios undefined |
| mnemonic-derivation    | All       | Tests not written        |
| single-key             | Most      | Tests not written        |
| entry-function         | Most      | Tests in progress        |
| raw-transaction        | Most      | Tests in progress        |
| signing                | Most      | Tests in progress        |
| fullnode-api           | Most      | Tests not written        |
| transaction-submission | Most      | Tests not written        |
| error-handling         | Most      | Tests not written        |

### Preferred (P1) - Medium Priority

| Feature        | Scenarios | Notes             |
| -------------- | --------- | ----------------- |
| faucet         | All 23    | Tests not written |
| gas-estimation | All 26    | Tests not written |
| view-functions | All 28    | Tests not written |
| retry          | All 31    | Tests not written |

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

> Last run: 2026-02-06

### By Feature Category

| Category                | Passed | Failed | Error | Skipped | Total |
| ----------------------- | ------ | ------ | ----- | ------- | ----- |
| 01-core-types           | 112    | 0      | 9     | 0       | 121   |
| 02-cryptography         | 50     | 2      | 7     | 33      | 92    |
| 03-account-management   | 24     | 8      | 17    | 35      | 84    |
| 04-transaction-building | 62     | 16     | 16    | 14      | 108   |
| 05-api-clients          | 122    | 66     | 2     | 3       | 193   |
| 06-advanced             | 89     | 29     | 8     | 63      | 189   |

### Test Run Summary

```
6 features passed, 14 failed, 6 error, 3 skipped
459 scenarios passed, 121 failed, 75 error, 136 skipped
2258 steps passed, 121 failed, 74 error, 604 skipped, 1 undefined
Duration: ~1.2s
```

### Well-Implemented Areas

- Address parsing and formatting (22/22)
- Ed25519 cryptography (25/25)
- Hashing (19/20)
- Error handling (30/30)
- API client basics (many passing)
- Simulation basics
- Multi-agent / fee-payer basics

### Needs Work

- Secp256k1 key operations (errors in key-from-bytes)
- Account management (scheme identifiers, AIP-80)
- Entry function BCS serialization edge cases
- Multi-sig validation assertions
- Keyless (not supported in SDK)
- Code generation (not supported in SDK)
