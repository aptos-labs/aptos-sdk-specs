package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initClientSteps registers client configuration step definitions.
func initClientSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Client Configuration Steps
	// =============================================================================

	ctx.Step(`^an Aptos client with auto-gas enabled$`, func() error {
		client, err := NewTestClient(aptos.DevnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		world.TestVectors["autoGasEnabled"] = true
		return nil
	})

	ctx.Step(`^an Aptos client with faucet$`, func() error {
		client, err := NewTestClient(aptos.DevnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		world.TestVectors["faucetEnabled"] = true
		return nil
	})

	ctx.Step(`^configured for testnet faucet$`, func() error {
		client, err := NewTestClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^an unexpected response format$`, func() error {
		world.TestVectors["unexpectedFormat"] = true
		return nil
	})

	// =============================================================================
	// Account Setup Steps
	// =============================================================================

	ctx.Step(`^an Ed25519 sender$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["senderAccount"] = account
		return nil
	})

	ctx.Step(`^an account address with NFTs$`, func() error {
		// TODO: awaiting SDK implementation - NFT queries
		return godog.ErrPending
	})

	ctx.Step(`^an account transaction$`, func() error {
		world.TestVectors["accountTransaction"] = true
		return nil
	})

	ctx.Step(`^an account with (\d+) octas$`, func(octas int) error {
		world.TestVectors["accountOctas"] = uint64(octas)
		return nil
	})

	ctx.Step(`^an account with an NFT$`, func() error {
		// TODO: awaiting SDK implementation - NFT queries
		return godog.ErrPending
	})

	ctx.Step(`^an account with many NFTs$`, func() error {
		// TODO: awaiting SDK implementation - NFT queries
		return godog.ErrPending
	})

	ctx.Step(`^an account with no NFTs$`, func() error {
		// TODO: awaiting SDK implementation - NFT queries
		return godog.ErrPending
	})

	ctx.Step(`^an account with various transaction types$`, func() error {
		world.TestVectors["variousTransactionTypes"] = true
		return nil
	})

	ctx.Step(`^an existing account with (\d+) APT$`, func(apt int) error {
		world.TestVectors["existingAccountAPT"] = uint64(apt)
		return nil
	})

	// =============================================================================
	// Entry Function Steps
	// =============================================================================

	ctx.Step(`^an entry function "([^"]*)"$`, func(name string) error {
		world.TestVectors["entryFunctionName"] = name
		return nil
	})

	ctx.Step(`^an entry function$`, func() error {
		world.TestVectors["hasEntryFunction"] = true
		return nil
	})

	// =============================================================================
	// Event Steps
	// =============================================================================

	ctx.Step(`^an event query result$`, func() error {
		// TODO: awaiting SDK implementation - event queries
		return godog.ErrPending
	})

	ctx.Step(`^an event type$`, func() error {
		world.TestVectors["eventType"] = "0x1::coin::DepositEvent"
		return nil
	})

	// =============================================================================
	// Keyless/Ephemeral Steps - All Pending
	// =============================================================================

	ctx.Step(`^an ephemeral key pair$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^an ephemeral key with (\d+) hour expiry$`, func(hours int) error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^an expired JWT$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^an invalid JWT$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^an invalid ephemeral key$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^audience \(client_id\) "([^"]*)"$`, func(clientID string) error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^different client_ids \(audiences\)$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^different issuers \(Google vs Apple\)$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^different peppers$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^both peppers should be identical$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// BLS Steps - All Pending
	// =============================================================================

	ctx.Step(`^an aggregated signature from N signers$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^an invalid BLS private key \(e\.g\., zero\)$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	// =============================================================================
	// ABI Steps - All Pending
	// =============================================================================

	ctx.Step(`^an ABI with view functions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	// =============================================================================
	// Address Steps
	// =============================================================================

	ctx.Step(`^an invalid address string$`, func() error {
		world.HexString = "invalid_address"
		return nil
	})

	// =============================================================================
	// Arguments Steps
	// =============================================================================

	ctx.Step(`^arguments \["([^"]*)"\]$`, func(args string) error {
		world.TestVectors["arguments"] = args
		return nil
	})

	ctx.Step(`^arguments should be empty$`, func() error {
		// TODO: implement argument validation
		return godog.ErrPending
	})

	// =============================================================================
	// Derivation Steps - All Pending
	// =============================================================================

	ctx.Step(`^derivation path "([^"]*)"$`, func(path string) error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	// =============================================================================
	// Rust/Codegen Steps - All Pending
	// =============================================================================

	ctx.Step(`^appropriate derive macros$`, func() error {
		// TODO: awaiting SDK implementation - codegen
		return godog.ErrPending
	})
}
