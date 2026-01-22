# C++ SDK Test Coverage Implementation Plan

This document outlines the plan for implementing behavioral specification tests for the Aptos C++
SDK.

## Overview

Set up a C++ test implementation using CWT-Cucumber (C++20) to validate the Var Meta Aptos C++ SDK
against the Gherkin specifications, following the same patterns as the existing TypeScript, Go, and
Rust implementations.

## Context

The Aptos C++ SDK (built by Var Meta) is listed as an official SDK on aptos.dev but has limited
public documentation and no publicly accessible GitHub repository at this time. This scaffold is
prepared to be connected once the SDK API is clarified.

## Architecture

```
tests/cpp/
├── CMakeLists.txt          # Build configuration with Conan/FetchContent
├── conanfile.txt           # Conan dependencies (cwt-cucumber, nlohmann_json)
├── Makefile                # Convenience commands (test, test-required, etc.)
├── README.md               # Setup and usage documentation
├── PLAN.md                 # This file
├── src/
│   └── main.cpp            # Test runner entry point
├── steps/
│   ├── address_steps.cpp   # Address parsing step definitions
│   ├── cryptography_steps.cpp
│   ├── serialization_steps.cpp
│   ├── hashing_steps.cpp
│   ├── account_steps.cpp
│   └── transaction_steps.cpp
└── support/
    ├── world.hpp           # TestWorld struct (state between steps)
    ├── vectors.hpp         # Test vector type definitions
    └── vectors.cpp         # Test vector loading utilities
```

## Implementation Status

### Completed

- [x] CMakeLists.txt - Build configuration with C++20, Conan, FetchContent fallback
- [x] conanfile.txt - Conan package dependencies
- [x] Makefile - Make targets for building and running tests
- [x] src/main.cpp - CWT-Cucumber test runner
- [x] support/world.hpp - Test world with placeholder types
- [x] support/vectors.hpp - Test vector type definitions
- [x] support/vectors.cpp - JSON vector loading from test-vectors/
- [x] steps/address_steps.cpp - Address parsing steps (scaffold)
- [x] steps/cryptography_steps.cpp - Ed25519/Secp256k1/r1 steps (scaffold)
- [x] steps/serialization_steps.cpp - BCS serialization steps (scaffold)
- [x] steps/hashing_steps.cpp - SHA3-256, SHA2-256, etc. (scaffold)
- [x] steps/account_steps.cpp - Mnemonic derivation, auth keys (scaffold)
- [x] steps/transaction_steps.cpp - Transaction building/signing (scaffold)
- [x] README.md - Setup and usage documentation

### Pending SDK Integration

- [ ] Obtain Aptos C++ SDK repository access
- [ ] Add SDK dependency to CMakeLists.txt
- [ ] Replace placeholder types in world.hpp with actual SDK types
- [ ] Implement step definitions with real SDK API calls
- [ ] Run and debug tests against the SDK
- [ ] Update FEATURE_COVERAGE.md with passing tests

## SDK Integration Notes

The Var Meta C++ SDK is available at: **https://github.com/VAR-META-Tech/Aptos-Cpp-SDK**

### SDK Features (from their README)

- Generate new wallets (ED25519)
- Create/simulate/submit transactions
- Create collections and tokens (NFTs)
- Check account information
- Import wallets via BIP-39/BIP-32 mnemonics
- Compatibility with main, dev, and test networks

### SDK Dependencies

The SDK requires several third-party libraries:
- [bip3x](https://github.com/edwardstock/bip3x) - BIP-39/32 implementation
- [toolbox](https://github.com/edwardstock/toolbox)
- [cryptopp](https://github.com/weidai11/cryptopp) - Cryptography
- [cpprestsdk](https://github.com/microsoft/cpprestsdk) - REST client

### Current Integration Setup

The CMakeLists.txt includes four integration options (all currently commented out):

1. **Option A: Local path** - For development with a local SDK clone
2. **Option B: FetchContent** - Once GitHub repo is public
3. **Option C: find_package** - If SDK provides CMake config
4. **Option D: Conan** - If SDK is published to Conan

The `support/world.hpp` uses conditional compilation:
- `APTOS_SDK_AVAILABLE=1` → Uses actual SDK types
- Not defined → Uses placeholder types (allows scaffold to compile)

### Integration Steps

1. Clone and build the SDK:
   ```bash
   git clone https://github.com/VAR-META-Tech/Aptos-Cpp-SDK.git
   cd Aptos-Cpp-SDK
   git submodule update --init --recursive
   conan install . -s compiler.cppstd=20 --build=missing
   cd build && cmake .. && make
   ```

2. Set the SDK path in `CMakeLists.txt`:
   ```cmake
   set(APTOS_CPP_SDK_PATH "/path/to/Aptos-Cpp-SDK")
   ```

3. Update `support/world.hpp` includes based on SDK structure:
   - Headers are in `Src/` directory
   - Key classes: `Wallet`, `Account`, `RestClient`, `EntryFunction`

4. Update step definitions to use actual SDK APIs

### Known Issues

- CWT-Cucumber may crash with complex feature files from this repository
- The framework works with simple test scenarios (verified)
- May need to investigate Gherkin syntax compatibility or add more step definitions
- Consider using `--verbose` and `--dry-run` flags to debug step matching

### Expected SDK Types

Based on other Aptos SDKs, the C++ SDK likely provides:

```cpp
// Account address
class AccountAddress {
    static AccountAddress from_hex(const std::string& hex);
    std::string to_string_long() const;
    std::string to_string_short() const;
};

// Ed25519 cryptography
class Ed25519PrivateKey {
    static Ed25519PrivateKey generate();
    Ed25519PublicKey public_key() const;
    Ed25519Signature sign(const std::vector<uint8_t>& message) const;
};

// Transactions
class RawTransaction {
    std::vector<uint8_t> signing_message() const;
    SignedTransaction sign(const Ed25519PrivateKey& key) const;
};
```

## Key Design Decisions

### BDD Framework: CWT-Cucumber

Selected for:
- Modern C++20 support
- No mandatory external dependencies
- Full Gherkin syntax support
- Active maintenance

### Test World Pattern

Following the Rust implementation pattern with:
- Single global TestWorld struct
- Optional fields for all state
- Reset between scenarios
- Error handling via last_error field

### Build System

- Primary: CMake with Conan for dependency management
- Fallback: CMake FetchContent for when Conan unavailable
- C++20 required for CWT-Cucumber compatibility

## Testing Commands

```bash
# Install dependencies
make install-deps

# Build
make build

# Run all tests
make test

# Run by priority
make test-required    # P0
make test-preferred   # P1
make test-optional    # P2

# Run by category
make test-core-types
make test-cryptography
make test-accounts
make test-transactions
```

## Files to Update After SDK Integration

1. **CMakeLists.txt** - Add SDK find_package or FetchContent
2. **support/world.hpp** - Replace placeholder types with SDK types
3. **steps/*.cpp** - Implement TODO sections with SDK calls
4. **FEATURE_COVERAGE.md** - Mark scenarios as implemented

## References

- [CWT-Cucumber Documentation](https://those1990.github.io/cwt-cucumber/)
- [Aptos C++ SDK Documentation](https://aptos.dev/build/sdks/cpp-sdk)
- [Rust Test Implementation](../rust/) - Pattern reference
- [Feature Specifications](../../features/)
- [Test Vectors](../../test-vectors/)
