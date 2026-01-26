"""
Step definitions for view-functions.feature
Tests view function execution for reading on-chain state.
"""

from support.vectors import hex_to_bytes, bytes_to_hex
from aptos_sdk.bcs import Serializer
from aptos_sdk.type_tag import TypeTag
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient
from behave import given, when, then
import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Helper to run async functions synchronously
def run_async(coro):
    """Run an async coroutine synchronously."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# =============================================================================
# Given Steps - View Function Setup
# =============================================================================


@given("a view function client")
def step_given_view_function_client(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"


@given('a view function module "{module}"')
def step_given_view_module(context, module):
    context.world.test_vectors["view_module"] = module


@given('a view function name "{function}"')
def step_given_view_function_name(context, function):
    context.world.test_vectors["view_function"] = function


@given("view function arguments []")
def step_given_empty_view_args(context):
    context.world.test_vectors["view_args"] = []


@given('a view function argument "{arg}"')
def step_given_view_arg(context, arg):
    args = context.world.test_vectors.get("view_args", [])
    args.append(arg)
    context.world.test_vectors["view_args"] = args


@given("view function type arguments []")
def step_given_empty_view_type_args(context):
    context.world.test_vectors["view_type_args"] = []


@given('a view function type argument "{type_arg}"')
def step_given_view_type_arg(context, type_arg):
    type_args = context.world.test_vectors.get("view_type_args", [])
    type_args.append(type_arg)
    context.world.test_vectors["view_type_args"] = type_args


# =============================================================================
# Given Steps - Common View Functions
# =============================================================================


@given('I want to check balance of "{address}"')
def step_given_check_balance(context, address):
    context.world.test_vectors["view_module"] = "0x1::coin"
    context.world.test_vectors["view_function"] = "balance"
    context.world.test_vectors["view_args"] = [address]
    context.world.test_vectors["view_type_args"] = ["0x1::aptos_coin::AptosCoin"]


@given('I want to check if account "{address}" exists')
def step_given_check_account_exists(context, address):
    context.world.test_vectors["view_module"] = "0x1::account"
    context.world.test_vectors["view_function"] = "exists_at"
    context.world.test_vectors["view_args"] = [address]
    context.world.test_vectors["view_type_args"] = []


@given('I want to get sequence number of "{address}"')
def step_given_get_sequence_number(context, address):
    context.world.test_vectors["view_module"] = "0x1::account"
    context.world.test_vectors["view_function"] = "get_sequence_number"
    context.world.test_vectors["view_args"] = [address]
    context.world.test_vectors["view_type_args"] = []


# =============================================================================
# When Steps - View Function Execution
# =============================================================================


@when("I execute the view function")
def step_execute_view_function(context):
    try:

        async def _execute_view():
            client = RestClient(context.world.network_url)
            try:
                module = context.world.test_vectors.get("view_module", "0x1::coin")
                function = context.world.test_vectors.get("view_function", "balance")
                args = context.world.test_vectors.get("view_args", [])
                type_args = context.world.test_vectors.get("view_type_args", [])

                result = await client.view(f"{module}::{function}", type_args, args)
                return result
            finally:
                await client.close()

        context.world.result = run_async(_execute_view())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I execute the view function with BCS encoding")
def step_execute_view_bcs(context):
    try:

        async def _execute_view_bcs():
            client = RestClient(context.world.network_url)
            try:
                module = context.world.test_vectors.get("view_module")
                function = context.world.test_vectors.get("view_function")
                args = context.world.test_vectors.get("view_args", [])
                type_args = context.world.test_vectors.get("view_type_args", [])

                # BCS encode arguments
                encoded_args = []
                for arg in args:
                    if arg.startswith("0x"):
                        # Address argument
                        serializer = Serializer()
                        serializer.struct(AccountAddress.from_str(arg))
                        encoded_args.append(serializer.output())
                    else:
                        # String argument as-is
                        encoded_args.append(arg)

                result = await client.view(
                    f"{module}::{function}", type_args, encoded_args
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_execute_view_bcs())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to execute an invalid view function")
def step_execute_invalid_view(context):
    try:

        async def _execute_invalid():
            client = RestClient(context.world.network_url)
            try:
                result = await client.view("0x1::nonexistent::function", [], [])
                return result
            finally:
                await client.close()

        context.world.result = run_async(_execute_invalid())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I execute the view function with wrong argument count")
def step_execute_view_wrong_args(context):
    try:

        async def _execute_wrong_args():
            client = RestClient(context.world.network_url)
            try:
                # coin::balance requires an address argument
                result = await client.view(
                    "0x1::coin::balance",
                    ["0x1::aptos_coin::AptosCoin"],
                    [],  # Missing required argument
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_execute_wrong_args())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I execute the view function with wrong type arguments")
def step_execute_view_wrong_type_args(context):
    try:

        async def _execute_wrong_type():
            client = RestClient(context.world.network_url)
            try:
                result = await client.view(
                    "0x1::coin::balance", ["invalid::type::Tag"], ["0x1"]
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_execute_wrong_type())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - View Function Assertions
# =============================================================================


@then("the view function should succeed")
def step_view_function_succeed(context):
    assert context.world.error is None


@then("the view function should fail")
def step_view_function_fail(context):
    assert context.world.error is not None


@then("the result should be returned")
def step_view_result_returned(context):
    assert context.world.result is not None


@then("the result should be a list")
def step_view_result_is_list(context):
    assert isinstance(context.world.result, list)


@then("the result should have {count:d} elements")
def step_view_result_count(context, count):
    assert len(context.world.result) == count


@then('the result should contain "{expected}"')
def step_view_result_contains(context, expected):
    result_str = str(context.world.result)
    assert expected in result_str


@then("the result should be a number")
def step_view_result_is_number(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    # Could be string representation of number
    assert str(result).isdigit() or isinstance(result, (int, float))


@then("the result should be a boolean")
def step_view_result_is_boolean(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert isinstance(result, bool) or result in ["true", "false", True, False]


# Note: "the result should be true/false" are defined in general_steps.py


# =============================================================================
# Then Steps - Error Assertions
# =============================================================================


@then("I should get a function not found error")
def step_function_not_found_error(context):
    assert context.world.error is not None
    error_str = str(context.world.error).lower()
    assert "not found" in error_str or "does not exist" in error_str


@then("I should get an argument error")
def step_argument_error(context):
    assert context.world.error is not None


@then("I should get a type argument error")
def step_type_argument_error(context):
    assert context.world.error is not None
