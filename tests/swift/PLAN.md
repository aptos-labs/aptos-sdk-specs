# Swift SDK Test Implementation Plan

> **Status:** SDK Replaced — Tests Need Verification  
> **Last Updated:** 2026-02-23  
> **Target SDK:** aptos-labs/aptos-swift-sdk (official)  
> **BDD Framework:** XCTest (CucumberSwift step definitions prepared for future integration)

## SDK Migration (2026-02-23)

### Old SDK (ALCOVE-LAB)
- **Package URL**: `https://github.com/ALCOVE-LAB/aptos-swift-sdk.git`
- **Import**: `import Aptos`, `import BCS`, `import Core`, `import Transactions`, `import Utils`
- **Publisher**: ALCOVE-LAB (community)
- **Swift**: 5.9+, iOS 15+, macOS 12+

### New SDK (aptos-labs)
- **Package URL**: `https://github.com/aptos-labs/aptos-swift-sdk.git`
- **Import**: `import AptosSDK` (single unified module)
- **Publisher**: aptos-labs (official)
- **Swift**: 6.0+, iOS 17+, macOS 14+

### Key API Changes
- `import Aptos/BCS/Core/Transactions/Utils` → `import AptosSDK`
- `Account.Ed25519Account` → `Ed25519Account`
- `Account.SingleKeyAccount` → `SingleKeyAccount`
- `AccountProtocol` → `AptosAccount`
- `Aptos(aptosConfig:)` → `AptosClient(config:)`
- `AptosConfig.Network.*` → `Network.*`
- `AptosConfig.mainnet` → `AptosConfig.mainnet()`
- `network.localnet` → `Network.local`

### New Features in Official SDK
- Secp256r1 (P-256) support for WebAuthn/passkeys
- Keyless authentication (OIDC pepper/prover)
- Fee-payer transaction support
- Multi-agent transaction support
- 15 domain APIs (Account, Transaction, Coin, Faucet, etc.)
- AIP-80 private key format
- Actor-based HTTP client with retry
- Full strict Swift 6 concurrency

## Current Coverage

Tests need verification after SDK migration.

| Category          | Tests   | Status        |
| ----------------- | ------- | ------------- |
| Address           | 32      | 🔄 Migrated  |
| Ed25519           | 18      | 🔄 Migrated  |
| Secp256k1         | 18      | 🔄 Migrated  |
| SingleKey Account | 5       | 🔄 Migrated  |
| Mnemonic/BIP-44   | 9       | 🔄 Migrated  |
| Account           | 17      | 🔄 Migrated  |
| TypeTag           | 32      | 🔄 Migrated  |
| Hashing           | 9       | 🔄 Migrated  |
| AuthenticationKey | 8       | 🔄 Migrated  |
| BCS Serialization | 23      | 🔄 Migrated  |
| Network Config    | 19      | 🔄 Migrated  |
| AptosConfig       | 6       | 🔄 Migrated  |
| Other             | ~90     | 🔄 Migrated  |

## Project Structure

```
tests/swift/
├── Package.swift                    # SPM manifest
├── Makefile                         # Standard test commands
├── README.md                        # Setup and usage
├── SDK_STATUS.md                    # Coverage tracking
├── PLAN.md                          # This file
├── Sources/
│   └── AptosSpecs/
│       └── AptosSpecs.swift         # Empty (test-only project)
└── Tests/
    └── AptosSpecsTests/
        ├── AptosSpecsTests.swift    # Main test file
        ├── Support/
        │   ├── World.swift          # Test context
        │   ├── Hooks.swift          # Helper functions
        │   └── Vectors.swift        # Test vector loading
        └── CucumberTests/           # Prepared for CucumberSwift
```

## Next Steps

### Phase 1: Verification (Priority)
- [ ] Verify all migrated tests compile with new SDK
- [ ] Fix any compilation errors from API changes
- [ ] Run tests and verify pass rate

### Phase 2: Transaction Building
- [ ] Entry function building
- [ ] Raw transaction construction
- [ ] Transaction signing
- [ ] Signed transaction serialization

### Phase 3: New SDK Features
- [ ] Secp256r1 (P-256) tests
- [ ] Keyless authentication tests
- [ ] Fee-payer transaction tests
- [ ] Multi-agent transaction tests

### Phase 4: API Integration (requires network)
- [ ] Faucet funding (testnet/devnet)
- [ ] Account info queries
- [ ] Transaction submission
- [ ] Transaction status polling

## Running Tests

```bash
cd tests/swift

# Run all tests
swift test

# Run with verbose output
swift test --verbose

# Clean build
swift package clean && swift test
```

## Dependencies

- AptosSDK (official, via SPM from aptos-labs/aptos-swift-sdk)
  - Includes: secp256k1.swift, BigInt, CTweetNaCl (embedded)
- CryptoKit (Apple framework)
