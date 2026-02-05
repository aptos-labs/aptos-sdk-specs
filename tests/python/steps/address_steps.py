"""
Step definitions for address.feature
Tests AccountAddress parsing, formatting, and BCS serialization.
"""

from support.vectors import (
    get_address_parsing_vectors,
    bytes_to_hex,
)
from aptos_sdk.bcs import Serializer, Deserializer
from aptos_sdk.account_address import AccountAddress
from behave import given, when, then
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# =============================================================================
# Helper Functions
# =============================================================================


def to_full_hex(address: AccountAddress) -> str:
    """Format address as full 64-character hex string."""
    return "0x" + address.address.hex()


def to_short_string(address: AccountAddress) -> str:
    """Format address as short string (strip leading zeros)."""
    full_hex = address.address.hex()
    trimmed = full_hex.lstrip("0") or "0"
    return "0x" + trimmed


def parse_address(hex_string: str) -> AccountAddress:
    """Parse an address using relaxed parsing."""
    return AccountAddress.from_str_relaxed(hex_string)


# =============================================================================
# Given Steps - Address Input
# =============================================================================


@given('a hex string "{hex_string}"')
def step_given_hex_string(context, hex_string):
    context.world.hex_string = hex_string


@given('a hex string ""')
def step_given_empty_hex_string(context):
    context.world.hex_string = ""


@given('a valid hex address string "{hex_string}"')
def step_given_valid_hex_address(context, hex_string):
    context.world.hex_string = hex_string


@given('the address string "{address}"')
def step_given_address_string(context, address):
    context.world.hex_string = address


@given('a short address "{address}"')
def step_given_short_address(context, address):
    context.world.hex_string = address


@given("a full 64-character hex address")
def step_given_full_hex_address(context):
    context.world.hex_string = (
        "0x0000000000000000000000000000000000000000000000000000000000000001"
    )


# Note: "an invalid hex string" is defined in account_steps.py


@given("test vectors from addresses.json")
def step_given_address_test_vectors(context):
    vectors = get_address_parsing_vectors()
    context.world.test_vectors["address_parsing"] = vectors


# =============================================================================
# Given Steps - Address Creation
# =============================================================================


@given("an AccountAddress with value {value:d}")
def step_given_address_with_value(context, value):
    # Create address with specific byte value in last position
    address_bytes = bytearray(32)
    address_bytes[31] = value
    full_hex = "0x" + bytes(address_bytes).hex()
    context.world.address = AccountAddress.from_str_relaxed(full_hex)


@given('an AccountAddress from hex "{hex_string}"')
def step_given_address_from_hex(context, hex_string):
    context.world.address = parse_address(hex_string)
    context.world.addresses = [context.world.address]
    context.world.test_vectors["original_address"] = context.world.address


@given('another AccountAddress from hex "{hex_string}"')
def step_given_another_address_from_hex(context, hex_string):
    address2 = parse_address(hex_string)
    if not context.world.addresses:
        context.world.addresses = [context.world.address]
    context.world.addresses.append(address2)


# =============================================================================
# Given Steps - Bytes
# =============================================================================


@given("32 random bytes")
def step_given_random_bytes(context):
    import os

    context.world.bytes_value = os.urandom(32)


@given("32 bytes with value {value:d} in the last byte")
def step_given_bytes_with_value(context, value):
    data = bytearray(32)
    data[31] = value
    context.world.bytes_value = bytes(data)


# =============================================================================
# Given Steps - Address Constants
# =============================================================================


@given("the ZERO address constant")
def step_given_zero_address(context):
    context.world.address = AccountAddress.from_str(
        "0x0000000000000000000000000000000000000000000000000000000000000000"
    )


@given("the zero address constant")
def step_given_zero_address_alt(context):
    context.world.address = AccountAddress.from_str(
        "0x0000000000000000000000000000000000000000000000000000000000000000"
    )


@given("the ONE address constant")
def step_given_one_address(context):
    context.world.address = AccountAddress.from_str(
        "0x0000000000000000000000000000000000000000000000000000000000000001"
    )


@given("the framework address constant")
def step_given_framework_address(context):
    context.world.address = AccountAddress.from_str(
        "0x0000000000000000000000000000000000000000000000000000000000000001"
    )


@given("the THREE address constant")
def step_given_three_address(context):
    context.world.address = AccountAddress.from_str(
        "0x0000000000000000000000000000000000000000000000000000000000000003"
    )


@given("the FOUR address constant")
def step_given_four_address(context):
    context.world.address = AccountAddress.from_str(
        "0x0000000000000000000000000000000000000000000000000000000000000004"
    )


# =============================================================================
# Given Steps - Address Pairs
# =============================================================================


@given('two addresses "{addr1}" and "{addr2}"')
def step_given_two_addresses(context, addr1, addr2):
    context.world.addresses = [
        parse_address(addr1),
        parse_address(addr2),
    ]


# =============================================================================
# When Steps - Parsing
# =============================================================================


@when("I parse the address")
def step_parse_address(context):
    try:
        context.world.address = AccountAddress.from_str_relaxed(
            context.world.hex_string
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I parse the address string")
def step_parse_address_string(context):
    step_parse_address(context)


@when("I parse it as an AccountAddress")
def step_parse_as_account_address(context):
    step_parse_address(context)


@when("I create an AccountAddress from the bytes")
def step_create_address_from_bytes(context):
    try:
        hex_str = bytes_to_hex(context.world.bytes_value)
        context.world.address = AccountAddress.from_str(hex_str)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to parse it as an address")
def step_try_parse_address(context):
    try:
        context.world.address = AccountAddress.from_str_relaxed(
            context.world.hex_string
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Formatting
# =============================================================================


@when("I format the address as a string")
def step_format_address_as_string(context):
    context.world.hex_string = str(context.world.address)


@when("I format it as full hex")
def step_format_as_full_hex(context):
    context.world.result = to_full_hex(context.world.address)


@when("I format it as a full hex string")
def step_format_as_full_hex_string(context):
    context.world.hex_string = str(context.world.address)


@when("I format it as short string")
def step_format_as_short_string(context):
    context.world.result = to_short_string(context.world.address)


@when("I format it as a short string")
def step_format_as_short_string_alt(context):
    context.world.hex_string = to_short_string(context.world.address)


# =============================================================================
# When Steps - Bytes/Serialization
# =============================================================================


@when("I get the raw bytes")
def step_get_raw_bytes(context):
    # AccountAddress stores bytes internally
    context.world.bytes_value = bytes(context.world.address.address)


@when("I BCS serialize the address")
def step_bcs_serialize_address(context):
    serializer = Serializer()
    serializer.struct(context.world.address)
    context.world.bytes_value = serializer.output()


@when("I BCS deserialize as AccountAddress")
def step_bcs_deserialize_address(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.address = AccountAddress.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize the result as AccountAddress")
def step_bcs_deserialize_result_as_address(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.result = AccountAddress.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Comparison
# =============================================================================


@when("I compare them for equality")
def step_compare_addresses(context):
    addr1 = context.world.addresses[0]
    addr2 = context.world.addresses[1]
    context.world.result = str(addr1) == str(addr2)


# =============================================================================
# When Steps - Test Vectors
# =============================================================================


@when("I run all parsing test vectors")
def step_run_parsing_test_vectors(context):
    vectors = context.world.test_vectors.get("address_parsing", [])
    results = []

    for vector in vectors:
        try:
            address = AccountAddress.from_str(vector["input"])
            full_hex = str(address)
            short_str = to_short_string(address)

            passed = (
                full_hex.lower() == vector["expected"]["full_hex"].lower()
                and short_str.lower() == vector["expected"]["short_string"].lower()
            )
            results.append({"name": vector["name"], "passed": passed})
        except Exception as e:
            results.append({"name": vector["name"], "passed": False, "error": str(e)})

    context.world.result = results


# =============================================================================
# Then Steps - Parsing Success/Failure
# =============================================================================


@then("the parsing should succeed")
def step_parsing_should_succeed(context):
    assert context.world.error is None, f"Expected no error, got: {context.world.error}"
    # Check various things that might be set after parsing
    has_something = (
        context.world.address is not None
        or context.world.result is not None
        or getattr(context.world, "type_tag", None) is not None
        or getattr(context.world, "module_address", None) is not None
        or getattr(context.world, "hash_value", None) is not None
    )
    assert (
        has_something
    ), "Expected address, result, type_tag, module_address, or hash_value to be set"


@then("I should get a valid AccountAddress")
def step_should_get_valid_address(context):
    assert context.world.error is None
    assert context.world.address is not None


@then("the address should be valid")
def step_address_should_be_valid(context):
    assert context.world.error is None
    assert context.world.address is not None


@then("parsing should fail")
def step_parsing_should_fail(context):
    assert context.world.error is not None, "Expected an error but got none"


@then("parsing should fail with an error")
def step_parsing_should_fail_with_error(context):
    assert context.world.error is not None


@then("the parsing should fail with an invalid address error")
def step_parsing_should_fail_invalid_address(context):
    assert context.world.error is not None


@then("the parsing should fail with an invalid hex error")
def step_parsing_should_fail_invalid_hex(context):
    assert context.world.error is not None


@then("the parsing should fail with an invalid length error")
def step_parsing_should_fail_invalid_length(context):
    assert context.world.error is not None


@then("it should fail with an InvalidAddress error")
def step_should_fail_invalid_address(context):
    assert context.world.error is not None


# =============================================================================
# Then Steps - Address Byte Assertions
# =============================================================================


@then("the address bytes should have length {length:d}")
def step_address_bytes_length(context, length):
    addr_bytes = bytes(context.world.address.address)
    assert len(addr_bytes) == length


@then("byte {index:d} should equal {value:d}")
def step_byte_should_equal(context, index, value):
    if context.world.address:
        data = bytes(context.world.address.address)
    else:
        data = context.world.bytes_value
    assert data[index] == value


@then("bytes {start:d}-{end:d} should all be {value:d}")
def step_bytes_range_should_equal(context, start, end, value):
    if context.world.address:
        data = bytes(context.world.address.address)
    else:
        data = context.world.bytes_value
    for i in range(start, end + 1):
        assert data[i] == value, f"Byte {i} is {data[i]}, expected {value}"


@then("all 32 bytes should be {value:d}")
def step_all_bytes_should_equal(context, value):
    data = bytes(context.world.address.address)
    for i in range(32):
        assert data[i] == value


@then("the byte length should be 32")
def step_byte_length_should_be_32(context):
    assert len(context.world.bytes_value) == 32


@then("the bytes should be 32 bytes")
def step_bytes_should_be_32(context):
    assert len(context.world.bytes_value) == 32


@then("the result should be 32 bytes")
def step_result_should_be_32_bytes(context):
    assert len(context.world.bytes_value) == 32


@then("the first byte should be zero")
def step_first_byte_zero(context):
    assert context.world.bytes_value[0] == 0


@then("the last byte should be {expected:d}")
def step_last_byte_should_be(context, expected):
    if context.world.address:
        data = bytes(context.world.address.address)
    else:
        data = context.world.bytes_value
    assert data[31] == expected


# =============================================================================
# Then Steps - String Format Assertions
# =============================================================================


@then('the full hex should be "{expected}"')
def step_full_hex_should_be(context, expected):
    actual = to_full_hex(context.world.address)
    assert actual.lower() == expected.lower()


@then('the full hex representation should be "{expected}"')
def step_full_hex_representation_should_be(context, expected):
    actual = to_full_hex(context.world.address)
    assert actual.lower() == expected.lower()


@then('the short string should be "{expected}"')
def step_short_string_should_be(context, expected):
    actual = to_short_string(context.world.address)
    assert actual.lower() == expected.lower()


@then('the address should equal "{expected}"')
def step_address_should_equal(context, expected):
    actual = str(context.world.address)
    assert actual.lower() == expected.lower()


@then('the result should be "{expected}"')
def step_result_should_be(context, expected):
    actual = (
        context.world.test_vectors.get("formattedString")
        or context.world.result
        or context.world.hex_string
    )
    assert str(actual).lower() == expected.lower()


# =============================================================================
# Then Steps - Address Equality
# =============================================================================


@then('it should equal address "{expected}"')
def step_should_equal_address(context, expected):
    expected_addr = parse_address(expected)
    assert to_full_hex(context.world.address) == to_full_hex(expected_addr)


@then("the two addresses should be equal")
def step_two_addresses_equal(context):
    assert to_full_hex(context.world.addresses[0]) == to_full_hex(
        context.world.addresses[1]
    )


@then("the two addresses should not be equal")
def step_two_addresses_not_equal(context):
    assert to_full_hex(context.world.addresses[0]) != to_full_hex(
        context.world.addresses[1]
    )


@then("they should be equal")
def step_they_should_be_equal(context):
    if "hash1" in context.world.test_vectors and "hash2" in context.world.test_vectors:
        hash1 = context.world.test_vectors["hash1"]
        hash2 = context.world.test_vectors["hash2"]
        assert hash1.hex() == hash2.hex()
    else:
        assert context.world.result is True


@then("they should not be equal")
def step_they_should_not_be_equal(context):
    assert context.world.result is False


@then("the result should equal the original address")
def step_result_equals_original(context):
    original = context.world.test_vectors.get("original_address")
    result = context.world.result
    assert str(result) == str(original)


# =============================================================================
# Then Steps - Test Vectors
# =============================================================================


@then("all test vectors should pass")
def step_all_vectors_pass(context):
    results = context.world.result
    failures = [r for r in results if not r["passed"]]

    if failures:
        failure_msgs = [
            f"  - {f['name']}: {f.get('error', 'mismatch')}" for f in failures
        ]
        raise AssertionError(
            f"{len(failures)} test vectors failed:\n" + "\n".join(failure_msgs)
        )
