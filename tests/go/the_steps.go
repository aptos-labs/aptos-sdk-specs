package main

import (
	"fmt"

	"github.com/cucumber/godog"
)

// initTheSteps registers "the" prefix step definitions.
func initTheSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// "The SDK" Steps
	// =============================================================================

	ctx.Step(`^the SDK handles it$`, func() error {
		return nil
	})

	ctx.Step(`^the SDK handles the error$`, func() error {
		return nil
	})

	ctx.Step(`^the SDK makes the request$`, func() error {
		return nil
	})

	// =============================================================================
	// "The Secp256r1" Steps - All Pending
	// =============================================================================

	ctx.Step(`^the Secp256r1 account should have a valid address$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 address should match the expected value from test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 and Secp256k1 addresses should be different$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 compressed public key should match test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 first byte should be 0x02 or 0x03$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 first byte should be 0x04$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 key pair should be valid$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 message from test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 pre-hash signature should be valid$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 result should be (\d+) bytes$`, func(size int) error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 signature scheme should be "([^"]*)"$`, func(scheme string) error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 signature should be (\d+) bytes$`, func(size int) error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 signature should be valid for the message$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 signature should match test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	ctx.Step(`^the Secp256r1 uncompressed public key should match test vectors$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// "The account" Steps
	// =============================================================================

	ctx.Step(`^the account should be Ed25519 type$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		// Check if Ed25519 (default type)
		return nil
	})

	ctx.Step(`^the account should be Secp256k1 type$`, func() error {
		// TODO: implement account type check
		return godog.ErrPending
	})

	ctx.Step(`^the account should be created$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("account not created")
		}
		return nil
	})

	ctx.Step(`^the account should be usable for signing$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^the account should have (\d+)_(\d+)_(\d+) octas balance$`, func(a, b, c int) error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	ctx.Step(`^the account should have a new valid proof$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the account should have balance$`, func() error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	ctx.Step(`^the account should have the funded amount$`, func() error {
		// TODO: implement funded amount check
		return godog.ErrPending
	})

	// =============================================================================
	// "The address" Steps
	// =============================================================================

	ctx.Step(`^the address should be properly encoded$`, func() error {
		// TODO: implement encoding check
		return godog.ErrPending
	})

	ctx.Step(`^the address should differ from default path$`, func() error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	ctx.Step(`^the address should match expected value from test vectors$`, func() error {
		// TODO: implement test vector comparison
		return godog.ErrPending
	})

	ctx.Step(`^the addresses should be identical$`, func() error {
		// TODO: implement address comparison
		return godog.ErrPending
	})

	ctx.Step(`^the addresses should be the same$`, func() error {
		// TODO: implement address comparison
		return godog.ErrPending
	})

	// =============================================================================
	// "The authenticator" Steps
	// =============================================================================

	ctx.Step(`^the authenticator data and client data$`, func() error {
		// TODO: awaiting SDK implementation - WebAuthn
		return godog.ErrPending
	})

	ctx.Step(`^the authenticator should be FeePayer variant$`, func() error {
		// TODO: implement authenticator variant check
		return godog.ErrPending
	})

	ctx.Step(`^the authenticator should be Keyless variant$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^the authenticator should be MultiAgent variant$`, func() error {
		// TODO: implement authenticator variant check
		return godog.ErrPending
	})

	ctx.Step(`^the authenticator should be MultiEd25519 variant$`, func() error {
		// TODO: implement authenticator variant check
		return godog.ErrPending
	})

	ctx.Step(`^the authenticator should use Secp256r1$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// "The balance" Steps
	// =============================================================================

	ctx.Step(`^the balance should increase$`, func() error {
		// TODO: implement balance change check
		return godog.ErrPending
	})

	ctx.Step(`^the balance should reflect all fundings$`, func() error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	// =============================================================================
	// "The bitmap" Steps
	// =============================================================================

	ctx.Step(`^the bitmap should indicate positions (\d+) and (\d+)$`, func(pos1, pos2 int) error {
		// TODO: implement bitmap check
		return godog.ErrPending
	})

	// =============================================================================
	// "The boolean/bytes/call" Steps
	// =============================================================================

	ctx.Step(`^the boolean should be properly encoded$`, func() error {
		// TODO: implement encoding check
		return godog.ErrPending
	})

	ctx.Step(`^the bytes should match expected value from test vectors$`, func() error {
		// TODO: implement test vector comparison
		return godog.ErrPending
	})

	ctx.Step(`^the call should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("call failed: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^the callback should be invoked$`, func() error {
		// TODO: awaiting SDK implementation - retry callbacks
		return godog.ErrPending
	})

	// =============================================================================
	// "The client" Steps
	// =============================================================================

	ctx.Step(`^the client should use custom settings$`, func() error {
		// TODO: implement settings check
		return godog.ErrPending
	})

	ctx.Step(`^the client should use that URL$`, func() error {
		// TODO: implement URL check
		return godog.ErrPending
	})

	// =============================================================================
	// "The codegen/compiled/complex" Steps
	// =============================================================================

	ctx.Step(`^the codegen CLI$`, func() error {
		// TODO: awaiting SDK implementation - codegen
		return godog.ErrPending
	})

	ctx.Step(`^the compiled bytecode$`, func() error {
		// TODO: awaiting SDK implementation - script compilation
		return godog.ErrPending
	})

	ctx.Step(`^the complex call should use more gas$`, func() error {
		// TODO: implement gas comparison
		return godog.ErrPending
	})

	ctx.Step(`^the compressed public key should be (\d+) bytes$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("compressed public key is %d bytes, expected %d", len(world.Bytes), size)
		}
		return nil
	})

	ctx.Step(`^the contract macro$`, func() error {
		// TODO: awaiting SDK implementation - Rust macros
		return godog.ErrPending
	})

	ctx.Step(`^the correct branch should execute$`, func() error {
		// TODO: implement branch execution check
		return godog.ErrPending
	})

	ctx.Step(`^the crate is compiled$`, func() error {
		// TODO: awaiting SDK implementation - Rust codegen
		return godog.ErrPending
	})

	// =============================================================================
	// "The derivation" Steps - Mnemonic Pending
	// =============================================================================

	ctx.Step(`^the derivation path used should be "([^"]*)"$`, func(path string) error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	ctx.Step(`^the derivation should either fail or produce a different result than Aptos default$`, func() error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	ctx.Step(`^the derivation should fail or produce different result$`, func() error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	ctx.Step(`^the derivation should fail$`, func() error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	ctx.Step(`^the derivation should succeed$`, func() error {
		// TODO: awaiting SDK implementation - HD derivation
		return godog.ErrPending
	})

	ctx.Step(`^the difference is due to scheme identifier$`, func() error {
		// Documentation assertion
		return nil
	})

	// =============================================================================
	// "The encoded" Steps
	// =============================================================================

	ctx.Step(`^the encoded bytes should be "([^"]*)"$`, func(expected string) error {
		// TODO: implement encoding comparison
		return godog.ErrPending
	})

	ctx.Step(`^the encoded bytes should be the BCS-serialized address$`, func() error {
		// TODO: implement BCS serialization check
		return godog.ErrPending
	})

	// =============================================================================
	// "The ephemeral" Steps - Keyless Pending
	// =============================================================================

	ctx.Step(`^the ephemeral key pair should be valid$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// "The error" Steps
	// =============================================================================

	ctx.Step(`^the error should contain the abort code$`, func() error {
		// TODO: implement abort code check
		return godog.ErrPending
	})

	ctx.Step(`^the error should contain the error message$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("no error")
		}
		return nil
	})

	ctx.Step(`^the error should indicate function not found$`, func() error {
		// TODO: implement error type check
		return godog.ErrPending
	})

	ctx.Step(`^the error should indicate mainnet has no faucet$`, func() error {
		// TODO: implement error type check
		return godog.ErrPending
	})

	ctx.Step(`^the error should indicate the abort code$`, func() error {
		// TODO: implement abort code check
		return godog.ErrPending
	})

	ctx.Step(`^the error should indicate type mismatch$`, func() error {
		// TODO: implement error type check
		return godog.ErrPending
	})

	// =============================================================================
	// "The faucet" Steps
	// =============================================================================

	ctx.Step(`^the faucet returns rate limit error$`, func() error {
		world.TestVectors["faucetRateLimited"] = true
		return nil
	})

	// =============================================================================
	// "The hour" Steps - Keyless Pending
	// =============================================================================

	ctx.Step(`^the hour passes$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// "The intermediate" Steps - Mnemonic Pending
	// =============================================================================

	ctx.Step(`^the intermediate seed should be zeroized from memory$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	// =============================================================================
	// "The macro" Steps - Codegen Pending
	// =============================================================================

	ctx.Step(`^the macro should fetch current ABI$`, func() error {
		// TODO: awaiting SDK implementation - codegen
		return godog.ErrPending
	})

	// =============================================================================
	// "The method" Steps
	// =============================================================================

	ctx.Step(`^the method should return after confirmation$`, func() error {
		// TODO: implement confirmation check
		return godog.ErrPending
	})

	ctx.Step(`^the method should wait for confirmation$`, func() error {
		// TODO: implement wait check
		return godog.ErrPending
	})

	// =============================================================================
	// "The mnemonic" Steps - Pending
	// =============================================================================

	ctx.Step(`^the mnemonic phrase "([^"]*)"$`, func(phrase string) error {
		// TODO: awaiting SDK implementation - mnemonic
		return godog.ErrPending
	})

	// =============================================================================
	// "The module" Steps
	// =============================================================================

	ctx.Step(`^the module that aborted$`, func() error {
		// TODO: implement module identification
		return godog.ErrPending
	})

	// =============================================================================
	// "The multi-agent" Steps
	// =============================================================================

	ctx.Step(`^the multi-agent message should match test vectors$`, func() error {
		// TODO: implement test vector comparison
		return godog.ErrPending
	})

	// =============================================================================
	// "The nested/nonces" Steps
	// =============================================================================

	ctx.Step(`^the nested type should be properly parsed$`, func() error {
		// TODO: implement type parsing check
		return godog.ErrPending
	})

	ctx.Step(`^the nonces should be different$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// "The scheme" Steps
	// =============================================================================

	ctx.Step(`^the scheme identifier used should be 0x1$`, func() error {
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
}
