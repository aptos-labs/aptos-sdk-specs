/// BCS Serialization step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/01-core-types/serialization.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_bool_value, "a boolean value {word}")
{
    auto& world = cuke::context<TestWorld>();
    std::string val = CUKE_ARG(1);
    world.bool_value = (val == "true");
}

GIVEN(given_u8_value, "a u8 value {int}")
{
    auto& world = cuke::context<TestWorld>();
    int val = CUKE_ARG(1);
    world.u8_value = static_cast<uint8_t>(val);
}

GIVEN(given_u64_value, "a u64 value {int}")
{
    auto& world = cuke::context<TestWorld>();
    int val = CUKE_ARG(1);
    world.u64_value = static_cast<uint64_t>(val);
}

GIVEN(given_bytes_hex, "bytes from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.bytes_value = vectors::hex_to_bytes(hex);
}

GIVEN(given_string_value, "a string {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string value = CUKE_ARG(1);
    world.string_value = value;
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_serialize_bool_bcs, "I serialize the boolean with BCS")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.bool_value) {
        world.set_error("No boolean value");
        return;
    }
    world.serialized_bytes = std::vector<uint8_t>{*world.bool_value ? uint8_t(1) : uint8_t(0)};
}

WHEN(when_serialize_u8_bcs, "I serialize the u8 with BCS")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.u8_value) {
        world.set_error("No u8 value");
        return;
    }
    world.serialized_bytes = std::vector<uint8_t>{*world.u8_value};
}

WHEN(when_serialize_u64_bcs, "I serialize the u64 with BCS")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.u64_value) {
        world.set_error("No u64 value");
        return;
    }
    uint64_t val = *world.u64_value;
    std::vector<uint8_t> bytes(8);
    for (int i = 0; i < 8; i++) {
        bytes[i] = static_cast<uint8_t>((val >> (8 * i)) & 0xFF);
    }
    world.serialized_bytes = bytes;
}

// =============================================================================
// Then Steps
// =============================================================================

THEN(then_serialized_hex_should_be, "the serialized hex should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.serialized_bytes.has_value());
    
    std::string expected = CUKE_ARG(1);
    std::string actual = vectors::bytes_to_hex(*world.serialized_bytes);
    cuke::equal(actual, expected);
}
