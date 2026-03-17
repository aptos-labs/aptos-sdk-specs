# Advanced Features Specification

## Abstract

This document specifies advanced features for Aptos SDKs including multi-signature accounts,
multi-agent transactions, fee payer (sponsored) transactions, and keyless accounts. These features
extend SDK capabilities for complex use cases.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Multi-Signature Accounts](#2-multi-signature-accounts)
3. [Multi-Agent Transactions](#3-multi-agent-transactions)
4. [Fee Payer Transactions](#4-fee-payer-transactions)
5. [Keyless Accounts](#5-keyless-accounts)
6. [Transaction Simulation](#6-transaction-simulation)
7. [Code Generation](#7-code-generation)
8. [Test Vectors](#8-test-vectors)
9. [Security Considerations](#9-security-considerations)
10. [References](#10-references)

---

## 1. Introduction

### 1.1 Purpose

Advanced features enable sophisticated use cases beyond basic single-signer transactions, including
shared custody, sponsored transactions, and OAuth-based authentication.

### 1.2 Scope

This specification covers:

- Multi-Ed25519 threshold accounts
- MultiKey mixed-type accounts
- Multi-agent transactions with multiple signers
- Fee payer (sponsored) transactions
- Keyless accounts using OIDC providers

### 1.3 Definitions

| Term          | Definition                                       |
| ------------- | ------------------------------------------------ |
| Multi-sig     | Account requiring M-of-N signatures              |
| Multi-agent   | Transaction with multiple independent signers    |
| Fee Payer     | Third party paying transaction gas fees          |
| Keyless       | Account authenticated via OIDC (OAuth) providers |
| Threshold     | Minimum signatures required for authorization    |
| Ephemeral Key | Short-lived key used in keyless authentication   |

---

## 2. Multi-Signature Accounts

### 2.1 Overview

Multi-signature accounts require a threshold of signatures from a set of authorized keys.

**Priority: P2 (Optional)**

### 2.2 MultiEd25519

#### 2.2.1 Key Components

| Component   | Description                         |
| ----------- | ----------------------------------- |
| public_keys | Vec of N Ed25519 public keys        |
| threshold   | M signatures required (1 <= M <= N) |
| signatures  | Vec of (index, signature) pairs     |

#### 2.2.2 Construction [P2]

**Signatures:**

```
MultiEd25519PublicKey::new(
    keys: Vec<Ed25519PublicKey>,
    threshold: u8
) -> Result<MultiEd25519PublicKey, Error>

MultiEd25519Account::new(
    private_keys: Vec<Ed25519PrivateKey>,
    threshold: u8
) -> Result<MultiEd25519Account, Error>
```

**Requirements:**

1. `threshold` **MUST** be >= 1
2. `threshold` **MUST** be <= number of keys
3. Number of keys **MUST** be <= 32

#### 2.2.3 Authentication Key Derivation [P2]

**Formula:**

```
auth_key = SHA3-256(
    pk1 || pk2 || ... || pkN ||
    threshold ||
    0x01
)
```

Where:

- `pk1...pkN` are the 32-byte Ed25519 public keys
- `threshold` is a single byte
- `0x01` is the MultiEd25519 scheme identifier

#### 2.2.4 Signature Collection [P2]

**Methods:**

```
can_sign() -> bool                    // Check if enough keys for threshold
add_signature(index: u8, sig) -> ()   // Add partial signature
collect_signatures() -> MultiEd25519Signature
```

#### 2.2.5 BCS Serialization [P2]

**Public Key:**

```
BCS(MultiEd25519PublicKey) :=
    BCS(public_keys: Vec<[u8; 32]>) ||
    BCS(threshold: u8)
```

**Signature:**

```
BCS(MultiEd25519Signature) :=
    BCS(signatures: Vec<[u8; 64]>) ||
    BCS(bitmap: [u8; 4])
```

The bitmap indicates which signers provided signatures (bit i set = signer i signed).

### 2.3 MultiKey (Mixed Key Types)

#### 2.3.1 Overview

MultiKey allows mixing different key types (Ed25519, Secp256k1, etc.) with optional weights.

**Priority: P2 (Optional)**

#### 2.3.2 Key Components

| Component           | Description                       |
| ------------------- | --------------------------------- |
| public_keys         | Vec of AnyPublicKey (mixed types) |
| signatures_required | Total signature weight required   |

#### 2.3.3 Authentication Key Derivation [P2]

**Formula:**

```
auth_key = SHA3-256(
    ULEB128(N) ||           // Number of keys
    pk1 || pk2 || ... || pkN ||
    signatures_required ||
    0x03
)
```

Where `0x03` is the MultiKey scheme identifier.

---

## 3. Multi-Agent Transactions

### 3.1 Overview

Multi-agent transactions have multiple independent signers, each authorizing their portion of the
transaction.

**Priority: P2 (Optional)**

### 3.2 Use Cases

- Atomic swaps between parties
- Multi-party agreements
- Shared resource operations
- Escrow releases

### 3.3 Signing Message [P2]

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

### 3.4 Signing Process [P2]

1. Sender creates RawTransaction
2. Sender signs the multi-agent signing message
3. Each secondary signer signs the same message
4. Signatures are collected into MultiAgentAuthenticator
5. Transaction is submitted

### 3.5 Construction [P2]

**Methods:**

```
// Add secondary signer to transaction
add_secondary_signer(address: AccountAddress) -> ()

// Sign as primary sender
sign_as_sender(
    raw_txn: RawTransaction,
    secondary_addresses: Vec<AccountAddress>,
    sender_account: Account
) -> AccountAuthenticator

// Sign as secondary signer
sign_as_secondary(
    raw_txn: RawTransaction,
    sender: AccountAddress,
    secondary_addresses: Vec<AccountAddress>,
    signer_account: Account
) -> AccountAuthenticator

// Combine into signed transaction
combine_multi_agent_signatures(
    raw_txn: RawTransaction,
    sender_auth: AccountAuthenticator,
    secondary_addresses: Vec<AccountAddress>,
    secondary_auths: Vec<AccountAuthenticator>
) -> SignedTransaction
```

### 3.6 MultiAgentAuthenticator Structure [P2]

| Field                      | Type                      |
| -------------------------- | ------------------------- |
| sender                     | AccountAuthenticator      |
| secondary_signer_addresses | Vec<AccountAddress>       |
| secondary_signers          | Vec<AccountAuthenticator> |

**Requirements:**

1. `secondary_signer_addresses.len()` **MUST** equal `secondary_signers.len()`
2. Order of addresses **MUST** match order of authenticators
3. All parties **MUST** sign the same message

---

## 4. Fee Payer Transactions

### 4.1 Overview

Fee payer (sponsored) transactions allow a third party to pay gas fees on behalf of the sender.

**Priority: P2 (Optional)**

### 4.2 Use Cases

- User onboarding (gasless first transaction)
- dApp subsidized operations
- Enterprise sponsored activities
- Game item minting without user gas

### 4.3 Signing Message [P2]

**Formula:**

```
signing_message = prefix || BCS(RawTransactionWithData::FeePayer)
```

**Prefix:**

```
prefix = SHA3-256("APTOS::RawTransactionWithData")
```

**RawTransactionWithData::FeePayer:**

```
{
    raw_txn: RawTransaction,
    secondary_signer_addresses: Vec<AccountAddress>,
    fee_payer_address: AccountAddress
}
```

### 4.4 Fee Payer Flow [P2]

1. Sender creates RawTransaction (gas fields can be placeholders)
2. Sender signs the fee payer signing message
3. Transaction is sent to fee payer
4. Fee payer reviews transaction details
5. Fee payer signs the same message
6. Signatures combined into FeePayerAuthenticator
7. Transaction is submitted

### 4.5 Construction [P2]

**Methods:**

```
// Sign as sender (not paying gas)
sign_as_sender_for_fee_payer(
    raw_txn: RawTransaction,
    fee_payer_address: AccountAddress,
    sender_account: Account
) -> AccountAuthenticator

// Sign as fee payer (paying gas)
sign_as_fee_payer(
    raw_txn: RawTransaction,
    sender: AccountAddress,
    secondary_addresses: Vec<AccountAddress>,
    fee_payer_account: Account
) -> AccountAuthenticator

// Combine into signed transaction
combine_fee_payer_signatures(
    raw_txn: RawTransaction,
    sender_auth: AccountAuthenticator,
    secondary_addresses: Vec<AccountAddress>,
    secondary_auths: Vec<AccountAuthenticator>,
    fee_payer_address: AccountAddress,
    fee_payer_auth: AccountAuthenticator
) -> SignedTransaction
```

### 4.6 FeePayerAuthenticator Structure [P2]

| Field                      | Type                      |
| -------------------------- | ------------------------- |
| sender                     | AccountAuthenticator      |
| secondary_signer_addresses | Vec<AccountAddress>       |
| secondary_signers          | Vec<AccountAuthenticator> |
| fee_payer_address          | AccountAddress            |
| fee_payer_signer           | AccountAuthenticator      |

### 4.7 Gas Considerations [P2]

1. Fee payer's account is charged for gas
2. Fee payer **SHOULD** verify transaction won't drain excessive gas
3. RawTransaction's gas fields apply (max_gas_amount, gas_unit_price)

---

## 5. Keyless Accounts

### 5.1 Overview

Keyless accounts use OpenID Connect (OIDC) for authentication instead of traditional cryptographic
keys.

**Priority: P2 (Optional)**

### 5.2 Supported Providers

| Provider | Issuer URL                  |
| -------- | --------------------------- |
| Google   | https://accounts.google.com |
| Apple    | https://appleid.apple.com   |

### 5.3 Components

| Component        | Description                         |
| ---------------- | ----------------------------------- |
| EphemeralKeyPair | Short-lived Ed25519 key for signing |
| JWT              | OIDC identity token from provider   |
| Pepper           | Privacy-preserving random value     |
| ZK Proof         | Zero-knowledge proof of identity    |

### 5.4 Authentication Key Derivation [P2]

**Formula:**

```
auth_key = SHA3-256(
    SHA3-256(iss) ||
    SHA3-256(aud) ||
    SHA3-256(uid_key || uid_val) ||
    pepper ||
    0x05
)
```

Where:

- `iss` is the OIDC issuer URL
- `aud` is the application's client ID
- `uid_key` is the claim name (e.g., "sub" or "email")
- `uid_val` is the user's identifier
- `pepper` is a 31-byte random value
- `0x05` is the Keyless scheme identifier

### 5.5 Ephemeral Key Pair [P2]

**Properties:**

| Property    | Type              | Description              |
| ----------- | ----------------- | ------------------------ |
| private_key | Ed25519PrivateKey | Signing key              |
| public_key  | Ed25519PublicKey  | Verification key         |
| expiry_time | u64               | Unix timestamp of expiry |
| nonce       | string            | Used in OIDC flow        |

**Construction:**

```
EphemeralKeyPair::generate(expiry_secs: u64) -> EphemeralKeyPair
```

**Nonce Derivation:**

```
nonce = Hash(public_key || expiry_time || blinding_factor)
```

### 5.6 Keyless Account Creation Flow [P2]

1. Generate ephemeral key pair with nonce
2. Redirect user to OIDC provider with nonce in request
3. User authenticates with provider
4. Receive JWT from provider (includes nonce claim)
5. Request pepper from Pepper Service
6. Request ZK proof from Prover Service
7. Create KeylessAccount from components

**Construction:**

```
KeylessAccount::from_jwt(
    jwt: string,
    ephemeral_key: EphemeralKeyPair,
    pepper: [u8; 31],
    proof: ZkProof
) -> Result<KeylessAccount, Error>
```

### 5.7 Services [P2]

#### 5.7.1 Pepper Service

Provides privacy-preserving pepper derivation.

**Purpose:** Prevents address linkability across applications.

**SDK Method:**

```
fetch_pepper(jwt: string, ephemeral_public_key: bytes) -> Result<[u8; 31], Error>
```

#### 5.7.2 Prover Service

Generates zero-knowledge proofs.

**Purpose:** Proves identity without revealing JWT contents on-chain.

**SDK Method:**

```
fetch_proof(
    jwt: string,
    ephemeral_key: EphemeralKeyPair,
    pepper: [u8; 31],
    uid_key: string
) -> Result<ZkProof, Error>
```

### 5.8 Keyless Signing [P2]

**Signing Process:**

1. Create signing message (same as single-signer)
2. Sign with ephemeral private key
3. Include ZK proof in authenticator

**KeylessAuthenticator:**

| Field            | Type             |
| ---------------- | ---------------- |
| ephemeral_pubkey | Ed25519PublicKey |
| ephemeral_sig    | Ed25519Signature |
| expiry_time      | u64              |
| proof            | ZkProof          |

### 5.9 Proof Refresh [P2]

ZK proofs have limited validity. When expired:

```
refresh_proof(jwt: string, prover: ProverService) -> Result<ZkProof, Error>
```

### 5.10 Validity Checks [P2]

```
is_valid() -> bool  // Check if ephemeral key and proof are valid
```

Returns false if:

- Ephemeral key has expired
- ZK proof has expired
- JWT has expired

---

## 6. Transaction Simulation

### 6.1 Overview

Transaction simulation executes a transaction without committing, returning expected results.

**Priority: P1 (Preferred)**

### 6.2 Simulation Request [P1]

**Endpoint:** `POST /v1/transactions/simulate`

**SDK Method:**

```
simulate(
    raw_txn: RawTransaction,
    sender_public_key: Option<PublicKey>
) -> Result<SimulationResult, Error>
```

`sender_public_key` is optional for SDKs that support skipping authentication key checks in
simulation.

### 6.3 Multi-Agent / Fee Payer Simulation Inputs [P1]

For multi-agent and fee payer simulation, SDKs MAY accept additional signer public keys to run
authentication key checks before simulation.

**TypeScript-style shape (illustrative):**

```
simulate_multi_agent(
    raw_txn: RawTransaction,
    secondary_signer_addresses: Vec<AccountAddress>,
    sender_public_key: Option<PublicKey>,
    secondary_signers_public_keys: Option<Vec<Option<PublicKey>>>
) -> Result<SimulationResult, Error>

simulate_fee_payer(
    raw_txn: RawTransaction,
    secondary_signer_addresses: Vec<AccountAddress>,
    fee_payer_address: AccountAddress,
    sender_public_key: Option<PublicKey>,
    secondary_signers_public_keys: Option<Vec<Option<PublicKey>>>,
    fee_payer_public_key: Option<PublicKey>
) -> Result<SimulationResult, Error>
```

**Requirements:**

1. If signer public keys (sender / secondary / fee payer) are provided, SDK **MUST** check provided
   signer/address mappings via authentication keys.
2. If signer public keys are omitted, SDK **MAY** skip authentication key checks and still simulate.
3. For multi-agent simulation, SDK **MAY** support partial checks by allowing `undefined`/`None`
   entries in secondary signer key slots.
4. Malformed key mappings (e.g., address count and key-slot count mismatch) **MUST** fail validation
   before simulation request execution.
5. Simulation **MUST NOT** be treated as full transaction authenticator validation.

### 6.4 Simulation Result [P1]

| Field     | Type        | Description                    |
| --------- | ----------- | ------------------------------ |
| success   | bool        | Whether execution succeeded    |
| vm_status | string      | VM status code/message         |
| gas_used  | u64         | Gas consumed                   |
| changes   | Vec<Change> | State changes that would occur |
| events    | Vec<Event>  | Events that would be emitted   |

### 6.5 Use Cases [P1]

1. **Gas Estimation:** Determine gas needed before submission
2. **Error Preview:** Check for errors before submission
3. **Effect Preview:** Show users what will happen
4. **Validation:** Verify transaction is well-formed

---

## 7. Code Generation

### 7.1 Overview

Code generation creates type-safe SDK bindings from Move module ABIs.

**Priority: P2 (Optional)**

### 7.2 ABI Retrieval [P2]

**Endpoint:** `GET /v1/accounts/{address}/module/{module_name}`

Returns module bytecode and ABI including:

- Struct definitions
- Function signatures
- Type parameters

### 7.3 Generated Types [P2]

For each Move struct, generate:

- Type definition with fields
- BCS serialization/deserialization
- Constructor methods

### 7.4 Generated Functions [P2]

For each entry function, generate:

- Type-safe wrapper function
- Argument encoding
- Transaction payload construction

**Example Generated Code:**

```
// For 0x1::coin::transfer<CoinType>(to: address, amount: u64)
fn transfer<CoinType>(
    to: AccountAddress,
    amount: u64
) -> EntryFunction {
    EntryFunction::new(
        module_id("0x1", "coin"),
        "transfer",
        vec![type_tag::<CoinType>()],
        vec![bcs::to_bytes(&to), bcs::to_bytes(&amount)]
    )
}
```

---

## 8. Test Vectors

### 8.1 Multi-Signature

Test vectors in `test-vectors/multi-sig.json`:

```json
{
  "multi_ed25519_vectors": [
    {
      "name": "2_of_3_threshold",
      "public_keys": ["0x...", "0x...", "0x..."],
      "threshold": 2,
      "expected_auth_key": "0x...",
      "message": "0x...",
      "signatures": [
        { "index": 0, "signature": "0x..." },
        { "index": 2, "signature": "0x..." }
      ],
      "expected_combined_signature": "0x..."
    }
  ]
}
```

### 8.2 Fee Payer

```json
{
  "fee_payer_vectors": [
    {
      "name": "basic_fee_payer",
      "raw_txn_bcs": "0x...",
      "sender": "0x...",
      "fee_payer": "0x...",
      "expected_signing_message": "0x..."
    }
  ]
}
```

---

## 9. Security Considerations

### 9.1 Multi-Signature

1. Validate threshold bounds: `1 <= M <= N`
2. Prevent signature replay across messages
3. Verify all signer indices are unique and valid
4. Validate key ordering consistency

### 9.2 Multi-Agent

1. All parties **MUST** sign the same message
2. Secondary signer order **MUST** match addresses
3. Each party **SHOULD** verify transaction details before signing

### 9.3 Fee Payer

1. Fee payer **SHOULD** verify transaction won't drain funds
2. Fee payer **SHOULD** set reasonable gas limits
3. Fee payer signs last to see full transaction
4. Consider rate limiting fee payer usage

### 9.4 Keyless

1. Ephemeral keys **SHOULD** expire quickly (max 24 hours recommended)
2. Pepper values **MUST** never be exposed
3. JWT claims **MUST** be validated before use
4. ZK proofs have limited validity and must be refreshed
5. Use secure channels for pepper/proof services

---

## 10. References

### 10.1 Related Specifications

- [03-cryptography.md](03-cryptography.md) - Underlying cryptographic primitives
- [04-accounts.md](04-accounts.md) - Basic account types
- [05-transactions.md](05-transactions.md) - Transaction structures

### 10.2 Feature Files

- `features/06-advanced/multi-signature.feature` - 24 multi-sig scenarios
- `features/06-advanced/multi-agent.feature` - 22 multi-agent scenarios
- `features/06-advanced/fee-payer.feature` - 23 fee payer scenarios
- `features/06-advanced/keyless.feature` - 28 keyless scenarios
- `features/06-advanced/simulation.feature` - 31 simulation scenarios
- `features/06-advanced/codegen.feature` - 30 codegen scenarios

### 10.3 Test Vectors

- `test-vectors/multi-sig.json`

### 10.4 External References

- [Aptos Keyless Documentation](https://aptos.dev/guides/keyless-accounts)
- [OpenID Connect Specification](https://openid.net/specs/openid-connect-core-1_0.html)
