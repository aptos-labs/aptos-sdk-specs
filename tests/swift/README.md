# Swift SDK Behavioral Specification Tests

This directory contains BDD test implementations for the Aptos Swift SDK using CucumberSwift.

## Prerequisites

- Xcode 14.0+ or Swift 5.7+
- macOS 12.0+ (for development)
- iOS 13.0+ (for iOS target)

## Setup

```bash
cd tests/swift

# Resolve dependencies
swift package resolve

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
        ├── AptosSpecsTests.swift    # CucumberSwift test runner
        ├── Steps/                   # Step definitions
        │   ├── AddressSteps.swift
        │   ├── CryptoSteps.swift
        │   └── ...
        └── Support/                 # Test utilities
            ├── World.swift          # Test context
            ├── Vectors.swift        # Test vector loading
            └── Hooks.swift          # Before/After hooks
```

## Running Tests

```bash
# Run all tests
make test
# or
swift test

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

## Implementation Status

See [SDK_STATUS.md](./SDK_STATUS.md) for detailed coverage information.

See [PLAN.md](./PLAN.md) for the implementation roadmap.
