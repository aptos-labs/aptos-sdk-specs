# Aptos SDK Behavioral Specifications

[![CI](https://github.com/aptos-labs/aptos-sdk-specs/actions/workflows/ci.yml/badge.svg)](https://github.com/aptos-labs/aptos-sdk-specs/actions/workflows/ci.yml)
[![Nightly Tests](https://github.com/aptos-labs/aptos-sdk-specs/actions/workflows/nightly.yml/badge.svg)](https://github.com/aptos-labs/aptos-sdk-specs/actions/workflows/nightly.yml)

This repository contains language-agnostic behavioral specifications for Aptos SDK implementations.
These specifications ensure consistent behavior across all official and community SDKs.

## SDK Coverage

See **[FEATURE_COVERAGE.md](FEATURE_COVERAGE.md)** for detailed test coverage across all SDKs,
including:

- SDK versions and publishers
- Feature-level compatibility matrix
- Individual test status per scenario
- Follow-up actions per SDK
- Performance benchmarks (planned)

For per-SDK details, see the `SDK_STATUS.md` file in each `tests/<language>/` directory.

## Purpose

1. **Standardization**: Define expected SDK behaviors that must be consistent across languages
2. **Testing**: Provide Gherkin scenarios executable with BDD frameworks in any language
3. **Documentation**: Serve as authoritative reference for SDK implementers
4. **Validation**: Enable automated cross-SDK compatibility testing

## Directory Structure

```
specifications/
├── README.md                    # This file
├── plan.md                      # Implementation plan and methodology
├── feature-matrix.md            # Feature comparison across SDKs
│
├── categories/
│   ├── required.md              # P0: Must-have features
│   ├── preferred.md             # P1: Recommended features
│   └── optional.md              # P2: Nice-to-have features
│
├── features/
│   ├── 01-core-types/           # Address, TypeTag, serialization
│   │   ├── spec.md
│   │   ├── address.feature      # 31 scenarios
│   │   ├── type-tags.feature    # 27 scenarios
│   │   └── serialization.feature # 32 scenarios
│   │
│   ├── 02-cryptography/         # Keys, signatures, hashing
│   │   ├── spec.md
│   │   ├── ed25519.feature      # 23 scenarios
│   │   ├── secp256k1.feature    # 18 scenarios
│   │   ├── secp256r1.feature    # 26 scenarios (WebAuthn/Passkey)
│   │   └── hashing.feature      # 21 scenarios
│   │
│   ├── 03-account-management/   # Account creation, derivation
│   │   ├── spec.md
│   │   ├── single-key.feature   # 30 scenarios
│   │   ├── mnemonic-derivation.feature # 31 scenarios
│   │   └── authentication-key.feature  # 19 scenarios
│   │
│   ├── 04-transaction-building/ # Transaction construction
│   │   ├── spec.md
│   │   ├── raw-transaction.feature   # 25 scenarios
│   │   ├── entry-function.feature    # 29 scenarios
│   │   ├── script.feature            # 25 scenarios
│   │   └── signing.feature           # 26 scenarios
│   │
│   ├── 05-api-clients/          # REST API, indexer
│   │   ├── spec.md
│   │   ├── fullnode-api.feature      # 24 scenarios
│   │   ├── view-functions.feature    # 28 scenarios
│   │   ├── transaction-submission.feature # 30 scenarios
│   │   ├── faucet.feature            # 24 scenarios
│   │   ├── indexer.feature           # 32 scenarios
│   │   ├── gas-estimation.feature    # 26 scenarios
│   │   └── retry.feature             # 27 scenarios
│   │
│   └── 06-advanced/             # Multi-sig, keyless, etc.
│       ├── spec.md
│       ├── multi-signature.feature   # 24 scenarios
│       ├── multi-agent.feature       # 22 scenarios
│       ├── fee-payer.feature         # 23 scenarios
│       ├── keyless.feature           # 28 scenarios
│       ├── codegen.feature           # 30 scenarios
│       ├── error-handling.feature    # 28 scenarios
│       └── simulation.feature        # 23 scenarios
│
├── test-vectors/
│   ├── README.md                # Test vector documentation
│   ├── addresses.json           # Address parsing/formatting vectors
│   ├── mnemonics.json           # BIP-39 derivation vectors
│   ├── transactions.json        # Signed transaction vectors
│   ├── signatures.json          # Cryptographic signature vectors
│   ├── type-tags.json           # TypeTag parsing vectors
│   ├── bcs.json                 # BCS encoding vectors
│   └── multi-sig.json           # Multi-signature transaction vectors
│
└── tests/                       # Executable test implementations
    ├── README.md                # Test setup documentation
    ├── typescript/              # Tests for @aptos-labs/ts-sdk
    │   ├── package.json
    │   ├── steps/               # Cucumber step definitions
    │   └── support/             # Test utilities
    └── go/                      # Tests for aptos-go-sdk
        ├── go.mod
        ├── *_steps.go           # Godog step definitions
        └── Makefile
```

## Feature Categories

### Required (P0)

Features every SDK **must** implement to be considered functional. These are the minimum viable
features for basic blockchain interaction.

### Preferred (P1)

Features **recommended** for production SDKs. These enhance developer experience and are expected in
mature implementations.

### Optional (P2)

**Extended** features for comprehensive SDKs. These provide advanced functionality but are not
necessary for basic usage.

## How to Use These Specifications

### For SDK Implementers

1. Start with **Required (P0)** features
2. Use test vectors to validate your implementation
3. Run Gherkin scenarios against your SDK
4. Progress to Preferred and Optional features

### For Contributors

1. New features must include a design document (`spec.md`)
2. All behaviors must have corresponding Gherkin scenarios
3. Deterministic behaviors require test vectors
4. Follow the existing document structure

### For Testers

1. Use the appropriate BDD framework for your language:
   - TypeScript: Cucumber.js
   - Python: Behave
   - Go: Godog
   - C#: SpecFlow
   - Rust: cucumber-rs
   - Kotlin: Cucumber-JVM
   - C++: cucumber-cpp
   - Swift: XCTest-Gherkin

2. Implement step definitions for each `.feature` file
3. Load test vectors for deterministic validation

## Gherkin Syntax Reference

```gherkin
Feature: Feature Name
  As an SDK user
  I want to perform some action
  So that I can achieve some goal

  @required
  @category-tag
  Scenario: Descriptive scenario name
    Given some precondition
    When I perform an action
    Then I should see expected result

  @required
  @category-tag
  Scenario Outline: Parameterized scenario
    Given input "<input>"
    When I process it
    Then output should be "<output>"

    Examples:
      | input | output |
      | a     | b      |
      | c     | d      |
```

## Test Vector Format

```json
{
  "version": "1.0",
  "description": "Description of test vectors",
  "vectors": [
    {
      "name": "descriptive_test_name",
      "description": "What this test validates",
      "input": {
        "field1": "value1"
      },
      "expected": {
        "field2": "value2"
      }
    }
  ]
}
```

## Reference SDKs

These specifications are derived from analyzing:

| SDK        | Repository                                                                    | Language   |
| ---------- | ----------------------------------------------------------------------------- | ---------- |
| TypeScript | [aptos-labs/aptos-ts-sdk](https://github.com/aptos-labs/aptos-ts-sdk)         | TypeScript |
| Python     | [aptos-labs/aptos-python-sdk](https://github.com/aptos-labs/aptos-python-sdk) | Python     |
| Go         | [aptos-labs/aptos-go-sdk](https://github.com/aptos-labs/aptos-go-sdk)         | Go         |
| .NET       | [aptos-labs/aptos-dotnet-sdk](https://github.com/aptos-labs/aptos-dotnet-sdk) | C#         |

## Running Tests Locally

### Quick Start

```bash
# Format all code
make format

# Lint all code
make lint

# Run tests for a specific SDK
cd tests/typescript && bun test
cd tests/go && make test
cd tests/rust && cargo test --test specs
cd tests/python && make test
```

### By Priority Level

Each SDK supports running tests by priority:

```bash
# Required tests only (must pass)
make test-required

# Preferred tests (should pass)
make test-preferred

# Optional tests (nice to have)
make test-optional
```

### CI Workflows

- **CI** (`ci.yml`): Runs on every PR - format check + required/preferred tests
- **Nightly** (`nightly.yml`): Runs daily at 2 AM UTC - full test suite

You can manually trigger nightly tests from the Actions tab.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add/modify specifications following existing patterns
4. Ensure all test vectors are valid
5. Run `make format` before committing
6. Submit a pull request

## License

These specifications are part of the Aptos SDK project and follow the same license terms.
