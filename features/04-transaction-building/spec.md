# Transaction Building Specification

## Overview

The transaction building module provides types and utilities for constructing, signing, and serializing Aptos transactions. It supports various transaction types including entry functions, scripts, and advanced transaction modes.

## Goals

1. Type-safe transaction construction
2. Support all transaction payload types
3. Enable multi-agent and fee payer transactions
4. Provide ergonomic builder pattern

## Non-Goals

- Transaction simulation (handled by API clients)
- Transaction submission (handled by API clients)
- Gas estimation (handled by API clients)

---

## RawTransaction (Required - P0)

### Description

The unsigned transaction structure containing all transaction details.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| sender | AccountAddress | Transaction sender's address |
| sequence_number | u64 | Sender's account sequence number |
| payload | TransactionPayload | The transaction operation |
| max_gas_amount | u64 | Maximum gas units to consume |
| gas_unit_price | u64 | Gas price in octas |
| expiration_timestamp_secs | u64 | Unix timestamp after which tx expires |
| chain_id | ChainId | Network chain identifier |

### Construction

| Method | Priority | Description |
|--------|----------|-------------|
| `new(...)` | P0 | Create with all fields |
| `builder()` | P1 | Create using builder pattern |

### Methods

| Method | Priority | Description |
|--------|----------|-------------|
| `sender()` | P0 | Get sender address |
| `sequence_number()` | P0 | Get sequence number |
| `payload()` | P0 | Get payload reference |
| `signing_message()` | P0 | Generate bytes to sign |
| `sign(account)` | P0 | Sign and create SignedTransaction |

### BCS Serialization Order

Fields must be serialized in this exact order:
1. sender (32 bytes)
2. sequence_number (u64)
3. payload (variant + data)
4. max_gas_amount (u64)
5. gas_unit_price (u64)
6. expiration_timestamp_secs (u64)
7. chain_id (u8)

---

## TransactionPayload (Required - P0)

### Description

Enum of possible transaction operations.

### Variants

| Variant | Priority | Description |
|---------|----------|-------------|
| EntryFunction | P0 | Call a Move entry function |
| Script | P2 | Execute compiled Move script |
| Multisig | P2 | Execute through multisig account |

---

## EntryFunction (Required - P0)

### Description

Payload for calling Move entry functions.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| module | MoveModuleId | Module containing the function |
| function | String | Function name |
| type_args | Vec<TypeTag> | Type arguments |
| args | Vec<Vec<u8>> | BCS-encoded arguments |

### Construction

| Method | Priority | Description |
|--------|----------|-------------|
| `new(module, function, type_args, args)` | P0 | Create from components |
| `apt_transfer(to, amount)` | P0 | Create APT transfer |
| `coin_transfer(coin_type, to, amount)` | P0 | Create coin transfer |

### Common Entry Functions

| Function | Priority | Module | Description |
|----------|----------|--------|-------------|
| APT Transfer | P0 | `0x1::aptos_account::transfer` | Transfer APT |
| Coin Transfer | P0 | `0x1::coin::transfer` | Transfer any coin |
| Register Coin | P1 | `0x1::managed_coin::register` | Register coin store |

### Argument Encoding

All arguments must be BCS-encoded:
```
address → 32 bytes
u64 → 8 bytes little-endian
bool → 1 byte (0x00 or 0x01)
vector<u8> → ULEB128 length + bytes
string → ULEB128 length + UTF-8 bytes
```

---

## SignedTransaction (Required - P0)

### Description

A signed transaction ready for submission.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| raw_txn | RawTransaction | The unsigned transaction |
| authenticator | TransactionAuthenticator | Signature(s) |

### Construction

| Method | Priority | Description |
|--------|----------|-------------|
| `new(raw_txn, authenticator)` | P0 | Create from components |

### Methods

| Method | Priority | Description |
|--------|----------|-------------|
| `raw_transaction()` | P0 | Get raw transaction reference |
| `authenticator()` | P0 | Get authenticator reference |
| `to_bytes()` | P0 | Serialize to BCS bytes |
| `hash()` | P0 | Compute transaction hash |

### Transaction Hash

```
hash = SHA3-256(SHA3-256("APTOS::Transaction") || bcs(SignedTransaction))
```

---

## TransactionAuthenticator (Required - P0)

### Description

Container for transaction signatures.

### Variants

| Variant | Priority | Description |
|---------|----------|-------------|
| Ed25519 | P0 | Single Ed25519 signature |
| Secp256k1Ecdsa | P1 | Single Secp256k1 signature |
| MultiAgent | P2 | Multiple signers |
| FeePayer | P2 | Sponsored transaction |

### Ed25519 Variant

| Field | Type |
|-------|------|
| public_key | Ed25519PublicKey |
| signature | Ed25519Signature |

### Secp256k1 Variant

| Field | Type |
|-------|------|
| public_key | Secp256k1PublicKey |
| signature | Secp256k1Signature |

---

## Signing Message Construction

### Single Signer (Required - P0)

```
message = SHA3-256("APTOS::RawTransaction") || bcs(RawTransaction)
```

The domain separator `SHA3-256("APTOS::RawTransaction")` is 32 bytes.

### Multi-Agent (Optional - P2)

```
message = SHA3-256("APTOS::RawTransactionWithData") || bcs(RawTransactionWithData::MultiAgent)
```

Where `RawTransactionWithData::MultiAgent` contains:
- raw_txn: RawTransaction
- secondary_signer_addresses: Vec<AccountAddress>

### Fee Payer (Optional - P2)

```
message = SHA3-256("APTOS::RawTransactionWithData") || bcs(RawTransactionWithData::FeePayer)
```

Where `RawTransactionWithData::FeePayer` contains:
- raw_txn: RawTransaction
- secondary_signer_addresses: Vec<AccountAddress>
- fee_payer_address: AccountAddress

---

## TransactionBuilder (Preferred - P1)

### Description

Fluent builder for constructing transactions.

### Default Values

| Field | Default |
|-------|---------|
| max_gas_amount | 200,000 |
| gas_unit_price | 100 |
| expiration | current time + 600 seconds |

### Methods

| Method | Priority | Description |
|--------|----------|-------------|
| `new()` | P1 | Create builder with defaults |
| `sender(address)` | P1 | Set sender |
| `sequence_number(seq)` | P1 | Set sequence number |
| `payload(payload)` | P1 | Set payload |
| `max_gas_amount(amount)` | P1 | Set max gas |
| `gas_unit_price(price)` | P1 | Set gas price |
| `expiration_timestamp_secs(ts)` | P1 | Set expiration |
| `expiration_from_now(secs)` | P1 | Set relative expiration |
| `chain_id(id)` | P1 | Set chain ID |
| `build()` | P1 | Build RawTransaction |

---

## Script Payload (Optional - P2)

### Description

Execute compiled Move script bytecode.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| code | Vec<u8> | Compiled script bytecode |
| type_args | Vec<TypeTag> | Type arguments |
| args | Vec<ScriptArgument> | Script arguments |

### ScriptArgument Variants

| Variant | Type |
|---------|------|
| U8 | u8 |
| U16 | u16 |
| U32 | u32 |
| U64 | u64 |
| U128 | u128 |
| U256 | U256 |
| Address | AccountAddress |
| Bool | bool |
| U8Vector | Vec<u8> |

---

## Error Handling

### Required Error Cases

| Error | Cause | Priority |
|-------|-------|----------|
| MissingSender | Builder missing sender | P1 |
| MissingSequenceNumber | Builder missing seq num | P1 |
| MissingPayload | Builder missing payload | P1 |
| MissingChainId | Builder missing chain ID | P1 |
| MissingExpiration | Builder missing expiration | P1 |
| SerializationError | BCS encoding failed | P0 |
| SigningError | Signature creation failed | P0 |

---

## Security Considerations

1. **Signing Message**: Always use domain separator
2. **Expiration**: Set reasonable expiration (not too long)
3. **Sequence Number**: Ensure correct to prevent replay
4. **Gas Limits**: Set appropriate limits to prevent draining

---

## Cross-SDK Compatibility

All SDKs must produce identical:
1. BCS-serialized RawTransaction bytes
2. Signing messages for same transaction
3. Transaction hashes for same signed transaction

Test vectors in `test-vectors/transactions.json` provide deterministic test cases.

