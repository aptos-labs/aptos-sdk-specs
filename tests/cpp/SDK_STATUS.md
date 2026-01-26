# C++ SDK Test Status

> **Last Updated:** 2026-01-22  
> **Last Verified:** 2026-01-22 via `make test`

---

## 1. SDK Information

| Property             | Value                                          |
| -------------------- | ---------------------------------------------- |
| **Package**          | `Aptos-Cpp-SDK`                                |
| **Version Tested**   | dev (main branch)                              |
| **Publisher**        | VAR-META-Tech (community)                      |
| **Repository**       | https://github.com/VAR-META-Tech/Aptos-Cpp-SDK |
| **Package Registry** | Source (CMake/Conan)                           |
| **Test Framework**   | CWT-Cucumber (C++20)                           |

---

## 2. Coverage Summary

| Priority       | Passing | Total   | Percentage | Status |
| -------------- | ------- | ------- | ---------- | ------ |
| Required (P0)  | 49      | 370     | 13%        | ❌     |
| Preferred (P1) | 0       | 183     | 0%         | ❌     |
| Optional (P2)  | 0       | 250     | 0%         | ❌     |
| **Total**      | **49**  | **803** | **6%**     | ❌     |

> **Notes:**
>
> - SDK integration in progress
> - Many step definitions are scaffolds
> - Community SDK from VAR-META-Tech

---

## 3. Feature Availability

### ✅ Fully Available Features

| Feature | Notes                                           |
| ------- | ----------------------------------------------- |
| address | Address parsing via `AccountAddress::FromHex()` |
| ed25519 | Key generation, signing via SDK                 |

### 🟡 Partially Available

| Feature             | Reason                            | Impact            |
| ------------------- | --------------------------------- | ----------------- |
| serialization       | BCS available, tests partial      | Scaffold only     |
| hashing             | SHA3-256 available, tests partial | Scaffold only     |
| mnemonic-derivation | BIP-39/BIP-44 available           | Tests not written |
| authentication-key  | Available, tests partial          | Scaffold only     |

### ➖ Not Available in SDK

| Feature    | Reason          | Tracking Issue |
| ---------- | --------------- | -------------- |
| secp256k1  | Not implemented | -              |
| secp256r1  | Not implemented | -              |
| bls12381   | Not implemented | -              |
| keyless    | Not implemented | -              |
| codegen    | Not implemented | -              |
| simulation | Not implemented | -              |

---

## 4. Known Issues

| Scenario           | Issue                                    | Workaround                 |
| ------------------ | ---------------------------------------- | -------------------------- |
| Address formatting | `ToString()` returns AIP-40 short format | Expected behavior per spec |
| SDK build          | Requires Conan dependencies              | Run SDK build first        |
| Step definitions   | Many are scaffolds                       | Implementation in progress |

### SDK-Specific Behaviors

| Behavior         | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| AIP-40 addresses | `ToString()` returns "0x1" not full 64-char for special addresses  |
| Namespaces       | Types in `Aptos::Accounts::`, `Aptos::BCS::`, etc.                 |
| BCS location     | `RawTransaction` is in `Aptos::BCS::`, not `Aptos::Transactions::` |

---

## 5. Missing Test Implementations

### Required (P0) - High Priority

| Feature                | Scenarios     | Notes                     |
| ---------------------- | ------------- | ------------------------- |
| address                | #6-10, #19-22 | Error handling, BCS tests |
| serialization          | All 18        | Scaffold only             |
| type-tags              | All 24        | Not implemented           |
| ed25519                | Most          | Signing tests needed      |
| secp256k1              | All           | Feature not in SDK        |
| hashing                | Most          | Scaffold only             |
| authentication-key     | Most          | Scaffold only             |
| mnemonic-derivation    | Most          | Tests not written         |
| single-key             | All           | Not implemented           |
| entry-function         | All           | Scaffold only             |
| raw-transaction        | All           | Scaffold only             |
| signing                | All           | Scaffold only             |
| fullnode-api           | All           | Not implemented           |
| transaction-submission | All           | Not implemented           |
| error-handling         | All           | Not implemented           |

### Preferred (P1) - Medium Priority

All preferred features need step definitions.

### Optional (P2) - Low Priority

All optional features need step definitions.

---

## 6. SDK-Specific Notes

### SDK Structure

```cpp
// Accounts/AccountAddress.h
namespace Aptos::Accounts {
    class AccountAddress {
        static AccountAddress FromHex(std::string address);
        std::string ToString() const;  // AIP-40 compliant
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
```

### Build Requirements

- **C++20** required for CWT-Cucumber
- **Conan** for dependency management
- SDK dependencies: cryptopp, cpprestsdk, Boost, OpenSSL
- SDK submodule: bip3x for BIP-39/32

---

## 7. How to Run Tests

```bash
cd tests/cpp

# Install dependencies
make install-deps

# Build (requires SDK built first)
make build

# Run all tests
make test

# Run by priority
make test-required
make test-preferred

# Run by category
make test-core-types
make test-cryptography
make test-accounts
make test-transactions

# Dry run (check step definitions)
./build/aptos-specs --dry-run
```

### Building the SDK First

```bash
# Clone SDK
git clone https://github.com/VAR-META-Tech/Aptos-Cpp-SDK.git sdk
cd sdk

# Initialize submodules
git submodule update --init --recursive

# Build with Conan
conan install . -s compiler.cppstd=20 --build=missing
cd build && cmake .. && make
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add step definitions in `steps/*.cpp`
2. Build with `make build`
3. Run `make test` to verify tests pass
4. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
5. Update this file's coverage summary
6. Submit PR with test results

### Step Definition Pattern (C++)

```cpp
WHEN("I parse the address", [](const cuke::table&) {
    auto& w = cuke::context<TestWorld>();
    try {
        w.address = Aptos::Accounts::AccountAddress::FromHex(w.hex_string);
        w.address_valid = true;
    } catch (const std::exception& e) {
        w.last_error = e.what();
        w.address_valid = false;
    }
});
```

### Conditional Compilation

Step definitions use `#ifdef APTOS_SDK_AVAILABLE` to support both:

- Full SDK mode (when SDK is built and linked)
- Placeholder mode (allows scaffold to compile without SDK)

---

## 9. Test Results Matrix

> Last run: 2026-01-22

### By Feature Category

| Category                | Passed | Failed | Undefined | Total |
| ----------------------- | ------ | ------ | --------- | ----- |
| 01-core-types           | 22     | 1      | 41        | 64    |
| 02-cryptography         | 15     | 0      | 105       | 120   |
| 03-account-management   | 8      | 0      | 54        | 62    |
| 04-transaction-building | 4      | 0      | 82        | 86    |
| 05-api-clients          | 0      | 0      | 140       | 140   |
| 06-advanced             | 0      | 0      | 276       | 276   |

### Test Run Summary

```
Total: 49 passed, 1 failed, 748 undefined
```

### Implemented Tests Detail

| Feature               | Passing Tests                                  |
| --------------------- | ---------------------------------------------- |
| address.feature       | Parse with/without prefix, full hex, constants |
| ed25519.feature       | Random key generation, key from hex            |
| serialization.feature | Basic ULEB128 (scaffold)                       |
| hashing.feature       | SHA3-256 basic (scaffold)                      |

### Community SDK Notes

This is a community-maintained SDK from VAR-META-Tech. It may have:

- Different API patterns than official SDKs
- Features that differ from official releases

Check the [Aptos-Cpp-SDK repository](https://github.com/VAR-META-Tech/Aptos-Cpp-SDK) for updates.
