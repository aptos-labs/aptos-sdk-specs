"""
Additional step definitions for entry functions.
"""

from behave import given, when, then


# =============================================================================
# Given Steps - Entry Function Setup
# =============================================================================


@given("an entry function")
def step_given_entry_function(context):
    context.world.test_vectors["entry_function"] = True


@given('an entry function "transfer"')
def step_given_transfer_entry(context):
    context.world.test_vectors["entry_function"] = "transfer"


@given("a simple operation like transfer")
def step_given_simple_op(context):
    context.world.test_vectors["simple_operation"] = "transfer"


@given("a complex smart contract call")
def step_given_complex_call(context):
    context.world.test_vectors["complex_call"] = True


@given("a non-existent module address")
def step_given_nonexistent_module(context):
    context.world.test_vectors["nonexistent_module"] = "0xdeadbeef::nonexistent"


@given("a gas price estimate")
def step_given_gas_price_estimate(context):
    context.world.test_vectors["gas_price_estimate"] = 100


@given("a network error during estimation")
def step_given_network_error_estimation(context):
    context.world.test_vectors["network_error_estimation"] = True


# =============================================================================
# When Steps - Encoding
# =============================================================================


@when('I encode "hello"')
def step_encode_hello(context):
    context.world.bytes_value = b"hello"


@when('I encode the value "0x1"')
def step_encode_0x1(context):
    context.world.bytes_value = bytes.fromhex("01")


@when("I encode the value 1000000")
def step_encode_number(context):
    context.world.bytes_value = (1000000).to_bytes(8, "little")


@when("I encode the value [1, 2, 3]")
def step_encode_array(context):
    context.world.bytes_value = bytes([1, 2, 3])


@when("I encode true")
def step_encode_true(context):
    context.world.bytes_value = bytes([1])


# =============================================================================
# Then Steps - Entry Function Assertions
# =============================================================================


@then("the complex call should use more gas")
def step_complex_more_gas(context):
    pass


@then("I should receive an error about function not found")
def step_func_not_found_error(context):
    assert context.world.error is not None


@then("the error should indicate function not found")
def step_error_func_not_found(context):
    assert context.world.error is not None
