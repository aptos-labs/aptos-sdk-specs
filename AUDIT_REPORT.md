# Aptos SDK API Specs Audit Report

> **Date:** 2026-02-06 **Author:** Automated Audit **Scope:** Aptos API behavioral specs vs. Aptos
> TS SDK, Rust SDK, Go SDK, and aptos-core protocol
>
> **Historical note:** This report predates the BLS specification removal. Any BLS references in
> this document reflect the repository state at audit time and are not current behavioral
> requirements.

---

## Executive Summary

This audit evaluates the Aptos SDK behavioral specification repository against the actual
capabilities of the Aptos TypeScript SDK (`@aptos-labs/ts-sdk` ^5.2.0), the Aptos Rust SDK
(`aptos-sdk` dev/git), and the Aptos Go SDK (`aptos-go-sdk` v1.11.0), cross-referenced with the
protocol features available in `aptos-labs/aptos-core`.

### Key Findings

| Area                    | Status          | Summary                                                                            |
| ----------------------- | --------------- | ---------------------------------------------------------------------------------- |
| **Spec Completeness**   | 🟡 Partial      | 826 scenarios across 7 categories; several protocol features are not yet specified |
| **TypeScript Coverage** | 🟡 ~91% defined | 750/826 step definitions exist; 76 undefined (BLS12-381, codegen)                  |
| **Rust Coverage**       | ✅ ~92% pass    | 761/826 scenarios pass (when buildable); most comprehensive SDK                    |
| **Go Coverage**         | 🟡 ~40% pass    | 333/826 pass; 148 failed (mostly network/faucet); 345 pending                      |
| **Protocol Gaps**       | ❌ Significant  | Multiple aptos-core features have no spec coverage                                 |

---

## 1. Specification vs. Protocol Gap Analysis

### 1.1 Features in aptos-core / TS SDK with NO spec coverage

These are significant capabilities available in the Aptos protocol and the TypeScript SDK that have
**no corresponding feature files** in the specs repository:

| Missing Feature                    | Priority | Available In  | Notes                                                                                                                                                     |
| ---------------------------------- | -------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Account Abstraction**            | P1       | TS SDK        | `addAuthenticationFunctionTransaction()`, `removeAuthenticationFunctionTransaction()`, `removeDispatchableAuthenticatorTransaction()` - newer AIP feature |
| **ANS (Aptos Name Service)**       | P1       | TS SDK, Go v2 | `registerName()`, `getOwnerAddress()`, `getTargetAddress()`, `setPrimaryName()`, `renewDomain()`, `getAccountDomains()`                                   |
| **Digital Asset (NFT) Operations** | P1       | TS SDK        | `createCollectionTransaction()`, `mintDigitalAssetTransaction()`, `transferDigitalAssetTransaction()`, `burnDigitalAssetTransaction()`, token queries     |
| **Fungible Asset Operations**      | P1       | TS SDK        | `transferFungibleAsset()`, `getFungibleAssetMetadata()`, `getCurrentFungibleAssetBalances()`, `getFungibleAssetActivities()`                              |
| **Coin Operations**                | P0       | TS SDK, Go    | `transferCoinTransaction()`, APT transfer helpers, coin balance queries                                                                                   |
| **Staking**                        | P2       | TS SDK        | `getDelegatedStakingActivities()`, `getNumberOfDelegators()`                                                                                              |
| **Table Operations**               | P2       | TS SDK, Go    | `getTableItem()`, `getTableItemsData()`                                                                                                                   |
| **Object Operations**              | P2       | TS SDK        | `getObjectDataByObjectAddress()`, `transferObjectTransaction()`                                                                                           |
| **Block Endpoints**                | P1       | aptos-core    | `GET /v1/blocks/by_height/{height}`, `GET /v1/blocks/by_version/{version}`                                                                                |
| **Batch Transaction Submission**   | P1       | aptos-core    | `POST /v1/transactions/batch` - submit multiple txs in one request                                                                                        |
| **Transaction Summaries**          | P2       | aptos-core    | `get_accounts_transaction_summaries` endpoint                                                                                                             |
| **Encode Submission**              | P2       | aptos-core    | `POST /v1/transactions/encode_submission`                                                                                                                 |
| **Wait for Transaction by Hash**   | P0       | aptos-core    | Native `wait_transaction_by_hash` endpoint (vs polling)                                                                                                   |
| **Go SDK v2**                      | N/A      | Go v2         | Tests target v1.11.0 but Go SDK has a v2 with keyless, sponsored tx, codegen, ANS                                                                         |

### 1.2 Spec features with no protocol support

| Feature                                     | Status  | Notes                                                        |
| ------------------------------------------- | ------- | ------------------------------------------------------------ |
| **Performance Benchmarks** (07-performance) | Partial | Framework exists but no meaningful results yet for most SDKs |

---

## 2. TypeScript SDK (`@aptos-labs/ts-sdk` ^5.2.0) — Reference Implementation

### 2.1 Current Coverage

| Metric                     | Value          |
| -------------------------- | -------------- |
| **Total scenarios**        | 826            |
| **Step definitions exist** | 750 (91%)      |
| **Undefined steps**        | 76 (9%)        |
| **Estimated passing**      | ~551/826 (67%) |

### 2.2 Fully Covered Areas (All scenarios have step definitions)

- ✅ **01-core-types**: address (22/22), serialization (18/18), type-tags (24/24)
- ✅ **02-cryptography**: ed25519 (25/25), hashing (20/20), secp256k1 (19/19), secp256r1 (26/26)
- ✅ **03-account-management**: authentication-key (17/17), single-key (28/28), mnemonic (29/29)
- ✅ **04-transaction-building**: entry-function (24/24), raw-transaction (21/21), signing (24/24),
  script (15/25 partial)
- ✅ **05-api-clients**: fullnode-api (25/25), transaction-submission (27/28), faucet (23/23),
  gas-estimation (24/26), view-functions (28/28), retry (25/32), indexer (28/31)
- ✅ **06-advanced**: error-handling (28/30), simulation (21/26), multi-agent (20/20), fee-payer
  (21/23), multi-signature (23/23), keyless (32/33)

### 2.3 Undefined Scenarios (76 total)

| Category           | Count | Details                                                       |
| ------------------ | ----- | ------------------------------------------------------------- |
| **BLS12-381**      | 35    | All scenarios — feature not implemented in TS SDK             |
| **Codegen**        | 34    | All scenarios — feature not implemented in TS SDK             |
| **Gas estimation** | 1     | `#36: Use simulation for max_gas_amount`                      |
| **Indexer**        | 3     | Raw GraphQL query, query with variables, handle query timeout |
| **Fee-payer**      | 2     | Fee payer insufficient balance, fee payer gas payment         |
| **Keyless**        | 1     | Sign transaction with ephemeral key pair                      |

### 2.4 Issues Found

1. **Faucet authentication change**: The Aptos testnet faucet now requires an `x-is-jwt` header.
   Tests using the faucet without this header will fail. This affects Go SDK tests significantly
   (148 failures).

2. **Mock-heavy tests**: Keyless, script, and some secp256r1 tests use mocks rather than real SDK
   calls. These don't validate actual protocol behavior.

3. **Missing TS SDK capabilities not in specs**: The TS SDK has `AccountAbstraction`, `ANS`,
   `DigitalAsset`, `FungibleAsset`, `Coin`, `Staking`, `Table`, and `Object` modules with no
   corresponding feature specs.

---

## 3. Rust SDK (`aptos-sdk` dev) — Most Feature-Complete

### 3.1 Current Coverage

| Metric              | Value                                   |
| ------------------- | --------------------------------------- |
| **Total scenarios** | 826                                     |
| **Passing**         | 591 (72%)                               |
| **Skipped**         | 235 (28%)                               |
| **Build status**    | ❌ Requires Cargo nightly (edition2024) |

### 3.2 Build Issue

The Rust SDK requires `edition2024` in Cargo, which needs a newer Rust toolchain than the current CI
environment (cargo 1.82.0). The `aptos-sdk-macros` crate uses this unstable feature.

**Action needed**: Update CI Rust toolchain to nightly or stable >= 1.85.0.

### 3.3 Feature Availability

The Rust SDK is the most complete implementation with all these features available:

- ✅ All core types, cryptography (including BLS12-381), serialization
- ✅ All account management including mnemonic derivation
- ✅ All transaction building and signing
- ✅ Multi-agent, fee-payer, multi-signature, keyless
- ✅ Codegen (via macros)
- ✅ Fullnode API, faucet, indexer

### 3.4 Skipped Tests (235)

Primarily:

- Network-dependent tests requiring live testnet/devnet access
- Some advanced feature edge cases
- Error handling scenarios requiring specific API responses

### 3.5 Missing from Specs

The Rust SDK has capabilities not covered in specs:

- **Transaction batching** (`transaction/batch.rs`)
- **Sponsored transactions** (`transaction/sponsored.rs`)
- **Simulation** (`transaction/simulation.rs`) — partially specified

---

## 4. Go SDK (`aptos-go-sdk` v1.11.0)

### 4.1 Current Coverage

| Metric              | Value     |
| ------------------- | --------- |
| **Total scenarios** | 826       |
| **Passing**         | 333 (40%) |
| **Failed**          | 148 (18%) |
| **Pending**         | 345 (42%) |

### 4.2 Test Results Analysis

**Pass breakdown by category:**

| Category                | Passed | Failed | Pending | Total |
| ----------------------- | ------ | ------ | ------- | ----- |
| 01-core-types           | 121    | 0      | 0       | 121   |
| 02-cryptography         | ~60    | ~10    | ~15     | ~85   |
| 03-account-management   | ~35    | ~5     | ~8      | ~48   |
| 04-transaction-building | ~55    | ~10    | 0       | ~65   |
| 05-api-clients          | ~50    | ~15    | 0       | ~65   |
| 06-advanced             | ~8     | ~44    | 0       | ~52   |
| 07-performance          | 0      | ~10    | 0       | ~10   |

### 4.3 Root Causes of Failures (148)

1. **Faucet authentication** (~80 failures): The testnet faucet now requires `x-is-jwt` header set
   to `true`. The Go SDK's faucet client doesn't send this header, causing all faucet-dependent
   tests to fail with `500 Internal Server Error`.

2. **Network-dependent tests** (~50): Tests requiring live testnet connections fail due to network
   issues or changed API behavior.

3. **SDK limitations** (~10): Secp256r1/MultiEd25519/MultiKey not fully implemented.

4. **Coin module difference** (~4): Go SDK uses `aptos_account::transfer` instead of
   `coin::transfer`.

### 4.4 Critical Gap: Go SDK v2 Not Tested

The Go SDK repository now has a **v2** directory (`v2/`) with significantly expanded capabilities:

| v2 Feature                 | v1 Status        | Notes                                         |
| -------------------------- | ---------------- | --------------------------------------------- |
| **Keyless auth**           | ❌ Not available | `v2/keyless/` has full keyless implementation |
| **Sponsored transactions** | ❌ Not available | `v2/sponsored/` has fee-payer support         |
| **ANS**                    | ❌ Not available | `v2/ans/` has name service support            |
| **Codegen**                | ❌ Not available | `v2/codegen/` has code generation             |
| **Account module**         | Partial          | `v2/account/` has improved account management |

**Recommendation**: Update test suite to target Go SDK v2, or at minimum add v2 as an additional
test target.

### 4.5 Missing Step Definitions (345 pending)

Major areas without Go step definitions:

| Feature               | Pending Scenarios | SDK Support             |
| --------------------- | ----------------- | ----------------------- |
| Faucet                | 23                | ✅ Available (v1)       |
| Gas estimation        | 26                | ✅ Available (v1)       |
| View functions        | 28                | ✅ Available (v1)       |
| Retry                 | 32                | 🟡 Partial (internal)   |
| Simulation            | 26                | ✅ Available (v1)       |
| Error handling (most) | ~29               | 🟡 Partial              |
| Multi-agent           | 20                | ❌ Need v2              |
| Fee-payer             | 23                | ❌ Need v2              |
| Multi-signature       | 23                | 🟡 MultiEd25519 partial |
| Keyless               | 33                | ❌ Need v2              |
| Codegen               | 34                | ❌ Need v2              |
| Indexer               | 31                | ✅ Available (v1)       |

---

## 5. Cross-SDK Comparison Matrix

### 5.1 Feature Coverage by Category

| Feature Category    | TS      | Rust         | Go (v1) | Go (v2) | aptos-core |
| ------------------- | ------- | ------------ | ------- | ------- | ---------- |
| **Core Types**      | ✅ 100% | ✅ 100%      | ✅ 100% | ✅      | ✅         |
| **Ed25519**         | ✅ 100% | ✅ 100%      | 🟡 92%  | ✅      | ✅         |
| **Secp256k1**       | ✅ 100% | ✅ 100%      | ➖ N/A  | ✅      | ✅         |
| **Secp256r1**       | ✅ 100% | ✅ 100%      | ➖ N/A  | ?       | ✅         |
| **BLS12-381**       | ❌ 0%   | ✅ Available | ➖ N/A  | ?       | ✅         |
| **Hashing**         | ✅ 100% | ✅ 100%      | ✅ 100% | ✅      | ✅         |
| **Auth Keys**       | ✅ 100% | ✅ 100%      | 🟡 71%  | ✅      | ✅         |
| **Single Key**      | ✅ 100% | ✅ 100%      | 🟡 61%  | ✅      | ✅         |
| **Mnemonic**        | ✅ 100% | ✅ 100%      | ➖ N/A  | ?       | ✅         |
| **Entry Function**  | ✅ 100% | ✅ 100%      | 🟡 92%  | ✅      | ✅         |
| **Raw Transaction** | ✅ 100% | ✅ 100%      | 🟡 86%  | ✅      | ✅         |
| **Signing**         | ✅ 100% | ✅ 100%      | 🟡 71%  | ✅      | ✅         |
| **Script**          | 🟡 60%  | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Fullnode API**    | ✅ 100% | ✅ 100%      | 🟡 76%  | ✅      | ✅         |
| **Tx Submission**   | 🟡 96%  | ✅ 100%      | 🟡 64%  | ✅      | ✅         |
| **Faucet**          | ✅ 100% | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Gas Estimation**  | 🟡 92%  | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **View Functions**  | ✅ 100% | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Retry**           | 🟡 78%  | ❌ 0%        | ❌ 0%   | ?       | N/A        |
| **Indexer**         | 🟡 90%  | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Error Handling**  | 🟡 93%  | 🟡 90%       | 🟡 3%   | ?       | ✅         |
| **Simulation**      | 🟡 81%  | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Multi-Agent**     | ✅ 100% | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Fee-Payer**       | 🟡 91%  | ❌ 0%        | ❌ 0%   | ✅ (v2) | ✅         |
| **Multi-Sig**       | ✅ 100% | ❌ 0%        | ❌ 0%   | ?       | ✅         |
| **Keyless**         | ✅ 100% | ❌ 0%        | ❌ 0%   | ✅ (v2) | ✅         |
| **Codegen**         | ❌ 0%   | ❌ 0%        | ❌ 0%   | ✅ (v2) | N/A        |

### 5.2 Required (P0) Feature Gaps

Features tagged `@required` that are NOT fully passing:

| SDK            | P0 Gaps                                   | Impact                             |
| -------------- | ----------------------------------------- | ---------------------------------- |
| **TypeScript** | 4 failures in error-handling/simulation   | Low                                |
| **Rust**       | Build failure (toolchain); 235 skipped    | Medium — fix toolchain             |
| **Go**         | 148 failures (mostly faucet); 345 pending | High — faucet auth + missing steps |

---

## 6. Protocol Compatibility Issues

### 6.1 Faucet Authentication Change (CRITICAL)

The Aptos testnet faucet now requires the `x-is-jwt` header set to `'true'`. This is a protocol
change that breaks existing SDK faucet integrations:

```
Error: "The x-is-jwt header must be present and set to 'true'"
```

**Affected SDKs:**

- Go SDK v1: All faucet-dependent tests fail (estimated 80+ scenarios)
- Other SDKs: May be affected if running against live testnet

**Required Action:**

1. Update Go SDK's `faucet.go` to include `x-is-jwt: true` header
2. Update spec to document this requirement in `faucet.feature`
3. Add test scenario for faucet authentication requirements

### 6.2 API Endpoint Changes

| Endpoint                                          | Spec Status        | aptos-core Status | Action Needed             |
| ------------------------------------------------- | ------------------ | ----------------- | ------------------------- |
| `POST /v1/transactions/batch`                     | ❌ Not specified   | ✅ Available      | Add batch submission spec |
| `GET /v1/blocks/by_height`                        | ❌ Not specified   | ✅ Available      | Add block query spec      |
| `GET /v1/blocks/by_version`                       | ❌ Not specified   | ✅ Available      | Add block query spec      |
| `POST /v1/transactions/encode_submission`         | ❌ Not specified   | ✅ Available      | Add encode spec           |
| `GET /v1/accounts/{addr}/events/{handle}/{field}` | 🟡 In spec.md only | ✅ Available      | Add feature file          |
| `POST /v1/view` (versioned)                       | ✅ Specified       | ✅ Available      | OK                        |

### 6.3 Move Module Interactions Not Specified

The specs focus on generic API calls but don't specify interactions with standard Move modules:

| Module                                     | TS SDK Support        | Spec Status |
| ------------------------------------------ | --------------------- | ----------- |
| `0x1::coin`                                | ✅ coin.ts            | ❌ No spec  |
| `0x1::aptos_coin`                          | ✅ (via coin)         | ❌ No spec  |
| `0x1::aptos_account`                       | ✅                    | ❌ No spec  |
| `0x1::fungible_asset`                      | ✅ fungibleAsset.ts   | ❌ No spec  |
| `0x4::token` (Digital Asset)               | ✅ digitalAsset.ts    | ❌ No spec  |
| `0x4::collection`                          | ✅ (via digitalAsset) | ❌ No spec  |
| `0x1::aptos_names`                         | ✅ ans.ts             | ❌ No spec  |
| `0x1::staking_contract`                    | ✅ staking.ts         | ❌ No spec  |
| `0x1::object`                              | ✅ object.ts          | ❌ No spec  |
| `0x1::account::dispatchable_authenticator` | ✅ abstraction.ts     | ❌ No spec  |

---

## 7. Recommendations

### 7.1 Critical (Do Immediately)

1. **Fix Go faucet authentication**: Update the Go SDK tests to include the `x-is-jwt` header or
   switch to a mock faucet for non-integration tests. This alone would recover ~80 failing
   scenarios.

2. **Update Rust CI toolchain**: The Rust tests cannot build because the SDK requires `edition2024`.
   Upgrade to Rust 1.85+ or nightly.

3. **Add faucet auth requirement to spec**: Update `faucet.feature` to include a scenario requiring
   JWT authentication headers.

### 7.2 High Priority (Next Sprint)

4. **Create Coin/Token Transfer specs**: Add a `08-token-operations/` feature category covering:
   - APT transfers
   - Fungible Asset transfers
   - Digital Asset (NFT) minting, transfer, burn
   - Coin balance queries

5. **Create ANS specs**: Add Aptos Name Service feature file covering name registration, resolution,
   primary names.

6. **Create Account Abstraction specs**: Add feature file for the newer account
   abstraction/dispatchable authenticator feature.

7. **Create Block Query specs**: Add `blocks.feature` to `05-api-clients/` covering block-by-height
   and block-by-version queries.

8. **Create Batch Transaction specs**: Add batch submission feature to
   `05-api-clients/transaction-submission.feature` or a new file.

9. **Target Go SDK v2**: The Go SDK v2 has significantly more capabilities (keyless, sponsored tx,
   codegen, ANS). Update `tests/go/go.mod` and step definitions accordingly.

### 7.3 Medium Priority (Roadmap)

10. **Implement Rust SDK preferred/optional test steps**: The Rust SDK supports faucet, gas
    estimation, view functions, indexer, simulation, multi-agent, fee-payer, multi-sig, and keyless
    — but 235 spec scenarios are skipped. Implement step definitions for these.

11. **Implement Go SDK P1 step definitions**: View functions, gas estimation, faucet, retry, and
    simulation all have SDK support in Go v1 but no step definitions (130+ scenarios).

12. **Add Staking and Table specs**: Create feature files for staking queries and table item
    lookups.

13. **Remove mock-dependent tests or label them**: Keyless tests using mock JWTs, script tests using
    mock RawTransactions, and secp256r1 tests using mock transaction messages should be clearly
    labeled `@mock` or replaced with real integration tests.

14. **Add BLS12-381 TS SDK steps**: The TS SDK doesn't support BLS12-381, but the Rust SDK does.
    Consider whether BLS specs should remain or be marked SDK-specific.

### 7.4 Low Priority (Backlog)

15. **Complete codegen specs**: Currently 34 scenarios all undefined. Given Rust SDK has codegen via
    macros and Go v2 has a generator, implement step definitions.

16. **Performance benchmark standardization**: Fill in the missing performance data for TS, Rust,
    Python, Java, and .NET SDKs.

17. **Add WebSocket/streaming specs**: aptos-core likely supports event streaming; this is not
    specified.

18. **Add Object resource specs**: Object-based resource queries are a common pattern not currently
    specified.

---

## 8. Missing Test Vectors

| Feature             | Test Vector File    | Status                                   |
| ------------------- | ------------------- | ---------------------------------------- |
| Addresses           | `addresses.json`    | ✅ Complete                              |
| BCS Serialization   | `bcs.json`          | ✅ Complete                              |
| Mnemonics           | `mnemonics.json`    | ✅ Complete                              |
| Multi-Sig           | `multi-sig.json`    | ✅ Complete                              |
| Signatures          | `signatures.json`   | ✅ Complete                              |
| Transactions        | `transactions.json` | ✅ Complete                              |
| Type Tags           | `type-tags.json`    | ✅ Complete                              |
| **BLS12-381**       | ❌ Missing          | Needed for BLS test vectors              |
| **Secp256r1**       | ❌ Missing          | Needed for P-256 curve test vectors      |
| **Keyless**         | ❌ Missing          | Needed for keyless address/proof vectors |
| **Block queries**   | ❌ Missing          | Needed for block endpoint tests          |
| **Fungible Assets** | ❌ Missing          | Needed for FA transfer tests             |
| **ANS**             | ❌ Missing          | Needed for name resolution tests         |

---

## 9. Summary of Changes Needed

### New Feature Files Needed

| File                                         | Category  | Priority | Scenarios (est.) |
| -------------------------------------------- | --------- | -------- | ---------------- |
| `08-token-operations/coin-transfer.feature`  | Token Ops | P0       | ~15              |
| `08-token-operations/fungible-asset.feature` | Token Ops | P1       | ~20              |
| `08-token-operations/digital-asset.feature`  | Token Ops | P1       | ~25              |
| `05-api-clients/blocks.feature`              | API       | P1       | ~10              |
| `05-api-clients/batch-submission.feature`    | API       | P1       | ~8               |
| `06-advanced/account-abstraction.feature`    | Advanced  | P1       | ~15              |
| `06-advanced/ans.feature`                    | Advanced  | P1       | ~15              |
| `05-api-clients/table.feature`               | API       | P2       | ~8               |
| `06-advanced/staking.feature`                | Advanced  | P2       | ~10              |
| `06-advanced/object.feature`                 | Advanced  | P2       | ~10              |

### Existing Feature Files Needing Updates

| File                             | Change                                      | Priority |
| -------------------------------- | ------------------------------------------- | -------- |
| `faucet.feature`                 | Add JWT authentication requirement scenario | P0       |
| `transaction-submission.feature` | Add batch submission scenarios              | P1       |
| `fullnode-api.feature`           | Add block query scenarios                   | P1       |
| `codegen.feature`                | Implement TS/Rust/Go step definitions       | P2       |

### Test Infrastructure Updates

| Change                                       | Priority | Impact                                           |
| -------------------------------------------- | -------- | ------------------------------------------------ |
| Fix Go faucet `x-is-jwt` header              | P0       | Recovers ~80 Go test failures                    |
| Update Rust toolchain to 1.85+               | P0       | Enables all Rust tests to build                  |
| Add Go SDK v2 test target                    | P1       | Unlocks keyless, sponsored, ANS, codegen testing |
| Add mock faucet for offline tests            | P1       | Decouples tests from live network                |
| Add test vectors for BLS, secp256r1, keyless | P1       | Enables deterministic cross-SDK validation       |

---

## 10. Conclusion

The specification repository provides solid coverage for core cryptographic operations, BCS
serialization, and basic transaction building. However, significant gaps exist in:

1. **Higher-level token/asset operations** — The most commonly used SDK features (coin transfers,
   NFT operations, fungible assets) have zero spec coverage.

2. **Newer protocol features** — Account Abstraction, ANS, and block queries are available in the
   protocol but not specified.

3. **Go SDK targeting** — Tests target the older Go SDK v1 while v2 offers substantially more
   features.

4. **Infrastructure issues** — The faucet authentication change and Rust toolchain issue prevent
   meaningful test runs.

The TypeScript SDK serves well as the reference implementation (~91% step definitions), while the
Rust SDK has the most features. The Go SDK has the largest gap between available features
(especially in v2) and test coverage.

**Priority actions**: Fix the faucet auth issue, upgrade Rust toolchain, create coin/token transfer
specs, and target Go SDK v2.
