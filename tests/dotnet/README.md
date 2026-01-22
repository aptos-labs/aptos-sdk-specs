# Aptos .NET SDK Behavioral Tests

BDD (Behavior-Driven Development) tests for the official
[Aptos .NET SDK](https://github.com/aptos-labs/aptos-dotnet-sdk) using Reqnroll and NUnit.

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- Make (optional, for convenience commands)

## Quick Start

```bash
# Restore packages and run all tests
make test

# Or using dotnet directly
dotnet restore
dotnet test
```

## Running Tests

### By Priority Level

```bash
# Required tests (P0) - must pass for SDK compliance
make test-required

# Preferred tests (P1) - expected in production SDKs
make test-preferred

# Optional tests (P2) - for comprehensive SDKs
make test-optional
```

### By Category

```bash
make test-core-types      # Address parsing, BCS serialization
make test-cryptography    # Ed25519, Secp256k1, hashing
make test-accounts        # Account generation, mnemonics
make test-transactions    # Transaction building and signing
make test-api-clients     # Fullnode API, faucet
make test-advanced        # Multi-agent, fee payer, simulation
```

### Using dotnet CLI

```bash
# All tests
dotnet test

# Specific tag filter
dotnet test --filter "Category=required"

# Verbose output
dotnet test --logger "console;verbosity=detailed"
```

## Project Structure

```
tests/dotnet/
├── Aptos.Specs.csproj       # Project file
├── Features/                # Symlinks to shared feature files
│   ├── 01-core-types -> ../../features/01-core-types
│   └── ...
├── StepDefinitions/         # Gherkin step implementations
│   ├── AddressSteps.cs
│   ├── CommonSteps.cs
│   └── ...
├── Support/
│   ├── TestWorld.cs         # Scenario context
│   ├── Vectors.cs           # Test vector loading
│   └── Hooks.cs             # Before/After hooks
├── Makefile
├── README.md
└── reqnroll.json            # Reqnroll configuration
```

## Feature Files

Feature files are shared across all SDK implementations and located in `../../features/`. They are
linked into this project via the `.csproj` file.

## Test Vectors

Deterministic test vectors are in `../../test-vectors/`:

- `addresses.json` - Address parsing vectors
- `signatures.json` - Cryptographic signature vectors
- `bcs.json` - BCS serialization vectors
- `mnemonics.json` - BIP-39 derivation vectors
- `type-tags.json` - Type tag parsing vectors
- `transactions.json` - Transaction building vectors

## SDK Reference

- [Aptos .NET SDK GitHub](https://github.com/aptos-labs/aptos-dotnet-sdk)
- [Aptos .NET SDK Docs](https://aptos.dev/en/build/sdks/dotnet-sdk)
- [API Reference](https://aptos-labs.github.io/aptos-dotnet-sdk/)

## Troubleshooting

### Missing Steps

If tests fail with "No matching step definition found", the step needs to be implemented in the
appropriate `StepDefinitions/*.cs` file.

### SDK API Changes

The .NET SDK is currently in beta. If tests fail due to API changes:

1. Check the [SDK changelog](https://github.com/aptos-labs/aptos-dotnet-sdk/releases)
2. Update step definitions to match new API
3. Report issues in the SDK repo if behavior is incorrect

### Package Restore Issues

```bash
# Clear NuGet cache and restore
dotnet nuget locals all --clear
dotnet restore
```
