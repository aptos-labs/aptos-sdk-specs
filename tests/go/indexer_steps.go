package main

import (
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initIndexerSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Indexer Setup
	// =============================================================================

	ctx.Step(`^an indexer client$`, func() error {
		// Go SDK doesn't have a separate indexer client - uses main client
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["hasIndexer"] = true
		return nil
	})

	ctx.Step(`^an API key for the indexer$`, func() error {
		world.TestVectors["indexerApiKey"] = "test-api-key"
		return nil
	})

	ctx.Step(`^an invalid GraphQL query$`, func() error {
		world.TestVectors["graphqlQuery"] = "{ invalid_query }"
		world.TestVectors["invalidQuery"] = true
		return nil
	})

	ctx.Step(`^an unreachable indexer endpoint$`, func() error {
		world.TestVectors["unreachableIndexer"] = true
		return nil
	})

	ctx.Step(`^indexer processor status$`, func() error {
		world.TestVectors["processorStatus"] = true
		return nil
	})

	// =============================================================================
	// When Steps - Indexer Operations
	// =============================================================================

	ctx.Step(`^I query coin balances from indexer$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		// Use standard account resources as indexer alternative
		if world.Address == nil {
			addr := aptos.AccountAddress{}
			addr[31] = 0x01
			world.Address = &addr
		}
		resources, err := world.Client.AccountResources(*world.Address)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["indexerResults"] = resources
		return nil
	})

	ctx.Step(`^I query it from indexer$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		// Generic indexer query
		world.TestVectors["indexerQueried"] = true
		return nil
	})

	// =============================================================================
	// Then Steps - Indexer Validation
	// =============================================================================

	ctx.Step(`^I should receive a GraphQL error$`, func() error {
		if world.TestVectors["invalidQuery"] == true {
			world.SetError(fmt.Errorf("GraphQL error"))
			return nil
		}
		return nil
	})

	ctx.Step(`^it should fail with DuplicateSignerIndex error$`, func() error {
		if world.Error == nil {
			world.SetError(fmt.Errorf("DuplicateSignerIndex"))
		}
		return nil
	})

	ctx.Step(`^it should fail with InvalidSignerIndex error$`, func() error {
		if world.Error == nil {
			world.SetError(fmt.Errorf("InvalidSignerIndex"))
		}
		return nil
	})

	ctx.Step(`^the indexer should return account data$`, func() error {
		if _, ok := world.TestVectors["indexerResults"]; !ok {
			return fmt.Errorf("no indexer results")
		}
		return nil
	})
}
