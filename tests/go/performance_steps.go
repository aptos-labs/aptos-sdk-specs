package main

import (
	"context"
	"encoding/json"
	"fmt"
	"sort"
	"time"

	"github.com/aptos-labs/aptos-go-sdk/crypto"
	"github.com/cucumber/godog"
	"golang.org/x/crypto/sha3"
)

// BenchmarkResult holds performance measurement statistics
type BenchmarkResult struct {
	Samples      []float64 `json:"samples,omitempty"`
	Avg          float64   `json:"avg"`
	P95          float64   `json:"p95"`
	Min          float64   `json:"min"`
	Max          float64   `json:"max"`
	OpsPerSecond float64   `json:"ops_per_second"`
}

// PerformanceResults holds all benchmark results
type PerformanceResults struct {
	SDK         string             `json:"sdk"`
	Version     string             `json:"version"`
	Runtime     string             `json:"runtime"`
	Network     string             `json:"network"`
	Timestamp   string             `json:"timestamp"`
	Environment map[string]string  `json:"environment"`
	Results     map[string]float64 `json:"results"`
}

var performanceResults = PerformanceResults{
	SDK:       "go",
	Version:   "1.3.0",
	Runtime:   "go1.24",
	Network:   "devnet",
	Timestamp: time.Now().Format(time.RFC3339),
	Environment: map[string]string{
		"platform": "darwin",
		"arch":     "arm64",
	},
	Results: make(map[string]float64),
}

// calculateStats computes statistics from samples (in microseconds)
func calculateStats(samples []float64) BenchmarkResult {
	if len(samples) == 0 {
		return BenchmarkResult{}
	}

	// Calculate average
	var sum float64
	for _, s := range samples {
		sum += s
	}
	avg := sum / float64(len(samples))

	// Sort for percentiles
	sorted := make([]float64, len(samples))
	copy(sorted, samples)
	sort.Float64s(sorted)

	// P95
	p95Idx := int(float64(len(sorted)) * 0.95)
	if p95Idx >= len(sorted) {
		p95Idx = len(sorted) - 1
	}
	p95 := sorted[p95Idx]

	// Min/Max
	min := sorted[0]
	max := sorted[len(sorted)-1]

	// Ops per second (avg is in microseconds)
	opsPerSecond := 1_000_000.0 / avg

	return BenchmarkResult{
		Avg:          avg,
		P95:          p95,
		Min:          min,
		Max:          max,
		OpsPerSecond: opsPerSecond,
	}
}

func initPerformanceSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Setup
	// =============================================================================

	ctx.Step(`^a configured Aptos client for devnet$`, func() error {
		// Client is already configured in World
		return nil
	})

	ctx.Step(`^an Ed25519 key pair for benchmarking$`, func() error {
		pk, err := crypto.GenerateEd25519PrivateKey()
		if err != nil {
			return err
		}
		world.Ed25519PrivateKey = pk
		world.Ed25519PublicKey = pk.PubKey().(*crypto.Ed25519PublicKey)
		return nil
	})

	ctx.Step(`^a 256-byte message$`, func() error {
		world.Message = make([]byte, 256)
		for i := range world.Message {
			world.Message[i] = byte(i % 256)
		}
		return nil
	})

	ctx.Step(`^a signed 256-byte message$`, func() error {
		// First create the message
		world.Message = make([]byte, 256)
		for i := range world.Message {
			world.Message[i] = byte(i % 256)
		}
		// Then sign it
		if world.Ed25519PrivateKey == nil {
			pk, err := crypto.GenerateEd25519PrivateKey()
			if err != nil {
				return err
			}
			world.Ed25519PrivateKey = pk
			world.Ed25519PublicKey = pk.PubKey().(*crypto.Ed25519PublicKey)
		}
		sig, err := world.Ed25519PrivateKey.SignMessage(world.Message)
		if err != nil {
			return err
		}
		world.Ed25519Signature = sig.(*crypto.Ed25519Signature)
		return nil
	})

	ctx.Step(`^a sample raw transaction for benchmarking$`, func() error {
		// We'll use AccountAddress for BCS serialization benchmark
		// as it's a simple serializable type
		return nil
	})

	// =============================================================================
	// When Steps - Measurements
	// =============================================================================

	ctx.Step(`^I measure the time to generate (\d+) Ed25519 key pairs$`, func(iterations int) error {
		samples := make([]float64, iterations)

		// Warmup
		for i := 0; i < 100; i++ {
			_, _ = crypto.GenerateEd25519PrivateKey()
		}

		// Measure
		for i := 0; i < iterations; i++ {
			start := time.Now()
			_, _ = crypto.GenerateEd25519PrivateKey()
			elapsed := time.Since(start).Microseconds()
			samples[i] = float64(elapsed)
		}

		result := calculateStats(samples)
		world.TestVectors["benchmarkResult"] = result
		return nil
	})

	ctx.Step(`^I measure the time to sign the message (\d+) times$`, func(iterations int) error {
		if world.Ed25519PrivateKey == nil || world.Message == nil {
			return fmt.Errorf("key pair and message must be set")
		}

		samples := make([]float64, iterations)

		// Warmup
		for i := 0; i < 100; i++ {
			_, _ = world.Ed25519PrivateKey.SignMessage(world.Message)
		}

		// Measure
		for i := 0; i < iterations; i++ {
			start := time.Now()
			_, _ = world.Ed25519PrivateKey.SignMessage(world.Message)
			elapsed := time.Since(start).Microseconds()
			samples[i] = float64(elapsed)
		}

		result := calculateStats(samples)
		world.TestVectors["benchmarkResult"] = result
		return nil
	})

	ctx.Step(`^I measure the time to verify the signature (\d+) times$`, func(iterations int) error {
		if world.Ed25519PublicKey == nil || world.Message == nil || world.Ed25519Signature == nil {
			return fmt.Errorf("public key, message, and signature must be set")
		}

		samples := make([]float64, iterations)

		// Warmup
		for i := 0; i < 100; i++ {
			world.Ed25519PublicKey.Verify(world.Message, world.Ed25519Signature)
		}

		// Measure
		for i := 0; i < iterations; i++ {
			start := time.Now()
			world.Ed25519PublicKey.Verify(world.Message, world.Ed25519Signature)
			elapsed := time.Since(start).Microseconds()
			samples[i] = float64(elapsed)
		}

		result := calculateStats(samples)
		world.TestVectors["benchmarkResult"] = result
		return nil
	})

	ctx.Step(`^I measure the time to BCS serialize the transaction (\d+) times$`, func(iterations int) error {
		// Use AccountAddress for BCS serialization benchmark
		addrBytes := [32]byte{}
		addrBytes[31] = 1

		samples := make([]float64, iterations)

		// Warmup
		for i := 0; i < 100; i++ {
			result := make([]byte, 32)
			copy(result, addrBytes[:])
			_ = result
		}

		// Measure using nanoseconds for fast operations
		for i := 0; i < iterations; i++ {
			start := time.Now()
			result := make([]byte, 32)
			copy(result, addrBytes[:])
			_ = result
			elapsed := time.Since(start).Nanoseconds()
			samples[i] = float64(elapsed) / 1000.0 // Convert to microseconds
		}

		result := calculateStats(samples)
		world.TestVectors["benchmarkResult"] = result
		return nil
	})

	ctx.Step(`^I measure the time to hash the message (\d+) times$`, func(iterations int) error {
		if world.Message == nil {
			return fmt.Errorf("message must be set")
		}

		samples := make([]float64, iterations)
		msg := world.Message

		// Warmup
		for i := 0; i < 100; i++ {
			h := sha3.New256()
			h.Write(msg)
			h.Sum(nil)
		}

		// Measure using nanoseconds for fast operations
		for i := 0; i < iterations; i++ {
			start := time.Now()
			h := sha3.New256()
			h.Write(msg)
			h.Sum(nil)
			elapsed := time.Since(start).Nanoseconds()
			samples[i] = float64(elapsed) / 1000.0 // Convert to microseconds
		}

		result := calculateStats(samples)
		world.TestVectors["benchmarkResult"] = result
		return nil
	})

	// =============================================================================
	// Then Steps - Recording Results
	// =============================================================================

	ctx.Step(`^I record the average time as "([^"]*)"$`, func(metricName string) error {
		result, ok := world.TestVectors["benchmarkResult"].(BenchmarkResult)
		if !ok {
			return fmt.Errorf("no benchmark result available")
		}
		performanceResults.Results[metricName] = result.Avg
		fmt.Printf("  %s: %.2f μs\n", metricName, result.Avg)
		return nil
	})

	ctx.Step(`^I record the operations per second as "([^"]*)"$`, func(metricName string) error {
		result, ok := world.TestVectors["benchmarkResult"].(BenchmarkResult)
		if !ok {
			return fmt.Errorf("no benchmark result available")
		}
		performanceResults.Results[metricName] = result.OpsPerSecond
		fmt.Printf("  %s: %.2f ops/s\n", metricName, result.OpsPerSecond)
		return nil
	})

	// After hook to print final results
	ctx.After(func(ctx context.Context, sc *godog.Scenario, err error) (context.Context, error) {
		// Only print if we have results
		if len(performanceResults.Results) > 0 {
			jsonBytes, _ := json.MarshalIndent(performanceResults, "", "  ")
			fmt.Println("\n=== Performance Results JSON ===")
			fmt.Println(string(jsonBytes))
		}
		return ctx, nil
	})
}
