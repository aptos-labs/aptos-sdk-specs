#pragma once

/// Test vector loading utilities.
///
/// Loads JSON test vectors from ../test-vectors/*.json

#include <nlohmann/json.hpp>
#include <optional>
#include <string>
#include <vector>

namespace aptos::specs::vectors {

// =============================================================================
// Address Vectors
// =============================================================================

struct AddressExpected {
    std::string full_hex;
    std::string short_hex;
    std::optional<std::string> special_name;
};

struct AddressParsingVector {
    std::string name;
    std::string description;
    std::string input;
    AddressExpected expected;
};

struct AddressInvalidVector {
    std::string name;
    std::string description;
    std::string input;
    std::string error_contains;
};

std::vector<AddressParsingVector> get_address_parsing_vectors();
std::vector<AddressInvalidVector> get_address_invalid_vectors();

// =============================================================================
// Signature Vectors
// =============================================================================

struct Ed25519SignatureVector {
    std::string name;
    std::string description;
    struct {
        std::string private_key_hex;
        std::string message_hex;
    } input;
    struct {
        std::string public_key_hex;
        std::string signature_hex;
    } expected;
};

struct Secp256k1SignatureVector {
    std::string name;
    std::string description;
    struct {
        std::string private_key_hex;
        std::string message_hex;
    } input;
    struct {
        std::string public_key_hex;
        std::string signature_hex;
    } expected;
};

std::vector<Ed25519SignatureVector> get_ed25519_signature_vectors();
std::vector<Secp256k1SignatureVector> get_secp256k1_signature_vectors();

// =============================================================================
// BCS Serialization Vectors
// =============================================================================

struct BcsVector {
    std::string name;
    std::string description;
    std::string type;
    nlohmann::json value;
    std::string expected_hex;
};

std::vector<BcsVector> get_bcs_vectors();

// =============================================================================
// Mnemonic Vectors
// =============================================================================

struct MnemonicVector {
    std::string name;
    std::string description;
    struct {
        std::string mnemonic;
        std::string passphrase;
        std::string derivation_path;
    } input;
    struct {
        std::string private_key_hex;
        std::string public_key_hex;
        std::string address;
    } expected;
};

std::vector<MnemonicVector> get_mnemonic_vectors();

// =============================================================================
// Type Tag Vectors
// =============================================================================

struct TypeTagVector {
    std::string name;
    std::string description;
    std::string input;
    struct {
        std::string canonical;
        std::string bcs_hex;
    } expected;
};

struct TypeTagInvalidVector {
    std::string name;
    std::string description;
    std::string input;
    std::string error_contains;
};

std::vector<TypeTagVector> get_type_tag_vectors();
std::vector<TypeTagInvalidVector> get_type_tag_invalid_vectors();

// =============================================================================
// Transaction Vectors
// =============================================================================

struct TransactionVector {
    std::string name;
    std::string description;
    nlohmann::json input;
    struct {
        std::string raw_transaction_bcs_hex;
        std::string signing_message_hex;
        std::string signed_transaction_bcs_hex;
        std::string transaction_hash;
    } expected;
};

std::vector<TransactionVector> get_transaction_vectors();

// =============================================================================
// Utility Functions
// =============================================================================

/// Get the path to the test vectors directory.
std::string get_vectors_dir();

/// Load a JSON file from the test vectors directory.
nlohmann::json load_vector_file(const std::string& filename);

/// Convert hex string to bytes.
std::vector<uint8_t> hex_to_bytes(const std::string& hex);

/// Convert bytes to hex string.
std::string bytes_to_hex(const std::vector<uint8_t>& bytes);

} // namespace aptos::specs::vectors
