package main

import (
	"context"
	"os"
	"testing"

	"github.com/cucumber/godog"
	"github.com/cucumber/godog/colors"
)

var opts = godog.Options{
	Output: colors.Colored(os.Stdout),
	Format: "progress",
	Paths:  []string{"../../features"},
	Tags:   "",
}

func init() {
	// Parse command line flags for godog
	godog.BindCommandLineFlags("godog.", &opts)

	// Also check environment variable for tags
	if tags := os.Getenv("GODOG_TAGS"); tags != "" {
		opts.Tags = tags
	}
}

func TestFeatures(t *testing.T) {
	suite := godog.TestSuite{
		ScenarioInitializer: InitializeScenario,
		Options:             &opts,
	}

	if suite.Run() != 0 {
		t.Fatal("non-zero status returned, tests failed")
	}
}

func InitializeScenario(ctx *godog.ScenarioContext) {
	world := NewWorld()

	// Cryptography steps (register first for more specific patterns)
	initHashingSteps(ctx, world)
	initCryptoSteps(ctx, world)

	// Core types steps
	initAddressSteps(ctx, world)
	initSerializationSteps(ctx, world)
	initTypeTagSteps(ctx, world)

	// Account steps
	initAccountSteps(ctx, world)
	initAuthKeySteps(ctx, world)

	// Transaction steps
	initTransactionSteps(ctx, world)
	initSigningSteps(ctx, world)
	initEntryFunctionSteps(ctx, world)

	// API client steps
	initAPIClientSteps(ctx, world)

	// Error handling steps
	initErrorSteps(ctx, world)

	// Faucet steps
	initFaucetSteps(ctx, world)

	// Multi-agent and fee payer steps
	initMultiAgentSteps(ctx, world)

	// View function steps
	initViewFunctionSteps(ctx, world)

	// Miscellaneous steps
	initMiscSteps(ctx, world)

	// Indexer steps
	initIndexerSteps(ctx, world)

	// Retry steps
	initRetrySteps(ctx, world)

	// Multi-sig steps
	initMultiSigSteps(ctx, world)

	// Keyless steps (all pending - awaiting SDK implementation)
	initKeylessSteps(ctx, world)

	// BLS steps (all pending - awaiting SDK implementation)
	initBLSSteps(ctx, world)

	// Mnemonic/derivation steps
	initMnemonicSteps(ctx, world)

	// Script steps
	initScriptSteps(ctx, world)

	// ABI steps
	initABISteps(ctx, world)

	// Encoding steps
	initEncodingSteps(ctx, world)

	// Query steps (mostly pending - requires indexer)
	initQuerySteps(ctx, world)

	// Codegen steps (all pending - SDK doesn't have codegen)
	initCodegenSteps(ctx, world)

	// Validation steps
	initValidationSteps(ctx, world)

	// Action steps
	initActionSteps(ctx, world)

	// Given steps
	initGivenSteps(ctx, world)

	// Try steps
	initTrySteps(ctx, world)

	// Setup steps
	initSetupSteps(ctx, world)

	// Assertion steps
	initAssertionSteps(ctx, world)

	// Performance steps
	initPerformanceSteps(ctx, world)

	// Reset world before each scenario
	ctx.Before(func(ctx context.Context, sc *godog.Scenario) (context.Context, error) {
		world.Reset()
		return ctx, nil
	})
}
