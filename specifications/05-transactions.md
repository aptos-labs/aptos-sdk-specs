# Transactions Specification

## Abstract

This document specifies the transaction types and operations for Aptos SDKs, including raw
transaction construction, payload types, signing, and authenticators. Transactions are the primary
means of interacting with the Aptos blockchain.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [RawTransaction](#2-rawtransaction)
3. [Transaction Payloads](#3-transaction-payloads)
4. [Entry Function](#4-entry-function)
5. [Transaction Signing](#5-transaction-signing)
6. [SignedTransaction](#6-signedtransaction)
7. [Transaction Authenticator](#7-transaction-authenticator)
8. [Transaction Builder](#8-transaction-builder)
9. [Script Payload](#9-script-payload)
10. [Test Vectors](#10-test-vectors)
11. [Security Considerations](#11-security-considerations)
12. [References](#12-references)

---

## 1. Introduction

### 1.1 Purpose

Transactions are the fundamental unit of state change on Aptos. This specification defines how
SDKs construct, sign, and serialize transactions for submission to the network.

### 1.2 Scope

This specification covers:
- Raw transaction structure and fields
- Transaction payload types
- Entry function construction
- Signing message generation
- Transaction authenticators
- Builder pattern for transaction construction

### 1.3 Definitions

| Term                | Definition                                              |
| ------------------- | ------------------------------------------------------- |
| RawTransaction      | Unsigned transaction with all fields                    |
| SignedTransaction   | RawTransaction with authenticator (signature)           |
| Payload             | The operation to execute (entry function, script, etc.) |
| Authenticator       | Proof of authorization (signature + public key)         |
| Sequence Number     | Nonce preventing replay attacks                         |
| Gas                 | Computational resource unit                             |

---

## 2. RawTransaction

### 2.1 Overview

A `RawTransaction` contains all transaction data except the signature. It defines what operation to
perform, who is performing it, and the transaction parameters.

**Priority: P0 (Required)**

### 2.2 Fields [P0]

| Field                     | Type               | Description                           |
| ------------------------- | ------------------ | ------------------------------------- |
| sender                    | AccountAddress     | Transaction sender's address          |
| sequence_number           | u64                | Sender's current sequence number      |
| payload                   | TransactionPayload | The operation to execute              |
| max_gas_amount            | u64                | Maximum gas units to consume          |
| gas_unit_price            | u64                | Gas price in octas (1 APT = 10^8 octas)|
| expiration_timestamp_secs | u64                | Unix timestamp after which tx expires |
| chain_id                  | ChainId            | Network chain identifier              |

### 2.3 Construction [P0]

**Signature:**
```
RawTransaction::new(
    sender: AccountAddress,
    sequence_number: u64,
    payload: TransactionPayload,
    max_gas_amount: u64,
    gas_unit_price: u64,
    expiration_timestamp_secs: u64,
    chain_id: ChainId
) -> RawTransaction
```

### 2.4 Methods [P0]

| Method                          | Return Type        | Description                |
| ------------------------------- | ------------------ | -------------------------- |
| `sender()`                      | AccountAddress     | Get sender address         |
| `sequence_number()`             | u64                | Get sequence number        |
| `payload()`                     | &TransactionPayload| Get payload reference      |
| `max_gas_amount()`              | u64                | Get max gas                 |
| `gas_unit_price()`              | u64                | Get gas price              |
| `expiration_timestamp_secs()`   | u64                | Get expiration timestamp   |
| `chain_id()`                    | ChainId            | Get chain ID               |
| `signing_message()`             | bytes              | Get bytes to sign          |
| `sign(account)`                 | SignedTransaction  | Sign with account          |

### 2.5 BCS Serialization [P0]

Fields **MUST** be serialized in this exact order:

```
BCS(RawTransaction) :=
    BCS(sender)                     ||  // 32 bytes
    BCS(sequence_number)            ||  // 8 bytes, little-endian u64
    BCS(payload)                    ||  // Variable (enum)
    BCS(max_gas_amount)             ||  // 8 bytes, little-endian u64
    BCS(gas_unit_price)             ||  // 8 bytes, little-endian u64
    BCS(expiration_timestamp_secs)  ||  // 8 bytes, little-endian u64
    BCS(chain_id)                       // 1 byte
```

---

## 3. Transaction Payloads

### 3.1 Overview

`TransactionPayload` is an enum specifying the operation to execute.

**Priority: P0 (Required)**

### 3.2 Variants [P0]

```
TransactionPayload :=
    | Script(Script)           // 0x00 - Compiled Move script (deprecated)
    | ModuleBundle             // 0x01 - Module publishing (deprecated)
    | EntryFunction(EntryFunction)  // 0x02 - Call entry function
    | Multisig(Multisig)       // 0x03 - Multisig transaction
```

### 3.3 BCS Serialization [P0]

```
BCS(TransactionPayload) :=
    | 0x00 || BCS(Script)
    | 0x01                          // ModuleBundle (no additional data)
    | 0x02 || BCS(EntryFunction)
    | 0x03 || BCS(Multisig)
```

### 3.4 EntryFunction Variant [P0]

The `EntryFunction` variant is the primary payload type for most transactions.

---

## 4. Entry Function

### 4.1 Overview

An `EntryFunction` represents a call to a Move entry function on-chain.

**Priority: P0 (Required)**

### 4.2 Fields [P0]

| Field     | Type           | Description                        |
| --------- | -------------- | ---------------------------------- |
| module    | MoveModuleId   | Module containing the function     |
| function  | string         | Function name (identifier)         |
| type_args | Vec<TypeTag>   | Generic type arguments             |
| args      | Vec<bytes>     | BCS-encoded function arguments     |

### 4.3 Construction [P0]

**Signature:**
```
EntryFunction::new(
    module: MoveModuleId,
    function: string,
    type_args: Vec<TypeTag>,
    args: Vec<bytes>
) -> EntryFunction
```

### 4.4 Common Entry Functions [P0]

#### 4.4.1 APT Transfer

**Module:** `0x1::aptos_account`
**Function:** `transfer`
**Type Args:** None
**Args:** `[recipient: address, amount: u64]`

**Convenience Constructor:**
```
EntryFunction::apt_transfer(to: AccountAddress, amount: u64) -> EntryFunction
```

#### 4.4.2 Coin Transfer

**Module:** `0x1::coin`
**Function:** `transfer`
**Type Args:** `[CoinType]`
**Args:** `[recipient: address, amount: u64]`

**Convenience Constructor:**
```
EntryFunction::coin_transfer(
    coin_type: TypeTag,
    to: AccountAddress,
    amount: u64
) -> EntryFunction
```

### 4.5 Argument Encoding [P0]

Function arguments **MUST** be individually BCS-encoded:

| Move Type     | BCS Encoding                        |
| ------------- | ----------------------------------- |
| `address`     | 32 bytes (AccountAddress)           |
| `u8`          | 1 byte                              |
| `u16`         | 2 bytes, little-endian              |
| `u32`         | 4 bytes, little-endian              |
| `u64`         | 8 bytes, little-endian              |
| `u128`        | 16 bytes, little-endian             |
| `u256`        | 32 bytes, little-endian             |
| `bool`        | 1 byte (0x00 or 0x01)               |
| `vector<u8>`  | ULEB128 length + raw bytes          |
| `String`      | ULEB128 length + UTF-8 bytes        |
| `vector<T>`   | ULEB128 length + each element       |
| `Option<T>`   | 0x00 (None) or 0x01 + BCS(value)    |

### 4.6 BCS Serialization [P0]

```
BCS(EntryFunction) :=
    BCS(module)     ||  // MoveModuleId
    BCS(function)   ||  // String (ULEB128 len + UTF-8)
    BCS(type_args)  ||  // Vec<TypeTag> (ULEB128 count + each)
    BCS(args)           // Vec<bytes> (ULEB128 count + each as bytes)
```

---

## 5. Transaction Signing

### 5.1 Overview

Transaction signing creates a cryptographic proof that the sender authorized the transaction.

**Priority: P0 (Required)**

### 5.2 Single Signer Signing Message [P0]

**Formula:**
```
signing_message = prefix || BCS(raw_transaction)
```

**Prefix Computation:**
```
prefix = SHA3-256("APTOS::RawTransaction")
```

The prefix is a fixed 32-byte value:
```
prefix_hex = "0xb5e97db07fa0bd0e5598aa3643a9bc6f6693bddc1a9fec9e674a461eaa00b193"
```

### 5.3 Signing Process [P0]

1. Compute signing message: `prefix || BCS(raw_transaction)`
2. Sign the message with account's private key
3. Create authenticator with public key and signature
4. Combine raw transaction and authenticator into SignedTransaction

### 5.4 Multi-Agent Signing Message [P2]

For transactions with multiple signers:

**Formula:**
```
signing_message = prefix || BCS(RawTransactionWithData::MultiAgent)
```

**Prefix:**
```
prefix = SHA3-256("APTOS::RawTransactionWithData")
```

**RawTransactionWithData::MultiAgent:**
```
{
    raw_txn: RawTransaction,
    secondary_signer_addresses: Vec<AccountAddress>
}
```

### 5.5 Fee Payer Signing Message [P2]

For sponsored transactions:

**Formula:**
```
signing_message = prefix || BCS(RawTransactionWithData::FeePayer)
```

**RawTransactionWithData::FeePayer:**
```
{
    raw_txn: RawTransaction,
    secondary_signer_addresses: Vec<AccountAddress>,
    fee_payer_address: AccountAddress
}
```

---

## 6. SignedTransaction

### 6.1 Overview

A `SignedTransaction` is a `RawTransaction` combined with an authenticator, ready for submission.

**Priority: P0 (Required)**

### 6.2 Fields [P0]

| Field         | Type                     | Description              |
| ------------- | ------------------------ | ------------------------ |
| raw_txn       | RawTransaction           | The unsigned transaction |
| authenticator | TransactionAuthenticator | Signature(s)             |

### 6.3 Construction [P0]

**Signature:**
```
SignedTransaction::new(
    raw_txn: RawTransaction,
    authenticator: TransactionAuthenticator
) -> SignedTransaction
```

### 6.4 Methods [P0]

| Method              | Return Type                 | Description                   |
| ------------------- | --------------------------- | ----------------------------- |
| `raw_transaction()` | &RawTransaction             | Get raw transaction reference |
| `authenticator()`   | &TransactionAuthenticator   | Get authenticator reference   |
| `to_bytes()`        | bytes                       | Serialize to BCS bytes        |
| `hash()`            | HashValue                   | Compute transaction hash      |

### 6.5 Transaction Hash [P0]

**Formula:**
```
hash = SHA3-256(prefix || BCS(SignedTransaction))
```

**Prefix:**
```
prefix = SHA3-256("APTOS::Transaction")
```

### 6.6 BCS Serialization [P0]

```
BCS(SignedTransaction) :=
    BCS(raw_txn) ||
    BCS(authenticator)
```

---

## 7. Transaction Authenticator

### 7.1 Overview

`TransactionAuthenticator` provides proof of transaction authorization.

**Priority: P0 (Required)**

### 7.2 Variants [P0]

```
TransactionAuthenticator :=
    | Ed25519(Ed25519Authenticator)              // 0x00
    | MultiEd25519(MultiEd25519Authenticator)    // 0x01
    | MultiAgent(MultiAgentAuthenticator)        // 0x02
    | FeePayer(FeePayerAuthenticator)            // 0x03
    | SingleSender(SingleSenderAuthenticator)    // 0x04
```

### 7.3 Ed25519Authenticator [P0]

| Field      | Type             | Size     |
| ---------- | ---------------- | -------- |
| public_key | Ed25519PublicKey | 32 bytes |
| signature  | Ed25519Signature | 64 bytes |

**BCS Serialization:**
```
BCS(Ed25519Authenticator) :=
    BCS(public_key) ||  // 32 bytes
    BCS(signature)      // 64 bytes
```

### 7.4 SingleSenderAuthenticator [P0]

Used with `AnyPublicKey` for flexible key type support.

| Field | Type                 |
| ----- | -------------------- |
| sender| AccountAuthenticator |

### 7.5 AccountAuthenticator [P0]

```
AccountAuthenticator :=
    | Ed25519(Ed25519Authenticator)           // 0x00
    | MultiEd25519(MultiEd25519Authenticator) // 0x01
    | SingleKey(SingleKeyAuthenticator)       // 0x02
    | MultiKey(MultiKeyAuthenticator)         // 0x03
```

### 7.6 MultiAgentAuthenticator [P2]

| Field                      | Type                      |
| -------------------------- | ------------------------- |
| sender                     | AccountAuthenticator      |
| secondary_signer_addresses | Vec<AccountAddress>       |
| secondary_signers          | Vec<AccountAuthenticator> |

### 7.7 FeePayerAuthenticator [P2]

| Field                      | Type                      |
| -------------------------- | ------------------------- |
| sender                     | AccountAuthenticator      |
| secondary_signer_addresses | Vec<AccountAddress>       |
| secondary_signers          | Vec<AccountAuthenticator> |
| fee_payer_address          | AccountAddress            |
| fee_payer_signer           | AccountAuthenticator      |

---

## 8. Transaction Builder

### 8.1 Overview

The `TransactionBuilder` provides a fluent API for constructing transactions.

**Priority: P1 (Preferred)**

### 8.2 Default Values [P1]

| Field              | Default Value              |
| ------------------ | -------------------------- |
| max_gas_amount     | 200,000                    |
| gas_unit_price     | 100                        |
| expiration         | current_time + 600 seconds |

### 8.3 Builder Methods [P1]

| Method                          | Description                    |
| ------------------------------- | ------------------------------ |
| `new()`                         | Create builder with defaults   |
| `sender(address)`               | Set sender address             |
| `sequence_number(seq)`          | Set sequence number            |
| `payload(payload)`              | Set transaction payload        |
| `max_gas_amount(amount)`        | Set maximum gas                |
| `gas_unit_price(price)`         | Set gas price                  |
| `expiration_timestamp_secs(ts)` | Set absolute expiration        |
| `expiration_from_now(secs)`     | Set relative expiration        |
| `chain_id(id)`                  | Set chain ID                   |
| `build()`                       | Build RawTransaction           |

### 8.4 Example Usage

```
let raw_txn = TransactionBuilder::new()
    .sender(account.address())
    .sequence_number(0)
    .payload(EntryFunction::apt_transfer(recipient, 100_000_000))
    .max_gas_amount(10_000)
    .gas_unit_price(100)
    .expiration_from_now(600)
    .chain_id(ChainId::TESTNET)
    .build()?;
```

### 8.5 Validation [P1]

`build()` **MUST** fail if required fields are missing:

| Missing Field    | Error                    |
| ---------------- | ------------------------ |
| sender           | MissingSender            |
| sequence_number  | MissingSequenceNumber    |
| payload          | MissingPayload           |
| chain_id         | MissingChainId           |

---

## 9. Script Payload

### 9.1 Overview

A `Script` payload executes compiled Move script bytecode directly.

**Priority: P2 (Optional)**

### 9.2 Fields [P2]

| Field     | Type                | Description              |
| --------- | ------------------- | ------------------------ |
| code      | bytes               | Compiled script bytecode |
| type_args | Vec<TypeTag>        | Type arguments           |
| args      | Vec<ScriptArgument> | Script arguments         |

### 9.3 ScriptArgument Variants [P2]

```
ScriptArgument :=
    | U8(u8)                 // 0x00
    | U64(u64)               // 0x01
    | U128(u128)             // 0x02
    | Address(AccountAddress)// 0x03
    | U8Vector(Vec<u8>)      // 0x04
    | Bool(bool)             // 0x05
    | U16(u16)               // 0x06
    | U32(u32)               // 0x07
    | U256(U256)             // 0x08
```

---

## 10. Test Vectors

### 10.1 Transaction Serialization

Test vectors in `test-vectors/transactions.json`:

```json
{
  "raw_transaction_vectors": [
    {
      "name": "apt_transfer",
      "sender": "0x...",
      "sequence_number": 0,
      "payload": {
        "type": "entry_function",
        "module": "0x1::aptos_account",
        "function": "transfer",
        "type_args": [],
        "args": ["0x...", "1000000"]
      },
      "max_gas_amount": 10000,
      "gas_unit_price": 100,
      "expiration_timestamp_secs": 1700000000,
      "chain_id": 2,
      "expected_bcs_hex": "0x...",
      "expected_signing_message_hex": "0x..."
    }
  ]
}
```

### 10.2 Signing Message

```json
{
  "signing_vectors": [
    {
      "raw_txn_bcs_hex": "0x...",
      "expected_signing_message_hex": "0x...",
      "private_key_hex": "0x...",
      "expected_signature_hex": "0x..."
    }
  ]
}
```

---

## 11. Security Considerations

### 11.1 Signing Safety

1. Implementation **MUST** use domain separation for signing messages
2. Implementation **MUST NOT** sign arbitrary data without explicit user consent
3. Implementation **SHOULD** display transaction details before signing

### 11.2 Sequence Number

1. Sequence number **MUST** match account's current sequence number
2. Incorrect sequence number results in transaction rejection
3. Implementation **SHOULD** fetch current sequence number before signing

### 11.3 Expiration

1. Expiration **SHOULD** be set to reasonable future time (5-10 minutes)
2. Expired transactions are rejected by the network
3. Too-long expiration increases replay attack window

### 11.4 Gas Limits

1. max_gas_amount **SHOULD** be set to reasonable limit
2. Unlimited gas can drain account on failed transactions
3. Implementation **MAY** provide simulation to estimate gas

### 11.5 Chain ID

1. Chain ID **MUST** match the target network
2. Mismatched chain ID results in rejection
3. Prevents replay attacks across networks

---

## 12. References

### 12.1 Related Specifications

- [01-core-types.md](01-core-types.md) - AccountAddress, TypeTag, ChainId
- [02-bcs-serialization.md](02-bcs-serialization.md) - BCS format
- [04-accounts.md](04-accounts.md) - Account signing
- [06-api-clients.md](06-api-clients.md) - Transaction submission

### 12.2 Feature Files

- `features/04-transaction-building/raw-transaction.feature` - 25 raw txn scenarios
- `features/04-transaction-building/entry-function.feature` - 29 entry fn scenarios
- `features/04-transaction-building/script.feature` - 25 script scenarios
- `features/04-transaction-building/signing.feature` - 26 signing scenarios

### 12.3 Test Vectors

- `test-vectors/transactions.json`
