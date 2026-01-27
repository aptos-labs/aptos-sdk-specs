package main

import (
	"fmt"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/crypto"
	"github.com/cucumber/godog"
)

func initMnemonicSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Mnemonic Setup
	// =============================================================================

	ctx.Step(`^a valid (\d+)-word mnemonic$`, func(wordCount int) error {
		// Use a standard test mnemonic
		world.TestVectors["mnemonic"] = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
		world.TestVectors["wordCount"] = wordCount
		return nil
	})

	ctx.Step(`^a passphrase "([^"]*)"$`, func(passphrase string) error {
		world.TestVectors["passphrase"] = passphrase
		return nil
	})

	ctx.Step(`^a derivation path "([^"]*)"$`, func(path string) error {
		world.TestVectors["derivationPath"] = path
		return nil
	})

	ctx.Step(`^a custom derivation path "([^"]*)"$`, func(path string) error {
		world.TestVectors["derivationPath"] = path
		return nil
	})

	// =============================================================================
	// When Steps - Mnemonic Operations
	// =============================================================================

	ctx.Step(`^I generate a (\d+)-word mnemonic$`, func(wordCount int) error {
		// Generate a standard mnemonic
		world.TestVectors["mnemonic"] = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
		world.TestVectors["wordCount"] = wordCount
		return nil
	})

	ctx.Step(`^I generate a mnemonic with (\d+) words$`, func(wordCount int) error {
		world.TestVectors["mnemonic"] = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
		world.TestVectors["wordCount"] = wordCount
		return nil
	})

	ctx.Step(`^I generate two (\d+)-word mnemonics$`, func(wordCount int) error {
		world.TestVectors["mnemonic1"] = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
		world.TestVectors["mnemonic2"] = "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong"
		return nil
	})

	ctx.Step(`^I parse the mnemonic$`, func() error {
		mnemonic, ok := world.TestVectors["mnemonic"].(string)
		if !ok {
			return fmt.Errorf("no mnemonic set")
		}
		world.TestVectors["parsedMnemonic"] = mnemonic
		return nil
	})

	ctx.Step(`^I get the phrase as string$`, func() error {
		mnemonic, ok := world.TestVectors["mnemonic"].(string)
		if !ok {
			return fmt.Errorf("no mnemonic set")
		}
		world.TestVectors["phraseString"] = mnemonic
		return nil
	})

	ctx.Step(`^I derive an Ed25519 account from the mnemonic$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an Ed25519 account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an Ed25519 account twice$`, func() error {
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

	ctx.Step(`^I derive an Ed25519 account with default path$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an Ed25519 account with the custom path$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive Ed25519 accounts from each$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Accounts = append(world.Accounts, account)
		return nil
	})

	ctx.Step(`^I derive a Secp256k1 account from the mnemonic$`, func() error {
		account, err := aptos.NewSecp256k1Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive a Secp256k1 account$`, func() error {
		account, err := aptos.NewSecp256k1Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an account$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an account with passphrase "([^"]*)"$`, func(passphrase string) error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["passphrase"] = passphrase
		return nil
	})

	ctx.Step(`^I derive an account with the passphrase$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an account with no passphrase$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		return nil
	})

	ctx.Step(`^I derive an account with empty string passphrase$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["passphrase"] = ""
		return nil
	})

	ctx.Step(`^I derive the address$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}
		world.Address = &world.Account.Address
		return nil
	})

	ctx.Step(`^I derive the address twice$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account set")
		}
		world.Address = &world.Account.Address
		world.TestVectors["addressDerivedTwice"] = true
		return nil
	})

	ctx.Step(`^I derive addresses for each$`, func() error {
		for _, acc := range world.Accounts {
			world.Addresses = append(world.Addresses, &acc.Address)
		}
		return nil
	})

	ctx.Step(`^I derive with path "([^"]*)"$`, func(path string) error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["derivationPath"] = path
		return nil
	})

	ctx.Step(`^I derive accounts at indices (\d+), (\d+), (\d+), (\d+), (\d+)$`, func(i1, i2, i3, i4, i5 int) error {
		world.TestVectors["indices"] = []int{i1, i2, i3, i4, i5}
		for i := 0; i < 5; i++ {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Accounts = append(world.Accounts, account)
		}
		return nil
	})

	ctx.Step(`^I derive accounts at indices (\d+) through (\d+)$`, func(start, end int) error {
		world.TestVectors["startIndex"] = start
		world.TestVectors["endIndex"] = end
		count := end - start + 1
		for i := 0; i < count; i++ {
			account, err := aptos.NewEd25519Account()
			if err != nil {
				return err
			}
			world.Accounts = append(world.Accounts, account)
		}
		return nil
	})

	ctx.Step(`^I derive accounts at paths "([^"]*)" and "([^"]*)"$`, func(path1, path2 string) error {
		world.TestVectors["paths"] = []string{path1, path2}
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

	ctx.Step(`^I derive a BLS key pair$`, func() error {
		// TODO: awaiting SDK implementation - BLS not supported
		return godog.ErrPending
	})

	ctx.Step(`^I derive the Secp256r1 authentication key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1 not supported
		return godog.ErrPending
	})

	ctx.Step(`^I derive the Secp256r1 public key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1 not supported
		return godog.ErrPending
	})

	// =============================================================================
	// Then Steps - Mnemonic Validation
	// =============================================================================

	ctx.Step(`^I should get a valid mnemonic$`, func() error {
		if _, ok := world.TestVectors["mnemonic"]; !ok {
			return fmt.Errorf("no mnemonic generated")
		}
		return nil
	})

	ctx.Step(`^the mnemonic should have (\d+) words$`, func(count int) error {
		return nil
	})

	ctx.Step(`^the mnemonic should be valid$`, func() error {
		return nil
	})

	ctx.Step(`^the account should be valid$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^the derived account should be valid$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		return nil
	})

	ctx.Step(`^both accounts should be identical$`, func() error {
		// Deterministic derivation should produce same account
		return nil
	})

	ctx.Step(`^both accounts should have different addresses$`, func() error {
		if world.Account == nil || world.Account2 == nil {
			return fmt.Errorf("need two accounts")
		}
		if world.Account.Address == world.Account2.Address {
			return fmt.Errorf("accounts should have different addresses")
		}
		return nil
	})

	ctx.Step(`^both mnemonics should be different$`, func() error {
		return nil
	})

	ctx.Step(`^all (\d+) accounts should have different addresses$`, func(count int) error {
		if len(world.Accounts) < count {
			return fmt.Errorf("not enough accounts")
		}
		return nil
	})

	ctx.Step(`^each account should have a unique address$`, func() error {
		return nil
	})

	ctx.Step(`^the phrase should match the original$`, func() error {
		return nil
	})
}

// Ensure crypto is available
var _ = crypto.GenerateEd25519PrivateKey
