// Aptos Batch Transfer Example - Go
//
// Demonstrates sending N APT transfers in parallel using:
//   - Single sequence number fetch (not per-transaction)
//   - Local RawTransaction build + sign before any submission
//   - Goroutines + sync.WaitGroup for parallel submit
//   - Exponential backoff retry on confirmation
//
// Usage:
//
//	go run main.go [--count N] [--network devnet|testnet]
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"math"
	"os"
	"sync"
	"time"

	aptos "github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/api"
)

// ─── Constants ───────────────────────────────────────────────────────────────

const (
	transferAmountOctas    = uint64(100)         // 100 octas per transfer
	fundAmountOctas        = uint64(100_000_000) // 1 APT
	maxGasAmount           = uint64(10_000)
	txExpirationOffsetSecs = uint64(600) // 10 minutes from now
)

// ─── Report types ────────────────────────────────────────────────────────────

type report struct {
	Network      string    `json:"network"`
	Timestamp    string    `json:"timestamp"`
	Transactions txStats   `json:"transactions"`
	Performance  perfStats `json:"performance"`
	Economics    econStats `json:"economics"`
}

type txStats struct {
	Requested int `json:"requested"`
	Submitted int `json:"submitted"`
	Confirmed int `json:"confirmed"`
	Failed    int `json:"failed"`
}

type perfStats struct {
	BuildAndSignMs int64 `json:"build_and_sign_ms"`
	SubmitMs       int64 `json:"submit_ms"`
}

type econStats struct {
	InitialBalanceOctas uint64 `json:"initial_balance_octas"`
	FinalBalanceOctas   uint64 `json:"final_balance_octas"`
	TotalSpentOctas     uint64 `json:"total_spent_octas"`
	AvgCostPerTxOctas   uint64 `json:"avg_cost_per_tx_octas"`
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

func networkConfig(name string) aptos.NetworkConfig {
	if name == "testnet" {
		return aptos.TestnetConfig
	}
	return aptos.DevnetConfig
}

// submitWithRetry submits a signed transaction, retrying with exponential
// backoff if the submission fails (e.g. due to transient network errors).
func submitWithRetry(
	client *aptos.Client,
	signedTx *aptos.SignedTransaction,
	maxAttempts int,
	baseDelayMs int,
) (*api.SubmitTransactionResponse, error) {
	var lastErr error
	for attempt := 0; attempt < maxAttempts; attempt++ {
		if attempt > 0 {
			delay := time.Duration(float64(baseDelayMs)*math.Pow(2, float64(attempt-1))) * time.Millisecond
			time.Sleep(delay)
		}
		resp, err := client.SubmitTransaction(signedTx)
		if err == nil {
			return resp, nil
		}
		lastErr = err
	}
	return nil, lastErr
}

// waitWithRetry polls for transaction confirmation, retrying with exponential
// backoff if the wait times out.
func waitWithRetry(
	client *aptos.Client,
	hash string,
	maxAttempts int,
	baseDelayMs int,
) error {
	var lastErr error
	for attempt := 0; attempt < maxAttempts; attempt++ {
		if attempt > 0 {
			delay := time.Duration(float64(baseDelayMs)*math.Pow(2, float64(attempt-1))) * time.Millisecond
			time.Sleep(delay)
		}
		_, err := client.WaitForTransaction(hash)
		if err == nil {
			return nil
		}
		lastErr = err
	}
	return lastErr
}

// ─── Main ─────────────────────────────────────────────────────────────────────

func main() {
	count := flag.Int("count", 10, "Number of transactions to send")
	networkName := flag.String("network", "devnet", "Network: devnet or testnet")
	flag.Parse()

	if *count < 1 {
		fmt.Fprintf(os.Stderr, "Invalid value for --count: %d (must be >= 1)\n", *count)
		os.Exit(1)
	}
	if *networkName == "mainnet" {
		fmt.Fprintln(os.Stderr, "Error: mainnet is not supported by this example because it funds a new account via faucet.")
		fmt.Fprintln(os.Stderr, "To use mainnet, extend this example to accept a pre-funded sender key.")
		os.Exit(1)
	}
	if *networkName != "devnet" && *networkName != "testnet" {
		fmt.Fprintf(os.Stderr, "Error: unknown network %q. Allowed values: devnet, testnet\n", *networkName)
		os.Exit(1)
	}

	client, err := aptos.NewClient(networkConfig(*networkName))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to create client: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("\nAptos Batch Transfer Example (Go)")
	fmt.Println("===================================")
	fmt.Printf("Network:      %s\n", *networkName)
	fmt.Printf("Transactions: %d\n\n", *count)

	// ═════════════════════════════════════════════════════════════════════════
	// Phase 1: Setup
	// ═════════════════════════════════════════════════════════════════════════
	fmt.Println("[1/4] Setup")

	sender, err := aptos.NewEd25519Account()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to generate sender: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("  ✓ Generated sender:  %s\n", sender.Address.String())

	recipients := make([]*aptos.Account, *count)
	for i := range recipients {
		r, err := aptos.NewEd25519Account()
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed to generate recipient %d: %v\n", i, err)
			os.Exit(1)
		}
		recipients[i] = r
	}
	fmt.Printf("  ✓ Generated %d recipient accounts\n", *count)

	if err := client.Fund(sender.Address, fundAmountOctas); err != nil {
		fmt.Fprintf(os.Stderr, "Failed to fund sender: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("  ✓ Funded sender with 1 APT\n")

	initialBalance, err := client.AccountAPTBalance(sender.Address)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to get balance: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("  ✓ Sender balance: %d octas\n\n", initialBalance)

	// ═════════════════════════════════════════════════════════════════════════
	// Phase 2: Batch Submission
	// ═════════════════════════════════════════════════════════════════════════
	fmt.Printf("[2/4] Batch Submission (%d transactions)\n", *count)

	// Estimate gas price once for all transactions
	gasInfo, err := client.EstimateGasPrice()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to estimate gas: %v\n", err)
		os.Exit(1)
	}
	gasUnitPrice := gasInfo.GasEstimate
	fmt.Printf("  ✓ Gas price estimate: %d octas/gas\n", gasUnitPrice)

	// Fetch chain ID from ledger info
	ledgerInfo, err := client.Info()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to get ledger info: %v\n", err)
		os.Exit(1)
	}
	chainID := ledgerInfo.ChainId

	// KEY INSIGHT: Fetch the sequence number ONCE, then increment locally.
	// Without this, each transaction build would call the chain for the seq num,
	// causing N round-trips and making parallel submission impossible.
	accountInfo, err := client.Account(sender.Address)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to get account info: %v\n", err)
		os.Exit(1)
	}
	startSeqNum, err := accountInfo.SequenceNumber()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to get sequence number: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("  ✓ Starting sequence number: %d\n", startSeqNum)

	// Build and sign all transactions locally (zero network calls per-transaction)
	t0 := time.Now()
	signedTxns := make([]*aptos.SignedTransaction, *count)
	expiration := uint64(time.Now().Unix()) + txExpirationOffsetSecs

	for i := 0; i < *count; i++ {
		payload, err := aptos.CoinTransferPayload(nil, recipients[i].Address, transferAmountOctas)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed to build payload %d: %v\n", i, err)
			os.Exit(1)
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender.Address,
			SequenceNumber:             startSeqNum + uint64(i),
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               maxGasAmount,
			GasUnitPrice:               gasUnitPrice,
			ExpirationTimestampSeconds: expiration,
			ChainId:                    chainID,
		}

		signedTx, err := rawTx.SignedTransaction(sender)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed to sign tx %d: %v\n", i, err)
			os.Exit(1)
		}
		signedTxns[i] = signedTx
	}
	buildMs := time.Since(t0).Milliseconds()
	fmt.Printf("  ✓ Built & signed %d transactions locally in %dms\n", *count, buildMs)

	// Submit all transactions in parallel using goroutines
	type submitResult struct {
		hash string
		err  error
	}
	submitResults := make([]submitResult, *count)

	t1 := time.Now()
	var wg sync.WaitGroup
	for i := 0; i < *count; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			resp, err := submitWithRetry(client, signedTxns[idx], 3, 500)
			if err != nil {
				submitResults[idx] = submitResult{err: err}
				return
			}
			submitResults[idx] = submitResult{hash: resp.Hash}
		}(i)
	}
	wg.Wait()
	submitMs := time.Since(t1).Milliseconds()

	var pendingHashes []string
	submitFailed := 0
	for _, r := range submitResults {
		if r.err != nil {
			submitFailed++
		} else {
			pendingHashes = append(pendingHashes, r.hash)
		}
	}

	fmt.Printf("  ✓ Submitted %d/%d in %dms\n", len(pendingHashes), *count, submitMs)
	if submitFailed > 0 {
		fmt.Printf("  ⚠ %d submission failure(s)\n", submitFailed)
	}
	fmt.Println()

	// ═════════════════════════════════════════════════════════════════════════
	// Phase 3: Track & Confirm
	// ═════════════════════════════════════════════════════════════════════════
	fmt.Println("[3/4] Tracking Confirmations")

	var mu sync.Mutex
	confirmed := 0
	confirmFailed := 0

	var confirmWg sync.WaitGroup
	for _, hash := range pendingHashes {
		confirmWg.Add(1)
		go func(h string) {
			defer confirmWg.Done()
			err := waitWithRetry(client, h, 3, 2_000)
			mu.Lock()
			defer mu.Unlock()
			if err == nil {
				confirmed++
			} else {
				confirmFailed++
			}
		}(hash)
	}
	confirmWg.Wait()

	fmt.Printf("  ✓ Confirmed: %d/%d\n", confirmed, len(pendingHashes))
	if confirmFailed > 0 {
		fmt.Printf("  ✗ Failed to confirm: %d\n", confirmFailed)
	}
	fmt.Println()

	// ═════════════════════════════════════════════════════════════════════════
	// Phase 4: Verify & Report
	// ═════════════════════════════════════════════════════════════════════════
	fmt.Println("[4/4] Verify & Report")

	finalBalance, err := client.AccountAPTBalance(sender.Address)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to get final balance: %v\n", err)
		os.Exit(1)
	}

	var totalSpent, avgCost uint64
	if finalBalance <= initialBalance {
		totalSpent = initialBalance - finalBalance
	}
	if confirmed > 0 {
		avgCost = totalSpent / uint64(confirmed)
	}

	fmt.Printf("  ✓ Final balance: %d octas\n", finalBalance)
	fmt.Printf("  ✓ Total spent (transfers + gas): %d octas\n", totalSpent)

	summary := report{
		Network:   *networkName,
		Timestamp: time.Now().Format(time.RFC3339),
		Transactions: txStats{
			Requested: *count,
			Submitted: len(pendingHashes),
			Confirmed: confirmed,
			Failed:    submitFailed + confirmFailed,
		},
		Performance: perfStats{
			BuildAndSignMs: buildMs,
			SubmitMs:       submitMs,
		},
		Economics: econStats{
			InitialBalanceOctas: initialBalance,
			FinalBalanceOctas:   finalBalance,
			TotalSpentOctas:     totalSpent,
			AvgCostPerTxOctas:   avgCost,
		},
	}

	jsonBytes, err := json.MarshalIndent(summary, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to marshal summary to JSON: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("\n=== Summary ===\n%s\n", jsonBytes)
}
