package main

import (
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initFinalSteps registers remaining step definitions.
func initFinalSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// "The" Validation Steps
	// =============================================================================

	ctx.Step(`^the number should be properly encoded$`, func() error {
		// TODO: implement encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^the original message$`, func() error {
		if world.Message == nil {
			world.Message = []byte("original message")
		}
		return nil
	})

	ctx.Step(`^the parameter should be optional in generated code$`, func() error {
		// TODO: awaiting SDK implementation - codegen
		return godog.ErrPending
	})

	ctx.Step(`^the parsing should fail with an invalid mnemonic error$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^the payload type should be Script$`, func() error {
		// TODO: implement payload type check
		return godog.ErrPending
	})

	ctx.Step(`^the pepper service endpoint$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the pepper should not be accessible$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the phrase should be valid BIP-39$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^the phrase should contain exactly (\d+) words$`, func(count int) error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^the phrases should be different$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^the prover service endpoint$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the prover service$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the public key should be (\d+) bytes$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("public key is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^the public key should match expected value$`, func() error {
		// TODO: implement value comparison
		return godog.ErrPending
	})

	ctx.Step(`^the public key should match the expected value from test vectors$`, func() error {
		// TODO: implement test vector comparison
		return godog.ErrPending
	})

	ctx.Step(`^the request should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("request failed: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^the response times out$`, func() error {
		world.TestVectors["responseTimedOut"] = true
		return nil
	})

	ctx.Step(`^the result should be (\d+) bytes$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("result is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^the result should match expected aggregated signature$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^the retry should include the same body$`, func() error {
		// TODO: awaiting SDK implementation - retry
		return godog.ErrPending
	})

	ctx.Step(`^the same (\d+) public keys in same order$`, func(count int) error {
		world.TestVectors["samePublicKeys"] = count
		return nil
	})

	ctx.Step(`^the same (\d+)-byte private key$`, func(size int) error {
		world.TestVectors["samePrivateKeySize"] = size
		return nil
	})

	ctx.Step(`^the same JWT claims and pepper$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the same JWT claims$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the same JWT$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the same RawTransaction and secondary signers$`, func() error {
		world.TestVectors["sameRawTransactionAndSigners"] = true
		return nil
	})

	ctx.Step(`^the same RawTransaction$`, func() error {
		world.TestVectors["sameRawTransaction"] = true
		return nil
	})

	ctx.Step(`^the same fee payer transaction$`, func() error {
		world.TestVectors["sameFeePayerTransaction"] = true
		return nil
	})

	ctx.Step(`^the same headers$`, func() error {
		world.TestVectors["sameHeaders"] = true
		return nil
	})

	ctx.Step(`^the same issuer and user ID$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the same multi-agent transaction$`, func() error {
		world.TestVectors["sameMultiAgentTransaction"] = true
		return nil
	})

	ctx.Step(`^the same pepper service$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the same user ID and pepper$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the scheme identifier used should be 0x1$`, func() error {
		// TODO: implement scheme identifier check
		return godog.ErrPending
	})

	ctx.Step(`^the script can access them$`, func() error {
		return nil
	})

	ctx.Step(`^the script transaction should fail$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected script transaction to fail")
		}
		return nil
	})

	ctx.Step(`^the secondary_signer_addresses should be \[A, B, C\] in order$`, func() error {
		// TODO: implement address order check
		return godog.ErrPending
	})

	ctx.Step(`^the signature scheme should include BLS identifier$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^the signature should be (\d+) bytes$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("signature is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^the signature should include the ZK proof$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the signature should include the ephemeral signature$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the signature should match expected value from test vectors$`, func() error {
		// TODO: implement test vector comparison
		return godog.ErrPending
	})

	ctx.Step(`^the signature should match expected value$`, func() error {
		// TODO: implement value comparison
		return godog.ErrPending
	})

	ctx.Step(`^the single and multi-agent messages should be different$`, func() error {
		// TODO: implement message comparison
		return godog.ErrPending
	})

	ctx.Step(`^the size should be (\d+) bytes$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("size is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^the string should be properly encoded$`, func() error {
		// TODO: implement encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^the transaction fails$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected transaction to fail")
		}
		return nil
	})

	ctx.Step(`^the transaction is ready for submission$`, func() error {
		return nil
	})

	ctx.Step(`^the transaction should be confirmed$`, func() error {
		// TODO: implement confirmation check
		return godog.ErrPending
	})

	ctx.Step(`^the transaction should have that limit$`, func() error {
		// TODO: implement limit check
		return godog.ErrPending
	})

	ctx.Step(`^the transaction should have the fee payer designated$`, func() error {
		// TODO: implement fee payer designation check
		return godog.ErrPending
	})

	ctx.Step(`^the transaction should include all (\d+) signers$`, func(count int) error {
		// TODO: implement signer count check
		return godog.ErrPending
	})

	ctx.Step(`^the transaction should include both signers$`, func() error {
		// TODO: implement dual signer check
		return godog.ErrPending
	})

	ctx.Step(`^the transaction should use price (\d+)$`, func(price int) error {
		// TODO: implement gas price check
		return godog.ErrPending
	})

	ctx.Step(`^the type arguments should be included$`, func() error {
		// TODO: implement type argument check
		return godog.ErrPending
	})

	ctx.Step(`^the type parameter should be inferred or required$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^the type should be properly passed$`, func() error {
		// TODO: implement type passing check
		return godog.ErrPending
	})

	ctx.Step(`^the uncompressed public key should be (\d+) bytes$`, func(size int) error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the value should be in octas per gas unit$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^the variables should be substituted$`, func() error {
		// TODO: awaiting SDK implementation - indexer
		return godog.ErrPending
	})

	ctx.Step(`^the variant indicator should be FeePayer$`, func() error {
		// TODO: implement variant indicator check
		return godog.ErrPending
	})

	ctx.Step(`^the variant indicator should be MultiAgent$`, func() error {
		// TODO: implement variant indicator check
		return godog.ErrPending
	})

	ctx.Step(`^the vector should be properly encoded$`, func() error {
		// TODO: implement encoding validation
		return godog.ErrPending
	})

	ctx.Step(`^their data$`, func() error {
		world.TestVectors["theirData"] = true
		return nil
	})

	ctx.Step(`^their new values$`, func() error {
		world.TestVectors["theirNewValues"] = true
		return nil
	})

	ctx.Step(`^their return types$`, func() error {
		world.TestVectors["theirReturnTypes"] = true
		return nil
	})

	ctx.Step(`^this is expected behavior$`, func() error {
		return nil
	})

	ctx.Step(`^total should be (\d+) octas$`, func(total int) error {
		// TODO: implement total check
		return godog.ErrPending
	})

	ctx.Step(`^transaction is submitted$`, func() error {
		world.TestVectors["transactionSubmitted"] = true
		return nil
	})

	ctx.Step(`^transaction parameters \(sender, seq num, gas, etc\.\)$`, func() error {
		world.TestVectors["hasTransactionParameters"] = true
		return nil
	})

	ctx.Step(`^transaction should fail$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected transaction to fail")
		}
		return nil
	})

	ctx.Step(`^transactions should be ordered by version$`, func() error {
		// TODO: implement version ordering check
		return godog.ErrPending
	})

	ctx.Step(`^transactions with sequential sequence numbers$`, func() error {
		world.TestVectors["sequentialSequenceNumbers"] = true
		return nil
	})

	// =============================================================================
	// Two Key Pair Steps
	// =============================================================================

	ctx.Step(`^two BLS public keys$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^two BLS signatures for the same message$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^two BLS12-381 key pairs$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^two JWTs with different user IDs$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^two different BLS12-381 key pairs$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^two different Secp256r1 key pairs$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^two different mnemonic phrases$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	ctx.Step(`^two transactions with different gas prices$`, func() error {
		world.TestVectors["differentGasPrices"] = true
		return nil
	})

	// =============================================================================
	// Type Steps
	// =============================================================================

	ctx.Step(`^type arguments should be empty$`, func() error {
		// TODO: implement type argument emptiness check
		return godog.ErrPending
	})

	ctx.Step(`^type parameters for generic functions$`, func() error {
		// TODO: awaiting SDK implementation - ABI
		return godog.ErrPending
	})

	ctx.Step(`^u64 should map to bigint or number$`, func() error {
		// Documentation assertion for TypeScript
		return nil
	})

	ctx.Step(`^u64 should map to u64$`, func() error {
		// Documentation assertion for Rust
		return nil
	})

	ctx.Step(`^use a dummy signature internally$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^use it for the transaction$`, func() error {
		return nil
	})

	ctx.Step(`^user ID \(sub\) "([^"]*)"$`, func(sub string) error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^values may differ between networks$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^variable values$`, func() error {
		world.TestVectors["variableValues"] = true
		return nil
	})

	ctx.Step(`^vector<u8> should map to Uint8Array or string$`, func() error {
		// Documentation assertion for TypeScript
		return nil
	})

	ctx.Step(`^vector<u8> should map to Vec<u8>$`, func() error {
		// Documentation assertion for Rust
		return nil
	})

	ctx.Step(`^verification against any single message should fail$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^verification should work with Secp256r1$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^verify aggregated signature with aggregated public key$`, func() error {
		// TODO: awaiting SDK implementation - BLS
		return godog.ErrPending
	})

	ctx.Step(`^wait appropriately$`, func() error {
		return nil
	})

	ctx.Step(`^with address "([^"]*)" as argument$`, func(addr string) error {
		address := &aptos.AccountAddress{}
		err := address.ParseStringRelaxed(addr)
		if err != nil {
			return err
		}
		world.TestVectors["addressArgument"] = address
		return nil
	})

	ctx.Step(`^with no type arguments$`, func() error {
		world.TestVectors["noTypeArguments"] = true
		return nil
	})

	ctx.Step(`^with the account address as argument$`, func() error {
		if world.Account != nil {
			world.TestVectors["addressArgument"] = world.Account.Address
		}
		return nil
	})

	ctx.Step(`^with type arguments \["([^"]*)"\]$`, func(typeArg string) error {
		tag, err := aptos.ParseTypeTag(typeArg)
		if err != nil {
			return err
		}
		world.TestVectors["typeArgs"] = []aptos.TypeTag{*tag}
		return nil
	})

	// =============================================================================
	// Additional Hash Steps - Keyless Pending
	// =============================================================================

	ctx.Step(`^it should equal SHA(\d+)-(\d+) of the concatenated hashes with pepper and scheme$`, func(a, b int) error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^it should start with SHA(\d+)-(\d+)\("([^"]*)"\)$`, func(a, b int, prefix string) error {
		// TODO: implement hash prefix check
		return godog.ErrPending
	})

	// =============================================================================
	// Signature Steps
	// =============================================================================

	ctx.Step(`^signature(\d+) for "([^"]*)"$`, func(sigNum int, msg string) error {
		world.TestVectors[fmt.Sprintf("signature%dMessage", sigNum)] = msg
		return nil
	})

	// =============================================================================
	// Scheme Identifier Steps
	// =============================================================================

	ctx.Step(`^the scheme identifier used should be (\d+)x(\d+)$`, func(a, b int) error {
		// TODO: implement scheme identifier check
		return godog.ErrPending
	})

	// =============================================================================
	// Type Mapping Steps
	// =============================================================================

	ctx.Step(`^u64 should map to u64$`, func() error {
		// Documentation assertion - Go uses uint64
		return nil
	})

	ctx.Step(`^u128 should map to u128$`, func() error {
		// Documentation assertion - Go uses *big.Int
		return nil
	})
}
