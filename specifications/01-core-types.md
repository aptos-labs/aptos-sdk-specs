# Core Types Specification

## Abstract

This document specifies the fundamental data types used throughout Aptos SDKs: `AccountAddress`,
`ChainId`, `TypeTag`, `StructTag`, and related types. These types provide type-safe representations
of Aptos blockchain primitives and form the foundation for all SDK operations.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [AccountAddress](#2-accountaddress)
3. [ChainId](#3-chainid)
4. [TypeTag](#4-typetag)
5. [StructTag](#5-structtag)
6. [MoveModuleId](#6-movemoduleid)
7. [U256](#7-u256)
8. [Test Vectors](#8-test-vectors)
9. [Security Considerations](#9-security-considerations)
10. [References](#10-references)

---

## 1. Introduction

### 1.1 Purpose

Core types provide the foundational data structures for representing Aptos blockchain entities.
Correct implementation of these types is essential for all SDK functionality including transaction
building, signing, and API interaction.

### 1.2 Scope

This specification covers:

- Account address representation and formatting
- Chain/network identification
- Move type representation (TypeTag, StructTag)
- Module identification
- Large integer handling (U256)

### 1.3 Definitions

| Term            | Definition                                          |
| --------------- | --------------------------------------------------- |
| Account Address | 32-byte unique identifier for an account on Aptos   |
| Chain ID        | 8-bit identifier for an Aptos network               |
| TypeTag         | Representation of a Move type for generic arguments |
| StructTag       | Fully qualified Move struct type                    |
| Short Form      | Address format with leading zeros removed           |
| Full Form       | Address format as complete 64-character hex string  |

---

## 2. AccountAddress

### 2.1 Overview

An `AccountAddress` is a 32-byte (256-bit) value that uniquely identifies an account on the Aptos
blockchain. It is derived from the account's authentication key at creation time.

### 2.2 Data Representation

```
AccountAddress := [u8; 32]  // Fixed 32-byte array
```

The address is stored as a big-endian byte array where byte 0 is the most significant byte.

### 2.3 Construction

#### 2.3.1 From Hex String [P0]

Implementations **MUST** provide a method to parse addresses from hex strings.

**Signature:**

```
from_hex(input: string) -> Result<AccountAddress, ParseError>
```

**Parsing Rules:**

1. The `0x` prefix **MUST** be accepted
2. The `0x` prefix **SHOULD** be optional for compatibility
3. Input **MUST** be case-insensitive (accept `0xABCD`, `0xabcd`, `0xAbCd`)
4. Short-form addresses **MUST** be accepted and left-padded with zeros
5. Input **MUST NOT** exceed 64 hex characters (excluding `0x` prefix)
6. Non-hex characters **MUST** cause a parse error
7. Empty input (or just `0x`) **MUST** cause a parse error

**Examples:**

| Input                              | Result                              |
| ---------------------------------- | ----------------------------------- |
| `"0x1"`                            | Success: `[0,0,...,0,1]`            |
| `"1"`                              | Success: `[0,0,...,0,1]`            |
| `"0x0000...0001"` (64 chars)       | Success: `[0,0,...,0,1]`            |
| `"0xABCDEF"`                       | Success: `[0,0,...,0xAB,0xCD,0xEF]` |
| `""`                               | Error: InvalidAddress               |
| `"0x"`                             | Error: InvalidAddress               |
| `"0xGHIJKL"`                       | Error: InvalidHex                   |
| `"0x00000...00001"` (65 hex chars) | Error: InvalidLength                |

#### 2.3.2 From Bytes [P0]

Implementations **MUST** provide a method to create an address from raw bytes.

**Signature:**

```
from_bytes(bytes: [u8; 32]) -> AccountAddress
```

The input **MUST** be exactly 32 bytes. Implementations **SHOULD** provide a `try_from_bytes`
variant for variable-length input that returns an error if length is not 32.

### 2.4 Standard Constants [P0]

Implementations **MUST** provide the following address constants:

| Constant | Value | Bytes           | Purpose                |
| -------- | ----- | --------------- | ---------------------- |
| `ZERO`   | 0x0   | `[0; 32]`       | All-zeros address      |
| `ONE`    | 0x1   | `[0,0,...,0,1]` | Framework address      |
| `THREE`  | 0x3   | `[0,0,...,0,3]` | Token module address   |
| `FOUR`   | 0x4   | `[0,0,...,0,4]` | Objects module address |

### 2.5 Formatting

#### 2.5.1 Full Hex Format [P0]

**Signature:**

```
to_hex() -> string
```

**Requirements:**

1. Output **MUST** include `0x` prefix
2. Output **MUST** be exactly 66 characters (`0x` + 64 hex chars)
3. Output **MUST** use lowercase hex characters
4. All 32 bytes **MUST** be represented, including leading zeros

**Example:**

```
Address bytes: [0,0,...,0,1]
to_hex(): "0x0000000000000000000000000000000000000000000000000000000000000001"
```

#### 2.5.2 Short String Format [P0]

**Signature:**

```
to_short_string() -> string
```

**Requirements:**

1. Output **MUST** include `0x` prefix
2. Leading zeros **MUST** be removed (except one if the value is 0)
3. Output **MUST** use lowercase hex characters
4. The zero address **MUST** format as `"0x0"`

**Examples:**

| Bytes                           | Short String                    |
| ------------------------------- | ------------------------------- |
| `[0,0,...,0,0]`                 | `"0x0"`                         |
| `[0,0,...,0,1]`                 | `"0x1"`                         |
| `[0,0,...,0,0x10]`              | `"0x10"`                        |
| `[0x12,0x34,...,0xef]` (all 32) | `"0x1234...ef"` (full 64 chars) |

### 2.6 Comparison [P0]

#### 2.6.1 Equality

Implementations **MUST** support equality comparison. Two addresses are equal if and only if all 32
bytes are identical.

#### 2.6.2 Ordering

Implementations **SHOULD** support lexicographic ordering based on byte comparison (big-endian).

### 2.7 Serialization

#### 2.7.1 BCS Serialization [P0]

BCS serialization of `AccountAddress`:

1. Serialize as exactly 32 bytes
2. No length prefix
3. Big-endian byte order preserved

```
BCS(AccountAddress) := bytes[0..32]  // Raw 32 bytes
```

#### 2.7.2 JSON Serialization [P0]

JSON serialization **MUST** use the full hex format:

```json
"0x0000000000000000000000000000000000000000000000000000000000000001"
```

### 2.8 Display and Debug [P1]

- `Display` format **SHOULD** use short string format
- `Debug` format **SHOULD** use full hex format with type annotation

---

## 3. ChainId

### 3.1 Overview

A `ChainId` is an 8-bit unsigned integer that identifies an Aptos network.

### 3.2 Data Representation

```
ChainId := u8
```

### 3.3 Standard Constants [P0]

| Constant  | Value | Description   |
| --------- | ----- | ------------- |
| `MAINNET` | 1     | Aptos mainnet |
| `TESTNET` | 2     | Aptos testnet |

### 3.4 Additional Constants [P1]

| Constant | Value  | Description                     |
| -------- | ------ | ------------------------------- |
| `DEVNET` | varies | Aptos devnet (value may change) |
| `LOCAL`  | 4      | Local development network       |

### 3.5 Construction [P0]

**Signature:**

```
new(value: u8) -> ChainId
```

### 3.6 Methods [P0]

**Signature:**

```
id() -> u8  // Get the numeric chain ID value
```

### 3.7 BCS Serialization [P0]

```
BCS(ChainId) := u8  // Single byte
```

---

## 4. TypeTag

### 4.1 Overview

A `TypeTag` represents a Move type, used primarily for generic type arguments in transactions and
view functions.

### 4.2 Variants [P0]

```
TypeTag :=
  | Bool
  | U8
  | U16
  | U32
  | U64
  | U128
  | U256
  | Address
  | Signer
  | Vector(TypeTag)
  | Struct(StructTag)
```

### 4.3 Parsing [P0]

Implementations **MUST** parse TypeTag from string representation.

**Signature:**

```
from_string(input: string) -> Result<TypeTag, ParseError>
```

**Parsing Rules:**

| Input Format                   | TypeTag Variant     |
| ------------------------------ | ------------------- |
| `"bool"`                       | `Bool`              |
| `"u8"`                         | `U8`                |
| `"u16"`                        | `U16`               |
| `"u32"`                        | `U32`               |
| `"u64"`                        | `U64`               |
| `"u128"`                       | `U128`              |
| `"u256"`                       | `U256`              |
| `"address"`                    | `Address`           |
| `"signer"`                     | `Signer`            |
| `"vector<T>"`                  | `Vector(parse(T))`  |
| `"addr::module::Name"`         | `Struct(StructTag)` |
| `"addr::module::Name<T1, T2>"` | `Struct(StructTag)` |

**Additional Parsing Requirements:**

1. Parsing **MUST** be case-sensitive for primitive types
2. Whitespace around `<`, `>`, and `,` **SHOULD** be tolerated
3. Nested generics **MUST** be supported: `vector<vector<u8>>`
4. Multiple type parameters **MUST** be supported: `0x1::table::Table<address, u64>`

### 4.4 Formatting [P0]

**Signature:**

```
to_string() -> string
```

**Requirements:**

1. Primitive types **MUST** format as lowercase (`bool`, `u8`, etc.)
2. Vector types **MUST** format as `vector<inner>`
3. Struct types **MUST** format as `address::module::Name` or `address::module::Name<T1, T2>`
4. Addresses in struct types **SHOULD** use short form

### 4.5 BCS Serialization [P0]

TypeTag uses variant encoding:

```
BCS(TypeTag) :=
  | 0x00                          // Bool
  | 0x01                          // U8
  | 0x02                          // U64
  | 0x03                          // U128
  | 0x04                          // Address
  | 0x05                          // Signer
  | 0x06 || BCS(TypeTag)          // Vector
  | 0x07 || BCS(StructTag)        // Struct
  | 0x08                          // U16
  | 0x09                          // U32
  | 0x0a                          // U256
```

---

## 5. StructTag

### 5.1 Overview

A `StructTag` is a fully qualified Move struct type including address, module, name, and type
parameters.

### 5.2 Fields [P0]

```
StructTag := {
  address: AccountAddress,
  module: string,           // Move identifier
  name: string,             // Move identifier
  type_args: Vec<TypeTag>
}
```

### 5.3 Construction [P0]

**Signature:**

```
new(
  address: AccountAddress,
  module: string,
  name: string,
  type_args: Vec<TypeTag>
) -> StructTag
```

### 5.4 Parsing [P0]

**Signature:**

```
from_string(input: string) -> Result<StructTag, ParseError>
```

**Format:**

```
address::module::Name
address::module::Name<TypeArg1, TypeArg2>
```

**Examples:**

| Input                                                | Parsed StructTag                          |
| ---------------------------------------------------- | ----------------------------------------- |
| `"0x1::aptos_coin::AptosCoin"`                       | `{0x1, "aptos_coin", "AptosCoin", []}`    |
| `"0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"` | `{0x1, "coin", "CoinStore", [AptosCoin]}` |

### 5.5 Formatting [P0]

**Signature:**

```
to_string() -> string
```

**Format:**

- Without type args: `{address}::{module}::{name}`
- With type args: `{address}::{module}::{name}<{type_args joined by ", "}>`

Address **SHOULD** use short form in output.

### 5.6 BCS Serialization [P0]

```
BCS(StructTag) :=
  BCS(address) ||           // 32 bytes
  BCS(module as string) ||  // ULEB128 length + UTF-8 bytes
  BCS(name as string) ||    // ULEB128 length + UTF-8 bytes
  BCS(type_args as Vec)     // ULEB128 count + each TypeTag
```

---

## 6. MoveModuleId

### 6.1 Overview

A `MoveModuleId` identifies a Move module by its address and name.

### 6.2 Fields [P0]

```
MoveModuleId := {
  address: AccountAddress,
  name: string              // Move identifier
}
```

### 6.3 Construction [P0]

**Signatures:**

```
new(address: AccountAddress, name: string) -> MoveModuleId
from_string(input: string) -> Result<MoveModuleId, ParseError>
```

**String Format:** `address::name`

### 6.4 Formatting [P0]

**Format:** `{address}::{name}` with short-form address.

**Example:** `0x1::coin`

### 6.5 BCS Serialization [P0]

```
BCS(MoveModuleId) :=
  BCS(address) ||           // 32 bytes
  BCS(name as string)       // ULEB128 length + UTF-8 bytes
```

---

## 7. U256

### 7.1 Overview

`U256` represents a 256-bit unsigned integer, corresponding to Move's `u256` type.

### 7.2 Construction [P0]

| Method                 | Description                        |
| ---------------------- | ---------------------------------- |
| `from_u64(value)`      | Create from u64 value              |
| `from_u128(value)`     | Create from u128 value             |
| `from_bytes_le(bytes)` | Create from 32 little-endian bytes |
| `from_bytes_be(bytes)` | Create from 32 big-endian bytes    |

### 7.3 Constants [P0]

| Constant | Value     |
| -------- | --------- |
| `ZERO`   | 0         |
| `ONE`    | 1         |
| `MAX`    | 2^256 - 1 |

### 7.4 String Parsing [P1]

**Signature:**

```
from_string(input: string) -> Result<U256, ParseError>
```

Input **MUST** be a decimal string representation.

### 7.5 BCS Serialization [P0]

```
BCS(U256) := bytes[0..32]  // 32 bytes, little-endian
```

---

## 8. Test Vectors

### 8.1 Address Parsing

Test vectors are provided in `test-vectors/addresses.json`.

**Example vectors:**

```json
{
  "input": "0x1",
  "expected": {
    "full_hex": "0x0000000000000000000000000000000000000000000000000000000000000001",
    "short_string": "0x1",
    "last_byte": 1
  }
}
```

### 8.2 TypeTag Parsing

Test vectors are provided in `test-vectors/type-tags.json`.

### 8.3 BCS Serialization

Test vectors are provided in `test-vectors/bcs.json`.

---

## 9. Security Considerations

### 9.1 Address Validation

1. Implementations **MUST** validate address length before use
2. Implementations **MUST NOT** perform arithmetic on addresses
3. Implementations **SHOULD** use constant-time comparison for security-sensitive contexts

### 9.2 Input Sanitization

1. Implementations **MUST** reject malformed input with clear error messages
2. Implementations **MUST NOT** silently truncate or modify invalid input
3. Implementations **SHOULD** limit input string length to prevent DoS

### 9.3 Display Safety

1. Address display **SHOULD** not leak sensitive information
2. Full addresses **SHOULD** be displayed in contexts requiring verification

---

## 10. References

### 10.1 Related Specifications

- [02-bcs-serialization.md](02-bcs-serialization.md) - BCS format details
- [04-accounts.md](04-accounts.md) - Account address derivation

### 10.2 Feature Files

- `features/01-core-types/address.feature` - 31 address scenarios
- `features/01-core-types/type-tags.feature` - 27 TypeTag scenarios
- `features/01-core-types/serialization.feature` - 32 serialization scenarios

### 10.3 Test Vectors

- `test-vectors/addresses.json`
- `test-vectors/type-tags.json`
- `test-vectors/bcs.json`
