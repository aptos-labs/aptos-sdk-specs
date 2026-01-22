#pragma once

/// Test world - holds state between Cucumber steps.
///
/// This follows the same pattern as the Rust implementation in
/// tests/rust/src/support/world.rs

#include <array>
#include <cstdint>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

// =============================================================================
// SDK Integration
// =============================================================================
// When APTOS_SDK_AVAILABLE is defined (set via CMake), include actual SDK headers.
// Otherwise, use placeholder types that allow the test scaffold to compile.

#ifdef APTOS_SDK_AVAILABLE
// Include actual Aptos C++ SDK headers
// Adjust these paths based on the actual SDK structure once available
#include <aptos/account_address.hpp>
#include <aptos/crypto/ed25519.hpp>
#include <aptos/crypto/secp256k1.hpp>
#include <aptos/crypto/secp256r1.hpp>
#include <aptos/transaction.hpp>
#include <aptos/bcs.hpp>
#endif

namespace aptos::specs {

#ifndef APTOS_SDK_AVAILABLE
/// Placeholder types until the Aptos C++ SDK is integrated.
/// These allow the test scaffold to compile without the SDK.
/// Once SDK is available, set APTOS_SDK_AVAILABLE=1 in CMake.
namespace placeholder {

struct AccountAddress {
    std::array<uint8_t, 32> bytes;
    
    static std::optional<AccountAddress> from_hex(const std::string& hex);
    std::string to_string_long() const;
    std::string to_string_short() const;
};

struct Ed25519PrivateKey {
    std::array<uint8_t, 32> bytes;
    
    static Ed25519PrivateKey generate();
    static std::optional<Ed25519PrivateKey> from_bytes(const std::vector<uint8_t>& bytes);
};

struct Ed25519PublicKey {
    std::array<uint8_t, 32> bytes;
};

struct Ed25519Signature {
    std::array<uint8_t, 64> bytes;
};

struct Secp256k1PrivateKey {
    std::array<uint8_t, 32> bytes;
};

struct Secp256k1PublicKey {
    std::vector<uint8_t> bytes; // 33 or 65 bytes depending on compression
};

struct Secp256k1Signature {
    std::vector<uint8_t> bytes;
};

struct Secp256r1PrivateKey {
    std::array<uint8_t, 32> bytes;
};

struct Secp256r1PublicKey {
    std::vector<uint8_t> bytes;
};

struct Secp256r1Signature {
    std::vector<uint8_t> bytes;
};

struct TypeTag {
    std::string type_string;
};

struct RawTransaction {};
struct SignedTransaction {};
struct TransactionPayload {};

} // namespace placeholder
#endif // APTOS_SDK_AVAILABLE

// =============================================================================
// Type Aliases
// =============================================================================
// When SDK is available, these should point to actual SDK types.
// For now, they use placeholder types.

#ifdef APTOS_SDK_AVAILABLE
// Use actual SDK types (adjust namespaces based on SDK structure)
using AccountAddress = aptos::AccountAddress;
using Ed25519PrivateKey = aptos::crypto::Ed25519PrivateKey;
using Ed25519PublicKey = aptos::crypto::Ed25519PublicKey;
using Ed25519Signature = aptos::crypto::Ed25519Signature;
using Secp256k1PrivateKey = aptos::crypto::Secp256k1PrivateKey;
using Secp256k1PublicKey = aptos::crypto::Secp256k1PublicKey;
using Secp256k1Signature = aptos::crypto::Secp256k1Signature;
using Secp256r1PrivateKey = aptos::crypto::Secp256r1PrivateKey;
using Secp256r1PublicKey = aptos::crypto::Secp256r1PublicKey;
using Secp256r1Signature = aptos::crypto::Secp256r1Signature;
using TypeTag = aptos::TypeTag;
using RawTransaction = aptos::RawTransaction;
using SignedTransaction = aptos::SignedTransaction;
using TransactionPayload = aptos::TransactionPayload;
#else
// Use placeholder types
using AccountAddress = placeholder::AccountAddress;
using Ed25519PrivateKey = placeholder::Ed25519PrivateKey;
using Ed25519PublicKey = placeholder::Ed25519PublicKey;
using Ed25519Signature = placeholder::Ed25519Signature;
using Secp256k1PrivateKey = placeholder::Secp256k1PrivateKey;
using Secp256k1PublicKey = placeholder::Secp256k1PublicKey;
using Secp256k1Signature = placeholder::Secp256k1Signature;
using Secp256r1PrivateKey = placeholder::Secp256r1PrivateKey;
using Secp256r1PublicKey = placeholder::Secp256r1PublicKey;
using Secp256r1Signature = placeholder::Secp256r1Signature;
using TypeTag = placeholder::TypeTag;
using RawTransaction = placeholder::RawTransaction;
using SignedTransaction = placeholder::SignedTransaction;
using TransactionPayload = placeholder::TransactionPayload;
#endif // APTOS_SDK_AVAILABLE

/// The test world holds state between Cucumber steps within a scenario.
struct TestWorld {
    // =========================================================================
    // Address State
    // =========================================================================
    
    /// The current hex string input.
    std::optional<std::string> hex_string;
    
    /// The parsed address result (success or error message).
    std::optional<AccountAddress> address;
    
    /// A second address for comparison.
    std::optional<AccountAddress> address2;
    
    /// BCS serialized bytes.
    std::optional<std::vector<uint8_t>> bcs_bytes;
    
    /// Formatted string result.
    std::optional<std::string> formatted_string;
    
    // =========================================================================
    // Cryptography State
    // =========================================================================
    
    /// Ed25519 private key.
    std::optional<Ed25519PrivateKey> ed25519_private_key;
    
    /// Ed25519 public key.
    std::optional<Ed25519PublicKey> ed25519_public_key;
    
    /// Second Ed25519 key pair for comparison.
    std::optional<Ed25519PrivateKey> ed25519_private_key2;
    std::optional<Ed25519PublicKey> ed25519_public_key2;
    
    /// Current message to sign.
    std::optional<std::vector<uint8_t>> message;
    
    /// Second message for comparison.
    std::optional<std::vector<uint8_t>> message2;
    
    /// Ed25519 signature.
    std::optional<Ed25519Signature> ed25519_signature;
    
    /// Second signature for comparison.
    std::optional<Ed25519Signature> ed25519_signature2;
    
    /// Seed bytes for key derivation.
    std::optional<std::vector<uint8_t>> seed_bytes;
    
    /// Private key bytes (for creating keys from bytes).
    std::optional<std::vector<uint8_t>> private_key_bytes;
    
    // =========================================================================
    // Secp256k1 State
    // =========================================================================
    
    std::optional<Secp256k1PrivateKey> secp256k1_private_key;
    std::optional<Secp256k1PublicKey> secp256k1_public_key;
    std::optional<Secp256k1PrivateKey> secp256k1_private_key2;
    std::optional<Secp256k1PublicKey> secp256k1_public_key2;
    std::optional<Secp256k1Signature> secp256k1_signature;
    std::optional<Secp256k1Signature> secp256k1_signature2;
    
    // =========================================================================
    // Secp256r1 State
    // =========================================================================
    
    std::optional<Secp256r1PrivateKey> secp256r1_private_key;
    std::optional<Secp256r1PublicKey> secp256r1_public_key;
    std::optional<Secp256r1PrivateKey> secp256r1_private_key2;
    std::optional<Secp256r1PublicKey> secp256r1_public_key2;
    std::optional<Secp256r1Signature> secp256r1_signature;
    std::optional<Secp256r1Signature> secp256r1_signature2;
    
    // =========================================================================
    // Account State
    // =========================================================================
    
    /// Authentication key bytes.
    std::optional<std::vector<uint8_t>> auth_key_bytes;
    
    // =========================================================================
    // Type Tag State
    // =========================================================================
    
    std::optional<std::string> type_tag_string;
    std::optional<std::string> type_string;
    std::optional<std::string> module_string;
    std::optional<TypeTag> type_tag;
    std::optional<TypeTag> type_tag_deserialized;
    
    // =========================================================================
    // Transaction State
    // =========================================================================
    
    std::optional<std::vector<uint8_t>> raw_transaction_bytes;
    std::optional<std::vector<uint8_t>> signed_transaction_bytes;
    std::optional<std::array<uint8_t, 32>> transaction_hash;
    std::optional<std::array<uint8_t, 32>> transaction_hash2;
    std::optional<RawTransaction> raw_transaction;
    std::optional<RawTransaction> raw_transaction2;
    std::optional<SignedTransaction> signed_transaction;
    std::optional<SignedTransaction> signed_transaction2;
    std::optional<AccountAddress> tx_sender;
    std::optional<uint64_t> tx_sequence_number;
    std::optional<TransactionPayload> tx_payload;
    std::optional<uint64_t> tx_max_gas;
    std::optional<uint64_t> tx_gas_price;
    std::optional<uint64_t> tx_expiration;
    std::optional<uint8_t> tx_chain_id;
    std::optional<std::vector<uint8_t>> signing_message;
    std::optional<std::vector<uint8_t>> signing_message2;
    
    // =========================================================================
    // Serialization State
    // =========================================================================
    
    std::optional<bool> bool_value;
    std::optional<uint8_t> u8_value;
    std::optional<uint16_t> u16_value;
    std::optional<uint32_t> u32_value;
    std::optional<uint64_t> u64_value;
    std::optional<__uint128_t> u128_value;
    std::optional<std::array<uint8_t, 32>> u256_value;
    std::optional<std::vector<uint8_t>> bytes_value;
    std::optional<std::vector<uint8_t>> vec_u8_value;
    std::optional<std::vector<uint64_t>> vec_u64_value;
    std::optional<std::vector<std::vector<uint8_t>>> vec_vec_u8_value;
    std::optional<std::optional<uint64_t>> option_u64_value;
    std::optional<std::vector<uint8_t>> serialized_bytes;
    std::optional<std::vector<uint8_t>> serialized_bytes2;
    std::optional<size_t> uleb_value;
    std::optional<size_t> uleb_decoded;
    
    // =========================================================================
    // Hashing State
    // =========================================================================
    
    std::optional<std::vector<uint8_t>> hash_input;
    std::optional<std::vector<uint8_t>> hash_input2;
    std::optional<std::vector<std::vector<uint8_t>>> hash_parts;
    std::optional<std::array<uint8_t, 32>> hash_result;
    std::optional<std::array<uint8_t, 32>> hash_result2;
    std::optional<std::string> domain_string;
    std::optional<std::string> domain_string2;
    
    // =========================================================================
    // Error State
    // =========================================================================
    
    /// Error from the last operation.
    std::optional<std::string> last_error;
    
    /// Generic error storage.
    std::optional<std::string> error;
    
    // =========================================================================
    // Generic State
    // =========================================================================
    
    std::optional<std::vector<uint8_t>> bytes;
    std::optional<std::string> string_value;
    std::optional<bool> bool_result;
    std::unordered_map<std::string, std::string> named_values;
    
    // =========================================================================
    // Methods
    // =========================================================================
    
    /// Clear all state for a new scenario.
    void reset() {
        *this = TestWorld{};
    }
    
    /// Store an error message.
    void set_error(const std::string& err) {
        last_error = err;
    }
    
    /// Check if there was an error.
    bool has_error() const {
        return last_error.has_value() || error.has_value();
    }
    
    /// Get the last error message.
    std::optional<std::string> get_error() const {
        return last_error;
    }
    
    /// Clear the last error.
    void clear_error() {
        last_error = std::nullopt;
    }
};

/// Global test world instance for the current scenario.
/// CWT-Cucumber uses cuke::context<T>() for this, but we provide
/// a convenience accessor.
TestWorld& get_world();

} // namespace aptos::specs
