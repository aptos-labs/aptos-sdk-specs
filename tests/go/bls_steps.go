package main

import (
	"github.com/cucumber/godog"
)

// initBLSSteps registers all BLS12-381 related steps as pending
// since BLS is not yet fully supported in the Go SDK.
func initBLSSteps(ctx *godog.ScenarioContext, world *World) {
	// All BLS steps return pending as they require BLS12-381 support
	// TODO: awaiting SDK implementation

	// =============================================================================
	// BLS Account/Key Steps - All Pending
	// =============================================================================

	ctx.Step(`^a BLS12-381 account$`, func() error {
		// TODO: awaiting SDK implementation - BLS12-381 not supported in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^a BLS12-381 key pair$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a BLS public key and its PoP$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a BLS12-381 signature$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a BLS signature for "([^"]*)"$`, func(msg string) error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^a hex-encoded BLS12-381 private key$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	// =============================================================================
	// BLS Aggregation Steps - All Pending
	// =============================================================================

	ctx.Step(`^I verify the BLS signature$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I verify the BLS PoP$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I aggregate BLS signatures$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I aggregate BLS public keys$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^the BLS signature should be valid$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^the BLS PoP should be valid$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^the aggregated BLS signature should be valid$`, func() error {
		// TODO: awaiting SDK implementation
		return godog.ErrPending
	})

	ctx.Step(`^I generate a proof of possession$`, func() error {
		// TODO: awaiting SDK implementation - BLS12-381 PoP
		return godog.ErrPending
	})

	ctx.Step(`^I generate a random BLS12-381 key pair$`, func() error {
		// TODO: awaiting SDK implementation - BLS12-381
		return godog.ErrPending
	})

	// =============================================================================
	// Secp256r1 Steps - All Pending (not supported in Go SDK)
	// =============================================================================

	ctx.Step(`^I generate a random Secp256r1 key pair$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^I get the Secp256r1 uncompressed public key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^I parse it as Secp256r1 public key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 account$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 key pair$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 public key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 signature$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1/P-256 not in Go SDK
		return godog.ErrPending
	})
}
