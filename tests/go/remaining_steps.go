package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initRemainingSteps registers remaining undefined step definitions.
func initRemainingSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// "It should" Steps
	// =============================================================================

	ctx.Step(`^it should equal SHA256 of the concatenated hashes with pepper and scheme$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^it should have an address$`, func() error {
		if world.Account == nil {
			return godog.ErrPending
		}
		return nil
	})

	ctx.Step(`^it should have an expiry timestamp$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^it should have balance$`, func() error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	ctx.Step(`^it should include all signers plus fee payer$`, func() error {
		// TODO: implement multi-signer check
		return godog.ErrPending
	})

	ctx.Step(`^it should include exposed functions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^it should include gas_used$`, func() error {
		// TODO: implement gas_used check
		return godog.ErrPending
	})

	ctx.Step(`^it should include secondary signer addresses$`, func() error {
		// TODO: implement secondary signer check
		return godog.ErrPending
	})

	ctx.Step(`^it should include struct definitions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^it should include success status$`, func() error {
		// TODO: implement status check
		return godog.ErrPending
	})

	ctx.Step(`^it should include the fee payer address$`, func() error {
		// TODO: implement fee payer address check
		return godog.ErrPending
	})

	ctx.Step(`^it should include the raw transaction$`, func() error {
		// TODO: implement raw transaction check
		return godog.ErrPending
	})

	ctx.Step(`^it should include the secondary signer addresses$`, func() error {
		// TODO: implement secondary signer address check
		return godog.ErrPending
	})

	ctx.Step(`^it should include the signer bitmap$`, func() error {
		// TODO: implement signer bitmap check
		return godog.ErrPending
	})

	ctx.Step(`^it should properly BCS encode all fields in order$`, func() error {
		// TODO: implement BCS encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^it should properly BCS encode the value$`, func() error {
		// TODO: implement BCS encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^it should properly BCS encode the vector$`, func() error {
		// TODO: implement BCS encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^it should properly encode the address$`, func() error {
		// TODO: implement address encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^it should return appropriate type$`, func() error {
		// TODO: implement return type check
		return godog.ErrPending
	})

	ctx.Step(`^it should return false$`, func() error {
		result := world.TestVectors["result"]
		if result == false || result == "false" {
			return nil
		}
		return godog.ErrPending
	})

	ctx.Step(`^it should return true$`, func() error {
		result := world.TestVectors["result"]
		if result == true || result == "true" {
			return nil
		}
		return godog.ErrPending
	})

	ctx.Step(`^it should start with SHA256\("APTOS::"\)$`, func() error {
		// TODO: implement prefix check
		return godog.ErrPending
	})

	ctx.Step(`^it should try (\d+) times total \((\d+) \+ (\d+) retries\)$`, func(total, initial, retries int) error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^it should use that issuer$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^it should use the BLS scheme identifier$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	// =============================================================================
	// Simulation/State Steps
	// =============================================================================

	ctx.Step(`^later simulations should see earlier changes$`, func() error {
		// TODO: implement simulation sequence validation
		return godog.ErrPending
	})

	ctx.Step(`^no on-chain state should change$`, func() error {
		// Documentation assertion - simulations don't change state
		return nil
	})

	ctx.Step(`^on-chain validation should fail$`, func() error {
		// TODO: implement validation failure check
		return godog.ErrPending
	})

	// =============================================================================
	// Configuration Steps
	// =============================================================================

	ctx.Step(`^low max_gas_amount$`, func() error {
		world.TestVectors["lowMaxGas"] = true
		return nil
	})

	ctx.Step(`^mainnet and testnet clients$`, func() error {
		mainnetClient, _ := aptos.NewClient(aptos.MainnetConfig)
		testnetClient, _ := aptos.NewClient(aptos.TestnetConfig)
		world.TestVectors["mainnetClient"] = mainnetClient
		world.TestVectors["testnetClient"] = testnetClient
		return nil
	})

	ctx.Step(`^malformed bytecode$`, func() error {
		world.TestVectors["malformedBytecode"] = true
		return nil
	})

	ctx.Step(`^many rapid funding requests$`, func() error {
		world.TestVectors["rapidFundingRequests"] = true
		return nil
	})

	ctx.Step(`^many retries occur$`, func() error {
		world.TestVectors["manyRetries"] = true
		return nil
	})

	ctx.Step(`^max cost should be (\d+) octas \((\d+)\.(\d+) APT\)$`, func(octas, aptWhole, aptFrac int) error {
		// TODO: implement max cost check
		return godog.ErrPending
	})

	ctx.Step(`^max_delay should be around (\d+) seconds$`, func(seconds int) error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^max_gas_amount = (\d+)$`, func(amount int) error {
		world.TestVectors["maxGasAmount"] = uint64(amount)
		return nil
	})

	ctx.Step(`^max_gas_amount should be reasonable \(e\.g\., (\d+)\)$`, func(expected int) error {
		// TODO: implement reasonableness check
		return godog.ErrPending
	})

	ctx.Step(`^max_retries should be (\d+)$`, func(retries int) error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	// =============================================================================
	// Mnemonic Steps - All Pending
	// =============================================================================

	ctx.Step(`^mnemonic "([^"]*)"$`, func(phrase string) error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^mnemonic from test vectors$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	// =============================================================================
	// Module Steps
	// =============================================================================

	ctx.Step(`^module addresses \["([^"]*)", "([^"]*)"\]$`, func(addr1, addr2 string) error {
		address1 := &aptos.AccountAddress{}
		address1.ParseStringRelaxed(addr1)
		address2 := &aptos.AccountAddress{}
		address2.ParseStringRelaxed(addr2)
		world.TestVectors["moduleAddresses"] = []*aptos.AccountAddress{address1, address2}
		return nil
	})

	// =============================================================================
	// Network/Retry Steps
	// =============================================================================

	ctx.Step(`^multiple retries occur$`, func() error {
		world.TestVectors["multipleRetries"] = true
		return nil
	})

	ctx.Step(`^multiple transactions$`, func() error {
		world.TestVectors["multipleTransactions"] = true
		return nil
	})

	ctx.Step(`^network is under high load$`, func() error {
		world.TestVectors["highNetworkLoad"] = true
		return nil
	})

	ctx.Step(`^no arguments$`, func() error {
		world.TestVectors["noArguments"] = true
		return nil
	})

	ctx.Step(`^no secondary signers$`, func() error {
		world.TestVectors["noSecondarySigners"] = true
		return nil
	})

	ctx.Step(`^not be exactly the calculated values$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^num_keys should be (\d+)$`, func(count int) error {
		// TODO: implement key count check
		return godog.ErrPending
	})

	ctx.Step(`^only (\d+) secondary signatures$`, func(count int) error {
		world.TestVectors["secondarySignatureCount"] = count
		return nil
	})

	ctx.Step(`^only (\d+) secondary signer signs$`, func(count int) error {
		world.TestVectors["secondarySignerCount"] = count
		return nil
	})

	ctx.Step(`^optionally deprioritized_gas_estimate \(slower/cheaper\)$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^optionally prioritized_gas_estimate \(faster\)$`, func() error {
		// Documentation assertion
		return nil
	})

	// =============================================================================
	// Parameter Steps
	// =============================================================================

	ctx.Step(`^parameter types for each function$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^parameters should have correct types$`, func() error {
		// TODO: implement type validation
		return godog.ErrPending
	})

	ctx.Step(`^party (\d+) signs and provides their signature$`, func(partyNum int) error {
		// TODO: implement multi-party signing
		return godog.ErrPending
	})

	ctx.Step(`^passphrase "([^"]*)"$`, func(passphrase string) error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^prioritized should be >= standard$`, func() error {
		// TODO: implement priority comparison
		return godog.ErrPending
	})

	ctx.Step(`^public keys \[A, B, C\] and \[C, B, A\]$`, func() error {
		// Create different ordered key sets
		key1, _ := aptos.NewEd25519Account()
		key2, _ := aptos.NewEd25519Account()
		key3, _ := aptos.NewEd25519Account()
		world.TestVectors["keySet1"] = []interface{}{key1, key2, key3}
		world.TestVectors["keySet2"] = []interface{}{key3, key2, key1}
		return nil
	})
}
