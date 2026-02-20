# API Clients Specification

## Overview

The API clients module provides interfaces for interacting with Aptos network services: the fullnode
REST API, the faucet service, and the indexer GraphQL API.

## Goals

1. Full coverage of Aptos REST API
2. Type-safe request/response handling
3. Proper error handling with context
4. Support for all network environments

## Non-Goals

- WebSocket subscriptions (future feature)
- Caching layer (user responsibility)
- Client-side rate limiting (server handles this)

---

## Network Configuration (Required - P0)

### Description

Configuration for connecting to Aptos networks.

### Pre-configured Networks

| Network  | Fullnode URL                              | Faucet URL                           | Indexer URL                                      | Chain ID |
| -------- | ----------------------------------------- | ------------------------------------ | ------------------------------------------------ | -------- |
| Mainnet  | https://fullnode.mainnet.aptoslabs.com/v1 | N/A                                  | https://indexer.mainnet.aptoslabs.com/v1/graphql | 1        |
| Testnet  | https://fullnode.testnet.aptoslabs.com/v1 | https://faucet.testnet.aptoslabs.com | https://indexer.testnet.aptoslabs.com/v1/graphql | 2        |
| Devnet   | https://fullnode.devnet.aptoslabs.com/v1  | https://faucet.devnet.aptoslabs.com  | https://indexer.devnet.aptoslabs.com/v1/graphql  | ~varies  |
| Localnet | http://localhost:8080/v1                  | http://localhost:8081                | N/A                                              | 4        |

### Configuration Methods

| Method                   | Priority | Description             |
| ------------------------ | -------- | ----------------------- |
| `mainnet()`              | P0       | Pre-configured mainnet  |
| `testnet()`              | P0       | Pre-configured testnet  |
| `devnet()`               | P1       | Pre-configured devnet   |
| `localnet()`             | P1       | Pre-configured localnet |
| `custom(url)`            | P0       | Custom fullnode URL     |
| `with_faucet(url)`       | P1       | Add faucet URL          |
| `with_indexer(url)`      | P2       | Add indexer URL         |
| `with_timeout(duration)` | P1       | Set request timeout     |

---

## Fullnode REST API Client (Required - P0)

### Ledger Information

| Endpoint | Method | Priority | Description                               |
| -------- | ------ | -------- | ----------------------------------------- |
| `/v1`    | GET    | P0       | Get ledger info (chain ID, version, etc.) |

### Account Endpoints

| Endpoint                                 | Method | Priority | Description           |
| ---------------------------------------- | ------ | -------- | --------------------- |
| `/v1/accounts/{address}`                 | GET    | P0       | Get account info      |
| `/v1/accounts/{address}/resources`       | GET    | P0       | Get all resources     |
| `/v1/accounts/{address}/resource/{type}` | GET    | P0       | Get specific resource |
| `/v1/accounts/{address}/modules`         | GET    | P1       | Get all modules       |
| `/v1/accounts/{address}/module/{name}`   | GET    | P1       | Get specific module   |

### Module ABI Structure

The module ABI includes struct definitions. Each struct in the ABI has the following fields:

| Field               | Type                         | Description                                       |
| ------------------- | ---------------------------- | ------------------------------------------------- |
| name                | string                       | Name of the struct or enum                        |
| is_native           | bool                         | Whether it is a native (built-in) struct          |
| is_event            | bool                         | Whether it is annotated with `#[event]`           |
| is_enum             | bool                         | Whether it is a Move enum rather than a struct    |
| abilities           | string[]                     | Abilities: `copy`, `drop`, `store`, `key`         |
| generic_type_params | MoveStructGenericTypeParam[] | Generic type parameter constraints                |
| fields              | MoveStructField[]            | Fields (populated for structs, empty for enums)   |
| variants            | MoveStructVariant[]          | Variants (populated for enums, empty for structs) |

Each `MoveStructVariant` has:

| Field  | Type              | Description                     |
| ------ | ----------------- | ------------------------------- |
| name   | string            | Name of the variant             |
| fields | MoveStructField[] | Fields belonging to the variant |

Each `MoveStructField` has:

| Field | Type   | Description            |
| ----- | ------ | ---------------------- |
| name  | string | Name of the field      |
| type  | string | Move type of the field |

For example, given the Move enum:

```move
enum DrawCommand has copy, drop, store {
    Fill { shape: Shape, color: Color },
    Stroke { shape: Shape, color: Color, thickness: u64 },
    Clear,
}
```

The ABI JSON would include:

```json
{
  "name": "DrawCommand",
  "is_native": false,
  "is_event": false,
  "is_enum": true,
  "abilities": ["copy", "drop", "store"],
  "generic_type_params": [],
  "fields": [],
  "variants": [
    {
      "name": "Fill",
      "fields": [
        { "name": "shape", "type": "0x1::enums::Shape" },
        { "name": "color", "type": "0x1::enums::Color" }
      ]
    },
    {
      "name": "Stroke",
      "fields": [
        { "name": "shape", "type": "0x1::enums::Shape" },
        { "name": "color", "type": "0x1::enums::Color" },
        { "name": "thickness", "type": "u64" }
      ]
    },
    { "name": "Clear", "fields": [] }
  ]
}
```

**Note:** `std::option::Option` is a special case. Despite being an enum internally, it is
represented as a struct with a single `vec` field for backwards compatibility (`is_enum` is
`false`).

### Transaction Endpoints

| Endpoint                                | Method | Priority | Description          |
| --------------------------------------- | ------ | -------- | -------------------- |
| `/v1/transactions`                      | POST   | P0       | Submit transaction   |
| `/v1/transactions/by_hash/{hash}`       | GET    | P0       | Get by hash          |
| `/v1/transactions/by_version/{version}` | GET    | P0       | Get by version       |
| `/v1/accounts/{address}/transactions`   | GET    | P1       | Get account txns     |
| `/v1/transactions/simulate`             | POST   | P1       | Simulate transaction |
| `/v1/transactions/encode_submission`    | POST   | P2       | Encode for signing   |

### View Functions

| Endpoint   | Method | Priority | Description           |
| ---------- | ------ | -------- | --------------------- |
| `/v1/view` | POST   | P1       | Execute view function |

### Gas Estimation

| Endpoint                 | Method | Priority | Description            |
| ------------------------ | ------ | -------- | ---------------------- |
| `/v1/estimate_gas_price` | GET    | P1       | Get gas price estimate |

### Block Endpoints

| Endpoint                          | Method | Priority | Description          |
| --------------------------------- | ------ | -------- | -------------------- |
| `/v1/blocks/by_height/{height}`   | GET    | P2       | Get block by height  |
| `/v1/blocks/by_version/{version}` | GET    | P2       | Get block by version |

### Event Endpoints

| Endpoint                                         | Method | Priority | Description |
| ------------------------------------------------ | ------ | -------- | ----------- |
| `/v1/accounts/{address}/events/{handle}/{field}` | GET    | P1       | Get events  |

---

## Response Handling

### Response Wrapper

All API responses should include:

| Field | Type        | Description               |
| ----- | ----------- | ------------------------- |
| data  | T           | Response payload          |
| state | LedgerState | Ledger state from headers |

### LedgerState (from headers)

| Header                        | Field                 | Type |
| ----------------------------- | --------------------- | ---- |
| X-Aptos-Chain-Id              | chain_id              | u8   |
| X-Aptos-Epoch                 | epoch                 | u64  |
| X-Aptos-Ledger-Version        | ledger_version        | u64  |
| X-Aptos-Oldest-Ledger-Version | oldest_ledger_version | u64  |
| X-Aptos-Ledger-TimestampUsec  | ledger_timestamp      | u64  |
| X-Aptos-Block-Height          | block_height          | u64  |
| X-Aptos-Oldest-Block-Height   | oldest_block_height   | u64  |

---

## Transaction Submission

### Request Format

| Header       | Value                                      |
| ------------ | ------------------------------------------ |
| Content-Type | application/x.aptos.signed_transaction+bcs |

Body: BCS-serialized SignedTransaction bytes

### Response

```json
{
  "hash": "0x...",
  "sender": "0x...",
  "sequence_number": "0",
  ...
}
```

### Wait for Transaction

Polling pattern:

1. Submit transaction
2. Get pending transaction hash
3. Poll `/v1/transactions/by_hash/{hash}` until:
   - Transaction appears with `success: true/false`
   - Timeout exceeded
   - Ledger version exceeds expiration

---

## Transaction Simulation

### Request

Same as submission but without signature validity requirement.

### Response

Returns simulated execution result including:

- Gas used
- VM status
- Changes
- Events

---

## View Functions (Preferred - P1)

### Request Format

```json
{
  "function": "0x1::coin::balance",
  "type_arguments": ["0x1::aptos_coin::AptosCoin"],
  "arguments": ["0x1"]
}
```

### Response

```json
["1000000"]
```

Return values are JSON-encoded Move values.

---

## Faucet Client (Preferred - P1)

### Description

Client for requesting test tokens on testnet/devnet.

### Endpoints

| Endpoint | Method | Description  |
| -------- | ------ | ------------ |
| `/mint`  | POST   | Fund account |

### Request

Query parameters:

- `address`: Account address
- `amount`: Amount in octas (optional, default varies)

### Response

Returns transaction hashes for funding transactions.

---

## Indexer GraphQL Client (Optional - P2)

### Description

Client for querying indexed blockchain data.

### Common Queries

| Query               | Description               |
| ------------------- | ------------------------- |
| Account tokens      | Get NFTs owned by account |
| Fungible assets     | Get FA balances           |
| Transaction history | Get account transactions  |
| Events              | Query specific events     |

---

## Error Handling

### Error Categories

| Error         | HTTP Status | Priority |
| ------------- | ----------- | -------- |
| Network       | N/A         | P0       |
| Timeout       | N/A         | P0       |
| NotFound      | 404         | P0       |
| BadRequest    | 400         | P0       |
| InternalError | 500         | P0       |
| RateLimited   | 429         | P1       |

### API Error Response

```json
{
  "message": "Error description",
  "error_code": "error_code_string",
  "vm_error_code": 12345
}
```

### Errors Must Include

1. Error type/category
2. Human-readable message
3. Original response body (when available)
4. HTTP status code (when available)

---

## Retry Strategy (Preferred - P1)

### Retryable Errors

- Network failures
- Timeout
- 429 Rate Limited
- 5xx Server Errors

### Non-Retryable Errors

- 400 Bad Request
- 404 Not Found
- 401/403 Auth Errors

### Configuration

| Setting        | Default | Description                |
| -------------- | ------- | -------------------------- |
| max_retries    | 3       | Maximum retry attempts     |
| initial_delay  | 100ms   | Initial backoff delay      |
| max_delay      | 5s      | Maximum backoff delay      |
| backoff_factor | 2.0     | Exponential backoff factor |

---

## Content Types

### Request Content Types

| Operation            | Content-Type                               |
| -------------------- | ------------------------------------------ |
| Submit Transaction   | application/x.aptos.signed_transaction+bcs |
| Simulate Transaction | application/x.aptos.signed_transaction+bcs |
| View Function        | application/json                           |
| Other POST           | application/json                           |

### Response Content Types

All responses are `application/json`.

---

## Security Considerations

1. **HTTPS Only**: Use HTTPS for all production endpoints
2. **Timeout Protection**: Always set request timeouts
3. **No Credentials in URLs**: Use headers for auth tokens
4. **Rate Limit Respect**: Handle 429 responses appropriately

---

## Cross-SDK Compatibility

All SDKs must:

1. Use the same API endpoints
2. Send the same request format
3. Parse responses consistently
4. Handle errors uniformly

---

## Related Gherkin Feature Files

| File                             | Scenarios | Description                        |
| -------------------------------- | --------- | ---------------------------------- |
| `fullnode-api.feature`           | 24        | Core REST API interactions         |
| `view-functions.feature`         | 28        | View function calls                |
| `transaction-submission.feature` | 30        | Transaction submission and waiting |
| `faucet.feature`                 | 24        | Testnet/devnet funding             |
| `indexer.feature`                | 32        | GraphQL indexer queries            |
| `gas-estimation.feature`         | 26        | Gas price and usage estimation     |
| `retry.feature`                  | 27        | Automatic retry and backoff        |
