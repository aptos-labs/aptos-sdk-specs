# Aptos C++ SDK Behavioral Specification Tests

This directory contains BDD tests that validate the Aptos C++ SDK against the Gherkin specifications
in `../../features/`.

## SDK Under Test

- **SDK**: Aptos C++/Unreal SDK (built by Var Meta)
- **Repository**: https://github.com/VAR-META-Tech/Aptos-Cpp-SDK
- **Documentation**: https://aptos.dev/build/sdks/cpp-sdk
- **Framework**: CWT-Cucumber (C++20)

## Prerequisites

- **CMake** 3.16 or later
- **C++20** compatible compiler (GCC 10+, Clang 10+, MSVC 2019+)
- **Conan** 2.x (recommended) or dependencies will be fetched via CMake FetchContent

### Installing Conan (Recommended)

```bash
pip install conan
```

## Quick Start

```bash
# Install dependencies
make install-deps

# Build and run all tests
make test

# Run only required (P0) tests
make test-required
```

## Build Options

### Option 1: Using Conan (Recommended)

```bash
# Install dependencies
conan install . --output-folder=build --build=missing

# Configure with Conan toolchain
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake

# Build
cmake --build build

# Run tests
./build/aptos_spec_tests ../../features
```

### Option 2: Using CMake FetchContent

If Conan is not available, CMake will automatically fetch dependencies:

```bash
cmake -S . -B build
cmake --build build
./build/aptos_spec_tests ../../features
```

## Running Tests

### All Tests

```bash
make test
# or
./build/aptos_spec_tests ../../features
```

### By Priority Level

```bash
make test-required    # P0 - Must-have features
make test-preferred   # P1 - Recommended features
make test-optional    # P2 - Extended features
```

### By Category

```bash
make test-core-types      # Address, TypeTag, BCS
make test-cryptography    # Keys, signatures, hashing
make test-accounts        # Account management
make test-transactions    # Transaction building
make test-api-clients     # REST API clients
make test-advanced        # Multi-sig, keyless, etc.
```

### Offline (No Network)

```bash
make test-offline
```

### Using CTest

```bash
cd build
ctest                    # All tests
ctest -R required        # Tests matching "required"
ctest -R cryptography    # Tests matching "cryptography"
```

## Project Structure

```
cpp/
├── CMakeLists.txt          # Build configuration
├── conanfile.txt           # Conan dependencies
├── Makefile                # Convenience targets
├── README.md               # This file
├── PLAN.md                 # Implementation plan
├── src/
│   └── main.cpp            # Test runner entry point
├── steps/
│   ├── address_steps.cpp   # Address parsing steps
│   ├── cryptography_steps.cpp
│   ├── serialization_steps.cpp
│   ├── hashing_steps.cpp
│   ├── account_steps.cpp
│   └── transaction_steps.cpp
└── support/
    ├── world.hpp           # Test state struct
    ├── vectors.hpp         # Test vector definitions
    └── vectors.cpp         # Test vector loading
```

## Implementation Status

> **Note**: This test scaffold is prepared but not yet connected to the Aptos C++ SDK. The SDK
> integration is pending confirmation of the SDK's public API and repository.

### Current State

- [x] CMake build configuration
- [x] CWT-Cucumber integration
- [x] Test world structure (following Rust pattern)
- [x] Test vector loading
- [x] Step definition scaffolds
- [ ] Aptos C++ SDK dependency
- [ ] Step implementation with SDK calls

### Next Steps

1. Clone and build the SDK:
   ```bash
   git clone https://github.com/VAR-META-Tech/Aptos-Cpp-SDK.git
   cd Aptos-Cpp-SDK
   git submodule update --init --recursive
   conan install . -s compiler.cppstd=20 --build=missing
   cd build && cmake .. && make
   ```
2. Set SDK path in `CMakeLists.txt`
3. Replace placeholder types in `support/world.hpp` with actual SDK types
4. Implement step definitions with real SDK calls (see SDK examples in `AptosSDKDemo/`)
5. Run tests and fix any issues

## Step Definition Pattern

CWT-Cucumber uses macros for step definitions:

```cpp
#include <cwt/cucumber.hpp>
#include "support/world.hpp"

using namespace aptos::specs;

GIVEN("a hex string {string}") {
    auto& world = get_world();
    world.hex_string = CUKE_ARG(1);
}

WHEN("I parse it as an AccountAddress") {
    auto& world = get_world();
    // TODO: Replace with SDK call
    world.address = AccountAddress::from_hex(*world.hex_string);
}

THEN("the parsing should succeed") {
    auto& world = get_world();
    cuke::is_true(world.address.has_value());
}
```

## Test Vectors

Test vectors are loaded from `../../test-vectors/*.json`:

```cpp
#include "support/vectors.hpp"

auto vectors = vectors::get_address_parsing_vectors();
for (const auto& v : vectors) {
    auto addr = AccountAddress::from_hex(v.input);
    assert(addr->to_string_long() == v.expected.full_hex);
}
```

## Debugging

### Dry Run (Show Steps)

```bash
./build/aptos_spec_tests ../../features --dry-run
```

### Verbose Output

```bash
./build/aptos_spec_tests ../../features --verbose
```

### Single Feature File

```bash
./build/aptos_spec_tests ../../features/01-core-types/address.feature
```

## Dependencies

| Dependency    | Version | Purpose                       |
| ------------- | ------- | ----------------------------- |
| cwt-cucumber  | 2.7+    | BDD test framework            |
| nlohmann_json | 3.11+   | JSON parsing for test vectors |
| aptos-cpp-sdk | TBD     | SDK under test                |

## Contributing

When adding new step definitions:

1. Create steps in the appropriate `steps/*.cpp` file
2. Follow existing patterns for world state management
3. Use test vectors where applicable
4. Update `FEATURE_COVERAGE.md` when tests pass

## References

- [CWT-Cucumber Documentation](https://those1990.github.io/cwt-cucumber/)
- [Aptos C++ SDK Documentation](https://aptos.dev/build/sdks/cpp-sdk)
- [Feature Specifications](../../features/)
- [Test Vectors](../../test-vectors/)
