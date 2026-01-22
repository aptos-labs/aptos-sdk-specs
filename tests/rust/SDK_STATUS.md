# Rust SDK Test Status

> **Last Updated:** 2026-01-22
> **Last Verified:** Not verified (SDK path not available locally)

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `aptos-rust-sdk-v2` |
| **Version Tested** | dev (local path) |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-rust-sdk |
| **Package Registry** | crates.io (when published) |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | N/A | 370 | N/A |
| Preferred (P1) | N/A | 183 | N/A |
| Optional (P2) | N/A | 250 | N/A |
| **Total** | N/A | 803 | N/A |

> **Note:** Tests cannot run - SDK depends on local path `../../../crates/aptos-rust-sdk-v2`
> which is not available. Update Cargo.toml to use published crate or git dependency.

## Feature Availability

Features that are **not available** in this SDK (marked `[-]` in coverage matrix):

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| bls12381 | Not yet implemented | - |
| WebAuthn (secp256r1 #19-21) | Not yet implemented | - |
| faucet | API client not implemented | - |
| gas-estimation | API helpers not implemented | - |
| view-functions | API helpers not implemented | - |
| simulation | API helpers not implemented | - |
| multi-agent | Not yet implemented | - |
| fee-payer | Not yet implemented | - |
| multi-signature | Not yet implemented | - |
| keyless | Not yet implemented | - |
| codegen | Not yet implemented | - |

## Known Issues

Issues with tests that are marked `[~]` (partial):

| Scenario | Issue | Workaround |
|----------|-------|------------|
| address.feature #6 | Error message format differs | Test accepts SDK error format |
| address.feature #7 | Error message format differs | Test accepts SDK error format |

## Missing Test Implementations

### Required (P0) - Priority

Core required features are implemented. Gaps mainly in:
- Some error message format differences

### Preferred (P1)

- `mnemonic-derivation.feature` - Full (29/29)
- `secp256k1.feature` - Full (19/19)
- `faucet.feature` - None (0/23) - API not implemented
- `gas-estimation.feature` - None (0/26) - API not implemented
- `view-functions.feature` - None (0/28) - API not implemented
- `retry.feature` - None (0/32) - Not implemented
- `simulation.feature` - None (0/26) - API not implemented

### Optional (P2)

- `secp256r1.feature` #19-21 - WebAuthn support
- All advanced features (multi-agent, fee-payer, multi-sig, keyless, codegen)

## SDK-Specific Notes

- Uses Rust idioms (Result types, ownership)
- Strong type safety with compile-time checks
- BCS serialization uses `aptos-bcs` crate
- Async runtime uses `tokio`
- Currently in active development (v2)

## How to Run Tests

```bash
cd tests/rust
cargo test --test specs     # Run all tests
make test-required          # Run only @required tests
make test-cryptography      # Run @cryptography tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `src/steps/*.rs`
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `cargo test --test specs` to verify
