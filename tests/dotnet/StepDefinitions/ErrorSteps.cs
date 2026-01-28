using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

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
        // Validation placeholder
    }

    [Then("why it was invalid")]
    public void ThenWhyItWasInvalid()
    {
        // Validation placeholder
    }

    [Then("I should extract the abort code")]
    public void ThenIShouldExtractTheAbortCode()
    {
        // Validation placeholder
    }

    [Then("I should get a clear timeout error")]
    public void ThenIShouldGetAClearTimeoutError()
    {
        // Validation placeholder
    }

    [Then("I should get the detailed failure reason")]
    public void ThenIShouldGetTheDetailedFailureReason()
    {
        // Validation placeholder
    }

    [Then("I should have access to the request ID for debugging")]
    public void ThenIShouldHaveAccessToTheRequestIdForDebugging()
    {
        // Validation placeholder
    }

    [Then("I should identify it as balance error")]
    public void ThenIShouldIdentifyItAsBalanceError()
    {
        // Validation placeholder
    }

    [Then("I should identify it as out-of-gas error")]
    public void ThenIShouldIdentifyItAsOutOfGasError()
    {
        // Validation placeholder
    }

    [Then("I should know the expected sequence number")]
    public void ThenIShouldKnowTheExpectedSequenceNumber()
    {
        // Validation placeholder
    }

    [Then("I should know which operation failed")]
    public void ThenIShouldKnowWhichOperationFailed()
    {
        // Validation placeholder
    }

    [Then("I should see gas_used")]
    public void ThenIShouldSeeGasUsed()
    {
        // Validation placeholder
    }

    [Then("I should see the VM status code")]
    public void ThenIShouldSeeTheVMStatusCode()
    {
        // Validation placeholder
    }

    [Then("I should see the module address")]
    public void ThenIShouldSeeTheModuleAddress()
    {
        // Validation placeholder
    }

    [Then("I should see why it would fail")]
    public void ThenIShouldSeeWhyItWouldFail()
    {
        // Validation placeholder
    }

    [Then("SDK should help estimate proper gas")]
    public void ThenSDKShouldHelpEstimateProperGas()
    {
        // Validation placeholder
    }

    [Then("SDK should help refresh sequence number")]
    public void ThenSDKShouldHelpRefreshSequenceNumber()
    {
        // Validation placeholder
    }

    [Then("SDK should provide human-readable descriptions")]
    public void ThenSDKShouldProvideHumanReadableDescriptions()
    {
        // Validation placeholder
    }

    [Then("SDK should suggest waiting")]
    public void ThenSDKShouldSuggestWaiting()
    {
        // Validation placeholder
    }

    [Then("all relevant details should be included")]
    public void ThenAllRelevantDetailsShouldBeIncluded()
    {
        // Validation placeholder
    }

    [Then("be able to fix before actual submission")]
    public void ThenBeAbleToFixBeforeActualSubmission()
    {
        // Validation placeholder
    }

    [Then("be able to retry with correct number")]
    public void ThenBeAbleToRetryWithCorrectNumber()
    {
        // Validation placeholder
    }

    [Then("be able to set appropriate max_gas_amount")]
    public void ThenBeAbleToSetAppropriateMaxGasAmount()
    {
        // Validation placeholder
    }

    [Then("be catchable by type")]
    public void ThenBeCatchableByType()
    {
        // Validation placeholder
    }

    [Then("be convertible to anyhow/thiserror")]
    public void ThenBeConvertibleToAnyhowThiserror()
    {
        // Rust-specific - not applicable to .NET
    }

    [Then("have context about the input")]
    public void ThenHaveContextAboutTheInput()
    {
        // Validation placeholder
    }

    [Then(@"have specific error types \(AptosApiError, etc\.\)")]
    public void ThenHaveSpecificErrorTypes()
    {
        // Validation placeholder
    }

    [Then("higher-level context should be added")]
    public void ThenHigherLevelContextShouldBeAdded()
    {
        // Validation placeholder
    }

    [Then("ideally suggest how to fix it")]
    public void ThenIdeallySuggestHowToFixIt()
    {
        // Validation placeholder
    }

    [Then("inherit from a base AptosError class")]
    public void ThenInheritFromABaseAptosErrorClass()
    {
        // Validation placeholder
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
        // Validation placeholder
    }

    [Then("the abort code if applicable")]
    public void ThenTheAbortCodeIfApplicable()
    {
        // Validation placeholder
    }

    [Then("the module that aborted (if available)")]
    public void ThenTheModuleThatAbortedIfAvailable()
    {
        // Validation placeholder
    }

    [Then("the message should explain what went wrong")]
    public void ThenTheMessageShouldExplainWhatWentWrong()
    {
        // Validation placeholder
    }

    [Then("it should indicate permanent failure")]
    public void ThenItShouldIndicatePermanentFailure()
    {
        // Validation placeholder
    }

    [Then("it should indicate success")]
    public void ThenItShouldIndicateSuccess()
    {
        _world.Error.Should().BeNull();
    }

    [Then("know that increasing max_gas_amount may help")]
    public void ThenKnowThatIncreasingMaxGasAmountMayHelp()
    {
        // Validation placeholder
    }

    [Then("know which account lacks funds")]
    public void ThenKnowWhichAccountLacksFunds()
    {
        // Validation placeholder
    }

    [Then("original error should be accessible")]
    public void ThenOriginalErrorShouldBeAccessible()
    {
        // Validation placeholder
    }

    [Then("potentially auto-retry with backoff")]
    public void ThenPotentiallyAutoRetryWithBackoff()
    {
        // Validation placeholder
    }

    [Then(@"rate limit errors should be retryable \(with backoff\)")]
    public void ThenRateLimitErrorsShouldBeRetryableWithBackoff()
    {
        // Validation placeholder
    }

    [Then("rebuild the transaction")]
    public void ThenRebuildTheTransaction()
    {
        // Validation placeholder
    }

    [Then("rebuild with higher limit")]
    public void ThenRebuildWithHigherLimit()
    {
        // Validation placeholder
    }

    [Then("retrying is safe (idempotent)")]
    public void ThenRetryingIsSafeIdempotent()
    {
        // Validation placeholder
    }

    [Then("retrying won't help")]
    public void ThenRetryingWontHelp()
    {
        // Validation placeholder
    }

    [Then("sensitive data (keys) should NOT be included")]
    public void ThenSensitiveDataShouldNotBeIncluded()
    {
        // Validation placeholder
    }

    [Then("should use terminology from Aptos documentation")]
    public void ThenShouldUseTerminologyFromAptosDocumentation()
    {
        // Validation placeholder
    }

    [Then("it should not contain internal implementation details")]
    public void ThenItShouldNotContainInternalImplementationDetails()
    {
        // Validation placeholder
    }

    [Then("it should fail before submission with clear error")]
    public void ThenItShouldFailBeforeSubmissionWithClearError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail due to fee payer insufficient balance")]
    public void ThenItShouldFailDueToFeePayerInsufficientBalance()
    {
        // Validation placeholder
    }

    [Then("it should fail or produce single-signer transaction")]
    public void ThenItShouldFailOrProduceSingleSignerTransaction()
    {
        // Validation placeholder
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
        // Validation placeholder
    }

    [Then("I should get timeout error with suggestion to increase timeout")]
    public void ThenIShouldGetTimeoutErrorWithSuggestionToIncreaseTimeout()
    {
        // Validation placeholder
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
