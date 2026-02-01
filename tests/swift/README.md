# Swift SDK Behavioral Specification Tests

This directory contains BDD test implementations for the Aptos Swift SDK using CucumberSwift and
XCTest.

## Prerequisites

- Xcode 15.0+ or Swift 5.9+
- macOS 12.0+ (for development)
- iOS 13.0+ (for iOS target)

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
        ├── AptosSpecsTests.swift    # XCTest-based tests (286 tests)
        ├── Support/                 # Test utilities
        │   ├── World.swift          # Test context
        │   ├── Vectors.swift        # Test vector loading
        │   └── Hooks.swift          # Before/After hooks
        └── CucumberTests/           # CucumberSwift BDD tests
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

# Run only Cucumber BDD tests
make test-cucumber

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

| Property          | Value                                                 |
| ----------------- | ----------------------------------------------------- |
| **Package**       | `aptos-swift-sdk`                                     |
| **Repository**    | https://github.com/ALCOVE-LAB/aptos-swift-sdk         |
| **Documentation** | https://aptos.dev/build/sdks/community-sdks/swift-sdk |

## Dependencies

- **CucumberSwift** - BDD testing framework for Swift
- **aptos-swift-sdk** - Aptos SDK for Swift
- **CryptoSwift** - For SHA3-256 hashing
- **secp256k1.swift** - For secp256k1 cryptography

## Test Frameworks

This project uses two complementary test approaches:

1. **XCTest-based tests** (`AptosSpecsTests.swift`)
   - 286 manually translated tests from Gherkin scenarios
   - Uses XCTest assertions directly
   - Follows `test_<Feature>_<Scenario>` naming pattern

2. **CucumberSwift BDD tests** (`CucumberTests/`)
   - Parses Gherkin `.feature` files directly
   - Step definitions in `Steps/` directory
   - Better alignment with shared feature files

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

CucumberSwift has a bug in `CucumberTest.swift` line 84 - it uses `addTeardownBlock` without the
required `@available(macOS 10.15, iOS 13.0, tvOS 13.0, *)` annotation. This causes compilation
errors even when targeting macOS 10.15 or newer.

The step definitions in `CucumberTests/Steps/` are ready and waiting for this upstream fix. Once
fixed, uncomment the CucumberSwift dependency and CucumberTests target in `Package.swift`.

**Workaround:** Use the XCTest-based tests in `AptosSpecsTests.swift` (286 tests, all passing).

### SDK Path Behaviors

- `AccountAddress.toString()` only shortens "special" addresses (0x0-0xf)
- For non-special addresses, use `toStringLong()` for consistent format
- Ed25519 BIP-44 path uses hardened derivation: `m/44'/637'/0'/0'/0'`
- Secp256k1 BIP-44 path uses standard derivation: `m/44'/637'/0'/0/0`

## Implementation Status

See [SDK_STATUS.md](./SDK_STATUS.md) for detailed coverage information.

See [PLAN.md](./PLAN.md) for the implementation roadmap.
