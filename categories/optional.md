# Optional Features (P2)

These features provide **extended functionality** for comprehensive Aptos SDK implementations. They
serve specific use cases and can be added incrementally based on user needs.

## Criteria for Optional Features

A feature is classified as Optional if:

1. It provides advanced functionality
2. Only some reference SDKs implement it
3. It serves specific or niche use cases
4. It can be added incrementally without affecting core functionality

---

## Cryptography

### Secp256r1 (P-256) ECDSA

- Generate random key pairs
- Create key pair from private key
- Sign and verify messages
- Derive authentication key
- WebAuthn/Passkey compatibility

### BLS12-381

- Generate random key pairs
- Sign messages
- Verify signatures
- Aggregate signatures
- Aggregate public keys
- Proof of possession

### Multi-Key Cryptography

- Combine multiple public keys with weights
- Threshold signature schemes
- Mixed key type support

---

## Account Management

### Multi-Ed25519 Accounts

- Create M-of-N threshold accounts
- Derive authentication key for multi-key
- Collect signatures from multiple signers
- Aggregate signatures with indices

### MultiKey Accounts

- Support mixed key types (Ed25519 + Secp256k1)
- Weighted signature thresholds
- Flexible signer combinations

### Keyless Accounts (OIDC)

- Generate ephemeral key pairs
- Create nonce for OIDC flow
- Derive address from JWT claims
- Integration with pepper service
- Integration with prover service
- ZK proof management

---

## Transaction Building

### Multi-Agent Transactions

- Add secondary signers
- Generate multi-agent signing message
- Collect secondary signatures
- Create multi-agent authenticator

### Fee Payer (Sponsored) Transactions

- Specify fee payer address
- Generate fee payer signing message
- Collect fee payer signature
- Create fee payer authenticator

### Script Transactions

- Execute compiled Move scripts
- Script argument encoding
- Script type arguments

### Multisig Account Transactions

- Execute through on-chain multisig accounts
- Propose transactions
- Approve/reject transactions

---

## API Client

### Indexer GraphQL Client

- Execute GraphQL queries
- Query account tokens (NFTs)
- Query fungible asset balances
- Query transaction history
- Query events
- Pagination support

### Block Queries

- Get block by height
- Get block by version
- Include transactions in block response

### Table Queries

- Get table item by key
- Decode table values

### WebSocket Subscriptions

- Subscribe to transactions
- Subscribe to events
- Real-time updates

---

## Code Generation

### ABI-Based Code Generation

- Parse Move module ABI
- Generate type definitions
- Generate function wrappers
- Type-safe argument encoding

### Contract Bindings

- Strongly-typed contract interfaces
- Compile-time verification
- IDE autocomplete support

---

## Advanced Features

### Batch Operations

- Submit multiple transactions
- Batch resource queries
- Batch view function calls

### Caching

- Cache account resources
- Cache module ABIs
- Invalidation strategies

### Rate Limiting

- Client-side rate limiting
- Respect server rate limits
- Queue management

---

## Platform-Specific Features

### Hardware Wallet Support

- Ledger integration
- Signing via hardware device
- Address derivation

### Mobile SDKs

- iOS-specific optimizations
- Android-specific optimizations
- React Native bindings

### Browser Extensions

- Wallet adapter interface
- Message signing
- Transaction approval flow

---

## Compliance Checklist

An SDK claiming P2 compliance for specific features must:

1. Pass all P0 and P1 requirements
2. Pass relevant `@optional` Gherkin scenarios

Feature-specific compliance:

### Multi-Signature

- [ ] `06-advanced/multi-signature.feature`

### Multi-Agent

- [ ] `06-advanced/multi-agent.feature`

### Fee Payer

- [ ] `06-advanced/fee-payer.feature`

### Keyless

- [ ] `06-advanced/keyless.feature`

### Indexer

- [ ] `05-api-clients/indexer.feature`

### Secp256r1

- [ ] `02-cryptography/secp256r1.feature`

### BLS12-381

- [ ] `02-cryptography/bls12381.feature`

---

## Implementation Notes

### Incremental Adoption

Optional features can be implemented independently. SDKs may choose to implement only the optional
features relevant to their users.

### Feature Flags

Languages supporting conditional compilation (Rust, C++) should use feature flags for optional
features to minimize binary size.

### Documentation

Each optional feature should be clearly documented as optional, with installation/enable
instructions if applicable.
