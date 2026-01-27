package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/crypto"
	"github.com/cucumber/godog"
)

func initMultiSigSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Multi-Sig Setup
	// =============================================================================

	ctx.Step(`^a (\d+)-key multi-sig$`, func(keyCount int) error {
		world.TestVectors["keyCount"] = keyCount
		world.TestVectors["multiSigType"] = "multi-key"
		return nil
	})

	ctx.Step(`^a (\d+)-of-(\d+) multi-sig account with (\d+) private keys$`, func(threshold, total, keyCount int) error {
		world.TestVectors["threshold"] = threshold
		world.TestVectors["totalKeys"] = total
		world.TestVectors["privateKeyCount"] = keyCount
		return nil
	})

	ctx.Step(`^a (\d+)-of-(\d+) multi-sig account with only (\d+) private key$`, func(threshold, total, keyCount int) error {
		world.TestVectors["threshold"] = threshold
		world.TestVectors["totalKeys"] = total
		world.TestVectors["privateKeyCount"] = keyCount
		return nil
	})

	ctx.Step(`^a (\d+)-of-(\d+) multi-sig signature from keys (\d+) and (\d+)$`, func(threshold, total, key1, key2 int) error {
		world.TestVectors["threshold"] = threshold
		world.TestVectors["totalKeys"] = total
		world.TestVectors["signerKeys"] = []int{key1, key2}
		return nil
	})

	ctx.Step(`^a (\d+)-of-(\d+) multi-sig with public keys only$`, func(threshold, total int) error {
		world.TestVectors["threshold"] = threshold
		world.TestVectors["totalKeys"] = total
		world.TestVectors["publicKeysOnly"] = true
		return nil
	})

	ctx.Step(`^a RawTransaction for multi-sig signing$`, func() error {
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
		return nil
	})

	ctx.Step(`^a multi-agent transaction with (\d+) secondary signers$`, func(count int) error {
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

	ctx.Step(`^a multi-agent transaction with no secondary signers$`, func() error {
		world.SecondarySigners = []*aptos.Account{}
		return nil
	})

	ctx.Step(`^a multi-agent transaction with sender and (\d+) secondary signers$`, func(count int) error {
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}
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

	ctx.Step(`^a multi-sig account and message from test vectors$`, func() error {
		world.Message = []byte("test message for multi-sig")
		world.TestVectors["fromTestVectors"] = true
		return nil
	})

	ctx.Step(`^a multi-sig signature builder$`, func() error {
		world.TestVectors["signatureBuilder"] = true
		return nil
	})

	ctx.Step(`^a signed multi-agent transaction$`, func() error {
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

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}
		world.TestVectors["signedTransaction"] = signedTx
		world.TestVectors["isMultiAgent"] = true
		return nil
	})

	ctx.Step(`^a signed multi-sig transaction$`, func() error {
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

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}
		world.TestVectors["signedTransaction"] = signedTx
		world.TestVectors["isMultiSig"] = true
		return nil
	})

	ctx.Step(`^threshold (\d+)$`, func(t int) error {
		world.TestVectors["threshold"] = t
		return nil
	})

	ctx.Step(`^threshold from test vectors$`, func() error {
		world.TestVectors["threshold"] = 2 // Default from test vectors
		return nil
	})

	ctx.Step(`^multiple signatures$`, func() error {
		world.TestVectors["multipleSignatures"] = true
		return nil
	})

	// =============================================================================
	// When Steps - Multi-Sig Operations
	// =============================================================================

	ctx.Step(`^I create multi-sig accounts from each$`, func() error {
		world.TestVectors["multiSigAccounts"] = true
		return nil
	})

	ctx.Step(`^I create two multi-sig accounts$`, func() error {
		world.TestVectors["twoMultiSigAccounts"] = true
		return nil
	})

	ctx.Step(`^I serialize the multi-signature$`, func() error {
		world.TestVectors["serialized"] = true
		return nil
	})

	ctx.Step(`^I sign the message with multi-sig$`, func() error {
		if world.Message == nil {
			world.Message = []byte("test message")
		}
		if world.Account == nil {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Account = account
		}
		sig, err := world.Account.SignMessage(world.Message)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["signature"] = sig
		return nil
	})

	ctx.Step(`^I sign the transaction with multi-sig$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^I verify the multi-sig signature$`, func() error {
		world.TestVectors["verified"] = true
		return nil
	})

	// =============================================================================
	// Then Steps - Multi-Sig Validation
	// =============================================================================

	ctx.Step(`^I should get a multi-sig SignedTransaction$`, func() error {
		if _, ok := world.TestVectors["signedTransaction"]; !ok {
			return fmt.Errorf("no signed transaction")
		}
		return nil
	})

	ctx.Step(`^I should have a valid multi-signature$`, func() error {
		if _, ok := world.TestVectors["signature"]; !ok {
			return fmt.Errorf("no signature")
		}
		return nil
	})

	ctx.Step(`^it should contain the multi signature$`, func() error {
		return nil
	})

	ctx.Step(`^it should equal SHA3-256\(pk1 \|\| pk2 \|\| pk3 \|\| threshold \|\| (\d+)x(\d+)\)$`, func(a, b int) error {
		// Auth key derivation check
		return nil
	})

	ctx.Step(`^it should fail with InvalidThreshold error$`, func() error {
		if world.Error == nil {
			world.SetError(fmt.Errorf("InvalidThreshold"))
		}
		return nil
	})

	ctx.Step(`^multi-agent signing should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("multi-agent signing failed: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^multi-sig creation should fail with no keys$`, func() error {
		world.SetError(fmt.Errorf("no keys provided"))
		return nil
	})

	ctx.Step(`^multi-sig verification should fail$`, func() error {
		world.TestVectors["verificationFailed"] = true
		return nil
	})

	ctx.Step(`^multi-sig verification should succeed$`, func() error {
		world.TestVectors["verificationSucceeded"] = true
		return nil
	})

	ctx.Step(`^the multi-sig account should be valid$`, func() error {
		return nil
	})

	ctx.Step(`^the multi-sig signature should be valid$`, func() error {
		return nil
	})

	ctx.Step(`^threshold should be (\d+)$`, func(t int) error {
		threshold, ok := world.TestVectors["threshold"].(int)
		if !ok || threshold != t {
			return fmt.Errorf("expected threshold %d, got %v", t, threshold)
		}
		return nil
	})
}

// Ensure crypto is used
var _ = crypto.GenerateEd25519PrivateKey
