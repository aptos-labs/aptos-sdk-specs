# Python SDK Test Status

> **Last Updated:** 2026-01-22

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
| Required (P0) | 179 | 306 | 58% |
| Preferred (P1) | 0 | 183 | 0% |
| Optional (P2) | 0 | 250 | 0% |
| **Total** | 179 | 739 | 24% |

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
