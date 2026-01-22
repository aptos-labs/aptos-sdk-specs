# Kotlin SDK (Kaptos) Test Implementation Plan

> **Status**: Infrastructure Complete, SDK Limitations (0.1.2-beta)
> **Last Updated**: 2026-01-22
> **SDK**: [Kaptos](https://github.com/mcxross/kaptos) (Aptos Kotlin Multiplatform SDK)
> **Maven**: `xyz.mcxross.kaptos:kaptos-jvm:0.1.2-beta`
> **BDD Framework**: Cucumber-JVM with Kotlin
>
> **Note**: The Kaptos SDK is in beta (0.1.2-beta) with limited API exposure.
> Many step definitions are stubs that will be implemented as the SDK matures.

## Overview

This document outlines the plan for implementing BDD test steps for the Aptos Kotlin SDK (Kaptos)
against the shared Gherkin specifications in `../../features/`.

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
    │   └── Vectors.kt               # Test vector loading utilities
    └── steps/
        ├── AddressSteps.kt          # Address parsing/formatting
        ├── SerializationSteps.kt    # BCS encoding/decoding
        ├── TypeTagSteps.kt          # TypeTag parsing/formatting
        ├── CryptoSteps.kt           # Ed25519, Secp256k1 keys/signing
        ├── HashingSteps.kt          # SHA3-256, SHA2-256, HMAC
        ├── AccountSteps.kt          # Account creation/management
        ├── AuthKeySteps.kt          # Authentication key derivation
        ├── MnemonicSteps.kt         # BIP-39 mnemonic derivation
        ├── TransactionSteps.kt      # Raw/signed transactions
        ├── EntryFunctionSteps.kt    # Entry function payloads
        ├── ClientSteps.kt           # API client operations
        └── AdvancedSteps.kt         # Multi-agent, fee-payer, etc.
```

## Implementation Phases

### Phase 1: Project Setup ✅

- [x] Create directory structure
- [x] Create `build.gradle.kts` with dependencies
- [x] Create `settings.gradle.kts`
- [x] Create `World.kt` context class
- [x] Create `Vectors.kt` for test vector loading
- [x] Create `RunCucumberTest.kt` runner
- [x] Create `Makefile` with build/test commands
- [x] Create `.gitignore`
- [x] Create `README.md`
- [x] Verify Kaptos SDK can be resolved (kaptos-jvm:0.1.2-beta)
- [x] Create `CommonSteps.kt` for shared step definitions
- [x] Create `Hooks.kt` for test lifecycle management

---

### Phase 2: Core Types (Required)

**Feature Files:**
- `features/01-core-types/address.feature` (22 scenarios)
- `features/01-core-types/serialization.feature` (18 scenarios)
- `features/01-core-types/type-tags.feature` (24 scenarios)

**Step Files to Create:**
- [x] `AddressSteps.kt` (Partial - AccountAddress.fromString() works)
- [~] `SerializationSteps.kt` (Manual BCS impl - SDK doesn't expose Bcs class)
- [~] `TypeTagSteps.kt` (Manual parsing - TypeTag.fromString() signature differs)

**Total Scenarios:** ~64
**SDK Limitations:** No direct `Bcs` class access; `TypeTag` API differs from spec

---

### Phase 3: Cryptography (Required)

**Feature Files:**
- `features/02-cryptography/ed25519.feature` (25 scenarios)
- `features/02-cryptography/hashing.feature` (20 scenarios)

**Step Files to Create:**
- [~] `CryptoSteps.kt` (Limited - Account.generate() works, no private key access)
- [x] `HashingSteps.kt` (JVM stdlib - SHA3-256, SHA2-256, HMAC)

**Total Scenarios:** ~45
**SDK Limitations:** No `Ed25519PrivateKey`, `Secp256k1` classes; no signature verification

---

### Phase 4: Account Management (Required)

**Feature Files:**
- `features/03-account-management/authentication-key.feature` (17 scenarios)
- `features/03-account-management/single-key.feature` (28 scenarios)

**Step Files to Create:**
- [~] `AccountSteps.kt` (Limited - Account.generate() works, no auth key derivation)
- [~] `AuthKeySteps.kt` - merged into AccountSteps.kt

**Total Scenarios:** ~45
**SDK Limitations:** No `AuthenticationKey` class; no AIP-80 format support

---

### Phase 5: Transaction Building (Required)

**Feature Files:**
- `features/04-transaction-building/entry-function.feature` (24 scenarios)
- `features/04-transaction-building/raw-transaction.feature` (21 scenarios)
- `features/04-transaction-building/signing.feature` (24 scenarios)

**Step Files to Create:**
- [~] `TransactionSteps.kt` (Stubs - no low-level tx primitives exposed)
- [~] `EntryFunctionSteps.kt` - merged into TransactionSteps.kt

**Total Scenarios:** ~69
**SDK Limitations:** No `RawTransaction`, `SignedTransaction`, `EntryFunction` constructors exposed

---

### Phase 6: API Clients (Required)

**Feature Files:**
- `features/05-api-clients/fullnode-api.feature` (25 scenarios)
- `features/05-api-clients/transaction-submission.feature` (28 scenarios)

**Step Files to Create:**
- [ ] `ClientSteps.kt`

**Total Scenarios:** ~53

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
- [ ] `MnemonicSteps.kt`
- [ ] Additional methods in existing step files

**Total Scenarios:** ~183

---

### Phase 8: Optional/Advanced Features

**Feature Files:**
- `features/02-cryptography/secp256r1.feature` (26 scenarios)
- `features/02-cryptography/bls12381.feature` (35 scenarios)
- `features/04-transaction-building/script.feature` (25 scenarios)
- `features/05-api-clients/indexer.feature` (31 scenarios)
- `features/06-advanced/error-handling.feature` (30 scenarios)
- `features/06-advanced/multi-agent.feature` (20 scenarios)
- `features/06-advanced/fee-payer.feature` (23 scenarios)
- `features/06-advanced/multi-signature.feature` (23 scenarios)
- `features/06-advanced/keyless.feature` (33 scenarios)
- `features/06-advanced/codegen.feature` (34 scenarios)

**Step Files to Create:**
- [ ] `AdvancedSteps.kt`
- [ ] Additional methods in existing step files

**Total Scenarios:** ~250

---

## Current Test Results

As of 2026-01-22:
- **Total Tests:** 1616
- **Passed:** 176 (58% of required scenarios)
- **Failed:** 1440 (mostly undefined steps for preferred/optional features)

The test infrastructure is complete, but the Kaptos SDK (0.1.2-beta) doesn't expose
the low-level primitives needed for most spec scenarios. Implementation will improve
as the SDK matures.

## Dependencies

### Gradle Dependencies (build.gradle.kts)

```kotlin
dependencies {
    // Kaptos SDK - published to Maven Central (JVM variant for pure JVM testing)
    implementation("xyz.mcxross.kaptos:kaptos-jvm:0.1.2-beta")  // Beta version
    
    // Cucumber BDD
    testImplementation("io.cucumber:cucumber-java:7.15.0")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:7.15.0")
    testImplementation("io.cucumber:cucumber-picocontainer:7.15.0")
    
    // JUnit 5
    testImplementation("org.junit.platform:junit-platform-suite:1.10.1")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")
    
    // JSON parsing for test vectors
    testImplementation("com.google.code.gson:gson:2.10.1")
    
    // Kotlin coroutines (if Kaptos uses suspend functions)
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    
    // Assertions
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
}
```

## Configuration

### Kotlin Version
- **Target**: Kotlin 1.9+ with JVM 17
- **Reason**: Latest stable Kotlin with modern JVM support

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

# Build only
make build

# Clean
make clean
```

## Step Definition Pattern

Cucumber-JVM works with Kotlin using standard annotations:

```kotlin
package com.aptos.specs.steps

import io.cucumber.java.en.Given
import io.cucumber.java.en.When
import io.cucumber.java.en.Then
import com.aptos.specs.support.World

class AddressSteps(private val world: World) {
    
    @Given("a hex string {string}")
    fun givenAHexString(hex: String) {
        world.hexString = hex
    }
    
    @When("I parse it as an AccountAddress")
    fun whenIParseItAsAnAccountAddress() {
        try {
            world.address = AccountAddress.fromString(world.hexString!!)
            world.clearError()
        } catch (e: Exception) {
            world.setError(e)
        }
    }
    
    @Then("the parsing should succeed")
    fun thenTheParsingShouldSucceed() {
        world.error shouldBe null
        world.address shouldNotBe null
    }
}
```

### World Context Class

```kotlin
package com.aptos.specs.support

class World {
    // String/bytes for input
    var hexString: String? = null
    var bytes: ByteArray? = null
    
    // Parsed objects
    var address: AccountAddress? = null
    var privateKey: Ed25519PrivateKey? = null
    var publicKey: Ed25519PublicKey? = null
    var signature: Ed25519Signature? = null
    var keyPair: Ed25519KeyPair? = null
    
    // Transaction objects
    var rawTransaction: RawTransaction? = null
    var signedTransaction: SignedTransaction? = null
    var entryFunction: EntryFunction? = null
    
    // Error handling
    var error: Throwable? = null
    
    fun setError(e: Throwable) {
        error = e
    }
    
    fun clearError() {
        error = null
    }
    
    fun reset() {
        hexString = null
        bytes = null
        address = null
        privateKey = null
        publicKey = null
        signature = null
        keyPair = null
        rawTransaction = null
        signedTransaction = null
        entryFunction = null
        error = null
    }
}
```

### Handling Coroutines

If Kaptos uses Kotlin coroutines (suspend functions), use `runBlocking` in step definitions:

```kotlin
@When("I submit the transaction")
fun whenISubmitTheTransaction() = runBlocking {
    try {
        world.submittedTxHash = world.client!!.submitTransaction(world.signedTransaction!!)
        world.clearError()
    } catch (e: Exception) {
        world.setError(e)
    }
}
```

## Progress Tracking

Update `FEATURE_COVERAGE.md` in the repository root as steps are implemented:
- Mark `[ ]` → `[x]` when steps are implemented and tests pass
- Mark `[ ]` → `[~]` for partial implementation or known issues

## Notes

### SDK API Compatibility
The Kaptos SDK API may differ from other SDKs. Step implementations should:
1. Follow Kotlin idioms (null safety, data classes, extension functions)
2. Document any SDK limitations that prevent implementing certain scenarios
3. Use Kotlin best practices (sealed classes for errors, coroutines for async)

### Kotlin-Specific Considerations
- Use `?.let {}` for null-safe operations
- Use `runCatching {}` for error handling
- Use Kotest matchers for expressive assertions
- Handle suspend functions appropriately with `runBlocking` or coroutine test utilities

### Error Handling
- Use Kotlin's `Result` type or exceptions as appropriate
- Store errors in World context for assertion steps
- Follow Cucumber best practices for error scenarios

### Test Isolation
- Each scenario gets a fresh World instance (via PicoContainer)
- No state leaks between scenarios
- Use `@Before` hooks for setup if needed

## References

- [Kaptos SDK Repository](https://github.com/aspect-labs/kaptos) (verify actual location)
- [Cucumber-JVM Documentation](https://cucumber.io/docs/cucumber/)
- [Cucumber with Kotlin](https://cucumber.io/docs/installation/kotlin/)
- [Kotest Assertions](https://kotest.io/docs/assertions/assertions.html)
- [Kotlin Coroutines Testing](https://kotlinlang.org/docs/coroutines-testing.html)
