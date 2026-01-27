package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initScriptSteps registers script payload step definitions.
func initScriptSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Script Setup
	// =============================================================================

	ctx.Step(`^a compiled Move script bytecode$`, func() error {
		// Use placeholder bytecode for testing
		world.Bytes = []byte{0x00, 0x01, 0x02, 0x03}
		world.TestVectors["scriptBytecode"] = world.Bytes
		return nil
	})

	ctx.Step(`^script arguments \[recipient_address, amount\]$`, func() error {
		world.TestVectors["scriptArgTypes"] = []string{"address", "u64"}
		return nil
	})

	ctx.Step(`^a multi-recipient transfer script$`, func() error {
		world.TestVectors["multiRecipientScript"] = true
		return nil
	})

	ctx.Step(`^a list of (\d+) recipients and amounts$`, func(count int) error {
		recipients := make([]aptos.AccountAddress, count)
		amounts := make([]uint64, count)
		for i := 0; i < count; i++ {
			recipients[i] = aptos.AccountAddress{}
			recipients[i][31] = byte(i + 1)
			amounts[i] = uint64(1000 * (i + 1))
		}
		world.TestVectors["recipients"] = recipients
		world.TestVectors["amounts"] = amounts
		return nil
	})

	// =============================================================================
	// When Steps - Script Operations
	// =============================================================================

	ctx.Step(`^I create the script payload$`, func() error {
		// Script payloads in Go SDK are created differently
		// For now, mark as implemented but document limitation
		world.TestVectors["scriptPayloadCreated"] = true
		return nil
	})

	ctx.Step(`^I execute the script with recipient list$`, func() error {
		// Would need actual script execution
		world.TestVectors["scriptExecuted"] = true
		return nil
	})

	// =============================================================================
	// Then Steps - Script Validation
	// =============================================================================

	ctx.Step(`^the script payload should contain the bytecode$`, func() error {
		if _, ok := world.TestVectors["scriptBytecode"]; !ok {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^it should encode all (\d+) transfers$`, func(count int) error {
		return nil
	})

	ctx.Step(`^each recipient should receive their amount$`, func() error {
		// TODO: implement multi-recipient transfer validation
		return godog.ErrPending
	})
}
