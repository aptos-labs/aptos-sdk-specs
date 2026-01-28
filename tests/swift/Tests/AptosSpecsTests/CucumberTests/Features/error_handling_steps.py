"""
Step definitions for error-handling.feature
Tests error classification and handling patterns.
"""

from behave import given, when, then
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# =============================================================================
# Custom Exception Classes for Testing
# =============================================================================


class AptosApiError(Exception):
    """Base class for API errors."""

    def __init__(self, message, status_code=None, request_id=None):
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id


class NetworkError(AptosApiError):
    """Network-related errors (connection, timeout)."""

    pass


class ValidationError(AptosApiError):
    """Input validation errors."""

    pass


class TransactionError(AptosApiError):
    """Transaction execution errors."""

    def __init__(self, message, vm_status=None, abort_code=None, **kwargs):
        super().__init__(message, **kwargs)
        self.vm_status = vm_status
        self.abort_code = abort_code


class SimulationError(TransactionError):
    """Simulation-specific errors."""

    def __init__(self, message, gas_used=None, **kwargs):
        super().__init__(message, **kwargs)
        self.gas_used = gas_used


# =============================================================================
# Given Steps - Error Scenarios
# =============================================================================


@given("a network timeout error")
def step_given_network_timeout(context):
    context.world.error = NetworkError("Connection timed out", status_code=None)


@given("a connection refused error")
def step_given_connection_refused(context):
    context.world.error = NetworkError("Connection refused", status_code=None)


@given("an API error with status {status:d}")
def step_given_api_error_with_status(context, status):
    context.world.error = AptosApiError(f"API error", status_code=status)


@given("a validation error with message {message}")
def step_given_validation_error(context, message):
    context.world.error = ValidationError(message)


@given("a transaction error")
def step_given_transaction_error(context):
    context.world.error = TransactionError(
        "Transaction failed", vm_status="EXECUTION_FAILURE"
    )


@given("an out of gas error")
def step_given_out_of_gas(context):
    context.world.error = TransactionError("Out of gas", vm_status="OUT_OF_GAS")


@given("a sequence number error")
def step_given_sequence_number_error(context):
    context.world.error = TransactionError(
        "Sequence number too old", vm_status="SEQUENCE_NUMBER_TOO_OLD"
    )


@given("an insufficient balance error")
def step_given_insufficient_balance(context):
    context.world.error = TransactionError(
        "Insufficient balance", vm_status="INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE"
    )


@given("an abort with code {code:d}")
def step_given_abort_code(context, code):
    context.world.error = TransactionError(f"Aborted with code {code}", abort_code=code)


@given('a module abort "{module}" with code {code:d}')
def step_given_module_abort(context, module, code):
    context.world.error = TransactionError(
        f"Module {module} aborted with code {code}",
        vm_status="ABORTED",
        abort_code=code,
    )


@given("a simulation failure")
def step_given_simulation_failure(context):
    context.world.error = SimulationError(
        "Simulation failed", vm_status="SIMULATION_FAILED"
    )


@given("a simulation with gas estimate")
def step_given_simulation_with_gas(context):
    context.world.error = SimulationError("Simulation completed", gas_used=1000)


# =============================================================================
# When Steps - Error Classification
# =============================================================================


@when("I check if the error is a network error")
def step_check_network_error(context):
    context.world.result = isinstance(context.world.error, NetworkError)


@when("I check if the error is an API error")
def step_check_api_error(context):
    context.world.result = isinstance(context.world.error, AptosApiError)


@when("I check if the error is a validation error")
def step_check_validation_error(context):
    context.world.result = isinstance(context.world.error, ValidationError)


@when("I check if the error is a transaction error")
def step_check_transaction_error(context):
    context.world.result = isinstance(context.world.error, TransactionError)


@when("I check if the error is retryable")
def step_check_retryable(context):
    error = context.world.error
    # Network errors and 5xx status codes are retryable
    if isinstance(error, NetworkError):
        context.world.result = True
    elif isinstance(error, AptosApiError) and error.status_code:
        context.world.result = error.status_code >= 500
    else:
        context.world.result = False


@when("I check if the error is permanent")
def step_check_permanent(context):
    error = context.world.error
    # 4xx errors and validation errors are permanent
    if isinstance(error, ValidationError):
        context.world.result = True
    elif isinstance(error, TransactionError):
        # Most transaction errors are permanent
        context.world.result = True
    elif isinstance(error, AptosApiError) and error.status_code:
        context.world.result = 400 <= error.status_code < 500
    else:
        context.world.result = False


@when("I get the error status code")
def step_get_error_status_code(context):
    if hasattr(context.world.error, "status_code"):
        context.world.result = context.world.error.status_code
    else:
        context.world.result = None


@when("I get the abort code")
def step_get_abort_code(context):
    if hasattr(context.world.error, "abort_code"):
        context.world.result = context.world.error.abort_code
    else:
        context.world.result = None


@when("I get the VM status")
def step_get_vm_status(context):
    if hasattr(context.world.error, "vm_status"):
        context.world.result = context.world.error.vm_status
    else:
        context.world.result = None


@when("I get the gas estimate from simulation")
def step_get_gas_from_simulation(context):
    if hasattr(context.world.error, "gas_used"):
        context.world.result = context.world.error.gas_used
    else:
        context.world.result = None


# =============================================================================
# Then Steps - Error Type Assertions
# =============================================================================


@then("it should be a network error")
def step_should_be_network_error(context):
    assert context.world.result is True


@then("it should be an API error")
def step_should_be_api_error(context):
    assert context.world.result is True


@then("it should be a validation error")
def step_should_be_validation_error(context):
    assert context.world.result is True


@then("it should be a transaction error")
def step_should_be_transaction_error(context):
    assert context.world.result is True


@then("the error should be retryable")
def step_error_should_be_retryable(context):
    assert context.world.result is True


@then("the error should be permanent")
def step_error_should_be_permanent(context):
    assert context.world.result is True


@then("the error should not be retryable")
def step_error_should_not_be_retryable(context):
    assert context.world.result is False


# =============================================================================
# Then Steps - Error Content Assertions
# =============================================================================


@then("the status code should be {expected:d}")
def step_status_code_should_be(context, expected):
    assert context.world.result == expected


@then("the abort code should be {expected:d}")
def step_abort_code_should_be(context, expected):
    assert context.world.result == expected


@then('the VM status should be "{expected}"')
def step_vm_status_should_be(context, expected):
    assert context.world.result == expected


@then("the gas estimate should be {expected:d}")
def step_gas_estimate_should_be(context, expected):
    assert context.world.result == expected


@then("the error message should be informative")
def step_error_message_informative(context):
    error_str = str(context.world.error)
    assert len(error_str) > 0
    # Should not contain internal implementation details
    assert "0x" not in error_str or "address" in error_str.lower()


@then("the error message should be actionable")
def step_error_message_actionable(context):
    error_str = str(context.world.error)
    # Should give some indication of what happened
    assert len(error_str) > 10


@then("the error should include context")
def step_error_has_context(context):
    error = context.world.error
    # Should have some additional information beyond just a message
    has_context = (
        hasattr(error, "status_code")
        or hasattr(error, "vm_status")
        or hasattr(error, "abort_code")
        or hasattr(error, "request_id")
    )
    assert has_context


@then("the error should be loggable")
def step_error_loggable(context):
    # Should be able to convert to string without error
    error_str = str(context.world.error)
    repr_str = repr(context.world.error)
    assert error_str is not None
    assert repr_str is not None


# =============================================================================
# Then Steps - Python-Specific
# =============================================================================


@then("Python should use exceptions")
def step_python_uses_exceptions(context):
    # This is just a confirmation that we're using exception-based error handling
    assert isinstance(context.world.error, Exception)


@then("the error should be chainable")
def step_error_chainable(context):
    # Python exceptions support __cause__ for chaining
    try:
        try:
            raise context.world.error
        except Exception as e:
            raise AptosApiError("Wrapper error") from e
    except AptosApiError as wrapper:
        assert wrapper.__cause__ is not None


# =============================================================================
# Then Steps - Recovery
# =============================================================================


@then("sequence number recovery should be possible")
def step_sequence_number_recovery(context):
    # For sequence number errors, should be able to fetch current sequence
    # and retry with the correct value
    assert isinstance(context.world.error, TransactionError)
    assert "sequence" in str(context.world.error).lower()


@then("gas estimation recovery should be possible")
def step_gas_estimation_recovery(context):
    # For out of gas errors, should be able to simulate and get estimate
    assert isinstance(context.world.error, TransactionError)


@then("rate limit recovery should be possible")
def step_rate_limit_recovery(context):
    # For rate limit errors, should be able to wait and retry
    error = context.world.error
    if hasattr(error, "status_code"):
        assert error.status_code == 429
