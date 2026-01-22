/// Address step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/01-core-types/address.feature

#include <cucumber.hpp>
#include <iomanip>
#include <sstream>

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

GIVEN(given_address_with_value, "an AccountAddress with value {int}")
{
    auto& world = cuke::context<TestWorld>();
    int value = CUKE_ARG(1);
    // Create address with the given value
    std::stringstream ss;
    ss << "0x" << std::hex << value;
    world.hex_string = ss.str();
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex(*world.hex_string);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto result = AccountAddress::from_hex(*world.hex_string);
    if (result) {
        world.address = *result;
    }
#endif
}

GIVEN(given_address_from_hex, "an AccountAddress from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.hex_string = hex;
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex(hex);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto result = AccountAddress::from_hex(hex);
    if (result) {
        world.address = *result;
    } else {
        world.set_error("Failed to parse address");
    }
#endif
}

GIVEN(given_another_address_from_hex, "another AccountAddress from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address2 = AccountAddress::FromHex(hex);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto result = AccountAddress::from_hex(hex);
    if (result) {
        world.address2 = *result;
    } else {
        world.set_error("Failed to parse address");
    }
#endif
}

GIVEN(given_zero_address_constant, "the ZERO address constant")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex("0x0");
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.address = AccountAddress::from_hex("0x0");
#endif
}

GIVEN(given_one_address_constant, "the ONE address constant")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex("0x1");
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.address = AccountAddress::from_hex("0x1");
#endif
}

GIVEN(given_three_address_constant, "the THREE address constant")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex("0x3");
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.address = AccountAddress::from_hex("0x3");
#endif
}

GIVEN(given_four_address_constant, "the FOUR address constant")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex("0x4");
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.address = AccountAddress::from_hex("0x4");
#endif
}

GIVEN(given_32_bytes_with_last_byte, "32 bytes with value {int} in the last byte")
{
    auto& world = cuke::context<TestWorld>();
    int value = CUKE_ARG(1);
    std::vector<uint8_t> bytes(32, 0);
    bytes[31] = static_cast<uint8_t>(value);
    world.bcs_bytes = bytes;
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
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex(*world.hex_string);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto result = AccountAddress::from_hex(*world.hex_string);
    if (result) {
        world.address = *result;
    } else {
        world.set_error("Failed to parse address");
    }
#endif
}

WHEN(when_parse_address, "I parse the address")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.hex_string) {
        world.set_error("No hex string provided");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.address = AccountAddress::FromHex(*world.hex_string);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto result = AccountAddress::from_hex(*world.hex_string);
    if (result) {
        world.address = *result;
    } else {
        world.set_error("Failed to parse address");
    }
#endif
}

WHEN(when_convert_to_full_hex, "I convert it to a full hex string")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
#ifdef APTOS_SDK_AVAILABLE
    world.formatted_string = world.address->ToString();
#else
    world.formatted_string = world.address->to_string_long();
#endif
}

WHEN(when_format_as_full_hex, "I format it as full hex")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
#ifdef APTOS_SDK_AVAILABLE
    // SDK uses AIP-40 format (short for special addresses)
    // For full hex, we need to pad manually
    auto bytes = world.address->addressBytes();
    std::stringstream ss;
    ss << "0x";
    for (size_t i = 0; i < bytes.size(); ++i) {
        ss << std::hex << std::setfill('0') << std::setw(2) << static_cast<int>(bytes[i]);
    }
    world.formatted_string = ss.str();
#else
    world.formatted_string = world.address->to_string_long();
#endif
}

WHEN(when_format_as_short_string, "I format it as short string")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
#ifdef APTOS_SDK_AVAILABLE
    // SDK's ToString() already uses AIP-40 short format
    world.formatted_string = world.address->ToString();
#else
    world.formatted_string = world.address->to_string_short();
#endif
}

WHEN(when_serialize_address_bcs, "I serialize the address with BCS")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
#ifdef APTOS_SDK_AVAILABLE
    auto bytes = world.address->addressBytes();
    world.bcs_bytes = std::vector<uint8_t>(bytes.begin(), bytes.end());
#else
    world.bcs_bytes = std::vector<uint8_t>(
        world.address->bytes.begin(), 
        world.address->bytes.end()
    );
#endif
}

WHEN(when_bcs_serialize_address, "I BCS serialize the address")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.address) {
        world.set_error("No address available");
        return;
    }
#ifdef APTOS_SDK_AVAILABLE
    auto bytes = world.address->addressBytes();
    world.bcs_bytes = std::vector<uint8_t>(bytes.begin(), bytes.end());
#else
    world.bcs_bytes = std::vector<uint8_t>(
        world.address->bytes.begin(), 
        world.address->bytes.end()
    );
#endif
}

WHEN(when_bcs_deserialize_address, "I BCS deserialize as AccountAddress")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.bcs_bytes || world.bcs_bytes->size() != 32) {
        world.set_error("Invalid BCS bytes for address");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock bytes(world.bcs_bytes->data(), world.bcs_bytes->size());
        world.address = AccountAddress(bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    std::array<uint8_t, 32> arr;
    std::copy(world.bcs_bytes->begin(), world.bcs_bytes->end(), arr.begin());
    world.address = AccountAddress{arr};
#endif
}

WHEN(when_bcs_deserialize_result_address, "I BCS deserialize the result as AccountAddress")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.bcs_bytes || world.bcs_bytes->size() != 32) {
        world.set_error("Invalid BCS bytes for address");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock bytes(world.bcs_bytes->data(), world.bcs_bytes->size());
        world.address2 = AccountAddress(bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    std::array<uint8_t, 32> arr;
    std::copy(world.bcs_bytes->begin(), world.bcs_bytes->end(), arr.begin());
    world.address2 = AccountAddress{arr};
#endif
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

THEN(then_parsing_should_fail_invalid_address, "the parsing should fail with an invalid address error")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.has_error() || !world.address.has_value());
}

THEN(then_parsing_should_fail_invalid_hex, "the parsing should fail with an invalid hex error")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.has_error() || !world.address.has_value());
}

THEN(then_parsing_should_fail_invalid_length, "the parsing should fail with an invalid length error")
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
#ifdef APTOS_SDK_AVAILABLE
    std::string actual = world.address->ToString();
#else
    std::string actual = world.address->to_string_long();
#endif
    cuke::equal(actual, expected);
}

THEN(then_full_hex_should_be_value, "the full hex should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
    std::string expected = CUKE_ARG(1);
#ifdef APTOS_SDK_AVAILABLE
    // Build full hex from bytes
    auto bytes = world.address->addressBytes();
    std::stringstream ss;
    ss << "0x";
    for (size_t i = 0; i < bytes.size(); ++i) {
        ss << std::hex << std::setfill('0') << std::setw(2) << static_cast<int>(bytes[i]);
    }
    std::string actual = ss.str();
#else
    std::string actual = world.address->to_string_long();
#endif
    cuke::equal(actual, expected);
}

THEN(then_short_string_should_be, "the short string should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
    std::string expected = CUKE_ARG(1);
#ifdef APTOS_SDK_AVAILABLE
    // SDK's ToString() uses AIP-40 short format for special addresses
    std::string actual = world.address->ToString();
#else
    std::string actual = world.address->to_string_short();
#endif
    cuke::equal(actual, expected);
}

THEN(then_formatted_string_should_be, "the formatted string should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.formatted_string.has_value());
    
    std::string expected = CUKE_ARG(1);
    cuke::equal(*world.formatted_string, expected);
}

THEN(then_result_should_be, "the result should be {string}")
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

THEN(then_address_bytes_length_32, "the address bytes should have length 32")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    auto bytes = world.address->addressBytes();
    cuke::equal(static_cast<int>(bytes.size()), 32);
#else
    cuke::equal(static_cast<int>(world.address->bytes.size()), 32);
#endif
}

THEN(then_byte_should_equal, "byte {int} should equal {int}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
    int index = CUKE_ARG(1);
    int expected_value = CUKE_ARG(2);
    
#ifdef APTOS_SDK_AVAILABLE
    auto bytes = world.address->addressBytes();
    cuke::equal(static_cast<int>(bytes[index]), expected_value);
#else
    cuke::equal(static_cast<int>(world.address->bytes[index]), expected_value);
#endif
}

THEN(then_bytes_should_all_be_zero, "bytes {int}-{int} should all be 0")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
    int start = CUKE_ARG(1);
    int end = CUKE_ARG(2);
    
#ifdef APTOS_SDK_AVAILABLE
    auto bytes = world.address->addressBytes();
    for (int i = start; i <= end; ++i) {
        cuke::equal(static_cast<int>(bytes[i]), 0);
    }
#else
    for (int i = start; i <= end; ++i) {
        cuke::equal(static_cast<int>(world.address->bytes[i]), 0);
    }
#endif
}

THEN(then_all_32_bytes_zero, "all 32 bytes should be 0")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    auto bytes = world.address->addressBytes();
    for (int i = 0; i < 32; ++i) {
        cuke::equal(static_cast<int>(bytes[i]), 0);
    }
#else
    for (int i = 0; i < 32; ++i) {
        cuke::equal(static_cast<int>(world.address->bytes[i]), 0);
    }
#endif
}

THEN(then_result_should_be_32_bytes, "the result should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bcs_bytes.has_value());
    cuke::equal(static_cast<int>(world.bcs_bytes->size()), 32);
}

THEN(then_two_addresses_equal, "the two addresses should be equal")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    cuke::is_true(world.address2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_true(*world.address == *world.address2);
#else
    cuke::equal(world.address->bytes, world.address2->bytes);
#endif
}

THEN(then_two_addresses_not_equal, "the two addresses should not be equal")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    cuke::is_true(world.address2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_false(*world.address == *world.address2);
#else
    cuke::is_false(world.address->bytes == world.address2->bytes);
#endif
}

THEN(then_result_equals_original, "the result should equal the original address")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.address.has_value());
    cuke::is_true(world.address2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_true(*world.address == *world.address2);
#else
    cuke::equal(world.address->bytes, world.address2->bytes);
#endif
}
