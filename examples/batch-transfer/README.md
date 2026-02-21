# Batch Transfer Example

Demonstrates sending **N APT transfers in parallel** using a single funded sender account.

This example showcases:

- Account generation and faucet funding
- Gas price estimation
- **Sequence number pre-fetching** — fetch once, increment locally (avoids N round-trips)
- Building and signing all transactions **locally** before any network calls
- Parallel submission via goroutines / Promise.allSettled
- Retry with exponential backoff on confirmation
- Structured JSON output for cross-SDK comparison

## The Core Pattern: Sequence Number Management

The naive approach to batch transactions fetches the account's sequence number _per transaction_:

```
for each tx:
  fetch seq_num from chain  ← N network round-trips!
  build tx with seq_num
  submit
```

This example uses the efficient approach:

```
fetch seq_num from chain once
for each tx (local, no network):
  build tx with (seq_num + i)
  sign tx
submit all in parallel
```

This reduces N round-trips to 1 and enables true parallel submission.

## Implementations

| Language   | Directory                    | Command           |
| ---------- | ---------------------------- | ----------------- |
| TypeScript | [typescript/](./typescript/) | `bun src/main.ts` |
| Go         | [go/](./go/)                 | `go run main.go`  |

## Expected Output

```
Aptos Batch Transfer Example (TypeScript)
==========================================
Network:      devnet
Transactions: 10

[1/4] Setup
  ✓ Generated sender:  0x3f2a...
  ✓ Generated 10 recipient accounts
  ✓ Funded sender with 1 APT (tx: 0xabc...)
  ✓ Sender balance: 100,000,000 octas

[2/4] Batch Submission (10 transactions)
  ✓ Gas price estimate: 100 octas/gas
  ✓ Starting sequence number: 1
  ✓ Built & signed 10 transactions locally in 45ms
  ✓ Submitted 10/10 in 312ms

[3/4] Tracking Confirmations
  ✓ Confirmed: 10/10

[4/4] Verify & Report
  ✓ Final balance: 99,978,000 octas
  ✓ Total spent (transfers + gas): 22,000 octas

=== Summary ===
{
  "network": "devnet",
  "timestamp": "2026-02-21T12:00:00Z",
  "transactions": {
    "requested": 10,
    "submitted": 10,
    "confirmed": 10,
    "failed": 0
  },
  "performance": {
    "build_and_sign_ms": 45,
    "submit_ms": 312
  },
  "economics": {
    "initial_balance_octas": 100000000,
    "final_balance_octas": 99978000,
    "total_spent_octas": 22000,
    "avg_cost_per_tx_octas": 2200
  }
}
```

## CLI Options

```
--count N       Number of transactions to send (default: 10)
--network NAME  Network: devnet, testnet, or mainnet (default: devnet)
```

## Extending This Example

This is intentionally simple to serve as a starting point. Consider adding:

- **Simulate before submit**: Call the simulation API to get exact gas estimates
- **Retry on sequence number error**: Refetch and rebuild if a tx is rejected for invalid seq num
- **Concurrent senders**: Split N transactions across M sender accounts for higher throughput
- **Token transfers**: Replace APT coin transfers with fungible asset or NFT transfers
- **Wait strategies**: Implement polling vs. long-poll vs. webhook confirmation patterns
