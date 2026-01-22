# Python SDK Test Status

> **Last Updated:** 2026-01-22
> **Last Verified:** Not verified (pip not available in test environment)

## SDK Information

| Property | Value |
|----------|-------|
| **Package** | `aptos-sdk` |
| **Version Tested** | >=0.11.0 |
| **Publisher** | aptos-labs |
| **Repository** | https://github.com/aptos-labs/aptos-python-sdk |
| **Package Registry** | PyPI |

## Coverage Summary

| Priority | Passing | Total | Percentage |
|----------|---------|-------|------------|
| Required (P0) | N/A | 370 | N/A |
| Preferred (P1) | N/A | 183 | N/A |
| Optional (P2) | N/A | 250 | N/A |
| **Total** | N/A | 803 | N/A |

> **Note:** Tests could not be run due to missing Python/pip in test environment.
> Install dependencies with `pip install -r requirements.txt` then run `behave`.

## Feature Availability

Features that are **not available** in this SDK (marked `[-]` in coverage matrix):

| Feature | Reason | Tracking Issue |
|---------|--------|----------------|
| secp256k1 | Not implemented in SDK | - |
| secp256r1 | Not implemented in SDK | - |
| bls12381 | Not implemented in SDK | - |

## Known Issues

No partial implementations currently tracked.

## Missing Test Implementations

### Required (P0) - Priority

Tests in progress. Key areas:
- Core types (address, serialization, type-tags)
- Cryptography (ed25519, hashing)
- Account management
- Transaction building
- API clients

### Preferred (P1)

- All preferred features (tests not yet implemented)

### Optional (P2)

- All optional features (tests not yet implemented)

## SDK-Specific Notes

- Uses Python asyncio for async operations
- Uses Behave for BDD testing
- PyNaCl for Ed25519 cryptography
- Strong typing with type hints
- Python 3.8+ required

## How to Run Tests

```bash
cd tests/python
pip install -r requirements.txt
behave                      # Run all tests
behave --tags=@required     # Run only @required tests
behave --tags=@core-types   # Run @core-types tests
```

## Contributing

To add tests for this SDK:

1. Add step definitions in `steps/*.py`
2. Update `FEATURE_COVERAGE.md` with test status
3. Update this file's coverage summary
4. Run `behave` to verify
