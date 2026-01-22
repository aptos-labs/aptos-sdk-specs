# TypeScript SDK Test Status

> **Last Updated:** 2026-01-22

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `@aptos-labs/ts-sdk` |
| **Version Tested** | ^5.2.0 |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-ts-sdk |
| **Package Registry** | npm |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | 280 | 306 | 92% |
| Preferred (P1) | 150 | 183 | 82% |
| Optional (P2) | 80 | 250 | 32% |
| **Total** | 510 | 739 | 69% |

## Feature Availability

All features are available in this SDK. No features marked as N/A.

## Known Issues

Issues with tests that are marked `[~]` (partial):

| Scenario | Issue | Workaround |
|----------|-------|------------|
| transaction-submission #17 | VM error format differs from spec | Test adjusted to match SDK behavior |

## Missing Test Implementations

### Required (P0) - Priority

All required tests are implemented.

### Preferred (P1)

- `gas-estimation.feature` #19-20 - Historical gas prices, percentiles
- `retry.feature` #16, #23, #25, #28-31 - Circuit breaker, statistics, graceful degradation

### Optional (P2)

- `bls12381.feature` - All 35 scenarios (feature not in SDK)
- `codegen.feature` - All 34 scenarios (feature not in SDK)
- `script.feature` #8-12, #18, #21-22, #24 - Script compilation scenarios

## SDK-Specific Notes

- Most complete SDK implementation
- Primary reference implementation for specs
- Async/await patterns throughout
- Strong TypeScript type safety

## How to Run Tests

```bash
cd tests/typescript
bun install
bun test                    # Run all tests
bun run test:required       # Run only @required tests
bun run test:core-types     # Run @core-types tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `steps/*.steps.ts`
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `bun test` to verify
