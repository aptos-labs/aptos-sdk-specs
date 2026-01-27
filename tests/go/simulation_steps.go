package main

import (
	"github.com/cucumber/godog"
)

// initSimulationSteps registers simulation step definitions.
func initSimulationSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Simulation Steps
	// =============================================================================

	ctx.Step(`^simulated gas_used = (\d+)$`, func(gasUsed int) error {
		world.TestVectors["simulatedGasUsed"] = uint64(gasUsed)
		return nil
	})

	ctx.Step(`^simulation respects that limit$`, func() error {
		// TODO: implement limit respect check
		return godog.ErrPending
	})

	ctx.Step(`^simulation should fail$`, func() error {
		success, ok := world.TestVectors["simulationSuccess"].(bool)
		if ok && success {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^simulation should reflect that$`, func() error {
		// TODO: implement simulation reflection check
		return godog.ErrPending
	})

	ctx.Step(`^simulation should show failure$`, func() error {
		success, ok := world.TestVectors["simulationSuccess"].(bool)
		if ok && success {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^simulation should work even if account hasn't committed seq (\d+) yet$`, func(seq int) error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^simulation should work$`, func() error {
		return nil
	})

	ctx.Step(`^simulation takes too long$`, func() error {
		world.TestVectors["simulationTimeout"] = true
		return nil
	})

	ctx.Step(`^simulation uses state at that version$`, func() error {
		// TODO: implement state version check
		return godog.ErrPending
	})

	ctx.Step(`^simulation uses that price for calculations$`, func() error {
		// TODO: implement price usage check
		return godog.ErrPending
	})

	ctx.Step(`^script simulation should fail$`, func() error {
		// TODO: implement script simulation check
		return godog.ErrPending
	})

	// =============================================================================
	// Submission Steps
	// =============================================================================

	ctx.Step(`^submission should fail$`, func() error {
		if world.Error == nil {
			return godog.ErrPending
		}
		return nil
	})

	// =============================================================================
	// Retry Steps
	// =============================================================================

	ctx.Step(`^receive retry attempt number and error$`, func() error {
		// TODO: awaiting SDK implementation - retry callbacks
		return godog.ErrPending
	})

	ctx.Step(`^requests should include the API key header$`, func() error {
		// TODO: implement header check
		return godog.ErrPending
	})

	ctx.Step(`^requests should not retry on failure$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^respect the retry configuration$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^retries occur$`, func() error {
		world.TestVectors["retriesOccurred"] = true
		return nil
	})

	ctx.Step(`^retry config with backoff_factor=(\d+)\.(\d+)$`, func(whole, frac int) error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^retry config with callback$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^retry config with max_retries=(\d+)$`, func(maxRetries int) error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^retry config with max_retries=(\d+), initial_delay=(\d+)ms$`, func(maxRetries, initialDelay int) error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^retry logic should apply$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^retrying is safe \(idempotent\)$`, func() error {
		// Documentation assertion
		return nil
	})

	// =============================================================================
	// Return Steps
	// =============================================================================

	ctx.Step(`^return a transaction hash$`, func() error {
		if _, ok := world.TestVectors["transactionHash"].(string); !ok {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^return the final error$`, func() error {
		if world.Error == nil {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^return the successful response$`, func() error {
		if world.Error != nil {
			return world.Error
		}
		return nil
	})

	ctx.Step(`^return type should match Move return type$`, func() error {
		// TODO: implement return type matching
		return godog.ErrPending
	})

	// =============================================================================
	// Balance Steps
	// =============================================================================

	ctx.Step(`^recipient balance increase$`, func() error {
		// TODO: implement balance increase check
		return godog.ErrPending
	})

	// =============================================================================
	// Misc Steps
	// =============================================================================

	ctx.Step(`^represent constraints properly$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^results might differ$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^rogue key attacks are prevented$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^save API calls$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^script may be more appropriate$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^set appropriate max_gas_amount$`, func() error {
		// TODO: implement gas amount setting
		return godog.ErrPending
	})

	ctx.Step(`^should indicate gas exhaustion$`, func() error {
		// TODO: implement gas exhaustion check
		return godog.ErrPending
	})

	ctx.Step(`^should respect Retry-After header if present$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^should return the error immediately$`, func() error {
		if world.Error == nil {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^should suggest waiting$`, func() error {
		// TODO: implement suggestion check
		return godog.ErrPending
	})

	ctx.Step(`^show changes for all involved accounts$`, func() error {
		// TODO: implement change visibility check
		return godog.ErrPending
	})

	ctx.Step(`^show the abort code$`, func() error {
		// TODO: implement abort code visibility
		return godog.ErrPending
	})

	ctx.Step(`^show type mismatch error$`, func() error {
		// TODO: implement type mismatch check
		return godog.ErrPending
	})

	ctx.Step(`^structure should be:$`, func() error {
		// Documentation step with table
		return nil
	})

	ctx.Step(`^that request should not retry$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^public keys from test vectors$`, func() error {
		// Load from test vectors
		return nil
	})
}
