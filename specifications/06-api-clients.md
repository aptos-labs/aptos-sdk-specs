# API Clients Specification

## Abstract

This document specifies the client interfaces for interacting with Aptos network services, including
the Fullnode REST API, Faucet service, and Indexer GraphQL API. These clients enable SDKs to query
blockchain state and submit transactions.

## Status

Final

## Version

1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Network Configuration](#2-network-configuration)
3. [Fullnode REST API Client](#3-fullnode-rest-api-client)
4. [Transaction Submission](#4-transaction-submission)
5. [View Functions](#5-view-functions)
6. [Faucet Client](#6-faucet-client)
7. [Indexer GraphQL Client](#7-indexer-graphql-client)
8. [Response Handling](#8-response-handling)
9. [Retry Strategy](#9-retry-strategy)
10. [Test Scenarios](#10-test-scenarios)
11. [Security Considerations](#11-security-considerations)
12. [References](#12-references)

---

## 1. Introduction

### 1.1 Purpose

API clients provide the interface between SDKs and Aptos network services. They handle HTTP
communication, request serialization, response parsing, and error handling.

### 1.2 Scope

This specification covers:

- Network configuration and endpoints
- Fullnode REST API operations
- Transaction submission and waiting
- View function execution
- Faucet interaction (testnet/devnet)
- Indexer GraphQL queries

### 1.3 Definitions

| Term           | Definition                                         |
| -------------- | -------------------------------------------------- |
| Fullnode       | Aptos node serving the REST API                    |
| Faucet         | Service that funds accounts on test networks       |
| Indexer        | Service providing GraphQL queries for indexed data |
| Ledger Version | Monotonically increasing transaction counter       |
| Octa           | Smallest unit of APT (1 APT = 10^8 octas)          |

---

## 2. Network Configuration

### 2.1 Overview

Network configuration specifies the endpoints and parameters for connecting to Aptos networks.

**Priority: P0 (Required)**

### 2.2 Pre-configured Networks [P0]

| Network  | Fullnode URL                              | Faucet URL                           | Chain ID |
| -------- | ----------------------------------------- | ------------------------------------ | -------- |
| Mainnet  | https://fullnode.mainnet.aptoslabs.com/v1 | N/A                                  | 1        |
| Testnet  | https://fullnode.testnet.aptoslabs.com/v1 | https://faucet.testnet.aptoslabs.com | 2        |
| Devnet   | https://fullnode.devnet.aptoslabs.com/v1  | https://faucet.devnet.aptoslabs.com  | varies   |
| Localnet | http://localhost:8080/v1                  | http://localhost:8081                | 4        |

### 2.3 Indexer URLs [P2]

| Network | Indexer URL                                      |
| ------- | ------------------------------------------------ |
| Mainnet | https://indexer.mainnet.aptoslabs.com/v1/graphql |
| Testnet | https://indexer.testnet.aptoslabs.com/v1/graphql |
| Devnet  | https://indexer.devnet.aptoslabs.com/v1/graphql  |

### 2.4 Configuration Methods [P0]

| Method                   | Priority | Description             |
| ------------------------ | -------- | ----------------------- |
| `mainnet()`              | P0       | Pre-configured mainnet  |
| `testnet()`              | P0       | Pre-configured testnet  |
| `devnet()`               | P1       | Pre-configured devnet   |
| `localnet()`             | P1       | Pre-configured localnet |
| `custom(fullnode_url)`   | P0       | Custom fullnode URL     |
| `with_faucet(url)`       | P1       | Add faucet URL          |
| `with_indexer(url)`      | P2       | Add indexer URL         |
| `with_timeout(duration)` | P1       | Set request timeout     |

### 2.5 Default Timeout [P1]

Default request timeout: 30 seconds

Implementations **SHOULD** allow configurable timeouts.

---

## 3. Fullnode REST API Client

### 3.1 Overview

The Fullnode REST API provides access to blockchain state and transaction submission.

**Priority: P0 (Required)**

### 3.2 Ledger Information [P0]

**Endpoint:** `GET /v1`

**Response Fields:**

| Field                 | Type | Description                   |
| --------------------- | ---- | ----------------------------- |
| chain_id              | u8   | Network chain identifier      |
| epoch                 | u64  | Current epoch number          |
| ledger_version        | u64  | Latest committed version      |
| oldest_ledger_version | u64  | Oldest available version      |
| ledger_timestamp      | u64  | Timestamp in microseconds     |
| block_height          | u64  | Current block height          |
| oldest_block_height   | u64  | Oldest available block height |

**SDK Method:**

```
get_ledger_info() -> Result<LedgerInfo, Error>
```

### 3.3 Account Information [P0]

#### 3.3.1 Get Account

**Endpoint:** `GET /v1/accounts/{address}`

**Response Fields:**

| Field              | Type   | Description                |
| ------------------ | ------ | -------------------------- |
| sequence_number    | u64    | Account's sequence number  |
| authentication_key | string | Current authentication key |

**SDK Method:**

```
get_account(address: AccountAddress) -> Result<AccountInfo, Error>
```

#### 3.3.2 Get Account Resources

**Endpoint:** `GET /v1/accounts/{address}/resources`

**SDK Method:**

```
get_account_resources(address: AccountAddress) -> Result<Vec<Resource>, Error>
```

#### 3.3.3 Get Specific Resource

**Endpoint:** `GET /v1/accounts/{address}/resource/{resource_type}`

**SDK Method:**

```
get_account_resource(
    address: AccountAddress,
    resource_type: string
) -> Result<Resource, Error>
```

**Example:**

```
get_account_resource(
    address,
    "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
)
```

### 3.4 Account Modules [P1]

#### 3.4.1 Get All Modules

**Endpoint:** `GET /v1/accounts/{address}/modules`

**SDK Method:**

```
get_account_modules(address: AccountAddress) -> Result<Vec<Module>, Error>
```

#### 3.4.2 Get Specific Module

**Endpoint:** `GET /v1/accounts/{address}/module/{module_name}`

**SDK Method:**

```
get_account_module(
    address: AccountAddress,
    module_name: string
) -> Result<Module, Error>
```

### 3.5 Transaction Queries [P0]

#### 3.5.1 Get Transaction by Hash

**Endpoint:** `GET /v1/transactions/by_hash/{txn_hash}`

**SDK Method:**

```
get_transaction_by_hash(hash: string) -> Result<Transaction, Error>
```

#### 3.5.2 Get Transaction by Version

**Endpoint:** `GET /v1/transactions/by_version/{version}`

**SDK Method:**

```
get_transaction_by_version(version: u64) -> Result<Transaction, Error>
```

### 3.6 Account Transactions [P1]

**Endpoint:** `GET /v1/accounts/{address}/transactions`

**Query Parameters:**

| Parameter | Type | Description                    |
| --------- | ---- | ------------------------------ |
| start     | u64  | Starting sequence number       |
| limit     | u64  | Maximum transactions to return |

**SDK Method:**

```
get_account_transactions(
    address: AccountAddress,
    start: Option<u64>,
    limit: Option<u64>
) -> Result<Vec<Transaction>, Error>
```

### 3.7 Gas Estimation [P1]

**Endpoint:** `GET /v1/estimate_gas_price`

**Response Fields:**

| Field                      | Type | Description              |
| -------------------------- | ---- | ------------------------ |
| gas_estimate               | u64  | Estimated gas price      |
| deprioritized_gas_estimate | u64  | Lower priority estimate  |
| prioritized_gas_estimate   | u64  | Higher priority estimate |

**SDK Method:**

```
estimate_gas_price() -> Result<GasEstimate, Error>
```

### 3.8 Block Queries [P2]

#### 3.8.1 Get Block by Height

**Endpoint:** `GET /v1/blocks/by_height/{height}`

**SDK Method:**

```
get_block_by_height(height: u64, with_transactions: bool) -> Result<Block, Error>
```

#### 3.8.2 Get Block by Version

**Endpoint:** `GET /v1/blocks/by_version/{version}`

**SDK Method:**

```
get_block_by_version(version: u64, with_transactions: bool) -> Result<Block, Error>
```

### 3.9 Event Queries [P1]

**Endpoint:** `GET /v1/accounts/{address}/events/{event_handle}/{field_name}`

**SDK Method:**

```
get_events(
    address: AccountAddress,
    event_handle: string,
    field_name: string,
    start: Option<u64>,
    limit: Option<u64>
) -> Result<Vec<Event>, Error>
```

---

## 4. Transaction Submission

### 4.1 Overview

Transaction submission sends signed transactions to the network for execution.

**Priority: P0 (Required)**

### 4.2 Submit Transaction [P0]

**Endpoint:** `POST /v1/transactions`

**Request:**

| Header       | Value                                      |
| ------------ | ------------------------------------------ |
| Content-Type | application/x.aptos.signed_transaction+bcs |

**Body:** BCS-serialized SignedTransaction bytes

**Response:**

```json
{
  "hash": "0x...",
  "sender": "0x...",
  "sequence_number": "0",
  "max_gas_amount": "10000",
  "gas_unit_price": "100",
  "expiration_timestamp_secs": "1700000000",
  "payload": { ... },
  "signature": { ... }
}
```

**SDK Method:**

```
submit_transaction(signed_txn: SignedTransaction) -> Result<PendingTransaction, Error>
```

### 4.3 Wait for Transaction [P0]

**Polling Pattern:**

1. Submit transaction, receive pending transaction hash
2. Poll `GET /v1/transactions/by_hash/{hash}`
3. Continue until:
   - Transaction appears with `success: true` or `success: false`
   - Timeout exceeded
   - Ledger version exceeds transaction expiration

**SDK Method:**

```
wait_for_transaction(
    hash: string,
    timeout: Option<Duration>
) -> Result<Transaction, Error>
```

**Default Timeout:** 30 seconds

### 4.4 Submit and Wait [P1]

Convenience method combining submission and waiting.

**SDK Method:**

```
submit_and_wait(
    signed_txn: SignedTransaction
) -> Result<Transaction, Error>
```

### 4.5 Transaction Simulation [P1]

**Endpoint:** `POST /v1/transactions/simulate`

**Request:**

| Header       | Value                                      |
| ------------ | ------------------------------------------ |
| Content-Type | application/x.aptos.signed_transaction+bcs |

**Body:** BCS-serialized SignedTransaction (signature validity not checked)

**Response:** Simulated execution result including:

- Gas used
- VM status
- State changes
- Events

**SDK Method:**

```
simulate_transaction(
    raw_txn: RawTransaction,
    public_key: PublicKey
) -> Result<SimulationResult, Error>
```

---

## 5. View Functions

### 5.1 Overview

View functions execute read-only Move functions without transaction submission.

**Priority: P1 (Preferred)**

### 5.2 Execute View Function [P1]

**Endpoint:** `POST /v1/view`

**Request:**

| Header       | Value            |
| ------------ | ---------------- |
| Content-Type | application/json |

**Body:**

```json
{
  "function": "0x1::coin::balance",
  "type_arguments": ["0x1::aptos_coin::AptosCoin"],
  "arguments": ["0x1"]
}
```

**Response:**

```json
["1000000"]
```

Return values are JSON-encoded Move values.

**SDK Method:**

```
view(
    function: string,
    type_arguments: Vec<TypeTag>,
    arguments: Vec<MoveValue>
) -> Result<Vec<MoveValue>, Error>
```

### 5.3 Common View Functions [P1]

#### 5.3.1 Get Balance

**Function:** `0x1::coin::balance` **Type Args:** `[CoinType]` **Args:** `[address]`

**SDK Method:**

```
get_balance(
    address: AccountAddress,
    coin_type: Option<TypeTag>
) -> Result<u64, Error>
```

Default coin type: `0x1::aptos_coin::AptosCoin`

---

## 6. Faucet Client

### 6.1 Overview

The Faucet provides test tokens on testnet and devnet.

**Priority: P1 (Preferred)**

**Note:** Faucet is NOT available on mainnet.

### 6.2 Fund Account [P1]

**Endpoint:** `POST /mint`

**Query Parameters:**

| Parameter | Type   | Required | Description                      |
| --------- | ------ | -------- | -------------------------------- |
| address   | string | Yes      | Account address to fund          |
| amount    | u64    | No       | Amount in octas (default varies) |

**Response:**

Array of transaction hashes for funding transactions.

**SDK Method:**

```
fund_account(
    address: AccountAddress,
    amount: Option<u64>
) -> Result<Vec<string>, Error>
```

### 6.3 Create and Fund Account [P1]

Convenience method to create a new account and fund it.

**SDK Method:**

```
create_and_fund_account(
    amount: Option<u64>
) -> Result<Account, Error>
```

### 6.4 Rate Limiting

Faucet endpoints have rate limits. Implementations **SHOULD**:

1. Handle 429 (Too Many Requests) responses
2. Implement backoff between requests
3. Document rate limit expectations

---

## 7. Indexer GraphQL Client

### 7.1 Overview

The Indexer provides GraphQL access to indexed blockchain data.

**Priority: P2 (Optional)**

### 7.2 GraphQL Queries [P2]

**Endpoint:** `POST /v1/graphql`

**Request:**

| Header       | Value            |
| ------------ | ---------------- |
| Content-Type | application/json |

**Body:**

```json
{
  "query": "...",
  "variables": { ... }
}
```

**SDK Method:**

```
query(
    query: string,
    variables: Option<Map<string, Value>>
) -> Result<Value, Error>
```

### 7.3 Common Queries [P2]

#### 7.3.1 Account Tokens (NFTs)

```graphql
query GetAccountTokens($address: String!) {
  current_token_ownerships(where: { owner_address: { _eq: $address } }) {
    token_data_id
    name
    collection_name
    amount
  }
}
```

#### 7.3.2 Account Transactions

```graphql
query GetAccountTransactions($address: String!, $limit: Int!) {
  account_transactions(
    where: { account_address: { _eq: $address } }
    limit: $limit
    order_by: { transaction_version: desc }
  ) {
    transaction_version
    transaction_hash
  }
}
```

#### 7.3.3 Fungible Asset Balances

```graphql
query GetFungibleAssetBalances($address: String!) {
  current_fungible_asset_balances(where: { owner_address: { _eq: $address } }) {
    asset_type
    amount
  }
}
```

---

## 8. Response Handling

### 8.1 Response Wrapper [P0]

All API responses **SHOULD** be wrapped with ledger state information.

| Field | Type        | Description               |
| ----- | ----------- | ------------------------- |
| data  | T           | Response payload          |
| state | LedgerState | Ledger state from headers |

### 8.2 Ledger State Headers [P0]

| Header                        | Field                 | Type |
| ----------------------------- | --------------------- | ---- |
| X-Aptos-Chain-Id              | chain_id              | u8   |
| X-Aptos-Epoch                 | epoch                 | u64  |
| X-Aptos-Ledger-Version        | ledger_version        | u64  |
| X-Aptos-Oldest-Ledger-Version | oldest_ledger_version | u64  |
| X-Aptos-Ledger-TimestampUsec  | ledger_timestamp      | u64  |
| X-Aptos-Block-Height          | block_height          | u64  |
| X-Aptos-Oldest-Block-Height   | oldest_block_height   | u64  |

### 8.3 Error Response Format [P0]

```json
{
  "message": "Error description",
  "error_code": "error_code_string",
  "vm_error_code": 12345
}
```

### 8.4 Error Categories [P0]

| HTTP Status | Category      | Description            |
| ----------- | ------------- | ---------------------- |
| 400         | BadRequest    | Invalid request format |
| 404         | NotFound      | Resource not found     |
| 429         | RateLimited   | Too many requests      |
| 500         | InternalError | Server error           |
| N/A         | Network       | Connection failed      |
| N/A         | Timeout       | Request timed out      |

---

## 9. Retry Strategy

### 9.1 Overview

Implementations **SHOULD** provide automatic retry for transient failures.

**Priority: P1 (Preferred)**

### 9.2 Retryable Errors [P1]

| Error Type       | Retry |
| ---------------- | ----- |
| Network failure  | Yes   |
| Timeout          | Yes   |
| 429 Rate Limited | Yes   |
| 5xx Server Error | Yes   |
| 400 Bad Request  | No    |
| 404 Not Found    | No    |
| 401/403 Auth     | No    |

### 9.3 Retry Configuration [P1]

| Setting        | Default | Description                    |
| -------------- | ------- | ------------------------------ |
| max_retries    | 3       | Maximum retry attempts         |
| initial_delay  | 100ms   | Initial backoff delay          |
| max_delay      | 5s      | Maximum backoff delay          |
| backoff_factor | 2.0     | Exponential backoff multiplier |

### 9.4 Backoff Algorithm [P1]

```
delay = min(initial_delay * (backoff_factor ^ attempt), max_delay)
```

With optional jitter:

```
delay = delay * random(0.5, 1.5)
```

---

## 10. Test Scenarios

### 10.1 Connection Tests

| Scenario               | Expected Behavior                 |
| ---------------------- | --------------------------------- |
| Connect to mainnet     | Successfully retrieve ledger info |
| Connect to invalid URL | Return connection error           |
| Request with timeout   | Return timeout error after delay  |

### 10.2 Account Tests

| Scenario                 | Expected Behavior    |
| ------------------------ | -------------------- |
| Get existing account     | Return account info  |
| Get non-existent account | Return 404 NotFound  |
| Get account resources    | Return resource list |

### 10.3 Transaction Tests

| Scenario                   | Expected Behavior               |
| -------------------------- | ------------------------------- |
| Submit valid transaction   | Return pending transaction hash |
| Submit invalid transaction | Return error with details       |
| Wait for confirmed txn     | Return committed transaction    |
| Wait with timeout          | Return timeout error            |

---

## 11. Security Considerations

### 11.1 Transport Security

1. Production endpoints **MUST** use HTTPS
2. Implementations **SHOULD** verify TLS certificates
3. Implementations **SHOULD NOT** disable certificate verification

### 11.2 Timeout Protection

1. All requests **MUST** have timeouts
2. Default timeout **SHOULD** be reasonable (30s)
3. Long-running operations **SHOULD** be cancellable

### 11.3 Rate Limiting

1. Implementations **SHOULD** handle 429 responses gracefully
2. Implementations **SHOULD** implement backoff
3. Implementations **SHOULD NOT** retry immediately on rate limit

### 11.4 Error Information

1. Error responses **MUST NOT** expose sensitive information
2. API keys **MUST NOT** appear in error messages
3. Stack traces **SHOULD NOT** be exposed to users

---

## 12. References

### 12.1 Related Specifications

- [05-transactions.md](05-transactions.md) - Transaction structures
- [08-error-handling.md](08-error-handling.md) - Error handling

### 12.2 External References

- [Aptos REST API Specification](https://aptos.dev/nodes/aptos-api-spec)
- [Aptos Indexer Documentation](https://aptos.dev/indexer/indexer-landing)

### 12.3 Feature Files

- `features/05-api-clients/fullnode-api.feature` - 24 fullnode scenarios
- `features/05-api-clients/view-functions.feature` - 28 view scenarios
- `features/05-api-clients/transaction-submission.feature` - 30 submission scenarios
- `features/05-api-clients/faucet.feature` - 24 faucet scenarios
- `features/05-api-clients/indexer.feature` - 32 indexer scenarios
- `features/05-api-clients/gas-estimation.feature` - 26 gas scenarios
- `features/05-api-clients/retry.feature` - 27 retry scenarios
