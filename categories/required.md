# Required Features (P0)

These features are **mandatory** for any Aptos SDK implementation. Without these features, an SDK cannot be considered functional for basic blockchain interaction.

## Criteria for Required Features

A feature is classified as Required if:
1. It is necessary for basic blockchain interaction
2. All reference SDKs (TypeScript, Python, Go, .NET) implement it
3. Users cannot reasonably work around its absence
4. It involves core Aptos protocol concepts

---

## Core Types

### AccountAddress
- Parse hex strings with and without `0x` prefix
- Support short-form addresses (e.g., `0x1`)
- Format to full 64-character hex string
- Format to short string (leading zeros removed)
- Validate address length (32 bytes)
- Provide standard addresses (ONE, ZERO, THREE, FOUR)
- BCS serialization as 32 bytes
- JSON serialization as hex string

### ChainId
- Create from numeric value (u8)
- Provide constants for known networks (MAINNET=1, TESTNET=2, DEVNET=3)
- BCS serialization as single byte

### TypeTag
- Parse primitive types (bool, u8, u16, u32, u64, u128, u256, address, signer)
- Parse vector types (vector<T>)
- Parse struct types (address::module::Name<T>)
- Format to canonical string representation
- BCS serialization

---

## Cryptography

### Ed25519
- Generate random key pairs
- Create key pair from 32-byte seed
- Create key pair from 64-byte private key (seed + public key)
- Sign arbitrary messages
- Verify signatures
- Export public key as 32 bytes
- Export private key as bytes (with appropriate security warnings)

### Hashing
- SHA3-256 hashing
- SHA2-256 hashing (for BIP-39 compatibility)
- Domain-separated hashing for Aptos types

### AuthenticationKey
- Derive from Ed25519 public key
- Derive from any public key with scheme identifier
- Convert to AccountAddress

---

## Account Management

### Single-Key Accounts
- Create Ed25519 account from private key
- Create Ed25519 account from hex-encoded private key
- Generate new random Ed25519 account
- Get account address
- Get public key
- Sign messages
- Sign transactions

### Account Interface
- Unified interface for all account types
- Get address
- Get public key bytes
- Get signature scheme identifier
- Sign arbitrary bytes

---

## Transaction Building

### RawTransaction
- Construct with all required fields:
  - sender address
  - sequence number
  - payload
  - max gas amount
  - gas unit price
  - expiration timestamp
  - chain ID
- BCS serialization
- Generate signing message (with domain separator)

### TransactionPayload
- EntryFunction payload construction
- Specify module ID (address::name)
- Specify function name
- Specify type arguments
- Specify BCS-encoded arguments

### EntryFunction
- Create APT transfer (0x1::aptos_account::transfer)
- Create coin transfer with type argument
- BCS-encode Move arguments

### SignedTransaction
- Create from RawTransaction and authenticator
- BCS serialization for submission
- Compute transaction hash

### TransactionAuthenticator
- Ed25519 single-signer authenticator
- Include public key and signature

---

## BCS Serialization

### Primitives
- Serialize/deserialize bool
- Serialize/deserialize u8, u16, u32, u64, u128
- Serialize/deserialize bytes (length-prefixed)
- Serialize/deserialize strings (length-prefixed UTF-8)
- Serialize/deserialize optional values
- Serialize/deserialize sequences (length-prefixed)

### Aptos Types
- Serialize/deserialize AccountAddress
- Serialize/deserialize RawTransaction
- Serialize/deserialize SignedTransaction
- Serialize/deserialize EntryFunction

---

## API Client

### Fullnode REST API

#### Ledger Info
- Get current ledger information
- Parse chain ID, ledger version, block height

#### Account Queries
- Get account info (sequence number, authentication key)
- Get account resources
- Get specific resource by type

#### Transaction Queries
- Get transaction by hash
- Get transaction by version

#### Transaction Submission
- Submit signed transaction (BCS format)
- Handle submission response
- Parse pending transaction hash

#### Transaction Waiting
- Wait for transaction confirmation
- Handle timeout
- Parse final transaction status

---

## Error Handling

### Required Error Cases
- Invalid address format
- Invalid private key
- Invalid signature
- Transaction not found
- Account not found
- Network connection failure
- Request timeout
- API error responses

### Error Information
- Error type/code
- Human-readable message
- Original error cause (when applicable)

---

## Compliance Checklist

An SDK claiming P0 compliance must pass all Gherkin scenarios tagged with `@required` in the following feature files:

- [ ] `01-core-types/address.feature`
- [ ] `01-core-types/type-tags.feature`
- [ ] `01-core-types/serialization.feature`
- [ ] `02-cryptography/ed25519.feature`
- [ ] `02-cryptography/hashing.feature`
- [ ] `03-account-management/single-key.feature`
- [ ] `03-account-management/authentication-key.feature`
- [ ] `04-transaction-building/raw-transaction.feature`
- [ ] `04-transaction-building/entry-function.feature`
- [ ] `04-transaction-building/signing.feature`
- [ ] `05-api-clients/fullnode-api.feature`
- [ ] `05-api-clients/transaction-submission.feature`

