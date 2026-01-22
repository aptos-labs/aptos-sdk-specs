package main

import (
	"context"
	"crypto/rand"
	"fmt"
	"strings"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initAddressSteps(ctx *godog.ScenarioContext, world *World) {
	// Given steps
	ctx.Step(`^a valid hex address string "([^"]*)"$`, func(hex string) error {
		world.HexString = hex
		return nil
	})

	ctx.Step(`^the address string "([^"]*)"$`, func(address string) error {
		world.HexString = address
		return nil
	})

	ctx.Step(`^a short address "([^"]*)"$`, func(address string) error {
		world.HexString = address
		return nil
	})

	ctx.Step(`^a full 64-character hex address$`, func() error {
		world.HexString = "0x0000000000000000000000000000000000000000000000000000000000000001"
		return nil
	})

	ctx.Step(`^32 random bytes$`, func() error {
		world.Bytes = make([]byte, 32)
		_, err := rand.Read(world.Bytes)
		return err
	})

	ctx.Step(`^an invalid hex string "([^"]*)"$`, func(hex string) error {
		world.HexString = hex
		return nil
	})

	ctx.Step(`^test vectors from addresses\.json$`, func() error {
		vectors, err := GetAddressParsingVectors()
		if err != nil {
			return err
		}
		world.TestVectors["address_parsing"] = vectors
		return nil
	})

	ctx.Step(`^the framework address constant$`, func() error {
		addr := aptos.AccountOne
		world.Address = &addr
		return nil
	})

	ctx.Step(`^the zero address constant$`, func() error {
		addr := aptos.AccountZero
		world.Address = &addr
		return nil
	})

	ctx.Step(`^two addresses "([^"]*)" and "([^"]*)"$`, func(addr1, addr2 string) error {
		a1 := &aptos.AccountAddress{}
		if err := a1.ParseStringRelaxed(addr1); err != nil {
			return err
		}
		a2 := &aptos.AccountAddress{}
		if err := a2.ParseStringRelaxed(addr2); err != nil {
			return err
		}
		world.Addresses = []*aptos.AccountAddress{a1, a2}
		return nil
	})

	// When steps
	ctx.Step(`^I parse the address$`, func() error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(world.HexString)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Address = addr
		world.ClearError()
		return nil
	})

	ctx.Step(`^I parse the address string$`, func() error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(world.HexString)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Address = addr
		world.ClearError()
		return nil
	})

	ctx.Step(`^I parse it as an AccountAddress$`, func() error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(world.HexString)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Address = addr
		world.ClearError()
		return nil
	})

	ctx.Step(`^I create an AccountAddress from the bytes$`, func() error {
		if len(world.Bytes) != 32 {
			world.SetError(fmt.Errorf("expected 32 bytes, got %d", len(world.Bytes)))
			return nil
		}
		addr := &aptos.AccountAddress{}
		copy(addr[:], world.Bytes)
		world.Address = addr
		world.ClearError()
		return nil
	})

	ctx.Step(`^I try to parse it as an address$`, func() error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(world.HexString)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.Address = addr
		world.ClearError()
		return nil
	})

	ctx.Step(`^I format the address as a string$`, func() error {
		world.HexString = world.Address.String()
		return nil
	})

	ctx.Step(`^I format it as a full hex string$`, func() error {
		world.HexString = world.Address.StringLong()
		return nil
	})

	ctx.Step(`^I format it as a short string$`, func() error {
		world.HexString = world.Address.String()
		return nil
	})

	ctx.Step(`^I get the raw bytes$`, func() error {
		world.Bytes = world.Address[:]
		return nil
	})

	ctx.Step(`^I BCS serialize the address$`, func() error {
		world.Bytes = world.Address[:]
		return nil
	})

	ctx.Step(`^I compare them for equality$`, func() error {
		world.Result = *world.Addresses[0] == *world.Addresses[1]
		return nil
	})

	ctx.Step(`^I run all parsing test vectors$`, func() error {
		vectors := world.TestVectors["address_parsing"].([]AddressVector)
		type Result struct {
			Name   string
			Passed bool
			Error  string
		}
		var results []Result

		for _, v := range vectors {
			addr := &aptos.AccountAddress{}
			err := addr.ParseStringRelaxed(v.Input)
			if err != nil {
				results = append(results, Result{Name: v.Name, Passed: false, Error: err.Error()})
				continue
			}

			fullHex := addr.StringLong()
			shortString := addr.String()

			passed := strings.EqualFold(fullHex, v.Expected.FullHex) &&
				strings.EqualFold(shortString, v.Expected.ShortString)

			results = append(results, Result{Name: v.Name, Passed: passed})
		}

		world.Result = results
		return nil
	})

	// Then steps
	ctx.Step(`^I should get a valid AccountAddress$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected no error, got: %v", world.Error)
		}
		if world.Address == nil {
			return fmt.Errorf("expected address to be set")
		}
		return nil
	})

	ctx.Step(`^the address should be valid$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected no error, got: %v", world.Error)
		}
		if world.Address == nil {
			return fmt.Errorf("expected address to be set")
		}
		return nil
	})

	ctx.Step(`^parsing should fail$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected error, but parsing succeeded")
		}
		return nil
	})

	ctx.Step(`^parsing should fail with an error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected error, but parsing succeeded")
		}
		return nil
	})

	ctx.Step(`^it should fail with an InvalidAddress error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected error, but parsing succeeded")
		}
		return nil
	})

	ctx.Step(`^the full hex representation should be "([^"]*)"$`, func(expected string) error {
		actual := world.Address.StringLong()
		if !strings.EqualFold(actual, expected) {
			return fmt.Errorf("expected %s, got %s", expected, actual)
		}
		return nil
	})

	ctx.Step(`^the short string should be "([^"]*)"$`, func(expected string) error {
		actual := world.Address.String()
		if !strings.EqualFold(actual, expected) {
			return fmt.Errorf("expected %s, got %s", expected, actual)
		}
		return nil
	})

	ctx.Step(`^the address should equal "([^"]*)"$`, func(expected string) error {
		actual := world.Address.String()
		if !strings.EqualFold(actual, expected) {
			return fmt.Errorf("expected %s, got %s", expected, actual)
		}
		return nil
	})

	ctx.Step(`^the byte length should be 32$`, func() error {
		if len(world.Bytes) != 32 {
			return fmt.Errorf("expected 32 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the bytes should be 32 bytes$`, func() error {
		if len(world.Bytes) != 32 {
			return fmt.Errorf("expected 32 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the result should be 32 bytes$`, func() error {
		if len(world.Bytes) != 32 {
			return fmt.Errorf("expected 32 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^all test vectors should pass$`, func() error {
		type Result struct {
			Name   string
			Passed bool
			Error  string
		}
		results := world.Result.([]Result)
		var failures []Result
		for _, r := range results {
			if !r.Passed {
				failures = append(failures, r)
			}
		}
		if len(failures) > 0 {
			var msgs []string
			for _, f := range failures {
				msgs = append(msgs, fmt.Sprintf("  - %s: %s", f.Name, f.Error))
			}
			return fmt.Errorf("%d test vectors failed:\n%s", len(failures), strings.Join(msgs, "\n"))
		}
		return nil
	})

	ctx.Step(`^the first byte should be zero$`, func() error {
		if world.Bytes[0] != 0 {
			return fmt.Errorf("expected first byte to be 0, got %d", world.Bytes[0])
		}
		return nil
	})

	ctx.Step(`^the last byte should be (\d+)$`, func(expected int) error {
		if int(world.Bytes[31]) != expected {
			return fmt.Errorf("expected last byte to be %d, got %d", expected, world.Bytes[31])
		}
		return nil
	})

	ctx.Step(`^it should equal address "([^"]*)"$`, func(expected string) error {
		expectedAddr := &aptos.AccountAddress{}
		if err := expectedAddr.ParseStringRelaxed(expected); err != nil {
			return err
		}
		if *world.Address != *expectedAddr {
			return fmt.Errorf("expected %s, got %s", expected, world.Address.String())
		}
		return nil
	})

	ctx.Step(`^they should be equal$`, func() error {
		if world.Result != true {
			return fmt.Errorf("expected addresses to be equal")
		}
		return nil
	})

	ctx.Step(`^they should not be equal$`, func() error {
		if world.Result != false {
			return fmt.Errorf("expected addresses to not be equal")
		}
		return nil
	})

	// Unused context parameter - required by godog signature
	_ = context.Background()
}
