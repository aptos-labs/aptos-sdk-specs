#include "vectors.hpp"

#include <filesystem>
#include <fstream>
#include <sstream>
#include <stdexcept>

namespace aptos::specs::vectors {

// =============================================================================
// Utility Functions
// =============================================================================

std::string get_vectors_dir() {
    // Try relative path from build directory
    std::filesystem::path paths[] = {
        "../../test-vectors",           // From build/
        "../../../test-vectors",        // From build/subdir/
        "test-vectors",                 // From repo root
    };
    
    for (const auto& path : paths) {
        if (std::filesystem::exists(path)) {
            return path.string();
        }
    }
    
    throw std::runtime_error("Could not find test-vectors directory");
}

nlohmann::json load_vector_file(const std::string& filename) {
    std::filesystem::path filepath = std::filesystem::path(get_vectors_dir()) / filename;
    
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open vector file: " + filepath.string());
    }
    
    nlohmann::json j;
    file >> j;
    return j;
}

std::vector<uint8_t> hex_to_bytes(const std::string& hex) {
    std::string clean_hex = hex;
    
    // Remove 0x prefix if present
    if (clean_hex.size() >= 2 && clean_hex[0] == '0' && (clean_hex[1] == 'x' || clean_hex[1] == 'X')) {
        clean_hex = clean_hex.substr(2);
    }
    
    // Pad with leading zero if odd length
    if (clean_hex.size() % 2 != 0) {
        clean_hex = "0" + clean_hex;
    }
    
    std::vector<uint8_t> bytes;
    bytes.reserve(clean_hex.size() / 2);
    
    for (size_t i = 0; i < clean_hex.size(); i += 2) {
        uint8_t byte = static_cast<uint8_t>(std::stoi(clean_hex.substr(i, 2), nullptr, 16));
        bytes.push_back(byte);
    }
    
    return bytes;
}

std::string bytes_to_hex(const std::vector<uint8_t>& bytes) {
    std::ostringstream oss;
    oss << "0x";
    for (uint8_t byte : bytes) {
        oss << std::hex << std::setfill('0') << std::setw(2) << static_cast<int>(byte);
    }
    return oss.str();
}

// =============================================================================
// Address Vectors
// =============================================================================

std::vector<AddressParsingVector> get_address_parsing_vectors() {
    auto json = load_vector_file("addresses.json");
    std::vector<AddressParsingVector> vectors;
    
    if (json.contains("valid_addresses")) {
        for (const auto& v : json["valid_addresses"]) {
            AddressParsingVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input = v["input"].get<std::string>();
            vec.expected.full_hex = v["expected"]["full_hex"].get<std::string>();
            vec.expected.short_hex = v["expected"].value("short_hex", "");
            if (v["expected"].contains("special_name")) {
                vec.expected.special_name = v["expected"]["special_name"].get<std::string>();
            }
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

std::vector<AddressInvalidVector> get_address_invalid_vectors() {
    auto json = load_vector_file("addresses.json");
    std::vector<AddressInvalidVector> vectors;
    
    if (json.contains("invalid_addresses")) {
        for (const auto& v : json["invalid_addresses"]) {
            AddressInvalidVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input = v["input"].get<std::string>();
            vec.error_contains = v.value("error_contains", "");
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

// =============================================================================
// Signature Vectors
// =============================================================================

std::vector<Ed25519SignatureVector> get_ed25519_signature_vectors() {
    auto json = load_vector_file("signatures.json");
    std::vector<Ed25519SignatureVector> vectors;
    
    if (json.contains("ed25519")) {
        for (const auto& v : json["ed25519"]) {
            Ed25519SignatureVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input.private_key_hex = v["input"]["private_key_hex"].get<std::string>();
            vec.input.message_hex = v["input"]["message_hex"].get<std::string>();
            vec.expected.public_key_hex = v["expected"]["public_key_hex"].get<std::string>();
            vec.expected.signature_hex = v["expected"]["signature_hex"].get<std::string>();
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

std::vector<Secp256k1SignatureVector> get_secp256k1_signature_vectors() {
    auto json = load_vector_file("signatures.json");
    std::vector<Secp256k1SignatureVector> vectors;
    
    if (json.contains("secp256k1")) {
        for (const auto& v : json["secp256k1"]) {
            Secp256k1SignatureVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input.private_key_hex = v["input"]["private_key_hex"].get<std::string>();
            vec.input.message_hex = v["input"]["message_hex"].get<std::string>();
            vec.expected.public_key_hex = v["expected"]["public_key_hex"].get<std::string>();
            vec.expected.signature_hex = v["expected"]["signature_hex"].get<std::string>();
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

// =============================================================================
// BCS Serialization Vectors
// =============================================================================

std::vector<BcsVector> get_bcs_vectors() {
    auto json = load_vector_file("bcs.json");
    std::vector<BcsVector> vectors;
    
    // BCS vectors may be organized by type
    for (const auto& [key, values] : json.items()) {
        if (key == "version" || key == "description") continue;
        
        if (values.is_array()) {
            for (const auto& v : values) {
                BcsVector vec;
                vec.name = v.value("name", "");
                vec.description = v.value("description", "");
                vec.type = key;
                vec.value = v["input"];
                vec.expected_hex = v["expected"]["bcs_hex"].get<std::string>();
                vectors.push_back(vec);
            }
        }
    }
    
    return vectors;
}

// =============================================================================
// Mnemonic Vectors
// =============================================================================

std::vector<MnemonicVector> get_mnemonic_vectors() {
    auto json = load_vector_file("mnemonics.json");
    std::vector<MnemonicVector> vectors;
    
    if (json.contains("derivations")) {
        for (const auto& v : json["derivations"]) {
            MnemonicVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input.mnemonic = v["input"]["mnemonic"].get<std::string>();
            vec.input.passphrase = v["input"].value("passphrase", "");
            vec.input.derivation_path = v["input"]["derivation_path"].get<std::string>();
            vec.expected.private_key_hex = v["expected"]["private_key_hex"].get<std::string>();
            vec.expected.public_key_hex = v["expected"]["public_key_hex"].get<std::string>();
            vec.expected.address = v["expected"]["address"].get<std::string>();
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

// =============================================================================
// Type Tag Vectors
// =============================================================================

std::vector<TypeTagVector> get_type_tag_vectors() {
    auto json = load_vector_file("type-tags.json");
    std::vector<TypeTagVector> vectors;
    
    if (json.contains("valid_type_tags")) {
        for (const auto& v : json["valid_type_tags"]) {
            TypeTagVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input = v["input"].get<std::string>();
            vec.expected.canonical = v["expected"]["canonical"].get<std::string>();
            vec.expected.bcs_hex = v["expected"].value("bcs_hex", "");
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

std::vector<TypeTagInvalidVector> get_type_tag_invalid_vectors() {
    auto json = load_vector_file("type-tags.json");
    std::vector<TypeTagInvalidVector> vectors;
    
    if (json.contains("invalid_type_tags")) {
        for (const auto& v : json["invalid_type_tags"]) {
            TypeTagInvalidVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input = v["input"].get<std::string>();
            vec.error_contains = v.value("error_contains", "");
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

// =============================================================================
// Transaction Vectors
// =============================================================================

std::vector<TransactionVector> get_transaction_vectors() {
    auto json = load_vector_file("transactions.json");
    std::vector<TransactionVector> vectors;
    
    if (json.contains("transactions")) {
        for (const auto& v : json["transactions"]) {
            TransactionVector vec;
            vec.name = v.value("name", "");
            vec.description = v.value("description", "");
            vec.input = v["input"];
            vec.expected.raw_transaction_bcs_hex = v["expected"].value("raw_transaction_bcs_hex", "");
            vec.expected.signing_message_hex = v["expected"].value("signing_message_hex", "");
            vec.expected.signed_transaction_bcs_hex = v["expected"].value("signed_transaction_bcs_hex", "");
            vec.expected.transaction_hash = v["expected"].value("transaction_hash", "");
            vectors.push_back(vec);
        }
    }
    
    return vectors;
}

} // namespace aptos::specs::vectors
