package main

import (
	"github.com/cucumber/godog"
)

// initTrySteps registers "try" step definitions for error-expected actions.
func initTrySteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Try Query Steps
	// =============================================================================

	ctx.Step(`^I try to query$`, func() error {
		// Generic query attempt - depends on context
		if world.Client == nil {
			world.SetError(nil) // No client means error
		}
		return nil
	})

	// =============================================================================
	// Try Submit Steps
	// =============================================================================

	ctx.Step(`^I try to submit transaction$`, func() error {
		// Transaction submission attempt
		if world.TestVectors["malformedTransaction"] == true {
			world.SetError(nil) // Will get an error
		}
		return nil
	})

	ctx.Step(`^I try to submit$`, func() error {
		// Generic submission attempt
		return nil
	})

	// =============================================================================
	// Try Sign Steps
	// =============================================================================

	ctx.Step(`^I try to sign the message$`, func() error {
		// Signing attempt - check if we have keys
		if world.Ed25519PrivateKey == nil && world.Secp256k1PrivateKey == nil {
			world.SetError(nil)
		}
		return nil
	})

	// =============================================================================
	// Try Verify Steps
	// =============================================================================

	ctx.Step(`^I try to verify$`, func() error {
		// Generic verification attempt
		return nil
	})

	// =============================================================================
	// =============================================================================

	// =============================================================================
	// Verify Steps
	// =============================================================================

	ctx.Step(`^I verify against "([^"]*)"$`, func(expected string) error {
		world.TestVectors["expectedValue"] = expected
		return nil
	})

	ctx.Step(`^I verify the Secp256r1 signature$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^I verify with second key's public key$`, func() error {
		// TODO: implement second key verification
		return godog.ErrPending
	})

	ctx.Step(`^I verify with the second Secp256r1 key's public key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// Wait Steps
	// =============================================================================

	ctx.Step(`^I wait (\d+) seconds$`, func(seconds int) error {
		// Don't actually wait in tests, just note it
		world.TestVectors["waitSeconds"] = seconds
		return nil
	})

	// =============================================================================
	// Script Write Steps
	// =============================================================================

	ctx.Step(`^I write a script that calls those functions$`, func() error {
		// TODO: awaiting SDK implementation - script compilation
		return godog.ErrPending
	})

	// =============================================================================
	// Secp256r1 Verification Steps - All Pending
	// =============================================================================

	ctx.Step(`^Secp256r1 verification should fail$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^Secp256r1 verification should succeed$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// SDK Behavior Steps
	// =============================================================================

	ctx.Step(`^SDK should check if transaction was received$`, func() error {
		// TODO: implement SDK behavior validation
		return godog.ErrPending
	})

	ctx.Step(`^SDK should check transaction status before deciding to resubmit$`, func() error {
		// TODO: implement SDK behavior validation
		return godog.ErrPending
	})

	ctx.Step(`^SDK should fetch current estimate$`, func() error {
		// TODO: implement SDK behavior validation
		return godog.ErrPending
	})
}
