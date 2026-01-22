# .NET SDK Test Status

> **Last Updated:** 2026-01-22

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `Aptos` |
| **Version Tested** | 0.0.x-beta |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-dotnet-sdk |
| **Package Registry** | NuGet |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | 95 | 306 | 31% |
| Preferred (P1) | 26 | 183 | 14% |
| Optional (P2) | 10 | 250 | 4% |
| **Total** | 131 | 739 | 18% |

## Feature Availability

Features that are **not available** in this SDK (marked `[-]` in coverage matrix):

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| secp256k1 | Not yet implemented | - |
| secp256r1 | Not yet implemented | - |
| bls12381 | Not yet implemented | - |
| mnemonic-derivation | Not yet implemented | - |

## Known Issues

No partial implementations currently tracked.

## Missing Test Implementations

### Required (P0) - Priority

Beta SDK with core features in progress:
- Core types partially implemented
- Cryptography basics implemented
- Transaction building in progress
- API clients in progress

### Preferred (P1)

- Most preferred features not yet implemented

### Optional (P2)

- All optional features not yet implemented

## SDK-Specific Notes

- **Beta SDK** - API may change
- .NET 10.0 target framework
- Uses Reqnroll (SpecFlow successor) for BDD testing
- Uses BouncyCastle for cryptography
- NUnit test framework
- FluentAssertions for assertions

## How to Run Tests

```bash
cd tests/dotnet
dotnet restore
dotnet test                 # Run all tests
dotnet test --filter "Category=required"  # Run only @required tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `Steps/*.cs`
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `dotnet test` to verify

## Beta SDK Note

This SDK is in beta. The API may change significantly between versions.
Check the repository for the latest documentation and breaking changes.
