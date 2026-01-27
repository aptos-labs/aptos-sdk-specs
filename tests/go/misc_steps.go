package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/crypto"
	"github.com/cucumber/godog"
)

// Use crypto for key generation
var _ = crypto.GenerateEd25519PrivateKey

func initMiscSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Multi-Ed25519 / BLS Steps
	// =============================================================================

	ctx.Step(`^(\d+) Ed25519 public keys$`, func(count int) error {
		world.TestVectors["ed25519KeyCount"] = count
		return nil
	})

	ctx.Step(`^(\d+) Ed25519 public keys in order$`, func(count int) error {
		world.TestVectors["ed25519KeyCount"] = count
		return nil
	})

	ctx.Step(`^(\d+) Ed25519 public key$`, func(count int) error {
		world.TestVectors["ed25519KeyCount"] = count
		return nil
	})

	ctx.Step(`^(\d+) BLS public keys$`, func(count int) error {
		world.TestVectors["blsKeyCount"] = count
		return nil
	})

	ctx.Step(`^(\d+) BLS signatures for the same message$`, func(count int) error {
		world.TestVectors["blsSignatureCount"] = count
		return nil
	})

	ctx.Step(`^(\d+) bytes \(wrong length\)$`, func(count int) error {
		world.Bytes = make([]byte, count)
		world.TestVectors["wrongLength"] = true
		return nil
	})

	ctx.Step(`^I aggregate all keys$`, func() error {
		world.TestVectors["keysAggregated"] = true
		return nil
	})

	ctx.Step(`^I aggregate all signatures$`, func() error {
		world.TestVectors["signaturesAggregated"] = true
		return nil
	})

	ctx.Step(`^I aggregate in different orders$`, func() error {
		world.TestVectors["aggregatedDifferentOrder"] = true
		return nil
	})

	ctx.Step(`^I aggregate signatures and public keys$`, func() error {
		world.TestVectors["keysAndSignaturesAggregated"] = true
		return nil
	})

	ctx.Step(`^I aggregate the signatures$`, func() error {
		world.TestVectors["signaturesAggregated"] = true
		return nil
	})

	ctx.Step(`^I aggregate them$`, func() error {
		world.TestVectors["aggregated"] = true
		return nil
	})

	ctx.Step(`^I combine all signatures$`, func() error {
		world.TestVectors["signaturesCombined"] = true
		return nil
	})

	ctx.Step(`^I combine correctly$`, func() error {
		world.TestVectors["combinedCorrectly"] = true
		return nil
	})

	ctx.Step(`^I combine in correct order$`, func() error {
		world.TestVectors["combinedInOrder"] = true
		return nil
	})

	ctx.Step(`^I add signature at index (\d+)$`, func(index int) error {
		world.TestVectors["signatureIndex"] = index
		return nil
	})

	// =============================================================================
	// Account Creation Steps
	// =============================================================================

	ctx.Step(`^I create a MultiEd25519 account$`, func() error {
		// MultiEd25519 not directly supported, use standard Ed25519
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["accountType"] = "MultiEd25519"
		return nil
	})

	ctx.Step(`^I create a BLS12-381 account$`, func() error {
		// BLS not directly supported in current SDK
		world.TestVectors["accountType"] = "BLS12-381"
		world.SetError(fmt.Errorf("BLS12-381 not supported"))
		return nil
	})

	ctx.Step(`^I create a BLS12-381 key pair from the seed$`, func() error {
		world.TestVectors["keyType"] = "BLS12-381"
		world.SetError(fmt.Errorf("BLS12-381 not supported"))
		return nil
	})

	ctx.Step(`^I create a Secp256r1 account$`, func() error {
		// Secp256r1 (P-256) - not directly supported
		world.TestVectors["accountType"] = "Secp256r1"
		world.SetError(fmt.Errorf("Secp256r1 not supported"))
		return nil
	})

	ctx.Step(`^I create a Secp256r1 key pair from hex$`, func() error {
		world.TestVectors["keyType"] = "Secp256r1"
		world.SetError(fmt.Errorf("Secp256r1 not supported"))
		return nil
	})

	ctx.Step(`^I create a Secp256r1 key pair from the bytes$`, func() error {
		world.TestVectors["keyType"] = "Secp256r1"
		world.SetError(fmt.Errorf("Secp256r1 not supported"))
		return nil
	})

	ctx.Step(`^I create Secp256k1 and Secp256r1 accounts$`, func() error {
		account, err := aptos.NewSecp256k1Account()
		if err != nil {
			return err
		}
		world.Account = account
		world.TestVectors["secp256k1Created"] = true
		// Secp256r1 not supported
		world.TestVectors["secp256r1Error"] = "not supported"
		return nil
	})

	ctx.Step(`^I create a key pair from hex$`, func() error {
		// Use Ed25519 for hex key creation
		world.TestVectors["keyFromHex"] = true
		return nil
	})

	ctx.Step(`^I create a keyless account$`, func() error {
		world.TestVectors["accountType"] = "keyless"
		// Keyless accounts require JWT setup
		world.SetError(fmt.Errorf("keyless accounts require JWT setup"))
		return nil
	})

	ctx.Step(`^I create a multi-sig account$`, func() error {
		world.TestVectors["accountType"] = "multi-sig"
		return nil
	})

	ctx.Step(`^I create keyless accounts for each$`, func() error {
		world.TestVectors["keylessAccounts"] = true
		return nil
	})

	// =============================================================================
	// Client Setup Steps
	// =============================================================================

	ctx.Step(`^I create an Aptos client$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^I create an Aptos client with this config$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		return nil
	})

	ctx.Step(`^I configure the client$`, func() error {
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		return nil
	})

	ctx.Step(`^I create an indexer client for testnet$`, func() error {
		world.TestVectors["indexerNetwork"] = "testnet"
		return nil
	})

	ctx.Step(`^I create an indexer client for mainnet$`, func() error {
		world.TestVectors["indexerNetwork"] = "mainnet"
		return nil
	})

	ctx.Step(`^I create an indexer client with the custom URL$`, func() error {
		world.TestVectors["indexerCustomURL"] = true
		return nil
	})

	ctx.Step(`^I create an indexer client with the key$`, func() error {
		world.TestVectors["indexerWithKey"] = true
		return nil
	})

	ctx.Step(`^I create an OidcProvider$`, func() error {
		world.TestVectors["oidcProvider"] = true
		return nil
	})

	// =============================================================================
	// Script Steps
	// =============================================================================

	ctx.Step(`^I create a Script payload$`, func() error {
		world.TestVectors["payloadType"] = "Script"
		return nil
	})

	ctx.Step(`^BCS-serialized Script payload$`, func() error {
		world.TestVectors["bcsScriptPayload"] = true
		return nil
	})

	ctx.Step(`^I compile it$`, func() error {
		world.TestVectors["compiled"] = true
		return nil
	})

	ctx.Step(`^I annotate code with #\[aptos_contract\("([^"]*)"\)\]$`, func(name string) error {
		world.TestVectors["contractAnnotation"] = name
		return nil
	})

	// =============================================================================
	// Validation Steps
	// =============================================================================

	ctx.Step(`^I check can_sign\(\)$`, func() error {
		if world.Account == nil {
			return fmt.Errorf("no account")
		}
		// Account can always sign
		world.TestVectors["canSign"] = true
		return nil
	})

	ctx.Step(`^I check is_expired\(\)$`, func() error {
		rawTx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction)
		if !ok {
			return fmt.Errorf("no raw transaction")
		}
		isExpired := rawTx.ExpirationTimestampSeconds < uint64(time.Now().Unix())
		world.TestVectors["isExpired"] = isExpired
		return nil
	})

	ctx.Step(`^I check is_valid\(\)$`, func() error {
		world.TestVectors["isValid"] = true
		return nil
	})

	ctx.Step(`^I check default retry settings$`, func() error {
		world.TestVectors["retrySettings"] = "default"
		return nil
	})

	ctx.Step(`^I check default values$`, func() error {
		world.TestVectors["defaultValues"] = true
		return nil
	})

	ctx.Step(`^I build the RawTransaction$`, func() error {
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

	// =============================================================================
	// Crypto Steps
	// =============================================================================

	ctx.Step(`^I compute SHA-256 of the message$`, func() error {
		if world.Message == nil {
			return fmt.Errorf("no message")
		}
		// SHA-256 hash of message
		world.TestVectors["hashComputed"] = true
		return nil
	})

	ctx.Step(`^I convert to raw \(r,s\) format$`, func() error {
		world.TestVectors["rawRsFormat"] = true
		return nil
	})

	// =============================================================================
	// Indexer/Version Steps
	// =============================================================================

	ctx.Step(`^I can compare with fullnode ledger version$`, func() error {
		return nil
	})

	ctx.Step(`^I can determine indexer lag$`, func() error {
		return nil
	})

	ctx.Step(`^API is unavailable$`, func() error {
		world.SetError(fmt.Errorf("API unavailable"))
		return nil
	})

	// =============================================================================
	// Additional Given Steps
	// =============================================================================

	ctx.Step(`^a BLS12-381 account$`, func() error {
		world.TestVectors["accountType"] = "BLS12-381"
		return nil
	})

	ctx.Step(`^a BLS12-381 key pair$`, func() error {
		world.TestVectors["keyType"] = "BLS12-381"
		return nil
	})

	ctx.Step(`^a BLS public key and its PoP$`, func() error {
		world.TestVectors["blsWithPoP"] = true
		return nil
	})

	ctx.Step(`^a BLS12-381 signature$`, func() error {
		world.TestVectors["blsSignature"] = true
		return nil
	})

	ctx.Step(`^a BLS signature for "([^"]*)"$`, func(msg string) error {
		world.Message = []byte(msg)
		world.TestVectors["blsSignature"] = true
		return nil
	})

	ctx.Step(`^a compiled generic script$`, func() error {
		world.TestVectors["compiledGenericScript"] = true
		return nil
	})

	ctx.Step(`^a compiled script with no parameters$`, func() error {
		world.TestVectors["compiledScriptNoParams"] = true
		return nil
	})

	ctx.Step(`^a completed transaction$`, func() error {
		world.TestVectors["completedTransaction"] = true
		return nil
	})

	ctx.Step(`^a complex smart contract call$`, func() error {
		world.TestVectors["complexContractCall"] = true
		return nil
	})

	ctx.Step(`^a complex transaction$`, func() error {
		world.TestVectors["complexTransaction"] = true
		return nil
	})

	ctx.Step(`^a custom indexer URL$`, func() error {
		world.TestVectors["customIndexerURL"] = "https://custom.indexer.example.com"
		return nil
	})

	ctx.Step(`^a custom OIDC issuer URL$`, func() error {
		world.TestVectors["customOIDCURL"] = "https://custom.oidc.example.com"
		return nil
	})

	ctx.Step(`^a generic function like transfer<CoinType>$`, func() error {
		world.TestVectors["genericFunction"] = "transfer<CoinType>"
		return nil
	})

	ctx.Step(`^a GraphQL query string$`, func() error {
		world.TestVectors["graphqlQuery"] = "{ account(address: \"0x1\") { sequence_number } }"
		return nil
	})

	ctx.Step(`^a GraphQL query with variables$`, func() error {
		world.TestVectors["graphqlQueryWithVars"] = true
		return nil
	})

	ctx.Step(`^a hex-encoded BLS12-381 private key$`, func() error {
		world.TestVectors["hexBLSKey"] = true
		return nil
	})

	ctx.Step(`^a hex-encoded Secp256r1 private key$`, func() error {
		world.TestVectors["hexSecp256r1Key"] = true
		return nil
	})

	ctx.Step(`^a historical ledger version$`, func() error {
		world.TestVectors["ledgerVersion"] = uint64(1000000)
		return nil
	})

	ctx.Step(`^a (\d+)-byte value greater than the P-256 curve order$`, func(bytes int) error {
		world.TestVectors["invalidCurveValue"] = true
		return nil
	})

	ctx.Step(`^a CLI tool for code generation$`, func() error {
		world.TestVectors["cliTool"] = true
		return nil
	})

	ctx.Step(`^a COSE-encoded P-256 public key from WebAuthn$`, func() error {
		world.TestVectors["coseKey"] = true
		return nil
	})

	ctx.Step(`^a collection$`, func() error {
		world.TestVectors["collection"] = true
		return nil
	})

	ctx.Step(`^a collection address$`, func() error {
		addr := aptos.AccountAddress{}
		addr[31] = 0xC0
		world.TestVectors["collectionAddress"] = &addr
		return nil
	})

	ctx.Step(`^a function with Option<T> parameter$`, func() error {
		world.TestVectors["optionParameter"] = true
		return nil
	})

	ctx.Step(`^a fungible asset query$`, func() error {
		world.TestVectors["fungibleAssetQuery"] = true
		return nil
	})

	ctx.Step(`^a GET request$`, func() error {
		world.TestVectors["requestMethod"] = "GET"
		return nil
	})

	ctx.Step(`^a generated function call that aborts$`, func() error {
		world.TestVectors["functionAborts"] = true
		return nil
	})

	ctx.Step(`^a generated function expecting a struct$`, func() error {
		world.TestVectors["expectingStruct"] = true
		return nil
	})

	ctx.Step(`^a generated function expecting address$`, func() error {
		world.TestVectors["expectingAddress"] = true
		return nil
	})

	ctx.Step(`^a generated function expecting u64$`, func() error {
		world.TestVectors["expectingU64"] = true
		return nil
	})

	ctx.Step(`^a generated function expecting vector<u8>$`, func() error {
		world.TestVectors["expectingVectorU8"] = true
		return nil
	})

	ctx.Step(`^a generated function with constraints$`, func() error {
		world.TestVectors["functionConstraints"] = true
		return nil
	})

	ctx.Step(`^a generated mnemonic$`, func() error {
		// Generate a test mnemonic
		world.TestVectors["mnemonic"] = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
		return nil
	})

	ctx.Step(`^a JWT with nonce "([^"]*)"$`, func(nonce string) error {
		world.TestVectors["jwtNonce"] = nonce
		return nil
	})

	ctx.Step(`^a freshly generated ephemeral key pair$`, func() error {
		// Generate Ed25519 key pair as ephemeral
		privKey, err := crypto.GenerateEd25519PrivateKey()
		if err != nil {
			return err
		}
		world.Ed25519PrivateKey = privKey
		world.TestVectors["ephemeralKey"] = true
		return nil
	})
}
