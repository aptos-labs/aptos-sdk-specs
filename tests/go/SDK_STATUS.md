# Go SDK Test Status

> **Last Updated:** 2026-02-06  
> **Last Verified:** 2026-02-06 via `go test -v ./...`

---

## 1. SDK Information

| Property             | Value                                      |
| -------------------- | ------------------------------------------ |
| **Package (v1)**     | `github.com/aptos-labs/aptos-go-sdk`       |
| **Package (v2)**     | `github.com/aptos-labs/aptos-go-sdk/v2`    |
| **Version Tested**   | v1.11.0 (v2 migration pending)             |
| **Publisher**        | aptos-labs                                 |
| **Repository**       | https://github.com/aptos-labs/aptos-go-sdk |
| **Package Registry** | Go modules                                 |
| **Test Framework**   | Godog (Cucumber for Go)                    |

> **Note:** Go SDK v2 (`2.0.0-alpha`) is a complete API rewrite with context-first methods, improved
> error handling, and new features (keyless, sponsored tx, codegen, ANS). Migration from v1 is
> tracked. See the
> [v2 migration guide](https://github.com/aptos-labs/aptos-go-sdk/blob/main/v2/MIGRATION.md).

---

## 2. Coverage Summary

| Priority       | Passing  | Total   | Percentage | Status |
| -------------- | -------- | ------- | ---------- | ------ |
| Required (P0)  | 333      | 791     | 42%        | 🟡     |
| Preferred (P1) | included | -       | -          | -      |
| Optional (P2)  | included | -       | -          | -      |
| **Total**      | **333**  | **791** | **42%**    | 🟡     |

> **Notes:**
>
> - 333 scenarios passed, 136 failed, 312 pending, 10 undefined
> - 1897 steps passed, 136 failed, 312 pending, 11 undefined, 702 skipped
> - Test duration: ~36 seconds

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature                | Notes                                            |
| ---------------------- | ------------------------------------------------ |
| address                | Full address parsing and formatting              |
| serialization          | BCS via `bcs` package                            |
| type-tags              | TypeTag parsing and serialization                |
| ed25519                | Complete Ed25519 support                         |
| secp256k1              | Full Secp256k1 support via `crypto` package      |
| hashing                | SHA2-256, SHA3-256, domain separation, HashValue |
| authentication-key     | Ed25519 and Secp256k1 auth keys                  |
| entry-function         | Entry function building with type args           |
| raw-transaction        | Transaction building                             |
| signing                | Ed25519 and Secp256k1 transaction signing        |
| fullnode-api           | Full API client with testnet/devnet support      |
| transaction-submission | Submit transactions and wait for completion      |
| multi-agent            | Multi-agent transaction support                  |
| fee-payer              | Fee payer (sponsored) transaction support        |
| faucet                 | Testnet/devnet faucet integration                |
| gas-estimation         | Gas estimation via simulation                    |
| view-functions         | View function calls                              |

### 🟡 Partially Available

| Feature         | Notes                                |
| --------------- | ------------------------------------ |
| multi-signature | MultiEd25519 partial support         |
| retry           | Retry logic (SDK handles internally) |
| simulation      | Transaction simulation via API       |

### ➖ Not Available in SDK (Tests marked as Pending)

| Feature             | Reason                             | Status  |
| ------------------- | ---------------------------------- | ------- |
| secp256r1           | P-256/WebAuthn not implemented     | Pending |
| keyless             | JWT/OIDC authentication not in SDK | Pending |
| ephemeral-keys      | Keyless dependency                 | Pending |
| pepper-service      | Keyless infrastructure             | Pending |
| mnemonic-derivation | HD derivation not exposed          | Pending |
| AIP-80 key format   | Not implemented                    | Pending |
| codegen             | Code generation not available      | Pending |

---

## 4. Known Issues

Issues with tests marked 🟡 (partial):

| Scenario                | Issue                                                                            | Workaround          |
| ----------------------- | -------------------------------------------------------------------------------- | ------------------- |
| entry-function #12      | `CoinTransferPayload` uses `aptos_account::transfer` instead of `coin::transfer` | SDK design decision |
| authentication-key #5-8 | Secp256r1/MultiEd25519/MultiKey keys not supported                               | Feature not in SDK  |

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature                | Scenarios                   | Notes                                |
| ---------------------- | --------------------------- | ------------------------------------ |
| ed25519                | #24-25                      | Private key zeroization/debug hiding |
| authentication-key     | #5-8, #15                   | Secp256k1-related                    |
| single-key             | #6-7, #15-20, #22, #26-28   | AIP-80, Secp256k1                    |
| entry-function         | #20-21                      | Optional arguments                   |
| raw-transaction        | #15-16, #19                 | Expiration helpers                   |
| signing                | #15-18, #23-24              | Secp256k1 signing                    |
| fullnode-api           | #2-3, #14, #21-22, #25      | Various API features                 |
| transaction-submission | #7, #9, #12, #15-21, #25-27 | Simulation, waiting                  |
| error-handling         | Most scenarios              | Error handling patterns              |

### Preferred (P1) - Medium Priority

| Feature        | Scenarios | Notes           |
| -------------- | --------- | --------------- |
| faucet         | All 23    | Not implemented |
| gas-estimation | All 26    | Not implemented |
| view-functions | All 28    | Not implemented |
| retry          | All 31    | Not implemented |

### Optional (P2) - Low Priority

All optional features are not available in SDK.

---

## 6. Performance Benchmarks

> **Last Updated:** 2026-01-23  
> **Network:** Devnet  
> **Hardware:** Apple Silicon (arm64)  
> **Runtime:** Go 1.24

### REST API Read Performance ✅

| Metric                  | Value   | Unit |
| ----------------------- | ------- | ---- |
| Ledger Info (avg)       | **59**  | ms   |
| Ledger Info (p95)       | 63      | ms   |
| Account Info (avg)      | **62**  | ms   |
| Account Info (p95)      | 70      | ms   |
| Account Resources (avg) | **169** | ms   |
| Account Resources (p95) | 214     | ms   |
| Account Balance (avg)   | **66**  | ms   |
| Account Balance (p95)   | 72      | ms   |

### GraphQL/Indexer Read Performance

| Metric                     | Value | Unit |
| -------------------------- | ----- | ---- |
| Account Tokens (avg)       | -     | ms   |
| Account Transactions (avg) | -     | ms   |
| Fungible Assets (avg)      | -     | ms   |
| Events (avg)               | -     | ms   |

### Transaction Performance

| Metric               | Value | Unit |
| -------------------- | ----- | ---- |
| Build + Sign (avg)   | -     | ms   |
| Submit no wait (avg) | -     | ms   |
| Submit no wait (p95) | -     | ms   |
| Round-trip (avg)     | -     | ms   |
| Round-trip (p95)     | -     | ms   |
| Round-trip (min)     | -     | ms   |
| Round-trip (max)     | -     | ms   |
| Full Flow (avg)      | -     | ms   |

### Cryptographic Operations ✅

| Metric                        | Value          | Unit |
| ----------------------------- | -------------- | ---- |
| Ed25519 Key Gen (avg)         | **10.8**       | μs   |
| Ed25519 Key Gen (ops/s)       | **92,353**     | ops  |
| Ed25519 Sign (avg)            | **13.2**       | μs   |
| Ed25519 Sign (ops/s)          | **75,517**     | ops  |
| Ed25519 Verify (avg)          | **35.6**       | μs   |
| Ed25519 Verify (ops/s)        | **28,108**     | ops  |
| BCS Serialize Address (avg)   | **0.014**      | μs   |
| BCS Serialize Address (ops/s) | **71,546,111** | ops  |
| SHA3-256 (avg)                | **0.54**       | μs   |
| SHA3-256 (ops/s)              | **1,837,384**  | ops  |

### Run Performance Tests

```bash
cd tests/go
make test-performance

# Or run only crypto benchmarks
GODOG_TAGS="@crypto" go test -v ./...
```

---

## 7. SDK-Specific Notes

- Focuses on **core transaction building and submission**
- Uses Go idioms (error returns, no exceptions)
- BCS serialization happens internally, not exposed for general use
- Limited advanced feature support compared to TypeScript SDK
- Good for simple transaction workflows

---

## 8. How to Run Tests

```bash
cd tests/go
go mod download

# Run all tests
make test

# Run by priority
make test-required          # Only @required tests
make test-preferred         # Only @preferred tests

# Run by category
make test-core-types        # @core-types tests
make test-cryptography      # @cryptography tests

# Verbose output
go test -v ./...
```

---

## 9. Contributing

To add or update tests for this SDK:

1. Add step definitions in `*_steps.go` files
2. Run `make test` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Document any SDK limitations in TO_FIX.md
6. Submit PR with test results

---

## 10. Test Results Matrix

> Last run: 2026-02-06

### Full Test Suite Summary

```
791 scenarios (333 passed, 136 failed, 312 pending, 10 undefined)
3058 steps (1897 passed, 136 failed, 312 pending, 11 undefined, 702 skipped)
Duration: ~36s
```

### Pending Features (Awaiting SDK Implementation)

| Feature   | Scenarios | Reason                           |
| --------- | --------- | -------------------------------- |
| Secp256r1 | ~10       | P-256 curve not in SDK           |
| Keyless   | ~33       | JWT/OIDC infrastructure required |
| Codegen   | ~34       | Code generation not available    |
| Mnemonic  | ~29       | HD derivation not exposed        |

### Failure Details

| Failure Type      | Count | Examples                                  |
| ----------------- | ----- | ----------------------------------------- |
| SDK Limitations   | ~40   | Secp256r1, MultiKey, specific API methods |
| Network-dependent | ~50   | Testnet/devnet connection required        |
| Pending steps     | ~312  | Step definitions return ErrPending        |
| Test Setup        | ~6    | Missing test fixtures or state            |
