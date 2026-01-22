/// Address step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/01-core-types/address.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_hex_string, "a hex string {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string value = CUKE_ARG(1);
    world.hex_string = value;
}

GIVEN(given_short_address, "a short address {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string value = CUKE_ARG(1);
    world.hex_string = value;
}

GIVEN(given_full_address, "a full address {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string value = CUKE_ARG(1);
    world.hex_string = value;
}

GIVEN(given_valid_account_address, "a valid AccountAddress")
{
    auto& world = cuke::context<TestWorld>();
    world.hex_string = std::string("0x1");
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_parse_as_account_address, "I parse it as an AccountAddress")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hex_string) {
        world.set_error("No hex string provided");
        return;
    }
    
    auto result = AccountAddress::from_hex(*world.hex_string);
    if (result) {
        world.address = *result;
    } else {
        world.set_error("Failed to parse address");
    }
}

WHEN(when_parse_address, "I parse the address")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hex_string) {
        world.set_error("No hex string provided");
        return;
    }
    
    auto result = AccountAddress::from_hex(*world.hex_string);
    if (result) {
        world.address = *result;
    } else {
        world.set_error("Failed to parse address");
    }
}

WHEN(when_convert_to_full_hex, "I convert it to a full hex string")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
    world.formatted_string = world.address->to_string_long();
}

WHEN(when_serialize_address_bcs, "I serialize the address with BCS")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
    world.bcs_bytes = std::vector<uint8_t>(
        world.address->bytes.begin(), 
        world.address->bytes.end()
    );
}

// =============================================================================
// Then Steps
// =============================================================================

THEN(then_parsing_should_succeed, "the parsing should succeed")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    cuke::is_false(world.has_error());
}

THEN(then_parsing_should_fail, "the parsing should fail")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.has_error() || !world.address.has_value());
}

THEN(then_should_get_valid_address, "I should get a valid AccountAddress")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
}

THEN(then_full_hex_should_be, "the full hex representation should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
    std::string expected = CUKE_ARG(1);
    std::string actual = world.address->to_string_long();
    cuke::equal(actual, expected);
}

THEN(then_formatted_string_should_be, "the formatted string should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.formatted_string.has_value());
    
    std::string expected = CUKE_ARG(1);
    cuke::equal(*world.formatted_string, expected);
}

THEN(then_error_should_contain, "the error message should contain {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.has_error());
    
    std::string expected_substring = CUKE_ARG(1);
    auto error = world.get_error();
    cuke::is_true(error.has_value());
    bool contains = error->find(expected_substring) != std::string::npos;
    cuke::is_true(contains, "Error message does not contain expected substring");
}
