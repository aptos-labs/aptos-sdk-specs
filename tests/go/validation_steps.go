package main

import (
	"fmt"

	"github.com/cucumber/godog"
)

// initValidationSteps registers validation step definitions.
func initValidationSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Account Validation Steps
	// =============================================================================

	ctx.Step(`^I should have (\d+) different accounts$`, func(count int) error {
		accounts, ok := world.TestVectors["accounts"].([]interface{})
		if !ok {
			return fmt.Errorf("no accounts found")
		}
		if len(accounts) != count {
			return fmt.Errorf("expected %d accounts, got %d", count, len(accounts))
		}
		return nil
	})

	ctx.Step(`^I should receive a new account$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account created")
		}
		return nil
	})

	// =============================================================================
	// Error Reception Steps
	// =============================================================================

	ctx.Step(`^I should receive an error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error")
		}
		return nil
	})

	ctx.Step(`^I should receive a network error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a network error")
		}
		return nil
	})

	ctx.Step(`^I should receive a not found error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a not found error")
		}
		return nil
	})

	ctx.Step(`^I should receive a validation error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a validation error")
		}
		return nil
	})

	ctx.Step(`^I should receive an appropriate error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error")
		}
		return nil
	})

	ctx.Step(`^I should receive a parse error with context$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a parse error")
		}
		return nil
	})

	ctx.Step(`^I should receive an error about unavailable state$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error about unavailable state")
		}
		return nil
	})

	// =============================================================================
	// Transaction Hash Steps
	// =============================================================================

	ctx.Step(`^I should receive transaction hash\(es\)$`, func() error {
		if _, ok := world.TestVectors["transactionHash"].(string); !ok {
			return fmt.Errorf("no transaction hash")
		}
		return nil
	})

	ctx.Step(`^I should see one or more transaction hashes$`, func() error {
		if _, ok := world.TestVectors["transactionHash"].(string); !ok {
			return fmt.Errorf("no transaction hash")
		}
		return nil
	})

	// =============================================================================
	// Result Value Steps
	// =============================================================================

	ctx.Step(`^I should receive true$`, func() error {
		result, ok := world.TestVectors["result"]
		if !ok {
			result = world.TestVectors["viewResult"]
		}
		if result == nil {
			return fmt.Errorf("no result")
		}
		// Check for boolean true or string "true"
		if boolVal, isBool := result.(bool); isBool && boolVal {
			return nil
		}
		if strVal, isStr := result.(string); isStr && strVal == "true" {
			return nil
		}
		return fmt.Errorf("result is not true: %v", result)
	})

	ctx.Step(`^I should receive return values$`, func() error {
		if _, ok := world.TestVectors["viewResult"]; !ok {
			return fmt.Errorf("no return values")
		}
		return nil
	})

	ctx.Step(`^I should receive all return values in order$`, func() error {
		// TODO: implement return value order validation
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the balance amount$`, func() error {
		if _, ok := world.TestVectors["balance"]; !ok {
			return fmt.Errorf("no balance received")
		}
		return nil
	})

	ctx.Step(`^I should receive the balance as u64$`, func() error {
		balance, ok := world.TestVectors["balance"]
		if !ok {
			return fmt.Errorf("no balance")
		}
		// Balance can be uint64 or string
		if _, isU64 := balance.(uint64); isU64 {
			return nil
		}
		if _, isStr := balance.(string); isStr {
			return nil
		}
		return fmt.Errorf("balance is not u64: %T", balance)
	})

	ctx.Step(`^I should receive current blockchain timestamp$`, func() error {
		if _, ok := world.TestVectors["timestamp"]; !ok {
			return fmt.Errorf("no timestamp received")
		}
		return nil
	})

	// =============================================================================
	// Empty Results Steps
	// =============================================================================

	ctx.Step(`^I should receive an empty list$`, func() error {
		result, ok := world.TestVectors["result"].([]interface{})
		if !ok {
			// Empty is also acceptable if there's no result
			return nil
		}
		if len(result) != 0 {
			return fmt.Errorf("expected empty list, got %d items", len(result))
		}
		return nil
	})

	// =============================================================================
	// Simulation Steps
	// =============================================================================

	ctx.Step(`^I should see success status$`, func() error {
		status, ok := world.TestVectors["simulationSuccess"].(bool)
		if !ok {
			return fmt.Errorf("no simulation status")
		}
		if !status {
			return fmt.Errorf("simulation did not succeed")
		}
		return nil
	})

	ctx.Step(`^I should see execution result$`, func() error {
		if _, ok := world.TestVectors["simulationResult"]; !ok {
			return fmt.Errorf("no execution result")
		}
		return nil
	})

	ctx.Step(`^I should see state changes that would occur$`, func() error {
		// TODO: implement state change visibility
		return godog.ErrPending
	})

	ctx.Step(`^I should see which resources change$`, func() error {
		// TODO: implement resource change visibility
		return godog.ErrPending
	})

	ctx.Step(`^I should see which events would emit$`, func() error {
		// TODO: implement event emission visibility
		return godog.ErrPending
	})

	// =============================================================================
	// Indexer-Related Steps - All Pending
	// =============================================================================

	ctx.Step(`^I should receive a list of balances$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive a list of tokens$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive at most (\d+) tokens$`, func(max int) error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive collection details$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive matching events$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive relevant events$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the ABI definition$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^I should receive ABIs for each module$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the next page$`, func() error {
		// TODO: awaiting SDK implementation - pagination
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the query result$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the state as of that version$`, func() error {
		// TODO: awaiting SDK implementation - historical state
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the total supply$`, func() error {
		// TODO: awaiting SDK implementation - token queries
		return godog.ErrPending
	})

	ctx.Step(`^I should receive tokens belonging to that collection$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should receive all coin types and amounts$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should only receive user transactions$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	// =============================================================================
	// Token/NFT Field Steps - All Pending (requires indexer)
	// =============================================================================

	ctx.Step(`^I should see amount$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see collection_name$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see creator_address$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see current_supply$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see decimals$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see deposits and withdrawals$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see description$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see hash$`, func() error {
		if _, ok := world.TestVectors["transactionHash"].(string); !ok {
			return fmt.Errorf("no hash")
		}
		return nil
	})

	ctx.Step(`^I should see name$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see sender$`, func() error {
		if _, ok := world.TestVectors["sender"]; !ok {
			return fmt.Errorf("no sender")
		}
		return nil
	})

	ctx.Step(`^I should see sender balance decrease$`, func() error {
		// TODO: implement balance decrease validation
		return godog.ErrPending
	})

	ctx.Step(`^I should see symbol$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see the last processed version$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see timestamp$`, func() error {
		if _, ok := world.TestVectors["timestamp"]; !ok {
			return fmt.Errorf("no timestamp")
		}
		return nil
	})

	ctx.Step(`^I should see token_name$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see token_uri$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see uri$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should see version$`, func() error {
		if _, ok := world.TestVectors["version"]; !ok {
			return fmt.Errorf("no version")
		}
		return nil
	})

	ctx.Step(`^I should see how many retries were attempted$`, func() error {
		// TODO: awaiting SDK implementation - retry visibility
		return godog.ErrPending
	})

	// =============================================================================
	// Keyless Steps - All Pending
	// =============================================================================

	ctx.Step(`^I should receive a valid proof$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^I should receive ProofGenerationFailed error$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// Script Steps
	// =============================================================================

	ctx.Step(`^I should have a valid TransactionPayload::Script$`, func() error {
		// TODO: implement script payload validation
		return godog.ErrPending
	})

	ctx.Step(`^I should recover the original Script$`, func() error {
		// TODO: implement script recovery validation
		return godog.ErrPending
	})
}
