# Error Handling Specification

## Abstract

This document specifies error handling requirements for Aptos SDKs, including error categories,
error types, error information, and handling patterns. Consistent error handling enables developers
to write robust applications that gracefully handle failures.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Error Categories](#2-error-categories)
3. [Error Types by Domain](#3-error-types-by-domain)
4. [Error Information](#4-error-information)
5. [API Error Responses](#5-api-error-responses)
6. [VM Error Codes](#6-vm-error-codes)
7. [Error Handling Patterns](#7-error-handling-patterns)
8. [Language-Specific Guidelines](#8-language-specific-guidelines)
9. [Test Scenarios](#9-test-scenarios)
10. [References](#10-references)

---

## 1. Introduction

### 1.1 Purpose

Consistent error handling across SDKs enables developers to:

- Programmatically handle specific error cases
- Provide meaningful feedback to users
- Debug issues efficiently
- Write resilient applications

### 1.2 Scope

This specification covers:

- Error categorization
- Required error types for each SDK domain
- Error information requirements
- API error mapping
- VM error code handling

### 1.3 Definitions

| Term           | Definition                                             |
| -------------- | ------------------------------------------------------ |
| Error Category | High-level classification of error source              |
| Error Type     | Specific error within a category                       |
| Error Code     | Numeric or string identifier for programmatic handling |
| VM Error       | Error from Move VM execution                           |
| API Error      | Error returned by REST API                             |

---

## 2. Error Categories

### 2.1 Overview

Errors **MUST** be categorized to enable programmatic handling at different levels of granularity.

**Priority: P0 (Required)**

### 2.2 Category Definitions [P0]

| Category        | Description                            |
| --------------- | -------------------------------------- |
| `Parse`         | Input parsing or validation failed     |
| `Crypto`        | Cryptographic operation failed         |
| `Serialization` | BCS/JSON encoding or decoding failed   |
| `Network`       | Network communication failed           |
| `Api`           | API returned an error response         |
| `Timeout`       | Operation exceeded time limit          |
| `NotFound`      | Requested resource does not exist      |
| `InvalidState`  | Operation invalid in current state     |
| `InvalidInput`  | Input values are invalid               |
| `Unauthorized`  | Authentication or authorization failed |
| `RateLimited`   | Request was rate limited               |
| `Internal`      | Internal SDK error (bug)               |

### 2.3 Category Hierarchy

```
AptosError
├── ParseError
│   ├── InvalidAddress
│   ├── InvalidHex
│   ├── InvalidTypeTag
│   └── ...
├── CryptoError
│   ├── InvalidPrivateKey
│   ├── InvalidSignature
│   └── ...
├── SerializationError
│   ├── BcsError
│   └── JsonError
├── NetworkError
│   ├── ConnectionFailed
│   ├── DnsError
│   └── ...
├── ApiError
│   ├── BadRequest
│   ├── NotFound
│   ├── InternalServerError
│   └── ...
└── ...
```

---

## 3. Error Types by Domain

### 3.1 Core Types Errors [P0]

| Error Type         | Category | Trigger                          |
| ------------------ | -------- | -------------------------------- |
| `InvalidAddress`   | Parse    | Malformed address string         |
| `InvalidHex`       | Parse    | Non-hex characters in hex string |
| `InvalidLength`    | Parse    | Incorrect byte length            |
| `InvalidTypeTag`   | Parse    | Malformed TypeTag string         |
| `InvalidStructTag` | Parse    | Malformed StructTag string       |
| `InvalidModuleId`  | Parse    | Malformed module ID string       |

### 3.2 Cryptography Errors [P0]

| Error Type            | Category | Trigger                       |
| --------------------- | -------- | ----------------------------- |
| `InvalidPrivateKey`   | Crypto   | Malformed private key bytes   |
| `InvalidPublicKey`    | Crypto   | Malformed public key bytes    |
| `InvalidSignature`    | Crypto   | Malformed signature bytes     |
| `VerificationFailed`  | Crypto   | Signature verification failed |
| `KeyGenerationFailed` | Crypto   | Random key generation failed  |

### 3.3 Account Errors [P1]

| Error Type              | Category     | Trigger                        |
| ----------------------- | ------------ | ------------------------------ |
| `InvalidMnemonic`       | Parse        | Bad mnemonic phrase            |
| `InvalidDerivationPath` | Parse        | Malformed BIP-44 path          |
| `KeyDerivationFailed`   | Crypto       | Path derivation error          |
| `UnsupportedScheme`     | InvalidInput | Requested scheme not available |
| `ChecksumMismatch`      | Parse        | Mnemonic checksum invalid      |

### 3.4 Transaction Errors [P0]

| Error Type              | Category      | Trigger                    |
| ----------------------- | ------------- | -------------------------- |
| `MissingSender`         | InvalidInput  | Builder missing sender     |
| `MissingSequenceNumber` | InvalidInput  | Builder missing seq number |
| `MissingPayload`        | InvalidInput  | Builder missing payload    |
| `MissingChainId`        | InvalidInput  | Builder missing chain ID   |
| `SerializationError`    | Serialization | BCS encoding failed        |
| `SigningError`          | Crypto        | Signature creation failed  |
| `InvalidExpiration`     | InvalidInput  | Expiration in past         |

### 3.5 API Client Errors [P0]

| Error Type            | Category      | Trigger                    |
| --------------------- | ------------- | -------------------------- |
| `ConnectionFailed`    | Network       | Cannot connect to endpoint |
| `Timeout`             | Timeout       | Request exceeded timeout   |
| `BadRequest`          | Api           | HTTP 400 response          |
| `NotFound`            | NotFound      | HTTP 404 response          |
| `RateLimited`         | RateLimited   | HTTP 429 response          |
| `InternalServerError` | Api           | HTTP 5xx response          |
| `InvalidResponse`     | Serialization | Cannot parse response      |

### 3.6 Transaction Submission Errors [P0]

| Error Type               | Category | Trigger                       |
| ------------------------ | -------- | ----------------------------- |
| `SequenceNumberMismatch` | Api      | Wrong sequence number         |
| `InsufficientBalance`    | Api      | Not enough funds for gas      |
| `TransactionExpired`     | Api      | Transaction past expiration   |
| `DuplicateTransaction`   | Api      | Transaction already submitted |
| `VmError`                | Api      | Move VM execution error       |

### 3.7 Multi-Signature Errors [P2]

| Error Type               | Category     | Trigger                           |
| ------------------------ | ------------ | --------------------------------- |
| `InvalidThreshold`       | InvalidInput | Threshold > keys or threshold = 0 |
| `InsufficientSignatures` | InvalidInput | Not enough sigs for threshold     |
| `DuplicateSignerIndex`   | InvalidInput | Same index used twice             |
| `InvalidSignerIndex`     | InvalidInput | Index >= num_keys                 |

### 3.8 Keyless Errors [P2]

| Error Type              | Category     | Trigger                   |
| ----------------------- | ------------ | ------------------------- |
| `EphemeralKeyExpired`   | InvalidState | Ephemeral key past expiry |
| `InvalidJwt`            | Parse        | JWT validation failed     |
| `ProofGenerationFailed` | Network      | Prover service error      |
| `PepperServiceError`    | Network      | Pepper service error      |
| `ProofExpired`          | InvalidState | ZK proof no longer valid  |

---

## 4. Error Information

### 4.1 Required Information [P0]

All errors **MUST** include:

| Field    | Type   | Description                |
| -------- | ------ | -------------------------- |
| category | enum   | Error category             |
| message  | string | Human-readable description |

### 4.2 Recommended Information [P1]

Errors **SHOULD** include when applicable:

| Field         | Type   | Description                        |
| ------------- | ------ | ---------------------------------- |
| error_code    | string | Machine-readable error code        |
| cause         | Error  | Underlying error that caused this  |
| context       | Map    | Additional context (address, etc.) |
| documentation | string | Link to documentation              |

### 4.3 Error Message Guidelines [P0]

Error messages **MUST**:

1. Be human-readable
2. Describe what went wrong
3. Not expose sensitive information (keys, tokens)

Error messages **SHOULD**:

1. Suggest how to fix the issue
2. Include relevant values (e.g., expected vs actual)
3. Be consistent in style and format

**Good Examples:**

```
"Invalid address: expected 64 hex characters, got 65"
"Transaction expired: expiration 1699999999 is before current time 1700000000"
"Insufficient balance: account has 100 octas, transaction requires 1000 octas"
```

**Bad Examples:**

```
"Error"
"Something went wrong"
"0x1234abcd"  // No context
```

---

## 5. API Error Responses

### 5.1 REST API Error Format [P0]

The Aptos REST API returns errors in this format:

```json
{
  "message": "Human-readable error description",
  "error_code": "error_code_identifier",
  "vm_error_code": 12345
}
```

### 5.2 HTTP Status Mapping [P0]

| HTTP Status | SDK Error Category  | Description              |
| ----------- | ------------------- | ------------------------ |
| 400         | BadRequest          | Invalid request format   |
| 404         | NotFound            | Resource not found       |
| 409         | Conflict            | Sequence number conflict |
| 413         | PayloadTooLarge     | Request too large        |
| 429         | RateLimited         | Too many requests        |
| 500         | InternalServerError | Server error             |
| 502         | BadGateway          | Gateway error            |
| 503         | ServiceUnavailable  | Service temporarily down |

### 5.3 Common API Error Codes [P0]

| Error Code                   | Description                       |
| ---------------------------- | --------------------------------- |
| `account_not_found`          | Account does not exist            |
| `resource_not_found`         | Resource not found on account     |
| `module_not_found`           | Module not found on account       |
| `table_item_not_found`       | Table item not found              |
| `transaction_not_found`      | Transaction not found             |
| `invalid_transaction_update` | Transaction already finalized     |
| `sequence_number_too_old`    | Sequence number already used      |
| `sequence_number_too_new`    | Sequence number too far in future |
| `transaction_expired`        | Transaction past expiration       |
| `invalid_signature`          | Signature verification failed     |
| `vm_error`                   | Move VM error during execution    |

### 5.4 Parsing API Errors [P0]

SDK implementations **MUST**:

1. Parse the JSON error response
2. Map to appropriate SDK error type
3. Preserve the original error message
4. Preserve error_code if present
5. Preserve vm_error_code if present

---

## 6. VM Error Codes

### 6.1 Overview

When Move VM execution fails, the API returns a `vm_error_code` indicating the failure reason.

### 6.2 Major VM Status Codes [P1]

| Code  | Name                           | Description                   |
| ----- | ------------------------------ | ----------------------------- |
| 1     | UNKNOWN_VALIDATION_STATUS      | Unknown validation error      |
| 2     | INVALID_SIGNATURE              | Bad signature                 |
| 3     | INVALID_AUTH_KEY               | Auth key mismatch             |
| 4     | SEQUENCE_NUMBER_TOO_OLD        | Sequence number already used  |
| 5     | SEQUENCE_NUMBER_TOO_NEW        | Sequence number too far ahead |
| 6     | INSUFFICIENT_BALANCE           | Not enough balance            |
| 7     | TRANSACTION_EXPIRED            | Past expiration time          |
| 8     | SENDING_ACCOUNT_DOES_NOT_EXIST | Sender account missing        |
| 1000+ | (Abort codes)                  | Move abort with specific code |

### 6.3 Abort Codes [P1]

Move functions can abort with custom codes. The code format is:

```
abort_code = (module_category << 16) | reason_code
```

Common framework abort codes:

| Module  | Code    | Meaning                       |
| ------- | ------- | ----------------------------- |
| coin    | 0x10001 | ECOIN_STORE_NOT_PUBLISHED     |
| coin    | 0x10002 | ECOIN_STORE_ALREADY_PUBLISHED |
| coin    | 0x10005 | EINSUFFICIENT_BALANCE         |
| account | 0x80001 | EACCOUNT_ALREADY_EXISTS       |
| account | 0x80002 | EACCOUNT_DOES_NOT_EXIST       |

### 6.4 SDK Handling [P1]

SDKs **SHOULD**:

1. Parse vm_error_code when present
2. Provide human-readable descriptions for common codes
3. Include the raw code for unknown errors
4. Provide utilities to decode abort codes

---

## 7. Error Handling Patterns

### 7.1 Result Types [P0]

Implementations **MUST** use the language's idiomatic error handling:

| Language   | Pattern                             |
| ---------- | ----------------------------------- |
| Rust       | `Result<T, AptosError>`             |
| TypeScript | `Promise<T>` with thrown errors     |
| Go         | `(T, error)` return values          |
| Python     | Raised exceptions                   |
| Java       | Thrown checked/unchecked exceptions |
| Swift      | `throws` functions                  |

### 7.2 Error Wrapping [P1]

When errors are caused by underlying errors, implementations **SHOULD**:

1. Wrap the underlying error
2. Preserve the error chain
3. Provide access to the root cause

**Example (Rust):**

```rust
#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    #[error("Request failed: {0}")]
    Network(#[from] reqwest::Error),

    #[error("Invalid response: {0}")]
    Parse(#[from] serde_json::Error),
}
```

### 7.3 Error Context [P1]

Add context when re-raising errors:

**Example (Go):**

```go
if err != nil {
    return fmt.Errorf("failed to submit transaction %s: %w", txnHash, err)
}
```

### 7.4 Retry on Transient Errors [P1]

Implement retry for transient errors:

```
Retryable:
- Network errors
- Timeout errors
- Rate limited (429)
- Server errors (5xx)

Non-Retryable:
- Parse errors
- Invalid input
- Not found
- Bad request (400)
```

---

## 8. Language-Specific Guidelines

### 8.1 Rust

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AptosError {
    #[error("Invalid address: {0}")]
    InvalidAddress(String),

    #[error("API error: {message}")]
    Api {
        message: String,
        error_code: Option<String>,
        vm_error_code: Option<u64>,
    },

    #[error("Network error: {0}")]
    Network(#[from] reqwest::Error),
}
```

### 8.2 TypeScript

```typescript
export class AptosError extends Error {
  constructor(
    message: string,
    public readonly category: ErrorCategory,
    public readonly errorCode?: string,
    public readonly cause?: Error,
  ) {
    super(message);
    this.name = "AptosError";
  }
}

export class InvalidAddressError extends AptosError {
  constructor(address: string, reason: string) {
    super(`Invalid address '${address}': ${reason}`, ErrorCategory.Parse);
  }
}
```

### 8.3 Go

```go
type AptosError struct {
    Category  ErrorCategory
    Message   string
    ErrorCode string
    Cause     error
}

func (e *AptosError) Error() string {
    return e.Message
}

func (e *AptosError) Unwrap() error {
    return e.Cause
}

var ErrInvalidAddress = errors.New("invalid address")
var ErrNotFound = errors.New("not found")
```

### 8.4 Python

```python
class AptosError(Exception):
    def __init__(self, message: str, category: ErrorCategory,
                 error_code: str = None, cause: Exception = None):
        super().__init__(message)
        self.category = category
        self.error_code = error_code
        self.__cause__ = cause

class InvalidAddressError(AptosError):
    def __init__(self, address: str, reason: str):
        super().__init__(
            f"Invalid address '{address}': {reason}",
            ErrorCategory.PARSE
        )
```

---

## 9. Test Scenarios

### 9.1 Parse Error Scenarios

| Scenario               | Expected Error |
| ---------------------- | -------------- |
| Parse empty address    | InvalidAddress |
| Parse non-hex address  | InvalidHex     |
| Parse too-long address | InvalidLength  |
| Parse invalid TypeTag  | InvalidTypeTag |

### 9.2 API Error Scenarios

| Scenario                   | Expected Error         |
| -------------------------- | ---------------------- |
| Get non-existent account   | NotFound               |
| Submit with wrong seq num  | SequenceNumberMismatch |
| Submit expired transaction | TransactionExpired     |
| Request timeout            | Timeout                |

### 9.3 Error Information Scenarios

| Scenario                 | Verification                |
| ------------------------ | --------------------------- |
| Error has message        | message is non-empty string |
| Error has category       | category is valid enum      |
| API error preserves code | error_code matches response |
| Wrapped error has cause  | cause is accessible         |

---

## 10. References

### 10.1 Related Specifications

- [06-api-clients.md](06-api-clients.md) - API error responses
- [05-transactions.md](05-transactions.md) - Transaction errors

### 10.2 Feature Files

- `features/06-advanced/error-handling.feature` - 28 error handling scenarios

### 10.3 External References

- [Aptos REST API Errors](https://aptos.dev/nodes/aptos-api-spec)
- [Move VM Status Codes](https://github.com/aptos-labs/aptos-core/blob/main/types/src/vm_status.rs)
