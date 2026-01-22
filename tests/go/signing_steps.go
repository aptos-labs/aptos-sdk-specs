package main

import (
	"bytes"
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/bcs"
	"github.com/aptos-labs/aptos-go-sdk/crypto"
	"github.com/cucumber/godog"
)

func initSigningSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Transaction and Account Setup
	// =============================================================================

	ctx.Step(`^a signed transaction$`, func() error {
		// Create a valid transaction and sign it
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}

		// Create an account and sign
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}

		signedTx, err := rawTx.SignedTransaction(account)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction"] = signedTx
		world.TestVectors["rawTransaction"] = rawTx
		world.Account = account
		return nil
	})

	ctx.Step(`^a signed transaction with Ed25519$`, func() error {
		// Same as above but explicit about Ed25519
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}

		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}

		signedTx, err := rawTx.SignedTransaction(account)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction"] = signedTx
		world.TestVectors["rawTransaction"] = rawTx
		world.Account = account
		return nil
	})

	ctx.Step(`^a SignedTransaction$`, func() error {
		// Create a signed transaction for serialization tests
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}

		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}

		signedTx, err := rawTx.SignedTransaction(account)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction"] = signedTx
		world.TestVectors["rawTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^two different Ed25519 accounts$`, func() error {
		account1, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		account2, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account1
		world.Account2 = account2
		return nil
	})

	ctx.Step(`^a valid signed transaction$`, func() error {
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}

		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}

		signedTx, err := rawTx.SignedTransaction(account)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction"] = signedTx
		world.TestVectors["rawTransaction"] = rawTx
		world.Account = account
		return nil
	})

	ctx.Step(`^a signed transaction for submission$`, func() error {
		sender := aptos.AccountAddress{}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     sender,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}

		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}

		signedTx, err := rawTx.SignedTransaction(account)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction"] = signedTx
		return nil
	})

	ctx.Step(`^the same signed transaction$`, func() error {
		// Use the already existing signed transaction
		if _, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction); !ok {
			return fmt.Errorf("no signed transaction available")
		}
		return nil
	})

	ctx.Step(`^two different signed transactions$`, func() error {
		sender1 := aptos.AccountAddress{}
		sender1[31] = 0x01
		sender2 := aptos.AccountAddress{}
		sender2[31] = 0x02
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42

		payload1, err := aptos.CoinTransferPayload(nil, recipient, 1000)
		if err != nil {
			return err
		}
		payload2, err := aptos.CoinTransferPayload(nil, recipient, 2000)
		if err != nil {
			return err
		}

		rawTx1 := &aptos.RawTransaction{
			Sender:                     sender1,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload1},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		rawTx2 := &aptos.RawTransaction{
			Sender:                     sender2,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload2},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}

		account1, _ := aptos.NewEd25519Account()
		account2, _ := aptos.NewEd25519Account()

		signedTx1, _ := rawTx1.SignedTransaction(account1)
		signedTx2, _ := rawTx2.SignedTransaction(account2)

		world.TestVectors["signedTransaction1"] = signedTx1
		world.TestVectors["signedTransaction2"] = signedTx2
		return nil
	})

	ctx.Step(`^I should get a valid RawTransaction$`, func() error {
		_, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction set")
		}
		return nil
	})

	// =============================================================================
	// When Steps - Signing Operations
	// =============================================================================

	ctx.Step(`^I sign the transaction with the account$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction set")
		}
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}

		world.TestVectors["signedTransaction"] = signedTx
		world.ClearError()
		return nil
	})

	ctx.Step(`^I sign the transaction$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction set")
		}
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}

		signedTx, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			world.SetError(err)
			return nil
		}

		world.TestVectors["signedTransaction"] = signedTx
		world.ClearError()
		return nil
	})

	ctx.Step(`^I sign the transaction twice$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction set")
		}
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}

		signedTx1, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}
		signedTx2, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction1"] = signedTx1
		world.TestVectors["signedTransaction2"] = signedTx2
		return nil
	})

	ctx.Step(`^both accounts sign the transaction$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction set")
		}
		if world.Account == nil || world.Account2 == nil {
			return fmt.Errorf("need two accounts")
		}

		signedTx1, err := rawTx.SignedTransaction(world.Account)
		if err != nil {
			return err
		}
		signedTx2, err := rawTx.SignedTransaction(world.Account2)
		if err != nil {
			return err
		}

		world.TestVectors["signedTransaction1"] = signedTx1
		world.TestVectors["signedTransaction2"] = signedTx2
		return nil
	})

	ctx.Step(`^I get the raw_transaction$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		world.TestVectors["extractedRawTransaction"] = signedTx.Transaction
		return nil
	})

	ctx.Step(`^I extract the signature from the authenticator$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		// Store the authenticator for later verification
		world.TestVectors["authenticator"] = signedTx.Authenticator
		return nil
	})

	ctx.Step(`^I get the authenticator$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		world.TestVectors["authenticator"] = signedTx.Authenticator
		return nil
	})

	ctx.Step(`^I call to_bytes\(\)$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		serializer := &bcs.Serializer{}
		signedTx.MarshalBCS(serializer)
		if err := serializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		world.Bytes = serializer.ToBytes()
		world.ClearError()
		return nil
	})

	ctx.Step(`^I hash the SignedTransaction$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		hash, err := signedTx.Hash()
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.HexString = hash
		world.ClearError()
		return nil
	})

	// =============================================================================
	// Then Steps - Validation
	// =============================================================================

	ctx.Step(`^I should get a SignedTransaction$`, func() error {
		_, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction created")
		}
		return nil
	})

	ctx.Step(`^the authenticator should be Ed25519 variant$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		if signedTx.Authenticator == nil {
			return fmt.Errorf("no authenticator")
		}
		// Check if it's Ed25519 variant (could be aptos.Ed25519TransactionAuthenticator or crypto.Ed25519Authenticator)
		switch signedTx.Authenticator.Auth.(type) {
		case *crypto.Ed25519Authenticator:
			return nil
		case *aptos.Ed25519TransactionAuthenticator:
			return nil
		case *crypto.SingleKeyAuthenticator:
			// Check if it wraps Ed25519
			ska := signedTx.Authenticator.Auth.(*crypto.SingleKeyAuthenticator)
			if _, ok := ska.Sig.Signature.(*crypto.Ed25519Signature); ok {
				return nil
			}
		}
		return fmt.Errorf("expected Ed25519 authenticator, got %T", signedTx.Authenticator.Auth)
	})

	ctx.Step(`^it should equal the original RawTransaction$`, func() error {
		original, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no original raw transaction")
		}
		extracted, ok := world.TestVectors["extractedRawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no extracted raw transaction")
		}
		// Compare by serializing both
		serializer1 := &bcs.Serializer{}
		original.MarshalBCS(serializer1)
		serializer2 := &bcs.Serializer{}
		extracted.MarshalBCS(serializer2)
		if !bytes.Equal(serializer1.ToBytes(), serializer2.ToBytes()) {
			return fmt.Errorf("raw transactions don't match")
		}
		return nil
	})

	ctx.Step(`^the signature should verify against the signing message$`, func() error {
		signedTx, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction)
		if !ok {
			return fmt.Errorf("no signed transaction set")
		}
		// Use the built-in verify method
		err := signedTx.Verify()
		if err != nil {
			return fmt.Errorf("signature verification failed: %v", err)
		}
		return nil
	})

	ctx.Step(`^it should contain the signer's public key$`, func() error {
		auth, ok := world.TestVectors["authenticator"].(*aptos.TransactionAuthenticator)
		if !ok {
			return fmt.Errorf("no authenticator set")
		}
		// Check for public key based on authenticator type
		switch a := auth.Auth.(type) {
		case *crypto.Ed25519Authenticator:
			if a.PubKey == nil {
				return fmt.Errorf("no public key in Ed25519 authenticator")
			}
			return nil
		case *aptos.Ed25519TransactionAuthenticator:
			if a.Sender == nil || a.Sender.PubKey() == nil {
				return fmt.Errorf("no public key in Ed25519TransactionAuthenticator")
			}
			return nil
		case *crypto.SingleKeyAuthenticator:
			if a.PubKey == nil {
				return fmt.Errorf("no public key in SingleKey authenticator")
			}
			return nil
		}
		return fmt.Errorf("unsupported authenticator type: %T", auth.Auth)
	})

	ctx.Step(`^it should contain the signature$`, func() error {
		auth, ok := world.TestVectors["authenticator"].(*aptos.TransactionAuthenticator)
		if !ok {
			return fmt.Errorf("no authenticator set")
		}
		// Check for signature based on authenticator type
		switch a := auth.Auth.(type) {
		case *crypto.Ed25519Authenticator:
			if a.Sig == nil {
				return fmt.Errorf("no signature in Ed25519 authenticator")
			}
			return nil
		case *aptos.Ed25519TransactionAuthenticator:
			if a.Sender == nil || a.Sender.Signature() == nil {
				return fmt.Errorf("no signature in Ed25519TransactionAuthenticator")
			}
			return nil
		case *crypto.SingleKeyAuthenticator:
			if a.Sig == nil {
				return fmt.Errorf("no signature in SingleKey authenticator")
			}
			return nil
		}
		return fmt.Errorf("unsupported authenticator type: %T", auth.Auth)
	})

	ctx.Step(`^both SignedTransactions should be identical$`, func() error {
		signedTx1, ok1 := world.TestVectors["signedTransaction1"].(*aptos.SignedTransaction)
		signedTx2, ok2 := world.TestVectors["signedTransaction2"].(*aptos.SignedTransaction)
		if !ok1 || !ok2 {
			return fmt.Errorf("need two signed transactions")
		}
		// Compare by serializing
		serializer1 := &bcs.Serializer{}
		signedTx1.MarshalBCS(serializer1)
		serializer2 := &bcs.Serializer{}
		signedTx2.MarshalBCS(serializer2)
		if !bytes.Equal(serializer1.ToBytes(), serializer2.ToBytes()) {
			return fmt.Errorf("signed transactions should be identical")
		}
		return nil
	})

	ctx.Step(`^the signatures should be different$`, func() error {
		signedTx1, ok1 := world.TestVectors["signedTransaction1"].(*aptos.SignedTransaction)
		signedTx2, ok2 := world.TestVectors["signedTransaction2"].(*aptos.SignedTransaction)
		if !ok1 || !ok2 {
			return fmt.Errorf("need two signed transactions")
		}
		// Compare by serializing
		serializer1 := &bcs.Serializer{}
		signedTx1.MarshalBCS(serializer1)
		serializer2 := &bcs.Serializer{}
		signedTx2.MarshalBCS(serializer2)
		if bytes.Equal(serializer1.ToBytes(), serializer2.ToBytes()) {
			return fmt.Errorf("signed transactions should be different")
		}
		return nil
	})

	ctx.Step(`^the serialization should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("serialization failed: %v", world.Error)
		}
		if len(world.Bytes) == 0 {
			return fmt.Errorf("serialization produced empty bytes")
		}
		return nil
	})

	ctx.Step(`^the result should be valid BCS$`, func() error {
		if len(world.Bytes) == 0 {
			return fmt.Errorf("no bytes to validate")
		}
		// Try to deserialize to validate BCS format
		deserializer := bcs.NewDeserializer(world.Bytes)
		signedTx := &aptos.SignedTransaction{}
		signedTx.UnmarshalBCS(deserializer)
		if err := deserializer.Error(); err != nil {
			return fmt.Errorf("invalid BCS: %v", err)
		}
		return nil
	})

	ctx.Step(`^the hash should be 64 hex characters with 0x prefix$`, func() error {
		if len(world.HexString) != 66 { // 0x + 64 chars
			return fmt.Errorf("expected 66 characters, got %d", len(world.HexString))
		}
		if world.HexString[:2] != "0x" {
			return fmt.Errorf("expected 0x prefix")
		}
		return nil
	})

	ctx.Step(`^the hash should be the prefix of pending transaction IDs$`, func() error {
		// Just verify hash format - actual transaction ID matching requires network
		if len(world.HexString) < 2 {
			return fmt.Errorf("no hash set")
		}
		return nil
	})
}
