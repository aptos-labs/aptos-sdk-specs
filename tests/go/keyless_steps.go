package main

import (
	"github.com/cucumber/godog"
)

// initKeylessSteps registers all keyless/JWT/OIDC related steps as pending
// since these features are not yet supported in the Go SDK.
func initKeylessSteps(ctx *godog.ScenarioContext, world *World) {
	// All keyless steps return pending as they require JWT/OIDC support
	// TODO: awaiting SDK implementation

	// =============================================================================
	// Keyless Account Steps - All Pending
	// =============================================================================

	ctx.Step(`^a keyless account$`, func() error {
		// TODO: awaiting SDK implementation - Keyless accounts require JWT/OIDC support
		return godog.ErrPending
	})

	ctx.Step(`^a keyless account from Google JWT$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a keyless account with expired ZK proof$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a keyless account with expired ephemeral key$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a keyless account with expiring proof$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a keyless account with valid proof$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a valid keyless account$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I derive the keyless address$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I try to create a keyless account$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	// =============================================================================
	// Ephemeral Key Steps - All Pending
	// =============================================================================

	ctx.Step(`^I generate an ephemeral key pair with (\d+) second expiry$`, func(seconds int) error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I generate two ephemeral key pairs$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^an ephemeral key pair with (\d+) second expiry$`, func(seconds int) error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^an ephemeral key pair with nonce "([^"]*)"$`, func(nonce string) error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I sign the message with an ephemeral key pair$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I sign the transaction with an ephemeral key pair$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	// =============================================================================
	// JWT/OIDC Steps - All Pending
	// =============================================================================

	ctx.Step(`^a valid JWT$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a valid JWT from Google$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a new JWT$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a malformed JWT string$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^JWT claims and pepper from test vectors$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^OidcProvider Google$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^OidcProvider Apple$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	// =============================================================================
	// Pepper/Nonce Steps - All Pending
	// =============================================================================

	ctx.Step(`^a pepper$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a pepper value$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a pepper from the pepper service$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I get the nonce$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I request a pepper$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I request pepper twice$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I should receive a pepper value$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I should receive PepperServiceError$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})
}
