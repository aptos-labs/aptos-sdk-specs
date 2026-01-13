# Core Types Specification

## Overview

Core types are the fundamental data structures used throughout an Aptos SDK. They provide type-safe
representations of blockchain primitives including addresses, hashes, chain identifiers, and Move
type representations.

## Goals

1. Provide type-safe representations of Aptos blockchain primitives
2. Enable efficient serialization/deserialization (BCS and JSON)
3. Support Display and Debug formatting for developer ergonomics
4. Maintain compatibility with on-chain data formats
5. Ensure consistent behavior across all SDK implementations

## Non-Goals

- Cryptographic operations (see 02-cryptography)
- Network communication (see 05-api-clients)
- Transaction logic (see 04-transaction-building)

---

## AccountAddress

### Description

A 32-byte value uniquely identifying an account on the Aptos blockchain.

### Requirements

#### Construction

| Method              | Priority | Description                                |
| ------------------- | -------- | ------------------------------------------ |
| `from_hex(string)`  | P0       | Parse hex string with or without 0x prefix |
| `from_bytes(bytes)` | P0       | Create from 32-byte array                  |
| `ZERO`              | P0       | Constant for all-zeros address             |
| `ONE`               | P0       | Constant for 0x1 (framework)               |
| `THREE`             | P0       | Constant for 0x3 (token)                   |
| `FOUR`              | P0       | Constant for 0x4 (objects)                 |

#### Parsing Rules

1. Accept with or without `0x` prefix
2. Accept short-form addresses (e.g., `0x1` → 32-byte padded)
3. Accept full 64-character hex strings
4. Reject invalid hex characters
5. Reject strings longer than 64 hex characters (excluding 0x)
6. Case-insensitive hex parsing

#### Formatting

| Method              | Priority | Description                            |
| ------------------- | -------- | -------------------------------------- |
| `to_hex()`          | P0       | Full 64-char hex with 0x prefix        |
| `to_short_string()` | P0       | Minimal hex with leading zeros removed |

#### Serialization

| Format | Priority | Representation            |
| ------ | -------- | ------------------------- |
| BCS    | P0       | Raw 32 bytes              |
| JSON   | P0       | Hex string with 0x prefix |

### Examples

```
Input: "0x1"
to_hex(): "0x0000000000000000000000000000000000000000000000000000000000000001"
to_short_string(): "0x1"

Input: "0x10"
to_hex(): "0x0000000000000000000000000000000000000000000000000000000000000010"
to_short_string(): "0x10"

Input: "1"
to_hex(): "0x0000000000000000000000000000000000000000000000000000000000000001"
```

---

## HashValue

### Description

A 32-byte cryptographic hash value, typically SHA3-256.

### Requirements

#### Construction

| Method              | Priority | Description                 |
| ------------------- | -------- | --------------------------- |
| `from_bytes(bytes)` | P0       | Create from 32-byte array   |
| `from_hex(string)`  | P0       | Parse hex string            |
| `sha3_256_of(data)` | P0       | Compute SHA3-256 hash       |
| `ZERO`              | P0       | Constant for all-zeros hash |

#### Formatting

| Method       | Priority | Description                     |
| ------------ | -------- | ------------------------------- |
| `to_hex()`   | P0       | Full 64-char hex with 0x prefix |
| `as_bytes()` | P0       | Raw 32-byte array               |

---

## ChainId

### Description

A network chain identifier (u8).

### Requirements

#### Constants

| Constant | Value | Priority |
| -------- | ----- | -------- |
| MAINNET  | 1     | P0       |
| TESTNET  | 2     | P0       |
| DEVNET   | 3     | P1       |
| LOCAL    | 4     | P1       |

#### Construction

| Method    | Priority | Description               |
| --------- | -------- | ------------------------- |
| `new(u8)` | P0       | Create from numeric value |
| `id()`    | P0       | Get numeric value         |

#### Serialization

| Format | Priority | Representation   |
| ------ | -------- | ---------------- |
| BCS    | P0       | Single byte (u8) |

---

## TypeTag

### Description

Representation of a Move type, used for generic type arguments.

### Requirements

#### Variants

| Variant             | Priority | Description         |
| ------------------- | -------- | ------------------- |
| `Bool`              | P0       | Move bool type      |
| `U8`                | P0       | Move u8 type        |
| `U16`               | P0       | Move u16 type       |
| `U32`               | P0       | Move u32 type       |
| `U64`               | P0       | Move u64 type       |
| `U128`              | P0       | Move u128 type      |
| `U256`              | P0       | Move u256 type      |
| `Address`           | P0       | Move address type   |
| `Signer`            | P0       | Move signer type    |
| `Vector(TypeTag)`   | P0       | Move vector<T> type |
| `Struct(StructTag)` | P0       | Move struct type    |

#### Parsing

Must parse strings in the following formats:

- Primitives: `bool`, `u8`, `u16`, `u32`, `u64`, `u128`, `u256`, `address`, `signer`
- Vectors: `vector<T>` where T is any TypeTag
- Structs: `address::module::Name` or `address::module::Name<T1, T2>`

#### Formatting

| Method        | Priority | Description                     |
| ------------- | -------- | ------------------------------- |
| `to_string()` | P0       | Canonical string representation |

---

## MoveModuleId

### Description

Identifies a Move module by address and name.

### Requirements

#### Construction

| Method               | Priority | Description                  |
| -------------------- | -------- | ---------------------------- |
| `new(address, name)` | P0       | Create from components       |
| `from_string(s)`     | P0       | Parse "address::name" format |

#### Components

| Field   | Type           | Description              |
| ------- | -------------- | ------------------------ |
| address | AccountAddress | Module's account address |
| name    | String         | Module name (identifier) |

#### Formatting

Format: `{address}::{name}` where address uses short form.

Example: `0x1::coin`

---

## MoveStructTag

### Description

Full Move struct type including address, module, name, and type parameters.

### Requirements

#### Construction

| Method                                  | Priority | Description              |
| --------------------------------------- | -------- | ------------------------ |
| `new(address, module, name, type_args)` | P0       | Create from components   |
| `from_string(s)`                        | P0       | Parse full struct string |

#### Components

| Field     | Type           | Description              |
| --------- | -------------- | ------------------------ |
| address   | AccountAddress | Struct's account address |
| module    | String         | Module name              |
| name      | String         | Struct name              |
| type_args | Vec<TypeTag>   | Type parameters          |

#### Formatting

Format: `{address}::{module}::{name}` or `{address}::{module}::{name}<T1, T2>` with type args.

Examples:

- `0x1::aptos_coin::AptosCoin`
- `0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>`

---

## U256

### Description

256-bit unsigned integer for Move's u256 type.

### Requirements

#### Construction

| Method                 | Priority | Description                 |
| ---------------------- | -------- | --------------------------- |
| `from_u64(u64)`        | P0       | Create from u64             |
| `from_u128(u128)`      | P0       | Create from u128            |
| `from_bytes_be(bytes)` | P0       | From 32 big-endian bytes    |
| `from_bytes_le(bytes)` | P0       | From 32 little-endian bytes |
| `from_string(s)`       | P1       | Parse decimal string        |

#### Constants

| Constant | Priority | Description   |
| -------- | -------- | ------------- |
| ZERO     | P0       | Zero value    |
| ONE      | P0       | One value     |
| MAX      | P0       | Maximum value |

#### Serialization

| Format | Priority | Representation          |
| ------ | -------- | ----------------------- |
| BCS    | P0       | 32 bytes, little-endian |

---

## BCS Serialization

### Description

Binary Canonical Serialization format used by Aptos.

### Required Primitives

| Type      | BCS Format                                | Priority |
| --------- | ----------------------------------------- | -------- |
| bool      | 1 byte (0x00 or 0x01)                     | P0       |
| u8        | 1 byte                                    | P0       |
| u16       | 2 bytes, little-endian                    | P0       |
| u32       | 4 bytes, little-endian                    | P0       |
| u64       | 8 bytes, little-endian                    | P0       |
| u128      | 16 bytes, little-endian                   | P0       |
| u256      | 32 bytes, little-endian                   | P0       |
| i8        | 1 byte, two's complement                  | P0       |
| i16       | 2 bytes, little-endian, two's complement  | P0       |
| i32       | 4 bytes, little-endian, two's complement  | P0       |
| i64       | 8 bytes, little-endian, two's complement  | P0       |
| i128      | 16 bytes, little-endian, two's complement | P0       |
| i256      | 32 bytes, little-endian, two's complement | P0       |
| bytes     | ULEB128 length + raw bytes                | P0       |
| string    | ULEB128 length + UTF-8 bytes              | P0       |
| Option<T> | 0x00 for None, 0x01 + T for Some          | P0       |
| Vec<T>    | ULEB128 length + elements                 | P0       |

### ULEB128 Encoding

Variable-length encoding for lengths and indices:

- Values 0-127: 1 byte
- Values 128-16383: 2 bytes
- And so on...

---

## Error Handling

### Required Error Cases

| Error          | Trigger                  | Priority |
| -------------- | ------------------------ | -------- |
| InvalidAddress | Malformed address string | P0       |
| InvalidHex     | Non-hex characters       | P0       |
| InvalidLength  | Wrong byte count         | P0       |
| ParseError     | TypeTag parse failure    | P0       |

---

## Security Considerations

1. **Address Validation**: Always validate address length and format before use
2. **No Address Arithmetic**: Addresses are opaque identifiers, not numbers
3. **Constant-Time Comparison**: Use constant-time comparison for security-sensitive operations
4. **Input Sanitization**: Reject malformed input early with clear errors

---

## Cross-SDK Compatibility

All SDKs must produce identical:

1. BCS-serialized bytes for the same input
2. Hex string representations
3. Parsing results for valid inputs
4. Error categories for invalid inputs

Test vectors in `test-vectors/addresses.json` provide deterministic test cases.
