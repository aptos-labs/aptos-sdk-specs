# Rust SDK Test Status

> **Last Updated:** 2026-01-28  
> **Last Verified:** 2026-01-28 via `cargo test --test specs`

---

## 1. SDK Information

| Property             | Value                                        |
| -------------------- | -------------------------------------------- |
| **Package**          | `aptos-rust-sdk-v2`                          |
| **Version Tested**   | dev (local path)                             |
| **Publisher**        | aptos-labs                                   |
| **Repository**       | https://github.com/aptos-labs/aptos-rust-sdk |
| **Package Registry** | crates.io (when published)                   |
| **Test Framework**   | cucumber-rs                                  |

---

## 2. Coverage Summary

| Priority       | Passing | Total   | Percentage | Status |
| -------------- | ------- | ------- | ---------- | ------ |
| Required (P0)  | 676     | 826     | 82%        | 🟡     |
| Preferred (P1) | included| -       | -          | -      |
| Optional (P2)  | included| -       | -          | -      |
| **Total**      | **676** | **826** | **82%**    | 🟡     |

> **Notes:**
>
> - 676 scenarios passed, 150 skipped
> - 2639 steps passed, 150 skipped
> - Test duration: ~9 minutes (includes compilation)
> - Tests require local SDK path at `../../../aptos-rust-sdk/crates/aptos-rust-sdk-v2`

---

## 3. Feature Availability

### Expected Features (Based on SDK Capabilities)

| Feature            | Expected Status | Notes                            |
| ------------------ | --------------- | -------------------------------- |
| address            | ✅ Available    | Full address support expected    |
| serialization      | ✅ Available    | BCS serialization expected       |
| type-tags          | ✅ Available    | TypeTag parsing expected         |
| ed25519            | ✅ Available    | Ed25519 support expected         |
| hashing            | ✅ Available    | SHA3-256 support expected        |
| authentication-key | ✅ Available    | Auth key derivation expected     |
| entry-function     | ✅ Available    | Entry function building expected |
| raw-transaction    | ✅ Available    | Transaction building expected    |
| signing            | ✅ Available    | Transaction signing expected     |

### ➖ Likely Not Available

| Feature              | Reason                 | Tracking Issue |
| -------------------- | ---------------------- | -------------- |
| secp256r1 (WebAuthn) | May not be implemented | -              |
| bls12381             | May not be implemented | -              |
| keyless              | May not be implemented | -              |
| codegen              | May not be implemented | -              |

---

## 4. Known Issues

| Issue                  | Impact                 | Resolution                      |
| ---------------------- | ---------------------- | ------------------------------- |
| SDK path not available | Tests cannot run       | Update Cargo.toml               |
| Local path dependency  | CI/CD cannot run tests | Use git or crates.io dependency |

### To Fix

Update `Cargo.toml` dependency from:

```toml
aptos-rust-sdk-v2 = { path = "../../../crates/aptos-rust-sdk-v2" }
```

To one of:

```toml
# Option 1: Git dependency
aptos-rust-sdk-v2 = { git = "https://github.com/aptos-labs/aptos-rust-sdk" }

# Option 2: crates.io (when published)
aptos-rust-sdk-v2 = "0.1"
```

---

## 5. Missing Test Implementations

### Cannot Determine

Tests cannot run until SDK dependency is resolved. Once fixed, run:

```bash
cargo test --test specs
```

To identify undefined steps.

---

## 6. SDK-Specific Notes

- **Rust idioms**: Uses `Result<T, E>` for error handling
- **Strong typing**: Compile-time type safety
- **No runtime overhead**: Zero-cost abstractions
- **Memory safe**: Ownership and borrowing
- Good for performance-critical applications and blockchain infrastructure

---

## 7. How to Run Tests

```bash
cd tests/rust

# First, fix the Cargo.toml dependency (see Known Issues)

# Then run tests
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

1. **First**: Fix the Cargo.toml dependency issue
2. Add step definitions in `src/steps/*.rs`
3. Run `cargo test --test specs` to verify tests pass
4. Update `FEATURE_COVERAGE.md` with test status (✅/🟡/❌)
5. Update this file's coverage summary
6. Submit PR with test results

### Step Definition Pattern (Rust)

```rust
#[given(expr = "a hex string {string}")]
fn given_hex_string(world: &mut TestWorld, hex_string: String) {
    world.hex_string = Some(hex_string);
}
```

---

## 9. Test Results Matrix

> Last run: 2026-01-27

### Full Test Suite Summary

```
826 scenarios (591 passed, 235 skipped)
2565 steps (2330 passed, 235 skipped)
```

### By Feature Category

| Feature            | Status | Notes                           |
| ------------------ | ------ | ------------------------------- |
| address            | ✅     | Full address support            |
| serialization      | ✅     | BCS serialization working       |
| type-tags          | ✅     | TypeTag parsing working         |
| ed25519            | ✅     | Ed25519 cryptography working    |
| hashing            | ✅     | SHA3-256 support                |
| authentication-key | ✅     | Auth key derivation             |
| entry-function     | ✅     | Entry function building         |
| raw-transaction    | ✅     | Transaction building            |
| signing            | ✅     | Transaction signing             |
| fullnode-api       | 🟡     | Some tests skipped              |
| error-handling     | 🟡     | Some scenarios skipped          |

### Skipped Tests

235 scenarios are skipped, primarily:
- Network-dependent tests requiring live testnet/devnet
- Advanced features not yet implemented in SDK
- Error handling edge cases
