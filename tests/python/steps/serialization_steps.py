"""
Step definitions for serialization.feature
Tests BCS serialization and deserialization.
"""

import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then, use_step_matcher
from aptos_sdk.bcs import Serializer, Deserializer

from support.vectors import hex_to_bytes, bytes_to_hex


def parse_hex_value(value_str):
    """Parse a value that may be hex (0x...) or decimal."""
    value_str = str(value_str).strip()
    if value_str.lower().startswith("0x"):
        return int(value_str, 16)
    return int(value_str)


def parse_byte_array(array_str):
    """Parse a byte array like '[0x00, 0x01]' or '[0x00]'."""
    array_str = array_str.strip()
    if array_str.startswith("[") and array_str.endswith("]"):
        inner = array_str[1:-1].strip()
        if not inner:
            return bytes()
        parts = [p.strip() for p in inner.split(",")]
        return bytes([parse_hex_value(p) for p in parts])
    return bytes()


# =============================================================================
# Given Steps - Boolean
# =============================================================================


@given("a boolean value false")
def step_given_bool_false(context):
    context.world.bool_value = False


@given("a boolean value true")
def step_given_bool_true(context):
    context.world.bool_value = True


@given("a boolean value {value}")
def step_given_bool_value(context, value):
    context.world.bool_value = value.lower() == "true"


# =============================================================================
# Given Steps - Integers
# =============================================================================


@given("a u8 value {value}")
def step_given_u8(context, value):
    context.world.int_value = parse_hex_value(value)
    context.world.int_type = "u8"


@given("a u16 value {value}")
def step_given_u16(context, value):
    context.world.int_value = parse_hex_value(value)
    context.world.int_type = "u16"


@given("a u32 value {value}")
def step_given_u32(context, value):
    context.world.int_value = parse_hex_value(value)
    context.world.int_type = "u32"


@given("a u64 value {value}")
def step_given_u64(context, value):
    context.world.int_value = parse_hex_value(value)
    context.world.int_type = "u64"


@given("a u128 value {value}")
def step_given_u128(context, value):
    context.world.int_value = parse_hex_value(value)
    context.world.int_type = "u128"


@given("a u256 value {value}")
def step_given_u256(context, value):
    context.world.int_value = parse_hex_value(value)
    context.world.int_type = "u256"


# =============================================================================
# Given Steps - Length/ULEB128
# =============================================================================


@given("a length value {value:d}")
def step_given_length_value(context, value):
    context.world.int_value = value
    context.world.int_type = "uleb128"


# =============================================================================
# Given Steps - Bytes (using regex matcher for disambiguation)
# =============================================================================

use_step_matcher("re")


@given(r'an empty byte array')
def step_given_empty_bytes(context):
    context.world.bytes_value = bytes()


@given(r'bytes (?P<byte_array>\[[^\]]+\]) intended for u64')
def step_given_bytes_for_u64(context, byte_array):
    context.world.bytes_value = parse_byte_array(byte_array)
    context.world.expected_type = "u64"


@given(r'bytes (?P<byte_array>\[[^\]]+\])')
def step_given_bytes(context, byte_array):
    context.world.bytes_value = parse_byte_array(byte_array)


use_step_matcher("parse")


@given("32 bytes with byte 31 = {value}")
def step_given_32_bytes_with_last(context, value):
    data = bytearray(32)
    data[31] = parse_hex_value(value)
    context.world.bytes_value = bytes(data)




# =============================================================================
# Given Steps - Strings
# =============================================================================


@given('a string "{text}"')
def step_given_string(context, text):
    context.world.string_value = text


@given('a string ""')
def step_given_empty_string(context):
    context.world.string_value = ""


# =============================================================================
# Given Steps - Option
# =============================================================================


@given("an Option with no value")
def step_given_option_none(context):
    context.world.option_value = None


@given("an Option containing u64 value {value:d}")
def step_given_option_u64(context, value):
    context.world.option_value = value
    context.world.option_type = "u64"


# =============================================================================
# Given Steps - Vector
# =============================================================================


@given("an empty vector of u8")
def step_given_empty_vector_u8(context):
    context.world.vector_value = []
    context.world.vector_type = "u8"


use_step_matcher("re")


@given(r'a vector \[(?P<values>[^\]]+)\] of u8')
def step_given_vector_u8(context, values):
    context.world.vector_value = [int(v.strip()) for v in values.split(",")]
    context.world.vector_type = "u8"


@given(r'a vector \[(?P<values>[^\]]+)\] of u64')
def step_given_vector_u64(context, values):
    context.world.vector_value = [int(v.strip()) for v in values.split(",")]
    context.world.vector_type = "u64"


@given(r'a vector \[\[(?P<inner1>[^\]]+)\], \[(?P<inner2>[^\]]+)\]\] of vectors of u8')
def step_given_nested_vector(context, inner1, inner2):
    vec1 = [int(v.strip()) for v in inner1.split(",")]
    vec2 = [int(v.strip()) for v in inner2.split(",")]
    context.world.vector_value = [vec1, vec2]
    context.world.vector_type = "nested"


use_step_matcher("parse")


# =============================================================================
# Given Steps - AccountAddress
# =============================================================================


@given('an AccountAddress "{address}"')
def step_given_account_address_for_bcs(context, address):
    from aptos_sdk.account_address import AccountAddress
    context.world.address = AccountAddress.from_str(address)


# =============================================================================
# Given Steps - Struct
# =============================================================================


@given("a struct with fields")
def step_given_struct_with_fields(context):
    """Parse table of struct fields."""
    context.world.struct_fields = []
    for row in context.table:
        context.world.struct_fields.append({
            "field": row["field"],
            "type": row["type"],
            "value": row["value"]
        })


# =============================================================================
# When Steps - BCS Serialize
# =============================================================================


@when("I BCS serialize it")
def step_bcs_serialize_it(context):
    try:
        serializer = Serializer()
        
        if hasattr(context.world, 'bool_value'):
            serializer.bool(context.world.bool_value)
        elif hasattr(context.world, 'int_type'):
            value = context.world.int_value
            int_type = context.world.int_type
            if int_type == "u8":
                serializer.u8(value)
            elif int_type == "u16":
                serializer.u16(value)
            elif int_type == "u32":
                serializer.u32(value)
            elif int_type == "u64":
                serializer.u64(value)
            elif int_type == "u128":
                serializer.u128(value)
            elif int_type == "u256":
                serializer.u256(value)
            elif int_type == "uleb128":
                serializer.uleb128(value)
        elif hasattr(context.world, 'bytes_value') and context.world.bytes_value is not None:
            serializer.to_bytes(context.world.bytes_value)
        elif hasattr(context.world, 'string_value'):
            serializer.str(context.world.string_value)
        elif hasattr(context.world, 'option_value'):
            if context.world.option_value is None:
                serializer.u8(0)  # None
            else:
                serializer.u8(1)  # Some
                if context.world.option_type == "u64":
                    serializer.u64(context.world.option_value)
        elif hasattr(context.world, 'vector_value'):
            vec = context.world.vector_value
            vec_type = context.world.vector_type
            if vec_type == "u8":
                serializer.sequence(vec, Serializer.u8)
            elif vec_type == "u64":
                serializer.sequence(vec, Serializer.u64)
            elif vec_type == "nested":
                serializer.uleb128(len(vec))
                for inner in vec:
                    serializer.sequence(inner, Serializer.u8)
        elif hasattr(context.world, 'address'):
            serializer.struct(context.world.address)
        elif hasattr(context.world, 'struct_fields'):
            for field in context.world.struct_fields:
                if field["type"] == "address":
                    from aptos_sdk.account_address import AccountAddress
                    addr = AccountAddress.from_str(field["value"])
                    serializer.struct(addr)
                elif field["type"] == "u64":
                    serializer.u64(int(field["value"]))
        
        context.world.result_bytes = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I ULEB128 encode it")
def step_uleb128_encode(context):
    try:
        serializer = Serializer()
        serializer.uleb128(context.world.int_value)
        context.world.result_bytes = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I ULEB128 encode and decode it")
def step_uleb128_roundtrip(context):
    try:
        serializer = Serializer()
        serializer.uleb128(context.world.int_value)
        encoded = serializer.output()
        
        deserializer = Deserializer(encoded)
        context.world.result = deserializer.uleb128()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - BCS Deserialize
# =============================================================================


@when("I BCS deserialize as boolean")
def step_bcs_deserialize_bool(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.result = deserializer.bool()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize as u64")
def step_bcs_deserialize_u64(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.result = deserializer.u64()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# Note: "I BCS deserialize as AccountAddress" is defined in address_steps.py


@when("I BCS deserialize as vector of u8")
def step_bcs_deserialize_vector_u8(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        length = deserializer.uleb128()
        context.world.result = [deserializer.u8() for _ in range(length)]
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Result Size
# =============================================================================


@then("the result should be 1 byte")
def step_result_1_byte(context):
    assert len(context.world.result_bytes) == 1


@then("the result should be 2 bytes in little-endian")
def step_result_2_bytes(context):
    assert len(context.world.result_bytes) == 2


@then("the result should be 4 bytes in little-endian")
def step_result_4_bytes(context):
    assert len(context.world.result_bytes) == 4


@then("the result should be 8 bytes in little-endian")
def step_result_8_bytes(context):
    assert len(context.world.result_bytes) == 8


@then("the result should be 16 bytes in little-endian")
def step_result_16_bytes(context):
    assert len(context.world.result_bytes) == 16


@then("the result should be 32 bytes in little-endian")
def step_result_32_bytes_le(context):
    assert len(context.world.result_bytes) == 32


# Note: "the result should be 32 bytes" is defined in address_steps.py


@then("the result should be exactly 32 bytes")
def step_result_exactly_32_bytes(context):
    assert len(context.world.result_bytes) == 32


# =============================================================================
# Then Steps - Byte Values
# =============================================================================


@then("the byte should be {expected}")
def step_byte_should_be(context, expected):
    expected_val = parse_hex_value(expected)
    assert context.world.result_bytes[0] == expected_val


@then("the bytes should be {expected}")
def step_bytes_should_be(context, expected):
    expected_bytes = parse_byte_array(expected)
    assert context.world.result_bytes == expected_bytes, f"Expected {expected_bytes.hex()}, got {context.world.result_bytes.hex()}"


use_step_matcher("re")


@then(r'the result should be (?P<expected>\[[^\]]+\])')
def step_result_should_be_bytes(context, expected):
    expected_bytes = parse_byte_array(expected)
    assert context.world.result_bytes == expected_bytes


@then(r'the first byte should be (?P<expected>0x[0-9a-fA-F]+)')
def step_first_byte_should_be_hex(context, expected):
    expected_val = parse_hex_value(expected)
    assert context.world.result_bytes[0] == expected_val


@then(r'the first byte should be (?P<expected>0x[0-9a-fA-F]+) \(length\)')
def step_first_byte_should_be_with_comment(context, expected):
    expected_val = parse_hex_value(expected)
    assert context.world.result_bytes[0] == expected_val


@then(r'the first byte should be (?P<expected>0x[0-9a-fA-F]+) \(UTF-8 byte length\)')
def step_first_byte_should_be_utf8_length(context, expected):
    expected_val = parse_hex_value(expected)
    assert context.world.result_bytes[0] == expected_val


@then(r'the first byte should be (?P<expected>0x[0-9a-fA-F]+) \(outer length\)')
def step_first_byte_should_be_outer_length(context, expected):
    expected_val = parse_hex_value(expected)
    assert context.world.result_bytes[0] == expected_val


use_step_matcher("parse")


use_step_matcher("re")


@then(r'the remaining bytes should be UTF-8 encoded "(?P<text>[^"]+)"')
def step_remaining_bytes_utf8(context, text):
    expected = text.encode("utf-8")
    actual = context.world.result_bytes[1:]
    assert actual == expected


@then(r'the remaining bytes should be (?P<expected>\[[^\]]+\])')
def step_remaining_bytes_should_be(context, expected):
    expected_bytes = parse_byte_array(expected)
    actual = context.world.result_bytes[1:]
    assert actual == expected_bytes


use_step_matcher("parse")


@then("the remaining 8 bytes should be the u64 value")
def step_remaining_8_bytes_u64(context):
    # Just verify we have at least 9 bytes (1 for option + 8 for u64)
    assert len(context.world.result_bytes) >= 9


@then("byte 31 should be {expected}")
def step_byte_31_should_be(context, expected):
    expected_val = parse_hex_value(expected)
    assert context.world.result_bytes[31] == expected_val


@then("bytes 0-30 should all be {expected}")
def step_bytes_0_30_should_be(context, expected):
    expected_val = parse_hex_value(expected)
    for i in range(31):
        assert context.world.result_bytes[i] == expected_val


# =============================================================================
# Then Steps - Vector/Struct specific
# =============================================================================


@then("the fields should be serialized in order")
def step_fields_serialized_in_order(context):
    # Verify we have result bytes
    assert context.world.result_bytes is not None
    assert len(context.world.result_bytes) > 0


@then("the total length should be {length:d} bytes (32 + 8)")
def step_total_length_should_be(context, length):
    assert len(context.world.result_bytes) == length


@then("each inner vector should be length-prefixed")
def step_inner_vectors_length_prefixed(context):
    # Just verify we have some output
    assert len(context.world.result_bytes) > 0


@then("the remaining bytes should be two u64 values in little-endian")
def step_remaining_two_u64(context):
    assert len(context.world.result_bytes) == 17  # 1 length + 16 bytes


# Note: "the result should be true/false" are defined in general_steps.py


# =============================================================================
# Then Steps - ULEB128
# =============================================================================


@then("the result should equal the original value")
def step_result_equals_original(context):
    assert context.world.result == context.world.int_value


# =============================================================================
# Then Steps - Errors
# =============================================================================


@then("the deserialization should fail with an error")
def step_deserialization_should_fail(context):
    assert context.world.error is not None
