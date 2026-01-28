# Performance Benchmarks Specification

## Purpose

This specification defines standardized performance benchmarks for Aptos SDKs. These benchmarks
allow developers to:

1. Compare SDK performance across different language implementations
2. Identify performance regressions in SDK updates
3. Choose the best SDK for their specific use case
4. Identify optimization opportunities

## Benchmark Categories

### 1. REST API Read Performance

Measures latency and throughput for common fullnode API operations:

| Metric                     | Description                           |
| -------------------------- | ------------------------------------- |
| `rest_ledger_info_*`       | Get current ledger info               |
| `rest_account_info_*`      | Get account information               |
| `rest_account_resources_*` | Get all account resources             |
| `rest_tx_by_hash_*`        | Get transaction by hash               |
| `rest_balance_*`           | Get account balance via view function |

### 2. GraphQL/Indexer Read Performance

Measures latency and throughput for indexer queries:

| Metric                 | Description                   |
| ---------------------- | ----------------------------- |
| `gql_account_tokens_*` | Query account tokens          |
| `gql_account_txs_*`    | Query account transactions    |
| `gql_fa_balances_*`    | Query fungible asset balances |
| `gql_events_*`         | Query events by account       |

### 3. Transaction Submission Performance

Measures transaction building and submission:

| Metric            | Description                        |
| ----------------- | ---------------------------------- |
| `tx_submit_*`     | Submit transaction without waiting |
| `tx_build_sign_*` | Build and sign transaction locally |

### 4. Transaction Round-Trip Performance

Measures full transaction lifecycle:

| Metric            | Description                        |
| ----------------- | ---------------------------------- |
| `tx_round_trip_*` | Submit and wait for confirmation   |
| `tx_full_flow_*`  | Complete flow including simulation |

### 5. Cryptographic Operations Performance

Measures local cryptographic operations:

| Metric                    | Description                   |
| ------------------------- | ----------------------------- |
| `crypto_ed25519_keygen_*` | Ed25519 key generation        |
| `crypto_ed25519_sign_*`   | Ed25519 signing               |
| `crypto_ed25519_verify_*` | Ed25519 verification          |
| `bcs_serialize_tx_*`      | BCS transaction serialization |
| `crypto_sha3_256_*`       | SHA3-256 hashing              |

## Measurement Methodology

### Statistical Metrics

For each benchmark, we record:

- **avg**: Arithmetic mean of all measurements
- **p95**: 95th percentile (worst 5% excluded)
- **min**: Minimum observed value
- **max**: Maximum observed value
- **ops/rps/tps**: Operations/requests/transactions per second

### Sample Sizes

| Operation Type     | Sample Size | Rationale                 |
| ------------------ | ----------- | ------------------------- |
| Network calls      | 100         | Balance accuracy vs. time |
| Transaction submit | 10          | Cost and rate limiting    |
| Local crypto ops   | 1000+       | Statistical significance  |

### Environment

Benchmarks should document:

- Network: devnet/testnet/mainnet
- Region: Geographic location
- Hardware: CPU, memory, disk
- SDK version
- Runtime version (Node.js, Go, etc.)

## Results Format

### JSON Output

```json
{
  "sdk": "typescript",
  "version": "5.2.0",
  "runtime": "bun 1.1.0",
  "network": "devnet",
  "timestamp": "2026-01-22T10:00:00Z",
  "environment": {
    "region": "us-west-2",
    "cpu": "Apple M2",
    "memory": "16GB"
  },
  "results": {
    "rest_ledger_info_avg_ms": 45.2,
    "rest_ledger_info_p95_ms": 78.5,
    "rest_ledger_info_rps": 22.1,
    ...
  }
}
```

### Markdown Table

| Metric                     | TypeScript | Go  | Rust | Java | Python |
| -------------------------- | ---------- | --- | ---- | ---- | ------ |
| REST: Ledger Info (avg ms) | 45         | 42  | 38   | 48   | 52     |
| REST: Ledger Info (p95 ms) | 78         | 72  | 65   | 85   | 92     |
| ...                        | ...        | ... | ...  | ...  | ...    |

## Running Benchmarks

### Prerequisites

1. Funded devnet account (for transaction tests)
2. Known transaction hash (for lookup tests)
3. Account with tokens (for indexer tests)
4. Stable network connection

### Commands

```bash
# TypeScript
cd tests/typescript
bun run test:performance

# Go
cd tests/go
make test-performance

# Rust
cd tests/rust
cargo test --test performance

# Python
cd tests/python
pytest tests/performance/ -v
```

## Interpreting Results

### Network Latency Considerations

- Results vary by geographic location
- Devnet may have different performance than mainnet
- Compare SDKs on the same machine/network for fairness

### Expected Ranges (Devnet)

| Operation              | Expected Range |
| ---------------------- | -------------- |
| REST API calls         | 30-100ms       |
| GraphQL queries        | 50-200ms       |
| Transaction submit     | 100-300ms      |
| Transaction round-trip | 500-3000ms     |
| Ed25519 signing        | 10-100μs       |
| BCS serialization      | 1-10μs         |

### Red Flags

- REST API > 200ms consistently
- Transaction round-trip > 5s
- Crypto ops > 1ms
- High variance (p95 > 3x avg)
