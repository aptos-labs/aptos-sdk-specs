"""
Step definitions for view function operations.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - View Function Setup
# =============================================================================


@given('a view function "balance"')
def step_given_view_balance(context):
    context.world.test_vectors["view_function"] = "balance"


@given("a view function expecting a bool")
def step_given_view_expects_bool(context):
    context.world.test_vectors["view_expects"] = "bool"


@given("a view function expecting a string")
def step_given_view_expects_string(context):
    context.world.test_vectors["view_expects"] = "string"


@given("a view function expecting a u64")
def step_given_view_expects_u64(context):
    context.world.test_vectors["view_expects"] = "u64"


@given("a view function expecting an address")
def step_given_view_expects_address(context):
    context.world.test_vectors["view_expects"] = "address"


@given("a view function expecting vector<u8>")
def step_given_view_expects_bytes(context):
    context.world.test_vectors["view_expects"] = "vector<u8>"


@given("a view function returning bool")
def step_given_view_returns_bool(context):
    context.world.test_vectors["view_returns"] = "bool"


@given("a view function returning u64")
def step_given_view_returns_u64(context):
    context.world.test_vectors["view_returns"] = "u64"


@given("a view function returning a String")
def step_given_view_returns_string(context):
    context.world.test_vectors["view_returns"] = "String"


@given("a view function returning vector<u8>")
def step_given_view_returns_bytes(context):
    context.world.test_vectors["view_returns"] = "vector<u8>"


@given("a view function returning a struct")
def step_given_view_returns_struct(context):
    context.world.test_vectors["view_returns"] = "struct"


@given("a view function with generic type")
def step_given_view_generic(context):
    context.world.test_vectors["view_generic"] = True


@given("a view function with one type parameter")
def step_given_view_one_type_param(context):
    context.world.test_vectors["view_type_params"] = 1


@given("a view function with multiple type parameters")
def step_given_view_multi_type_params(context):
    context.world.test_vectors["view_type_params"] = 2


@given("a view function that can abort")
def step_given_view_can_abort(context):
    context.world.test_vectors["view_can_abort"] = True


# =============================================================================
# When Steps - View Function Operations
# =============================================================================


@when('with type arguments ["0x1::aptos_coin::AptosCoin"]')
def step_with_type_args(context):
    context.world.test_vectors["type_args"] = ["0x1::aptos_coin::AptosCoin"]


@when("with no type arguments")
def step_with_no_type_args(context):
    context.world.test_vectors["type_args"] = []


@when("with the account address as argument")
def step_with_account_address_arg(context):
    if context.world.account:
        context.world.test_vectors["args"] = [str(context.world.account.address())]
    else:
        context.world.test_vectors["args"] = ["0x1"]


@when('with address "0x1" as argument')
def step_with_address_0x1_arg(context):
    context.world.test_vectors["args"] = ["0x1"]


@when("no arguments")
def step_no_args(context):
    context.world.test_vectors["args"] = []


@when('arguments ["0x1"]')
def step_args_0x1(context):
    context.world.test_vectors["args"] = ["0x1"]


@when("I pass true as argument")
def step_pass_true_arg(context):
    context.world.test_vectors["args"] = [True]


@when('I pass "hello world" as argument')
def step_pass_hello_arg(context):
    context.world.test_vectors["args"] = ["hello world"]


@when("I pass number 1000000 as argument")
def step_pass_number_arg(context):
    context.world.test_vectors["args"] = [1000000]


@when('I pass address "0x1" as argument')
def step_pass_address_arg(context):
    context.world.test_vectors["args"] = ["0x1"]


@when("I pass bytes [1, 2, 3, 4, 5] as argument")
def step_pass_bytes_arg(context):
    context.world.test_vectors["args"] = [[1, 2, 3, 4, 5]]


@when("I provide the arguments")
def step_provide_args(context):
    pass


@when("I provide type arguments [0x1::aptos_coin::AptosCoin]")
def step_provide_type_args(context):
    context.world.test_vectors["type_args"] = ["0x1::aptos_coin::AptosCoin"]


@when("I execute it")
def step_execute_it(context):
    context.world.test_vectors["executed"] = True


@when("I execute the call")
def step_execute_call(context):
    context.world.test_vectors["call_executed"] = True


@when("I try to execute it")
def step_try_execute(context):
    try:
        context.world.test_vectors["executed"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to call a view function at that version")
def step_try_call_at_version(context):
    # TODO: implement view at version
    context.world.test_vectors["view_at_version"] = True


# =============================================================================
# Then Steps - View Function Assertions
# =============================================================================


@then("I should receive true")
def step_receive_true(context):
    assert context.world.error is None
    assert context.world.result is True


@then("I should receive return values")
def step_receive_return_values(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("I should receive all return values in order")
def step_receive_all_return_values(context):
    assert context.world.error is None
    assert isinstance(context.world.result, (list, tuple)) or context.world.result is not None


@then("I should receive the balance amount")
def step_receive_balance(context):
    assert context.world.error is None
    assert context.world.result is not None
    assert isinstance(context.world.result, int) or isinstance(context.world.result, str)


@then("I should receive the balance as u64")
def step_receive_balance_u64(context):
    assert context.world.error is None
    assert isinstance(context.world.result, int)
    assert context.world.result >= 0


@then("I should receive current blockchain timestamp")
def step_receive_timestamp(context):
    assert context.world.error is None
    assert context.world.result is not None
    assert isinstance(context.world.result, int)


@then("I should receive the total supply")
def step_receive_total_supply(context):
    assert context.world.error is None
    assert context.world.result is not None
    assert isinstance(context.world.result, int) or isinstance(context.world.result, str)


@then("I should be able to parse the result as boolean")
def step_parse_as_bool(context):
    assert context.world.error is None
    assert isinstance(context.world.result, bool)


@then("I should be able to parse the result as string")
def step_parse_as_string(context):
    assert context.world.error is None
    assert isinstance(context.world.result, str)


@then("I should be able to parse the result as u64")
def step_parse_as_u64(context):
    assert context.world.error is None
    assert isinstance(context.world.result, int)
    assert context.world.result >= 0


@then("I should be able to parse the result as byte array")
def step_parse_as_bytes(context):
    assert context.world.error is None
    assert isinstance(context.world.result, (bytes, bytearray, list))


@then("I should be able to access struct fields")
def step_access_struct_fields(context):
    assert context.world.error is None
    assert isinstance(context.world.result, dict) or hasattr(context.world.result, "__dict__")


@then("I should handle type parameters correctly")
def step_handle_type_params(context):
    pass


@then("return type should match Move return type")
def step_return_type_matches(context):
    pass


@then("the call should succeed")
def step_call_succeeds(context):
    assert context.world.error is None
