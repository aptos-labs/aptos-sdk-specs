# Feature Coverage Matrix

> **Last Updated:** 2026-03-20
>
> This file tracks implementation status of behavioral specifications across all SDK
> implementations. Check boxes indicate that step definitions exist and tests pass for that
> scenario.
>
> For detailed per-SDK information, see individual `SDK_STATUS.md` files in each `tests/<language>/`
> directory.

---

## SDK Information

| SDK        | Package              | Version    | Publisher     | Repository                                                         | Status                                    |
| ---------- | -------------------- | ---------- | ------------- | ------------------------------------------------------------------ | ----------------------------------------- |
| TypeScript | `@aptos-labs/ts-sdk` | ^5.2.0     | aptos-labs    | [aptos-ts-sdk](https://github.com/aptos-labs/aptos-ts-sdk)         | [Details](tests/typescript/SDK_STATUS.md) |
| Go         | `aptos-go-sdk`       | v1.11.0    | aptos-labs    | [aptos-go-sdk](https://github.com/aptos-labs/aptos-go-sdk)         | [Details](tests/go/SDK_STATUS.md)         |
| Rust       | `aptos-sdk`          | dev (git)  | aptos-labs    | [aptos-rust-sdk](https://github.com/aptos-labs/aptos-rust-sdk)     | [Details](tests/rust/SDK_STATUS.md)       |
| Java       | `japtos`             | 1.1.8      | aptos-labs    | [aptos-java-sdk](https://github.com/aptos-labs/aptos-java-sdk)     | [Details](tests/java/SDK_STATUS.md)       |
| Kotlin     | `aptos-kotlin-sdk`   | 0.1.0      | aptos-labs    | [aptos-kotlin-sdk](https://github.com/aptos-labs/aptos-kotlin-sdk) | [Details](tests/kotlin/SDK_STATUS.md)     |
| Python     | `aptos-sdk`          | >=0.11.0   | aptos-labs    | [aptos-python-sdk](https://github.com/aptos-labs/aptos-python-sdk) | [Details](tests/python/SDK_STATUS.md)     |
| .NET       | `Aptos`              | 0.0.x-beta | aptos-labs    | [aptos-dotnet-sdk](https://github.com/aptos-labs/aptos-dotnet-sdk) | [Details](tests/dotnet/SDK_STATUS.md)     |
| C++        | `Aptos-Cpp-SDK`      | dev        | VAR-META-Tech | [Aptos-Cpp-SDK](https://github.com/VAR-META-Tech/Aptos-Cpp-SDK)    | [Details](tests/cpp/SDK_STATUS.md)        |
| Swift      | `aptos-swift-sdk`    | main       | aptos-labs    | [aptos-swift-sdk](https://github.com/aptos-labs/aptos-swift-sdk)   | [Details](tests/swift/SDK_STATUS.md)      |

---

## Coverage Summary

> **Last verified:** 2026-02-23. Numbers reflect actual test runs.

| SDK        | Required (P0)  | Preferred (P1) | Optional (P2) | Total   | Notes                                            |
| ---------- | -------------- | -------------- | ------------- | ------- | ------------------------------------------------ |
| TypeScript | ~494/796 (62%) | included       | included      | 494/796 | 49 failed, 37 undefined; API tests need network  |
| Go         | 333/791 (42%)  | included       | included      | 333/791 | 136 failed, 312 pending, 10 undefined            |
| Rust       | 723/791 (91%)  | included       | included      | 723/791 | 56 skipped, 12 failed (network/benchmarks)       |
| .NET       | 478/808 (59%)  | included       | included      | 478/808 | 330 failures (last verified 2026-01-28)          |
| Python     | 459/791 (58%)  | included       | included      | 459/791 | 121 failed, 75 errors, 136 skipped               |
| Java       | 22/802 (3%)    | included       | included      | 22/802  | 780 errors, most steps undefined                 |
| Kotlin     | —              | —              | —             | —       | SDK not yet published to Maven Central           |
| C++        | 0/791 (0%)     | included       | included      | 0/791   | Segfault in test runner                          |
| Swift      | —              | —              | —             | —       | Not verified (Swift 6.0/Xcode required, new SDK) |

---

## Legend

### Test Status

- ✅ **Passing** - Test implemented and passing
- 🟡 **Partial** - Partially implemented or known issues
- ❌ **Not Implemented** - Test step definitions not yet written
- ➖ **N/A** - Feature not available in SDK (cannot be tested)

### Feature-Level Status

- ✅ **Full** - All tests passing (100%)
- 🟡 **Partial** - Some tests passing (1-99%)
- ❌ **None** - No tests passing (0%)
- ➖ **N/A** - Feature not available in SDK

---

## 01-core-types

### Feature Summary

| Feature           | TS       | Go       | Rust     | Java     | Kotlin | Python   | .NET     | C++      | Swift |
| ----------------- | -------- | -------- | -------- | -------- | ------ | -------- | -------- | -------- | ----- |
| **address**       | ✅ 22/22 | ✅ 22/22 | ✅ 22/22 | ✅ 22/22 | 🟡     | ✅ 22/22 | 🟡 18/22 | 🟡 21/22 | ✅ 32 |
| **serialization** | ✅ 18/18 | ✅ 18/18 | ✅ 18/18 | ✅ 18/18 | ❌     | 🟡 16/18 | 🟡 12/18 | 🟡 1/18  | ✅ 23 |
| **type-tags**     | ✅ 24/24 | ✅ 24/24 | ✅ 24/24 | ✅ 24/24 | ❌     | 🟡 22/24 | 🟡 16/24 | ❌ 0/24  | ✅ 32 |

### address.feature `@required`

| #   | Scenario                                          | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Parse hex address with 0x prefix                  | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 2   | Parse hex address without 0x prefix               | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 3   | Parse full 64-character hex address               | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 4   | Parse uppercase hex address                       | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 5   | Parse mixed case hex address                      | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 6   | Reject empty string                               | ✅  | ✅  | 🟡   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 7   | Reject just 0x prefix                             | ✅  | ✅  | 🟡   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 8   | Reject non-hex characters                         | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 9   | Reject address too long                           | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 10  | Reject address with spaces                        | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 11  | Format address to full hex                        | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 12  | Format address to short string                    | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 13  | Format zero address                               | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 14  | ZERO address constant                             | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 15  | ONE address constant (framework)                  | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 16  | THREE address constant (token)                    | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 17  | FOUR address constant (objects)                   | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 18  | Addresses parsed from equivalent inputs are equal | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 19  | Different addresses are not equal                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 20  | BCS serialize address                             | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 21  | BCS deserialize address                           | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 22  | BCS round-trip                                    | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |

### serialization.feature `@required`

| #   | Scenario                                         | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------------------ | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | ULEB128 round-trip                               | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 2   | Serialize empty bytes                            | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 3   | Serialize short bytes                            | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 4   | Serialize string                                 | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ✅  | ✅    |
| 5   | Serialize empty string                           | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 6   | Serialize string with unicode                    | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 7   | Serialize None option                            | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 8   | Serialize Some option with u64                   | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 9   | Serialize empty vector                           | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 10  | Serialize vector of u8                           | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 11  | Serialize vector of u64                          | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 12  | Serialize nested vector                          | ✅  | ✅  | ✅   | ✅   | ❌     | 🟡     | ❌   | ❌  | ✅    |
| 13  | Serialize AccountAddress                         | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 14  | Deserialize AccountAddress                       | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 15  | Serialize struct with multiple fields            | ✅  | ✅  | ✅   | ✅   | ❌     | 🟡     | ❌   | ❌  | ✅    |
| 16  | Fail to deserialize truncated data               | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 17  | Fail to deserialize invalid boolean              | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 18  | Fail to deserialize sequence with invalid length | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |

### type-tags.feature `@required`

| #   | Scenario                                  | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Format primitive types                    | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 2   | Parse vector of u8                        | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 3   | Parse nested vector                       | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 4   | Parse vector of struct                    | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 5   | Format vector type                        | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 6   | Parse simple struct type                  | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 7   | Parse struct with type argument           | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 8   | Parse struct with multiple type arguments | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 9   | Parse struct with full address            | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 10  | Format struct type without type args      | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 11  | Format struct type with type args         | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 12  | Reject empty type string                  | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 13  | Reject unknown primitive                  | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 14  | Reject malformed vector                   | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 15  | Reject unclosed vector bracket            | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 16  | Reject invalid struct format              | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 17  | Reject struct with invalid address        | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 18  | Parse module ID                           | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 19  | Format module ID                          | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 20  | Reject invalid module ID                  | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 21  | Create MoveStructTag from components      | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 22  | BCS serialize primitive TypeTag           | ✅  | ✅  | ✅   | ✅   | ❌     | 🟡     | ❌   | ❌  | ✅    |
| 23  | BCS serialize struct TypeTag              | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 24  | BCS round-trip for complex TypeTag        | ✅  | ✅  | ✅   | ✅   | ❌     | 🟡     | ❌   | ❌  | ✅    |

---

## 02-cryptography

### Feature Summary

| Feature                    | TS       | Go       | Rust     | Java     | Kotlin | Python   | .NET     | C++      | Swift |
| -------------------------- | -------- | -------- | -------- | -------- | ------ | -------- | -------- | -------- | ----- |
| **ed25519** `@required`    | ✅ 25/25 | 🟡 23/25 | ✅ 25/25 | ✅ 25/25 | 🟡     | 🟡 23/25 | 🟡 20/25 | 🟡 20/25 | ✅ 18 |
| **hashing** `@required`    | ✅ 20/20 | ✅ 20/20 | ✅ 20/20 | ✅ 20/20 | 🟡     | 🟡 19/20 | 🟡 12/20 | 🟡 7/20  | ✅ 9  |
| **secp256k1** `@preferred` | ✅ 19/19 | ➖       | ✅ 19/19 | ➖       | ➖     | ❌ 0/19  | ➖       | ➖       | ✅ 18 |
| **secp256r1** `@optional`  | ✅ 26/26 | ➖       | ✅ 26/26 | ➖       | ➖     | ❌ 0/26  | ➖       | ➖       | ➖    |

### ed25519.feature `@required`

| #   | Scenario                                        | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Generate random Ed25519 key pair                | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 2   | Generate unique key pairs                       | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 3   | Create key pair from 32-byte seed               | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 4   | Create key pair from 64-byte private key        | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 5   | Create key pair from hex string                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 6   | Reject invalid private key length               | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 7   | Sign a message                                  | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 8   | Sign empty message                              | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 9   | Sign produces deterministic signatures          | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 10  | Different messages produce different signatures | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 11  | Different keys produce different signatures     | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 12  | Verify valid signature                          | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 13  | Reject signature from wrong key                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 14  | Reject signature for wrong message              | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 15  | Reject malformed signature                      | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 16  | Reject truncated signature                      | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 17  | Export public key bytes                         | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 18  | Export private key bytes                        | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 19  | Export keys as hex                              | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ❌    |
| 20  | Derive auth key from Ed25519 public key         | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ❌    |
| 21  | Derive account address from auth key            | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 22  | Known test vector - key derivation              | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 23  | Known test vector - signing                     | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 24  | Private key is zeroized on drop                 | ✅  | ❌  | ✅   | ✅   | ➖     | ➖     | ➖   | ➖  | ➖    |
| 25  | Private key not in debug output                 | ✅  | ❌  | ✅   | ✅   | ➖     | ➖     | ➖   | ➖  | ➖    |

### hashing.feature `@required`

| #   | Scenario                                       | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ---------------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Compute SHA3-256 of empty data                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 2   | Compute SHA3-256 of "hello"                    | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 3   | SHA3-256 different hashes for different inputs | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 4   | SHA3-256 is deterministic                      | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 5   | Compute SHA3-256 of multiple parts             | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 6   | Compute SHA2-256 of empty data                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 7   | Compute SHA2-256 of "hello"                    | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 8   | SHA2-256 differs from SHA3-256                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ✅  | ✅    |
| 9   | Domain-separated hash for RawTransaction       | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 10  | Different domains produce different hashes     | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 11  | Domain hash prefix computed correctly          | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 12  | Create HashValue from bytes                    | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 13  | Create HashValue from hex                      | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 14  | Reject invalid HashValue length                | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 15  | HashValue ZERO constant                        | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 16  | Format HashValue as hex                        | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 17  | HashValue equality                             | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 18  | HashValue from SHA3-256                        | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ❌    |
| 19  | HMAC-SHA512 for BIP-39 seed derivation         | ✅  | ✅  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Hashing large data                             | ✅  | ✅  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |

### secp256k1.feature `@preferred`

| #   | Scenario                                   | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------------ | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Generate random Secp256k1 key pair         | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 2   | Create key pair from 32-byte private key   | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 3   | Create key pair from hex string            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 4   | Reject invalid private key (zero)          | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 5   | Reject invalid private key (> curve order) | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 6   | Get compressed public key                  | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 7   | Get uncompressed public key                | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 8   | Compressed/uncompressed same key           | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 9   | Sign a message                             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 10  | Deterministic signatures (RFC 6979)        | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 11  | Sign pre-hashed message                    | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 12  | Verify valid signature                     | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 13  | Reject signature from wrong key            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 14  | Reject malformed signature                 | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 15  | Derive auth key from Secp256k1             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 16  | Auth key uses scheme 0x01                  | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 17  | Test vector - key derivation               | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 18  | Test vector - signing                      | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ✅    |
| 19  | Test vector - address derivation           | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ❌    |

### secp256r1.feature `@optional`

| #   | Scenario                                   | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------------ | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Generate random Secp256r1 key pair         | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 2   | Create key pair from 32-byte private key   | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 3   | Create key pair from hex string            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 4   | Reject invalid private key (zero)          | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 5   | Reject invalid private key (> curve order) | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 6   | Get compressed public key                  | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 7   | Get uncompressed public key                | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 8   | Parse compressed public key                | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 9   | Parse uncompressed public key              | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 10  | Sign a message                             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 11  | Deterministic signatures (RFC 6979)        | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 12  | Sign with SHA-256 pre-hash                 | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 13  | Verify valid signature                     | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 14  | Reject signature from wrong key            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 15  | Reject malformed signature                 | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 16  | Derive auth key from Secp256r1             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 17  | Secp256r1 uses scheme 0x02                 | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 18  | Secp256r1 addr differs from Secp256k1      | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 19  | Parse WebAuthn public key                  | ✅  | ➖  | ❌   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 20  | Verify WebAuthn assertion signature        | ✅  | ➖  | ❌   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 21  | Signature format compatibility             | ✅  | ➖  | ❌   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 22  | Create Secp256r1 account                   | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 23  | Sign transaction with Secp256r1            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 24  | Test vector - key derivation               | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 25  | Test vector - signing                      | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 26  | Test vector - address                      | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |

---

## 03-account-management

### Feature Summary

| Feature                              | TS       | Go       | Rust     | Java     | Kotlin | Python   | .NET     | C++     | Swift |
| ------------------------------------ | -------- | -------- | -------- | -------- | ------ | -------- | -------- | ------- | ----- |
| **authentication-key** `@required`   | ✅ 17/17 | 🟡 12/17 | ✅ 17/17 | ✅ 17/17 | 🟡     | 🟡 9/17  | 🟡 10/17 | ❌ 0/17 | ✅ 8  |
| **single-key** `@required`           | ✅ 28/28 | 🟡 17/28 | ✅ 28/28 | ✅ 28/28 | 🟡     | 🟡 13/28 | 🟡 18/28 | ❌ 0/28 | ✅ 22 |
| **mnemonic-derivation** `@preferred` | ✅ 29/29 | ➖       | ✅ 29/29 | ➖       | ➖     | ❌ 0/29  | ➖       | ❌ 0/29 | ✅ 9  |

### authentication-key.feature `@required`

| #   | Scenario                                  | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Derive auth key from Ed25519 pubkey       | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 2   | Auth key uses Ed25519 scheme id           | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 3   | Same pubkey produces same auth key        | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 4   | Different pubkeys different auth keys     | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 5   | Derive auth key from Secp256k1            | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 6   | Secp256k1 uses uncompressed pubkey        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 7   | Secp256k1 uses scheme 0x01                | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 8   | Derive auth key from arbitrary key/scheme | ✅  | ❌  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 9   | Convert auth key to account address       | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 10  | New account addr equals auth key          | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 11  | Auth key from_bytes                       | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 12  | Auth key as bytes                         | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 13  | Auth key to hex                           | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 14  | Test vector - Ed25519 auth key            | ✅  | ✅  | ✅   | ✅   | ✅     | 🟡     | ✅   | ❌  | ❌    |
| 15  | Test vector - Secp256k1 auth key          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Reject invalid auth key length            | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |
| 17  | Handle all-zero auth key                  | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ❌    |

### single-key.feature `@required`

| #   | Scenario                                  | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Generate random Ed25519 account           | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 2   | Generated accounts are unique             | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 3   | Create Ed25519 account from privkey bytes | ✅  | ✅  | ✅   | ✅   | ✅     | 🟡     | ✅   | ❌  | ✅    |
| 4   | Create Ed25519 account from hex string    | ✅  | ✅  | ✅   | ✅   | ✅     | 🟡     | ✅   | ❌  | ✅    |
| 5   | Create Ed25519 from 64-byte expanded key  | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 6   | Load account from AIP-80 string           | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 7   | Export account to AIP-80 string           | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 8   | Ed25519 account public key                | ✅  | ✅  | ✅   | ✅   | ✅     | 🟡     | ✅   | ❌  | ✅    |
| 9   | Ed25519 account auth key                  | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 10  | Ed25519 account address                   | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 11  | Sign message with Ed25519 account         | ✅  | ✅  | ✅   | ✅   | ✅     | 🟡     | ✅   | ❌  | ✅    |
| 12  | Sign transaction with Ed25519             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 13  | Verify signature from Ed25519             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 14  | Reject sig from different Ed25519         | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 15  | Generate random Secp256k1 account         | ✅  | ❌  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 16  | Create Secp256k1 from private key         | ✅  | ❌  | ✅   | ✅   | ❌     | ✅     | ❌   | ❌  | ✅    |
| 17  | Secp256k1 addr differs from Ed25519       | ✅  | ❌  | ✅   | ✅   | ❌     | 🟡     | ❌   | ❌  | ✅    |
| 18  | Sign message with Secp256k1               | ✅  | ❌  | ✅   | ✅   | ❌     | 🟡     | ❌   | ❌  | ✅    |
| 19  | Sign transaction with Secp256k1           | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Secp256k1 signature is recoverable        | ✅  | ❌  | ❌   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Test vector - Ed25519 account             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 22  | Test vector - Secp256k1 account           | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Reject invalid private key length         | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 24  | Reject invalid hex string                 | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 25  | Account equality by address               | ✅  | ✅  | ✅   | ✅   | ✅     | ✅     | ✅   | ❌  | ✅    |
| 26  | Private key not exposed accidentally      | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Private key export requires explicit      | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | AIP-80 format is ed25519-priv-...         | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |

### mnemonic-derivation.feature `@preferred`

| #   | Scenario                                  | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Generate 12-word mnemonic                 | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 2   | Generate 24-word mnemonic                 | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 3   | Generated mnemonics are unique            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 4   | Mnemonic words from BIP-39 wordlist       | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 5   | Parse valid mnemonic phrase               | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 6   | Mnemonic parsing case-insensitive         | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 7   | Reject invalid mnemonic word              | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 8   | Reject mnemonic wrong word count          | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 9   | Reject mnemonic invalid checksum          | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ✅    |
| 10  | Derive Ed25519 from mnemonic default      | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 11  | Derive Ed25519 with custom path           | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 12  | Same mnemonic same account                | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 13  | Different mnemonics different accounts    | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 14  | Different paths different accounts        | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 15  | Derive multiple accounts from one         | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 16  | Derive Secp256k1 from mnemonic            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 17  | Ed25519/Secp256k1 same mnemonic diff addr | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 18  | Derive account with passphrase            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 19  | Different passphrases different accounts  | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 20  | No passphrase = empty passphrase          | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 21  | Test vector - 12 word mnemonic            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 22  | Test vector - with passphrase             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 23  | Test vector - multiple indices            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 24  | Valid derivation path formats             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 25  | Reject path - missing m                   | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 26  | Reject path - wrong coin type             | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 27  | Reject path - non-hardened required       | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 28  | Mnemonic phrase retrievable               | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |
| 29  | Seed zeroized after derivation            | ✅  | ➖  | ✅   | ➖   | ➖     | ❌     | ➖   | ❌  | ❌    |

---

## 04-transaction-building

### Feature Summary

| Feature                         | TS       | Go       | Rust     | Java     | Kotlin | Python  | .NET     | C++     | Swift |
| ------------------------------- | -------- | -------- | -------- | -------- | ------ | ------- | -------- | ------- | ----- |
| **entry-function** `@required`  | ✅ 24/24 | 🟡 22/24 | ✅ 24/24 | ✅ 24/24 | 🟡     | ❌ 0/24 | 🟡 18/24 | ❌ 0/24 | ❌    |
| **raw-transaction** `@required` | ✅ 21/21 | 🟡 18/21 | ✅ 21/21 | ✅ 21/21 | 🟡     | ❌ 0/21 | 🟡 16/21 | ❌ 0/21 | ❌    |
| **signing** `@required`         | ✅ 24/24 | 🟡 17/24 | ✅ 24/24 | ✅ 24/24 | 🟡     | ❌ 0/24 | 🟡 15/24 | ❌ 0/24 | ❌    |
| **script** `@optional`          | 🟡 15/25 | ❌ 0/25  | ❌ 0/25  | ❌ 0/25  | ❌     | ❌ 0/25 | ❌ 0/25  | ❌ 0/25 | ❌    |

### entry-function.feature `@required`

| #   | Scenario                               | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | -------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Entry func payload no args             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 2   | Entry func payload u64 arg             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 3   | Entry func payload address arg         | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 4   | Entry func payload string arg          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 5   | Entry func payload vector arg          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 6   | Entry func payload bool arg            | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 7   | Entry func payload multiple args       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 8   | Entry func with type args              | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 9   | Entry func multiple type args          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 10  | BCS serialize entry func payload       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 11  | BCS deserialize entry func payload     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 12  | Entry func serialization deterministic | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 13  | Serialize u8 argument                  | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 14  | Serialize u16 argument                 | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 15  | Serialize u32 argument                 | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 16  | Serialize u64 argument                 | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 17  | Serialize u128 argument                | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 18  | Serialize u256 argument                | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 19  | Serialize nested vector arg            | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 20  | Serialize optional arg (Some)          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Serialize optional arg (None)          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Reject invalid module address          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 23  | Reject empty function name             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 24  | Test vector - entry function           | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |

### raw-transaction.feature `@required`

| #   | Scenario                               | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | -------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Create raw tx with required fields     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 2   | Raw tx has correct sender              | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 3   | Raw tx has correct sequence number     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 4   | Raw tx has correct max gas             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 5   | Raw tx has correct gas unit price      | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 6   | Raw tx has correct expiration          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 7   | Raw tx has correct chain ID            | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 8   | BCS serialize raw tx                   | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 9   | BCS deserialize raw tx                 | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 10  | Raw tx serialization deterministic     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 11  | Compute signing message from raw tx    | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 12  | Signing message uses domain separation | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 13  | Signing message is deterministic       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 14  | Different txs different signing msgs   | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 15  | Set expiration from duration           | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Set expiration from timestamp          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Reject zero max gas                    | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 18  | Reject zero gas unit price             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 19  | Reject expired transaction             | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Test vector - raw transaction          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 21  | Test vector - signing message          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |

### signing.feature `@required`

| #   | Scenario                              | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Sign raw tx with Ed25519              | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 2   | Signed tx contains original raw tx    | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 3   | Signed tx contains authenticator      | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 4   | Ed25519 authenticator structure       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 5   | BCS serialize signed tx               | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 6   | BCS deserialize signed tx             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 7   | Signed tx serialization deterministic | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 8   | Compute transaction hash              | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 9   | Tx hash is deterministic              | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 10  | Tx hash uses signed tx bytes          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 11  | Different signed txs different hashes | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 12  | Verify signed tx signature            | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 13  | Reject tampered transaction           | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 14  | Reject wrong signer                   | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 15  | Sign with Secp256k1 account           | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Secp256k1 authenticator structure     | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Verify Secp256k1 signed tx            | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | SingleKey authenticator wrapper       | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Sign tx twice same result             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 20  | Cannot sign with wrong chain ID       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 21  | Test vector - Ed25519 signing         | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 22  | Test vector - tx hash                 | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 23  | Test vector - Secp256k1 signing       | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Test vector - SingleKey auth          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |

### script.feature `@optional`

| #   | Scenario                            | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Create script payload from bytecode | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Script payload with no arguments    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Script payload with arguments       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Script payload with type arguments  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | BCS serialize script payload        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | BCS deserialize script payload      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Script serialization deterministic  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Compile Move script                 | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Compile script with dependencies    | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Compile script with arguments       | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Reject invalid Move script          | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Load script from file               | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Load script from hex string         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Create raw tx with script payload   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Sign and submit script tx           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Script with signer argument         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Script accesses sender              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Script with multiple signers        | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Script timeout and gas              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Inline script in transaction        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Complex script with loops           | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Script calling module functions     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Script with abort                   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Script return values                | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Test vector - script payload        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

---

## 05-api-clients

### Feature Summary

| Feature                                | TS       | Go       | Rust     | Java     | Kotlin | Python  | .NET     | C++     | Swift |
| -------------------------------------- | -------- | -------- | -------- | -------- | ------ | ------- | -------- | ------- | ----- |
| **fullnode-api** `@required`           | ✅ 25/25 | 🟡 19/25 | ✅ 25/25 | ✅ 25/25 | 🟡     | ❌ 0/25 | 🟡 18/25 | ❌ 0/25 | ✅ 19 |
| **transaction-submission** `@required` | 🟡 27/28 | 🟡 18/28 | ✅ 28/28 | ✅ 28/28 | 🟡     | ❌ 0/28 | 🟡 16/28 | ❌ 0/28 | ❌    |
| **faucet** `@preferred`                | ✅ 23/23 | ❌ 0/23  | ❌ 0/23  | ❌ 0/23  | ❌     | ❌ 0/23 | ❌ 0/23  | ❌ 0/23 | ❌    |
| **gas-estimation** `@preferred`        | 🟡 24/26 | ❌ 0/26  | ❌ 0/26  | ❌ 0/26  | ❌     | ❌ 0/26 | ❌ 0/26  | ❌ 0/26 | ❌    |
| **view-functions** `@preferred`        | ✅ 28/28 | ❌ 0/28  | ❌ 0/28  | ❌ 0/28  | ❌     | ❌ 0/28 | ❌ 0/28  | ❌ 0/28 | ❌    |
| **retry** `@preferred`                 | 🟡 25/32 | ❌ 0/32  | ❌ 0/32  | ❌ 0/32  | ❌     | ❌ 0/32 | ❌ 0/32  | ❌ 0/32 | ❌    |
| **indexer** `@optional`                | ✅ 31/31 | ❌ 0/31  | ❌ 0/31  | ❌ 0/31  | ❌     | ❌ 0/31 | ❌ 0/31  | ❌ 0/31 | ❌    |

### fullnode-api.feature `@required`

| #   | Scenario                            | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Create API client with URL          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 2   | API client URL normalization        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 3   | API client with custom headers      | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 4   | Get ledger info                     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 5   | Ledger info contains chain ID       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 6   | Ledger info contains epoch          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 7   | Ledger info contains ledger version | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 8   | Get account info                    | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 9   | Account info contains seq number    | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 10  | Account info contains auth key      | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 11  | Get account not found               | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 12  | Get account resources               | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 13  | Get specific account resource       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 14  | Get account modules                 | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ✅    |
| 15  | Get transaction by hash             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 16  | Get transaction by version          | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 17  | Get transactions                    | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 18  | Get account transactions            | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 19  | Check transaction success           | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ✅    |
| 20  | Check transaction failure           | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 21  | Get events by event key             | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Get events by creation number       | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Handle API 404 error                | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 24  | Handle API 400 error                | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 25  | Handle network error                | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |

### transaction-submission.feature `@required`

| #   | Scenario                           | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ---------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Submit valid signed tx             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 2   | Submit tx correct content type     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 3   | Submit tx returns hash             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 4   | Reject invalid tx format           | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 5   | Reject tx with invalid signature   | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 6   | Reject tx with wrong chain ID      | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 7   | Reject expired transaction         | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Wait for tx success                | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 9   | Wait for tx timeout                | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Wait returns success status        | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 11  | Wait returns failure status        | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 12  | Wait polls until completion        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Submit and wait for tx             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 14  | Sign, submit, and wait             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 15  | Simulate transaction               | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Simulate shows gas estimate        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Simulate shows VM error            | 🟡  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Simulate with insufficient balance | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Simulate no valid sig required     | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Get gas price estimate             | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Use gas estimate for tx            | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Get current sequence number        | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 23  | Submit with correct seq number     | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 24  | Reject wrong sequence number       | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |
| 25  | Submit multiple txs in sequence    | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Handle submission network error    | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Handle VM error in response        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | Tx hash is predictable             | ✅  | ✅  | ✅   | ✅   | ✅     | ❌     | ✅   | ❌  | ❌    |

### faucet.feature `@preferred`

| #   | Scenario                           | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ---------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Fund account default amount        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Fund account specific amount       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Faucet returns tx hashes           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Fund creates account if not exists | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Fund adds to existing balance      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Configure faucet URL               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Use devnet faucet                  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Use testnet faucet                 | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Faucet not available on mainnet    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Wait for faucet transaction        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Fund and wait in one call          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Handle faucet rate limiting        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Handle faucet service unavailable  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Faucet timeout                     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Fund multiple accounts             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Fund with authentication           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Balance after funding              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | New account zero initial balance   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Fund non-existent address format   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Reject invalid faucet URL          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Faucet tx is coin transfer         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Fund integration test accounts     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Parallel funding                   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### gas-estimation.feature `@preferred`

| #   | Scenario                         | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | -------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Get current gas price            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Gas price is in octas            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Gas price varies by network load | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Estimate gas for simple transfer | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Estimate gas for entry func call | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Estimate gas for complex tx      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Gas estimate via simulation      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Simulation returns gas_used      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Add buffer to gas estimate       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Calculate total fee from gas     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Prioritized gas price            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Deprioritized gas price          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Auto-set gas unit price          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Auto-set max gas amount          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Override auto gas settings       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Estimate fails for invalid tx    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Estimate for multi-agent tx      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Estimate for fee payer tx        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Historical gas prices            | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Gas price percentiles            | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Min and max gas price bounds     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Gas estimation timeout           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Estimate with specific account   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Estimate w/o account (sim only)  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Gas varies by payload size       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Storage gas costs                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### view-functions.feature `@preferred`

| #   | Scenario                        | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Execute simple view function    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | View func without type args     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | View func without args          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | View func with multiple returns | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Pass address argument           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Pass u64 argument               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Pass string argument            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Pass vector argument            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Pass bool argument              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Single type argument            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Multiple type arguments         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Nested type argument            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Parse u64 return value          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Parse string return value       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Parse bool return value         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Parse vector return value       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Parse struct return value       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | View function not found         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Invalid arguments               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Wrong number of arguments       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Wrong number of type arguments  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | View function aborts            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Get coin balance                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Check account exists            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Get current timestamp           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Get coin supply                 | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | View func at specific version   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | View func at too old version    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### retry.feature `@preferred`

| #   | Scenario                       | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------ | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Retry on network timeout       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Retry on connection refused    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Retry on 5xx server error      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | No retry on 4xx client error   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Configure max retry attempts   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Configure retry delay          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Exponential backoff            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Jitter in retry delay          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Max retry delay cap            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Retry callback/hook            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Custom retry condition         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Retry specific status codes    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | No retry by default            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Retry preserves request        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Total timeout across retries   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Circuit breaker pattern        | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Retry on rate limit (429)      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Respect Retry-After header     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Retry only idempotent ops      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | No retry on submit             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Retry with fresh data          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Log retry attempts             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Retry statistics               | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Abort retry on fatal error     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Graceful degradation           | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Retry for wait_for_transaction | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Tx not found during retry      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | Health check before retry      | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 29  | Per-endpoint retry config      | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 30  | Retry context propagation      | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 31  | Retry metrics/telemetry        | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 32  | Concurrent request retry       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### indexer.feature `@optional`

| #   | Scenario                      | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ----------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Create indexer client         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Configure indexer URL         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Query account tokens          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Query token by ID             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Query collection              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Query account NFTs            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Query fungible asset balances | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Query fungible asset metadata | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Query coin activities         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Query token activities        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Query events by type          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Query events by account       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Query txs by account          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Query txs by function         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Query with pagination         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Query with limit              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Query with offset             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Query with ordering           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Query with filtering          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Query with multiple filters   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Raw GraphQL query             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | GraphQL query variables       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Handle indexer lag            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Handle indexer unavailable    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Handle invalid query          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Account current holdings      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Account tx history            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | Get ANS name for address      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 29  | Get address for ANS name      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 30  | Query processor status        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 31  | Query latest indexed version  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

---

## 06-advanced

### Feature Summary

| Feature                         | TS       | Go      | Rust     | Java     | Kotlin | Python  | .NET     | C++     | Swift |
| ------------------------------- | -------- | ------- | -------- | -------- | ------ | ------- | -------- | ------- | ----- |
| **error-handling** `@required`  | 🟡 28/30 | 🟡 1/30 | 🟡 27/30 | 🟡 28/30 | 🟡     | ❌ 0/30 | 🟡 15/30 | ❌ 0/30 | ❌    |
| **simulation** `@preferred`     | 🟡 26/31 | ❌ 0/31 | ❌ 0/31  | ❌ 0/31  | ❌     | ❌ 0/31 | ❌ 0/31  | ❌ 0/31 | ❌    |
| **multi-agent** `@optional`     | ✅ 20/20 | ❌ 0/20 | ❌ 0/20  | ❌ 0/20  | ❌     | ❌ 0/20 | ❌ 0/20  | ❌ 0/20 | ❌    |
| **fee-payer** `@optional`       | ✅ 23/23 | ❌ 0/23 | ❌ 0/23  | ❌ 0/23  | ❌     | ❌ 0/23 | ❌ 0/23  | ❌ 0/23 | ❌    |
| **multi-signature** `@optional` | ✅ 23/23 | ❌ 0/23 | ❌ 0/23  | ❌ 0/23  | ❌     | ❌ 0/23 | ❌ 0/23  | ❌ 0/23 | ❌    |
| **keyless** `@optional`         | ✅ 33/33 | ❌ 0/33 | ❌ 0/33  | ❌ 0/33  | ❌     | ❌ 0/33 | ❌ 0/33  | ❌ 0/33 | ❌    |
| **codegen** `@optional`         | ❌ 0/34  | ❌ 0/34 | ❌ 0/34  | ❌ 0/34  | ❌     | ❌ 0/34 | ❌ 0/34  | ❌ 0/34 | ❌    |

### error-handling.feature `@required`

| #   | Scenario                         | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | -------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Network errors distinguishable   | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | API errors include status code   | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Validation errors informative    | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Tx errors include details        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Parse success status             | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Parse execution failure          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Parse out of gas failure         | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Parse sequence number error      | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Parse insufficient balance error | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Recognize standard abort codes   | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Custom module abort codes        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Errors include operation context | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Errors are chainable             | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Errors include request ID        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | TypeScript uses typed errors     | ✅  | ➖  | ➖   | ➖   | ➖     | ➖     | ➖   | ➖  | ➖    |
| 16  | Rust uses Result types           | ➖  | ➖  | ✅   | ➖   | ➖     | ➖     | ➖   | ➖  | ➖    |
| 17  | Python uses exceptions           | ➖  | ➖  | ➖   | ➖   | ➖     | ❌     | ➖   | ➖  | ➖    |
| 18  | Go uses error interface          | ➖  | ✅  | ➖   | ➖   | ➖     | ➖     | ➖   | ➖  | ➖    |
| 19  | Identify retryable errors        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Identify permanent failures      | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Simulation failure with details  | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Simulation gas estimation        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Tx not found during wait         | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Tx failed during wait            | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Error messages actionable        | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | No internal jargon in errors     | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Errors are loggable              | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | Sequence number recovery         | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 29  | Gas estimation recovery          | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 30  | Rate limit recovery              | ✅  | ❌  | ✅   | ✅   | ❌     | ❌     | ❌   | ❌  | ❌    |

### simulation.feature `@preferred`

| #   | Scenario                              | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Simulate valid transaction            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Simulate without signing              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Simulation result includes changes    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Use simulation for gas estimation     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Simulation shows max_gas_amount       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Gas varies by tx complexity           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Preview balance changes               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Preview resource changes              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Preview events                        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Simulation shows abort                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Simulation shows insufficient balance | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Simulation shows type errors          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Simulation catches access errors      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Simulate at specific version          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Simulate with gas override            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Simulate with gas price override      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Multi-agent sim with sender pubkey    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Multi-agent sim without pubkeys       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Multi-agent sim with partial checks   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Reject malformed signer key mapping   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Multi-agent sim includes changes      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Multi-agent + fee payer sim (skip)    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Multi-agent + fee payer sim (keys)    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Simulation doesn't commit             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Simulation may differ from exec       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Simulation with current seq           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Simulate multiple txs                 | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | Simulate tx sequence                  | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 29  | Simulation network error              | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 30  | Invalid tx for simulation             | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 31  | Simulation timeout                    | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### multi-agent.feature `@optional`

| #   | Scenario                                   | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------------ | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Multi-agent tx with one secondary          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Multi-agent tx with multiple secondary     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Secondary signer addrs preserved           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Multi-agent msg differs from single        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Multi-agent msg includes secondary addrs   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Multi-agent msg correct domain             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | All parties sign same message              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Sign multi-agent tx                        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Multi-agent authenticator structure        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Multi-agent with mixed account types       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Collect sigs from multiple parties         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Sigs can be collected any order            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Reject incomplete sig collection           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Reject mismatched secondary count          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Reject empty secondary signers             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Secondary addr must match sig              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Serialize multi-agent authenticator        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Multi-agent tx serialization deterministic | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Test vector - multi-agent signing msg      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Test vector - multi-agent tx               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### fee-payer.feature `@optional`

| #   | Scenario                                 | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ---------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Create fee payer tx with sponsor         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Fee payer tx with secondary signers      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Fee payer addr preserved                 | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Fee payer msg differs from multi-agent   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Fee payer msg includes fee payer addr    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Fee payer msg correct domain             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | All parties sign same message            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Sign fee payer tx                        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Fee payer authenticator structure        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Fee payer with no secondary              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Fee payer with mixed account types       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Sender initiates sponsored tx            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Sponsor completes sponsored tx           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Sigs can be collected any order          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Fee payer pays gas always                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Tx fails if fee payer insufficient gas   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Reject missing fee payer sig             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Reject missing sender sig                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Fee payer addr must match sig            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Serialize fee payer authenticator        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Fee payer tx serialization deterministic | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Test vector - fee payer signing msg      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Test vector - fee payer tx               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### multi-signature.feature `@optional`

| #   | Scenario                             | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | ------------------------------------ | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Create 2-of-3 multi-sig account      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Create 1-of-1 multi-sig account      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Multi-sig with all keys required     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Reject threshold of 0                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Reject threshold > key count         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Reject empty key list                | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Multi-sig auth key derivation        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Key order affects auth key           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Same keys same order same addr       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Sign with enough private keys        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Cannot sign without enough keys      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Collect sigs from multiple parties   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Reject duplicate signer indices      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Reject invalid signer index          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Multi-sig signature contains indices | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Sigs are ordered by index            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Sign tx with multi-sig account       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Multi-sig tx authenticator structure | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Verify multi-sig signature           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Reject sig with insufficient signers | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Reject sig with wrong signers        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Test vector - multi-sig addr         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Test vector - multi-sig signature    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### keyless.feature `@optional`

| #   | Scenario                                | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | --------------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Generate ephemeral key pair             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Ephemeral key pair unique nonce         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Check ephemeral key expiry              | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Fresh ephemeral key not expired         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Get ephemeral nonce for OIDC            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Create keyless account from JWT         | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Keyless account correct provider        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Keyless address is deterministic        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Different users different addresses     | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Keyless address derivation formula      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Different issuers different addresses   | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Different audiences different addresses | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Pepper affects address                  | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Sign message with keyless account       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Sign tx with keyless account            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Reject signing expired ephemeral        | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Check if keyless account valid          | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Keyless account expired proof           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Refresh proof                           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Google provider configuration           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Apple provider configuration            | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Custom OIDC provider                    | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Get pepper for JWT                      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Same JWT produces same pepper           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Handle pepper service error             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Generate ZK proof                       | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | Handle prover service error             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | Reject invalid JWT format               | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 29  | Reject JWT with wrong nonce             | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 30  | Reject expired JWT                      | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 31  | Ephemeral key expiry enforced           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 32  | Pepper not exposed in account           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 33  | Test vector - keyless address           | ✅  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

### codegen.feature `@optional`

| #   | Scenario                          | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| --- | --------------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| 1   | Fetch module ABI from chain       | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 2   | Fetch ABI for multiple modules    | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 3   | Handle module not found           | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 4   | Parse entry functions from ABI    | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 5   | Parse view functions from ABI     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 6   | Parse struct definitions from ABI | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 7   | Parse generic types               | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 8   | Generate TS types for structs     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 9   | Generate TS function wrappers     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 10  | Generate TS view func wrappers    | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 11  | Map Move types to TS              | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 12  | Generate Rust types for structs   | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 13  | Generate Rust func wrappers       | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 14  | Map Move types to Rust            | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 15  | Generate Python types for structs | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 16  | Generate Python func wrappers     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 17  | Generate Go types for structs     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 18  | Generate Go func wrappers         | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 19  | Code handles address encoding     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 20  | Code handles u64 encoding         | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 21  | Code handles vector encoding      | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 22  | Code handles struct encoding      | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 23  | Compile-time type checking        | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 24  | Type inference for generics       | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 25  | Optional parameters handling      | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 26  | Generate code via CLI             | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 27  | CLI multiple output formats       | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 28  | CLI from local ABI file           | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 29  | Procedural macro for bindings     | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 30  | Macro fetches ABI at build        | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 31  | Code surfaces Move errors         | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 32  | Code validates arguments          | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 33  | Generate documentation comments   | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |
| 34  | Include func signatures in docs   | ❌  | ❌  | ❌   | ❌   | ❌     | ❌     | ❌   | ❌  | ❌    |

---

## Performance Benchmarks

> **Last Updated:** 2026-01-23  
> **Network:** Devnet  
> **Hardware:** Apple Silicon (arm64)  
> **Note:** Results vary by network conditions, hardware, and geographic location. Compare SDKs on
> same machine for fairness.

### REST API Read Performance (avg ms)

| Operation               | TS  | Go      | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| ----------------------- | --- | ------- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| Get Ledger Info         | -   | **59**  | -    | -    | -      | -      | -    | -   | -     |
| Get Account Info        | -   | **62**  | -    | -    | -      | -      | -    | -   | -     |
| Get Account Resources   | -   | **169** | -    | -    | -      | -      | -    | -   | -     |
| Get Transaction by Hash | -   | -       | -    | -    | -      | -      | -    | -   | -     |
| Get Account Balance     | -   | **66**  | -    | -    | -      | -      | -    | -   | -     |

### GraphQL/Indexer Read Performance (avg ms)

| Operation                  | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| -------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| Query Account Tokens       | -   | -   | -    | -    | -      | -      | -    | -   | -     |
| Query Account Transactions | -   | -   | -    | -    | -      | -      | -    | -   | -     |
| Query Fungible Assets      | -   | -   | -    | -    | -      | -      | -    | -   | -     |
| Query Events               | -   | -   | -    | -    | -      | -      | -    | -   | -     |

### Transaction Performance (avg ms)

| Operation                  | TS  | Go  | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| -------------------------- | --- | --- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| Build + Sign Transaction   | -   | -   | -    | -    | -      | -      | -    | -   | -     |
| Submit (no wait)           | -   | -   | -    | -    | -      | -      | -    | -   | -     |
| Submit + Wait (round-trip) | -   | -   | -    | -    | -      | -      | -    | -   | -     |
| Full Flow (incl. simulate) | -   | -   | -    | -    | -      | -      | -    | -   | -     |

### Cryptographic Operations (avg μs)

| Operation                 | TS    | Go        | Rust | Java | Kotlin | Python | .NET | C++ | Swift |
| ------------------------- | ----- | --------- | ---- | ---- | ------ | ------ | ---- | --- | ----- |
| Ed25519 Key Generation    | 156   | **10.8**  | -    | -    | -      | -      | -    | -   | -     |
| Ed25519 Signing           | 274   | **13.2**  | -    | -    | -      | -      | -    | -   | -     |
| Ed25519 Verification      | 1,223 | **35.6**  | -    | -    | -      | -      | -    | -   | -     |
| BCS Serialize Address     | 0.41  | **0.014** | -    | -    | -      | -      | -    | -   | -     |
| SHA3-256 Hash (256 bytes) | 6.7   | **0.54**  | -    | -    | -      | -      | -    | -   | -     |

### Running Performance Tests

```bash
# TypeScript - Standalone benchmark
cd tests/typescript && bun benchmark.ts

# Go - Standalone benchmark
cd tests/go && go run benchmark.go

# Go - Cucumber-based (crypto only)
cd tests/go && GODOG_TAGS="@crypto" go test -v ./...

# Rust
cd tests/rust && cargo test --test performance

# Python
cd tests/python && pytest tests/performance/ -v

# Java
cd tests/java && mvn test -Dtest=PerformanceTests

# Swift
cd tests/swift && swift test --filter Performance
```

### Performance Test Specification

See [features/07-performance/spec.md](features/07-performance/spec.md) for methodology details.

---

## Maintenance

This file should be updated when:

1. New step definitions are added to any SDK
2. Tests are verified to pass
3. New scenarios are added to feature files

To check current status, run:

```bash
# TypeScript
cd tests/typescript && bun run cucumber-js --dry-run --format summary

# Go
cd tests/go && go test -v ./...

# Rust
cd tests/rust && cargo test --test specs
```

---

## Follow-Ups by SDK

### TypeScript (`@aptos-labs/ts-sdk` ^5.2.0) — [Full Status](tests/typescript/SDK_STATUS.md)

**Status:** Most complete implementation (reference SDK)

**Verified:** 2026-02-23 via `bun run cucumber-js`

**Test Results (non-network, non-performance):**

- 585 scenarios in this bucket (`not (@api-clients or @network or @performance)`)
- 2220 steps: 1993 passed, 49 failed, 132 undefined, 46 skipped
- api-clients: Requires network (133 scenarios for
  `@api-clients and not (@network or @performance)`; 193 total `@api-clients` scenarios)

**Mocked Tests (not real implementations):**

- `keyless.feature`: All scenarios use mock JWTs (real OIDC requires external providers)
- `script.feature` (partial): Mock RawTransaction for scripts
- `secp256r1.feature` (signing): Mock transaction message

**Missing/Failing Features:**

- `secp256r1`: 13 failures in cryptography (Secp256r1 address derivation issues)
- `simulation`: Some failures in advanced (gas charging assertions)
- `codegen.feature`: All 34 scenarios undefined (not implemented)
- `gas-estimation.feature` #19-20: Historical gas prices not implemented
- `retry.feature` #16, #23, #25, #28-31: Circuit breaker, statistics

---

### Go (`aptos-go-sdk` v1.11.0) — [Full Status](tests/go/SDK_STATUS.md)

**Status:** Core functionality (333/791 passing = 42%)

**Verified:** 2026-02-23 via `go test -v ./...`

**Test Results:**

- 333 passed, 136 failed, 312 pending, 10 undefined
- 1897 steps passed, 136 failed, 312 pending, 11 undefined, 702 skipped
- Duration: ~33 seconds

**Known Failures (136 total):**

- SDK limitations (Secp256r1/MultiEd25519/MultiKey keys, coin module)
- Network-dependent scenarios
- Missing API methods for some advanced features

**Pending (312 scenarios):**

- Step definitions exist but return `godog.ErrPending`
- Features not available in SDK: keyless, codegen, most advanced features

**Undefined (10 scenarios):**

- Secp256r1-related steps (P-256 curve not in SDK)

**SDK Gaps (features not available):**

- Secp256r1 cryptography
- Mnemonic/HD derivation
- AIP-80 key format
- Keyless authentication
- Code generation

---

### Rust (`aptos-sdk` dev) — [Full Status](tests/rust/SDK_STATUS.md)

**Status:** Excellent coverage (723/791 passing = 91%)

**Verified:** 2026-02-23 via `cargo test --test specs`

**Results:**

- 723 passed, 56 skipped, 12 failed
- All 12 failures are network-dependent performance benchmarks (require devnet access)
- 56 skipped scenarios are for features not yet tested
- Duration: ~110 seconds

**Note:** Tests depend on `aptos-sdk` from GitHub (`https://github.com/aptos-labs/aptos-rust-sdk`),
which is not yet on crates.io.

**Recent Fixes (2026-02-06):**

- Updated `get_apt_balance()` to `get_balance()` (method renamed in SDK)
- Replaced `get_account_transactions()` (removed from SDK) with alternative API calls
- Fixed `to_string()` to `to_long_string()` for full hex address formatting

---

### Java (`japtos` 1.1.8) — [Full Status](tests/java/SDK_STATUS.md)

**Status:** Early implementation (22/802 passing = 3%)

**Verified:** 2026-02-23 via `mvn test`

**Results:**

- Tests run: 802, Errors: 780, Failures: 0, Passed: 22
- Duration: ~17 seconds

**Implemented Tests:**

- Parse hex address (various formats)
- Generate random Ed25519 key pair
- Basic address formatting

**SDK Gaps (features not available):**

- Secp256k1/Secp256r1 cryptography
- Mnemonic derivation
- Keyless authentication
- Code generation

**Next Steps:**

- Implement step definitions for BCS serialization
- Add Ed25519 signing/verification steps
- Add TypeTag parsing steps
- Add account management steps

---

### Kotlin (`aptos-kotlin-sdk` 0.1.0) — [Full Status](tests/kotlin/SDK_STATUS.md)

**Status:** Official Aptos Labs SDK — not yet runnable

**Verified:** 2026-02-23 — build fails (SDK not published to Maven Central)

**Publisher:** aptos-labs (official)

**Notes:**

- Official Aptos Labs Kotlin SDK (replaced community kaptos SDK)
- JVM-focused with Android support
- Modular architecture (core, client, sdk, indexer)
- Full Ed25519 and Secp256k1 support
- BCS serialization, authentication keys, mnemonic derivation
- Cannot build: `com.aptos:core:0.1.0` not found in Maven Central or mavenLocal
- Step definitions updated, awaiting SDK publication

---

### Python (`aptos-sdk` >=0.11.0) — [Full Status](tests/python/SDK_STATUS.md)

**Status:** Significantly improved coverage (459/791 passing = 58%)

**Verified:** 2026-02-23 via `behave`

**Results (per category):**

- 01-core-types: 112 passed, 9 errors (93%)
- 02-cryptography: 50 passed, 2 failed, 7 errors, 33 skipped
- 03-account-management: 24 passed, 8 failed, 17 errors, 35 skipped
- 04-transaction-building: 62 passed, 16 failed, 16 errors, 14 skipped
- 05-api-clients: 122 passed, 66 failed, 2 errors, 3 skipped
- 06-advanced: 89 passed, 29 failed, 8 errors, 63 skipped
- **Total: 459 passed, 121 failed, 75 errors, 136 skipped**

**Well-Implemented:**

- Address parsing and formatting (22/22)
- Ed25519 cryptography (25/25)
- Hashing (19/20)
- Error handling (30/30)
- Basic API client operations

**Needs Work:**

- Secp256k1 key derivation (errors in key-from-bytes)
- Account management (auth key scheme identifiers)
- Entry function BCS serialization
- Multi-sig and fee-payer validation
- Keyless (not supported in SDK)

---

### .NET (`Aptos` 0.0.x-beta) — [Full Status](tests/dotnet/SDK_STATUS.md)

**Status:** Beta SDK (478/808 passing = 59%)

**Last Verified:** 2026-01-28 via `dotnet test`

**Current Issue (2026-02-23):** Cannot run tests — `dotnet` SDK not installed in environment.

**Results (from 2026-01-28):**

- 478 passed, 330 failed out of 808 tests
- Many failures due to missing step definitions

**Notes:**

- Beta SDK - API may change
- Uses Reqnroll (SpecFlow successor) for BDD
