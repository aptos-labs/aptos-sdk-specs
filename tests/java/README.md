# Aptos Java SDK BDD Tests

This directory contains Cucumber-JVM BDD tests that validate the
[japtos](https://github.com/aptos-labs/japtos) (Aptos Java SDK) against the shared Gherkin
specifications.

## Prerequisites

- **Java 17+** (LTS recommended)
- **Maven 3.8+**
- **japtos SDK v1.1.8+** (auto-installed via Maven)

## Maven Dependency

The tests use the official japtos SDK from Maven Central:

```xml
<dependency>
    <groupId>io.github.aptos-labs</groupId>
    <artifactId>japtos</artifactId>
    <version>1.1.8</version>
</dependency>
```

## Quick Start

```bash
# Install dependencies
mvn dependency:resolve

# Run all tests
make test

# Run only required (P0) tests
make test-required

# Run specific category
make test-core-types

# Run tests without network
make test-offline
```

## Project Structure

```
src/test/java/com/aptos/specs/
├── RunCucumberTest.java     # JUnit 5 test runner
├── support/
│   ├── World.java           # Test context/state between steps
│   └── Vectors.java         # Test vector loading utilities
└── steps/
    ├── AddressSteps.java    # Address parsing/formatting
    ├── SerializationSteps.java # BCS encoding/decoding
    ├── TypeTagSteps.java    # TypeTag parsing/formatting
    ├── CryptoSteps.java     # Cryptographic operations
    ├── HashingSteps.java    # Hash functions
    ├── AccountSteps.java    # Account management
    └── ...                  # Additional step definitions
```

## Running Tests

### Using Make

```bash
make test              # Run all tests
make test-required     # Run @required tests only
make test-preferred    # Run @preferred tests only
make test-optional     # Run @optional tests only
make test-core-types   # Run @core-types tests
make test-cryptography # Run @cryptography tests
make test-transactions # Run @transactions tests
make test-offline      # Run tests that don't need network
make dry-run           # Check step definitions exist
```

### Using Maven directly

```bash
# Run all tests
mvn test

# Run with specific profile
mvn test -Prequired
mvn test -Pcore-types

# Run with custom tag filter
mvn test -Dcucumber.filter.tags="@required and @core-types"

# Dry run
mvn test -Dcucumber.execution.dry-run=true
```

## Test Reports

After running tests, reports are generated in:

- **HTML Report**: `target/cucumber-reports/cucumber.html`
- **JSON Report**: `target/cucumber-reports/cucumber.json`

## Test Tags

| Tag             | Description                     |
| --------------- | ------------------------------- |
| `@required`     | Must-have features (P0)         |
| `@preferred`    | Recommended features (P1)       |
| `@optional`     | Nice-to-have features (P2)      |
| `@core-types`   | Address, TypeTag, serialization |
| `@cryptography` | Keys, signatures, hashing       |
| `@accounts`     | Account creation, derivation    |
| `@transactions` | Transaction building            |
| `@api-clients`  | REST API, faucet, indexer       |
| `@advanced`     | Multi-sig, keyless, etc.        |
| `@network`      | Requires network connectivity   |

## Writing Step Definitions

Step definitions follow Cucumber-JVM conventions using japtos SDK types:

```java
package com.aptos.specs.steps;

import io.cucumber.java.en.*;
import com.aptos.specs.support.World;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.account.Ed25519Account;
import static org.assertj.core.api.Assertions.*;

public class ExampleSteps {
    private final World world;

    public ExampleSteps(World world) {
        this.world = world;
    }

    @Given("a hex string {string}")
    public void givenHexString(String hex) {
        world.setHexString(hex);
    }

    @When("I parse it as an AccountAddress")
    public void whenParseAddress() {
        try {
            AccountAddress addr = AccountAddress.fromHex(world.getHexString());
            world.setAddress(addr);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }

    @Then("the parsing should succeed")
    public void thenParsingShouldSucceed() {
        assertThat(world.getError()).isNull();
        assertThat(world.getAddress()).isNotNull();
    }
}
```

## Key japtos SDK Classes

| Class               | Package                        | Purpose                       |
| ------------------- | ------------------------------ | ----------------------------- |
| `AccountAddress`    | `com.aptoslabs.japtos.types`   | 32-byte account addresses     |
| `Ed25519Account`    | `com.aptoslabs.japtos.account` | Ed25519 key pairs and signing |
| `Ed25519PrivateKey` | `com.aptoslabs.japtos.crypto`  | Private key operations        |
| `Ed25519PublicKey`  | `com.aptoslabs.japtos.crypto`  | Public key verification       |
| `AuthenticationKey` | `com.aptoslabs.japtos.types`   | Auth key derivation           |
| `HashValue`         | `com.aptoslabs.japtos.types`   | 32-byte hash values           |
| `AptosClient`       | `com.aptoslabs.japtos.client`  | REST API client               |
| `HexUtils`          | `com.aptoslabs.japtos.utils`   | Hex encoding/decoding         |

## Test Vectors

Test vectors are loaded from `../../test-vectors/*.json`:

```java
// Load address parsing vectors
List<AddressVector> vectors = Vectors.getAddressParsingVectors();
for (AddressVector v : vectors) {
    AccountAddress addr = AccountAddress.fromString(v.getInput());
    assertThat(addr.toStringLong()).isEqualToIgnoringCase(v.getExpected().getFullHex());
}
```

## Troubleshooting

### japtos SDK not found

If Maven cannot resolve the japtos dependency:

1. Check if japtos is published to Maven Central or GitHub Packages
2. Update the repository configuration in `pom.xml`
3. If building locally, install japtos to local Maven repository:
   ```bash
   cd /path/to/japtos
   mvn install -DskipTests
   ```

### Tests failing with "Step not implemented"

Run dry-run to check which steps are missing:

```bash
make dry-run
```

### Network-dependent tests failing

Run offline tests only:

```bash
make test-offline
```

## Contributing

See [PLAN.md](./PLAN.md) for the implementation roadmap and status.

When implementing new steps:

1. Follow existing patterns in step definition files
2. Update `FEATURE_COVERAGE.md` in the repo root
3. Run tests to verify implementation
