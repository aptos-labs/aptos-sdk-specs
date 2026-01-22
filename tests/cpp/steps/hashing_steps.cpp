/// Hashing step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/02-cryptography/hashing.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

#ifdef APTOS_SDK_AVAILABLE
#include <cryptopp/sha3.h>
#include <cryptopp/sha.h>
#include <cryptopp/filters.h>
#endif

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_input_bytes_hex, "input bytes from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.hash_input = vectors::hex_to_bytes(hex);
}

GIVEN(given_input_string, "input string {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string input = CUKE_ARG(1);
    world.hash_input = std::vector<uint8_t>(input.begin(), input.end());
}

GIVEN(given_empty_input, "an empty input")
{
    auto& world = cuke::context<TestWorld>();
    world.hash_input = std::vector<uint8_t>();
}

GIVEN(given_data_string, "data {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string input = CUKE_ARG(1);
    world.hash_input = std::vector<uint8_t>(input.begin(), input.end());
}

GIVEN(given_empty_data, "empty data")
{
    auto& world = cuke::context<TestWorld>();
    world.hash_input = std::vector<uint8_t>();
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_compute_sha3_256, "I compute the SHA3-256 hash")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hash_input) {
        world.set_error("No input bytes");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SHA3_256 hash;
    std::array<uint8_t, 32> digest;
    hash.CalculateDigest(digest.data(), world.hash_input->data(), world.hash_input->size());
    world.hash_result = digest;
#else
    // Placeholder - would use SHA3-256
    world.hash_result = std::array<uint8_t, 32>{};
#endif
}

WHEN(when_compute_sha2_256, "I compute the SHA2-256 hash")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hash_input) {
        world.set_error("No input bytes");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SHA256 hash;
    std::array<uint8_t, 32> digest;
    hash.CalculateDigest(digest.data(), world.hash_input->data(), world.hash_input->size());
    world.hash_result = digest;
#else
    // Placeholder
    world.hash_result = std::array<uint8_t, 32>{};
#endif
}

WHEN(when_hash_sha3_256_of_data, "I hash the data with SHA3-256")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hash_input) {
        world.set_error("No input bytes");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SHA3_256 hash;
    std::array<uint8_t, 32> digest;
    hash.CalculateDigest(digest.data(), world.hash_input->data(), world.hash_input->size());
    world.hash_result = digest;
#else
    world.hash_result = std::array<uint8_t, 32>{};
#endif
}

WHEN(when_hash_sha2_256_of_data, "I hash the data with SHA2-256")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hash_input) {
        world.set_error("No input bytes");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SHA256 hash;
    std::array<uint8_t, 32> digest;
    hash.CalculateDigest(digest.data(), world.hash_input->data(), world.hash_input->size());
    world.hash_result = digest;
#else
    world.hash_result = std::array<uint8_t, 32>{};
#endif
}

WHEN(when_hash_sha3_256_of_both_inputs, "I hash both inputs with SHA3-256")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hash_input) {
        world.set_error("No input bytes");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SHA3_256 hash1;
    std::array<uint8_t, 32> digest1;
    hash1.CalculateDigest(digest1.data(), world.hash_input->data(), world.hash_input->size());
    world.hash_result = digest1;
    
    if (world.hash_input2) {
        CryptoPP::SHA3_256 hash2;
        std::array<uint8_t, 32> digest2;
        hash2.CalculateDigest(digest2.data(), world.hash_input2->data(), world.hash_input2->size());
        world.hash_result2 = digest2;
    }
#endif
}

// =============================================================================
// Then Steps
// =============================================================================

THEN(then_hash_hex_should_be, "the hash hex should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.hash_result.has_value());
    
    std::string expected = CUKE_ARG(1);
    std::string actual = vectors::bytes_to_hex(
        std::vector<uint8_t>(world.hash_result->begin(), world.hash_result->end())
    );
    cuke::equal(actual, expected);
}

THEN(then_hash_should_be_32_bytes, "the hash should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.hash_result.has_value());
    cuke::equal(static_cast<int>(world.hash_result->size()), 32);
}

THEN(then_hashes_should_be_different, "the hashes should be different")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.hash_result.has_value());
    cuke::is_true(world.hash_result2.has_value());
    cuke::is_false(*world.hash_result == *world.hash_result2);
}

THEN(then_hashes_should_be_equal, "the hashes should be equal")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.hash_result.has_value());
    cuke::is_true(world.hash_result2.has_value());
    cuke::is_true(*world.hash_result == *world.hash_result2);
}
