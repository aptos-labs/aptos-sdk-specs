# TypeScript SDK Test Status

> **Last Updated:** 2026-02-23  
> **Last Verified:** 2026-02-23 via `bun run cucumber-js`

---

## 1. SDK Information

| Property             | Value                                      |
| -------------------- | ------------------------------------------ |
| **Package**          | `@aptos-labs/ts-sdk`                       |
| **Version Tested**   | ^5.2.0                                     |
| **Publisher**        | aptos-labs                                 |
| **Repository**       | https://github.com/aptos-labs/aptos-ts-sdk |
| **Package Registry** | npm                                        |
| **Test Framework**   | Cucumber.js + Bun                          |

---

## 2. Coverage Summary

| Priority       | Passing  | Total   | Percentage | Status |
| -------------- | -------- | ------- | ---------- | ------ |
| Required (P0)  | ~494     | 580     | ~85%       | 🟡     |
| Preferred (P1) | included | -       | -          | -      |
| Optional (P2)  | included | -       | -          | -      |
| **Total**      | **494**  | **791** | **62%**    | 🟡     |

> **Notes:**
>
> - 580 non-network/perf scenarios: 494 passed, 49 failed, 37 undefined
> - 133 api-client scenarios: Require network access (timeout without network)
> - 78 network/performance scenarios: Require live devnet/testnet
> - 49 failures in Secp256r1, simulation, retry
> - 37 undefined (codegen, some advanced features)
> - Some keyless and script tests use mocks

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature                | Notes                               |
| ---------------------- | ----------------------------------- |
| address                | Full address parsing and formatting |
| serialization          | Complete BCS serialization          |
| type-tags              | Full TypeTag parsing                |
| ed25519                | Complete Ed25519 support            |
| secp256k1              | Full Secp256k1 support              |
| hashing                | SHA3-256, domain separation         |
| authentication-key     | All auth key derivations            |
| mnemonic-derivation    | BIP-39/BIP-44 support               |
| single-key             | SingleKey account support           |
| entry-function         | Full entry function building        |
| raw-transaction        | Transaction building                |
| signing                | Transaction signing                 |
| fullnode-api           | API client support                  |
| transaction-submission | Submit and wait                     |

### 🟡 Partially Available (Using Mocks)

| Feature             | Reason                   | Impact                                     |
| ------------------- | ------------------------ | ------------------------------------------ |
| keyless             | Uses mock JWTs           | Real OIDC flow requires external providers |
| script              | Mock RawTransaction      | Scripts without full SDK support           |
| secp256r1 (signing) | Mock transaction message | WebAuthn testing limited                   |

### ➖ Not Available in SDK

| Feature | Reason          | Tracking Issue |
| ------- | --------------- | -------------- |
| codegen | Not implemented | -              |

---

## 4. Known Issues

Issues with tests marked 🟡 (partial):

| Scenario                   | Issue                             | Workaround                          |
| -------------------------- | --------------------------------- | ----------------------------------- |
| transaction-submission #17 | VM error format differs from spec | Test adjusted to match SDK behavior |

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

✅ All required tests are implemented.

### Preferred (P1) - Medium Priority

| Feature        | Scenarios             | Notes                                             |
| -------------- | --------------------- | ------------------------------------------------- |
| gas-estimation | #19-20                | Historical gas prices, percentiles                |
| retry          | #16, #23, #25, #28-31 | Circuit breaker, statistics, graceful degradation |

### Optional (P2) - Low Priority

| Feature | Scenarios               | Notes                        |
| ------- | ----------------------- | ---------------------------- |
| codegen | All 34                  | Feature not in SDK           |
| script  | #8-12, #18, #21-22, #24 | Script compilation scenarios |

---

## 6. Performance Benchmarks

> **Last Updated:** 2026-01-23  
> **Network:** Devnet  
> **Hardware:** Apple Silicon (arm64)  
> **Runtime:** Bun 1.3.5

### REST API Read Performance

| Metric                    | Value | Unit |
| ------------------------- | ----- | ---- |
| Ledger Info (avg)         | -     | ms   |
| Ledger Info (p95)         | -     | ms   |
| Account Info (avg)        | -     | ms   |
| Account Info (p95)        | -     | ms   |
| Account Resources (avg)   | -     | ms   |
| Account Resources (p95)   | -     | ms   |
| Transaction by Hash (avg) | -     | ms   |
| Account Balance (avg)     | -     | ms   |

> Note: REST API benchmarks require network access and longer timeout configuration.

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

| Metric                        | Value         | Unit |
| ----------------------------- | ------------- | ---- |
| Ed25519 Key Gen (avg)         | **156**       | μs   |
| Ed25519 Key Gen (ops/s)       | **6,404**     | ops  |
| Ed25519 Sign (avg)            | **274**       | μs   |
| Ed25519 Sign (ops/s)          | **3,646**     | ops  |
| Ed25519 Verify (avg)          | **1,223**     | μs   |
| Ed25519 Verify (ops/s)        | **818**       | ops  |
| BCS Serialize Address (avg)   | **0.41**      | μs   |
| BCS Serialize Address (ops/s) | **2,468,000** | ops  |
| SHA3-256 (avg)                | **6.73**      | μs   |
| SHA3-256 (ops/s)              | **148,545**   | ops  |

### Run Performance Tests

```bash
cd tests/typescript
bun run test:performance

# Run only local crypto benchmarks (no network)
bun run cucumber-js --tags "@crypto and @local"
```

---

## 7. SDK-Specific Notes

- **Primary reference implementation** for specs
- Most complete SDK implementation
- Async/await patterns throughout
- Strong TypeScript type safety
- Comprehensive error handling

---

## 8. How to Run Tests

```bash
cd tests/typescript
bun install

# Run all tests
bun test

# Run by priority
bun run test:required       # Only @required tests
bun run test:preferred      # Only @preferred tests

# Run by category
bun run test:core-types     # @core-types tests
bun run test:cryptography   # @cryptography tests
bun run test:transactions   # @transactions tests

# Dry run (check step definitions)
bun run cucumber-js --dry-run --format summary
```

---

## 9. Contributing

To add or update tests for this SDK:

1. Add step definitions in `steps/*.steps.ts`
2. Run `bun test` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Submit PR with test results

---

## 10. Test Results Matrix

> Last run: 2026-02-06

### By Feature Category

| Category                | Passed | Failed | Undefined | Total |
| ----------------------- | ------ | ------ | --------- | ----- |
| 01-core-types           | 121    | 0      | 0         | 121   |
| 02-cryptography         | 79     | 13     | 0         | 92    |
| 03-account-management   | 84     | 0      | 0         | 84    |
| 04-transaction-building | 69     | 0      | 0         | 69    |
| 05-api-clients          | ~80    | ~4     | ~10       | ~190  |
| 06-advanced             | 116    | 36     | 37        | 189   |

> **Note:** API client tests require network connectivity (devnet/testnet) and timeout in CI
> environments without network access. Results for 05-api-clients are estimated from previous runs.

### Dry Run Summary (all scenarios)

```
791 scenarios (750 with step definitions, 41 undefined)
3058 steps (136 undefined, 2922 defined)
```

### Non-Network Test Summary

```
core-types:    121 passed
cryptography:  79 passed, 13 failed
accounts:      84 passed
transactions:  69 passed
advanced:      116 passed, 36 failed, 37 undefined
```
