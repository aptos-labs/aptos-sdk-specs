# Kotlin SDK Test Implementation Plan

> **Status**: Infrastructure Complete, SDK Replaced with Official aptos-labs SDK
> **Last Updated**: 2026-02-23
> **SDK**: [aptos-kotlin-sdk](https://github.com/aptos-labs/aptos-kotlin-sdk)
> **Maven**: `com.aptos:core:0.1.0`
> **BDD Framework**: Cucumber-JVM with Kotlin

## Overview

This document outlines the plan for implementing BDD test steps for the official Aptos Kotlin SDK
against the shared Gherkin specifications in `../../features/`.

The SDK was migrated from the community `kaptos` SDK (mcxross) to the official `aptos-kotlin-sdk`
(aptos-labs) on 2026-02-23.

## Project Structure

```
tests/kotlin/
├── build.gradle.kts                 # Gradle build configuration (Kotlin DSL)
├── settings.gradle.kts              # Gradle settings
├── gradle.properties                # Gradle properties
├── Makefile                         # Build/test shortcuts
├── README.md                        # Setup instructions
├── PLAN.md                          # This file
└── src/test/kotlin/com/aptos/specs/
    ├── RunCucumberTest.kt           # JUnit 5 Cucumber runner
    ├── support/
    │   ├── World.kt                 # Test context (scenario state)
    │   ├── Hooks.kt                 # Lifecycle hooks
    │   └── Vectors.kt               # Test vector loading utilities
    └── steps/
        ├── AddressSteps.kt          # Address parsing/formatting
        ├── SerializationSteps.kt    # BCS encoding/decoding
        ├── TypeTagSteps.kt          # TypeTag parsing/formatting
        ├── CryptoSteps.kt           # Ed25519, Secp256k1 keys/signing
        ├── HashingSteps.kt          # SHA3-256, SHA2-256, HMAC
        ├── AccountSteps.kt          # Account creation/management
        ├── TransactionSteps.kt      # Transaction building/signing
        └── CommonSteps.kt           # Shared step definitions
```

## SDK Migration (2026-02-23)

### Old SDK (kaptos)
- **Package**: `xyz.mcxross.kaptos:kaptos-jvm:0.1.2-beta`
- **Publisher**: mcxross (community)
- **Limitations**: No private key access, no Secp256k1, no AuthenticationKey

### New SDK (aptos-kotlin-sdk)
- **Package**: `com.aptos:core:0.1.0`
- **Publisher**: aptos-labs (official)
- **Improvements**: Full Ed25519/Secp256k1, AuthenticationKey, BCS, Mnemonic

### Key API Changes
- `AccountAddress.fromString()` → `AccountAddress.fromHex()` / `fromHexRelaxed()`
- `Account.generate()` → `Ed25519Account.generate()`
- `account.accountAddress` → `account.address`
- `account.publicKey` → `account.publicKeyBytes`
- `account.sign(HexInput.fromByteArray())` → `account.sign(byteArray)`
- New: `Ed25519.PrivateKey`, `Ed25519.PublicKey`, `Secp256k1Account`
- New: `AuthenticationKey.fromEd25519()`, `AuthenticationKey.derivedAddress()`

## Implementation Phases

### Phase 1: Project Setup ✅

- [x] Create directory structure
- [x] Create `build.gradle.kts` with dependencies
- [x] Create `World.kt` context class
- [x] Create `Vectors.kt` for test vector loading
- [x] Create `RunCucumberTest.kt` runner
- [x] Create `Makefile` with build/test commands
- [x] Migrate from kaptos to aptos-kotlin-sdk

---

### Phase 2: Core Types ✅

**Feature Files:**
- `features/01-core-types/address.feature`
- `features/01-core-types/serialization.feature`
- `features/01-core-types/type-tags.feature`

**Step Files:**
- [x] `AddressSteps.kt` - Uses `AccountAddress.fromHex()/fromHexRelaxed()`
- [x] `SerializationSteps.kt` - Manual BCS + SDK AccountAddress
- [x] `TypeTagSteps.kt` - Manual TypeTag parsing

---

### Phase 3: Cryptography ✅

**Feature Files:**
- `features/02-cryptography/ed25519.feature`
- `features/02-cryptography/secp256k1.feature`
- `features/02-cryptography/hashing.feature`

**Step Files:**
- [x] `CryptoSteps.kt` - Ed25519Account, Secp256k1Account, signing, verification
- [x] `HashingSteps.kt` - JVM stdlib SHA3-256, SHA2-256, HMAC

---

### Phase 4: Account Management ✅

**Feature Files:**
- `features/03-account-management/authentication-key.feature`
- `features/03-account-management/single-key.feature`

**Step Files:**
- [x] `AccountSteps.kt` - Ed25519Account, Secp256k1Account, AuthenticationKey

---

### Phase 5: Transaction Building (Partial)

**Feature Files:**
- `features/04-transaction-building/entry-function.feature`
- `features/04-transaction-building/raw-transaction.feature`
- `features/04-transaction-building/signing.feature`

**Step Files:**
- [~] `TransactionSteps.kt` - Basic structure, needs full SDK integration

---

### Phase 6: API Clients (Pending)

- [ ] Fullnode API client steps
- [ ] Transaction submission steps

### Phase 7: Advanced Features (Pending)

- [ ] Multi-agent transactions
- [ ] Fee payer transactions
- [ ] Mnemonic derivation steps
- [ ] Keyless authentication steps

## Dependencies

### Gradle Dependencies (build.gradle.kts)

```kotlin
dependencies {
    // Official Aptos Kotlin SDK (aptos-labs)
    implementation("com.aptos:core:0.1.0")

    // Cucumber BDD
    testImplementation("io.cucumber:cucumber-java:7.15.0")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:7.15.0")
    testImplementation("io.cucumber:cucumber-picocontainer:7.15.0")

    // JUnit 5
    testImplementation("org.junit.platform:junit-platform-suite:1.10.1")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")

    // JSON parsing for test vectors
    testImplementation("com.google.code.gson:gson:2.10.1")

    // Kotlin coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")

    // Assertions
    testImplementation("io.kotest:kotest-assertions-core:5.9.1")
}
```

## Commands

```bash
make test              # Run all tests
make test-required     # Run only required (P0) tests
make test-core-types   # Run specific category
make test-cryptography
make test-transactions
make dry-run           # Check step definitions
make build             # Build only
make clean             # Clean
```

## References

- [Aptos Kotlin SDK](https://github.com/aptos-labs/aptos-kotlin-sdk)
- [Cucumber-JVM Documentation](https://cucumber.io/docs/cucumber/)
- [Kotest Assertions](https://kotest.io/docs/assertions/assertions.html)
