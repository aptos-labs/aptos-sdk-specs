/// Placeholder implementations for Aptos SDK types.
/// These are only used when APTOS_SDK_AVAILABLE is not defined.
/// They allow the test scaffold to compile and run (tests will fail/skip).

#ifndef APTOS_SDK_AVAILABLE

#include "world.hpp"
#include <algorithm>
#include <random>
#include <sstream>
#include <iomanip>

namespace aptos::specs::placeholder {

// =============================================================================
// Helper Functions
// =============================================================================

namespace {

std::string bytes_to_hex(const uint8_t* data, size_t len) {
    std::ostringstream oss;
    oss << "0x";
    for (size_t i = 0; i < len; ++i) {
        oss << std::hex << std::setfill('0') << std::setw(2) 
            << static_cast<int>(data[i]);
    }
    return oss.str();
}

std::optional<std::vector<uint8_t>> hex_to_bytes(const std::string& hex) {
    std::string clean = hex;
    
    // Remove 0x prefix
    if (clean.size() >= 2 && clean[0] == '0' && (clean[1] == 'x' || clean[1] == 'X')) {
        clean = clean.substr(2);
    }
    
    // Check for invalid characters
    for (char c : clean) {
        if (!std::isxdigit(c)) {
            return std::nullopt;
        }
    }
    
    // Pad with leading zero if odd length
    if (clean.size() % 2 != 0) {
        clean = "0" + clean;
    }
    
    std::vector<uint8_t> bytes;
    bytes.reserve(clean.size() / 2);
    
    for (size_t i = 0; i < clean.size(); i += 2) {
        uint8_t byte = static_cast<uint8_t>(std::stoi(clean.substr(i, 2), nullptr, 16));
        bytes.push_back(byte);
    }
    
    return bytes;
}

} // anonymous namespace

// =============================================================================
// AccountAddress Implementation
// =============================================================================

std::optional<AccountAddress> AccountAddress::from_hex(const std::string& hex) {
    auto bytes_opt = hex_to_bytes(hex);
    if (!bytes_opt) {
        return std::nullopt;
    }
    
    auto& bytes = *bytes_opt;
    
    // Address must be at most 32 bytes
    if (bytes.size() > 32) {
        return std::nullopt;
    }
    
    AccountAddress addr;
    addr.bytes.fill(0);
    
    // Copy bytes to the end (right-aligned, zero-padded on left)
    size_t offset = 32 - bytes.size();
    std::copy(bytes.begin(), bytes.end(), addr.bytes.begin() + offset);
    
    return addr;
}

std::string AccountAddress::to_string_long() const {
    return bytes_to_hex(bytes.data(), bytes.size());
}

std::string AccountAddress::to_string_short() const {
    // Find first non-zero byte
    size_t first_nonzero = 0;
    while (first_nonzero < bytes.size() - 1 && bytes[first_nonzero] == 0) {
        ++first_nonzero;
    }
    
    std::ostringstream oss;
    oss << "0x";
    
    // Print first non-zero byte without leading zero if possible
    oss << std::hex << static_cast<int>(bytes[first_nonzero]);
    
    // Print remaining bytes with full width
    for (size_t i = first_nonzero + 1; i < bytes.size(); ++i) {
        oss << std::setfill('0') << std::setw(2) << static_cast<int>(bytes[i]);
    }
    
    return oss.str();
}

// =============================================================================
// Ed25519 Implementation
// =============================================================================

Ed25519PrivateKey Ed25519PrivateKey::generate() {
    Ed25519PrivateKey key;
    
    // Generate random bytes (NOT cryptographically secure - placeholder only!)
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 255);
    
    for (auto& byte : key.bytes) {
        byte = static_cast<uint8_t>(dis(gen));
    }
    
    return key;
}

std::optional<Ed25519PrivateKey> Ed25519PrivateKey::from_bytes(const std::vector<uint8_t>& bytes) {
    if (bytes.size() != 32) {
        return std::nullopt;
    }
    
    Ed25519PrivateKey key;
    std::copy(bytes.begin(), bytes.end(), key.bytes.begin());
    return key;
}

} // namespace aptos::specs::placeholder

#endif // APTOS_SDK_AVAILABLE
