# Rust Behavioral Specification Tests

This directory contains the Cucumber-rs implementation of behavioral specification tests for
[`aptos-rust-sdk`](https://github.com/aptos-labs/aptos-rust-sdk).

## Prerequisites

- Rust 1.75+ (stable)
- The SDK is pulled from crates.io with the `full` feature enabled

## Quick Start

```bash
# Run all tests
cargo test --test specs

# Run with verbose output
cargo test --test specs -- -v

# Run only @required tests (P0)
make test-required

# Run specific categories
make test-core-types
make test-cryptography
make test-accounts
```

## Project Structure

```
rust/
├── Cargo.toml          # Package manifest
├── Makefile            # Convenience commands
├── src/
│   ├── lib.rs          # Library root
│   ├── steps/          # Step definitions
│   │   ├── address_steps.rs
│   │   ├── cryptography_steps.rs
│   │   └── account_steps.rs
│   └── support/
│       ├── vectors.rs  # Test vector loading
│       └── world.rs    # Test context/state
└── tests/
    └── specs.rs        # Main test runner
```

## SDK Dependency

The tests depend on [`aptos-sdk`](https://crates.io/crates/aptos-sdk) from crates.io:

```toml
aptos-sdk = { version = "0.3", features = ["full"] }
```

For local development against a local clone:

```toml
aptos-sdk = { path = "../../../aptos-rust-sdk/crates/aptos-sdk", features = ["full"] }
```

## Test Results

Current test status:

| Category     | Passed | Skipped | Failed |
| ------------ | ------ | ------- | ------ |
| Core Types   | ✅     | -       | 2      |
| Cryptography | ✅     | Many    | 0      |
| Accounts     | ✅     | Many    | 0      |
| Advanced     | -      | Many    | 0      |

### Known Behavioral Differences

1. **Empty string parsing**: The SDK treats `""` and `"0x"` as valid inputs that produce the zero
   address. The spec expects these to fail.

## Adding Step Definitions

To implement a new step:

1. Find the step pattern in a `.feature` file
2. Add a corresponding step function in the appropriate `*_steps.rs` file
3. Use the `#[given]`, `#[when]`, or `#[then]` macros

Example:

```rust
use cucumber::{given, when, then};

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

## Test Vectors

Test vectors are loaded from `../test-vectors/*.json`. These provide deterministic input/output
pairs that must match across all SDK implementations.

See `src/support/vectors.rs` for the vector loader implementation.

## CI Integration

Add to your GitHub Actions workflow:

```yaml
- name: Run behavioral specs
  run: |
    cd specifications/tests/rust
    cargo test --test specs
```

## Coverage Goals

| Priority       | Target      | Current     |
| -------------- | ----------- | ----------- |
| Required (P0)  | 100%        | ~90%        |
| Preferred (P1) | 90%+        | In progress |
| Optional (P2)  | Best effort | Planned     |
