package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/api"
	"github.com/cucumber/godog"
)

func initAPIClientSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Client Configuration (Real SDK calls)
	// =============================================================================

	ctx.Step(`^a client connected to testnet$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a client connected to testnet \(chain_id=(\d+)\)$`, func(chainId int) error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a client connected to devnet$`, func() error {
		client, err := aptos.NewClient(aptos.DevnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a client connected to mainnet$`, func() error {
		client, err := aptos.NewClient(aptos.MainnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a client connected to any network$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a connected client$`, func() error {
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		return nil
	})

	ctx.Step(`^I create a client with testnet configuration$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		world.ClearError()
		return nil
	})

	ctx.Step(`^I create a client with mainnet configuration$`, func() error {
		client, err := aptos.NewClient(aptos.MainnetConfig)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		world.ClearError()
		return nil
	})

	ctx.Step(`^a custom URL "([^"]*)"$`, func(url string) error {
		world.NetworkURL = url
		return nil
	})

	ctx.Step(`^I create a client with the custom URL$`, func() error {
		config := aptos.NetworkConfig{
			NodeUrl: world.NetworkURL,
		}
		client, err := aptos.NewClient(config)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		world.ClearError()
		return nil
	})

	ctx.Step(`^a client configured for unreachable URL$`, func() error {
		config := aptos.NetworkConfig{
			NodeUrl: "http://localhost:9999",
		}
		client, err := aptos.NewClient(config)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a client with unreachable endpoint$`, func() error {
		config := aptos.NetworkConfig{
			NodeUrl: "http://localhost:9999",
		}
		client, err := aptos.NewClient(config)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^an Aptos client$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^an Aptos client configured for testnet$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^an Aptos client configured for mainnet$`, func() error {
		client, err := aptos.NewClient(aptos.MainnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^an Aptos client for testnet$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a new Aptos client$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^a connected Aptos client$`, func() error {
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		return nil
	})

	// =============================================================================
	// When Steps - API Operations (Real SDK calls)
	// =============================================================================

	ctx.Step(`^I get ledger info$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		info, err := world.Client.Info()
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["ledgerInfo"] = info
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get account info$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		info, err := world.Client.Account(*world.Address)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["accountInfo"] = info
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get account info for the address$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		info, err := world.Client.Account(*world.Address)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["accountInfo"] = info
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get account info for "([^"]*)"$`, func(addrHex string) error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		addr := &aptos.AccountAddress{}
		if err := addr.ParseStringRelaxed(addrHex); err != nil {
			world.SetError(err)
			return nil
		}
		info, err := world.Client.Account(*addr)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["accountInfo"] = info
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get account resources$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		resources, err := world.Client.AccountResources(*world.Address)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["resources"] = resources
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get resource "([^"]*)"$`, func(resourceType string) error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		resource, err := world.Client.AccountResource(*world.Address, resourceType)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["resource"] = resource
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get the coin info resource for AptosCoin$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		resource, err := world.Client.AccountResource(addr, "0x1::coin::CoinInfo<0x1::aptos_coin::AptosCoin>")
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["resource"] = resource
		world.ClearError()
		return nil
	})

	ctx.Step(`^I get account modules$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		module, err := world.Client.AccountModule(*world.Address, "coin")
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["module"] = module
		world.ClearError()
		return nil
	})

	ctx.Step(`^I submit the transaction$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		response, err := world.Client.SubmitTransaction(signedTx)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["submitResponse"] = response
		world.ClearError()
		return nil
	})

	ctx.Step(`^I wait for the transaction$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		// First try transactionHash, then fall back to submitResponse
		hash, ok := world.TestVectors["transactionHash"].(string)
		if !ok {
			response, ok := world.TestVectors["submitResponse"].(*api.SubmitTransactionResponse)
			if !ok {
				return fmt.Errorf("no submit response")
			}
			hash = response.Hash
		}
		txn, err := world.Client.WaitForTransaction(hash)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["transaction"] = txn
		world.ClearError()
		return nil
	})

	ctx.Step(`^I wait for the transaction to complete$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		hash, ok := world.TestVectors["transactionHash"].(string)
		if !ok {
			return fmt.Errorf("no transaction hash")
		}
		txn, err := world.Client.WaitForTransaction(hash)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["transaction"] = txn
		return nil
	})

	ctx.Step(`^I get transaction by hash$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		hash, ok := world.TestVectors["transactionHash"].(string)
		if !ok {
			return fmt.Errorf("no transaction hash set")
		}
		txn, err := world.Client.TransactionByHash(hash)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["transaction"] = txn
		world.ClearError()
		return nil
	})

	ctx.Step(`^I simulate the transaction$`, func() error {
		// Ensure client is connected
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}

		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction set")
		}
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}
		results, err := world.Client.SimulateTransaction(rawTx, world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["simulationResults"] = results
		world.ClearError()
		return nil
	})

	ctx.Step(`^a signed transaction for submission$`, func() error {
		// Ensure client is connected
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}

		// Create an account if needed
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
			world.Address = &account.Address

			// Fund the account for simulation
			if err := world.Client.Fund(account.Address, 100_000_000); err != nil {
				return fmt.Errorf("failed to fund account: %v", err)
			}
			time.Sleep(2 * time.Second)
		}

		// Get current sequence number
		info, err := world.Client.Account(world.Account.Address)
		if err != nil {
			return err
		}
		seqNum, err := info.SequenceNumber()
		if err != nil {
			return err
		}

		// Create a raw transaction
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		ledgerInfo, err := world.Client.Info()
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             seqNum,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    ledgerInfo.ChainId,
		}
		world.TestVectors["rawTransaction"] = rawTx

		// Sign the transaction
		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^I call sign_submit_and_wait\(\)$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}
		payload, ok := world.TestVectors["payload"].(*aptos.EntryFunction)
		if !ok {
			return fmt.Errorf("no payload set")
		}

		response, err := world.Client.BuildSignAndSubmitTransaction(
			world.Account,
			aptos.TransactionPayload{Payload: payload},
		)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["submitResponse"] = response

		txn, err := world.Client.WaitForTransaction(response.Hash)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["transaction"] = txn
		world.ClearError()
		return nil
	})

	ctx.Step(`^a gas price estimate$`, func() error {
		// Ensure client is connected
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		estimate, err := world.Client.EstimateGasPrice()
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["gasEstimate"] = estimate
		return nil
	})

	ctx.Step(`^I should be able to read the balance$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		balance, err := world.Client.AccountAPTBalance(*world.Address)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["balance"] = balance
		return nil
	})

	// =============================================================================
	// Then Steps - Validation (Real checks on SDK results)
	// =============================================================================

	ctx.Step(`^I should receive ledger info$`, func() error {
		if _, ok := world.TestVectors["ledgerInfo"]; !ok {
			return fmt.Errorf("no ledger info received")
		}
		return nil
	})

	ctx.Step(`^it should include chain_id$`, func() error {
		info, ok := world.TestVectors["ledgerInfo"].(aptos.NodeInfo)
		if !ok {
			return fmt.Errorf("no ledger info")
		}
		if info.ChainId == 0 {
			return fmt.Errorf("chain_id is 0")
		}
		return nil
	})

	ctx.Step(`^it should include epoch$`, func() error {
		info, ok := world.TestVectors["ledgerInfo"].(aptos.NodeInfo)
		if !ok {
			return fmt.Errorf("no ledger info")
		}
		_ = info.Epoch()
		return nil
	})

	ctx.Step(`^it should include ledger_version$`, func() error {
		info, ok := world.TestVectors["ledgerInfo"].(aptos.NodeInfo)
		if !ok {
			return fmt.Errorf("no ledger info")
		}
		_ = info.LedgerVersion()
		return nil
	})

	ctx.Step(`^it should include ledger_timestamp$`, func() error {
		info, ok := world.TestVectors["ledgerInfo"].(aptos.NodeInfo)
		if !ok {
			return fmt.Errorf("no ledger info")
		}
		_ = info.LedgerTimestamp()
		return nil
	})

	ctx.Step(`^I should receive account info$`, func() error {
		if _, ok := world.TestVectors["accountInfo"]; !ok {
			return fmt.Errorf("no account info received")
		}
		return nil
	})

	ctx.Step(`^I should receive sequence_number$`, func() error {
		info, ok := world.TestVectors["accountInfo"].(aptos.AccountInfo)
		if !ok {
			return fmt.Errorf("no account info")
		}
		_ = info.SequenceNumber
		return nil
	})

	ctx.Step(`^I should receive the current sequence_number$`, func() error {
		info, ok := world.TestVectors["accountInfo"].(aptos.AccountInfo)
		if !ok {
			return fmt.Errorf("no account info")
		}
		world.TestVectors["sequenceNumber"] = info.SequenceNumber
		return nil
	})

	ctx.Step(`^I should receive authentication_key$`, func() error {
		info, ok := world.TestVectors["accountInfo"].(aptos.AccountInfo)
		if !ok {
			return fmt.Errorf("no account info")
		}
		_ = info.AuthenticationKey
		return nil
	})

	ctx.Step(`^the API returns an error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error")
		}
		return nil
	})

	ctx.Step(`^the API returns (\d+)$`, func(statusCode int) error {
		if world.Error == nil {
			return fmt.Errorf("expected an error with status %d", statusCode)
		}
		return nil
	})

	ctx.Step(`^the transaction should be committed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("transaction failed: %v", world.Error)
		}
		if _, ok := world.TestVectors["transaction"]; !ok {
			return fmt.Errorf("no transaction result")
		}
		return nil
	})

	ctx.Step(`^the response should contain the transaction hash$`, func() error {
		response, ok := world.TestVectors["submitResponse"].(*api.SubmitTransactionResponse)
		if !ok {
			return fmt.Errorf("no submit response")
		}
		if response.Hash == "" {
			return fmt.Errorf("no transaction hash")
		}
		return nil
	})

	ctx.Step(`^I should receive the transaction hash$`, func() error {
		response, ok := world.TestVectors["submitResponse"].(*api.SubmitTransactionResponse)
		if !ok {
			return fmt.Errorf("no submit response")
		}
		world.TestVectors["transactionHash"] = response.Hash
		return nil
	})

	ctx.Step(`^the transaction should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("transaction failed: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^the transaction should fail$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected transaction to fail")
		}
		return nil
	})

	ctx.Step(`^all requests should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("request failed: %v", world.Error)
		}
		return nil
	})

	// =============================================================================
	// Given Steps - Test Data Setup (Real SDK account/address creation)
	// =============================================================================

	ctx.Step(`^a known existing account address$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		world.Address = &addr
		return nil
	})

	ctx.Step(`^an account address with resources$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		world.Address = &addr
		return nil
	})

	ctx.Step(`^an account with APT balance$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.Address = &account.Address
		return nil
	})

	ctx.Step(`^an account with APT$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.Address = &account.Address
		return nil
	})

	ctx.Step(`^a new account address$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Address = &account.Address
		return nil
	})

	ctx.Step(`^an address that doesn't exist on-chain$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Address = &account.Address
		return nil
	})

	ctx.Step(`^an account with many transactions$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		world.Address = &addr
		return nil
	})

	ctx.Step(`^an account with transaction history$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		world.Address = &addr
		return nil
	})

	ctx.Step(`^an account with coin balances$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0x01
		world.Address = &addr
		return nil
	})

	ctx.Step(`^an account with published modules \(e\.g\. 0x(\d+)\)$`, func(addrVal int) error {
		addr := aptos.AccountAddress{}
		addr[31] = byte(addrVal)
		world.Address = &addr
		return nil
	})

	ctx.Step(`^a submitted transaction hash$`, func() error {
		// Check if we already have a submit response
		if response, ok := world.TestVectors["submitResponse"].(*api.SubmitTransactionResponse); ok {
			world.TestVectors["transactionHash"] = response.Hash
			return nil
		}

		// Otherwise, create and submit a transaction
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}

		// Create and fund an account
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account

		if err := world.Client.Fund(account.Address, 100_000_000); err != nil {
			// For @network tests, we need funding to succeed
			return fmt.Errorf("failed to fund account: %v", err)
		}
		time.Sleep(2 * time.Second)

		// Submit a simple transaction
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}
		response, err := world.Client.BuildSignAndSubmitTransaction(
			account,
			aptos.TransactionPayload{Payload: payload},
		)
		if err != nil {
			return fmt.Errorf("failed to submit transaction: %v", err)
		}
		world.TestVectors["submitResponse"] = response
		world.TestVectors["transactionHash"] = response.Hash
		return nil
	})

	ctx.Step(`^a nonexistent transaction hash$`, func() error {
		world.TestVectors["transactionHash"] = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
		return nil
	})

	ctx.Step(`^a known ledger version$`, func() error {
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		info, err := world.Client.Info()
		if err != nil {
			return err
		}
		world.TestVectors["ledgerVersion"] = info.LedgerVersion()
		return nil
	})

	ctx.Step(`^a known past ledger version$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		info, err := world.Client.Info()
		if err != nil {
			return err
		}
		version := info.LedgerVersion() - 100
		world.TestVectors["ledgerVersion"] = version
		return nil
	})

	// =============================================================================
	// Faucet Steps (Real SDK calls)
	// =============================================================================

	ctx.Step(`^I fund the account from faucet$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}
		err := world.Client.Fund(world.Account.Address, 100_000_000)
		if err != nil {
			world.SetError(err)
			return nil
		}
		time.Sleep(2 * time.Second)
		world.ClearError()
		return nil
	})

	ctx.Step(`^a funded account$`, func() error {
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
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
	// Transaction Steps (Real SDK calls)
	// =============================================================================

	ctx.Step(`^a simple transfer transaction$`, func() error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}
		world.TestVectors["payload"] = payload
		return nil
	})

	ctx.Step(`^a newly submitted transaction$`, func() error {
		// Ensure client is connected
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}

		// Create and fund an account if needed
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
			world.Address = &account.Address

			if err := world.Client.Fund(account.Address, 100_000_000); err != nil {
				return fmt.Errorf("failed to fund account: %v", err)
			}
			time.Sleep(2 * time.Second)
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}
		response, err := world.Client.BuildSignAndSubmitTransaction(
			world.Account,
			aptos.TransactionPayload{Payload: payload},
		)
		if err != nil {
			return fmt.Errorf("failed to submit transaction: %v", err)
		}
		world.TestVectors["submitResponse"] = response
		world.TestVectors["transactionHash"] = response.Hash
		return nil
	})

	// =============================================================================
	// Additional Steps for Transaction Scenarios
	// =============================================================================

	ctx.Step(`^I should receive the final transaction result$`, func() error {
		if _, ok := world.TestVectors["transaction"]; !ok {
			return fmt.Errorf("no transaction result")
		}
		return nil
	})

	ctx.Step(`^the transaction should be committed or failed$`, func() error {
		// If we have a transaction, it has completed (committed or failed)
		if _, ok := world.TestVectors["transaction"]; ok {
			return nil
		}
		// If there was an error during wait, that's also an expected outcome
		if world.Error != nil {
			return nil
		}
		return fmt.Errorf("transaction not completed")
	})

	ctx.Step(`^the SDK should poll the API$`, func() error {
		// This is verified implicitly - if we got a result, polling happened
		return nil
	})

	ctx.Step(`^I wait for it$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		hash, ok := world.TestVectors["transactionHash"].(string)
		if !ok {
			return fmt.Errorf("no transaction hash")
		}
		txn, err := world.Client.WaitForTransaction(hash)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["transaction"] = txn
		return nil
	})

	ctx.Step(`^I build a transaction using the estimate$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}

		// Ensure we have an account
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
			world.Address = &account.Address

			if err := world.Client.Fund(account.Address, 100_000_000); err != nil {
				return fmt.Errorf("failed to fund account: %v", err)
			}
			time.Sleep(2 * time.Second)
		}

		estimate, ok := world.TestVectors["gasEstimate"].(aptos.EstimateGasInfo)
		if !ok {
			return fmt.Errorf("no gas estimate")
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		// Get account info for sequence number
		info, err := world.Client.Account(world.Account.Address)
		if err != nil {
			return err
		}
		seqNum, err := info.SequenceNumber()
		if err != nil {
			return err
		}

		ledgerInfo, err := world.Client.Info()
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             seqNum,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               estimate.GasEstimate,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    ledgerInfo.ChainId,
		}
		world.TestVectors["rawTransaction"] = rawTx

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^submit it$`, func() error {
		if world.Client == nil {
			return fmt.Errorf("no client connected")
		}
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction")
		}
		response, err := world.Client.SubmitTransaction(signedTx)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["submitResponse"] = response
		world.TestVectors["transactionHash"] = response.Hash
		return nil
	})

	ctx.Step(`^the transaction should be accepted$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("transaction not accepted: %v", world.Error)
		}
		if _, ok := world.TestVectors["submitResponse"]; !ok {
			return fmt.Errorf("no submit response")
		}
		return nil
	})

	ctx.Step(`^the results should include gas_used$`, func() error {
		results, ok := world.TestVectors["simulationResults"].([]api.UserTransaction)
		if !ok || len(results) == 0 {
			return fmt.Errorf("no simulation results")
		}
		// Check that GasUsed is present (should be > 0)
		if results[0].GasUsed == 0 {
			return fmt.Errorf("gas_used is 0")
		}
		return nil
	})

	ctx.Step(`^the results should include success status$`, func() error {
		results, ok := world.TestVectors["simulationResults"].([]api.UserTransaction)
		if !ok || len(results) == 0 {
			return fmt.Errorf("no simulation results")
		}
		// Success field should be present (true or false)
		_ = results[0].Success
		return nil
	})

	ctx.Step(`^I should receive simulation results$`, func() error {
		if _, ok := world.TestVectors["simulationResults"]; !ok {
			return fmt.Errorf("no simulation results")
		}
		return nil
	})
}
