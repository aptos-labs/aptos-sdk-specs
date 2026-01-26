//go:build ignore
// +build ignore

package main

import (
	"encoding/json"
	"fmt"
	"runtime"
	"sort"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/crypto"
	"golang.org/x/crypto/sha3"
)

type BenchmarkResult struct {
	Name string  `json:"name"`
	Avg  float64 `json:"avg"`
	P95  float64 `json:"p95"`
	Min  float64 `json:"min"`
	Max  float64 `json:"max"`
	Ops  float64 `json:"ops"`
	Unit string  `json:"unit"`
}

func calculateStats(samples []float64) (avg, p95, min, max float64) {
	if len(samples) == 0 {
		return 0, 0, 0, 0
	}

	sorted := make([]float64, len(samples))
	copy(sorted, samples)
	sort.Float64s(sorted)

	var sum float64
	for _, s := range samples {
		sum += s
	}
	avg = sum / float64(len(samples))

	p95Idx := int(float64(len(sorted)) * 0.95)
	if p95Idx >= len(sorted) {
		p95Idx = len(sorted) - 1
	}
	p95 = sorted[p95Idx]
	min = sorted[0]
	max = sorted[len(sorted)-1]

	return avg, p95, min, max
}

func measureSync(fn func(), iterations int, warmup int) (avg, p95, min, max float64) {
	// Warmup
	for i := 0; i < warmup; i++ {
		fn()
	}

	// Measure
	samples := make([]float64, iterations)
	for i := 0; i < iterations; i++ {
		start := time.Now()
		fn()
		elapsed := float64(time.Since(start).Nanoseconds()) / 1000.0 // microseconds
		samples[i] = elapsed
	}

	return calculateStats(samples)
}

func measureAsync(fn func() error, iterations int, warmup int) (avg, p95, min, max float64, err error) {
	// Warmup
	for i := 0; i < warmup; i++ {
		if err := fn(); err != nil {
			return 0, 0, 0, 0, err
		}
	}

	// Measure
	samples := make([]float64, iterations)
	for i := 0; i < iterations; i++ {
		start := time.Now()
		if err := fn(); err != nil {
			return 0, 0, 0, 0, err
		}
		elapsed := float64(time.Since(start).Milliseconds()) // milliseconds
		samples[i] = elapsed
	}

	avg, p95, min, max = calculateStats(samples)
	return avg, p95, min, max, nil
}

func main() {
	fmt.Println("=== Aptos Go SDK Benchmarks ===")
	fmt.Println()
	fmt.Printf("Network: Devnet\n")
	fmt.Printf("Runtime: Go %s\n", runtime.Version())
	fmt.Printf("Date: %s\n\n", time.Now().Format(time.RFC3339))

	results := []BenchmarkResult{}

	// Initialize client
	client, err := aptos.NewClient(aptos.DevnetConfig)
	if err != nil {
		fmt.Printf("Failed to create client: %v\n", err)
		return
	}

	knownAddress := aptos.AccountOne

	// =============================================================================
	// Cryptographic Operations (Local)
	// =============================================================================
	fmt.Println("--- Cryptographic Operations ---")
	fmt.Println()

	// Ed25519 Key Generation
	{
		avg, p95, min, max := measureSync(func() {
			crypto.GenerateEd25519PrivateKey()
		}, 1000, 100)
		ops := 1000000.0 / avg
		results = append(results, BenchmarkResult{Name: "Ed25519 Key Gen", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "μs"})
		fmt.Printf("Ed25519 Key Gen: %.1f μs avg, %.0f ops/s\n", avg, ops)
	}

	// Ed25519 Signing
	{
		pk, _ := crypto.GenerateEd25519PrivateKey()
		message := make([]byte, 256)
		for i := range message {
			message[i] = 0x42
		}
		avg, p95, min, max := measureSync(func() {
			pk.SignMessage(message)
		}, 1000, 100)
		ops := 1000000.0 / avg
		results = append(results, BenchmarkResult{Name: "Ed25519 Sign", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "μs"})
		fmt.Printf("Ed25519 Sign: %.1f μs avg, %.0f ops/s\n", avg, ops)
	}

	// Ed25519 Verification
	{
		pk, _ := crypto.GenerateEd25519PrivateKey()
		pubKey := pk.PubKey().(*crypto.Ed25519PublicKey)
		message := make([]byte, 256)
		for i := range message {
			message[i] = 0x42
		}
		sig, _ := pk.SignMessage(message)
		ed25519Sig := sig.(*crypto.Ed25519Signature)
		avg, p95, min, max := measureSync(func() {
			pubKey.Verify(message, ed25519Sig)
		}, 1000, 100)
		ops := 1000000.0 / avg
		results = append(results, BenchmarkResult{Name: "Ed25519 Verify", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "μs"})
		fmt.Printf("Ed25519 Verify: %.1f μs avg, %.0f ops/s\n", avg, ops)
	}

	// SHA3-256 Hashing
	{
		message := make([]byte, 256)
		for i := range message {
			message[i] = 0x42
		}
		avg, p95, min, max := measureSync(func() {
			h := sha3.New256()
			h.Write(message)
			h.Sum(nil)
		}, 5000, 100)
		ops := 1000000.0 / avg
		results = append(results, BenchmarkResult{Name: "SHA3-256", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "μs"})
		fmt.Printf("SHA3-256 Hash: %.2f μs avg, %.0f ops/s\n", avg, ops)
	}

	// =============================================================================
	// REST API Operations (Network)
	// =============================================================================
	fmt.Println()
	fmt.Println("--- REST API Operations ---")
	fmt.Println()

	// Get Ledger Info
	{
		avg, p95, min, max, err := measureAsync(func() error {
			_, err := client.Info()
			return err
		}, 10, 3)
		if err != nil {
			fmt.Printf("Get Ledger Info: ERROR (%v)\n", err)
		} else {
			ops := 1000.0 / avg
			results = append(results, BenchmarkResult{Name: "Get Ledger Info", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "ms"})
			fmt.Printf("Get Ledger Info: %.1f ms avg, %.1f req/s\n", avg, ops)
		}
	}

	// Get Account Info
	{
		avg, p95, min, max, err := measureAsync(func() error {
			_, err := client.Account(knownAddress)
			return err
		}, 10, 3)
		if err != nil {
			fmt.Printf("Get Account Info: ERROR (%v)\n", err)
		} else {
			ops := 1000.0 / avg
			results = append(results, BenchmarkResult{Name: "Get Account Info", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "ms"})
			fmt.Printf("Get Account Info: %.1f ms avg, %.1f req/s\n", avg, ops)
		}
	}

	// Get Account Resources
	{
		avg, p95, min, max, err := measureAsync(func() error {
			_, err := client.AccountResources(knownAddress)
			return err
		}, 10, 3)
		if err != nil {
			fmt.Printf("Get Account Resources: ERROR (%v)\n", err)
		} else {
			ops := 1000.0 / avg
			results = append(results, BenchmarkResult{Name: "Get Account Resources", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "ms"})
			fmt.Printf("Get Account Resources: %.1f ms avg, %.1f req/s\n", avg, ops)
		}
	}

	// Get Account Balance
	{
		avg, p95, min, max, err := measureAsync(func() error {
			_, err := client.AccountAPTBalance(knownAddress)
			return err
		}, 10, 3)
		if err != nil {
			fmt.Printf("Get Account Balance: ERROR (%v)\n", err)
		} else {
			ops := 1000.0 / avg
			results = append(results, BenchmarkResult{Name: "Get Account Balance", Avg: avg, P95: p95, Min: min, Max: max, Ops: ops, Unit: "ms"})
			fmt.Printf("Get Account Balance: %.1f ms avg, %.1f req/s\n", avg, ops)
		}
	}

	// =============================================================================
	// Summary JSON
	// =============================================================================
	fmt.Println()
	fmt.Println("=== Results JSON ===")

	resultsMap := make(map[string]interface{})
	for _, r := range results {
		resultsMap[r.Name] = map[string]interface{}{
			"avg":  r.Avg,
			"p95":  r.P95,
			"ops":  r.Ops,
			"unit": r.Unit,
		}
	}

	output := map[string]interface{}{
		"sdk":       "go",
		"version":   "1.3.0",
		"runtime":   runtime.Version(),
		"network":   "devnet",
		"timestamp": time.Now().Format(time.RFC3339),
		"results":   resultsMap,
	}

	jsonBytes, _ := json.MarshalIndent(output, "", "  ")
	fmt.Println(string(jsonBytes))
}
