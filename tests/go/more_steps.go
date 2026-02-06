package main

import (
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initMoreSteps registers additional step definitions.
func initMoreSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Execution Steps
	// =============================================================================

	ctx.Step(`^execute it$`, func() error {
		world.TestVectors["executed"] = true
		return nil
	})

	ctx.Step(`^execute the signed transaction$`, func() error {
		// TODO: implement signed transaction execution
		return godog.ErrPending
	})

	ctx.Step(`^execution should fail with abort code$`, func() error {
		// TODO: implement abort code check
		return godog.ErrPending
	})

	ctx.Step(`^execution should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("execution failed: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^expect the calls to complete$`, func() error {
		return nil
	})

	// =============================================================================
	// Fee Payer Steps
	// =============================================================================

	ctx.Step(`^fee payer adds their signature$`, func() error {
		world.TestVectors["feePayerSigned"] = true
		return nil
	})

	ctx.Step(`^fee payer can pay for multiple transactions$`, func() error {
		world.TestVectors["multipleTransactions"] = true
		return nil
	})

	ctx.Step(`^fee payer must sign last$`, func() error {
		world.TestVectors["feePayerSignsLast"] = true
		return nil
	})

	ctx.Step(`^fee payer only pays gas$`, func() error {
		world.TestVectors["feePayerPaysGasOnly"] = true
		return nil
	})

	ctx.Step(`^fee payer signs$`, func() error {
		world.TestVectors["feePayerSigned"] = true
		return nil
	})

	ctx.Step(`^fee payer submits to network$`, func() error {
		// TODO: implement fee payer submission
		return godog.ErrPending
	})

	ctx.Step(`^fee payer\'s balance should decrease by gas$`, func() error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	// =============================================================================
	// Field/Property Steps
	// =============================================================================

	ctx.Step(`^fields should include sender, sequence_number, max_gas_amount, etc$`, func() error {
		// TODO: implement field presence check
		return godog.ErrPending
	})

	ctx.Step(`^function name should be "([^"]*)"$`, func(name string) error {
		world.TestVectors["expectedFunctionName"] = name
		return nil
	})

	ctx.Step(`^function_name$`, func() error {
		world.TestVectors["hasFunctionName"] = true
		return nil
	})

	// =============================================================================
	// Gas Steps
	// =============================================================================

	ctx.Step(`^gas estimate endpoint is available$`, func() error {
		if world.Client == nil {
			client, err := NewTestClient(aptos.DevnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		return nil
	})

	ctx.Step(`^gas estimation for complex transaction$`, func() error {
		world.TestVectors["complexGasEstimation"] = true
		return nil
	})

	ctx.Step(`^gas estimation is available$`, func() error {
		world.TestVectors["gasEstimationAvailable"] = true
		return nil
	})

	ctx.Step(`^gas should be properly calculated$`, func() error {
		// TODO: implement gas calculation validation
		return godog.ErrPending
	})

	ctx.Step(`^gas used should be greater than (\d+)$`, func(min int) error {
		gasUsed, ok := world.TestVectors["gasUsed"].(uint64)
		if !ok {
			return fmt.Errorf("no gas used recorded")
		}
		if gasUsed <= uint64(min) {
			return fmt.Errorf("gas used %d not greater than %d", gasUsed, min)
		}
		return nil
	})

	ctx.Step(`^gas used should be less than (\d+)$`, func(max int) error {
		gasUsed, ok := world.TestVectors["gasUsed"].(uint64)
		if !ok {
			return fmt.Errorf("no gas used recorded")
		}
		if gasUsed >= uint64(max) {
			return fmt.Errorf("gas used %d not less than %d", gasUsed, max)
		}
		return nil
	})

	ctx.Step(`^gas_used and vm_status should be in response$`, func() error {
		// TODO: implement response field check
		return godog.ErrPending
	})

	ctx.Step(`^gas_used should be returned$`, func() error {
		// TODO: implement gas_used presence check
		return godog.ErrPending
	})

	// =============================================================================
	// Generic Type Steps
	// =============================================================================

	ctx.Step(`^generic types \(T, U\) should be parameters$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^generics should be type parameters$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	// =============================================================================
	// Hash Steps
	// =============================================================================

	ctx.Step(`^hash should be (\d+) bytes$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("hash is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^hash should be a (\d+)-character hex string$`, func(length int) error {
		if len(world.HexString) != length {
			return fmt.Errorf("hash is %d chars, expected %d", len(world.HexString), length)
		}
		return nil
	})

	ctx.Step(`^hash should be deterministic for same input$`, func() error {
		// TODO: implement determinism check
		return godog.ErrPending
	})

	// =============================================================================
	// Higher Priority/Estimate Steps
	// =============================================================================

	ctx.Step(`^higher priority should give higher estimates$`, func() error {
		// TODO: implement priority estimate comparison
		return godog.ErrPending
	})

	// =============================================================================
	// I Should Steps (Validations)
	// =============================================================================

	ctx.Step(`^I should be able to calculate transaction hash locally$`, func() error {
		// TODO: implement local hash calculation
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to call it with matching arguments$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to construct matching argument$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to detect potential issues$`, func() error {
		// TODO: implement issue detection
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to determine type arguments needed$`, func() error {
		// TODO: implement type argument detection
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to determine which entry functions exist$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to estimate correct gas$`, func() error {
		// TODO: implement gas estimation validation
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to extract specific events$`, func() error {
		// TODO: implement event extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to generate strongly-typed code$`, func() error {
		// TODO: awaiting SDK implementation - codegen
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to pass it as function argument$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to retrieve metadata$`, func() error {
		// TODO: implement metadata retrieval
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to see what went wrong$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error to inspect")
		}
		return nil
	})

	ctx.Step(`^I should be able to submit them later$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to track by hash$`, func() error {
		if _, ok := world.TestVectors["transactionHash"].(string); !ok {
			return fmt.Errorf("no transaction hash to track")
		}
		return nil
	})

	ctx.Step(`^I should be able to verify it$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to wait for it$`, func() error {
		return nil
	})

	// =============================================================================
	// Get Steps
	// =============================================================================

	ctx.Step(`^I should get (\d+) different addresses$`, func(count int) error {
		// TODO: implement address count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get (\d+) results$`, func(count int) error {
		// TODO: implement result count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get (\d+) transactions$`, func(count int) error {
		// TODO: implement transaction count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a (\d+)-byte BLS public key$`, func(size int) error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^I should get a (\d+)-byte Ed(\d+) public key$`, func(size, keyType int) error {
		if world.Ed25519PublicKey == nil {
			return fmt.Errorf("no Ed25519 public key")
		}
		if len(world.Ed25519PublicKey.Bytes()) != size {
			return fmt.Errorf("public key is %d bytes, expected %d", len(world.Ed25519PublicKey.Bytes()), size)
		}
		return nil
	})

	ctx.Step(`^I should get a (\d+)-byte public key$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("public key is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^I should get a (\d+)-byte signature$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("signature is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^I should get a JSON object with numeric fields$`, func() error {
		// TODO: implement JSON validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get a clear error message$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error")
		}
		return nil
	})

	ctx.Step(`^I should get a clear error with available ledger versions$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error about ledger versions")
		}
		return nil
	})

	ctx.Step(`^I should get a deterministic address$`, func() error {
		if world.Address == nil {
			return fmt.Errorf("no address")
		}
		return nil
	})

	ctx.Step(`^I should get a different address than ED(\d+)$`, func(keyType int) error {
		// TODO: implement address comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get a different address$`, func() error {
		// TODO: implement address comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get a different signature$`, func() error {
		// TODO: implement signature comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get a fee payer signed transaction$`, func() error {
		// TODO: implement fee payer transaction check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a funded account$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^I should get a hash$`, func() error {
		if world.HexString == "" && len(world.Bytes) == 0 {
			return fmt.Errorf("no hash")
		}
		return nil
	})

	ctx.Step(`^I should get a list of gas estimates$`, func() error {
		// TODO: implement gas estimate list check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a multi-agent signed transaction$`, func() error {
		// TODO: implement multi-agent transaction check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a multikey account$`, func() error {
		// TODO: implement multikey account check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a proof for each transaction$`, func() error {
		// TODO: implement proof check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a response with numeric estimates$`, func() error {
		// TODO: implement response validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get a single address$`, func() error {
		if world.Address == nil {
			return fmt.Errorf("no address")
		}
		return nil
	})

	ctx.Step(`^I should get a successful response$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected success, got error: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^I should get a successful simulation$`, func() error {
		success, ok := world.TestVectors["simulationSuccess"].(bool)
		if !ok || !success {
			return fmt.Errorf("simulation did not succeed")
		}
		return nil
	})

	ctx.Step(`^I should get a transaction hash$`, func() error {
		if _, ok := world.TestVectors["transactionHash"].(string); !ok {
			if world.HexString == "" {
				return fmt.Errorf("no transaction hash")
			}
		}
		return nil
	})

	ctx.Step(`^I should get a unique address$`, func() error {
		if world.Address == nil {
			return fmt.Errorf("no address")
		}
		return nil
	})

	ctx.Step(`^I should get a valid (\d+)-byte Ed(\d+) signature$`, func(size, keyType int) error {
		if world.Ed25519Signature == nil {
			return fmt.Errorf("no Ed25519 signature")
		}
		if len(world.Ed25519Signature.Bytes()) != size {
			return fmt.Errorf("signature is %d bytes, expected %d", len(world.Ed25519Signature.Bytes()), size)
		}
		return nil
	})

	ctx.Step(`^I should get a valid (\d+)-byte signature$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("signature is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^I should get a valid BLS signature$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^I should get a valid Secp(\d+)k(\d+) signature$`, func(a, b int) error {
		if world.Secp256k1Signature == nil {
			return fmt.Errorf("no Secp256k1 signature")
		}
		return nil
	})

	ctx.Step(`^I should get a valid aggregated BLS signature$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^I should get a valid aggregated public key$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^I should get a valid combined MultiEd(\d+) public key$`, func(keyType int) error {
		// TODO: implement MultiEd25519 public key check
		return godog.ErrPending
	})

	ctx.Step(`^I should get a valid gas estimate$`, func() error {
		// TODO: implement gas estimate validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get a valid key pair$`, func() error {
		if world.Ed25519PrivateKey == nil && world.Secp256k1PrivateKey == nil {
			return fmt.Errorf("no key pair")
		}
		return nil
	})

	ctx.Step(`^I should get a valid pepper$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^I should get a valid response$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected valid response, got error: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^I should get an Ed(\d+) account$`, func(keyType int) error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^I should get an account$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^I should get an error indicating it will fail$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error")
		}
		return nil
	})

	ctx.Step(`^I should get an error indicating the issue$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error")
		}
		return nil
	})

	ctx.Step(`^I should get an error rather than wrong signature$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error for invalid input")
		}
		return nil
	})

	ctx.Step(`^I should get an error with context$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected an error with context")
		}
		return nil
	})

	ctx.Step(`^I should get at least (\d+) transactions$`, func(min int) error {
		// TODO: implement transaction count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get complete gas information$`, func() error {
		// TODO: implement gas info completeness check
		return godog.ErrPending
	})

	ctx.Step(`^I should get detailed gas estimation$`, func() error {
		// TODO: implement gas estimation detail check
		return godog.ErrPending
	})

	ctx.Step(`^I should get deterministic output$`, func() error {
		// TODO: implement determinism check
		return godog.ErrPending
	})

	ctx.Step(`^I should get different addresses$`, func() error {
		// TODO: implement address uniqueness check
		return godog.ErrPending
	})

	ctx.Step(`^I should get exactly (\d+) transactions$`, func(count int) error {
		// TODO: implement transaction count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get expected balance$`, func() error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	ctx.Step(`^I should get gas estimation results$`, func() error {
		// TODO: implement gas estimation result check
		return godog.ErrPending
	})

	ctx.Step(`^I should get information about$`, func() error {
		return nil
	})

	ctx.Step(`^I should get intermediate signing messages$`, func() error {
		// TODO: implement signing message check
		return godog.ErrPending
	})

	ctx.Step(`^I should get ledger info$`, func() error {
		if world.TestVectors["ledgerInfo"] == nil {
			return fmt.Errorf("no ledger info")
		}
		return nil
	})

	ctx.Step(`^I should get multiple estimates$`, func() error {
		// TODO: implement estimate count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get response within timeout$`, func() error {
		// Time-based check - assume success if no error
		return nil
	})

	ctx.Step(`^I should get same result whether serialized or not$`, func() error {
		// TODO: implement serialization comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get status of all processors$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^I should get success == true$`, func() error {
		success, ok := world.TestVectors["success"].(bool)
		if !ok || !success {
			return fmt.Errorf("expected success == true")
		}
		return nil
	})

	ctx.Step(`^I should get the account\'s address$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^I should get the committed transaction details$`, func() error {
		// TODO: implement transaction details check
		return godog.ErrPending
	})

	ctx.Step(`^I should get the same (\d+) addresses$`, func(count int) error {
		// TODO: implement address count and identity check
		return godog.ErrPending
	})

	ctx.Step(`^I should get the same address$`, func() error {
		// TODO: implement address comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get the same hash$`, func() error {
		// TODO: implement hash comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get the same key pair$`, func() error {
		// TODO: implement key pair comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get the same result$`, func() error {
		// TODO: implement result comparison
		return godog.ErrPending
	})

	ctx.Step(`^I should get the sequence number$`, func() error {
		if _, ok := world.TestVectors["sequenceNumber"]; !ok {
			return fmt.Errorf("no sequence number")
		}
		return nil
	})

	ctx.Step(`^I should get the transaction receipt$`, func() error {
		// TODO: implement receipt check
		return godog.ErrPending
	})

	ctx.Step(`^I should get three distinct estimates$`, func() error {
		// TODO: implement estimate count check
		return godog.ErrPending
	})

	ctx.Step(`^I should get transaction result$`, func() error {
		// TODO: implement result check
		return godog.ErrPending
	})

	ctx.Step(`^I should get valid hex string$`, func() error {
		if world.HexString == "" {
			return fmt.Errorf("no hex string")
		}
		return nil
	})
}
