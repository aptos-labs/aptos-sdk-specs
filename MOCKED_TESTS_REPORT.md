# Mocked, Skipped & Placeholder Tests Report

> Generated: 2026-01-31 Scope: All SDK test implementations (TypeScript, Go, Rust, Python, .NET,
> Kotlin)
>
> **Historical note:** This inventory predates the BLS specification removal. BLS mentions here
> describe legacy mocked/placeholder coverage and are kept for historical audit context.

## Executive Summary

| Category                 | Count | Fixable? |
| ------------------------ | ----- | -------- |
| Genuine SDK limitations  | ~660  | No       |
| No-op assertions         | ~108  | Yes      |
| Mock/placeholder impls   | ~31   | Partial  |
| Empty implementations    | ~489  | Partial  |
| Network-dependent        | ~6    | No       |
| Documentation-only steps | ~60   | No       |
| **Total**                | ~1354 |          |

## TypeScript (`tests/typescript/steps/`)

### No-Op Assertions (`expect(true).to.be.true`) — 108 instances

| File                            | Count | Fixable | Category                  |
| ------------------------------- | ----- | ------- | ------------------------- |
| error-handling.steps.ts         | 37    | 8       | error property assertions |
| transaction-submission.steps.ts | 19    | 4       | VM error/submission       |
| faucet.steps.ts                 | 13    | 0       | network-dependent         |
| retry.steps.ts                  | 11    | 5       | retry behavior            |
| simulation.steps.ts             | 10    | 1       | simulation events         |
| gas-estimation.steps.ts         | 7     | 4       | gas estimate properties   |
| transaction.steps.ts            | 3     | 0       | documentation-only        |
| api-client.steps.ts             | 3     | 0       | documentation-only        |
| secp256r1.steps.ts              | 2     | 0       | SDK limitation            |
| script.steps.ts                 | 1     | 0       | documentation-only        |
| keyless.steps.ts                | 1     | 0       | SDK limitation            |
| cryptography.steps.ts           | 1     | 0       | documentation-only        |

### Mock/Placeholder Implementations

| File                            | Type        | Description                                 | Fixable?                    |
| ------------------------------- | ----------- | ------------------------------------------- | --------------------------- |
| keyless.steps.ts                | Mock        | Mock JWT, pepper, ZK proof                  | No (requires OIDC provider) |
| script.steps.ts                 | Mock        | Mock RawTransaction, submission, simulation | Partial                     |
| transaction-submission.steps.ts | Mock        | Mock hash, simulated waits                  | Yes                         |
| secp256r1.steps.ts              | Mock        | Simulated WebAuthn assertion                | No (requires hardware)      |
| hashing.steps.ts                | Placeholder | Placeholder HMAC-SHA512                     | Yes                         |
| indexer.steps.ts                | TODO        | Should make actual indexer API call         | Network-dependent           |
| serialization.steps.ts          | TODO        | Signed integer types not working            | Yes                         |

---

## Go (`tests/go/`) — 737 `godog.ErrPending` instances

### Pending by Feature Area

| File                 | Count | Root Cause                                | Fixable?       |
| -------------------- | ----- | ----------------------------------------- | -------------- |
| the_steps.go         | 73    | Mixed (BLS, keyless, secp256r1, mnemonic) | No             |
| error_steps.go       | 68    | Error handling patterns                   | Partial        |
| more_steps.go        | 61    | Mixed features                            | Partial        |
| final_steps.go       | 61    | Mixed features                            | Partial        |
| feepayer_steps.go    | 55    | Fee payer (partial SDK support)           | Partial        |
| assertion_steps.go   | 48    | Validation assertions                     | Partial        |
| mnemonic_steps.go    | 43    | SDK limitation (no BIP-39)                | No             |
| remaining_steps.go   | 39    | Mixed features                            | Partial        |
| validation_steps.go  | 38    | Validation assertions                     | Partial        |
| retry_steps.go       | 36    | SDK handles internally                    | No (by design) |
| simulation_steps.go  | 32    | Simulation validation                     | Partial        |
| keyless_steps.go     | 30    | SDK limitation                            | No             |
| given_steps.go       | 27    | Setup steps                               | Partial        |
| bls_steps.go         | 22    | SDK limitation                            | No             |
| query_steps.go       | 22    | SDK limitation (no GraphQL)               | No             |
| client_steps.go      | 21    | API client tests                          | Partial        |
| sender_steps.go      | 18    | Sender setup                              | Partial        |
| codegen_steps.go     | 17    | SDK limitation                            | No             |
| transaction_steps.go | 16    | Transaction building                      | Partial        |
| action_steps.go      | 16    | Various actions                           | Partial        |
| abi_steps.go         | 14    | SDK limitation                            | No             |
| try_steps.go         | 13    | BLS/Secp256r1 verify                      | No             |
| indexer_steps.go     | 9     | SDK limitation                            | No             |
| misc_steps.go        | 8     | Various                                   | Partial        |
| encoding_steps.go    | 8     | Encoding helpers                          | Partial        |
| setup_steps.go       | 7     | Setup                                     | Partial        |
| multi_agent_steps.go | 5     | Multi-agent                               | Partial        |
| multisig_steps.go    | 3     | Multi-sig                                 | Partial        |
| script_steps.go      | 2     | Script transactions                       | Partial        |
| Others               | 4     | Various                                   | Various        |

### Genuine SDK Limitations (Not Fixable)

- **BLS12-381**: Not implemented in Go SDK
- **Keyless/OIDC**: Not implemented in Go SDK
- **Secp256r1/WebAuthn**: Not implemented in Go SDK
- **BIP-39 Mnemonic**: Not exposed by Go SDK
- **Indexer/GraphQL**: Not implemented in Go SDK
- **Codegen/ABI**: Not implemented in Go SDK
- **MultiKey**: Not implemented in Go SDK

---

## Rust (`tests/rust/src/steps/`) — ~31 placeholder instances

| File                    | Count | Type        | Description                              | Fixable?            |
| ----------------------- | ----- | ----------- | ---------------------------------------- | ------------------- |
| network_steps.rs        | 15    | Placeholder | Hardcoded benchmark timings, mock hashes | Yes                 |
| secp_steps.rs           | 3     | Placeholder | WebAuthn/COSE key placeholders           | Partial             |
| script_steps.rs         | 3     | Placeholder | Script simulation empty bodies           | Network-dependent   |
| entry_function_steps.rs | 3     | Placeholder | ABI stubs                                | No (SDK limitation) |
| multi_agent_steps.rs    | 2     | Placeholder | Ed25519 used instead of Secp256k1        | SDK limitation      |
| fee_payer_steps.rs      | 2     | Placeholder | Ed25519 used instead of Secp256k1        | SDK limitation      |
| mnemonic_steps.rs       | 1     | Placeholder | Secp256k1 mnemonic derivation            | SDK limitation      |
| keyless_steps.rs        | 1     | Placeholder | Mock keyless implementation              | Network-dependent   |
| bls_steps.rs            | 1     | Placeholder | BLS authenticator verification           | Partial             |

---

## Python (`tests/python/steps/`) — 312 skip calls + 489 empty `pass`

### Skip Calls (`context.scenario.skip()`) — 312 instances

| File                     | Count | Root Cause                | Fixable? |
| ------------------------ | ----- | ------------------------- | -------- |
| bls_steps.py             | 61    | SDK limitation            | No       |
| mnemonic_steps.py        | 50    | SDK limitation            | No       |
| secp256r1_steps.py       | 49    | SDK limitation            | No       |
| given_extra_steps.py     | 26    | Mixed (BLS, keyless, etc) | No       |
| keyless_steps.py         | 25    | SDK limitation            | No       |
| codegen_steps.py         | 23    | SDK limitation            | No       |
| when_more_steps.py       | 13    | Keyless/codegen           | No       |
| then_final_steps.py      | 12    | Secp256r1/BLS             | No       |
| then_more_steps.py       | 10    | Mixed                     | No       |
| when_extra_steps.py      | 8     | Mixed                     | Partial  |
| when_final_steps.py      | 7     | Mixed                     | Partial  |
| secp256k1_extra_steps.py | 6     | SDK limitation            | No       |
| assertion_steps.py       | 6     | Mixed                     | Partial  |
| then_extra_steps.py      | 4     | Mixed                     | Partial  |
| sdk_steps.py             | 4     | SDK limitation            | No       |
| script_steps.py          | 3     | Partial SDK support       | Partial  |
| account_extra_steps.py   | 3     | Mixed                     | Partial  |
| multi_sig_extra_steps.py | 2     | Partial SDK support       | Partial  |

### Empty `pass` Implementations — 489 instances

| File                   | Count | Root Cause                     | Fixable? |
| ---------------------- | ----- | ------------------------------ | -------- |
| then_final_steps.py    | 130   | Validation assertions missing  | Partial  |
| then_more_steps.py     | 112   | Validation assertions missing  | Partial  |
| assertion_steps.py     | 62    | Assertion stubs                | Partial  |
| then_extra_steps.py    | 39    | Validation assertions missing  | Partial  |
| indexer_steps.py       | 34    | SDK limitation (no indexer)    | No       |
| transaction_steps.py   | 20    | Transaction validation missing | Yes      |
| view_function_steps.py | 15    | View function validation       | Yes      |
| codegen_steps.py       | 12    | SDK limitation                 | No       |
| retry_steps.py         | 11    | SDK handles internally         | No       |
| account_extra_steps.py | 10    | Account validation             | Partial  |
| client_steps.py        | 8     | API client validation          | Partial  |
| when_more_steps.py     | 8     | Setup steps                    | Partial  |
| script_steps.py        | 8     | Script transaction stubs       | Partial  |
| misc_steps.py          | 4     | Various                        | Partial  |
| benchmark_steps.py     | 3     | Benchmark stubs                | Yes      |
| Others                 | 13    | Various                        | Various  |

---

## .NET (`tests/dotnet/StepDefinitions/`) — ~361 issues

| File                       | NotImpl | Pending | Placeholder | Fixable?            |
| -------------------------- | ------- | ------- | ----------- | ------------------- |
| KeylessSteps.cs            | 49      | 0       | 0           | No (SDK limitation) |
| ErrorSteps.cs              | 0       | 0       | 49          | Partial             |
| MultiAgentExtraSteps.cs    | 0       | 0       | 39          | Partial             |
| MoreCryptoSteps.cs         | 0       | 12      | 33          | No (BLS/keyless)    |
| CodegenSteps.cs            | 0       | 17      | 20          | No (SDK limitation) |
| KeylessStepsExtra.cs       | 0       | 33      | 0           | No (SDK limitation) |
| BLSSteps.cs                | 29      | 0       | 0           | No (SDK limitation) |
| TransactionBuilderSteps.cs | 0       | 0       | 27          | Partial             |
| SerializationExtraSteps.cs | 0       | 0       | 27          | Partial             |
| SigningSteps.cs            | 0       | 0       | 18          | Partial             |
| AdditionalSteps.cs         | 0       | 0       | 5           | Partial             |
| SerializationSteps.cs      | 1       | 0       | 0           | Yes                 |

---

## Kotlin (`tests/kotlin/src/test/kotlin/`) — 39 `NotImplementedError` throws

| File                | Count | Root Cause                         | Fixable? |
| ------------------- | ----- | ---------------------------------- | -------- |
| CryptoSteps.kt      | 19    | BLS, Secp256r1, keyless (SDK gaps) | No       |
| AccountSteps.kt     | 11    | Mnemonic, keyless (SDK gaps)       | No       |
| TransactionSteps.kt | 7     | Fee-payer, multi-agent (SDK gaps)  | No       |
| TypeTagSteps.kt     | 2     | Nested generics (SDK gap)          | No       |

---

## What's Fixable (Action Items)

### TypeScript (22 fixes)

1. **error-handling.steps.ts**: Replace 8 no-op assertions with real error property checks
2. **transaction-submission.steps.ts**: Replace 4 no-op assertions + mock hash with real calls
3. **retry.steps.ts**: Replace 5 no-op assertions with retry config assertions
4. **gas-estimation.steps.ts**: Replace 4 no-op assertions with gas estimate checks
5. **simulation.steps.ts**: Replace 1 no-op assertion with events comparison

### Go (partial fixes)

- Fix simulation, error handling, and multi-sig steps where SDK supports the feature
- Many pending steps are genuine SDK limitations and cannot be fixed

### Rust (benchmark fixes)

- Replace 15 hardcoded benchmark timings with actual measurements
- Fix Secp256r1 COSE key placeholder where SDK supports it

### Python (validation fixes)

- Replace empty `pass` in transaction validation, view function, and benchmark steps
- Many skips are genuine SDK limitations

### .NET (validation fixes)

- Replace "Validation placeholder" no-ops with real assertions in error, multi-agent, transaction
  builder, serialization, and signing steps

### Kotlin

- All 39 `NotImplementedError` are genuine SDK limitations — **no fixes possible**

## What's NOT Fixable

| Limitation              | Affected SDKs                        |
| ----------------------- | ------------------------------------ |
| BLS12-381               | TypeScript, Go, Python, .NET, Kotlin |
| Keyless/OIDC            | Go, Python, .NET, Kotlin             |
| Secp256r1/WebAuthn      | Go, Python, .NET, Kotlin             |
| BIP-39 Mnemonic         | Go, .NET, Kotlin                     |
| Indexer/GraphQL         | Go, Python                           |
| Codegen/ABI             | All SDKs                             |
| Secp256k1               | Python, .NET, Kotlin                 |
| MultiKey                | Go                                   |
| Network-dependent tests | All SDKs (testnet/faucet access)     |
