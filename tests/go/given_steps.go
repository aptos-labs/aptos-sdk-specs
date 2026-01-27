package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initGivenSteps registers "Given" step definitions for test setup.
func initGivenSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Known Data Steps
	// =============================================================================

	ctx.Step(`^a known seed from test vectors$`, func() error {
		// Seed from test vectors - mnemonic not supported
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^a known transaction hash for benchmarking$`, func() error {
		// Use a placeholder transaction hash
		world.TestVectors["transactionHash"] = "0x0000000000000000000000000000000000000000000000000000000000000001"
		return nil
	})

	ctx.Step(`^a known account with events$`, func() error {
		// TODO: awaiting SDK implementation - event queries
		return godog.ErrPending
	})

	ctx.Step(`^a known account with fungible assets$`, func() error {
		// TODO: awaiting SDK implementation - fungible asset queries
		return godog.ErrPending
	})

	ctx.Step(`^a known account with tokens$`, func() error {
		// TODO: awaiting SDK implementation - token queries
		return godog.ErrPending
	})

	// =============================================================================
	// Secp256r1 Steps - All Pending
	// =============================================================================

	ctx.Step(`^a known Secp256r1 key pair from test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a known Secp256r1 private key from test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a RawTransaction for Secp256r1 signing$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 public key \(uncompressed\)$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 signature created by the key pair$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 signature in DER format$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a Secp256r1 signature with invalid bytes$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// BLS Steps - All Pending
	// =============================================================================

	ctx.Step(`^a known BLS key pair and message from test vectors$`, func() error {
		// TODO: awaiting SDK implementation - BLS12-381
		return godog.ErrPending
	})

	ctx.Step(`^a PoP from a different key$`, func() error {
		// TODO: awaiting SDK implementation - BLS12-381
		return godog.ErrPending
	})

	// =============================================================================
	// Script Steps
	// =============================================================================

	ctx.Step(`^a Script payload$`, func() error {
		world.TestVectors["scriptPayload"] = true
		return nil
	})

	ctx.Step(`^a Script transaction$`, func() error {
		world.TestVectors["scriptTransaction"] = true
		return nil
	})

	ctx.Step(`^a Script with wrong argument types$`, func() error {
		world.TestVectors["wrongArgumentTypes"] = true
		return nil
	})

	ctx.Step(`^a RawTransaction with Script payload$`, func() error {
		// Create a raw transaction with script payload
		sender := aptos.AccountAddress{}
		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^a SignedTransaction with Script payload$`, func() error {
		// TODO: implement signed script transaction
		return godog.ErrPending
	})

	// =============================================================================
	// Move Steps - All Pending (requires ABI/codegen)
	// =============================================================================

	ctx.Step(`^a Move module with doc comments$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^a Move struct "([^"]*)"$`, func(name string) error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^a Move struct definition$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^Move script source code$`, func() error {
		// TODO: awaiting SDK implementation - script compilation
		return godog.ErrPending
	})

	ctx.Step(`^Move types \(u64, address, vector<u8>\)$`, func() error {
		world.TestVectors["moveTypes"] = []string{"u64", "address", "vector<u8>"}
		return nil
	})

	ctx.Step(`^Move types$`, func() error {
		world.TestVectors["moveTypes"] = []string{"u64", "address", "bool"}
		return nil
	})

	// =============================================================================
	// Request Steps
	// =============================================================================

	ctx.Step(`^a POST request with body$`, func() error {
		world.TestVectors["requestMethod"] = "POST"
		return nil
	})

	// =============================================================================
	// WebAuthn Steps - All Pending
	// =============================================================================

	ctx.Step(`^a WebAuthn assertion signature$`, func() error {
		// TODO: awaiting SDK implementation - WebAuthn
		return godog.ErrPending
	})

	// =============================================================================
	// Keyless Steps - All Pending
	// =============================================================================

	ctx.Step(`^a ZK proof from the prover service$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// Other Givens
	// =============================================================================

	ctx.Step(`^a ledger version older than oldest available$`, func() error {
		world.TestVectors["oldLedgerVersion"] = uint64(1)
		return nil
	})

	ctx.Step(`^a local ABI JSON file$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^a malformed (\d+)-byte signature$`, func(size int) error {
		world.TestVectors["malformedSignature"] = make([]byte, size)
		return nil
	})

	ctx.Step(`^a malformed transaction$`, func() error {
		world.TestVectors["malformedTransaction"] = true
		return nil
	})

	ctx.Step(`^a message and valid (\d+)-of-(\d+) signature$`, func(threshold, total int) error {
		world.TestVectors["threshold"] = threshold
		world.TestVectors["total"] = total
		return nil
	})

	ctx.Step(`^a message and valid signature$`, func() error {
		world.TestVectors["messageAndSignature"] = true
		return nil
	})

	ctx.Step(`^a message signed by first key$`, func() error {
		world.TestVectors["signedByFirstKey"] = true
		return nil
	})

	ctx.Step(`^a message signed by the first Secp256r1 key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^a RawTransaction and secondary addresses from test vectors$`, func() error {
		sender := aptos.AccountAddress{}
		secondary := aptos.AccountAddress{}
		secondary[31] = 0x02

		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["secondaryAddresses"] = []*aptos.AccountAddress{&secondary}
		return nil
	})

	ctx.Step(`^a Rust procedural macro$`, func() error {
		// TODO: awaiting SDK implementation - codegen
		return godog.ErrPending
	})
}
