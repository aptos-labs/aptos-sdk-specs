package main

import (
	"github.com/cucumber/godog"
)

// initIndexerSteps registers indexer/GraphQL-related step definitions.
// NOTE: The Go SDK doesn't have a dedicated GraphQL/Indexer client.
// These tests are marked as pending since they require GraphQL support.
func initIndexerSteps(ctx *godog.ScenarioContext, world *World) {
	// All indexer/GraphQL tests require GraphQL client support
	// which the Go SDK doesn't provide. Mark all as pending.

	// Given steps
	ctx.Step(`^an indexer client$`, func() error {
		// TODO: Go SDK doesn't have a dedicated indexer client
		return godog.ErrPending
	})

	ctx.Step(`^an API key for the indexer$`, func() error {
		// TODO: Go SDK doesn't support indexer API keys
		return godog.ErrPending
	})

	ctx.Step(`^an invalid GraphQL query$`, func() error {
		// TODO: Go SDK doesn't support GraphQL
		return godog.ErrPending
	})

	ctx.Step(`^an unreachable indexer endpoint$`, func() error {
		// TODO: Go SDK doesn't have configurable indexer endpoint
		return godog.ErrPending
	})

	ctx.Step(`^indexer processor status$`, func() error {
		// TODO: Go SDK doesn't support processor status queries
		return godog.ErrPending
	})

	// When steps
	ctx.Step(`^I query coin balances from indexer$`, func() error {
		// TODO: Go SDK doesn't support indexer queries
		return godog.ErrPending
	})

	ctx.Step(`^I query it from indexer$`, func() error {
		// TODO: Go SDK doesn't support indexer queries
		return godog.ErrPending
	})

	// Then steps
	ctx.Step(`^I should receive a GraphQL error$`, func() error {
		// TODO: Go SDK doesn't support GraphQL
		return godog.ErrPending
	})

	ctx.Step(`^the indexer should return account data$`, func() error {
		// TODO: Go SDK doesn't support indexer queries
		return godog.ErrPending
	})

	// Note: DuplicateSignerIndex and InvalidSignerIndex are transaction errors,
	// not indexer errors. They're handled in error_steps.go
}
