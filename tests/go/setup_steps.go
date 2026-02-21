package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initSetupSteps registers additional setup step definitions.
func initSetupSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Transaction Setup Steps
	// =============================================================================

	ctx.Step(`^a simulation$`, func() error {
		world.TestVectors["simulation"] = true
		return nil
	})

	ctx.Step(`^a submitted transaction with unknown status$`, func() error {
		world.TestVectors["unknownStatus"] = true
		return nil
	})

	ctx.Step(`^a successful funding request$`, func() error {
		world.TestVectors["fundingSuccess"] = true
		return nil
	})

	ctx.Step(`^a transaction I haven't signed yet$`, func() error {
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, _ := aptos.CoinTransferPayload(nil, recipient, 1000)
		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		world.TestVectors["unsignedTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^a transaction accessing non-existent resource$`, func() error {
		world.TestVectors["nonExistentResource"] = true
		return nil
	})

	ctx.Step(`^a transaction builder with defaults$`, func() error {
		world.TestVectors["builderWithDefaults"] = true
		return nil
	})

	ctx.Step(`^a transaction rejected for invalid sequence number$`, func() error {
		world.TestVectors["invalidSequenceNumber"] = true
		return nil
	})

	ctx.Step(`^a transaction requiring (\d+) gas$`, func(gas int) error {
		world.TestVectors["requiredGas"] = uint64(gas)
		return nil
	})

	ctx.Step(`^a transaction requiring (\d+) octas gas$`, func(gas int) error {
		world.TestVectors["requiredGasOctas"] = uint64(gas)
		return nil
	})

	ctx.Step(`^a transaction simulation result$`, func() error {
		world.TestVectors["simulationResult"] = true
		return nil
	})

	ctx.Step(`^a transaction simulation$`, func() error {
		world.TestVectors["simulation"] = true
		return nil
	})

	ctx.Step(`^a transaction submission that times out$`, func() error {
		world.TestVectors["submissionTimeout"] = true
		return nil
	})

	ctx.Step(`^a transaction that emits events$`, func() error {
		world.TestVectors["emitsEvents"] = true
		return nil
	})

	ctx.Step(`^a transaction that modifies resources$`, func() error {
		world.TestVectors["modifiesResources"] = true
		return nil
	})

	ctx.Step(`^a transaction that would abort$`, func() error {
		world.TestVectors["wouldAbort"] = true
		return nil
	})

	ctx.Step(`^a transaction with very low max_gas_amount$`, func() error {
		world.TestVectors["veryLowGas"] = true
		return nil
	})

	ctx.Step(`^a transaction with wrong type arguments$`, func() error {
		world.TestVectors["wrongTypeArgs"] = true
		return nil
	})

	ctx.Step(`^a transaction$`, func() error {
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, _ := aptos.CoinTransferPayload(nil, recipient, 1000)
		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^a transfer exceeding sender's balance$`, func() error {
		world.TestVectors["exceedsBalance"] = true
		return nil
	})

	ctx.Step(`^a transfer transaction$`, func() error {
		world.TestVectors["transferTransaction"] = true
		return nil
	})

	ctx.Step(`^a very complex query$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^a very complex transaction$`, func() error {
		world.TestVectors["complexTransaction"] = true
		return nil
	})

	ctx.Step(`^a very short timeout \((\d+)ms\)$`, func(ms int) error {
		world.TestVectors["timeoutMs"] = ms
		return nil
	})

	// =============================================================================
	// View Function Setup Steps
	// =============================================================================

	ctx.Step(`^a view function "([^"]*)"$`, func(name string) error {
		world.TestVectors["viewFunctionName"] = name
		return nil
	})

	ctx.Step(`^a view function expecting a bool$`, func() error {
		world.TestVectors["expectsBool"] = true
		return nil
	})

	ctx.Step(`^a view function expecting a string$`, func() error {
		world.TestVectors["expectsString"] = true
		return nil
	})

	ctx.Step(`^a view function expecting a u64$`, func() error {
		world.TestVectors["expectsU64"] = true
		return nil
	})

	ctx.Step(`^a view function expecting an address$`, func() error {
		world.TestVectors["expectsAddress"] = true
		return nil
	})

	ctx.Step(`^a view function expecting vector<u8>$`, func() error {
		world.TestVectors["expectsVectorU8"] = true
		return nil
	})

	ctx.Step(`^a view function returning a String$`, func() error {
		world.TestVectors["returnsString"] = true
		return nil
	})

	ctx.Step(`^a view function returning a struct$`, func() error {
		world.TestVectors["returnsStruct"] = true
		return nil
	})

	ctx.Step(`^a view function returning bool$`, func() error {
		world.TestVectors["returnsBool"] = true
		return nil
	})

	ctx.Step(`^a view function returning u64$`, func() error {
		world.TestVectors["returnsU64"] = true
		return nil
	})

	ctx.Step(`^a view function returning vector<u8>$`, func() error {
		world.TestVectors["returnsVectorU8"] = true
		return nil
	})

	ctx.Step(`^a view function that can abort$`, func() error {
		world.TestVectors["canAbort"] = true
		return nil
	})

	ctx.Step(`^a view function with generic type$`, func() error {
		world.TestVectors["genericType"] = true
		return nil
	})

	ctx.Step(`^a view function with multiple type parameters$`, func() error {
		world.TestVectors["multipleTypeParams"] = true
		return nil
	})

	ctx.Step(`^a view function with one type parameter$`, func() error {
		world.TestVectors["oneTypeParam"] = true
		return nil
	})

	// =============================================================================
	// Mnemonic Steps - All Pending
	// =============================================================================

	ctx.Step(`^a valid mnemonic phrase$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	// =============================================================================
	// ABI Setup Steps - All Pending
	// =============================================================================

	ctx.Step(`^abilities \(copy, drop, store, key\)$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^an ABI with entry functions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^an ABI with generic functions and structs$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^an ABI with struct definitions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})
}
