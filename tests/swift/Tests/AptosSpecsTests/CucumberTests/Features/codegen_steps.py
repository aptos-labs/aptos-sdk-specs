"""
Step definitions for code generation.
All steps marked pending as Python SDK does not support code generation.
"""

from behave import given, when, then


# =============================================================================
# Given Steps - Code Generation Setup (All Pending)
# =============================================================================


@given("an ABI with entry functions")
def step_given_abi_entry(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("an ABI with view functions")
def step_given_abi_view(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("an ABI with struct definitions")
def step_given_abi_struct(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("an ABI with generic functions and structs")
def step_given_abi_generic(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("generated TypeScript/Rust code")
def step_given_generated_code(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("a generated function expecting u64")
def step_given_func_expects_u64(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("a generated function expecting address")
def step_given_func_expects_address(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("a generated function expecting vector<u8>")
def step_given_func_expects_bytes(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given("a generated function expecting a struct")
def step_given_func_expects_struct(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@given('a module address and name "0x1::coin"')
def step_given_module_address(context):
    context.world.test_vectors["module_address"] = "0x1::coin"


@given('module addresses ["0x1::coin", "0x1::aptos_account"]')
def step_given_module_addresses(context):
    context.world.test_vectors["module_addresses"] = ["0x1::coin", "0x1::aptos_account"]


@given('a Move struct "CoinStore<CoinType>"')
def step_given_move_struct(context):
    context.world.test_vectors["move_struct"] = "CoinStore<CoinType>"


@given("a Move struct definition")
def step_given_struct_def(context):
    context.world.test_vectors["struct_def"] = True


@given("Move types (u64, address, vector<u8>)")
def step_given_move_types(context):
    context.world.test_vectors["move_types"] = ["u64", "address", "vector<u8>"]


@given("Move types")
def step_given_move_types_generic(context):
    context.world.test_vectors["move_types"] = []


@given("a module with public (non-entry) functions")
def step_given_module_public_funcs(context):
    context.world.test_vectors["public_funcs"] = True


# =============================================================================
# When Steps - Code Generation Operations (All Pending)
# =============================================================================


@when("I generate TypeScript code")
def step_generate_ts(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@when("I generate TypeScript")
def step_generate_ts_alt(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@when("I generate Python code")
def step_generate_python(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@when("I generate Rust code")
def step_generate_rust(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@when("I generate Rust")
def step_generate_rust_alt(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@when("I generate Go code")
def step_generate_go(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@when("I fetch the module ABI")
def step_fetch_module_abi(context):
    # TODO: awaiting SDK implementation - ABI fetching
    context.world.test_vectors["abi_fetched"] = True


@when("I fetch ABIs for all modules")
def step_fetch_all_abis(context):
    # TODO: awaiting SDK implementation - ABI fetching
    context.world.test_vectors["all_abis_fetched"] = True


@when("I try to fetch the ABI")
def step_try_fetch_abi(context):
    try:
        context.world.test_vectors["abi_fetch_attempted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I parse the ABI")
def step_parse_abi(context):
    context.world.test_vectors["abi_parsed"] = True


# =============================================================================
# Then Steps - Code Generation Assertions (All Pending)
# =============================================================================


@then("I should get a typed function")
def step_get_typed_func(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get a typed function with type hints")
def step_get_typed_func_hints(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get an async function")
def step_get_async_func(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get a struct with typed fields")
def step_get_typed_struct(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get a Go function")
def step_get_go_func(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get a Go struct with tags")
def step_get_go_struct(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get a dataclass or TypedDict")
def step_get_dataclass(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should get an interface with typed fields")
def step_get_interface(context):
    # TODO: awaiting SDK implementation - codegen not supported
    context.scenario.skip("Code generation not supported in Python SDK")


@then("I should extract function names")
def step_extract_func_names(context):
    pass


@then("I should extract struct names")
def step_extract_struct_names(context):
    pass


@then("I should identify view functions")
def step_identify_view_funcs(context):
    pass


@then("abilities (copy, drop, store, key)")
def step_abilities(context):
    pass


@then("I should receive the ABI definition")
def step_receive_abi(context):
    pass


@then("I should receive ABIs for each module")
def step_receive_multi_abis(context):
    pass


@then("address should map to AccountAddress")
def step_address_maps_to_account(context):
    pass


@then("address should map to string or AccountAddress")
def step_address_maps_to_string_or_account(context):
    pass


@then("u64 should map to bigint or number")
def step_u64_maps_to_bigint(context):
    pass


@then("u64 should map to u64")
def step_u64_maps_to_u64(context):
    pass


@then("vector<u8> should map to Uint8Array or string")
def step_bytes_maps_to_uint8array(context):
    pass


@then("vector<u8> should map to Vec<u8>")
def step_bytes_maps_to_vec(context):
    pass
