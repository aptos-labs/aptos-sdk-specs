# Go SDK Tests - Known Issues and Fixes Needed

This document tracks test failures and issues that need to be addressed.

## Current Status

- **Passed**: 239/370 required scenarios (65%)
- **Failed**: 8 scenarios
  - 4 known local issues (Secp256r1/MultiEd25519/MultiKey keys, coin module)
  - 4 network-dependent scenarios (need client connection in prior steps)
- **Undefined**: 127 scenarios (mostly network-dependent API tests)

Last updated: Fixed serialization tests:
- Added TypeTag struct creation steps
- Added AccountAddress formatting steps (short/long hex)
- Added address constant steps (ZERO, ONE, THREE, FOUR)
- Added address equality comparison steps
- Fixed MoveStructTag creation to preserve type arguments
- Fixed short string format to use StringShort() method

## Failed Tests

### 1. Scheme Identifiers for Secp256r1 (Not Implemented)

**File**: `features/03-account-management/authentication-key.feature:71`

**Error**: `no public key set`

**Issue**: The `a Secp256r1 public key` step is not implemented. Secp256r1 (P-256/prime256v1) keys are not commonly used in the Go SDK.

**Status**: Feature not implemented

**Fix**: Implement Secp256r1 key generation if the Go SDK supports it, or mark as unsupported.

---

### 2. Scheme Identifiers for MultiEd25519 (Not Implemented)

**File**: `features/03-account-management/authentication-key.feature:71`

**Error**: `no public key set`

**Issue**: The `a MultiEd25519 public key` step is not implemented. Multi-signature Ed25519 keys require additional implementation.

**Status**: Feature not implemented

**Fix**: Implement MultiEd25519 key generation using the Go SDK's multi-key support.

---

### 3. Scheme Identifiers for MultiKey (Not Implemented)

**File**: `features/03-account-management/authentication-key.feature:71`

**Error**: `no public key set`

**Issue**: The `a MultiKey public key` step is not implemented.

**Status**: Feature not implemented

**Fix**: Implement MultiKey support using the Go SDK's `crypto.MultiKey` type.

---

### 4. Create Coin Transfer (SDK Behavioral Difference)

**File**: `features/04-transaction-building/entry-function.feature:71`

**Error**: `expected module 0x1::coin, got 0x1::aptos_account`

**Issue**: The Go SDK's `CoinTransferPayload` uses `0x1::aptos_account::transfer` instead of `0x1::coin::transfer`. This is a design decision in the Go SDK.

**Status**: SDK behavioral difference

**Note**: The Go SDK provides a simpler APT-focused API rather than generic coin transfer.

---

## Undefined Features (Major Categories)

### API Client Features (Require Network)
- Client connection and configuration
- Transaction submission
- Account queries
- Gas estimation
- Ledger queries

### Advanced Features
- Multi-signature transactions
- Fee payer transactions  
- Multi-agent transactions
- Keyless authentication

### Other Features
- Transaction builder pattern
- Secp256k1 signing workflows

---

## Notes

- Many undefined scenarios require network access (API client tests)
- Some features may not be supported by the Go SDK
- Consider marking network-dependent tests as `@integration` for separate runs
