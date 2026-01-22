# Java SDK (japtos) Test Status

## Current Status: PARTIALLY WORKING

The Java SDK tests are now compiling and running. Initial step definitions have been implemented
for core address parsing, formatting, and basic Ed25519 cryptography.

## Coverage Summary

| Category | Status |
|----------|--------|
| Required (P0) | 11/306 (4%) |
| Preferred (P1) | 0/183 (0%) |
| Optional (P2) | 0/250 (0%) |
| **Total** | **11/739** |

## Passing Tests

### Core Types (Address)
- Parse hex address without 0x prefix
- Parse full 64-character hex address
- Parse various valid address formats (6 scenarios)
- Parse uppercase hex address
- Parse mixed case hex address

### Cryptography (Ed25519)
- Generate random Ed25519 key pair

## SDK Details

- **Package**: `io.github.aptos-labs:japtos`
- **Version**: 1.1.8
- **Repository**: [aptos-labs/japtos](https://github.com/aptos-labs/japtos)

## API Notes

The japtos SDK has some differences from the TypeScript SDK:

1. **Address Parsing**: `AccountAddress.fromHex()` requires full 64-character hex strings.
   Short addresses like "0x1" need to be padded before parsing.

2. **Hex Output**: `toHexString()` returns hex without the "0x" prefix.

3. **Package Structure**:
   - `com.aptoslabs.japtos.core.AccountAddress` - Account addresses
   - `com.aptoslabs.japtos.core.AuthenticationKey` - Auth key derivation
   - `com.aptoslabs.japtos.core.crypto.*` - Ed25519 keys and signatures
   - `com.aptoslabs.japtos.account.Ed25519Account` - Account abstraction
   - `com.aptoslabs.japtos.bcs.*` - BCS serialization
   - `com.aptoslabs.japtos.utils.*` - Hex utilities

## Next Steps

1. Implement step definitions for more address scenarios (invalid inputs, BCS)
2. Add TypeTag parsing step definitions
3. Add BCS serialization step definitions
4. Implement account management steps
5. Add Ed25519 signing/verification steps

## Running Tests

```bash
cd tests/java
mvn test

# Run only core-types
mvn test -Dcucumber.filter.tags="@core-types"

# Run only required tests
mvn test -Dcucumber.filter.tags="@required"
```

## Last Updated

2026-01-22
