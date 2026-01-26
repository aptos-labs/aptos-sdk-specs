# Swift SDK Test Implementation Plan

> **Status:** In Progress - Core + Crypto + Move + Config Complete **Last Updated:** 2026-01-22
> **Target SDK:** ALCOVE-LAB/aptos-swift-sdk **BDD Framework:** XCTest (CucumberSwift has SPM
> compatibility issues)

## Current Coverage

| Category          | Tests   | Status      |
| ----------------- | ------- | ----------- |
| Address           | 32      | ✅ Complete |
| Ed25519           | 18      | ✅ Complete |
| Secp256k1         | 18      | ✅ Complete |
| SingleKey Account | 5       | ✅ Complete |
| Mnemonic/BIP-44   | 9       | ✅ Complete |
| Account           | 17      | ✅ Complete |
| TypeTag           | 32      | ✅ Complete |
| Hashing           | 9       | ✅ Complete |
| AuthenticationKey | 8       | ✅ Complete |
| BCS Serialization | 23      | ✅ Complete |
| Hex Utilities     | 18      | ✅ Complete |
| Identifier        | 6       | ✅ Complete |
| ModuleId          | 6       | ✅ Complete |
| ChainId           | 9       | ✅ Complete |
| Move Primitives   | 12      | ✅ Complete |
| MoveString        | 5       | ✅ Complete |
| MoveVector        | 6       | ✅ Complete |
| MoveOption        | 12      | ✅ Complete |
| Network Config    | 19      | ✅ Complete |
| AptosConfig       | 6       | ✅ Complete |
| Signatures        | 7       | ✅ Complete |
| PublicKeys        | 9       | ✅ Complete |
| API Client        | 3       | ✅ Basic    |
| **Total**         | **286** | **93% P0**  |

## Known Issues

### CucumberSwift SPM Compatibility

CucumberSwift imports XCTest in its main library target, which causes compilation errors with Swift
Package Manager when building for non-test targets. This is a known limitation.

**Workaround:** Use XCTest directly with Gherkin-style naming conventions:

- Test methods follow `test_<FeatureName>_<ScenarioName>` pattern
- Step implementations are regular Swift test methods
- Feature file scenarios are manually translated to test methods

### Xcode Requirement

XCTest requires full Xcode installation, not just Command Line Tools. To run tests:

1. Install Xcode from the App Store
2. Run `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`
3. Then `swift test` will work

### SDK Behaviors

- `AccountAddress.toString()` only shortens "special" addresses (0x0-0xf)
- For non-special addresses, use `toStringLong()` for consistent format
- `Identifier` type uses `.identifier` property (not `.value`)
- Ed25519 BIP-44 path uses hardened derivation: `m/44'/637'/0'/0'/0'`
- Secp256k1 BIP-44 path uses standard derivation: `m/44'/637'/0'/0/0`

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
        ├── AptosSpecsTests.swift    # Main test file (286 tests)
        ├── Support/
        │   ├── World.swift          # Test context
        │   ├── Hooks.swift          # Helper functions
        │   └── Vectors.swift        # Test vector loading
        └── Features/                # (Copied from root)
```

## Completed Phases

### Phase 1: Core Types ✅

- AccountAddress parsing, formatting, BCS
- TypeTag parsing, formatting, BCS
- Hex utilities
- Hashing (SHA2-256, SHA3-256)
- Identifier and ModuleId
- ChainId

### Phase 2: Cryptography ✅

- Ed25519 key generation, signing, verification
- Secp256k1 key generation, signing, verification
- AuthenticationKey derivation
- Signatures and PublicKeys

### Phase 3: Account Management ✅

- Ed25519Account creation and signing
- SingleKeyAccount creation and signing
- Mnemonic/BIP-44 derivation paths

### Phase 4: BCS Serialization ✅

- Primitive types (bool, u8-u128, string)
- Bytes and ULEB128
- AccountAddress
- TypeTag

### Phase 5: Move Types ✅

- Move Primitives (Boolean, U8, U16, U32, U64)
- MoveString
- MoveVector<T>
- MoveOption<T>

### Phase 6: Configuration ✅

- Network configuration (mainnet, testnet, devnet, local, custom)
- AptosConfig presets
- Chain IDs, URLs

## Next Steps

### Phase 7: Transaction Building

- [ ] Entry function building
- [ ] Raw transaction construction
- [ ] Transaction signing
- [ ] Signed transaction serialization

### Phase 8: API Integration (requires network)

- [ ] Faucet funding (testnet/devnet)
- [ ] Account info queries
- [ ] Transaction submission
- [ ] Transaction status polling

### Phase 9: Advanced Features

- [ ] Multi-agent transactions
- [ ] Fee payer transactions
- [ ] View functions
- [ ] Simulate transactions

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

- aptos-swift-sdk (main branch)
- CryptoSwift (for SHA3-256)
- CryptoKit (for SHA2-256)
