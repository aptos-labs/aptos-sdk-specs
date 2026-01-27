package main

import (
	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/crypto"
)

// World holds the test context for each scenario
type World struct {
	// Configuration
	NetworkURL string
	Client     *aptos.Client

	// Addresses
	Address   *aptos.AccountAddress
	Addresses []*aptos.AccountAddress

	// Cryptography - Ed25519
	Ed25519PrivateKey  *crypto.Ed25519PrivateKey
	Ed25519PrivateKey2 *crypto.Ed25519PrivateKey
	Ed25519PublicKey   *crypto.Ed25519PublicKey
	Ed25519PublicKey2  *crypto.Ed25519PublicKey
	Ed25519Signature   *crypto.Ed25519Signature
	Ed25519Signature2  *crypto.Ed25519Signature

	// Cryptography - Secp256k1
	Secp256k1PrivateKey  *crypto.Secp256k1PrivateKey
	Secp256k1PrivateKey2 *crypto.Secp256k1PrivateKey
	Secp256k1PublicKey   *crypto.Secp256k1PublicKey
	Secp256k1PublicKey2  *crypto.Secp256k1PublicKey
	Secp256k1Signature   *crypto.Secp256k1Signature
	Secp256k1Signature2  *crypto.Secp256k1Signature

	// Messages
	Message  []byte
	Message2 []byte

	// Accounts
	Account  *aptos.Account
	Account2 *aptos.Account
	Accounts []*aptos.Account

	// Multi-agent/Fee payer
	SecondarySigners   []*aptos.Account
	SecondaryAddresses []aptos.AccountAddress
	FeePayer           *aptos.Account

	// General storage
	Result    interface{}
	Error     error
	Bytes     []byte
	HexString string

	// Test vectors
	TestVectors map[string]interface{}
}

// NewWorld creates a new test world
func NewWorld() *World {
	return &World{
		NetworkURL:  "https://fullnode.testnet.aptoslabs.com/v1",
		Addresses:   make([]*aptos.AccountAddress, 0),
		TestVectors: make(map[string]interface{}),
	}
}

// Reset clears state between scenarios
func (w *World) Reset() {
	w.Client = nil
	w.Address = nil
	w.Addresses = make([]*aptos.AccountAddress, 0)
	// Ed25519
	w.Ed25519PrivateKey = nil
	w.Ed25519PrivateKey2 = nil
	w.Ed25519PublicKey = nil
	w.Ed25519PublicKey2 = nil
	w.Ed25519Signature = nil
	w.Ed25519Signature2 = nil
	// Secp256k1
	w.Secp256k1PrivateKey = nil
	w.Secp256k1PrivateKey2 = nil
	w.Secp256k1PublicKey = nil
	w.Secp256k1PublicKey2 = nil
	w.Secp256k1Signature = nil
	w.Secp256k1Signature2 = nil
	// Messages
	w.Message = nil
	w.Message2 = nil
	w.Account = nil
	w.Account2 = nil
	w.Accounts = make([]*aptos.Account, 0)
	w.SecondarySigners = make([]*aptos.Account, 0)
	w.SecondaryAddresses = make([]aptos.AccountAddress, 0)
	w.FeePayer = nil
	w.Result = nil
	w.Error = nil
	w.Bytes = nil
	w.HexString = ""
	w.TestVectors = make(map[string]interface{})
}

// SetError stores an error
func (w *World) SetError(err error) {
	w.Error = err
}

// ClearError clears the error state
func (w *World) ClearError() {
	w.Error = nil
}
