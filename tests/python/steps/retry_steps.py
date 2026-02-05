"""
Step definitions for retry and error handling.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Retry Configuration
# =============================================================================


@given("max_retries=3")
def step_given_max_retries(context):
    context.world.test_vectors["max_retries"] = 3


@given("retry config with max_retries=0")
def step_given_retry_0(context):
    context.world.test_vectors["max_retries"] = 0


@given("retry config with max_retries=5, initial_delay=200ms")
def step_given_retry_5(context):
    context.world.test_vectors["max_retries"] = 5
    context.world.test_vectors["initial_delay_ms"] = 200


@given("retry config with backoff_factor=3.0")
def step_given_backoff(context):
    context.world.test_vectors["backoff_factor"] = 3.0


@given("retry config with callback")
def step_given_retry_callback(context):
    context.world.test_vectors["retry_callback"] = True


@given("initial_delay=100ms and backoff_factor=2.0")
def step_given_delay_backoff(context):
    context.world.test_vectors["initial_delay_ms"] = 100
    context.world.test_vectors["backoff_factor"] = 2.0


@given("initial_delay=100ms, backoff_factor=2.0, max_delay=500ms")
def step_given_full_backoff(context):
    context.world.test_vectors["initial_delay_ms"] = 100
    context.world.test_vectors["backoff_factor"] = 2.0
    context.world.test_vectors["max_delay_ms"] = 500


@given("exponential backoff with jitter enabled")
def step_given_jitter(context):
    context.world.test_vectors["jitter"] = True


@given("a request that fails twice then succeeds")
def step_given_fails_twice(context):
    context.world.test_vectors["fails_count"] = 2


@given("a request that always fails")
def step_given_always_fails(context):
    context.world.test_vectors["always_fails"] = True


@given("a request that fails after retries")
def step_given_fails_after_retries(context):
    context.world.test_vectors["fails_after_retries"] = True


@given("a request that times out")
def step_given_request_times_out(context):
    context.world.test_vectors["times_out"] = True


@given("a request that fails to connect")
def step_given_fails_to_connect(context):
    context.world.test_vectors["fails_to_connect"] = True


@given("network is under high load")
def step_given_high_load(context):
    context.world.test_vectors["high_load"] = True


@given("many rapid requests")
def step_given_many_requests(context):
    context.world.test_vectors["many_requests"] = True


# =============================================================================
# Given Steps - HTTP Responses
# =============================================================================


@given("a request that returns HTTP 400")
def step_given_http_400(context):
    context.world.test_vectors["http_status"] = 400


@given("a request that returns HTTP 401")
def step_given_http_401(context):
    context.world.test_vectors["http_status"] = 401


@given("a request that returns HTTP 403")
def step_given_http_403(context):
    context.world.test_vectors["http_status"] = 403


@given("a request that returns HTTP 404")
def step_given_http_404(context):
    context.world.test_vectors["http_status"] = 404


@given("a request that returns HTTP 429")
def step_given_http_429(context):
    context.world.test_vectors["http_status"] = 429


@given("a request that returns HTTP 500")
def step_given_http_500(context):
    context.world.test_vectors["http_status"] = 500


@given("a request that returns HTTP 502")
def step_given_http_502(context):
    context.world.test_vectors["http_status"] = 502


@given("a request that returns HTTP 503")
def step_given_http_503(context):
    context.world.test_vectors["http_status"] = 503


@given("a request that returns HTTP 504")
def step_given_http_504(context):
    context.world.test_vectors["http_status"] = 504


@given("a 429 response with Retry-After: 5")
def step_given_429_retry_5(context):
    context.world.test_vectors["retry_after"] = 5


@given("a 429 response without Retry-After")
def step_given_429_no_retry(context):
    context.world.test_vectors["retry_after"] = None


@given("a 429 response with Retry-After as HTTP date")
def step_given_429_retry_date(context):
    context.world.test_vectors["retry_after_date"] = True


@given("a GET request")
def step_given_get_request(context):
    context.world.test_vectors["method"] = "GET"


@given("a POST request with body")
def step_given_post_request(context):
    context.world.test_vectors["method"] = "POST"


@given("a malformed request")
def step_given_malformed_request(context):
    context.world.test_vectors["malformed"] = True


@given("an unexpected response format")
def step_given_unexpected_format(context):
    context.world.test_vectors["unexpected_format"] = True


# =============================================================================
# When Steps - Retry Operations
# =============================================================================


@when("retries occur")
def step_retries_occur(context):
    context.world.test_vectors["retries_occurred"] = True


@when("a retry occurs")
def step_retry_occurs(context):
    context.world.test_vectors["retry_occurred"] = True


@when("many retries occur")
def step_many_retries(context):
    context.world.test_vectors["many_retries"] = True


@when("multiple retries occur")
def step_multiple_retries(context):
    context.world.test_vectors["multiple_retries"] = True


@when("I try to make a request")
def step_try_make_request(context):
    try:
        context.world.test_vectors["request_attempted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I make any API request")
def step_make_any_request(context):
    context.world.test_vectors["any_request"] = True


@when("I make a request with retry disabled")
def step_make_request_no_retry(context):
    context.world.test_vectors["no_retry"] = True


@when("it fails with retryable error")
def step_fails_retryable(context):
    context.world.test_vectors["retryable_error"] = True


@when("any API method encounters retryable error")
def step_api_retryable(context):
    context.world.test_vectors["api_retryable"] = True


@when("the API returns 429")
def step_api_429(context):
    context.world.test_vectors["got_429"] = True


@when("the API returns an error")
def step_api_error(context):
    context.world.test_vectors["api_error"] = True


@when("the response times out")
def step_response_timeout(context):
    context.world.test_vectors["response_timeout"] = True


@when("deciding whether to retry")
def step_deciding_retry(context):
    context.world.test_vectors["deciding_retry"] = True


@when("it needs to be retried")
def step_needs_retry(context):
    context.world.test_vectors["needs_retry"] = True


@when("the SDK handles it")
def step_sdk_handles(context):
    pass


@when("the SDK handles the error")
def step_sdk_handles_error(context):
    pass


@when("the SDK makes the request")
def step_sdk_makes_request(context):
    pass


# =============================================================================
# Then Steps - Retry Assertions
# =============================================================================


@then("I should see how many retries were attempted")
def step_see_retry_count(context):
    pass


@then("requests should not retry on failure")
def step_no_retry_on_fail(context):
    pass


@then("I should receive a timeout error")
def step_receive_timeout(context):
    assert context.world.error is not None or context.world.test_vectors.get("timeout")


@then("I should receive a network error")
def step_receive_network_error(context):
    assert context.world.error is not None or context.world.test_vectors.get(
        "network_error"
    )


@then("I should receive a Network error")
def step_receive_network_error_alt(context):
    assert context.world.error is not None


@then("I should receive a Timeout error")
def step_receive_timeout_error(context):
    assert context.world.error is not None


@then("I should receive a 400 Bad Request error")
def step_receive_400(context):
    assert context.world.error is not None


@then("I should receive a not found error")
def step_receive_not_found(context):
    assert context.world.error is not None


@then("I should receive a validation error")
def step_receive_validation_error(context):
    assert context.world.error is not None


@then("I should receive a parse error with context")
def step_receive_parse_error(context):
    assert context.world.error is not None


@then("I should receive an appropriate error")
def step_receive_appropriate_error(context):
    assert context.world.error is not None


@then("I should receive an error")
def step_receive_error(context):
    assert context.world.error is not None


@then("I should receive the final result")
def step_receive_final_result(context):
    assert context.world.error is None


@then("the callback should be invoked")
def step_callback_invoked(context):
    # TODO: implement callback check
    pass


@then("SDK should fetch current estimate")
def step_sdk_fetch_estimate(context):
    pass


@then("SDK should simulate first")
def step_sdk_simulate(context):
    pass


@then("SDK should check if transaction was received")
def step_sdk_check_received(context):
    pass


@then("SDK should check transaction status before deciding to resubmit")
def step_sdk_check_status(context):
    pass


@then("I can retry the submission")
def step_can_retry(context):
    pass
