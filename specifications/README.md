# Aptos SDK Specifications

## Overview

This directory contains the formal specifications for Aptos SDK implementations. These documents
define the required behaviors, data structures, and interfaces that SDKs must implement to be
considered conformant with the Aptos ecosystem.

## Audience

These specifications are intended for:

- **SDK Implementers**: Developers building new Aptos SDKs in any programming language
- **SDK Maintainers**: Teams maintaining existing SDK implementations
- **Integration Developers**: Engineers integrating Aptos into existing systems

## Specification Documents

| Document                                              | Description                                      |
| ----------------------------------------------------- | ------------------------------------------------ |
| [00-conventions.md](00-conventions.md)                 | Conventions, keywords, and compliance levels     |
| [01-core-types.md](01-core-types.md)                   | AccountAddress, ChainId, TypeTag, StructTag      |
| [02-bcs-serialization.md](02-bcs-serialization.md)     | Binary Canonical Serialization format            |
| [03-cryptography.md](03-cryptography.md)               | Ed25519, Secp256k1, Secp256r1, BLS12-381, hashing|
| [04-accounts.md](04-accounts.md)                       | Account types, authentication, key derivation    |
| [05-transactions.md](05-transactions.md)               | RawTransaction, payloads, signing                |
| [06-api-clients.md](06-api-clients.md)                 | REST API, Faucet, Indexer clients                |
| [07-advanced-features.md](07-advanced-features.md)     | Multi-sig, multi-agent, fee payer, keyless       |
| [08-error-handling.md](08-error-handling.md)           | Error categories, codes, and handling            |

## Compliance Levels

Requirements are tagged with priority levels:

| Level | Tag         | Keyword   | Description                              |
| ----- | ----------- | --------- | ---------------------------------------- |
| P0    | `@required` | **MUST**  | Essential for basic SDK functionality    |
| P1    | `@preferred`| **SHOULD**| Expected in production-quality SDKs      |
| P2    | `@optional` | **MAY**   | Extended features for comprehensive SDKs |

### Compliance Tiers

- **Tier 1 (Basic)**: All P0 requirements - minimum viable SDK
- **Tier 2 (Production)**: All P0 + P1 requirements - production-ready SDK
- **Tier 3 (Full)**: All P0 + P1 + P2 requirements - comprehensive SDK

## Quick Start for SDK Implementers

### 1. Read the Conventions

Start with [00-conventions.md](00-conventions.md) to understand:
- Requirement keywords (MUST, SHOULD, MAY)
- Type notation used in specifications
- Naming conventions across languages
- Error handling requirements

### 2. Implement Core Types (P0)

Begin with [01-core-types.md](01-core-types.md):
- `AccountAddress` - 32-byte account identifier
- `ChainId` - Network identifier
- `TypeTag` - Move type representation

### 3. Implement BCS Serialization (P0)

[02-bcs-serialization.md](02-bcs-serialization.md) defines the binary format used for:
- Transaction encoding
- Argument serialization
- On-chain data structures

### 4. Implement Cryptography (P0)

[03-cryptography.md](03-cryptography.md) covers:
- Ed25519 key generation and signing (P0)
- Secp256k1 ECDSA (P1)
- SHA3-256 and SHA2-256 hashing (P0)

### 5. Implement Accounts (P0)

[04-accounts.md](04-accounts.md) specifies:
- Single-key Ed25519 accounts (P0)
- Authentication key derivation (P0)
- Mnemonic-based accounts (P1)

### 6. Implement Transactions (P0)

[05-transactions.md](05-transactions.md) defines:
- RawTransaction structure
- Entry function payloads
- Transaction signing

### 7. Implement API Clients (P0)

[06-api-clients.md](06-api-clients.md) specifies:
- Fullnode REST API client
- Transaction submission
- Response handling

### 8. Optional: Advanced Features (P2)

[07-advanced-features.md](07-advanced-features.md) covers:
- Multi-signature accounts
- Multi-agent transactions
- Fee payer (sponsored) transactions
- Keyless accounts

## Verifying Compliance

### Test Scenarios

Each specification has corresponding Gherkin test scenarios in the `features/` directory. Run them
to verify compliance:

```bash
# Run all required (P0) tests
make test-required

# Run required + preferred (P0 + P1) tests
make test-preferred

# Run all tests
make test
```

### Test Vectors

Deterministic operations have test vectors in `test-vectors/`:

| File               | Validates                          |
| ------------------ | ---------------------------------- |
| `addresses.json`   | Address parsing and formatting     |
| `bcs.json`         | BCS serialization                  |
| `mnemonics.json`   | BIP-39/BIP-44 key derivation       |
| `signatures.json`  | Cryptographic signatures           |
| `transactions.json`| Transaction serialization          |
| `type-tags.json`   | TypeTag parsing                    |
| `multi-sig.json`   | Multi-signature operations         |

## Relationship to Other Documentation

| Resource                        | Purpose                                |
| ------------------------------- | -------------------------------------- |
| `specifications/` (this folder) | Formal requirements for implementers   |
| `features/*.feature`            | Executable test scenarios (Gherkin)    |
| `features/**/spec.md`           | Design rationale and context           |
| `test-vectors/`                 | Deterministic test data                |
| `categories/`                   | Priority level explanations            |
| `FEATURE_COVERAGE.md`           | Implementation status across SDKs      |

## Reference Implementations

These SDKs serve as reference implementations:

| SDK        | Repository                                                                    | Language   |
| ---------- | ----------------------------------------------------------------------------- | ---------- |
| TypeScript | [aptos-labs/aptos-ts-sdk](https://github.com/aptos-labs/aptos-ts-sdk)         | TypeScript |
| Python     | [aptos-labs/aptos-python-sdk](https://github.com/aptos-labs/aptos-python-sdk) | Python     |
| Go         | [aptos-labs/aptos-go-sdk](https://github.com/aptos-labs/aptos-go-sdk)         | Go         |
| Rust       | [aptos-labs/aptos-rust-sdk](https://github.com/aptos-labs/aptos-rust-sdk)     | Rust       |
| .NET       | [aptos-labs/aptos-dotnet-sdk](https://github.com/aptos-labs/aptos-dotnet-sdk) | C#         |

## Contributing

To propose changes to these specifications:

1. Open an issue describing the proposed change
2. Reference specific sections and requirements affected
3. Provide rationale and impact assessment
4. Submit a pull request with the changes

## Version History

| Version | Date       | Changes                    |
| ------- | ---------- | -------------------------- |
| 1.0.0   | 2026-01-26 | Initial specification set  |
