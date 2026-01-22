"""
Step definitions for type-tags.feature
Tests TypeTag parsing, formatting, and BCS serialization.

Note: The Python SDK's TypeTag doesn't have a from_str parser.
We implement basic parsing here for testing purposes.
"""

import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then, use_step_matcher
from aptos_sdk.type_tag import TypeTag, StructTag
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer, Deserializer

from support.vectors import hex_to_bytes, bytes_to_hex


# =============================================================================
# TypeTag Parser (not provided by SDK, implemented for tests)
# =============================================================================


def parse_type_tag(type_string: str) -> TypeTag:
    """Parse a type string into a TypeTag."""
    type_string = type_string.strip()
    
    if not type_string:
        raise ValueError("Empty type string")
    
    # Primitives
    primitives = {
        "bool": TypeTag.BOOL,
        "u8": TypeTag.U8,
        "u16": TypeTag.U16,
        "u32": TypeTag.U32,
        "u64": TypeTag.U64,
        "u128": TypeTag.U128,
        "u256": TypeTag.U256,
        "address": TypeTag.ACCOUNT_ADDRESS,
        "signer": TypeTag.SIGNER,
    }
    
    if type_string in primitives:
        return TypeTag(primitives[type_string])
    
    # Vector<T>
    if type_string.startswith("vector<"):
        if not type_string.endswith(">"):
            raise ValueError("Unclosed vector bracket")
        inner = type_string[7:-1].strip()
        if not inner:
            raise ValueError("Empty vector type")
        inner_tag = parse_type_tag(inner)
        return TypeTag(inner_tag)  # Vector wraps another TypeTag
    
    # Struct: address::module::name<type_args>
    match = re.match(r'^(0x[0-9a-fA-F]+)::([a-zA-Z_][a-zA-Z0-9_]*)::([a-zA-Z_][a-zA-Z0-9_]*)(.*)$', type_string)
    if match:
        addr_str, module, name, rest = match.groups()
        addr = AccountAddress.from_str(addr_str)
        
        type_args = []
        if rest.startswith("<") and rest.endswith(">"):
            # Parse type args
            args_str = rest[1:-1]
            # Simple split by comma (doesn't handle nested generics perfectly)
            if args_str:
                depth = 0
                current = ""
                for c in args_str:
                    if c == "<":
                        depth += 1
                        current += c
                    elif c == ">":
                        depth -= 1
                        current += c
                    elif c == "," and depth == 0:
                        type_args.append(parse_type_tag(current.strip()))
                        current = ""
                    else:
                        current += c
                if current.strip():
                    type_args.append(parse_type_tag(current.strip()))
        
        struct_tag = StructTag(addr, module, name, type_args)
        return TypeTag(struct_tag)
    
    raise ValueError(f"Unknown type format: {type_string}")


def format_type_tag(tag: TypeTag) -> str:
    """Format a TypeTag as a string."""
    val = tag.value
    
    # Check for primitive types
    if val == TypeTag.BOOL:
        return "bool"
    elif val == TypeTag.U8:
        return "u8"
    elif val == TypeTag.U16:
        return "u16"
    elif val == TypeTag.U32:
        return "u32"
    elif val == TypeTag.U64:
        return "u64"
    elif val == TypeTag.U128:
        return "u128"
    elif val == TypeTag.U256:
        return "u256"
    elif val == TypeTag.ACCOUNT_ADDRESS:
        return "address"
    elif val == TypeTag.SIGNER:
        return "signer"
    
    # Check for vector (value is another TypeTag)
    if isinstance(val, TypeTag):
        return f"vector<{format_type_tag(val)}>"
    
    # Check for struct (value is StructTag)
    if isinstance(val, StructTag):
        return str(val)
    
    return str(tag)


def get_type_tag_variant(tag: TypeTag):
    """Get the variant type constant of a TypeTag."""
    val = tag.value
    
    # Primitive constants
    if val in (TypeTag.BOOL, TypeTag.U8, TypeTag.U16, TypeTag.U32, 
               TypeTag.U64, TypeTag.U128, TypeTag.U256, 
               TypeTag.ACCOUNT_ADDRESS, TypeTag.SIGNER):
        return val
    
    # Vector (value is another TypeTag)
    if isinstance(val, TypeTag):
        return TypeTag.VECTOR
    
    # Struct (value is StructTag)
    if isinstance(val, StructTag):
        return TypeTag.STRUCT
    
    return None


# =============================================================================
# Given Steps - Type String
# =============================================================================


@given('a type string "{type_string}"')
def step_given_type_string(context, type_string):
    context.world.type_string = type_string


@given('a type string ""')
def step_given_empty_type_string(context):
    context.world.type_string = ""


# =============================================================================
# Given Steps - TypeTag Variants
# =============================================================================


@given("a TypeTag of variant U64")
def step_given_typetag_u64(context):
    context.world.type_tag = TypeTag(TypeTag.U64)


@given("a TypeTag of variant Bool")
def step_given_typetag_bool(context):
    context.world.type_tag = TypeTag(TypeTag.BOOL)


@given("a TypeTag of Vector containing U8")
def step_given_typetag_vector_u8(context):
    inner = TypeTag(TypeTag.U8)
    context.world.type_tag = TypeTag(inner)


@given('a TypeTag struct with address "{address}", module "{module}", name "{name}"')
def step_given_typetag_struct(context, address, module, name):
    addr = AccountAddress.from_str(address)
    struct_tag = StructTag(addr, module, name, [])
    context.world.type_tag = TypeTag(struct_tag)


@given("a TypeTag for CoinStore of AptosCoin")
def step_given_typetag_coinstore(context):
    addr = AccountAddress.from_str("0x1")
    aptos_coin = StructTag(addr, "aptos_coin", "AptosCoin", [])
    coin_store = StructTag(addr, "coin", "CoinStore", [TypeTag(aptos_coin)])
    context.world.type_tag = TypeTag(coin_store)


# =============================================================================
# Given Steps - Module String
# =============================================================================


@given('a module string "{module_string}"')
def step_given_module_string(context, module_string):
    context.world.module_string = module_string


@given('a MoveModuleId with address "{address}" and name "{name}"')
def step_given_module_id(context, address, name):
    context.world.module_address = address
    context.world.module_name = name


# =============================================================================
# Given Steps - Struct Components
# =============================================================================


@given('address "{address}", module "{module}", name "{name}", and type args [{type_args}]')
def step_given_struct_components(context, address, module, name, type_args):
    context.world.struct_address = address
    context.world.struct_module = module
    context.world.struct_name = name
    context.world.struct_type_args = type_args


# =============================================================================
# When Steps - Parsing
# =============================================================================


@when("I parse it as a TypeTag")
def step_parse_as_typetag(context):
    try:
        context.world.type_tag = parse_type_tag(context.world.type_string)
        context.world.test_vectors["original_type_tag"] = context.world.type_tag
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I parse it as a MoveModuleId")
def step_parse_as_module_id(context):
    try:
        parts = context.world.module_string.split("::")
        if len(parts) != 2:
            raise ValueError("Invalid module ID format")
        context.world.module_address = parts[0]
        context.world.module_name = parts[1]
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I parse and BCS serialize the TypeTag")
def step_parse_and_bcs_serialize(context):
    try:
        type_tag = parse_type_tag(context.world.type_string)
        serializer = Serializer()
        type_tag.serialize(serializer)
        context.world.result_bytes = serializer.output()
        context.world.type_tag = type_tag
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Formatting
# =============================================================================


@when("I format it as a string")
def step_format_as_string(context):
    if getattr(context.world, 'type_tag', None) is not None:
        context.world.result = format_type_tag(context.world.type_tag)
    elif getattr(context.world, 'module_address', None) is not None:
        # Format module ID
        addr = context.world.module_address
        if addr.startswith("0x"):
            addr = "0x" + (addr[2:].lstrip("0") or "0")
        context.world.result = f"{addr}::{context.world.module_name}"
    else:
        raise ValueError("Nothing to format")


# =============================================================================
# When Steps - Struct Creation
# =============================================================================


@when("I create a MoveStructTag")
def step_create_struct_tag(context):
    try:
        addr = AccountAddress.from_str(context.world.struct_address)
        
        # Parse type args
        type_args = []
        if context.world.struct_type_args == "AptosCoin":
            aptos_coin = StructTag(AccountAddress.from_str("0x1"), "aptos_coin", "AptosCoin", [])
            type_args.append(TypeTag(aptos_coin))
        
        context.world.struct_tag = StructTag(
            addr,
            context.world.struct_module,
            context.world.struct_name,
            type_args
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the TypeTag")
def step_bcs_serialize_typetag(context):
    try:
        serializer = Serializer()
        context.world.type_tag.serialize(serializer)
        context.world.result_bytes = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS serialize and deserialize it")
def step_bcs_roundtrip_typetag(context):
    try:
        serializer = Serializer()
        context.world.type_tag.serialize(serializer)
        data = serializer.output()
        
        deserializer = Deserializer(data)
        context.world.result = TypeTag.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Parsing Success/Failure
# =============================================================================


@then("the parsing should fail with a parse error")
def step_parsing_fail_with_parse_error(context):
    assert context.world.error is not None


@then("the parsing should fail")
def step_parsing_fail(context):
    assert context.world.error is not None


# =============================================================================
# Then Steps - TypeTag Variant Assertions
# =============================================================================


@then("the TypeTag variant should be Bool")
def step_typetag_variant_bool(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.BOOL


@then("the TypeTag variant should be U8")
def step_typetag_variant_u8(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.U8


@then("the TypeTag variant should be U16")
def step_typetag_variant_u16(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.U16


@then("the TypeTag variant should be U32")
def step_typetag_variant_u32(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.U32


@then("the TypeTag variant should be U64")
def step_typetag_variant_u64(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.U64


@then("the TypeTag variant should be U128")
def step_typetag_variant_u128(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.U128


@then("the TypeTag variant should be U256")
def step_typetag_variant_u256(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.U256


@then("the TypeTag variant should be Address")
def step_typetag_variant_address(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.ACCOUNT_ADDRESS


@then("the TypeTag variant should be Signer")
def step_typetag_variant_signer(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.SIGNER


@then("the TypeTag variant should be Vector")
def step_typetag_variant_vector(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.VECTOR


@then("the TypeTag variant should be Struct")
def step_typetag_variant_struct(context):
    assert get_type_tag_variant(context.world.type_tag) == TypeTag.STRUCT


# =============================================================================
# Then Steps - Inner Type Assertions
# =============================================================================


@then("the inner type should be U8")
def step_inner_type_u8(context):
    inner = context.world.type_tag.value  # Vector's inner type
    assert get_type_tag_variant(inner) == TypeTag.U8


@then("the inner type should be a Vector of U8")
def step_inner_type_vector_u8(context):
    inner = context.world.type_tag.value
    assert get_type_tag_variant(inner) == TypeTag.VECTOR
    assert get_type_tag_variant(inner.value) == TypeTag.U8


@then("the inner type should be a Struct")
def step_inner_type_struct(context):
    inner = context.world.type_tag.value
    assert get_type_tag_variant(inner) == TypeTag.STRUCT


# =============================================================================
# Then Steps - Struct Assertions
# =============================================================================


def get_short_address(addr: AccountAddress) -> str:
    """Convert address to short form without leading zeros."""
    full = str(addr)
    hex_part = full[2:] if full.startswith("0x") else full
    return "0x" + (hex_part.lstrip("0") or "0")


@then('the struct address should be "{expected}"')
def step_struct_address(context, expected):
    struct_tag = context.world.type_tag.value  # StructTag
    actual = get_short_address(struct_tag.address)
    assert actual == expected, f"Expected {expected}, got {actual}"


@then('the struct module should be "{expected}"')
def step_struct_module(context, expected):
    struct_tag = context.world.type_tag.value
    assert struct_tag.module == expected


@then('the struct name should be "{expected}"')
def step_struct_name(context, expected):
    struct_tag = context.world.type_tag.value
    assert struct_tag.name == expected


@then("the struct should have {count:d} type arguments")
def step_struct_type_arg_count(context, count):
    struct_tag = context.world.type_tag.value
    assert len(struct_tag.type_args) == count


@then("the struct should have {count:d} type argument")
def step_struct_type_arg_count_singular(context, count):
    struct_tag = context.world.type_tag.value
    assert len(struct_tag.type_args) == count


@then('type argument {index:d} should be a Struct named "{name}"')
def step_type_arg_struct_named(context, index, name):
    struct_tag = context.world.type_tag.value
    type_arg = struct_tag.type_args[index]
    assert get_type_tag_variant(type_arg) == TypeTag.STRUCT
    assert type_arg.value.name == name


@then("type argument {index:d} should be U64")
def step_type_arg_u64(context, index):
    struct_tag = context.world.type_tag.value
    type_arg = struct_tag.type_args[index]
    assert get_type_tag_variant(type_arg) == TypeTag.U64


# =============================================================================
# Then Steps - Module ID Assertions
# =============================================================================


@then('the module address should be "{expected}"')
def step_module_address(context, expected):
    actual = context.world.module_address
    # Normalize for comparison
    if actual.startswith("0x"):
        actual = "0x" + (actual[2:].lstrip("0") or "0")
    expected_clean = expected.lstrip("0x")
    expected_norm = "0x" + (expected_clean.lstrip("0") or "0")
    assert actual == expected_norm, f"Expected {expected_norm}, got {actual}"


@then('the module name should be "{expected}"')
def step_module_name(context, expected):
    assert context.world.module_name == expected


# =============================================================================
# Then Steps - Struct Tag Assertions
# =============================================================================


@then("the struct tag should be valid")
def step_struct_tag_valid(context):
    assert context.world.error is None
    assert context.world.struct_tag is not None


@then('the string representation should be "{expected}"')
def step_string_representation(context, expected):
    actual = str(context.world.struct_tag)
    assert actual == expected, f"Expected {expected}, got {actual}"


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the first byte should be the U64 variant index")
def step_first_byte_u64_variant(context):
    # In BCS, TypeTag serializes the variant index first
    # U64 is one of the primitive variants
    assert context.world.result_bytes is not None
    # Variant index for U64 is 2 (0=Bool, 1=U8, 2=U64, etc.)
    assert context.world.result_bytes[0] == 2


@then("the serialization should succeed")
def step_serialization_succeed(context):
    assert context.world.error is None
    assert context.world.result_bytes is not None


@then("the result should be deserializable back to the same TypeTag")
def step_result_deserializable(context):
    deserializer = Deserializer(context.world.result_bytes)
    result = TypeTag.deserialize(deserializer)
    # Compare string representations
    assert format_type_tag(result) == format_type_tag(context.world.type_tag)


@then("the result should equal the original TypeTag")
def step_result_equals_original_typetag(context):
    original = context.world.test_vectors.get("original_type_tag")
    result = context.world.result
    assert format_type_tag(result) == format_type_tag(original)
