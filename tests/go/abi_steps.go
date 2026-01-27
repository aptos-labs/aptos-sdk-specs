package main

import (
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initABISteps registers ABI-related step definitions.
func initABISteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - ABI Setup
	// =============================================================================

	ctx.Step(`^a module address "([^"]*)"$`, func(addrStr string) error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(addrStr)
		if err != nil {
			return err
		}
		world.TestVectors["moduleAddress"] = addr
		return nil
	})

	ctx.Step(`^module name "([^"]*)"$`, func(name string) error {
		world.TestVectors["moduleName"] = name
		return nil
	})

	ctx.Step(`^an entry function in the ABI$`, func() error {
		world.TestVectors["hasEntryFunction"] = true
		return nil
	})

	ctx.Step(`^a view function in the ABI$`, func() error {
		world.TestVectors["hasViewFunction"] = true
		return nil
	})

	ctx.Step(`^a struct definition in the ABI$`, func() error {
		world.TestVectors["hasStruct"] = true
		return nil
	})

	// =============================================================================
	// When Steps - ABI Operations
	// =============================================================================

	ctx.Step(`^I fetch the module ABI$`, func() error {
		// Go SDK doesn't have direct ABI fetching - mark as pending
		// TODO: awaiting SDK implementation - module ABI fetching
		return godog.ErrPending
	})

	ctx.Step(`^I fetch ABIs for all modules$`, func() error {
		// Go SDK doesn't have direct ABI fetching - mark as pending
		// TODO: awaiting SDK implementation - module ABI fetching
		return godog.ErrPending
	})

	ctx.Step(`^I parse the ABI$`, func() error {
		// ABI is already parsed by the SDK
		world.TestVectors["abiParsed"] = true
		return nil
	})

	// =============================================================================
	// Then Steps - ABI Validation
	// =============================================================================

	ctx.Step(`^I should extract function names$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should extract struct names$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^the ABI should contain function definitions$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^the ABI should contain struct definitions$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see the function signature$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see the parameter types$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see the return type$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see the visibility$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see if it\'s a view function$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see the struct fields$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see the field types$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should see any generic parameters$`, func() error {
		// TODO: awaiting SDK implementation - ABI not supported
		return godog.ErrPending
	})

	ctx.Step(`^all modules should have ABIs$`, func() error {
		modules, ok := world.TestVectors["allModules"].([]interface{})
		if !ok {
			return fmt.Errorf("no modules found")
		}
		if len(modules) == 0 {
			return fmt.Errorf("no modules returned")
		}
		return nil
	})
}
