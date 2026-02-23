# Aptos Kotlin SDK BDD Tests

This directory contains BDD (Behavior-Driven Development) tests for the official
[Aptos Kotlin SDK](https://github.com/aptos-labs/aptos-kotlin-sdk), using Cucumber-JVM.

## Prerequisites

- **JDK 11+** - Required for building and running tests
- **Gradle 8.x** - Build tool (wrapper included)
- **Aptos Kotlin SDK** - The SDK must be available (see Dependencies section)

## Quick Start

```bash
# Install Gradle wrapper (if not present)
make wrapper

# Run all tests
make test

# Run only required (P0) tests
make test-required

# Run specific category
make test-core-types
make test-cryptography
```

## Project Structure

```
tests/kotlin/
├── build.gradle.kts                 # Gradle build configuration
├── settings.gradle.kts              # Gradle settings
├── Makefile                         # Build/test shortcuts
├── PLAN.md                          # Implementation plan
├── README.md                        # This file
└── src/test/kotlin/com/aptos/specs/
    ├── RunCucumberTest.kt           # JUnit 5 Cucumber runner
    ├── support/
    │   ├── World.kt                 # Test context
    │   ├── Hooks.kt                 # Lifecycle hooks
    │   └── Vectors.kt               # Test vector loading
    └── steps/
        ├── AddressSteps.kt          # Address operations
        ├── CryptoSteps.kt           # Ed25519/Secp256k1 crypto
        ├── AccountSteps.kt          # Account management
        ├── SerializationSteps.kt    # BCS serialization
        ├── TypeTagSteps.kt          # TypeTag parsing
        ├── TransactionSteps.kt      # Transaction building
        ├── HashingSteps.kt          # Hashing operations
        └── CommonSteps.kt           # Shared steps
```

## Available Commands

| Command                  | Description                            |
| ------------------------ | -------------------------------------- |
| `make test`              | Run all tests                          |
| `make test-required`     | Run only @required (P0) tests          |
| `make test-preferred`    | Run only @preferred (P1) tests         |
| `make test-core-types`   | Run only @core-types tests             |
| `make test-cryptography` | Run only @cryptography tests           |
| `make test-transactions` | Run only @transactions tests           |
| `make dry-run`           | Check step definitions without running |
| `make clean`             | Remove build artifacts                 |
| `make report`            | Open HTML test report                  |

## Dependencies

The official Aptos Kotlin SDK is used. The current dependency in `build.gradle.kts`:

```kotlin
// Official Aptos Kotlin SDK (aptos-labs)
implementation("com.aptos:core:0.1.0")
```

## Configuration

### Cucumber Options

Tests use Cucumber-JVM with the following configuration:

- **Feature files**: `../../features/` (shared Gherkin specs)
- **Glue packages**: `com.aptos.specs.steps`, `com.aptos.specs.support`
- **Reports**: HTML and JSON in `build/reports/cucumber/`

### Tag Filtering

Run tests with specific tags:

```bash
# Single tag
./gradlew test -Dcucumber.filter.tags="@required"

# Multiple tags (AND)
./gradlew test -Dcucumber.filter.tags="@required and @core-types"

# Multiple tags (OR)
./gradlew test -Dcucumber.filter.tags="@required or @preferred"

# Exclude tags
./gradlew test -Dcucumber.filter.tags="not @network"
```

## Writing Step Definitions

Step definitions use Cucumber annotations with Kotlin:

```kotlin
package com.aptos.specs.steps

import io.cucumber.java.en.Given
import io.cucumber.java.en.When
import io.cucumber.java.en.Then
import com.aptos.specs.support.World
import com.aptos.core.types.AccountAddress
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe

class AddressSteps(private val world: World) {

    @Given("a hex string {string}")
    fun givenAHexString(hex: String) {
        world.hexString = hex
    }

    @When("I parse it as an AccountAddress")
    fun parseAccountAddress() {
        runCatching {
            world.address = AccountAddress.fromHex(world.hexString!!)
        }.onFailure {
            world.error = it
        }
    }

    @Then("the parsing should succeed")
    fun parsingShouldSucceed() {
        world.error shouldBe null
        world.address shouldNotBe null
    }
}
```

## Test Reports

After running tests, reports are available at:

- **HTML Report**: `build/reports/cucumber/cucumber.html`
- **JSON Report**: `build/reports/cucumber/cucumber.json`

## Current Status

- **SDK Version:** 0.1.0 (official aptos-labs)
- **Test Infrastructure:** ✅ Complete
- **Step Definitions:** Updated for new SDK API

### SDK Features Available

- AccountAddress parsing (fromHex/fromHexRelaxed) and formatting
- Ed25519 key generation, signing, verification
- Secp256k1 key generation, signing, verification
- BCS serialization and deserialization
- AuthenticationKey derivation
- BIP-39 mnemonic and HD key derivation
- TypeTag parsing and formatting
- Transaction building primitives

## References

- [Aptos Kotlin SDK](https://github.com/aptos-labs/aptos-kotlin-sdk)
- [Cucumber-JVM Documentation](https://cucumber.io/docs/cucumber/)
- [Kotest Assertions](https://kotest.io/docs/assertions/assertions.html)
- [Feature Specifications](../../features/)
- [Test Vectors](../../test-vectors/)
