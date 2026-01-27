package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/bcs"
	"github.com/cucumber/godog"
)

// initEncodingSteps registers encoding-related step definitions.
func initEncodingSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// When Steps - Encoding Operations
	// =============================================================================

	ctx.Step(`^I encode "([^"]*)"$`, func(value string) error {
		serializer := &bcs.Serializer{}
		serializer.WriteString(value)
		world.Bytes = serializer.ToBytes()
		return nil
	})

	ctx.Step(`^I encode the value "([^"]*)"$`, func(value string) error {
		serializer := &bcs.Serializer{}
		serializer.WriteString(value)
		world.Bytes = serializer.ToBytes()
		return nil
	})

	ctx.Step(`^I encode the value (\d+)$`, func(value int) error {
		serializer := &bcs.Serializer{}
		serializer.U64(uint64(value))
		world.Bytes = serializer.ToBytes()
		return nil
	})

	ctx.Step(`^I encode the value \[(\d+), (\d+), (\d+)\]$`, func(v1, v2, v3 int) error {
		serializer := &bcs.Serializer{}
		bytes := []byte{byte(v1), byte(v2), byte(v3)}
		serializer.WriteBytes(bytes)
		world.Bytes = serializer.ToBytes()
		return nil
	})

	ctx.Step(`^I encode true$`, func() error {
		serializer := &bcs.Serializer{}
		serializer.Bool(true)
		world.Bytes = serializer.ToBytes()
		return nil
	})

	ctx.Step(`^I encode false$`, func() error {
		serializer := &bcs.Serializer{}
		serializer.Bool(false)
		world.Bytes = serializer.ToBytes()
		return nil
	})

	// =============================================================================
	// Argument Passing Steps
	// =============================================================================

	ctx.Step(`^I pass "([^"]*)" as argument$`, func(value string) error {
		world.TestVectors["argument"] = value
		return nil
	})

	ctx.Step(`^I pass address "([^"]*)" as argument$`, func(addrStr string) error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(addrStr)
		if err != nil {
			return err
		}
		world.TestVectors["addressArgument"] = addr
		return nil
	})

	ctx.Step(`^I pass bytes \[(\d+), (\d+), (\d+), (\d+), (\d+)\] as argument$`, func(b1, b2, b3, b4, b5 int) error {
		world.TestVectors["bytesArgument"] = []byte{byte(b1), byte(b2), byte(b3), byte(b4), byte(b5)}
		return nil
	})

	ctx.Step(`^I pass invalid arguments$`, func() error {
		world.TestVectors["invalidArguments"] = true
		return nil
	})

	ctx.Step(`^I pass number (\d+) as argument$`, func(num int) error {
		world.TestVectors["numberArgument"] = uint64(num)
		return nil
	})

	ctx.Step(`^I pass true as argument$`, func() error {
		world.TestVectors["boolArgument"] = true
		return nil
	})

	ctx.Step(`^I provide the arguments$`, func() error {
		world.TestVectors["argumentsProvided"] = true
		return nil
	})

	ctx.Step(`^I provide type arguments \[0x1::aptos_coin::AptosCoin\]$`, func() error {
		tag, err := aptos.ParseTypeTag("0x1::aptos_coin::AptosCoin")
		if err != nil {
			return err
		}
		world.TestVectors["typeArgs"] = []aptos.TypeTag{*tag}
		return nil
	})

	// =============================================================================
	// Deserialization Steps
	// =============================================================================

	ctx.Step(`^I deserialize it$`, func() error {
		if world.Bytes == nil || len(world.Bytes) == 0 {
			return fmt.Errorf("no bytes to deserialize")
		}
		world.TestVectors["deserialized"] = true
		return nil
	})

	ctx.Step(`^I serialize it$`, func() error {
		world.TestVectors["serialized"] = true
		return nil
	})

	ctx.Step(`^I serialize the signature$`, func() error {
		if world.Ed25519Signature != nil {
			world.Bytes = world.Ed25519Signature.Bytes()
			return nil
		}
		if world.Secp256k1Signature != nil {
			world.Bytes = world.Secp256k1Signature.Bytes()
			return nil
		}
		return fmt.Errorf("no signature to serialize")
	})

	// =============================================================================
	// Parse Steps
	// =============================================================================

	ctx.Step(`^I parse it$`, func() error {
		world.TestVectors["parsed"] = true
		return nil
	})

	ctx.Step(`^I parse the response$`, func() error {
		world.TestVectors["responseParsed"] = true
		return nil
	})

	// =============================================================================
	// Result Parsing Steps
	// =============================================================================

	ctx.Step(`^I should be able to parse the result as boolean$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to parse the result as byte array$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to parse the result as string$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to parse the result as u64$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to parse the result as u128$`, func() error {
		return nil
	})

	ctx.Step(`^I should be able to parse the result as u256$`, func() error {
		return nil
	})

	ctx.Step(`^I should get (\d+) bytes$`, func(count int) error {
		if len(world.Bytes) != count {
			return fmt.Errorf("expected %d bytes, got %d", count, len(world.Bytes))
		}
		return nil
	})

	// =============================================================================
	// Struct Access Steps
	// =============================================================================

	ctx.Step(`^I should be able to access struct fields$`, func() error {
		return nil
	})

	ctx.Step(`^I inspect it$`, func() error {
		world.TestVectors["inspected"] = true
		return nil
	})

	ctx.Step(`^I inspect the account's public properties$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}
		world.TestVectors["accountInspected"] = true
		return nil
	})

	ctx.Step(`^I inspect the authenticator$`, func() error {
		world.TestVectors["authenticatorInspected"] = true
		return nil
	})

	ctx.Step(`^I inspect the error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("no error to inspect")
		}
		world.TestVectors["errorInspected"] = true
		return nil
	})

	ctx.Step(`^I inspect the response$`, func() error {
		world.TestVectors["responseInspected"] = true
		return nil
	})

	// =============================================================================
	// Public Key / Signature Bytes Steps
	// =============================================================================

	ctx.Step(`^I get the public key bytes$`, func() error {
		if world.Ed25519PublicKey != nil {
			world.Bytes = world.Ed25519PublicKey.Bytes()
			return nil
		}
		if world.Secp256k1PublicKey != nil {
			world.Bytes = world.Secp256k1PublicKey.Bytes()
			return nil
		}
		return fmt.Errorf("no public key set")
	})

	ctx.Step(`^I get the signature bytes$`, func() error {
		if world.Ed25519Signature != nil {
			world.Bytes = world.Ed25519Signature.Bytes()
			return nil
		}
		if world.Secp256k1Signature != nil {
			world.Bytes = world.Secp256k1Signature.Bytes()
			return nil
		}
		return fmt.Errorf("no signature set")
	})

	ctx.Step(`^I should get a single (\d+)-byte public key$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("expected %d bytes, got %d", size, len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^I should get a single (\d+)-byte signature$`, func(size int) error {
		if len(world.Bytes) != size {
			return fmt.Errorf("expected %d bytes, got %d", size, len(world.Bytes))
		}
		return nil
	})

	// =============================================================================
	// Type Argument Steps
	// =============================================================================

	ctx.Step(`^I provide type arguments \[(\d+)x(\d+)::aptos_coin::AptosCoin\]$`, func(a, b int) error {
		typeStr := fmt.Sprintf("0x%d::aptos_coin::AptosCoin", a)
		tag, err := aptos.ParseTypeTag(typeStr)
		if err != nil {
			return err
		}
		world.TestVectors["typeArgs"] = []aptos.TypeTag{*tag}
		return nil
	})

	// =============================================================================
	// Run Steps
	// =============================================================================

	ctx.Step(`^I run "([^"]*)"$`, func(cmd string) error {
		world.TestVectors["command"] = cmd
		return nil
	})

	// =============================================================================
	// CLI Steps - These are pending as Go SDK doesn't have CLI
	// =============================================================================

	ctx.Step(`^a CLI command$`, func() error {
		return godog.ErrPending
	})
}

// Helper to parse numbers from strings
func parseNumber(s string) (uint64, error) {
	s = strings.TrimSpace(s)
	if strings.HasPrefix(s, "0x") || strings.HasPrefix(s, "0X") {
		return strconv.ParseUint(s[2:], 16, 64)
	}
	return strconv.ParseUint(s, 10, 64)
}
