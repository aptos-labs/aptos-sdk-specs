package main

import (
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
)

const vectorsDir = "../../test-vectors"

// AddressVector represents an address parsing test vector
type AddressVector struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Input       string `json:"input"`
	Expected    struct {
		FullHex     string `json:"full_hex"`
		ShortString string `json:"short_string"`
		BytesHex    string `json:"bytes_hex"`
		LastByte    int    `json:"last_byte"`
	} `json:"expected"`
}

// MnemonicVector represents a mnemonic derivation test vector
type MnemonicVector struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Input       struct {
		Mnemonic       string `json:"mnemonic"`
		Passphrase     string `json:"passphrase"`
		DerivationPath string `json:"derivation_path"`
	} `json:"input"`
	Expected struct {
		SeedHex       string `json:"seed_hex"`
		PrivateKeyHex string `json:"private_key_hex"`
		PublicKeyHex  string `json:"public_key_hex"`
		AuthKeyHex    string `json:"auth_key_hex"`
		Address       string `json:"address"`
	} `json:"expected"`
}

// HashVector represents a hash test vector
type HashVector struct {
	Name        string `json:"name"`
	Input       string `json:"input"`
	InputHex    string `json:"input_hex"`
	ExpectedHex string `json:"expected_hex"`
}

// BcsVector represents a BCS encoding test vector
type BcsVector struct {
	Name   string      `json:"name"`
	Type   string      `json:"type"`
	Value  interface{} `json:"value"`
	BcsHex string      `json:"bcs_hex"`
}

// loadVectorFile loads a JSON test vector file
func loadVectorFile(filename string) (map[string]interface{}, error) {
	path := filepath.Join(vectorsDir, filename)
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var result map[string]interface{}
	err = json.Unmarshal(data, &result)
	return result, err
}

// GetAddressVectors loads address test vectors
func GetAddressVectors() (map[string]interface{}, error) {
	return loadVectorFile("addresses.json")
}

// GetAddressParsingVectors returns address parsing vectors
func GetAddressParsingVectors() ([]AddressVector, error) {
	data, err := GetAddressVectors()
	if err != nil {
		return nil, err
	}

	vectorsRaw, ok := data["parsing_vectors"].([]interface{})
	if !ok {
		return nil, nil
	}

	var vectors []AddressVector
	for _, v := range vectorsRaw {
		jsonBytes, _ := json.Marshal(v)
		var av AddressVector
		json.Unmarshal(jsonBytes, &av)
		vectors = append(vectors, av)
	}
	return vectors, nil
}

// GetMnemonicVectors loads mnemonic test vectors
func GetMnemonicVectors() (map[string]interface{}, error) {
	return loadVectorFile("mnemonics.json")
}

// GetEd25519DerivationVectors returns Ed25519 derivation vectors
func GetEd25519DerivationVectors() ([]MnemonicVector, error) {
	data, err := GetMnemonicVectors()
	if err != nil {
		return nil, err
	}

	vectorsRaw, ok := data["ed25519_derivation_vectors"].([]interface{})
	if !ok {
		return nil, nil
	}

	var vectors []MnemonicVector
	for _, v := range vectorsRaw {
		jsonBytes, _ := json.Marshal(v)
		var mv MnemonicVector
		json.Unmarshal(jsonBytes, &mv)
		vectors = append(vectors, mv)
	}
	return vectors, nil
}

// GetSignatureVectors loads signature test vectors
func GetSignatureVectors() (map[string]interface{}, error) {
	return loadVectorFile("signatures.json")
}

// GetSha3256Vectors returns SHA3-256 hash vectors
func GetSha3256Vectors() ([]HashVector, error) {
	data, err := GetSignatureVectors()
	if err != nil {
		return nil, err
	}

	hashing, ok := data["hashing"].(map[string]interface{})
	if !ok {
		return nil, nil
	}

	vectorsRaw, ok := hashing["sha3_256"].([]interface{})
	if !ok {
		return nil, nil
	}

	var vectors []HashVector
	for _, v := range vectorsRaw {
		jsonBytes, _ := json.Marshal(v)
		var hv HashVector
		json.Unmarshal(jsonBytes, &hv)
		vectors = append(vectors, hv)
	}
	return vectors, nil
}

// GetBcsVectors loads BCS encoding test vectors
func GetBcsVectors() (map[string]interface{}, error) {
	return loadVectorFile("bcs.json")
}

// HexToBytes converts a hex string to bytes
func HexToBytes(hexStr string) ([]byte, error) {
	cleanHex := strings.TrimPrefix(hexStr, "0x")
	return hex.DecodeString(cleanHex)
}

// BytesToHex converts bytes to a hex string with 0x prefix
func BytesToHex(data []byte) string {
	return "0x" + hex.EncodeToString(data)
}

