# Kotlin SDK Test Status

> **Last Updated:** 2026-01-22

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `xyz.mcxross.kaptos:kaptos-jvm` |
| **Version Tested** | 0.1.2-beta |
| **Publisher** | mcxross (community) |
| **Repository** | https://github.com/mcxross/kaptos |
| **Package Registry** | Maven Central |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | 176 | 306 | 58% |
| Preferred (P1) | 0 | 183 | 0% |
| Optional (P2) | 0 | 250 | 0% |
| **Total** | 176 | 739 | 24% |

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

Tests not yet fully tracked in coverage matrix. Key gaps likely include:
- Advanced cryptography features
- Some API client features

### Preferred (P1)

- All preferred features (tests not yet implemented)

### Optional (P2)

- All optional features (tests not yet implemented)

## SDK-Specific Notes

- **Community SDK** - not maintained by aptos-labs
- Kotlin Multiplatform SDK (JVM artifact used for testing)
- Uses Kotlin coroutines for async operations
- Beta status - API may change
- Uses Kotest for assertions

## How to Run Tests

```bash
cd tests/kotlin
./gradlew test              # Run all tests
./gradlew testRequired      # Run only @required tests
./gradlew testCoreTypes     # Run @core-types tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `src/test/kotlin/com/aptos/specs/steps/`
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `./gradlew test` to verify

## Community SDK Note

This is a community-maintained SDK. For issues with the SDK itself (not the tests),
please file issues at https://github.com/mcxross/kaptos
