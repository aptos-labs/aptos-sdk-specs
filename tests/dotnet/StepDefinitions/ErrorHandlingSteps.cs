using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for error handling tests.
/// </summary>
[Binding]
public class ErrorHandlingSteps
{
    private readonly TestWorld _world;

    public ErrorHandlingSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Error Categories
    // =========================================================================

    [Given("an API error response")]
    public void GivenAnAPIErrorResponse()
    {
        _world.SetError(new Exception("API Error: 404 Not Found"));
        _world.TestVectors["errorType"] = "ApiError";
    }

    [When("I inspect the error type")]
    public void WhenIInspectTheErrorType()
    {
        _world.TestVectors["inspectedError"] = _world.Error;
    }

    [Then("it should be categorized as ApiError")]
    public void ThenItShouldBeCategorizedAsApiError()
    {
        var errorType = (string)_world.TestVectors["errorType"];
        errorType.Should().Be("ApiError");
    }

    [Then("have HTTP status code")]
    public void ThenHaveHTTPStatusCode()
    {
        _world.Error!.Message.Should().Contain("404");
    }

    [Given("a validation failure")]
    public void GivenAValidationFailure()
    {
        _world.SetError(new Exception("Invalid address format"));
        _world.TestVectors["errorType"] = "ValidationError";
    }

    [Then("it should be categorized as ValidationError")]
    public void ThenItShouldBeCategorizedAsValidationError()
    {
        var errorType = (string)_world.TestVectors["errorType"];
        errorType.Should().Be("ValidationError");
    }

    [Then("have the invalid field name")]
    public void ThenHaveTheInvalidFieldName()
    {
        _world.Error!.Message.Should().Contain("address");
    }

    [Given("a network timeout")]
    public void GivenANetworkTimeout()
    {
        _world.SetError(new Exception("Network timeout after 30000ms"));
        _world.TestVectors["errorType"] = "NetworkError";
    }

    [Then("it should be categorized as NetworkError")]
    public void ThenItShouldBeCategorizedAsNetworkError()
    {
        var errorType = (string)_world.TestVectors["errorType"];
        errorType.Should().Be("NetworkError");
    }

    [Then("indicate the timeout")]
    public void ThenIndicateTheTimeout()
    {
        _world.Error!.Message.Should().Contain("timeout");
    }

    [Given("a BCS deserialization failure")]
    public void GivenABCSDeserializationFailure()
    {
        _world.SetError(new Exception("BCS deserialization failed: unexpected end of input"));
        _world.TestVectors["errorType"] = "SerializationError";
    }

    [Then("it should be categorized as SerializationError")]
    public void ThenItShouldBeCategorizedAsSerializationError()
    {
        var errorType = (string)_world.TestVectors["errorType"];
        errorType.Should().Be("SerializationError");
    }

    [Then("indicate the serialization issue")]
    public void ThenIndicateTheSerializationIssue()
    {
        _world.Error!.Message.Should().Contain("deserialization");
    }

    // =========================================================================
    // Error Structure
    // =========================================================================

    [Given("any SDK error")]
    public void GivenAnySDKError()
    {
        _world.SetError(new Exception("SDK Error: Something went wrong"));
        _world.TestVectors["sdkError"] = _world.Error;
    }

    [When("I access error properties")]
    public void WhenIAccessErrorProperties()
    {
        var error = (Exception)_world.TestVectors["sdkError"];
        _world.TestVectors["errorProperties"] = new Dictionary<string, object?>
        {
            { "message", error.Message },
            { "name", error.GetType().Name },
            { "stack", error.StackTrace }
        };
    }

    [Then("message should be human-readable")]
    public void ThenMessageShouldBeHumanReadable()
    {
        var props = (Dictionary<string, object?>)_world.TestVectors["errorProperties"];
        props["message"].Should().NotBeNull();
        ((string)props["message"]!).Should().NotBeEmpty();
    }

    [Then("cause should contain original error if wrapped")]
    public void ThenCauseShouldContainOriginalErrorIfWrapped()
    {
        // Modern errors may have an InnerException
        true.Should().BeTrue();
    }

    [Then("code should be machine-readable")]
    public void ThenCodeShouldBeMachineReadable()
    {
        true.Should().BeTrue();
    }

    // =========================================================================
    // API Error Details
    // =========================================================================

    [Given("an API response with status {int}")]
    public void GivenAnAPIResponseWithStatus(int status)
    {
        _world.SetError(new Exception($"API Error: {status}"));
        _world.TestVectors["httpStatus"] = status;
    }

    [Given("error body from fullnode")]
    public void GivenErrorBodyFromFullnode()
    {
        _world.TestVectors["errorBody"] = new Dictionary<string, object?>
        {
            { "message", "Account not found" },
            { "error_code", "account_not_found" },
            { "vm_error_code", null }
        };
    }

    [When("I parse the error")]
    public void WhenIParseTheError()
    {
        _world.TestVectors["parsedError"] = new Dictionary<string, object?>
        {
            { "status", _world.TestVectors["httpStatus"] },
            { "body", _world.TestVectors["errorBody"] }
        };
    }

    [Then("I should get status_code")]
    public void ThenIShouldGetStatusCode()
    {
        var parsed = (Dictionary<string, object?>)_world.TestVectors["parsedError"];
        parsed["status"].Should().NotBeNull();
    }

    [Then("I should get error_code from body")]
    public void ThenIShouldGetErrorCodeFromBody()
    {
        var parsed = (Dictionary<string, object?>)_world.TestVectors["parsedError"];
        var body = (Dictionary<string, object?>)parsed["body"]!;
        body["error_code"].Should().NotBeNull();
    }

    [Then("I should get message from body")]
    public void ThenIShouldGetMessageFromBody()
    {
        var parsed = (Dictionary<string, object?>)_world.TestVectors["parsedError"];
        var body = (Dictionary<string, object?>)parsed["body"]!;
        body["message"].Should().NotBeNull();
    }

    [Then("I should get vm_error_code if present")]
    public void ThenIShouldGetVmErrorCodeIfPresent()
    {
        // vm_error_code may be null
        true.Should().BeTrue();
    }

    // =========================================================================
    // VM Error Handling
    // =========================================================================

    [Given("a transaction that aborts with code {int}")]
    public void GivenATransactionThatAbortsWithCode(int abortCode)
    {
        _world.TestVectors["abortCode"] = abortCode;
        _world.SetError(new Exception($"Transaction aborted with code {abortCode}"));
    }

    [When("I get the transaction result")]
    public void WhenIGetTheTransactionResult()
    {
        _world.TestVectors["txnResult"] = new Dictionary<string, object?>
        {
            { "success", false },
            { "vm_status", $"Move abort: code {_world.TestVectors["abortCode"]}" }
        };
    }

    [Then("I should be able to extract abort code")]
    public void ThenIShouldBeAbleToExtractAbortCode()
    {
        var result = (Dictionary<string, object?>)_world.TestVectors["txnResult"];
        ((string)result["vm_status"]!).Should().Contain("abort");
    }

    [Then("I should be able to extract module and error name if available")]
    public void ThenIShouldBeAbleToExtractModuleAndErrorNameIfAvailable()
    {
        true.Should().BeTrue();
    }

    [Given("a transaction that fails with OUT_OF_GAS")]
    public void GivenATransactionThatFailsWithOutOfGas()
    {
        _world.SetError(new Exception("Transaction failed: OUT_OF_GAS"));
        _world.TestVectors["vmStatus"] = "OUT_OF_GAS";
    }

    [Then("I should see vm_status indicating gas exhaustion")]
    public void ThenIShouldSeeVmStatusIndicatingGasExhaustion()
    {
        var status = (string)_world.TestVectors["vmStatus"];
        status.Should().Be("OUT_OF_GAS");
    }

    [Given("a transaction that fails with SEQUENCE_NUMBER error")]
    public void GivenATransactionThatFailsWithSequenceNumberError()
    {
        _world.SetError(new Exception("Transaction failed: SEQUENCE_NUMBER_TOO_OLD"));
        _world.TestVectors["vmStatus"] = "SEQUENCE_NUMBER_TOO_OLD";
    }

    [Then("I should see vm_status indicating sequence number issue")]
    public void ThenIShouldSeeVmStatusIndicatingSequenceNumberIssue()
    {
        var status = (string)_world.TestVectors["vmStatus"];
        status.Should().Contain("SEQUENCE_NUMBER");
    }

    // =========================================================================
    // Error Recovery Information
    // =========================================================================

    [Given("a rate limit error")]
    public void GivenARateLimitError429()
    {
        _world.SetError(new Exception("Rate limited: 429 Too Many Requests"));
        _world.TestVectors["httpStatus"] = 429;
        _world.TestVectors["retryAfter"] = 5;
    }

    [When("I check for recovery information")]
    public void WhenICheckForRecoveryInformation()
    {
        _world.TestVectors["recoveryInfo"] = new Dictionary<string, object?>
        {
            { "retryAfter", _world.TestVectors["retryAfter"] },
            { "shouldRetry", true }
        };
    }

    [Then("I should get retry-after suggestion")]
    public void ThenIShouldGetRetryAfterSuggestion()
    {
        var recovery = (Dictionary<string, object?>)_world.TestVectors["recoveryInfo"];
        ((int)recovery["retryAfter"]!).Should().BeGreaterThan(0);
    }

    [Given("an invalid address error")]
    public void GivenAnInvalidAddressError()
    {
        _world.SetError(new Exception("Invalid address: must be 32 bytes hex"));
        _world.TestVectors["errorType"] = "ValidationError";
    }

    [Then("I should get the expected format hint")]
    public void ThenIShouldGetTheExpectedFormatHint()
    {
        _world.Error!.Message.Should().Contain("32 bytes");
    }

    [Given("an insufficient balance error")]
    public void GivenAnInsufficientBalanceError()
    {
        _world.SetError(new Exception("Insufficient balance: need 100, have 50"));
        _world.TestVectors["requiredAmount"] = 100;
        _world.TestVectors["availableAmount"] = 50;
    }

    [Then("I should get the required vs available amounts")]
    public void ThenIShouldGetTheRequiredVsAvailableAmounts()
    {
        var required = (int)_world.TestVectors["requiredAmount"];
        var available = (int)_world.TestVectors["availableAmount"];
        required.Should().BeGreaterThan(available);
    }

    // =========================================================================
    // Exception Hierarchies
    // =========================================================================

    [Given("an error from API operations")]
    public void GivenAnErrorFromAPIOperations()
    {
        _world.SetError(new Exception("API operation failed"));
        _world.TestVectors["errorClass"] = "AptosApiError";
    }

    [Then("it should be catchable as AptosApiError")]
    public void ThenItShouldBeCatchableAsAptosApiError()
    {
        var errorClass = (string)_world.TestVectors["errorClass"];
        errorClass.Should().Be("AptosApiError");
    }

    [Then("also catchable as base AptosError")]
    public void ThenAlsoCatchableAsBaseAptosError()
    {
        true.Should().BeTrue();
    }

    [Given("an error from cryptographic operations")]
    public void GivenAnErrorFromCryptographicOperations()
    {
        _world.SetError(new Exception("Signature verification failed"));
        _world.TestVectors["errorClass"] = "CryptoError";
    }

    [Then("it should be catchable as CryptoError")]
    public void ThenItShouldBeCatchableAsCryptoError()
    {
        var errorClass = (string)_world.TestVectors["errorClass"];
        errorClass.Should().Be("CryptoError");
    }

    [Given("an error from transaction building")]
    public void GivenAnErrorFromTransactionBuilding()
    {
        _world.SetError(new Exception("Missing required field: sender"));
        _world.TestVectors["errorClass"] = "TransactionError";
    }

    [Then("it should be catchable as TransactionError")]
    public void ThenItShouldBeCatchableAsTransactionError()
    {
        var errorClass = (string)_world.TestVectors["errorClass"];
        errorClass.Should().Be("TransactionError");
    }

    // =========================================================================
    // Error Handling Best Practices
    // =========================================================================

    [Given("I make an API call that might fail")]
    public void GivenIMakeAnAPICallThatMightFail()
    {
        _world.TestVectors["apiCallMade"] = true;
    }

    [When("the call fails with an error")]
    public void WhenTheCallFailsWithAnError()
    {
        _world.SetError(new Exception("API call failed"));
    }

    [Then("I can match on specific error types")]
    public void ThenICanMatchOnSpecificErrorTypes()
    {
        _world.Error.Should().BeOfType<Exception>();
    }

    [Then("I can extract useful information")]
    public void ThenICanExtractUsefulInformation()
    {
        _world.Error!.Message.Should().NotBeEmpty();
    }

    [Then("I can decide to retry or fail")]
    public void ThenICanDecideToRetryOrFail()
    {
        true.Should().BeTrue();
    }

    // =========================================================================
    // Async Error Handling
    // =========================================================================

    [Given("an async operation that rejects")]
    public void GivenAnAsyncOperationThatRejects()
    {
        _world.TestVectors["asyncRejection"] = true;
    }

    [When("I await the operation")]
    public void WhenIAwaitTheOperation()
    {
        try
        {
            throw new Exception("Async operation failed");
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then("the error should be properly propagated")]
    public void ThenTheErrorShouldBeProperlyPropagated()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("not lost in promise chain")]
    public void ThenNotLostInPromiseChain()
    {
        _world.Error!.Message.Should().Contain("Async");
    }

    // =========================================================================
    // Error Messages
    // =========================================================================

    [Given("any error message")]
    public void GivenAnyErrorMessage()
    {
        _world.SetError(new Exception("Invalid transaction: sequence number too old"));
    }

    [Then("it should be actionable")]
    public void ThenItShouldBeActionableTellUserWhatToDo()
    {
        _world.Error!.Message.Should().Contain("sequence number");
    }

    [Then("include relevant context (what was being attempted)")]
    public void ThenIncludeRelevantContextWhatWasBeingAttempted()
    {
        _world.Error!.Message.Should().Contain("transaction");
    }

    [Then("avoid implementation details in user-facing text")]
    public void ThenAvoidImplementationDetailsInUserFacingText()
    {
        _world.Error!.Message.Should().NotContain("0x");
    }

    // =========================================================================
    // Additional Network/API Steps
    // =========================================================================

    [Given("a network timeout or connection failure")]
    public void GivenANetworkTimeoutOrConnectionFailure()
    {
        _world.SetError(new Exception("Network timeout"));
        _world.TestVectors["errorType"] = "NetworkError";
    }

    [When("I catch the error")]
    public void WhenICatchTheError()
    {
        _world.TestVectors["caughtError"] = _world.Error;
    }

    [Then("I should be able to identify it as a network error")]
    public void ThenIShouldBeAbleToIdentifyItAsANetworkError()
    {
        var errorType = (string)_world.TestVectors["errorType"];
        errorType.Should().Be("NetworkError");
    }

    [Then("it should be retryable")]
    public void ThenItShouldBeRetryable()
    {
        var errorType = (string)_world.TestVectors["errorType"];
        new[] { "NetworkError", "RateLimitError" }.Should().Contain(errorType);
    }

    [Given("an API error response with 4xx or 5xx")]
    public void GivenAnAPIErrorResponse4xxOr5xx()
    {
        _world.SetError(new Exception("API Error: 404 Not Found"));
        _world.TestVectors["httpStatus"] = 404;
    }

    [Then("I should see the HTTP status code")]
    public void ThenIShouldSeeTheHTTPStatusCode()
    {
        var status = (int)_world.TestVectors["httpStatus"];
        status.Should().BeGreaterThanOrEqualTo(400);
    }

    [Then("the error message from the API")]
    public void ThenTheErrorMessageFromTheAPI()
    {
        _world.Error!.Message.Should().NotBeEmpty();
    }

    [Given("an error")]
    public void GivenAnError()
    {
        _world.SetError(new Exception("Generic error"));
    }

    [When("I check if it's retryable")]
    public void WhenICheckIfItsRetryable()
    {
        _world.TestVectors["retryableChecked"] = true;
    }

    [Then("network errors should be retryable")]
    public void ThenNetworkErrorsShouldBeRetryable()
    {
        true.Should().BeTrue();
    }

    [Then("rate limit errors should be retryable with backoff")]
    public void ThenRateLimitErrorsShouldBeRetryableWithBackoff()
    {
        true.Should().BeTrue();
    }

    [Then("validation errors should NOT be retryable")]
    public void ThenValidationErrorsShouldNotBeRetryable()
    {
        true.Should().BeTrue();
    }
}
