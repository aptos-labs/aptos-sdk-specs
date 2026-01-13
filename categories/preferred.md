# Preferred Features (P1)

These features are **recommended** for production-ready Aptos SDK implementations. While not
strictly required, they significantly improve developer experience and are expected in mature SDKs.

## Criteria for Preferred Features

A feature is classified as Preferred if:

1. It significantly improves developer experience
2. Most reference SDKs implement it
3. Production applications typically need it
4. It follows established blockchain SDK patterns

---

## Cryptography

### Secp256k1 ECDSA

- Generate random key pairs
- Create key pair from 32-byte private key
- Sign messages (recoverable signatures)
- Verify signatures
- Support both compressed and uncompressed public keys
- Derive authentication key

### Key Derivation

- BIP-39 mnemonic generation (12, 15, 18, 21, 24 words)
- BIP-39 mnemonic validation
- BIP-39 seed derivation (with optional passphrase)
- BIP-44 path derivation for Ed25519 (m/44'/637'/0'/0'/n')
- BIP-44 path derivation for Secp256k1

---

## Account Management

### Mnemonic-Based Accounts

- Create account from mnemonic phrase
- Create account from mnemonic with custom derivation path
- Derive multiple accounts from single mnemonic
- Support Ed25519 and Secp256k1 schemes

### Secp256k1 Accounts

- Full account support matching Ed25519 interface
- Proper authentication key derivation
- Transaction signing

---

## Transaction Building

### Transaction Builder

- Fluent/builder pattern for transaction construction
- Sensible defaults for gas parameters
- Automatic expiration timestamp calculation
- Chain ID configuration

### Transaction Options

- Configurable max gas amount
- Configurable gas unit price
- Configurable expiration offset
- Sequence number override

### Transaction Simulation

- Simulate transaction before submission
- Parse simulation results
- Extract gas usage from simulation
- Check for VM errors

---

## API Client

### View Functions

- Execute view functions without transaction
- Pass type arguments
- Pass function arguments (JSON encoded)
- Parse return values

### Gas Estimation

- Get current gas price estimate
- Get prioritized gas estimate
- Get deprioritized gas estimate

### Resource Queries

- Get account modules
- Get specific module by name
- Get events by event handle

### Faucet Integration

- Fund account with test tokens
- Wait for funding transaction
- Support testnet and devnet faucets

---

## Error Handling

### Contextual Errors

- Include request context in errors
- Include response body in API errors
- Chain error causes
- Provide error codes for programmatic handling

### Retry Logic

- Automatic retry for transient failures
- Configurable retry count
- Exponential backoff
- Distinguish retryable vs non-retryable errors

---

## Type Safety

### Move Type Mapping

- Map Move primitives to language types
- Handle u128 and u256 appropriately
- Support vector types
- Support struct types

### Response Parsing

- Strongly-typed API responses
- Proper enum/variant handling
- Optional field handling

---

## Developer Experience

### Configuration

- Pre-configured network settings (mainnet, testnet, devnet)
- Custom network configuration
- Timeout configuration
- Header customization

### Logging/Debugging

- Request/response logging option
- Debug mode for troubleshooting
- Clear error messages

---

## Compliance Checklist

An SDK claiming P1 compliance must:

1. Pass all P0 requirements
2. Pass all Gherkin scenarios tagged with `@preferred` in feature files

Relevant feature files:

- [ ] `02-cryptography/secp256k1.feature`
- [ ] `03-account-management/mnemonic-derivation.feature`
- [ ] `04-transaction-building/builder.feature`
- [ ] `04-transaction-building/simulation.feature`
- [ ] `05-api-clients/view-functions.feature`
- [ ] `05-api-clients/gas-estimation.feature`
- [ ] `05-api-clients/faucet.feature`
