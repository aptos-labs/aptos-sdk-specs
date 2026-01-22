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

	// Address steps
	initAddressSteps(ctx, world)

	// Cryptography steps
	initCryptoSteps(ctx, world)

	// Account steps
	initAccountSteps(ctx, world)

	// Transaction steps
	initTransactionSteps(ctx, world)

	// Reset world before each scenario
	ctx.Before(func(ctx context.Context, sc *godog.Scenario) (context.Context, error) {
		world.Reset()
		return ctx, nil
	})
}

