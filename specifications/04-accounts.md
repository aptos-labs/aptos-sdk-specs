# Accounts Specification

## Abstract

This document specifies the account abstractions for Aptos SDKs, including single-key accounts,
multi-key accounts, authentication key derivation, and mnemonic-based account creation. These
abstractions wrap cryptographic primitives with a user-friendly interface.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Account Interface](#2-account-interface)
3. [Ed25519Account](#3-ed25519account)
4. [Secp256k1Account](#4-secp256k1account)
5. [Authentication Key](#5-authentication-key)
6. [Mnemonic-Based Accounts](#6-mnemonic-based-accounts)
7. [Dynamic Account (AnyAccount)](#7-dynamic-account-anyaccount)
8. [Account Serialization](#8-account-serialization)
9. [Test Vectors](#9-test-vectors)
10. [Security Considerations](#10-security-considerations)
11. [References](#11-references)

---

## 1. Introduction

### 1.1 Purpose

Account abstractions provide a unified interface for managing Aptos accounts across different
signature schemes. They encapsulate key management, signing, and address derivation, enabling
developers to work with accounts without dealing with low-level cryptographic details.

### 1.2 Scope

This specification covers:

- Common account interface
- Single-key account types (Ed25519, Secp256k1)
- Authentication key derivation
- Mnemonic-based account creation
- Dynamic/polymorphic account handling

### 1.3 Definitions

| Term               | Definition                                            |
| ------------------ | ----------------------------------------------------- |
| Account            | An entity on Aptos identified by an address           |
| Single-Key Account | Account authenticated by a single private key         |
| Authentication Key | 32-byte hash derived from public key                  |
| Account Address    | 32-byte identifier, initially equal to auth key       |
| Signature Scheme   | Algorithm used for signing (Ed25519, Secp256k1, etc.) |

---

## 2. Account Interface

### 2.1 Overview

All account types **MUST** implement a common interface enabling polymorphic usage.

**Priority: P0 (Required)**

### 2.2 Required Methods [P0]

| Method                 | Return Type       | Description                         |
| ---------------------- | ----------------- | ----------------------------------- |
| `address()`            | AccountAddress    | Get the account's address           |
| `public_key_bytes()`   | bytes             | Get public key as raw bytes         |
| `signature_scheme()`   | SignatureScheme   | Get the signature scheme identifier |
| `sign(message)`        | Signature         | Sign arbitrary bytes                |
| `authentication_key()` | AuthenticationKey | Get the authentication key          |

### 2.3 Signature Scheme Identifiers [P0]

| Scheme       | String Identifier   | Byte Identifier | Priority |
| ------------ | ------------------- | --------------- | -------- |
| Ed25519      | `"ed25519"`         | 0x00            | P0       |
| Secp256k1    | `"secp256k1_ecdsa"` | 0x01            | P1       |
| Secp256r1    | `"secp256r1_ecdsa"` | 0x02            | P2       |
| MultiEd25519 | `"multi_ed25519"`   | 0x01            | P2       |
| MultiKey     | `"multi_key"`       | 0x03            | P2       |
| Keyless      | `"keyless"`         | 0x05            | P2       |

### 2.4 Optional Methods [P1]

| Method                  | Return Type | Description                    |
| ----------------------- | ----------- | ------------------------------ |
| `sign_transaction(txn)` | SignedTxn   | Sign a RawTransaction          |
| `public_key()`          | PublicKey   | Get typed public key reference |
| `verify(msg, sig)`      | bool        | Verify a signature             |

---

## 3. Ed25519Account

### 3.1 Overview

`Ed25519Account` is the primary account type for Aptos, using Ed25519 signatures.

**Priority: P0 (Required)**

### 3.2 Properties

| Property    | Type              | Description                            |
| ----------- | ----------------- | -------------------------------------- |
| address     | AccountAddress    | The account's on-chain address         |
| public_key  | Ed25519PublicKey  | The public key                         |
| private_key | Ed25519PrivateKey | The private key (not exposed in Debug) |

### 3.3 Construction [P0]

#### 3.3.1 Random Generation

**Signature:**

```
generate() -> Ed25519Account
```

**Requirements:**

1. Implementation **MUST** use CSPRNG for key generation
2. Implementation **MUST** derive address from authentication key

#### 3.3.2 From Private Key

**Signature:**

```
from_private_key(key: Ed25519PrivateKey) -> Ed25519Account
```

**Requirements:**

1. Implementation **MUST** derive public key from private key
2. Implementation **MUST** derive authentication key from public key
3. Implementation **MUST** set address equal to authentication key

#### 3.3.3 From Hex String

**Signature:**

```
from_private_key_hex(hex: string) -> Result<Ed25519Account, Error>
```

**Requirements:**

1. Implementation **MUST** accept hex with or without `0x` prefix
2. Implementation **MUST** accept 64-char (32-byte) or 128-char (64-byte) hex

#### 3.3.4 From Bytes

**Signature:**

```
from_private_key_bytes(bytes: bytes) -> Result<Ed25519Account, Error>
```

**Requirements:**

1. Implementation **MUST** accept 32-byte seed or 64-byte extended key
2. Invalid length **MUST** cause an error

### 3.4 Mnemonic Construction [P1]

#### 3.4.1 From Mnemonic (Default Path)

**Signature:**

```
from_mnemonic(mnemonic: Mnemonic) -> Result<Ed25519Account, Error>
```

**Default Path:** `m/44'/637'/0'/0'/0'`

#### 3.4.2 From Mnemonic with Custom Path

**Signature:**

```
from_mnemonic_with_path(mnemonic: Mnemonic, path: string) -> Result<Ed25519Account, Error>
```

### 3.5 Methods [P0]

| Method                      | Return Type       | Description              |
| --------------------------- | ----------------- | ------------------------ |
| `address()`                 | AccountAddress    | Get account address      |
| `public_key()`              | Ed25519PublicKey  | Get public key reference |
| `sign(message: bytes)`      | Ed25519Signature  | Sign arbitrary bytes     |
| `sign_transaction(raw_txn)` | SignedTransaction | Sign a raw transaction   |

### 3.6 Address Derivation [P0]

For Ed25519 accounts, the address is derived as follows:

```
authentication_key = SHA3-256(public_key || 0x00)
address = authentication_key  // For new accounts
```

Where:

- `public_key` is the 32-byte Ed25519 public key
- `0x00` is the Ed25519 scheme identifier
- The result is a 32-byte address

---

## 4. Secp256k1Account

### 4.1 Overview

`Secp256k1Account` provides Ethereum-compatible signing for wallet interoperability.

**Priority: P1 (Preferred)**

### 4.2 Properties

| Property    | Type                | Description                    |
| ----------- | ------------------- | ------------------------------ |
| address     | AccountAddress      | The account's on-chain address |
| public_key  | Secp256k1PublicKey  | The public key                 |
| private_key | Secp256k1PrivateKey | The private key                |

### 4.3 Construction [P1]

#### 4.3.1 Random Generation

**Signature:**

```
generate() -> Secp256k1Account
```

#### 4.3.2 From Private Key

**Signature:**

```
from_private_key(key: Secp256k1PrivateKey) -> Secp256k1Account
from_private_key_hex(hex: string) -> Result<Secp256k1Account, Error>
```

#### 4.3.3 From Mnemonic

**Signature:**

```
from_mnemonic(mnemonic: Mnemonic) -> Result<Secp256k1Account, Error>
```

**Default Path:** `m/44'/637'/0'/0'/0'`

### 4.4 Address Derivation [P1]

For Secp256k1 accounts:

```
authentication_key = SHA3-256(uncompressed_public_key || 0x01)
address = authentication_key
```

Where:

- `uncompressed_public_key` is the 65-byte uncompressed public key
- `0x01` is the Secp256k1 scheme identifier

---

## 5. Authentication Key

### 5.1 Overview

An `AuthenticationKey` is a 32-byte value derived from a public key and scheme identifier.

**Priority: P0 (Required)**

### 5.2 Data Representation

```
AuthenticationKey := [u8; 32]
```

### 5.3 Construction [P0]

#### 5.3.1 From Ed25519 Public Key

**Signature:**

```
from_ed25519(public_key: Ed25519PublicKey) -> AuthenticationKey
```

**Formula:**

```
auth_key = SHA3-256(public_key_bytes || 0x00)
```

#### 5.3.2 From Secp256k1 Public Key

**Signature:**

```
from_secp256k1(public_key: Secp256k1PublicKey) -> AuthenticationKey
```

**Formula:**

```
auth_key = SHA3-256(uncompressed_public_key || 0x01)
```

#### 5.3.3 From Any Public Key

**Signature:**

```
from_public_key(public_key_bytes: bytes, scheme: u8) -> AuthenticationKey
```

**Formula:**

```
auth_key = SHA3-256(public_key_bytes || scheme)
```

#### 5.3.4 From Raw Bytes

**Signature:**

```
from_bytes(bytes: [u8; 32]) -> AuthenticationKey
```

### 5.4 Methods [P0]

| Method              | Return Type    | Description                   |
| ------------------- | -------------- | ----------------------------- |
| `account_address()` | AccountAddress | Convert to account address    |
| `as_bytes()`        | [u8; 32]       | Get raw 32-byte array         |
| `to_hex()`          | string         | Get hex string with 0x prefix |

### 5.5 Account Address Relationship [P0]

For newly created accounts (before any authentication key rotation):

```
account_address = authentication_key
```

After authentication key rotation, the account address remains the same but the authentication key
changes.

---

## 6. Mnemonic-Based Accounts

### 6.1 Overview

Mnemonic-based accounts use BIP-39 mnemonics and BIP-44 derivation paths for deterministic key
generation.

**Priority: P1 (Preferred)**

### 6.2 Mnemonic Type

#### 6.2.1 Generation

**Signature:**

```
Mnemonic::generate(word_count: u8) -> Mnemonic
```

**Supported Word Counts:** 12, 15, 18, 21, 24

#### 6.2.2 Parsing

**Signature:**

```
Mnemonic::from_phrase(phrase: string) -> Result<Mnemonic, Error>
```

**Requirements:**

1. Implementation **MUST** validate checksum
2. Implementation **MUST** use BIP-39 English wordlist
3. Implementation **SHOULD** be case-insensitive
4. Implementation **SHOULD** normalize whitespace

#### 6.2.3 Validation

**Signature:**

```
Mnemonic::validate(phrase: string) -> bool
```

#### 6.2.4 Methods

| Method          | Return Type | Description                 |
| --------------- | ----------- | --------------------------- |
| `phrase()`      | string      | Get the mnemonic phrase     |
| `word_count()`  | u8          | Get number of words         |
| `to_seed(pass)` | [u8; 64]    | Derive seed with passphrase |

### 6.3 Derivation Path

#### 6.3.1 Aptos Standard Path

```
m / 44' / 637' / account' / change' / address_index'
```

**Default:** `m/44'/637'/0'/0'/0'`

#### 6.3.2 Path Parsing

**Signature:**

```
DerivationPath::from_string(path: string) -> Result<DerivationPath, Error>
```

**Requirements:**

1. Implementation **MUST** accept hardened notation (`'` or `h`)
2. Implementation **MUST** validate path format
3. Invalid paths **MUST** cause an error

### 6.4 Deriving Multiple Accounts

To derive multiple accounts from the same mnemonic:

```
Account 0: m/44'/637'/0'/0'/0'
Account 1: m/44'/637'/0'/0'/1'
Account 2: m/44'/637'/0'/0'/2'
...
Account N: m/44'/637'/0'/0'/N'
```

### 6.5 Example Usage

```
// Generate mnemonic
mnemonic = Mnemonic::generate(12)

// Create default account
account_0 = Ed25519Account::from_mnemonic(mnemonic)

// Create additional accounts
account_1 = Ed25519Account::from_mnemonic_with_path(mnemonic, "m/44'/637'/0'/0'/1'")
account_2 = Ed25519Account::from_mnemonic_with_path(mnemonic, "m/44'/637'/0'/0'/2'")
```

---

## 7. Dynamic Account (AnyAccount)

### 7.1 Overview

`AnyAccount` provides runtime polymorphism for accounts when the account type is not known at
compile time.

**Priority: P1 (Preferred)**

### 7.2 Variants

| Variant      | Wraps               | Priority |
| ------------ | ------------------- | -------- |
| Ed25519      | Ed25519Account      | P0       |
| Secp256k1    | Secp256k1Account    | P1       |
| Secp256r1    | Secp256r1Account    | P2       |
| MultiEd25519 | MultiEd25519Account | P2       |
| MultiKey     | MultiKeyAccount     | P2       |

### 7.3 Construction [P1]

**Signatures:**

```
AnyAccount::ed25519(account: Ed25519Account) -> AnyAccount
AnyAccount::secp256k1(account: Secp256k1Account) -> AnyAccount
```

### 7.4 Methods [P1]

`AnyAccount` **MUST** implement the standard account interface:

| Method                 | Description            |
| ---------------------- | ---------------------- |
| `address()`            | Get account address    |
| `public_key_bytes()`   | Get public key bytes   |
| `signature_scheme()`   | Get signature scheme   |
| `sign(message)`        | Sign arbitrary bytes   |
| `authentication_key()` | Get authentication key |

### 7.5 Usage Pattern

```
// Load account from config without knowing type
let account = match config.key_type {
    "ed25519" => AnyAccount::ed25519(Ed25519Account::from_hex(key)?),
    "secp256k1" => AnyAccount::secp256k1(Secp256k1Account::from_hex(key)?),
    _ => return Err("Unsupported key type"),
};

// Use uniformly
let address = account.address();
let signature = account.sign(message);
```

---

## 8. Account Serialization

### 8.1 Private Key Export [P0]

Implementations **MUST** provide methods to export private keys with appropriate warnings.

**Signatures:**

```
private_key_bytes() -> bytes
private_key_hex() -> string
```

**Requirements:**

1. Methods **SHOULD** have names indicating sensitivity (e.g., `export_private_key`)
2. Documentation **MUST** warn about security implications
3. Returned data **SHOULD** be zeroized after use

### 8.2 Public Key Export [P0]

**Signatures:**

```
public_key_bytes() -> bytes
public_key_hex() -> string
```

### 8.3 JSON Serialization [P1]

Implementations **SHOULD** support JSON serialization for configuration storage.

**Format:**

```json
{
  "type": "ed25519",
  "private_key": "0x...",
  "address": "0x..."
}
```

**Requirements:**

1. Private key **MUST** be hex-encoded
2. Type field **MUST** indicate signature scheme
3. Deserialization **MUST** validate consistency

---

## 9. Test Vectors

### 9.1 Address Derivation

Test vectors in `test-vectors/mnemonics.json`:

```json
{
  "derivation_vectors": [
    {
      "name": "default_path",
      "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
      "passphrase": "",
      "path": "m/44'/637'/0'/0'/0'",
      "expected_private_key": "0x...",
      "expected_public_key": "0x...",
      "expected_address": "0x..."
    }
  ]
}
```

### 9.2 Authentication Key

```json
{
  "auth_key_vectors": [
    {
      "scheme": "ed25519",
      "public_key_hex": "0x...",
      "expected_auth_key": "0x...",
      "expected_address": "0x..."
    }
  ]
}
```

---

## 10. Security Considerations

### 10.1 Private Key Handling

1. Private keys **MUST** be zeroized when account is dropped/destroyed
2. Private keys **MUST NOT** implement `Display` trait or appear in debug output
3. Private keys **MUST NOT** be logged or transmitted without explicit user action
4. Cloning private keys **SHOULD** require explicit acknowledgment

### 10.2 Mnemonic Security

1. Mnemonics **MUST** be generated with CSPRNG entropy
2. Mnemonics **SHOULD** be zeroized after seed derivation
3. Passphrase **SHOULD** be zeroized after seed derivation
4. Seed **SHOULD** be zeroized after key derivation

### 10.3 Account Creation

1. Generated accounts **MUST** have cryptographically random keys
2. Account addresses **MUST** be derived correctly from authentication keys
3. Authentication key derivation **MUST** use correct scheme identifier

### 10.4 Signing Security

1. Signing methods **SHOULD** indicate when signing occurs
2. Transaction signing **SHOULD** validate transaction fields
3. Implementations **SHOULD** prevent signing malformed transactions

---

## 11. References

### 11.1 Related Specifications

- [03-cryptography.md](03-cryptography.md) - Underlying cryptographic primitives
- [05-transactions.md](05-transactions.md) - Transaction signing

### 11.2 Feature Files

- `features/03-account-management/single-key.feature` - 30 single-key scenarios
- `features/03-account-management/mnemonic-derivation.feature` - 31 mnemonic scenarios
- `features/03-account-management/authentication-key.feature` - 19 auth key scenarios

### 11.3 Test Vectors

- `test-vectors/mnemonics.json`
- `test-vectors/signatures.json`
