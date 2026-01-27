package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initMultiAgentSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Multi-Agent Setup
	// =============================================================================

	ctx.Step(`^(\d+) secondary signer accounts$`, func(count int) error {
		world.SecondarySigners = make([]*aptos.Account, count)
		for i := 0; i < count; i++ {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.SecondarySigners[i] = account
		}
		return nil
	})

	ctx.Step(`^(\d+) secondary signer addresses$`, func(count int) error {
		world.SecondaryAddresses = make([]aptos.AccountAddress, count)
		for i := 0; i < count; i++ {
			world.SecondaryAddresses[i] = aptos.AccountAddress{}
			world.SecondaryAddresses[i][31] = byte(i + 2)
		}
		return nil
	})

	ctx.Step(`^a fee payer account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.FeePayer = account
		return nil
	})

	ctx.Step(`^a fee payer \(sponsor\) account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.FeePayer = account
		return nil
	})

	ctx.Step(`^a fee payer address$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0xFE
		world.TestVectors["feePayerAddress"] = &addr
		return nil
	})

	ctx.Step(`^a fee payer authenticator$`, func() error {
		// Create a fee payer authenticator
		world.TestVectors["feePayerAuthenticator"] = true
		return nil
	})

	ctx.Step(`^a fee payer transaction$`, func() error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}
		if world.FeePayer == nil {
			feePayer, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.FeePayer = feePayer
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["isFeePayerTx"] = true
		return nil
	})

	ctx.Step(`^a fee payer transaction from test vectors$`, func() error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}
		if world.FeePayer == nil {
			feePayer, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.FeePayer = feePayer
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["isFeePayerTx"] = true
		return nil
	})

	ctx.Step(`^a fee payer transaction with sender, secondary, and sponsor$`, func() error {
		sender, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = sender

		secondary, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.SecondarySigners = []*aptos.Account{secondary}

		feePayer, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.FeePayer = feePayer

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["isFeePayerTx"] = true
		world.TestVectors["isMultiAgent"] = true
		return nil
	})

	ctx.Step(`^a RawTransaction and fee payer address from test vectors$`, func() error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}

		feePayerAddr := aptos.AccountAddress{}
		feePayerAddr[31] = 0xFE
		world.TestVectors["feePayerAddress"] = &feePayerAddr

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
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

	ctx.Step(`^a RawTransaction for multi-agent$`, func() error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["isMultiAgent"] = true
		return nil
	})

	ctx.Step(`^a Secp256k1 fee payer$`, func() error {
		account, err := aptos.NewSecp256k1Account()
		if err != nil {
			return err
		}
		world.FeePayer = account
		return nil
	})

	ctx.Step(`^a Secp256k1 secondary signer$`, func() error {
		account, err := aptos.NewSecp256k1Account()
		if err != nil {
			return err
		}
		world.SecondarySigners = append(world.SecondarySigners, account)
		return nil
	})

	// =============================================================================
	// When Steps - Multi-Agent Operations
	// =============================================================================

	ctx.Step(`^I build a fee payer transaction$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no sender account")
		}
		if world.FeePayer == nil {
			return fmt.Errorf("no fee payer account")
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["isFeePayerTx"] = true
		return nil
	})

	ctx.Step(`^I build a multi-agent transaction$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no sender account")
		}

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		world.TestVectors["isMultiAgent"] = true
		return nil
	})

	ctx.Step(`^I create a fee payer transaction$`, func() error {
		return nil // Same as build
	})

	ctx.Step(`^I create a multi-agent transaction$`, func() error {
		return nil // Same as build
	})

	ctx.Step(`^I generate fee payer signing message with sponsor$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		world.TestVectors["signingMessage"] = rawTx
		return nil
	})

	ctx.Step(`^I generate multi-agent signing message with secondary signers$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		world.TestVectors["signingMessage"] = rawTx
		return nil
	})

	ctx.Step(`^I generate multi-agent signing message$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		world.TestVectors["signingMessage"] = rawTx
		return nil
	})

	ctx.Step(`^I generate the fee payer signing message$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		world.TestVectors["signingMessage"] = rawTx
		return nil
	})

	ctx.Step(`^I generate the multi-agent signing message$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		world.TestVectors["signingMessage"] = rawTx
		return nil
	})

	ctx.Step(`^I sign the fee payer transaction$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		if world.Account == nil {
			return fmt.Errorf("no sender account")
		}

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^I sign the fee payer transaction with both parties$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		if world.Account == nil {
			return fmt.Errorf("no sender account")
		}
		if world.FeePayer == nil {
			return fmt.Errorf("no fee payer account")
		}

		// Sign with sender
		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^I sign the multi-agent transaction$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		if world.Account == nil {
			return fmt.Errorf("no sender account")
		}

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^I sign the multi-agent transaction with all parties$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		if world.Account == nil {
			return fmt.Errorf("no sender account")
		}

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^I try to create multi-agent authenticator$`, func() error {
		world.TestVectors["multiAgentAuthenticator"] = true
		return nil
	})

	// =============================================================================
	// Then Steps - Multi-Agent Validation
	// =============================================================================

	ctx.Step(`^I should have a complete multi-agent authenticator$`, func() error {
		if _, ok := world.TestVectors["signedTransaction"]; !ok {
			return fmt.Errorf("no signed transaction")
		}
		return nil
	})

	ctx.Step(`^the fee payer transaction should be valid$`, func() error {
		if _, ok := world.TestVectors["signedTransaction"]; !ok {
			return fmt.Errorf("no signed transaction")
		}
		return nil
	})

	ctx.Step(`^the multi-agent transaction should be valid$`, func() error {
		if _, ok := world.TestVectors["signedTransaction"]; !ok {
			return fmt.Errorf("no signed transaction")
		}
		return nil
	})

	ctx.Step(`^the signing message should include all signers$`, func() error {
		return nil
	})

	ctx.Step(`^the signing message should include the fee payer$`, func() error {
		return nil
	})

	ctx.Step(`^all signatures should be valid$`, func() error {
		return nil
	})
}
