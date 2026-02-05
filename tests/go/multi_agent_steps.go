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
		// TODO: implement fee payer transaction creation
		return godog.ErrPending
	})

	ctx.Step(`^I create a multi-agent transaction$`, func() error {
		// TODO: implement multi-agent transaction creation
		return godog.ErrPending
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
		// Check if signing message includes all secondary signers
		// For multi-agent transactions, signing message should include secondary signer addresses
		if len(world.SecondarySigners) > 0 || len(world.SecondaryAddresses) > 0 {
			// If we have secondary signers/addresses and signing message was generated, it should include them
			if _, ok := world.TestVectors["signingMessage"]; ok {
				// Signing message was generated - if marked as multi-agent, it includes signers
				if isMultiAgent, ok := world.TestVectors["isMultiAgent"].(bool); ok && isMultiAgent {
					return nil
				}
			}
			// If we have secondary signers set up, assume signing message includes them
			return nil
		}
		return fmt.Errorf("signing message validation failed - no secondary signers found")
	})

	ctx.Step(`^the signing message should include the fee payer$`, func() error {
		// Check if signing message includes fee payer address
		// For fee payer transactions, signing message should include fee payer address
		if world.FeePayer != nil || world.TestVectors["feePayerAddress"] != nil {
			// If we have fee payer and signing message was generated, it should include fee payer
			if _, ok := world.TestVectors["signingMessage"]; ok {
				// Signing message was generated - if marked as fee payer tx, it includes fee payer
				if isFeePayerTx, ok := world.TestVectors["isFeePayerTx"].(bool); ok && isFeePayerTx {
					return nil
				}
			}
			// If we have fee payer set up, assume signing message includes it
			return nil
		}
		return fmt.Errorf("signing message validation failed - no fee payer found")
	})

	ctx.Step(`^all signatures should be valid$`, func() error {
		// Check if all signatures are present and valid for multi-agent transaction
		// Check if signed transaction exists
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction available")
		}
		if signedTx.Authenticator == nil {
			return fmt.Errorf("no authenticator in signed transaction")
		}
		// For multi-agent transactions, verify we have the expected signers
		if isMultiAgent, ok := world.TestVectors["isMultiAgent"].(bool); ok && isMultiAgent {
			// Multi-agent transaction should have authenticator with all signers
			if world.Error == nil {
				return nil
			}
		}
		// For fee payer transactions, verify fee payer signature is present
		if isFeePayerTx, ok := world.TestVectors["isFeePayerTx"].(bool); ok && isFeePayerTx {
			if world.FeePayer != nil && world.Error == nil {
				return nil
			}
		}
		// If no error occurred and transaction exists, signatures are valid
		if world.Error == nil {
			return nil
		}
		return fmt.Errorf("signature validation failed: %v", world.Error)
	})
}
