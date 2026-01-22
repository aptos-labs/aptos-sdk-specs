# C++ SDK Test Coverage Implementation Plan

This document outlines the plan for implementing behavioral specification tests for the Aptos C++
SDK.

## Overview

Set up a C++ test implementation using CWT-Cucumber (C++20) to validate the Var Meta Aptos C++ SDK
against the Gherkin specifications, following the same patterns as the existing TypeScript, Go, and
Rust implementations.

## Context

The Aptos C++ SDK (built by Var Meta) is available at https://github.com/VAR-META-Tech/Aptos-Cpp-SDK.
The SDK has been cloned into the `sdk/` directory and integrated with conditional compilation.

## Architecture

```
tests/cpp/
├── CMakeLists.txt          # Build configuration with Conan/FetchContent
├── conanfile.txt           # Conan dependencies (cwt-cucumber, nlohmann_json)
├── Makefile                # Convenience commands (test, test-required, etc.)
├── README.md               # Setup and usage documentation
├── PLAN.md                 # This file
├── sdk/                    # Cloned Var Meta Aptos C++ SDK
│   ├── Src/                # SDK source code
│   ├── ThirdParty/bip3x/   # BIP-39/32 submodule
│   └── build/              # SDK build output
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
    ├── world.hpp           # TestWorld struct (SDK + placeholder types)
    ├── placeholders.cpp    # Placeholder implementations (fallback)
    ├── vectors.hpp         # Test vector type definitions
    └── vectors.cpp         # Test vector loading utilities
```

## Implementation Status

### Completed - Infrastructure

- [x] CMakeLists.txt - Build configuration with C++20, Conan, FetchContent fallback
- [x] conanfile.txt - Conan package dependencies
- [x] Makefile - Make targets for building and running tests
- [x] src/main.cpp - CWT-Cucumber test runner
- [x] support/world.hpp - Test world with SDK and placeholder types
- [x] support/vectors.hpp - Test vector type definitions
- [x] support/vectors.cpp - JSON vector loading from test-vectors/
- [x] README.md - Setup and usage documentation

### Completed - SDK Integration

- [x] Clone SDK into `sdk/` directory
- [x] Build SDK with Conan dependencies (cryptopp, cpprestsdk, Boost, OpenSSL)
- [x] Configure CMakeLists.txt to find and link SDK
- [x] Update world.hpp with conditional SDK types
- [x] Update step definitions with SDK API calls (ifdef guards)
- [x] Successfully build and test with SDK

### Completed - Step Definitions (Basic)

- [x] steps/address_steps.cpp - Address parsing (SDK: FromHex, ToString)
- [x] steps/cryptography_steps.cpp - Ed25519 (SDK: Random, FromHex, Sign, GetPublicKey)
- [x] steps/serialization_steps.cpp - BCS serialization (scaffold)
- [x] steps/hashing_steps.cpp - SHA3-256, SHA2-256, etc. (scaffold)
- [x] steps/account_steps.cpp - Mnemonic derivation, auth keys (scaffold)
- [x] steps/transaction_steps.cpp - Transaction building/signing (scaffold)

### Remaining Work

- [ ] Implement additional step definitions for full feature coverage
- [ ] Handle SDK-specific behaviors (AIP-40 short addresses)
- [ ] Update FEATURE_COVERAGE.md with passing tests
- [ ] Add more error handling and edge cases

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

The SDK is cloned into `sdk/` and built with Conan. The CMakeLists.txt automatically:
1. Detects if SDK is built (`sdk/build/build/Release/libAptos.dylib`)
2. Sets `APTOS_SDK_AVAILABLE=1` compile definition
3. Adds SDK include paths (`Src/`, `ThirdParty/bip3x/include`, toolbox)
4. Links against `libAptos.dylib`

The `support/world.hpp` uses conditional compilation:
- `APTOS_SDK_AVAILABLE=1` → Uses actual SDK types (Aptos::Accounts::*, etc.)
- Not defined → Uses placeholder types (allows scaffold to compile without SDK)

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

### Known Issues / Behaviors

1. **AIP-40 Short Addresses**: The SDK's `ToString()` returns short format for special addresses (e.g., "0x1" instead of full 64-char). This is correct per AIP-40 but differs from some test expectations.

2. **Step Coverage**: Many feature file scenarios use steps that aren't yet defined. Use `--dry-run` to identify missing steps.

3. **SDK Build Dependency**: The SDK must be built before tests can compile. Run the SDK build commands first.

4. **Conditional Compilation**: Step definitions use `#ifdef APTOS_SDK_AVAILABLE` to support both SDK and placeholder modes.

### Actual SDK Types

The Var Meta SDK provides these types (in `Aptos::` namespace):

```cpp
// Accounts/AccountAddress.h
namespace Aptos::Accounts {
    class AccountAddress {
        static AccountAddress FromHex(std::string address);  // throws on error
        std::string ToString() const;  // AIP-40 compliant (short for special)
        CryptoPP::SecByteBlock addressBytes() const;
    };
}

// Accounts/Ed25519/PrivateKey.h
namespace Aptos::Accounts::Ed25519 {
    class PrivateKey {
        static PrivateKey Random();
        static PrivateKey FromHex(std::string key);
        PublicKey GetPublicKey();
        Ed25519Signature Sign(CryptoPP::SecByteBlock message);
    };
}

// HDWallet/Wallet.h
namespace Aptos::HDWallet {
    class Wallet {
        explicit Wallet(const std::string& mnemonicWords, ...);
        Accounts::Account Account() const;
    };
}

// BCS/Rawtransaction.h (note: in BCS namespace, not Transactions)
namespace Aptos::BCS {
    class RawTransaction { ... };
    class SignedTransaction { ... };
    class TransactionPayload { ... };
}
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
