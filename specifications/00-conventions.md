# Specification Conventions

## Abstract

This document defines the conventions, terminology, and compliance requirements used throughout the
Aptos SDK specifications. All specification documents in this folder adhere to these conventions.

## Status

Final

## Version

1.0.0

---

## 1. Requirement Keywords

This specification uses requirement level keywords as defined in
[RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174).

### 1.1 Keyword Definitions

| Keyword              | Meaning                                                                 |
| -------------------- | ----------------------------------------------------------------------- |
| **MUST**             | Absolute requirement. Implementations that do not comply are non-conformant. |
| **MUST NOT**         | Absolute prohibition. Implementations that violate this are non-conformant. |
| **REQUIRED**         | Synonym for MUST.                                                       |
| **SHALL**            | Synonym for MUST.                                                       |
| **SHALL NOT**        | Synonym for MUST NOT.                                                   |
| **SHOULD**           | Recommended. Valid reasons may exist to ignore, but implications must be understood. |
| **SHOULD NOT**       | Not recommended. Valid reasons may exist to do this, but implications must be understood. |
| **RECOMMENDED**      | Synonym for SHOULD.                                                     |
| **MAY**              | Truly optional. Implementations may or may not include this feature.    |
| **OPTIONAL**         | Synonym for MAY.                                                        |

### 1.2 Keyword Formatting

Requirement keywords appear in **UPPERCASE BOLD** when used normatively. Lowercase usage (e.g.,
"may", "should") does not carry normative meaning.

---

## 2. Compliance Levels

Each requirement is associated with a priority level indicating its importance for SDK compliance.

### 2.1 Priority Levels

| Level | Tag         | RFC Keyword | Description                                    |
| ----- | ----------- | ----------- | ---------------------------------------------- |
| P0    | `@required` | MUST        | Essential for basic SDK functionality          |
| P1    | `@preferred`| SHOULD      | Expected in production-quality SDKs            |
| P2    | `@optional` | MAY         | Extended features for comprehensive SDKs       |

### 2.2 Compliance Tiers

SDKs may claim compliance at three tiers:

#### Tier 1: Basic Compliance (P0)

- Implements all P0 (MUST) requirements
- Passes all `@required` test scenarios
- Suitable for basic blockchain interaction

#### Tier 2: Production Compliance (P0 + P1)

- Implements all P0 and P1 requirements
- Passes all `@required` and `@preferred` test scenarios
- Suitable for production applications

#### Tier 3: Full Compliance (P0 + P1 + P2)

- Implements all requirements at all levels
- Passes all test scenarios
- Comprehensive SDK with all features

### 2.3 Compliance Verification

Compliance is verified by running the Gherkin test scenarios against the SDK implementation:

```bash
# Verify P0 compliance
make test-required

# Verify P0 + P1 compliance
make test-preferred

# Verify full compliance
make test
```

---

## 3. Type Notation

### 3.1 Primitive Types

| Notation   | Description                        | Size       |
| ---------- | ---------------------------------- | ---------- |
| `bool`     | Boolean value                      | 1 byte     |
| `u8`       | Unsigned 8-bit integer             | 1 byte     |
| `u16`      | Unsigned 16-bit integer            | 2 bytes    |
| `u32`      | Unsigned 32-bit integer            | 4 bytes    |
| `u64`      | Unsigned 64-bit integer            | 8 bytes    |
| `u128`     | Unsigned 128-bit integer           | 16 bytes   |
| `u256`     | Unsigned 256-bit integer           | 32 bytes   |
| `i8`       | Signed 8-bit integer               | 1 byte     |
| `i16`      | Signed 16-bit integer              | 2 bytes    |
| `i32`      | Signed 32-bit integer              | 4 bytes    |
| `i64`      | Signed 64-bit integer              | 8 bytes    |
| `i128`     | Signed 128-bit integer             | 16 bytes   |
| `i256`     | Signed 256-bit integer             | 32 bytes   |
| `bytes`    | Variable-length byte sequence      | Variable   |
| `string`   | UTF-8 encoded string               | Variable   |

### 3.2 Composite Types

| Notation       | Description                              |
| -------------- | ---------------------------------------- |
| `Vec<T>`       | Variable-length sequence of type T       |
| `Option<T>`    | Optional value (None or Some(T))         |
| `[T; N]`       | Fixed-size array of N elements of type T |
| `(T1, T2)`     | Tuple of types T1 and T2                 |
| `Enum { A, B }`| Enumeration with variants A and B        |

### 3.3 Domain Types

Domain-specific types are defined in their respective specification documents:

| Type                     | Defined In          |
| ------------------------ | ------------------- |
| `AccountAddress`         | 01-core-types.md    |
| `TypeTag`                | 01-core-types.md    |
| `ChainId`                | 01-core-types.md    |
| `Ed25519PrivateKey`      | 03-cryptography.md  |
| `Ed25519PublicKey`       | 03-cryptography.md  |
| `Ed25519Signature`       | 03-cryptography.md  |
| `AuthenticationKey`      | 04-accounts.md      |
| `RawTransaction`         | 05-transactions.md  |
| `SignedTransaction`      | 05-transactions.md  |

---

## 4. Naming Conventions

### 4.1 Cross-Language Considerations

SDK implementations **SHOULD** follow the naming conventions idiomatic to their language while
maintaining semantic equivalence:

| Concept        | Rust/Python (snake_case) | TypeScript/Java (camelCase) | Go (PascalCase) |
| -------------- | ------------------------ | --------------------------- | --------------- |
| Parse address  | `from_hex`               | `fromHex`                   | `FromHex`       |
| Format address | `to_short_string`        | `toShortString`             | `ToShortString` |
| Get bytes      | `as_bytes`               | `asBytes`                   | `AsBytes`       |
| Create new     | `new` or `from_*`        | constructor or `from*`      | `New*`          |

### 4.2 Method Categories

| Prefix/Suffix | Meaning                                      |
| ------------- | -------------------------------------------- |
| `from_*`      | Constructor from another representation      |
| `to_*`        | Convert to another representation            |
| `as_*`        | View as another type (no allocation)         |
| `into_*`      | Convert consuming self                       |
| `is_*`        | Boolean predicate                            |
| `try_*`       | May fail, returns Result/Option              |
| `*_unchecked` | Skips validation (use with caution)          |

---

## 5. Serialization Formats

### 5.1 BCS (Binary Canonical Serialization)

BCS is the primary binary serialization format used by Aptos. See
[02-bcs-serialization.md](02-bcs-serialization.md) for the complete specification.

- Used for transaction encoding
- Used for argument encoding
- Deterministic byte output

### 5.2 JSON

JSON is used for API communication and human-readable representations.

- Numbers > 2^53 are represented as strings
- Byte arrays are hex-encoded with `0x` prefix
- Addresses use full 64-character hex format in API responses

### 5.3 Hex Encoding

| Context           | Format                           | Example                    |
| ----------------- | -------------------------------- | -------------------------- |
| API responses     | Full 64-char with 0x prefix      | `0x000...001`              |
| User input        | Short form accepted              | `0x1`                      |
| Display (short)   | Minimal with 0x prefix           | `0x1`                      |
| Display (full)    | Full 64-char with 0x prefix      | `0x000...001`              |
| Raw bytes (no 0x) | Hex without prefix               | `000...001`                |

---

## 6. Error Handling

### 6.1 Error Categories

Errors **MUST** be categorized to enable programmatic handling:

| Category        | Description                              |
| --------------- | ---------------------------------------- |
| `Parse`         | Input parsing/validation failed          |
| `Crypto`        | Cryptographic operation failed           |
| `Serialization` | BCS/JSON encoding/decoding failed        |
| `Network`       | Network communication failed             |
| `Api`           | API returned an error response           |
| `Timeout`       | Operation timed out                      |
| `NotFound`      | Requested resource not found             |
| `InvalidState`  | Operation invalid in current state       |

### 6.2 Error Information

Errors **MUST** include:

1. Error category/type
2. Human-readable message

Errors **SHOULD** include:

1. Original cause (for wrapped errors)
2. Relevant context (address, hash, etc.)

---

## 7. Test Vectors

### 7.1 Purpose

Test vectors provide deterministic input/output pairs for validating implementations. They ensure
cross-SDK compatibility for deterministic operations.

### 7.2 Location

Test vectors are located in the `test-vectors/` directory:

| File               | Contents                           |
| ------------------ | ---------------------------------- |
| `addresses.json`   | Address parsing and formatting     |
| `bcs.json`         | BCS serialization                  |
| `mnemonics.json`   | BIP-39/BIP-44 key derivation       |
| `signatures.json`  | Cryptographic signatures           |
| `transactions.json`| Transaction serialization          |
| `type-tags.json`   | TypeTag parsing                    |
| `multi-sig.json`   | Multi-signature operations         |

### 7.3 Vector Format

```json
{
  "version": "1.x",
  "description": "What these vectors test",
  "category_name": [
    {
      "name": "vector_name",
      "description": "What this specific vector tests",
      "input": { ... },
      "expected": { ... }
    }
  ]
}
```

---

## 8. Document Versioning

### 8.1 Version Format

Specifications use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to requirements
- **MINOR**: New requirements added (backward compatible)
- **PATCH**: Clarifications, typo fixes, examples

### 8.2 Document Status

| Status   | Meaning                                          |
| -------- | ------------------------------------------------ |
| Draft    | Work in progress, subject to significant change  |
| Review   | Ready for review, may have minor changes         |
| Final    | Stable, changes require new version              |

---

## 9. References

### 9.1 External References

- [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) - Key words for use in RFCs
- [RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174) - Ambiguity of Uppercase vs Lowercase
- [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) - Mnemonic code
- [BIP-44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) - HD Wallets

### 9.2 Aptos References

- [Aptos Developer Documentation](https://aptos.dev)
- [Aptos REST API Specification](https://aptos.dev/nodes/aptos-api-spec)
- [Move Language Documentation](https://move-language.github.io/move/)
