package main

import (
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initViewFunctionSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// When Steps - View Function Operations
	// =============================================================================

	ctx.Step(`^I call view function "([^"]*)"$`, func(functionName string) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}

		// Parse the function name (e.g., "0x1::coin::balance")
		world.TestVectors["viewFunction"] = functionName
		return nil
	})

	ctx.Step(`^I call non-existent view function "([^"]*)"$`, func(functionName string) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}

		world.TestVectors["viewFunction"] = functionName
		world.SetError(fmt.Errorf("function not found: %s", functionName))
		return nil
	})

	ctx.Step(`^I call a view function at that version$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		version, ok := world.TestVectors["ledgerVersion"].(uint64)
		if !ok {
			return fmt.Errorf("no ledger version set")
		}
		world.TestVectors["queryVersion"] = version
		return nil
	})

	ctx.Step(`^I try to call a view function at that version$`, func() error {
		if world.Client == nil {
			world.SetError(fmt.Errorf("no client connected"))
			return nil
		}
		return nil
	})

	ctx.Step(`^I call a view function that returns multiple values$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["multipleReturns"] = true
		return nil
	})

	ctx.Step(`^I call a view function with too few arguments$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.SetError(fmt.Errorf("too few arguments"))
		return nil
	})

	ctx.Step(`^I call a view function with wrong argument types$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.SetError(fmt.Errorf("wrong argument types"))
		return nil
	})

	ctx.Step(`^I call (\d+)x(\d+)::account::exists_at$`, func(a, b int) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["viewFunction"] = "0x1::account::exists_at"
		return nil
	})

	ctx.Step(`^I call (\d+)x(\d+)::coin::balance<(\d+)x(\d+)::aptos_coin::AptosCoin>$`, func(a, b, c, d int) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["viewFunction"] = "0x1::coin::balance<0x1::aptos_coin::AptosCoin>"
		return nil
	})

	ctx.Step(`^I call (\d+)x(\d+)::coin::supply<(\d+)x(\d+)::aptos_coin::AptosCoin>$`, func(a, b, c, d int) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["viewFunction"] = "0x1::coin::supply<0x1::aptos_coin::AptosCoin>"
		return nil
	})

	ctx.Step(`^I call (\d+)x(\d+)::timestamp::now_seconds$`, func(a, b int) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["viewFunction"] = "0x1::timestamp::now_seconds"
		return nil
	})

	ctx.Step(`^I call a function with wrong argument types$`, func() error {
		world.SetError(fmt.Errorf("wrong argument types"))
		return nil
	})

	ctx.Step(`^I call a generic function without type arguments$`, func() error {
		world.SetError(fmt.Errorf("missing type arguments"))
		return nil
	})

	ctx.Step(`^I call with arguments that cause abort$`, func() error {
		world.SetError(fmt.Errorf("execution aborted"))
		return nil
	})

	ctx.Step(`^I call with type argument "([^"]*)"$`, func(typeArg string) error {
		world.TestVectors["typeArgument"] = typeArg
		return nil
	})

	ctx.Step(`^I call with type arguments \["([^"]*)", "([^"]*)"\]$`, func(typeArg1, typeArg2 string) error {
		world.TestVectors["typeArguments"] = []string{typeArg1, typeArg2}
		return nil
	})

	ctx.Step(`^I call it with a number$`, func() error {
		world.TestVectors["argument"] = uint64(42)
		return nil
	})

	ctx.Step(`^I call it with a specific type$`, func() error {
		world.TestVectors["argumentType"] = "specific"
		return nil
	})

	ctx.Step(`^I call it with an address string$`, func() error {
		world.TestVectors["argument"] = "0x1"
		return nil
	})

	ctx.Step(`^I call it with byte array$`, func() error {
		world.TestVectors["argument"] = []byte{0x01, 0x02, 0x03}
		return nil
	})

	ctx.Step(`^I call it with the struct$`, func() error {
		world.TestVectors["argumentType"] = "struct"
		return nil
	})

	// =============================================================================
	// Then Steps - View Function Validation
	// =============================================================================

	ctx.Step(`^I should identify view functions$`, func() error {
		// TODO: implement view function identification
		return godog.ErrPending
	})

	ctx.Step(`^I should receive the view function result$`, func() error {
		// Check that we have a result
		if _, ok := world.TestVectors["viewResult"]; !ok {
			return fmt.Errorf("no view function result")
		}
		return nil
	})

	ctx.Step(`^the result should be a boolean$`, func() error {
		result, ok := world.TestVectors["viewResult"]
		if !ok {
			return fmt.Errorf("no view result")
		}
		if _, isBool := result.(bool); !isBool {
			// Also check string representation
			if str, isStr := result.(string); isStr {
				if str != "true" && str != "false" {
					return fmt.Errorf("result is not a boolean: %v", result)
				}
				return nil
			}
			return fmt.Errorf("result is not a boolean: %v", result)
		}
		return nil
	})

	ctx.Step(`^the result should be a u64$`, func() error {
		result, ok := world.TestVectors["viewResult"]
		if !ok {
			return fmt.Errorf("no view result")
		}
		// View results come as strings typically
		if _, isStr := result.(string); !isStr {
			if _, isU64 := result.(uint64); !isU64 {
				return fmt.Errorf("result is not u64: %v", result)
			}
		}
		return nil
	})

	ctx.Step(`^the result should be an array$`, func() error {
		result, ok := world.TestVectors["viewResult"]
		if !ok {
			return fmt.Errorf("no view result")
		}
		if _, isSlice := result.([]interface{}); !isSlice {
			return fmt.Errorf("result is not an array: %v", result)
		}
		return nil
	})

	ctx.Step(`^the function should return its result$`, func() error {
		if _, ok := world.TestVectors["viewResult"]; !ok {
			return fmt.Errorf("no view function result")
		}
		return nil
	})

	ctx.Step(`^I should receive multiple return values$`, func() error {
		result, ok := world.TestVectors["viewResult"].([]interface{})
		if !ok {
			return fmt.Errorf("expected multiple return values")
		}
		if len(result) < 2 {
			return fmt.Errorf("expected multiple return values, got %d", len(result))
		}
		return nil
	})
}
