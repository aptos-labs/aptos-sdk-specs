# Advanced Features Specification

## Overview

Advanced features include multi-signature accounts, multi-agent transactions, fee payer (sponsored) transactions, and keyless accounts. These are optional features that extend SDK capabilities for specific use cases.

## Goals

1. Enable complex account structures
2. Support advanced transaction modes
3. Provide OIDC-based authentication
4. Maintain security for all advanced features

## Non-Goals

- Hardware wallet integration (separate specification)
- Wallet UI components
- On-chain governance modules

---

## Multi-Signature Accounts (Optional - P2)

### Description

Accounts requiring M-of-N signatures to authorize transactions.

### MultiEd25519

#### Key Components

| Component | Description |
|-----------|-------------|
| public_keys | List of N Ed25519 public keys |
| threshold | M signatures required |
| signatures | List of (index, signature) pairs |

#### Authentication Key Derivation

```
auth_key = SHA3-256(pk1 || pk2 || ... || pkN || threshold || 0x01)
```

Where `0x01` is the MultiEd25519 scheme identifier.

#### Requirements

| Method | Priority | Description |
|--------|----------|-------------|
| `from_public_keys(keys, threshold)` | P2 | Create from N public keys |
| `new(private_keys, threshold)` | P2 | Create with M private keys |
| `threshold()` | P2 | Get required signature count |
| `can_sign()` | P2 | Check if enough keys for signing |
| `add_signature(index, sig)` | P2 | Add partial signature |

### MultiKey (Mixed Key Types)

#### Description

Accounts with mixed key types (Ed25519 + Secp256k1) and weights.

#### Authentication Key

```
auth_key = SHA3-256(
  ULEB128(N) || 
  pk1 || pk2 || ... || pkN ||
  threshold ||
  0x03
)
```

---

## Multi-Agent Transactions (Optional - P2)

### Description

Transactions with multiple signers where each signer authorizes their portion.

### Use Cases

- Atomic swaps
- Multi-party agreements
- Shared resource operations

### Signing Message

```
message = SHA3-256("APTOS::RawTransactionWithData") || bcs(MultiAgent {
  raw_txn: RawTransaction,
  secondary_signer_addresses: Vec<AccountAddress>,
})
```

### Requirements

| Method | Priority | Description |
|--------|----------|-------------|
| `sign_multi_agent(raw_txn, sender, secondary_signers)` | P2 | Sign with all parties |
| `add_secondary_signer(address)` | P2 | Add secondary signer |
| `collect_signatures()` | P2 | Collect from all signers |

### TransactionAuthenticator::MultiAgent

| Field | Type |
|-------|------|
| sender | AccountAuthenticator |
| secondary_signer_addresses | Vec<AccountAddress> |
| secondary_signers | Vec<AccountAuthenticator> |

---

## Fee Payer Transactions (Optional - P2)

### Description

Sponsored transactions where a third party pays gas fees.

### Use Cases

- User onboarding (gasless transactions)
- dApp subsidized operations
- Enterprise sponsored activities

### Signing Message

```
message = SHA3-256("APTOS::RawTransactionWithData") || bcs(FeePayer {
  raw_txn: RawTransaction,
  secondary_signer_addresses: Vec<AccountAddress>,
  fee_payer_address: AccountAddress,
})
```

### Requirements

| Method | Priority | Description |
|--------|----------|-------------|
| `sign_fee_payer(raw_txn, sender, secondaries, fee_payer)` | P2 | Sign sponsored tx |
| `set_fee_payer(address)` | P2 | Designate fee payer |
| `sign_as_fee_payer(txn)` | P2 | Sign as the sponsor |

### TransactionAuthenticator::FeePayer

| Field | Type |
|-------|------|
| sender | AccountAuthenticator |
| secondary_signer_addresses | Vec<AccountAddress> |
| secondary_signers | Vec<AccountAuthenticator> |
| fee_payer_address | AccountAddress |
| fee_payer_signer | AccountAuthenticator |

### Fee Payer Flow

1. Sender creates RawTransaction (with any sender for gas fields)
2. Sender signs the fee payer signing message
3. Transaction sent to fee payer
4. Fee payer signs the same message
5. Combined into FeePayer authenticator
6. Transaction submitted

---

## Keyless Accounts (Optional - P2)

### Description

Accounts authenticated via OpenID Connect (OIDC) instead of cryptographic keys.

### Supported Providers

| Provider | Issuer |
|----------|--------|
| Google | https://accounts.google.com |
| Apple | https://appleid.apple.com |

### Components

| Component | Description |
|-----------|-------------|
| EphemeralKeyPair | Short-lived signing key |
| JWT | OIDC identity token |
| Pepper | Privacy-preserving salt |
| ZK Proof | Zero-knowledge proof of identity |

### Authentication Key Derivation

```
auth_key = SHA3-256(
  SHA3-256(iss) ||
  SHA3-256(aud) ||
  SHA3-256(uid) ||
  pepper ||
  0x05
)
```

### Ephemeral Key Pair

| Property | Description |
|----------|-------------|
| expiry | When the key expires |
| nonce | Used in OIDC flow |
| public_key | Ed25519 public key |
| private_key | Ed25519 private key |

### Services

| Service | Purpose |
|---------|---------|
| Pepper Service | Provides privacy-preserving pepper |
| Prover Service | Generates ZK proofs |

### Requirements

| Method | Priority | Description |
|--------|----------|-------------|
| `EphemeralKeyPair::generate(expiry_secs)` | P2 | Generate ephemeral key |
| `KeylessAccount::from_jwt(jwt, ephemeral, pepper, proof)` | P2 | Create from OIDC |
| `refresh_proof(jwt, prover)` | P2 | Refresh ZK proof |
| `is_valid()` | P2 | Check if proof is valid |

### Keyless Flow

1. Generate ephemeral key pair with nonce
2. User authenticates with OIDC provider (nonce in request)
3. Receive JWT from provider
4. Request pepper from Pepper Service
5. Request ZK proof from Prover Service
6. Create KeylessAccount
7. Sign transactions with ephemeral key + proof

---

## Error Handling

### Multi-Signature Errors

| Error | Cause |
|-------|-------|
| InvalidThreshold | threshold > num_keys or threshold == 0 |
| InsufficientSignatures | Not enough signatures for threshold |
| DuplicateSignerIndex | Same signer index used twice |
| InvalidSignerIndex | Index >= num_keys |

### Multi-Agent Errors

| Error | Cause |
|-------|-------|
| MissingSecondarySignature | Not all secondary signers signed |
| WrongSecondarySignerCount | Address/signature count mismatch |

### Fee Payer Errors

| Error | Cause |
|-------|-------|
| MissingFeePayer | Fee payer not specified |
| FeePayerSignatureMissing | Fee payer didn't sign |

### Keyless Errors

| Error | Cause |
|-------|-------|
| EphemeralKeyExpired | Ephemeral key has expired |
| InvalidJwt | JWT validation failed |
| ProofGenerationFailed | ZK proof service error |
| PepperServiceError | Pepper service error |

---

## Security Considerations

### Multi-Signature

1. Validate threshold bounds (1 <= M <= N)
2. Prevent signature replay across different messages
3. Verify all signer indices are unique
4. Validate key ordering is consistent

### Multi-Agent

1. All parties must sign the same message
2. Secondary signer order must match addresses
3. Each party verifies transaction details before signing

### Fee Payer

1. Fee payer should verify transaction won't drain funds
2. Set reasonable gas limits
3. Fee payer signs last to see full transaction

### Keyless

1. Ephemeral keys should expire quickly (max 24 hours)
2. Never expose pepper values
3. Validate JWT claims before use
4. Proofs have limited validity

---

## Cross-SDK Compatibility

All SDKs must produce identical:
1. Multi-sig authentication keys for same key sets
2. Multi-agent signing messages
3. Fee payer signing messages
4. Keyless addresses for same identity

Test vectors for advanced features are in `test-vectors/multi-sig.json`.

---

## Related Gherkin Feature Files

| File | Scenarios | Description |
|------|-----------|-------------|
| `multi-signature.feature` | 24 | Multi-Ed25519 threshold accounts |
| `multi-agent.feature` | 22 | Multi-signer transactions |
| `fee-payer.feature` | 23 | Sponsored/gasless transactions |
| `keyless.feature` | 28 | OIDC-based authentication |
| `codegen.feature` | 30 | Code generation from Move ABI |
| `error-handling.feature` | 28 | Error handling patterns |
| `simulation.feature` | 23 | Transaction simulation |

