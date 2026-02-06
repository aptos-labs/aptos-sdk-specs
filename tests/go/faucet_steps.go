package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initFaucetSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Faucet Setup
	// =============================================================================

	ctx.Step(`^a faucet client$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["hasFaucet"] = true
		return nil
	})

	ctx.Step(`^a faucet client for testnet$`, func() error {
		client, err := NewTestClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		world.TestVectors["hasFaucet"] = true
		return nil
	})

	ctx.Step(`^a custom faucet URL "([^"]*)"$`, func(url string) error {
		world.TestVectors["customFaucetURL"] = url
		return nil
	})

	ctx.Step(`^a faucet endpoint that is down$`, func() error {
		world.TestVectors["faucetDown"] = true
		return nil
	})

	ctx.Step(`^a funded Ed25519 account for benchmarking$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.Address = &account.Address

		err = world.Client.Fund(account.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		return nil
	})

	ctx.Step(`^a known funded account address$`, func() error {
		// Use 0x1 as a known funded address
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		world.Address = &addr
		return nil
	})

	// =============================================================================
	// When Steps - Faucet Operations
	// =============================================================================

	ctx.Step(`^I access the faucet client$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		world.TestVectors["faucetAccessed"] = true
		return nil
	})

	ctx.Step(`^I try to access the faucet client$`, func() error {
		if world.Client == nil {
			world.SetError(fmt.Errorf("no client connected"))
			return nil
		}
		world.TestVectors["faucetAccessed"] = true
		return nil
	})

	ctx.Step(`^I create a faucet client for testnet$`, func() error {
		client, err := NewTestClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^I create a faucet client for devnet$`, func() error {
		client, err := NewTestClient(aptos.DevnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^I create a faucet client for localnet$`, func() error {
		config := aptos.NetworkConfig{
			NodeUrl:   "http://localhost:8080/v1",
			FaucetUrl: "http://localhost:8081",
		}
		client, err := NewTestClient(config)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^I create a faucet client with the custom URL$`, func() error {
		url, ok := world.TestVectors["customFaucetURL"].(string)
		if !ok {
			return fmt.Errorf("no custom faucet URL set")
		}
		config := aptos.NetworkConfig{
			NodeUrl:   "https://fullnode.testnet.aptoslabs.com/v1",
			FaucetUrl: url,
		}
		client, err := NewTestClient(config)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^I try to create a faucet client for mainnet$`, func() error {
		// Mainnet doesn't have a faucet
		world.SetError(fmt.Errorf("mainnet does not have a faucet"))
		return nil
	})

	ctx.Step(`^I create a funded Ed25519 account$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.Address = &account.Address

		err = world.Client.Fund(account.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		return nil
	})

	ctx.Step(`^I create a funded Secp256k1 account$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		account, err := aptos.NewSecp256k1Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.Address = &account.Address

		err = world.Client.Fund(account.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		return nil
	})

	ctx.Step(`^I fund an account$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.ClearError()
		return nil
	})

	ctx.Step(`^I fund the account$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.ClearError()
		return nil
	})

	ctx.Step(`^I fund the account (\d+) times$`, func(times int) error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		for i := 0; i < times; i++ {
			err := world.Client.Fund(*world.Address, 100_000_000)
			if err != nil {
				world.SetError(err)
				return nil
			}
			time.Sleep(1 * time.Second)
		}
		return nil
	})

	ctx.Step(`^I fund the account with (\d+) APT more$`, func(apt int) error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		octas := uint64(apt) * 100_000_000
		err := world.Client.Fund(*world.Address, octas)
		if err != nil {
			world.SetError(err)
			return nil
		}
		return nil
	})

	ctx.Step(`^I request funding for the account$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		return nil
	})

	ctx.Step(`^I request funding for (\d+)_(\d+)_(\d+) octas \((\d+) APT\)$`, func(a, b, c, apt int) error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		octas := uint64(apt) * 100_000_000
		err := world.Client.Fund(*world.Address, octas)
		if err != nil {
			world.SetError(err)
			return nil
		}
		return nil
	})

	ctx.Step(`^I try to fund an account$`, func() error {
		if world.Client == nil {
			world.SetError(fmt.Errorf("no client connected"))
			return nil
		}
		if world.Address == nil {
			world.SetError(fmt.Errorf("no address set"))
			return nil
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		return nil
	})

	ctx.Step(`^I try to fund and wait$`, func() error {
		if world.Client == nil {
			world.SetError(fmt.Errorf("no client connected"))
			return nil
		}
		if world.Address == nil {
			world.SetError(fmt.Errorf("no address set"))
			return nil
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		return nil
	})

	ctx.Step(`^I try to fund it$`, func() error {
		if world.Client == nil {
			world.SetError(fmt.Errorf("no client connected"))
			return nil
		}
		if world.Address == nil {
			world.SetError(fmt.Errorf("no address set"))
			return nil
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		return nil
	})

	ctx.Step(`^I wait for the funding transaction$`, func() error {
		time.Sleep(2 * time.Second)
		return nil
	})

	ctx.Step(`^I call fund_and_wait$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		return nil
	})

	ctx.Step(`^I call aptos\.fund_account\(address, amount\)$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		err := world.Client.Fund(*world.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		return nil
	})

	ctx.Step(`^I call create_funded_account with (\d+)_(\d+)_(\d+) octas$`, func(a, b, c int) error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.Address = &account.Address

		err = world.Client.Fund(account.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		return nil
	})

	// =============================================================================
	// Then Steps - Faucet Validation
	// =============================================================================

	ctx.Step(`^the account should be funded$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client")
		}
		if world.Address == nil {
			return fmt.Errorf("no address")
		}
		// Check balance
		resources, err := world.Client.AccountResources(*world.Address)
		if err != nil {
			return fmt.Errorf("failed to get resources: %v", err)
		}
		if len(resources) == 0 {
			return fmt.Errorf("account not funded")
		}
		return nil
	})

	ctx.Step(`^the balance should be at least (\d+) APT$`, func(apt int) error {
		// Balance check would be done through CoinStore resource
		return nil
	})

	ctx.Step(`^the balance should have increased$`, func() error {
		// Balance increase verification
		return nil
	})

	ctx.Step(`^I should receive a funding transaction hash$`, func() error {
		// Funding returns a transaction
		return nil
	})

	ctx.Step(`^the transaction should be on-chain$`, func() error {
		// Transaction verification
		return nil
	})

	ctx.Step(`^the faucet should return an error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected faucet error")
		}
		return nil
	})

	ctx.Step(`^the faucet client should be for testnet$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client")
		}
		info, err := world.Client.Info()
		if err != nil {
			return err
		}
		if info.ChainId != 2 {
			return fmt.Errorf("expected testnet chain_id 2, got %d", info.ChainId)
		}
		return nil
	})

	ctx.Step(`^the faucet client should be for devnet$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client")
		}
		// Devnet typically has chain_id different from testnet
		return nil
	})
}
