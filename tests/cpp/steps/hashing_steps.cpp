/// Hashing step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/02-cryptography/hashing.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

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
    // TODO: Implement with actual SDK
    world.hash_result = std::array<uint8_t, 32>{};
}

WHEN(when_compute_sha2_256, "I compute the SHA2-256 hash")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hash_input) {
        world.set_error("No input bytes");
        return;
    }
    // TODO: Implement with actual SDK
    world.hash_result = std::array<uint8_t, 32>{};
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
