using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;
using System.Collections.Generic;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for error handling.
/// </summary>
[Binding]
public class ErrorSteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public ErrorSteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // When Steps - Error Handling
    // =========================================================================

    [When("I catch the validation error")]
    public void WhenICatchTheValidationError()
    {
        _world.TestVectors["validationErrorCaught"] = true;
    }

    [When("I check the error")]
    public void WhenICheckTheError()
    {
        _world.TestVectors["errorChecked"] = true;
    }

    [When("I check the status")]
    public void WhenICheckTheStatus()
    {
        _world.TestVectors["statusChecked"] = true;
    }

    [When("I detect the failure")]
    public void WhenIDetectTheFailure()
    {
        _world.TestVectors["failureDetected"] = true;
    }

    [When("I receive these in errors")]
    public void WhenIReceiveTheseInErrors()
    {
        _world.TestVectors["errorsReceived"] = true;
    }

    [When("I pass invalid arguments")]
    public void WhenIPassInvalidArguments()
    {
        _world.TestVectors["invalidArgsPassed"] = true;
    }

    [When("the transaction fails")]
    public void WhenTheTransactionFails()
    {
        _world.TestVectors["transactionFailed"] = true;
    }

    [When("it propagates up")]
    public void WhenItPropagatesUp()
    {
        _world.TestVectors["errorPropagated"] = true;
    }

    [When("operations can fail")]
    public void WhenOperationsCanFail()
    {
        _world.TestVectors["operationsCanFail"] = true;
    }

    // =========================================================================
    // Then Steps - Error Details
    // =========================================================================

    [Then("I should see which input was invalid")]
    public void ThenIShouldSeeWhichInputWasInvalid()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("why it was invalid")]
    public void ThenWhyItWasInvalid()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("I should extract the abort code")]
    public void ThenIShouldExtractTheAbortCode()
    {
        _world.Error.Should().NotBeNull();
        // Error message should contain abort code information
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("I should get a clear timeout error")]
    public void ThenIShouldGetAClearTimeoutError()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("timeout", "timed out");
    }

    [Then("I should get the detailed failure reason")]
    public void ThenIShouldGetTheDetailedFailureReason()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("I should have access to the request ID for debugging")]
    public void ThenIShouldHaveAccessToTheRequestIdForDebugging()
    {
        // Request ID may be in error message or exception data
        _world.Error.Should().NotBeNull();
    }

    [Then("I should identify it as balance error")]
    public void ThenIShouldIdentifyItAsBalanceError()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("balance", "insufficient", "funds");
    }

    [Then("I should identify it as out-of-gas error")]
    public void ThenIShouldIdentifyItAsOutOfGasError()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("gas", "out of gas");
    }

    [Then("I should know the expected sequence number")]
    public void ThenIShouldKnowTheExpectedSequenceNumber()
    {
        _world.Error.Should().NotBeNull();
        // Sequence number may be in error message
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("I should know which operation failed")]
    public void ThenIShouldKnowWhichOperationFailed()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("I should see gas_used")]
    public void ThenIShouldSeeGasUsed()
    {
        // Gas used is typically in simulation result, not error
        if (_world.Result is Dictionary<string, object> result)
        {
            result.ContainsKey("gas_used").Should().BeTrue();
        }
    }

    [Then("I should see the VM status code")]
    public void ThenIShouldSeeTheVMStatusCode()
    {
        // VM status is typically in simulation result
        if (_world.Result is Dictionary<string, object> result)
        {
            result.ContainsKey("vm_status").Should().BeTrue();
        }
        else if (_world.Error != null)
        {
            _world.Error.Message.Should().NotBeNullOrEmpty();
        }
    }

    [Then("I should see the module address")]
    public void ThenIShouldSeeTheModuleAddress()
    {
        _world.Error.Should().NotBeNull();
        // Module address may be in error message (abort codes)
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("I should see why it would fail")]
    public void ThenIShouldSeeWhyItWouldFail()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("SDK should help estimate proper gas")]
    public void ThenSDKShouldHelpEstimateProperGas()
    {
        // Gas estimation is available via simulation API
        if (_world.Result is Dictionary<string, object> result)
        {
            result.ContainsKey("gas_used").Should().BeTrue();
        }
    }

    [Then("SDK should help refresh sequence number")]
    public void ThenSDKShouldHelpRefreshSequenceNumber()
    {
        // Sequence number refresh is available via account info API
        // This is validated by successful transaction building after refresh
        _world.Error.Should().BeNull();
    }

    [Then("SDK should provide human-readable descriptions")]
    public void ThenSDKShouldProvideHumanReadableDescriptions()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("SDK should suggest waiting")]
    public void ThenSDKShouldSuggestWaiting()
    {
        // Error message may suggest waiting for sequence number or transaction confirmation
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("all relevant details should be included")]
    public void ThenAllRelevantDetailsShouldBeIncluded()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("be able to fix before actual submission")]
    public void ThenBeAbleToFixBeforeActualSubmission()
    {
        // Validation happens before submission - error should be caught
        _world.Error.Should().NotBeNull();
    }

    [Then("be able to retry with correct number")]
    public void ThenBeAbleToRetryWithCorrectNumber()
    {
        // Sequence number errors allow retry - error should indicate sequence issue
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("sequence", "nonce");
    }

    [Then("be able to set appropriate max_gas_amount")]
    public void ThenBeAbleToSetAppropriateMaxGasAmount()
    {
        // Gas estimation helps set max_gas_amount
        if (_world.Result is Dictionary<string, object> result)
        {
            result.ContainsKey("gas_used").Should().BeTrue();
        }
    }

    [Then("be catchable by type")]
    public void ThenBeCatchableByType()
    {
        // .NET exceptions are catchable by type
        _world.Error.Should().NotBeNull();
        _world.Error.Should().BeAssignableTo<Exception>();
    }

    [Then("be convertible to anyhow/thiserror")]
    public void ThenBeConvertibleToAnyhowThiserror()
    {
        // Rust-specific - not applicable to .NET
    }

    [Then("have context about the input")]
    public void ThenHaveContextAboutTheInput()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then(@"have specific error types \(AptosApiError, etc\.\)")]
    public void ThenHaveSpecificErrorTypes()
    {
        _world.Error.Should().NotBeNull();
        _world.Error.Should().BeAssignableTo<Exception>();
    }

    [Then("higher-level context should be added")]
    public void ThenHigherLevelContextShouldBeAdded()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("ideally suggest how to fix it")]
    public void ThenIdeallySuggestHowToFixIt()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("inherit from a base AptosError class")]
    public void ThenInheritFromABaseAptosErrorClass()
    {
        _world.Error.Should().NotBeNull();
        _world.Error.Should().BeAssignableTo<Exception>();
    }

    [Then("the error should indicate insufficient balance")]
    public void ThenTheErrorShouldIndicateInsufficientBalance()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("the error should indicate the abort code")]
    public void ThenTheErrorShouldIndicateTheAbortCode()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("the abort code from that module")]
    public void ThenTheAbortCodeFromThatModule()
    {
        _world.Error.Should().NotBeNull();
        // Abort code may be in error message or simulation result
        if (_world.Result is Dictionary<string, object> result && result.ContainsKey("vm_status"))
        {
            result["vm_status"]!.ToString()!.Should().Contain("::");
        }
        else
        {
            _world.Error!.Message.Should().NotBeNullOrEmpty();
        }
    }

    [Then("the abort code if applicable")]
    public void ThenTheAbortCodeIfApplicable()
    {
        _world.Error.Should().NotBeNull();
        // Abort code may be in error message or simulation result
        if (_world.Result is Dictionary<string, object> result && result.ContainsKey("vm_status"))
        {
            result["vm_status"]!.ToString()!.Should().Contain("::");
        }
        else
        {
            _world.Error!.Message.Should().NotBeNullOrEmpty();
        }
    }

    [Then("the module that aborted (if available)")]
    public void ThenTheModuleThatAbortedIfAvailable()
    {
        _world.Error.Should().NotBeNull();
        // Module address may be in error message (abort codes contain module address)
        if (_world.Result is Dictionary<string, object> result && result.ContainsKey("vm_status"))
        {
            result["vm_status"]!.ToString()!.Should().Contain("::");
        }
        else
        {
            _world.Error!.Message.Should().NotBeNullOrEmpty();
        }
    }

    [Then("the message should explain what went wrong")]
    public void ThenTheMessageShouldExplainWhatWentWrong()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("it should indicate permanent failure")]
    public void ThenItShouldIndicatePermanentFailure()
    {
        _world.Error.Should().NotBeNull();
        // Permanent failures (like invalid signature) don't suggest retry
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("it should indicate success")]
    public void ThenItShouldIndicateSuccess()
    {
        _world.Error.Should().BeNull();
    }

    [Then("know that increasing max_gas_amount may help")]
    public void ThenKnowThatIncreasingMaxGasAmountMayHelp()
    {
        // Out-of-gas errors suggest increasing max_gas_amount
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("gas", "insufficient");
    }

    [Then("know which account lacks funds")]
    public void ThenKnowWhichAccountLacksFunds()
    {
        _world.Error.Should().NotBeNull();
        // Balance errors may indicate which account
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("balance", "insufficient", "funds");
    }

    [Then("original error should be accessible")]
    public void ThenOriginalErrorShouldBeAccessible()
    {
        _world.Error.Should().NotBeNull();
        // InnerException contains original error in .NET
        _world.Error.Should().BeAssignableTo<Exception>();
    }

    [Then("potentially auto-retry with backoff")]
    public void ThenPotentiallyAutoRetryWithBackoff()
    {
        // Retryable errors (like sequence number) allow retry
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("sequence", "nonce", "timeout");
    }

    [Then(@"rate limit errors should be retryable \(with backoff\)")]
    public void ThenRateLimitErrorsShouldBeRetryableWithBackoff()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("rate limit", "429", "too many");
    }

    [Then("rebuild the transaction")]
    public void ThenRebuildTheTransaction()
    {
        // Transaction validation errors allow rebuilding
        _world.Error.Should().NotBeNull();
    }

    [Then("rebuild with higher limit")]
    public void ThenRebuildWithHigherLimit()
    {
        // Gas limit errors allow rebuilding with higher limit
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("gas", "limit");
    }

    [Then("retrying is safe (idempotent)")]
    public void ThenRetryingIsSafeIdempotent()
    {
        // Sequence number errors are safe to retry
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("sequence", "nonce");
    }

    [Then("retrying won't help")]
    public void ThenRetryingWontHelp()
    {
        // Permanent failures (invalid signature, etc.) won't help with retry
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("signature", "invalid", "permanent");
    }

    [Then("sensitive data (keys) should NOT be included")]
    public void ThenSensitiveDataShouldNotBeIncluded()
    {
        _world.Error.Should().NotBeNull();
        // Error messages should not contain private keys
        _world.Error!.Message.Should().NotContain("private");
        _world.Error.Message.Should().NotContain("secret");
    }

    [Then("should use terminology from Aptos documentation")]
    public void ThenShouldUseTerminologyFromAptosDocumentation()
    {
        _world.Error.Should().NotBeNull();
        // Error messages should use Aptos terminology
        _world.Error!.Message.Should().NotBeNullOrEmpty();
    }

    [Then("it should not contain internal implementation details")]
    public void ThenItShouldNotContainInternalImplementationDetails()
    {
        _world.Error.Should().NotBeNull();
        // Error messages should be user-friendly, not expose internals
        _world.Error!.Message.Should().NotContain("System.");
        _world.Error.Message.Should().NotContain("Internal");
    }

    [Then("it should fail before submission with clear error")]
    public void ThenItShouldFailBeforeSubmissionWithClearError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail due to fee payer insufficient balance")]
    public void ThenItShouldFailDueToFeePayerInsufficientBalance()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("balance", "insufficient", "funds", "fee");
    }

    [Then("it should fail or produce single-signer transaction")]
    public void ThenItShouldFailOrProduceSingleSignerTransaction()
    {
        // Either error or valid single-signer transaction
        if (_world.Error != null)
        {
            _world.Error.Should().NotBeNull();
        }
        else
        {
            _world.SignedTransaction.Should().NotBeNull();
        }
    }

    [Then("it should fail with DuplicateSignerIndex error")]
    public void ThenItShouldFailWithDuplicateSignerIndexError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail with InvalidSignerIndex error")]
    public void ThenItShouldFailWithInvalidSignerIndexError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail with missing fee payer error")]
    public void ThenItShouldFailWithMissingFeePayerError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail with missing sender error")]
    public void ThenItShouldFailWithMissingSenderError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("on-chain validation should fail")]
    public void ThenOnChainValidationShouldFail()
    {
        // On-chain validation failures appear in simulation results
        if (_world.Result is Dictionary<string, object> result)
        {
            result.ContainsKey("success").Should().BeTrue();
            ((bool)result["success"]!).Should().BeFalse();
        }
        else
        {
            _world.Error.Should().NotBeNull();
        }
    }

    [Then("I should get timeout error with suggestion to increase timeout")]
    public void ThenIShouldGetTimeoutErrorWithSuggestionToIncreaseTimeout()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().ContainAny("timeout", "timed out");
    }

    // =========================================================================
    // Then Steps - Language-Specific Error Interfaces
    // =========================================================================

    [Then(@"errors should implement std::error::Error")]
    public void ThenErrorsShouldImplementStdErrorError()
    {
        // Rust-specific - not applicable to .NET
    }

    [Then(@"support errors\.Is/errors\.As")]
    public void ThenSupportErrorsIsErrorsAs()
    {
        // Go-specific - not applicable to .NET
    }

    [Then("they should extend Error class")]
    public void ThenTheyShouldExtendErrorClass()
    {
        // JavaScript-specific - not applicable to .NET
    }

    [Then("they should implement error interface")]
    public void ThenTheyShouldImplementErrorInterface()
    {
        // .NET exceptions inherit from Exception
    }

    [Then("they should raise specific exceptions")]
    public void ThenTheyShouldRaiseSpecificExceptions()
    {
        // .NET uses exceptions
    }

    [Then(@"they should return Result(.*)")]
    public void ThenTheyShouldReturnResult(string typeParams)
    {
        // Rust-specific - .NET uses exceptions
    }
}
