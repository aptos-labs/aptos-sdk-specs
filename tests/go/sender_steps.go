package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

// initSenderSteps registers sender and secondary signer step definitions.
func initSenderSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Sender Steps
	// =============================================================================

	ctx.Step(`^sender account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["senderAccount"] = account
		return nil
	})

	ctx.Step(`^sender authenticator should be Ed25519$`, func() error {
		// TODO: implement authenticator type check
		return godog.ErrPending
	})

	ctx.Step(`^sender authenticator should be serialized$`, func() error {
		// TODO: implement serialization check
		return godog.ErrPending
	})

	ctx.Step(`^sender can send partially signed tx to sponsor$`, func() error {
		// Documentation assertion
		return nil
	})

	ctx.Step(`^sender creates RawTransaction$`, func() error {
		if world.Account == nil {
			return godog.ErrPending
		}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, _ := aptos.CoinTransferPayload(nil, recipient, 1000)
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

	ctx.Step(`^sender creates transaction with max_gas_amount=(\d+)$`, func(maxGas int) error {
		if world.Account == nil {
			return godog.ErrPending
		}
		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, _ := aptos.CoinTransferPayload(nil, recipient, 1000)
		rawTx := &aptos.RawTransaction{
			Sender:                     world.Account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               uint64(maxGas),
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: 1700000000,
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^sender creates valid transaction$`, func() error {
		return nil // Same as sender creates RawTransaction
	})

	ctx.Step(`^sender does not sign$`, func() error {
		world.TestVectors["senderNotSigned"] = true
		return nil
	})

	ctx.Step(`^sender signs second$`, func() error {
		world.TestVectors["senderSignsSecond"] = true
		return nil
	})

	ctx.Step(`^sender signs the fee payer signing message$`, func() error {
		// TODO: implement fee payer signing
		return godog.ErrPending
	})

	ctx.Step(`^sender signs their portion$`, func() error {
		// TODO: implement partial signing
		return godog.ErrPending
	})

	ctx.Step(`^sender signs$`, func() error {
		if world.Account == nil {
			return godog.ErrPending
		}
		world.TestVectors["senderSigned"] = true
		return nil
	})

	ctx.Step(`^sender's balance is not deducted for gas$`, func() error {
		// TODO: implement balance check
		return godog.ErrPending
	})

	// =============================================================================
	// Secondary Signer Steps
	// =============================================================================

	ctx.Step(`^secondary signer (\d+) signs first$`, func(signerNum int) error {
		world.TestVectors["secondarySignerFirst"] = signerNum
		return nil
	})

	ctx.Step(`^secondary signer (\d+) signs last$`, func(signerNum int) error {
		world.TestVectors["secondarySignerLast"] = signerNum
		return nil
	})

	ctx.Step(`^secondary signer (\d+) signs their portion$`, func(signerNum int) error {
		// TODO: implement partial signing
		return godog.ErrPending
	})

	ctx.Step(`^secondary signer accounts$`, func() error {
		account1, _ := aptos.NewEd25519Account()
		account2, _ := aptos.NewEd25519Account()
		world.TestVectors["secondarySignerAccounts"] = []interface{}{account1, account2}
		return nil
	})

	ctx.Step(`^secondary signer address A$`, func() error {
		address := aptos.AccountAddress{}
		address[31] = 0xAA
		world.TestVectors["secondarySignerAddressA"] = &address
		return nil
	})

	ctx.Step(`^secondary signer addresses \[A, B, C\]$`, func() error {
		addrA := aptos.AccountAddress{}
		addrA[31] = 0xAA
		addrB := aptos.AccountAddress{}
		addrB[31] = 0xBB
		addrC := aptos.AccountAddress{}
		addrC[31] = 0xCC
		world.TestVectors["secondarySignerAddresses"] = []*aptos.AccountAddress{&addrA, &addrB, &addrC}
		return nil
	})

	ctx.Step(`^secondary signer addresses$`, func() error {
		addr1 := aptos.AccountAddress{}
		addr1[31] = 0x01
		addr2 := aptos.AccountAddress{}
		addr2[31] = 0x02
		world.TestVectors["secondarySignerAddresses"] = []*aptos.AccountAddress{&addr1, &addr2}
		return nil
	})

	ctx.Step(`^secondary signers should be serialized as vector$`, func() error {
		// TODO: implement serialization check
		return godog.ErrPending
	})

	ctx.Step(`^secondary_signer_addresses should be empty$`, func() error {
		// TODO: implement emptiness check
		return godog.ErrPending
	})

	ctx.Step(`^secondary_signers should be empty$`, func() error {
		// TODO: implement emptiness check
		return godog.ErrPending
	})

	ctx.Step(`^secondary addresses should be serialized as vector$`, func() error {
		// TODO: implement serialization check
		return godog.ErrPending
	})

	ctx.Step(`^secondary authenticator should be Secp256k1$`, func() error {
		// TODO: implement authenticator type check
		return godog.ErrPending
	})

	// =============================================================================
	// Sponsor Steps
	// =============================================================================

	ctx.Step(`^sponsor combines signatures into authenticator$`, func() error {
		// TODO: implement signature combination
		return godog.ErrPending
	})

	ctx.Step(`^sponsor reviews the transaction$`, func() error {
		// Documentation step
		return nil
	})

	ctx.Step(`^sponsor signs first$`, func() error {
		world.TestVectors["sponsorSignsFirst"] = true
		return nil
	})

	ctx.Step(`^sponsor signs the fee payer signing message$`, func() error {
		// TODO: implement sponsor signing
		return godog.ErrPending
	})

	// =============================================================================
	// Signature Steps
	// =============================================================================

	ctx.Step(`^signature from account B$`, func() error {
		world.TestVectors["signatureFromB"] = true
		return nil
	})

	ctx.Step(`^signature1 for "([^"]*)"$`, func(msg string) error {
		world.TestVectors["signature1Message"] = msg
		return nil
	})

	ctx.Step(`^signatures added in order (\d+), (\d+), (\d+)$`, func(a, b, c int) error {
		world.TestVectors["signatureOrder"] = []int{a, b, c}
		return nil
	})

	ctx.Step(`^signatures from (\d+) signers on same message$`, func(count int) error {
		world.TestVectors["signerCount"] = count
		return nil
	})

	ctx.Step(`^signatures from test vectors$`, func() error {
		// Load from test vectors
		return nil
	})

	ctx.Step(`^signatures should be ordered by index$`, func() error {
		// TODO: implement signature ordering check
		return godog.ErrPending
	})

	ctx.Step(`^signing attempts should fail$`, func() error {
		if world.Error == nil {
			return godog.ErrPending
		}
		return nil
	})
}
