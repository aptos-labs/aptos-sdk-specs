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

	// =============================================================================
	// Message Steps
	// =============================================================================

	ctx.Step(`^a message to sign$`, func() error {
		world.Message = []byte("test message to sign")
		return nil
	})

	ctx.Step(`^a message$`, func() error {
		world.Message = []byte("test message")
		return nil
	})

	// =============================================================================
	// Mnemonic Steps - All Pending
	// =============================================================================

	ctx.Step(`^a mnemonic phrase with (\d+) words$`, func(wordCount int) error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^a mnemonic phrase with valid words but wrong checksum$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^a mnemonic phrase$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	// =============================================================================
	// Module/ABI Steps
	// =============================================================================

	ctx.Step(`^a module address and name "([^"]*)"$`, func(name string) error {
		world.TestVectors["moduleName"] = name
		return nil
	})

	ctx.Step(`^a module with public \(non-entry\) functions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^a non-existent module address$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0xFF
		world.TestVectors["moduleAddress"] = &addr
		return nil
	})

	// =============================================================================
	// Multi-Agent Steps
	// =============================================================================

	ctx.Step(`^a multi-agent authenticator$`, func() error {
		world.TestVectors["multiAgentAuthenticator"] = true
		return nil
	})

	ctx.Step(`^a multi-agent transaction from test vectors$`, func() error {
		// Set up from test vectors
		world.TestVectors["multiAgentTransaction"] = true
		return nil
	})

	ctx.Step(`^a multi-agent transaction$`, func() error {
		world.TestVectors["multiAgentTransaction"] = true
		return nil
	})

	// =============================================================================
	// Request/Network Steps
	// =============================================================================

	ctx.Step(`^a network error during estimation$`, func() error {
		world.TestVectors["networkError"] = true
		return nil
	})

	ctx.Step(`^a request that always fails$`, func() error {
		world.TestVectors["alwaysFails"] = true
		return nil
	})

	ctx.Step(`^a request that fails after retries$`, func() error {
		world.TestVectors["failsAfterRetries"] = true
		return nil
	})

	ctx.Step(`^a request that fails to connect$`, func() error {
		world.TestVectors["failsToConnect"] = true
		return nil
	})

	ctx.Step(`^a request that fails twice then succeeds$`, func() error {
		world.TestVectors["failsTwiceThenSucceeds"] = true
		return nil
	})

	ctx.Step(`^a request that returns HTTP (\d+)$`, func(statusCode int) error {
		world.TestVectors["httpStatus"] = statusCode
		return nil
	})

	ctx.Step(`^a request that times out$`, func() error {
		world.TestVectors["timesOut"] = true
		return nil
	})

	// =============================================================================
	// Script Argument Steps
	// =============================================================================

	ctx.Step(`^a script argument of type address$`, func() error {
		world.TestVectors["scriptArgType"] = "address"
		return nil
	})

	ctx.Step(`^a script argument of type bool$`, func() error {
		world.TestVectors["scriptArgType"] = "bool"
		return nil
	})

	ctx.Step(`^a script argument of type string$`, func() error {
		world.TestVectors["scriptArgType"] = "string"
		return nil
	})

	ctx.Step(`^a script argument of type u64$`, func() error {
		world.TestVectors["scriptArgType"] = "u64"
		return nil
	})

	ctx.Step(`^a script argument of type vector<u8>$`, func() error {
		world.TestVectors["scriptArgType"] = "vector<u8>"
		return nil
	})

	ctx.Step(`^a script expecting \(address, u64, vector<u8>\)$`, func() error {
		world.TestVectors["scriptExpects"] = []string{"address", "u64", "vector<u8>"}
		return nil
	})

	ctx.Step(`^a script that calls abort$`, func() error {
		world.TestVectors["scriptAborts"] = true
		return nil
	})

	ctx.Step(`^a script that transfers to multiple recipients$`, func() error {
		world.TestVectors["multiRecipientScript"] = true
		return nil
	})

	ctx.Step(`^a script with conditional logic$`, func() error {
		world.TestVectors["conditionalScript"] = true
		return nil
	})

	ctx.Step(`^a script with expensive operations$`, func() error {
		world.TestVectors["expensiveScript"] = true
		return nil
	})

	// =============================================================================
	// Account/Signer Steps
	// =============================================================================

	ctx.Step(`^a secondary signer account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.TestVectors["secondarySigner"] = account
		return nil
	})

	ctx.Step(`^a sender account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.TestVectors["senderAccount"] = account
		return nil
	})

	ctx.Step(`^a sender who wants sponsored transaction$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.TestVectors["sponsoredSender"] = account
		return nil
	})

	ctx.Step(`^a signing account$`, func() error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}
		return nil
	})

	// =============================================================================
	// Fee Payer Steps
	// =============================================================================

	ctx.Step(`^a partially signed fee payer transaction from sender$`, func() error {
		world.TestVectors["partiallySignedFeePayer"] = true
		return nil
	})

	ctx.Step(`^a signed fee payer transaction$`, func() error {
		world.TestVectors["signedFeePayer"] = true
		return nil
	})

	// =============================================================================
	// Miscellaneous Steps
	// =============================================================================

	ctx.Step(`^a short timeout$`, func() error {
		world.TestVectors["shortTimeout"] = true
		return nil
	})

	ctx.Step(`^a signature from different keys$`, func() error {
		world.TestVectors["differentKeys"] = true
		return nil
	})

	ctx.Step(`^a signature with only (\d+) signer$`, func(count int) error {
		world.TestVectors["signerCount"] = count
		return nil
	})

	ctx.Step(`^a simple operation like transfer$`, func() error {
		world.TestVectors["simpleTransfer"] = true
		return nil
	})

	ctx.Step(`^a simple transfer$`, func() error {
		world.TestVectors["simpleTransfer"] = true
		return nil
	})

	ctx.Step(`^a simulated and executed transaction$`, func() error {
		world.TestVectors["simulatedAndExecuted"] = true
		return nil
	})
}
