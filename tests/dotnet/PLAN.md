# Aptos .NET SDK BDD Test Implementation Plan

This document outlines the plan for implementing BDD (Behavior-Driven Development) tests for the
official Aptos .NET SDK (`aptos-labs/aptos-dotnet-sdk`).

## Overview

- **SDK Under Test**: [aptos-labs/aptos-dotnet-sdk](https://github.com/aptos-labs/aptos-dotnet-sdk)
- **NuGet Package**: `Aptos`
- **BDD Framework**: Reqnroll (successor to SpecFlow)
- **Test Runner**: NUnit
- **Target Framework**: .NET 8.0

## Directory Structure

```
tests/dotnet/
├── Aptos.Specs.csproj           # Project file with dependencies
├── PLAN.md                      # This file
├── README.md                    # Usage instructions
├── Makefile                     # Build and test commands
├── reqnroll.json                # Reqnroll configuration
├── Features/                    # Symlinks to ../../features/ directories
│   ├── 01-core-types -> ../../features/01-core-types
│   ├── 02-cryptography -> ../../features/02-cryptography
│   └── ...
├── StepDefinitions/             # Gherkin step implementations
│   ├── AddressSteps.cs          # Address parsing and formatting
│   ├── SerializationSteps.cs    # BCS serialization
│   ├── CryptoSteps.cs           # Ed25519, Secp256k1 cryptography
│   ├── HashingSteps.cs          # SHA3-256, SHA2-256 hashing
│   ├── AccountSteps.cs          # Account management
│   ├── MnemonicSteps.cs         # BIP-39 mnemonic derivation
│   ├── AuthKeySteps.cs          # Authentication key derivation
│   ├── TransactionSteps.cs      # Transaction building/signing
│   ├── TypeTagSteps.cs          # Type tag parsing
│   ├── CommonSteps.cs           # Shared steps (assertions, etc.)
│   ├── GeneralSteps.cs          # Common result validation
│   ├── ErrorHandlingSteps.cs    # Error handling patterns
│   ├── MultiSigSteps.cs         # Multi-signature accounts
│   ├── FeePayerSteps.cs         # Fee payer transactions
│   ├── SimulationSteps.cs       # Transaction simulation
│   ├── MultiAgentSteps.cs       # Multi-agent transactions
│   ├── ViewFunctionSteps.cs     # View function calls
│   ├── GasEstimationSteps.cs    # Gas price/usage estimation
│   ├── RetrySteps.cs            # Retry with exponential backoff
│   ├── ScriptSteps.cs           # Script transactions
│   ├── Secp256r1Steps.cs        # P-256 (WebAuthn/Passkey)
│   ├── TransactionSubmissionSteps.cs # Transaction submission
│   ├── ClientSteps.cs           # Fullnode API client (mocked)
│   ├── FaucetSteps.cs           # Faucet integration (mocked)
│   ├── IndexerSteps.cs          # GraphQL indexer client
│   ├── KeylessSteps.cs          # Keyless/OIDC (NOT SUPPORTED)
│   └── BLSSteps.cs              # BLS12-381 & codegen (NOT SUPPORTED)
├── Support/
│   ├── TestWorld.cs             # Scenario context/state
│   ├── Vectors.cs               # Test vector loading utilities
│   └── Hooks.cs                 # Before/After scenario hooks
└── .gitignore
```

## Implementation Phases

### Phase 1: Project Setup ✅

- [x] Create directory structure
- [x] Create `.csproj` with dependencies
- [x] Create `TestWorld.cs` context class
- [x] Create `Vectors.cs` for test vector loading
- [x] Create `Hooks.cs` for scenario lifecycle
- [x] Create `Makefile` with build/test commands
- [x] Create `reqnroll.json` configuration
- [x] Create `.gitignore`
- [x] Create `README.md`

### Phase 2: Core Types (@core-types, @required) - Complete

- [x] `AddressSteps.cs` - Address parsing, formatting, comparison
- [x] `SerializationSteps.cs` - BCS serialization/deserialization (simplified)
- [x] `TypeTagSteps.cs` - Type tag parsing and formatting
- [x] `CommonSteps.cs` - Shared assertion steps

### Phase 3: Cryptography (@cryptography, @required) - Complete

- [x] `CryptoSteps.cs` - Ed25519 key generation, signing, verification
- [x] `HashingSteps.cs` - SHA3-256, SHA2-256 hashing
- [x] Secp256k1 support (initial)

### Phase 4: Account Management (@account-management, @required) - Complete

- [x] `AccountSteps.cs` - Account generation, single-key accounts
- [x] `MnemonicSteps.cs` - BIP-39 mnemonic derivation
- [x] `AuthKeySteps.cs` - Authentication key derivation

### Phase 5: Transaction Building (@transaction-building, @required) - In Progress

- [x] `TransactionSteps.cs` - Raw transaction building (initial)
- [x] Entry function payload construction (simplified)
- [x] Transaction signing (simplified)

### Phase 6: API Clients & Advanced Features - Complete

- [x] `GeneralSteps.cs` - Common/shared assertion steps
- [x] `ErrorHandlingSteps.cs` - Error handling patterns
- [x] `MultiSigSteps.cs` - Multi-signature accounts
- [x] `FeePayerSteps.cs` - Fee payer transactions
- [x] `SimulationSteps.cs` - Transaction simulation
- [x] `MultiAgentSteps.cs` - Multi-agent transactions
- [x] `ViewFunctionSteps.cs` - View function calls

**Current Status: 385 tests passing / 808 total (48%)**

### Phase 7: Gas, Retry, Scripts, and Advanced Crypto - Complete

- [x] `GasEstimationSteps.cs` - Gas price and usage estimation
- [x] `RetrySteps.cs` - Automatic retry with exponential backoff
- [x] `ScriptSteps.cs` - Script transaction support
- [x] `Secp256r1Steps.cs` - P-256/NIST curve (WebAuthn/Passkey)
- [x] `TransactionSubmissionSteps.cs` - Transaction submission flows

### Phase 8: API Clients - Complete (Mocked for network isolation)

- [x] `ClientSteps.cs` - Fullnode API client (mocked - no network)
- [x] `FaucetSteps.cs` - Faucet integration (mocked - no network)
- [x] `IndexerSteps.cs` - GraphQL indexer client (mocked - no network)

### Unsupported Features (Throw NotImplementedException)

The following features are **not currently supported** by the Aptos .NET SDK and will throw
`NotImplementedException`:

- **Keyless Accounts (OIDC)** - `KeylessSteps.cs` - Ephemeral keys, JWT/OIDC flow, ZK proofs
- **BLS12-381 Cryptography** - `BLSSteps.cs` - BLS key pairs, signatures, PoP
- **Code Generation** - ABI parsing, Move struct codegen (external tooling)

### Remaining Work

- [ ] Network-dependent integration tests (requires live testnet)
- [ ] Review API client steps for actual SDK integration when available

## Dependencies

```xml
<!-- NuGet Packages -->
<PackageReference Include="Aptos" Version="*" />                    <!-- SDK under test -->
<PackageReference Include="Reqnroll" Version="2.*" />               <!-- BDD framework -->
<PackageReference Include="Reqnroll.NUnit" Version="2.*" />         <!-- NUnit integration -->
<PackageReference Include="NUnit" Version="4.*" />                  <!-- Test runner -->
<PackageReference Include="NUnit3TestAdapter" Version="4.*" />      <!-- VS Test adapter -->
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
```

## Step Definition Pattern

Reqnroll uses attributes to bind steps to methods:

```csharp
using Reqnroll;

[Binding]
public class AddressSteps
{
    private readonly TestWorld _world;

    public AddressSteps(TestWorld world)
    {
        _world = world;
    }

    [Given(@"a hex string ""(.*)""")]
    public void GivenAHexString(string hex)
    {
        _world.HexString = hex;
    }

    [When(@"I parse it as an AccountAddress")]
    public void WhenIParseItAsAnAccountAddress()
    {
        try
        {
            _world.Address = AccountAddress.FromString(_world.HexString);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then(@"the parsing should succeed")]
    public void ThenTheParsingShouldSucceed()
    {
        Assert.That(_world.Error, Is.Null);
        Assert.That(_world.Address, Is.Not.Null);
    }
}
```

## Test Vector Integration

Test vectors are loaded from `../../test-vectors/*.json`:

```csharp
public static class Vectors
{
    public static List<AddressVector> GetAddressParsingVectors()
    {
        var json = File.ReadAllText("../../test-vectors/addresses.json");
        var data = JsonSerializer.Deserialize<AddressVectorFile>(json);
        return data.AddressParsing;
    }
}
```

## Running Tests

```bash
# All tests
make test

# Only required tests
make test-required

# Only specific category
make test-core-types
make test-cryptography

# Build only
make build

# Clean
make clean
```

## SDK API Reference

Key classes from `aptos-labs/aptos-dotnet-sdk`:

- `Aptos.AptosClient` - Main client for blockchain interaction
- `Aptos.AptosConfig` - Client configuration
- `Aptos.AccountAddress` - 32-byte account address
- `Aptos.Account` - Account with signing capability
- `Aptos.Ed25519PrivateKey` / `Ed25519PublicKey` - Ed25519 keys
- `Aptos.Serializer` / `Deserializer` - BCS serialization

## Notes

- The .NET SDK is currently in **beta** - APIs may change
- Some features may not yet be implemented in the SDK
- Mark unimplemented scenarios as `[~]` in `FEATURE_COVERAGE.md`
- Update coverage matrix as steps are implemented

## References

- [Aptos .NET SDK GitHub](https://github.com/aptos-labs/aptos-dotnet-sdk)
- [Aptos .NET SDK Docs](https://aptos.dev/en/build/sdks/dotnet-sdk)
- [Reqnroll Documentation](https://docs.reqnroll.net/)
- [NUnit Documentation](https://docs.nunit.org/)
