"""
General step definitions that are commonly used across multiple features.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - General Setup
# =============================================================================


@given("the Aptos SDK is available")
def step_sdk_available(context):
    try:
        context.world.result = True
    except ImportError:
        context.world.result = False
        raise AssertionError("Aptos SDK is not installed")


@given("a testnet client")
def step_testnet_client(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"
    # Note: For actual API calls, would need to use async client


@given("a devnet client")
def step_devnet_client(context):
    context.world.network_url = "https://fullnode.devnet.aptoslabs.com/v1"


# =============================================================================
# When Steps - Generic Actions
# =============================================================================


@when("I do nothing")
def step_do_nothing(context):
    pass


@when("I wait for {seconds:d} seconds")
def step_wait_seconds(context, seconds):
    import time

    time.sleep(seconds)


# =============================================================================
# Then Steps - Generic Assertions
# =============================================================================


@then("it should succeed")
def step_should_succeed(context):
    assert (
        context.world.error is None
    ), f"Expected success but got error: {context.world.error}"


@then("it should fail")
def step_should_fail(context):
    assert context.world.error is not None, "Expected failure but succeeded"


@then("the result should be true")
def step_result_true(context):
    assert context.world.result is True


@then("the result should be false")
def step_result_false(context):
    assert context.world.result is False


@then("the result should not be null")
def step_result_not_null(context):
    assert context.world.result is not None


@then("there should be no error")
def step_no_error(context):
    assert context.world.error is None


@then("there should be an error")
def step_should_have_error(context):
    assert context.world.error is not None


@then('the error message should contain "{text}"')
def step_error_contains(context, text):
    assert context.world.error is not None
    assert text.lower() in str(context.world.error).lower()


# =============================================================================
# Then Steps - Comparison
# =============================================================================


@then("the result should equal {expected:d}")
def step_result_equals_int(context, expected):
    assert context.world.result == expected


@then('the result should equal "{expected}"')
def step_result_equals_string(context, expected):
    assert str(context.world.result) == expected


@then("the results should be identical")
def step_results_identical(context):
    result1 = context.world.test_vectors.get("result1")
    result2 = context.world.test_vectors.get("result2")
    assert result1 == result2


@then("the results should be different")
def step_results_different(context):
    # Check for hash results first
    if (
        context.world.hash_result is not None
        and context.world.hash_result_2 is not None
    ):
        assert context.world.hash_result != context.world.hash_result_2
    else:
        result1 = context.world.test_vectors.get("result1")
        result2 = context.world.test_vectors.get("result2")
        assert result1 != result2
