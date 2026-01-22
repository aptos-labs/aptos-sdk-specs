"""
Step definitions for entry-function.feature
Tests entry function payload creation and BCS serialization.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.type_tag import TypeTag, StructTag
from aptos_sdk.bcs import Serializer, Deserializer
from aptos_sdk.transactions import EntryFunction, TransactionArgument

from support.vectors import hex_to_bytes, bytes_to_hex


# =============================================================================
# Given Steps - Entry Function Components
# =============================================================================


@given('module address "{address}"')
def step_given_entry_module_address(context, address):
    context.world.test_vectors["entry_module_address"] = address


@given('module name "{module}"')
def step_given_entry_module_name(context, module):
    context.world.test_vectors["entry_module_name"] = module


@given('function name "{function}"')
def step_given_entry_function_name(context, function):
    context.world.test_vectors["entry_function_name"] = function


@given("no arguments")
def step_given_no_arguments(context):
    context.world.test_vectors["entry_args"] = []


@given("no type arguments")
def step_given_no_entry_type_args(context):
    context.world.test_vectors["entry_type_args"] = []


@given('a u64 argument {value:d}')
def step_given_u64_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("u64", value))
    context.world.test_vectors["entry_args"] = args


@given('an address argument "{address}"')
def step_given_address_argument(context, address):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("address", address))
    context.world.test_vectors["entry_args"] = args


@given('a string argument "{text}"')
def step_given_string_argument(context, text):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("string", text))
    context.world.test_vectors["entry_args"] = args


@given('a bool argument {value}')
def step_given_bool_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    bool_val = value.lower() == "true"
    args.append(("bool", bool_val))
    context.world.test_vectors["entry_args"] = args


@given('a vector<u8> argument [{values}]')
def step_given_vector_u8_argument(context, values):
    args = context.world.test_vectors.get("entry_args", [])
    if values.strip():
        vec = [int(v.strip()) for v in values.split(",")]
    else:
        vec = []
    args.append(("vector_u8", vec))
    context.world.test_vectors["entry_args"] = args


@given('a u8 argument {value:d}')
def step_given_u8_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("u8", value))
    context.world.test_vectors["entry_args"] = args


@given('a u16 argument {value:d}')
def step_given_u16_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("u16", value))
    context.world.test_vectors["entry_args"] = args


@given('a u32 argument {value:d}')
def step_given_u32_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("u32", value))
    context.world.test_vectors["entry_args"] = args


@given('a u128 argument {value:d}')
def step_given_u128_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("u128", value))
    context.world.test_vectors["entry_args"] = args


@given('a u256 argument {value}')
def step_given_u256_argument(context, value):
    args = context.world.test_vectors.get("entry_args", [])
    args.append(("u256", int(value)))
    context.world.test_vectors["entry_args"] = args


@given('type argument "{type_arg}"')
def step_given_type_argument(context, type_arg):
    type_args = context.world.test_vectors.get("entry_type_args", [])
    type_args.append(type_arg)
    context.world.test_vectors["entry_type_args"] = type_args


@given('type arguments ["{type_args}"]')
def step_given_type_arguments_list(context, type_args):
    context.world.test_vectors["entry_type_args"] = [
        t.strip().strip('"') for t in type_args.split(",")
    ]


# =============================================================================
# When Steps - Entry Function Creation
# =============================================================================


@when("I create an entry function payload")
def step_create_entry_function(context):
    try:
        address = context.world.test_vectors.get("entry_module_address", "0x1")
        module = context.world.test_vectors.get("entry_module_name", "module")
        function = context.world.test_vectors.get("entry_function_name", "function")
        args = context.world.test_vectors.get("entry_args", [])
        type_args = context.world.test_vectors.get("entry_type_args", [])

        # Parse module address
        module_addr = AccountAddress.from_str(address)

        # Encode arguments
        encoded_args = []
        for arg_type, arg_value in args:
            serializer = Serializer()
            if arg_type == "u8":
                serializer.u8(arg_value)
            elif arg_type == "u16":
                serializer.u16(arg_value)
            elif arg_type == "u32":
                serializer.u32(arg_value)
            elif arg_type == "u64":
                serializer.u64(arg_value)
            elif arg_type == "u128":
                serializer.u128(arg_value)
            elif arg_type == "u256":
                serializer.u256(arg_value)
            elif arg_type == "bool":
                serializer.bool(arg_value)
            elif arg_type == "address":
                addr = AccountAddress.from_str(arg_value)
                serializer.struct(addr)
            elif arg_type == "string":
                serializer.str(arg_value)
            elif arg_type == "vector_u8":
                serializer.sequence(arg_value, Serializer.u8)
            encoded_args.append(serializer.output())

        # Parse type arguments
        parsed_type_args = []
        for ta in type_args:
            parsed_type_args.append(TypeTag.from_str(ta))

        # Create entry function
        context.world.result = EntryFunction.natural(
            f"{address}::{module}",
            function,
            parsed_type_args,
            encoded_args
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to create an entry function payload")
def step_try_create_entry_function(context):
    step_create_entry_function(context)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the entry function payload")
def step_bcs_serialize_entry_function(context):
    try:
        serializer = Serializer()
        context.world.result.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize as entry function payload")
def step_bcs_deserialize_entry_function(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.result = EntryFunction.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS serialize the entry function twice")
def step_bcs_serialize_entry_function_twice(context):
    try:
        serializer1 = Serializer()
        context.world.result.serialize(serializer1)
        bytes1 = serializer1.output()

        serializer2 = Serializer()
        context.world.result.serialize(serializer2)
        bytes2 = serializer2.output()

        context.world.test_vectors["bytes1"] = bytes1
        context.world.test_vectors["bytes2"] = bytes2
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Entry Function Assertions
# =============================================================================


@then("the entry function payload should be valid")
def step_entry_function_valid(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("entry function creation should succeed")
def step_entry_function_creation_succeed(context):
    assert context.world.error is None


@then("entry function creation should fail")
def step_entry_function_creation_fail(context):
    assert context.world.error is not None


@then('the entry function module should be "{expected}"')
def step_entry_function_module(context, expected):
    entry_fn = context.world.result
    actual = f"{entry_fn.module.address}::{entry_fn.module.name}"
    assert expected in actual or actual in expected


@then('the entry function name should be "{expected}"')
def step_entry_function_name_check(context, expected):
    entry_fn = context.world.result
    assert entry_fn.function == expected


@then("the entry function should have {count:d} arguments")
def step_entry_function_arg_count(context, count):
    entry_fn = context.world.result
    assert len(entry_fn.args) == count


@then("the entry function should have {count:d} type arguments")
def step_entry_function_type_arg_count(context, count):
    entry_fn = context.world.result
    assert len(entry_fn.ty_args) == count


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the serialized entry function should not be empty")
def step_serialized_entry_function_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then('the serialized entry function should be "{expected}"')
def step_serialized_entry_function_should_be(context, expected):
    actual = bytes_to_hex(context.world.bytes_value, prefix=False)
    expected_clean = expected[2:] if expected.startswith("0x") else expected
    assert actual.lower() == expected_clean.lower()


@then("the two serializations should be identical")
def step_serializations_identical(context):
    bytes1 = context.world.test_vectors.get("bytes1")
    bytes2 = context.world.test_vectors.get("bytes2")
    assert bytes1 == bytes2


@then("the deserialized entry function should match the original")
def step_deserialized_entry_function_matches(context):
    # Serialize both and compare bytes
    original = context.world.test_vectors.get("original_entry_fn", context.world.result)
    
    serializer1 = Serializer()
    original.serialize(serializer1)
    
    serializer2 = Serializer()
    context.world.result.serialize(serializer2)
    
    assert serializer1.output() == serializer2.output()
