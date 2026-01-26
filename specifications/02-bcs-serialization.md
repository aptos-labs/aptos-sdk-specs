# BCS Serialization Specification

## Abstract

This document specifies Binary Canonical Serialization (BCS), the binary encoding format used by
Aptos for transactions, on-chain data, and inter-component communication. BCS provides a
deterministic, canonical byte representation that is consistent across all implementations.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Design Principles](#2-design-principles)
3. [Primitive Types](#3-primitive-types)
4. [Composite Types](#4-composite-types)
5. [ULEB128 Encoding](#5-uleb128-encoding)
6. [Aptos-Specific Types](#6-aptos-specific-types)
7. [Serializer Interface](#7-serializer-interface)
8. [Deserializer Interface](#8-deserializer-interface)
9. [Test Vectors](#9-test-vectors)
10. [Security Considerations](#10-security-considerations)
11. [References](#11-references)

---

## 1. Introduction

### 1.1 Purpose

BCS (Binary Canonical Serialization) is the standard binary encoding format for Aptos. It is used
for:

- Transaction encoding and signing
- Entry function argument encoding
- On-chain data storage
- API request/response bodies (when binary format is used)

### 1.2 Scope

This specification covers:
- Encoding rules for all primitive types
- Encoding rules for composite types (vectors, options, structs)
- ULEB128 variable-length integer encoding
- Aptos-specific type serialization

### 1.3 Definitions

| Term       | Definition                                              |
| ---------- | ------------------------------------------------------- |
| BCS        | Binary Canonical Serialization                          |
| ULEB128    | Unsigned Little-Endian Base 128 variable-length encoding|
| Canonical  | Exactly one valid encoding exists for any value         |
| Big-endian | Most significant byte first                             |
| Little-endian | Least significant byte first                         |

---

## 2. Design Principles

### 2.1 Canonical Encoding

BCS is canonical: for any value, there is exactly one valid byte sequence. This property is
essential for:

- Consistent transaction hashes across implementations
- Reliable signature verification
- Reproducible state roots

### 2.2 No Self-Description

BCS does **NOT** include type information in the encoded bytes. The deserializer must know the
expected type in advance. This makes BCS compact but requires schema agreement between encoder and
decoder.

### 2.3 Little-Endian

All multi-byte integers are encoded in little-endian format (least significant byte first).

### 2.4 Deterministic Ordering

For types with ordering (maps, sets), BCS requires a deterministic order. However, Aptos primarily
uses vectors rather than maps in BCS contexts.

---

## 3. Primitive Types

### 3.1 Boolean [P0]

```
BCS(bool) :=
  | 0x00  // false
  | 0x01  // true
```

Any value other than `0x00` or `0x01` **MUST** cause a deserialization error.

**Examples:**

| Value   | BCS Bytes |
| ------- | --------- |
| `false` | `00`      |
| `true`  | `01`      |

### 3.2 Unsigned Integers [P0]

#### 3.2.1 u8

```
BCS(u8) := byte[0]  // Single byte
```

**Examples:**

| Value | BCS Bytes |
| ----- | --------- |
| 0     | `00`      |
| 255   | `ff`      |

#### 3.2.2 u16

```
BCS(u16) := byte[0..2]  // 2 bytes, little-endian
```

**Examples:**

| Value  | BCS Bytes |
| ------ | --------- |
| 0      | `00 00`   |
| 256    | `00 01`   |
| 65535  | `ff ff`   |

#### 3.2.3 u32

```
BCS(u32) := byte[0..4]  // 4 bytes, little-endian
```

**Examples:**

| Value      | BCS Bytes     |
| ---------- | ------------- |
| 0          | `00 00 00 00` |
| 1          | `01 00 00 00` |
| 0x12345678 | `78 56 34 12` |

#### 3.2.4 u64

```
BCS(u64) := byte[0..8]  // 8 bytes, little-endian
```

**Examples:**

| Value              | BCS Bytes                 |
| ------------------ | ------------------------- |
| 0                  | `00 00 00 00 00 00 00 00` |
| 1                  | `01 00 00 00 00 00 00 00` |
| 0x123456789ABCDEF0 | `f0 de bc 9a 78 56 34 12` |

#### 3.2.5 u128

```
BCS(u128) := byte[0..16]  // 16 bytes, little-endian
```

#### 3.2.6 u256

```
BCS(u256) := byte[0..32]  // 32 bytes, little-endian
```

### 3.3 Signed Integers [P0]

Signed integers use two's complement representation in little-endian format.

#### 3.3.1 i8

```
BCS(i8) := byte[0]  // Single byte, two's complement
```

**Examples:**

| Value | BCS Bytes |
| ----- | --------- |
| 0     | `00`      |
| 1     | `01`      |
| -1    | `ff`      |
| -128  | `80`      |
| 127   | `7f`      |

#### 3.3.2 i16, i32, i64, i128, i256

Same encoding pattern as unsigned counterparts, using two's complement representation.

---

## 4. Composite Types

### 4.1 Bytes (Variable Length) [P0]

```
BCS(bytes) := ULEB128(length) || raw_bytes
```

**Examples:**

| Value          | BCS Bytes           |
| -------------- | ------------------- |
| `[]` (empty)   | `00`                |
| `[0x01]`       | `01 01`             |
| `[0x01, 0x02]` | `02 01 02`          |

### 4.2 String [P0]

Strings are encoded as UTF-8 bytes with length prefix.

```
BCS(string) := ULEB128(byte_length) || utf8_bytes
```

**Examples:**

| Value     | BCS Bytes              |
| --------- | ---------------------- |
| `""`      | `00`                   |
| `"a"`     | `01 61`                |
| `"hello"` | `05 68 65 6c 6c 6f`    |
| `"日本"`  | `06 e6 97 a5 e6 9c ac` |

**Requirements:**

1. The byte sequence **MUST** be valid UTF-8
2. Invalid UTF-8 **MUST** cause a deserialization error

### 4.3 Option [P0]

```
BCS(Option<T>) :=
  | 0x00                    // None
  | 0x01 || BCS(value)      // Some(value)
```

**Examples:**

| Value          | BCS Bytes     |
| -------------- | ------------- |
| `None`         | `00`          |
| `Some(0u8)`    | `01 00`       |
| `Some(255u8)`  | `01 ff`       |
| `Some("hi")`   | `01 02 68 69` |

### 4.4 Vector [P0]

```
BCS(Vec<T>) := ULEB128(length) || BCS(element_0) || BCS(element_1) || ... || BCS(element_n-1)
```

**Examples:**

| Value                | BCS Bytes           |
| -------------------- | ------------------- |
| `[]` (empty Vec<u8>) | `00`                |
| `[1u8, 2u8, 3u8]`    | `03 01 02 03`       |
| `[true, false]`      | `02 01 00`          |

### 4.5 Fixed-Size Arrays [P0]

Fixed-size arrays are encoded without a length prefix.

```
BCS([T; N]) := BCS(element_0) || BCS(element_1) || ... || BCS(element_N-1)
```

**Example:**

| Value                | BCS Bytes     |
| -------------------- | ------------- |
| `[1u8, 2u8, 3u8]`    | `01 02 03`    |

**Note:** This differs from `Vec<T>` which includes a length prefix.

### 4.6 Tuples [P0]

Tuples are encoded as concatenated elements without length prefix.

```
BCS((T1, T2, ...)) := BCS(field_1) || BCS(field_2) || ...
```

### 4.7 Structs [P0]

Structs are encoded as concatenated fields in declaration order.

```
BCS(Struct { field1: T1, field2: T2, ... }) := BCS(field1) || BCS(field2) || ...
```

**Requirements:**

1. Fields **MUST** be serialized in declaration order
2. No field names or type information is included
3. All fields **MUST** be serialized (no omission of default values)

### 4.8 Enums [P0]

Enums are encoded with a variant index followed by variant data.

```
BCS(Enum) := ULEB128(variant_index) || BCS(variant_data)
```

**Requirements:**

1. Variant index **MUST** be the zero-based index in declaration order
2. Unit variants have no additional data after the index

**Example:**

```rust
enum MyEnum {
    Unit,           // index 0
    Single(u64),    // index 1
    Multiple { a: u8, b: u16 },  // index 2
}
```

| Value                        | BCS Bytes                       |
| ---------------------------- | ------------------------------- |
| `MyEnum::Unit`               | `00`                            |
| `MyEnum::Single(256)`        | `01 00 01 00 00 00 00 00 00`    |
| `MyEnum::Multiple { a: 1, b: 2 }` | `02 01 02 00`              |

---

## 5. ULEB128 Encoding

### 5.1 Overview

ULEB128 (Unsigned Little-Endian Base 128) is a variable-length encoding for non-negative integers.
It is used for lengths and enum variant indices.

### 5.2 Encoding Algorithm [P0]

```
function encode_uleb128(value: u64) -> bytes:
    result = []
    while value >= 0x80:
        result.append((value & 0x7F) | 0x80)
        value = value >> 7
    result.append(value & 0x7F)
    return result
```

### 5.3 Decoding Algorithm [P0]

```
function decode_uleb128(bytes: &[u8]) -> (u64, bytes_consumed):
    value = 0
    shift = 0
    for i, byte in enumerate(bytes):
        value |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            return (value, i + 1)
        shift += 7
        if shift >= 64:
            error("ULEB128 overflow")
    error("Unexpected end of input")
```

### 5.4 Examples

| Value     | ULEB128 Bytes   |
| --------- | --------------- |
| 0         | `00`            |
| 1         | `01`            |
| 127       | `7f`            |
| 128       | `80 01`         |
| 255       | `ff 01`         |
| 256       | `80 02`         |
| 16383     | `ff 7f`         |
| 16384     | `80 80 01`      |

### 5.5 Maximum Value [P0]

BCS implementations **MUST** support ULEB128 values up to `u32::MAX` (4,294,967,295) for lengths.
Implementations **SHOULD** reject larger values to prevent memory exhaustion attacks.

---

## 6. Aptos-Specific Types

### 6.1 AccountAddress [P0]

```
BCS(AccountAddress) := byte[0..32]  // Fixed 32 bytes, no length prefix
```

### 6.2 TypeTag [P0]

```
BCS(TypeTag) :=
  | 0x00                          // Bool
  | 0x01                          // U8
  | 0x02                          // U64
  | 0x03                          // U128
  | 0x04                          // Address
  | 0x05                          // Signer
  | 0x06 || BCS(inner: TypeTag)   // Vector
  | 0x07 || BCS(StructTag)        // Struct
  | 0x08                          // U16
  | 0x09                          // U32
  | 0x0a                          // U256
```

### 6.3 StructTag [P0]

```
BCS(StructTag) :=
  BCS(address: AccountAddress) ||
  BCS(module: string) ||
  BCS(name: string) ||
  BCS(type_args: Vec<TypeTag>)
```

### 6.4 MoveModuleId [P0]

```
BCS(MoveModuleId) :=
  BCS(address: AccountAddress) ||
  BCS(name: string)
```

### 6.5 EntryFunction [P0]

```
BCS(EntryFunction) :=
  BCS(module: MoveModuleId) ||
  BCS(function: string) ||
  BCS(type_args: Vec<TypeTag>) ||
  BCS(args: Vec<bytes>)
```

Note: Each argument in `args` is already BCS-encoded bytes.

### 6.6 TransactionPayload [P0]

```
BCS(TransactionPayload) :=
  | 0x00 || BCS(Script)                // Script variant (deprecated)
  | 0x01                               // ModuleBundle variant (deprecated)
  | 0x02 || BCS(EntryFunction)         // EntryFunction variant
  | 0x03 || BCS(Multisig)              // Multisig variant
```

### 6.7 RawTransaction [P0]

```
BCS(RawTransaction) :=
  BCS(sender: AccountAddress) ||
  BCS(sequence_number: u64) ||
  BCS(payload: TransactionPayload) ||
  BCS(max_gas_amount: u64) ||
  BCS(gas_unit_price: u64) ||
  BCS(expiration_timestamp_secs: u64) ||
  BCS(chain_id: ChainId)
```

### 6.8 SignedTransaction [P0]

```
BCS(SignedTransaction) :=
  BCS(raw_txn: RawTransaction) ||
  BCS(authenticator: TransactionAuthenticator)
```

### 6.9 TransactionAuthenticator [P0]

```
BCS(TransactionAuthenticator) :=
  | 0x00 || BCS(Ed25519Authenticator)
  | 0x01 || BCS(MultiEd25519Authenticator)
  | 0x02 || BCS(MultiAgentAuthenticator)
  | 0x03 || BCS(FeePayerAuthenticator)
  | 0x04 || BCS(SingleSenderAuthenticator)
```

---

## 7. Serializer Interface

### 7.1 Required Methods [P0]

Implementations **MUST** provide methods to serialize:

| Method                   | Description                    |
| ------------------------ | ------------------------------ |
| `serialize_bool(bool)`   | Serialize boolean              |
| `serialize_u8(u8)`       | Serialize unsigned 8-bit int   |
| `serialize_u16(u16)`     | Serialize unsigned 16-bit int  |
| `serialize_u32(u32)`     | Serialize unsigned 32-bit int  |
| `serialize_u64(u64)`     | Serialize unsigned 64-bit int  |
| `serialize_u128(u128)`   | Serialize unsigned 128-bit int |
| `serialize_u256(u256)`   | Serialize unsigned 256-bit int |
| `serialize_bytes(bytes)` | Serialize byte sequence        |
| `serialize_str(string)`  | Serialize UTF-8 string         |
| `serialize_option(opt)`  | Serialize optional value       |
| `serialize_vec(vec)`     | Serialize vector               |

### 7.2 Convenience Methods [P1]

| Method                     | Description                    |
| -------------------------- | ------------------------------ |
| `serialize_i8(i8)`         | Serialize signed 8-bit int     |
| `serialize_i16(i16)`       | Serialize signed 16-bit int    |
| `serialize_i32(i32)`       | Serialize signed 32-bit int    |
| `serialize_i64(i64)`       | Serialize signed 64-bit int    |
| `serialize_i128(i128)`     | Serialize signed 128-bit int   |
| `serialize_i256(i256)`     | Serialize signed 256-bit int   |
| `serialize_fixed_bytes(b)` | Serialize fixed-size bytes     |

### 7.3 Helper Function [P0]

**to_bytes:**
```
to_bytes<T: Serializable>(value: T) -> bytes
```

Convenience function to serialize any BCS-serializable value to bytes.

---

## 8. Deserializer Interface

### 8.1 Required Methods [P0]

Implementations **MUST** provide methods to deserialize:

| Method                    | Description                     |
| ------------------------- | ------------------------------- |
| `deserialize_bool()`      | Deserialize boolean             |
| `deserialize_u8()`        | Deserialize unsigned 8-bit int  |
| `deserialize_u16()`       | Deserialize unsigned 16-bit int |
| `deserialize_u32()`       | Deserialize unsigned 32-bit int |
| `deserialize_u64()`       | Deserialize unsigned 64-bit int |
| `deserialize_u128()`      | Deserialize unsigned 128-bit int|
| `deserialize_u256()`      | Deserialize unsigned 256-bit int|
| `deserialize_bytes()`     | Deserialize byte sequence       |
| `deserialize_str()`       | Deserialize UTF-8 string        |
| `deserialize_option<T>()` | Deserialize optional value      |
| `deserialize_vec<T>()`    | Deserialize vector              |

### 8.2 Convenience Methods [P1]

| Method                     | Description                      |
| -------------------------- | -------------------------------- |
| `deserialize_i8()`         | Deserialize signed 8-bit int     |
| `deserialize_i16()`        | Deserialize signed 16-bit int    |
| `deserialize_i32()`        | Deserialize signed 32-bit int    |
| `deserialize_i64()`        | Deserialize signed 64-bit int    |
| `deserialize_i128()`       | Deserialize signed 128-bit int   |
| `deserialize_i256()`       | Deserialize signed 256-bit int   |
| `deserialize_fixed_bytes()`| Deserialize fixed-size bytes     |

### 8.3 Helper Function [P0]

**from_bytes:**
```
from_bytes<T: Deserializable>(bytes: &[u8]) -> Result<T, DeserializationError>
```

Convenience function to deserialize BCS bytes to a value.

### 8.4 Error Handling [P0]

Deserialization **MUST** fail with an error if:

1. Input bytes are exhausted before deserialization completes
2. Extra bytes remain after deserialization completes
3. Invalid data is encountered (e.g., bool != 0 or 1)
4. UTF-8 validation fails for strings
5. ULEB128 encoding is invalid or overflows

---

## 9. Test Vectors

### 9.1 Primitive Types

Test vectors for primitive type serialization are provided in `test-vectors/bcs.json`.

**Sample vectors:**

```json
{
  "primitives": [
    {
      "name": "bool_false",
      "type": "bool",
      "value": false,
      "bcs_hex": "00"
    },
    {
      "name": "u64_max",
      "type": "u64",
      "value": "18446744073709551615",
      "bcs_hex": "ffffffffffffffff"
    }
  ]
}
```

### 9.2 Complex Types

Vectors for complex types including transactions are in `test-vectors/transactions.json`.

---

## 10. Security Considerations

### 10.1 Length Limits

1. Implementations **MUST** enforce maximum length for vectors and bytes
2. Implementations **SHOULD** reject lengths > 10MB by default
3. Custom limits **MAY** be configured for specific use cases

### 10.2 Depth Limits

1. Implementations **SHOULD** limit recursion depth for nested types
2. Suggested maximum depth: 128 levels
3. Excessive nesting **MUST** cause a deserialization error

### 10.3 Memory Allocation

1. Implementations **MUST NOT** allocate memory based on untrusted length values without validation
2. Implementations **SHOULD** validate length against remaining input before allocation

### 10.4 Canonical Enforcement

1. Implementations **SHOULD** reject non-canonical ULEB128 encodings (leading zeros)
2. Implementations **MUST** produce canonical output during serialization

---

## 11. References

### 11.1 Related Specifications

- [01-core-types.md](01-core-types.md) - Type definitions
- [05-transactions.md](05-transactions.md) - Transaction structures

### 11.2 External References

- [BCS Specification (Diem)](https://github.com/diem/bcs)
- [LEB128 Wikipedia](https://en.wikipedia.org/wiki/LEB128)

### 11.3 Feature Files

- `features/01-core-types/serialization.feature` - 32 serialization scenarios

### 11.4 Test Vectors

- `test-vectors/bcs.json`
- `test-vectors/transactions.json`
