# Go SDK Test Status

> **Last Updated:** 2026-01-22
> **Last Verified:** 2026-01-22 (see TO_FIX.md)

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `github.com/aptos-labs/aptos-go-sdk` |
| **Version Tested** | v1.11.0 |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-go-sdk |
| **Package Registry** | Go modules |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | 212 | 370 | 57% |
| Preferred (P1) | 20 | 183 | 11% |
| Optional (P2) | 0 | 250 | 0% |
| **Total** | 232 | 803 | 29% |

> **Note:** 8 failures (4 SDK limitations, 4 network-dependent). 154 scenarios undefined.

## Feature Availability

Features that are **not available** in this SDK (marked `[-]` in coverage matrix):

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| secp256k1 | Not implemented in SDK | - |
| secp256r1 | Not implemented in SDK | - |
| bls12381 | Not implemented in SDK | - |
| mnemonic-derivation | Not implemented in SDK | - |
| AIP-80 key format | Not implemented in SDK | - |
| simulation | Not exposed in SDK API | - |
| multi-agent | Not implemented in SDK | - |
| fee-payer | Not implemented in SDK | - |
| multi-signature | Not implemented in SDK | - |
| keyless | Not implemented in SDK | - |

## Known Issues

No partial implementations currently tracked.

## Missing Test Implementations

### Required (P0) - Priority

- `serialization.feature` - 18 scenarios (BCS primitives not exposed in SDK API)
- `type-tags.feature` - 24 scenarios (TypeTag parsing not exposed)
- `hashing.feature` #9-20 - Domain separation, HashValue wrapper
- `ed25519.feature` #24-25 - Private key zeroization/debug hiding
- `authentication-key.feature` #5-8, #15 - Secp256k1-related
- `single-key.feature` #6-7, #15-20, #22, #26-28 - AIP-80, Secp256k1
- `entry-function.feature` #20-21 - Optional arguments
- `raw-transaction.feature` #15-16, #19 - Expiration helpers
- `signing.feature` #15-18, #23-24 - Secp256k1 signing
- `fullnode-api.feature` #2-3, #14, #21-22, #25 - Various API features
- `transaction-submission.feature` #7, #9, #12, #15-21, #25-27 - Simulation, waiting
- `error-handling.feature` - Most scenarios

### Preferred (P1)

- All faucet, gas-estimation, view-functions, retry, simulation features

### Optional (P2)

- All optional features (feature not available in SDK)

## SDK-Specific Notes

- Focuses on core transaction building and submission
- Uses Go idioms (error returns, no exceptions)
- BCS serialization happens internally, not exposed for general use
- Limited advanced feature support compared to TypeScript SDK

## How to Run Tests

```bash
cd tests/go
go mod download
make test                   # Run all tests
make test-required          # Run only @required tests
make test-cryptography      # Run @cryptography tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `*_steps.go` files
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `make test` to verify
