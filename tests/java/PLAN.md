# Java SDK (japtos) BDD Test Implementation Plan

## Current Status: Phase 1 - Partial Implementation

Tests are compiling and 11 scenarios are passing.

## Coverage Progress

| Priority | Passing | Total | Progress |
|----------|---------|-------|----------|
| Required (P0) | 11 | 306 | 4% |
| Preferred (P1) | 0 | 183 | 0% |
| Optional (P2) | 0 | 250 | 0% |
| **Total** | **11** | **739** | **1%** |

## Phase 1: Core Types (In Progress)

### Address Handling
- [x] Parse short address with 0x prefix
- [x] Parse address without 0x prefix  
- [x] Parse full 64-character hex address
- [x] Parse uppercase/mixed case addresses
- [x] Format address to full hex
- [x] Format address to short string
- [ ] Reject invalid addresses (empty, non-hex, too long)
- [ ] Address constants (ZERO, ONE, etc.)
- [ ] Address equality
- [ ] BCS serialization/deserialization

### TypeTag Parsing
- [ ] Parse primitive types (u8, u64, bool, address, etc.)
- [ ] Parse vector types
- [ ] Parse struct types
- [ ] Handle invalid type strings

### BCS Serialization
- [ ] Serialize/deserialize primitives
- [ ] Serialize/deserialize strings
- [ ] Serialize/deserialize byte arrays
- [ ] Serialize/deserialize addresses

## Phase 2: Cryptography

### Ed25519
- [x] Generate random key pair
- [ ] Create key pair from bytes/hex
- [ ] Sign and verify messages
- [ ] Key serialization

### Hashing
- [ ] SHA3-256
- [ ] SHA2-256
- [ ] Domain-separated hashing

## Phase 3: Account Management

- [ ] Single-key account creation
- [ ] Account from private key
- [ ] Authentication key derivation
- [ ] Account address derivation

## Phase 4+: Advanced Features

- Transaction building
- API clients
- Multi-agent transactions
- Fee payer transactions
- And more...

## Running Tests

```bash
cd tests/java
mvn test                                    # All tests
mvn test -Dcucumber.filter.tags="@core-types"  # Core types only
mvn test -Dcucumber.filter.tags="@required"    # Required only
```

## Notes

- japtos SDK requires full 64-char hex for address parsing
- toHexString() doesn't include 0x prefix
- Step definitions are in `src/test/java/com/aptos/specs/steps/AllSteps.java`
