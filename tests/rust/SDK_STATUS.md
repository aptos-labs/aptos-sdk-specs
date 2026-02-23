# Rust SDK Test Status

> **Last Updated:** 2026-02-23  
> **Last Verified:** 2026-02-23 via `cargo test --test specs`

---

## 1. SDK Information

| Property             | Value                                        |
| -------------------- | -------------------------------------------- |
| **Package**          | `aptos-sdk`                                  |
| **Version Tested**   | 0.3.x (crates.io)                            |
| **Publisher**        | aptos-labs                                   |
| **Repository**       | https://github.com/aptos-labs/aptos-rust-sdk |
| **Package Registry** | https://crates.io/crates/aptos-sdk           |
| **Test Framework**   | cucumber-rs                                  |

---

## 2. Coverage Summary

| Priority       | Passing  | Total   | Percentage | Status |
| -------------- | -------- | ------- | ---------- | ------ |
| Required (P0)  | 723      | 791     | 91%        | ✅     |
| Preferred (P1) | included | -       | -          | -      |
| Optional (P2)  | included | -       | -          | -      |
| **Total**      | **723**  | **791** | **91%**    | ✅     |

> **Notes:**
>
> - 723 scenarios passed, 56 skipped, 12 failed
> - All 12 failures are network-dependent performance benchmarks (require devnet)
> - Test duration: ~28 seconds
> - Tests use `aptos-sdk` v0.3.x from crates.io

---

## 3. Feature Availability

### Expected Features (Based on SDK Capabilities)

| Feature            | Expected Status | Notes                           |
| ------------------ | --------------- | ------------------------------- |
| address            | ✅ Available    | Full address support (AIP-40)   |
| serialization      | ✅ Available    | BCS serialization via aptos-bcs |
| type-tags          | ✅ Available    | TypeTag parsing                 |
| ed25519            | ✅ Available    | Ed25519 signatures              |
| secp256k1          | ✅ Available    | Secp256k1 ECDSA                 |
| secp256r1          | ✅ Available    | Secp256r1 (P-256) ECDSA         |
| hashing            | ✅ Available    | SHA3-256 and SHA2-256           |
| authentication-key | ✅ Available    | Auth key derivation             |
| mnemonic           | ✅ Available    | BIP-39 mnemonic support         |
| entry-function     | ✅ Available    | Entry function building         |
| raw-transaction    | ✅ Available    | Transaction building            |
| signing            | ✅ Available    | Transaction signing             |
| multi-agent        | ✅ Available    | Multi-agent transactions        |
| fee-payer          | ✅ Available    | Sponsored transactions          |
| multi-signature    | ✅ Available    | Multi-Ed25519 and MultiKey      |
| keyless            | ✅ Available    | OIDC-based keyless accounts     |
| codegen            | ✅ Available    | Code generation from Move ABIs  |

### Feature Flags

The SDK uses feature flags. The `full` feature enables all:

| Feature     | Default | Description             |
| ----------- | ------- | ----------------------- |
| `ed25519`   | Yes     | Ed25519 signatures      |
| `secp256k1` | Yes     | Secp256k1 ECDSA         |
| `secp256r1` | Yes     | Secp256r1 (P-256) ECDSA |
| `mnemonic`  | Yes     | BIP-39 mnemonic support |
| `indexer`   | Yes     | GraphQL indexer client  |
| `faucet`    | Yes     | Faucet integration      |
| `keyless`   | No      | OIDC-based keyless auth |
| `full`      | No      | All features combined   |

---

## 4. Known Issues

| Issue | Impact | Resolution |
| ----- | ------ | ---------- |
| None  | -      | -          |

### SDK Dependency

The Cargo.toml uses the SDK from crates.io:

```toml
aptos-sdk = { version = "0.3", features = ["full"] }
```

For local development against a local clone:

```toml
aptos-sdk = { path = "../../../aptos-rust-sdk/crates/aptos-sdk", features = ["full"] }
```

---

## 5. Missing Test Implementations

Run the following to identify undefined steps:

```bash
cargo test --test specs
```

Scenarios that skip (56) are typically due to:

- Network-dependent tests requiring live testnet/devnet
- Advanced features not yet fully tested
- Error handling edge cases

The 12 failed scenarios are all performance benchmarks requiring network access.

---

## 6. SDK-Specific Notes

- **Rust idioms**: Uses `Result<T, E>` for error handling
- **Strong typing**: Compile-time type safety
- **No runtime overhead**: Zero-cost abstractions
- **Memory safe**: Ownership and borrowing
- **Zeroize**: Private keys are zeroized on drop
- **Feature flags**: Selective compilation of crypto schemes
- Good for performance-critical applications and blockchain infrastructure

---

## 7. How to Run Tests

```bash
cd tests/rust

# Run all tests
cargo test --test specs

# Run by priority
make test-required
make test-preferred

# Run by category
cargo test --test specs -- --tags @core-types
cargo test --test specs -- --tags @cryptography
```

---

## 8. Contributing

To add or update tests for this SDK:

1. Add step definitions in `src/steps/*.rs`
2. Run `cargo test --test specs` to verify tests pass
3. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
4. Update this file's coverage summary
5. Submit PR with test results

### Step Definition Pattern (Rust)

```rust
#[given(expr = "a hex string {string}")]
fn given_hex_string(world: &mut TestWorld, hex_string: String) {
    world.hex_string = Some(hex_string);
}
```

---

## 9. Test Results Matrix

> Last run: 2026-02-06

### Full Test Suite Summary

```
791 scenarios (723 passed, 56 skipped, 12 failed)
2897 steps (2827 passed, 56 skipped, 14 failed)
Duration: ~28s
```

### Failed Tests (all network-dependent benchmarks)

All 12 failures are performance benchmark scenarios that require live devnet connectivity:

- Get ledger info, account info, account resources, transaction by hash, account balance
- Query account tokens, transactions, fungible assets, events
- Submit transactions, submit and wait, full transaction flow

### By Feature Category

| Feature            | Status | Notes                        |
| ------------------ | ------ | ---------------------------- |
| address            | ✅     | Full address support         |
| serialization      | ✅     | BCS serialization working    |
| type-tags          | ✅     | TypeTag parsing working      |
| ed25519            | ✅     | Ed25519 cryptography working |
| secp256k1          | ✅     | Secp256k1 ECDSA working      |
| secp256r1          | ✅     | Secp256r1/P-256 working      |
| hashing            | ✅     | SHA3-256 support             |
| authentication-key | ✅     | Auth key derivation          |
| mnemonic           | ✅     | BIP-39 derivation            |
| entry-function     | ✅     | Entry function building      |
| raw-transaction    | ✅     | Transaction building         |
| signing            | ✅     | Transaction signing          |
| fullnode-api       | 🟡     | Some tests skipped           |
| error-handling     | 🟡     | Some scenarios skipped       |

### Skipped Tests

235 scenarios are skipped, primarily:

- Network-dependent tests requiring live testnet/devnet
- Advanced features not yet implemented in SDK
- Error handling edge cases
