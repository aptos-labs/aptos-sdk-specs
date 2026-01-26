# Rust SDK Test Status

> **Last Updated:** 2026-01-22  
> **Last Verified:** Not verified (SDK path not available locally)

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
| Required (P0)  | N/A     | 370     | N/A        | ⚠️     |
| Preferred (P1) | N/A     | 183     | N/A        | ⚠️     |
| Optional (P2)  | N/A     | 250     | N/A        | ⚠️     |
| **Total**      | **N/A** | **803** | **N/A**    | ⚠️     |

> **⚠️ Tests Cannot Run**
>
> The SDK depends on a local path `../../../crates/aptos-rust-sdk-v2` which is not available. Update
> `Cargo.toml` to use a published crate or git dependency.

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

> Last run: N/A (tests cannot run)

### Blocked

Tests are blocked due to SDK path dependency issue.

### Expected Results (Once Fixed)

Based on step definitions in `src/steps/`, the following features have implementations:

| Feature            | Step Definitions | Status             |
| ------------------ | ---------------- | ------------------ |
| address            | ✅ Present       | Needs verification |
| serialization      | ✅ Present       | Needs verification |
| type-tags          | ✅ Present       | Needs verification |
| ed25519            | ✅ Present       | Needs verification |
| hashing            | ✅ Present       | Needs verification |
| authentication-key | ✅ Present       | Needs verification |
| entry-function     | ✅ Present       | Needs verification |
| raw-transaction    | ✅ Present       | Needs verification |
| signing            | ✅ Present       | Needs verification |

### Action Required

1. Update `Cargo.toml` with valid SDK dependency
2. Run `cargo test --test specs`
3. Update this file with actual test results
