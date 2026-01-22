# Java SDK Test Implementation Plan

> **Status**: In Progress (japtos v1.1.8 integrated)
> **Last Updated**: 2026-01-21
> **SDK**: [japtos](https://github.com/aptos-labs/japtos) (Aptos Java SDK) v1.1.8
> **BDD Framework**: Cucumber-JVM 7.15.0

## Overview

This document outlines the plan for implementing BDD test steps for the Aptos Java SDK (japtos)
against the shared Gherkin specifications in `../../features/`.

## Project Structure

```
tests/java/
├── pom.xml                          # Maven build configuration
├── Makefile                         # Build/test shortcuts
├── README.md                        # Setup instructions
├── PLAN.md                          # This file
└── src/test/java/com/aptos/specs/
    ├── RunCucumberTest.java         # JUnit 5 Cucumber runner
    ├── support/
    │   ├── World.java               # Test context (scenario state)
    │   └── Vectors.java             # Test vector loading utilities
    └── steps/
        ├── AddressSteps.java        # Address parsing/formatting
        ├── SerializationSteps.java  # BCS encoding/decoding
        ├── TypeTagSteps.java        # TypeTag parsing/formatting
        ├── CryptoSteps.java         # Ed25519, Secp256k1 keys/signing
        ├── HashingSteps.java        # SHA3-256, SHA2-256, HMAC
        ├── AccountSteps.java        # Account creation/management
        ├── AuthKeySteps.java        # Authentication key derivation
        ├── MnemonicSteps.java       # BIP-39 mnemonic derivation
        ├── TransactionSteps.java    # Raw/signed transactions
        ├── EntryFunctionSteps.java  # Entry function payloads
        ├── ClientSteps.java         # API client operations
        └── AdvancedSteps.java       # Multi-agent, fee-payer, etc.
```

## Implementation Phases

### Phase 1: Core Types (Required) ✅ In Progress

**Feature Files:**
- `features/01-core-types/address.feature` (22 scenarios)
- `features/01-core-types/serialization.feature` (18 scenarios)
- `features/01-core-types/type-tags.feature` (24 scenarios)

**Step Files Created:**
- [x] `AddressSteps.java` - Address parsing, formatting, comparison, BCS
- [x] `SerializationSteps.java` - BCS encoding for primitives, vectors, options
- [x] `TypeTagSteps.java` - TypeTag, MoveModuleId, MoveStructTag parsing

**Total Scenarios:** ~64

---

### Phase 2: Cryptography (Required) ✅ In Progress

**Feature Files:**
- `features/02-cryptography/ed25519.feature` (25 scenarios)
- `features/02-cryptography/hashing.feature` (20 scenarios)

**Step Files Created:**
- [x] `CryptoSteps.java` - Ed25519 key generation, signing, verification
- [x] `HashingSteps.java` - SHA3-256, SHA2-256, domain hashing, HashValue

**Total Scenarios:** ~45

---

### Phase 3: Account Management (Required) ✅ Complete

**Feature Files:**
- `features/03-account-management/authentication-key.feature` (17 scenarios)
- `features/03-account-management/single-key.feature` (28 scenarios)

**Step Files Created:**
- [x] `AuthKeySteps.java` - Authentication key derivation, scheme identifiers
- [x] `AccountSteps.java` - Account creation, properties, signing

**Total Scenarios:** ~45

---

### Phase 4: Transaction Building (Required) ✅ Complete

**Feature Files:**
- `features/04-transaction-building/entry-function.feature` (24 scenarios)
- `features/04-transaction-building/raw-transaction.feature` (21 scenarios)
- `features/04-transaction-building/signing.feature` (24 scenarios)

**Step Files Created:**
- [x] `EntryFunctionSteps.java` - Entry function payload creation, argument encoding
- [x] `RawTransactionSteps.java` - Raw transaction construction, signing message
- [x] `SigningSteps.java` - Transaction signing, authenticators, transaction hash

**Total Scenarios:** ~69

---

### Phase 5: API Clients (Required) ✅ In Progress

**Feature Files:**
- `features/05-api-clients/fullnode-api.feature` (25 scenarios)
- `features/05-api-clients/transaction-submission.feature` (28 scenarios)

**Step Files Created:**
- [x] `FullnodeApiSteps.java` - Client configuration, ledger info, account queries
- [x] `TransactionSubmissionSteps.java` - Transaction submission, waiting, simulation

**Total Scenarios:** ~53

---

### Phase 6: Error Handling (Required) ✅ In Progress

**Feature Files:**
- `features/06-advanced/error-handling.feature` (30 scenarios)

**Step Files Created:**
- [x] `ErrorHandlingSteps.java` - Error categories, VM status parsing, recovery patterns

**Total Scenarios:** ~30

---

### Phase 7: Preferred Features

**Feature Files:**
- `features/02-cryptography/secp256k1.feature` (19 scenarios)
- `features/03-account-management/mnemonic-derivation.feature` (29 scenarios)
- `features/05-api-clients/faucet.feature` (23 scenarios)
- `features/05-api-clients/gas-estimation.feature` (26 scenarios)
- `features/05-api-clients/view-functions.feature` (28 scenarios)
- `features/05-api-clients/retry.feature` (32 scenarios)
- `features/06-advanced/simulation.feature` (26 scenarios)

**Step Files to Create:**
- [ ] `MnemonicSteps.java`
- [ ] Additional methods in existing step files

**Total Scenarios:** ~183

---

### Phase 8: Optional/Advanced Features

**Feature Files:**
- `features/02-cryptography/secp256r1.feature` (26 scenarios)
- `features/02-cryptography/bls12381.feature` (35 scenarios)
- `features/04-transaction-building/script.feature` (25 scenarios)
- `features/05-api-clients/indexer.feature` (31 scenarios)
- `features/06-advanced/multi-agent.feature` (20 scenarios)
- `features/06-advanced/fee-payer.feature` (23 scenarios)
- `features/06-advanced/multi-signature.feature` (23 scenarios)
- `features/06-advanced/keyless.feature` (33 scenarios)
- `features/06-advanced/codegen.feature` (34 scenarios)

**Step Files to Create:**
- [ ] `AdvancedSteps.java`
- [ ] Additional methods in existing step files

**Total Scenarios:** ~250

---

## Dependencies

### Maven Dependencies (pom.xml)

```xml
<!-- Aptos Java SDK (japtos) - Official SDK from Maven Central -->
<dependency>
    <groupId>io.github.aptos-labs</groupId>
    <artifactId>japtos</artifactId>
    <version>1.1.8</version>
</dependency>

<!-- Cucumber BDD -->
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-java</artifactId>
    <version>7.15.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-junit-platform-engine</artifactId>
    <version>7.15.0</version>
    <scope>test</scope>
</dependency>

<!-- JUnit 5 -->
<dependency>
    <groupId>org.junit.platform</groupId>
    <artifactId>junit-platform-suite</artifactId>
    <version>1.10.1</version>
    <scope>test</scope>
</dependency>

<!-- JSON parsing for test vectors -->
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.10.1</version>
    <scope>test</scope>
</dependency>
```

## Configuration

### Java Version
- **Target**: Java 17+ (LTS)
- **Reason**: Modern features, long-term support, wide adoption

### Cucumber Configuration
- Feature files path: `../../features`
- Glue packages: `com.aptos.specs.steps`, `com.aptos.specs.support`
- Tags support for filtering: `@required`, `@preferred`, `@optional`

## Commands

```bash
# Run all tests
make test

# Run only required (P0) tests
make test-required

# Run specific category
make test-core-types
make test-cryptography
make test-transactions

# Dry run to check step definitions
make dry-run
```

## Progress Tracking

Update `FEATURE_COVERAGE.md` in the repository root as steps are implemented:
- Mark `[ ]` → `[x]` when steps are implemented and tests pass
- Mark `[ ]` → `[~]` for partial implementation or known issues

## Notes

### SDK API Compatibility
The japtos SDK v1.1.8 provides the following key classes:
- `AccountAddress` - 32-byte addresses with `fromHex()`, `toHexStringLong()`, `toHexStringShort()`
- `Ed25519Account` - Account generation with `generate()`, `fromPrivateKey()`
- `Ed25519PrivateKey`, `Ed25519PublicKey`, `Ed25519Signature` - Crypto primitives
- `AuthenticationKey` - Auth key derivation from public keys
- `HashValue` - 32-byte hash values
- `AptosClient`, `AptosConfig` - REST API client
- `HexUtils` - Hex encoding utilities

Step implementations should:
1. Follow japtos idioms and naming conventions
2. Document any SDK limitations that prevent implementing certain scenarios
3. Use Java best practices (try-with-resources, Optional, etc.)

### Error Handling
- Use Java exceptions appropriately
- Store errors in World context for assertion steps
- Follow Cucumber best practices for error scenarios

### Test Isolation
- Each scenario gets a fresh World instance
- No state leaks between scenarios
- Use `@Before` hooks for setup if needed
