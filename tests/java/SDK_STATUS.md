# Java SDK Test Status

> **Last Updated:** 2026-01-22

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `io.github.aptos-labs:japtos` |
| **Version Tested** | 1.1.8 |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-java-sdk |
| **Package Registry** | Maven Central |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | 306 | 306 | 100% |
| Preferred (P1) | 0 | 183 | 0% |
| Optional (P2) | 0 | 250 | 0% |
| **Total** | 306 | 739 | 41% |

## Feature Availability

Features that are **not available** in this SDK (marked `[-]` in coverage matrix):

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| secp256k1 | Not implemented in SDK | - |
| secp256r1 | Not implemented in SDK | - |
| bls12381 | Not implemented in SDK | - |
| mnemonic-derivation | Not implemented in SDK | - |

## Known Issues

No partial implementations currently tracked.

## Missing Test Implementations

### Required (P0) - Priority

**All required tests are passing!** This is the only SDK with 100% required coverage.

### Preferred (P1)

- `mnemonic-derivation.feature` - All 29 scenarios (feature not in SDK)
- `secp256k1.feature` - All 19 scenarios (feature not in SDK)
- `faucet.feature` - All 23 scenarios (tests not implemented)
- `gas-estimation.feature` - All 26 scenarios (tests not implemented)
- `view-functions.feature` - All 28 scenarios (tests not implemented)
- `retry.feature` - All 32 scenarios (tests not implemented)
- `simulation.feature` - All 26 scenarios (tests not implemented)

### Optional (P2)

- All optional features (tests not implemented)

## SDK-Specific Notes

- 100% required feature coverage - most complete for P0
- Uses Java idioms (exceptions, Builder pattern)
- JDK 17+ required
- Uses Cucumber-JVM for BDD testing
- Strong focus on core functionality

## How to Run Tests

```bash
cd tests/java
mvn dependency:resolve      # Install dependencies
make test                   # Run all tests
make test-required          # Run only @required tests
make test-core-types        # Run @core-types tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `src/test/java/com/aptos/specs/steps/`
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `mvn test` to verify
