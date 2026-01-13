# Behavioral Specification Tests

This directory contains test implementations that validate SDK behavior against the Gherkin specifications.

## Supported SDKs

| SDK | Framework | Directory | Status |
|-----|-----------|-----------|--------|
| TypeScript | Cucumber.js + Bun | `typescript/` | ✅ Ready |
| Go | Godog | `go/` | ✅ Ready |
| **Rust** | cucumber-rs | `rust/` | ✅ Ready |
| Python | Behave | `python/` | 📋 Planned |
| C# | SpecFlow | `dotnet/` | 📋 Planned |
| Kotlin | Cucumber-JVM | `kotlin/` | 📋 Planned |

## Quick Start

### TypeScript (tests `@aptos-labs/ts-sdk`)

```bash
cd typescript
bun install
bun test                    # Run all tests
bun run test:required       # Run only @required tests
bun run test:core-types     # Run @core-types tests
```

### Go (tests `aptos-go-sdk`)

```bash
cd go
go mod download
make test                   # Run all tests
make test-required          # Run only @required tests
make test-cryptography      # Run @cryptography tests
```

### Rust (tests `aptos-rust-sdk-v2`)

```bash
cd rust
cargo test --test specs     # Run all tests
make test-required          # Run only @required tests
make test-cryptography      # Run @cryptography tests
```

## Test Structure

Each language implementation follows the same pattern:

```
<language>/
├── steps/             # Step definitions (map Gherkin to SDK calls)
│   ├── address.steps.*
│   ├── cryptography.steps.*
│   └── account.steps.*
├── support/           # Test utilities
│   ├── world.*        # Test context/state
│   └── vectors.*      # Test vector loading
└── package.json / go.mod / etc.
```

### How Tests Work

1. **Feature files** (in `../features/`) define expected behaviors in Gherkin
2. **Step definitions** translate Gherkin steps into actual SDK calls
3. **Test vectors** (in `../test-vectors/`) provide deterministic input/output pairs
4. **World/Context** holds state between steps within a scenario

### Example Flow

```gherkin
# From features/01-core-types/address.feature
Scenario: Parse short address
  Given a short address "0x1"
  When I parse the address
  Then I should get a valid AccountAddress
  And the full hex representation should be "0x000...001"
```

This scenario:
1. Calls `Given` step with input `"0x1"`
2. Calls `When` step that invokes `AccountAddress.from("0x1")`
3. Calls `Then` steps that assert the result

## Writing New Step Definitions

### TypeScript Example

```typescript
import { Given, When, Then } from '@cucumber/cucumber';
import { AccountAddress } from '@aptos-labs/ts-sdk';

Given('a short address {string}', function(address: string) {
  this.hexString = address;
});

When('I parse the address', function() {
  this.address = AccountAddress.from(this.hexString);
});

Then('I should get a valid AccountAddress', function() {
  expect(this.address).to.not.be.undefined;
});
```

### Go Example

```go
ctx.Step(`^a short address "([^"]*)"$`, func(address string) error {
    world.HexString = address
    return nil
})

ctx.Step(`^I parse the address$`, func() error {
    addr, err := aptos.ParseAccountAddress(world.HexString)
    world.Address = &addr
    return err
})
```

### Rust Example

```rust
use cucumber::{given, when, then};
use aptos_rust_sdk_v2::types::AccountAddress;

#[given(expr = "a hex string {string}")]
fn given_hex_string(world: &mut TestWorld, hex: String) {
    world.hex_string = Some(hex);
}

#[when("I parse it as an AccountAddress")]
fn when_parse_address(world: &mut TestWorld) {
    if let Some(ref hex) = world.hex_string {
        world.address = AccountAddress::from_hex(hex).ok();
    }
}

#[then("the parsing should succeed")]
fn then_parsing_succeeds(world: &mut TestWorld) {
    assert!(world.address.is_some());
}
```

## Test Tags

Use tags to run specific subsets of tests:

| Tag | Description |
|-----|-------------|
| `@required` | Must-have features (P0) |
| `@preferred` | Recommended features (P1) |
| `@optional` | Nice-to-have features (P2) |
| `@core-types` | Address, TypeTag, serialization |
| `@cryptography` | Keys, signatures, hashing |
| `@accounts` | Account creation, derivation |
| `@transactions` | Transaction building |
| `@api-clients` | REST API, faucet, indexer |
| `@advanced` | Multi-sig, keyless, etc. |
| `@network` | Requires network connectivity |

### Running Tests Without Network

Many API client tests require actual network connectivity to testnet/devnet. To skip these tests when running offline:

```bash
# TypeScript - run only non-network tests
cd typescript
bun run cucumber-js --tags "not @network"

# Run required tests excluding network-dependent ones
bun run cucumber-js --tags "@required and not @network"

# Run api-clients config tests only (no network needed)
bun run cucumber-js --tags "@api-clients and not @network"
```

Network-dependent tests have a 5-second timeout and will fail gracefully when network is unavailable.

## Test Vectors

Load deterministic test cases from `../test-vectors/*.json`:

```typescript
// TypeScript
import { getAddressParsingVectors } from '../support/vectors';
const vectors = getAddressParsingVectors();
for (const v of vectors) {
  const addr = AccountAddress.from(v.input);
  expect(addr.toStringLong()).to.equal(v.expected.full_hex);
}
```

```go
// Go
vectors, _ := GetAddressParsingVectors()
for _, v := range vectors {
    addr, _ := aptos.ParseAccountAddress(v.Input)
    assert.Equal(t, v.Expected.FullHex, addr.StringLong())
}
```

## Coverage Goals

| Priority | Target | Description |
|----------|--------|-------------|
| Required (P0) | 100% | All tests must pass |
| Preferred (P1) | 90%+ | Most tests should pass |
| Optional (P2) | Best effort | Pass as many as possible |

## Adding a New Language

1. Create `<language>/` directory
2. Set up BDD framework (Cucumber, Behave, etc.)
3. Configure to use `../features/*.feature` files
4. Implement step definitions following existing patterns
5. Use `../test-vectors/*.json` for deterministic tests
6. Add to CI pipeline

