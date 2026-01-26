# Aptos Kotlin SDK (Kaptos) BDD Tests

This directory contains BDD (Behavior-Driven Development) tests for the
[Kaptos](https://github.com/mcxross/kaptos) Kotlin Multiplatform SDK, using Cucumber-JVM.

> **Note:** The Kaptos SDK is currently in beta (0.1.2-beta) with limited API exposure. Many step
> definitions are stubs that will be implemented as the SDK matures. The test infrastructure is
> complete and ready for future SDK updates.

## Prerequisites

- **JDK 17+** - Required for building and running tests
- **Gradle 8.x** - Build tool (wrapper included)
- **Kaptos SDK** - The Kotlin SDK must be available (see Dependencies section)

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
    │   └── Vectors.kt               # Test vector loading
    └── steps/
        ├── AddressSteps.kt          # Address operations
        ├── SerializationSteps.kt    # BCS serialization
        └── ...                      # Other step definitions
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

The Kaptos SDK is published to Maven Central. The current dependency in `build.gradle.kts`:

```kotlin
// Kaptos SDK - JVM variant for pure JVM testing
implementation("xyz.mcxross.kaptos:kaptos-jvm:0.1.2-beta")
```

**Note:** The SDK is in beta. Check
[Maven Central](https://search.maven.org/search?q=g:xyz.mcxross.kaptos) for the latest version.

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
            world.address = AccountAddress.fromString(world.hexString!!)
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

Open the HTML report:

```bash
make report
```

## Troubleshooting

### Gradle wrapper not found

```bash
make wrapper
```

### SDK dependency not found

Ensure the Kaptos SDK is published and accessible. Update `build.gradle.kts` with the correct
repository and coordinates.

### Feature files not found

Feature files are expected at `../../features/` relative to this directory. Ensure you're running
from `tests/kotlin/`.

## Contributing

1. Check `PLAN.md` for implementation status
2. Implement step definitions in `src/test/kotlin/com/aptos/specs/steps/`
3. Update `../../FEATURE_COVERAGE.md` when tests pass
4. Follow Kotlin coding conventions and idiomatic patterns

## Current Status

- **SDK Version:** 0.1.2-beta
- **Test Infrastructure:** ✅ Complete
- **Step Definitions:** ~30% implemented (limited by SDK API exposure)
- **Tests Passing:** ~8/1616 (most scenarios need SDK features not yet available)

### SDK Limitations (0.1.2-beta)

The current Kaptos SDK doesn't expose several low-level primitives needed for the specs:

- No direct `Bcs` class for serialization
- No `Ed25519PrivateKey`, `Secp256k1` key classes
- No `RawTransaction`, `SignedTransaction` constructors
- No `AuthenticationKey` class
- No AIP-80 format support

Step definitions for these features are stubs that will be implemented as the SDK matures.

## References

- [Kaptos SDK](https://github.com/mcxross/kaptos)
- [Kaptos on Maven Central](https://search.maven.org/search?q=g:xyz.mcxross.kaptos)
- [Cucumber-JVM Documentation](https://cucumber.io/docs/cucumber/)
- [Kotest Assertions](https://kotest.io/docs/assertions/assertions.html)
- [Feature Specifications](../../features/)
- [Test Vectors](../../test-vectors/)
