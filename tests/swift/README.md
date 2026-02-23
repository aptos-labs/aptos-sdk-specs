# Swift SDK Behavioral Specification Tests

This directory contains BDD test implementations for the official Aptos Swift SDK using XCTest.

## Prerequisites

- Xcode 16.0+ or Swift 6.0+
- macOS 14.0+ (for development)
- iOS 17.0+ (for iOS target)

## Setup

```bash
cd tests/swift

# Setup and link feature files
make setup

# Build
swift build

# Run tests
swift test
```

## Project Structure

```
swift/
├── Package.swift                    # SPM manifest
├── Makefile                         # Standard test commands
├── README.md                        # This file
├── SDK_STATUS.md                    # Coverage tracking
├── PLAN.md                          # Implementation plan
├── Sources/
│   └── AptosSpecs/
│       └── AptosSpecs.swift         # Empty (test-only package)
└── Tests/
    └── AptosSpecsTests/
        ├── AptosSpecsTests.swift    # XCTest-based tests
        ├── Support/                 # Test utilities
        │   ├── World.swift          # Test context
        │   ├── Vectors.swift        # Test vector loading
        │   └── Hooks.swift          # Before/After hooks
        └── CucumberTests/           # CucumberSwift BDD tests (disabled)
            ├── CucumberTestRunner.swift  # Cucumber test runner
            ├── Steps/               # Step definitions
            │   ├── AddressSteps.swift
            │   ├── Ed25519Steps.swift
            │   ├── SerializationSteps.swift
            │   └── ...
            └── Support/             # Cucumber test utilities
                └── TestWorld.swift  # Shared test context
```

## Running Tests

```bash
# Run all tests (XCTest + Cucumber)
make test
# or
swift test

# Run only XCTest-based tests
make test-xctest

# Run only @required tests
make test-required

# Run @core-types tests
make test-core-types

# Run @cryptography tests
make test-cryptography

# Run with verbose output
swift test --verbose
```

## SDK Under Test

| Property       | Value                                         |
| -------------- | --------------------------------------------- |
| **Package**    | `AptosSDK`                                    |
| **Repository** | https://github.com/aptos-labs/aptos-swift-sdk |
| **Publisher**  | aptos-labs (official)                         |

## Dependencies

- **AptosSDK** — Official Aptos SDK for Swift (includes secp256k1, BigInt, CTweetNaCl)
- **CucumberSwift** — BDD testing framework for Swift (disabled, upstream bug)

## Test Frameworks

This project uses two complementary test approaches:

1. **XCTest-based tests** (`AptosSpecsTests.swift`)
   - Manually translated tests from Gherkin scenarios
   - Uses XCTest assertions directly
   - Follows `test_<Feature>_<Scenario>` naming pattern

2. **CucumberSwift BDD tests** (`CucumberTests/`)
   - Parses Gherkin `.feature` files directly
   - Step definitions in `Steps/` directory
   - Currently disabled due to upstream CucumberSwift bug

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

## Known Issues

### Xcode Requirement

XCTest requires full Xcode installation, not just Command Line Tools. To run tests:

1. Install Xcode from the App Store
2. Run `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`
3. Then `swift test` will work

### CucumberSwift Bug

CucumberSwift has a compilation bug preventing its use. Step definitions in `CucumberTests/Steps/`
are ready for when this is fixed upstream.

**Workaround:** Use the XCTest-based tests in `AptosSpecsTests.swift`.

## Implementation Status

See [SDK_STATUS.md](./SDK_STATUS.md) for detailed coverage information.

See [PLAN.md](./PLAN.md) for the implementation roadmap.
