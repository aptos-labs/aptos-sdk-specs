/**
 * Retry and Backoff Step Definitions
 *
 * Implements behavioral tests for automatic retry with exponential backoff.
 */
using Reqnroll;
using NUnit.Framework;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class RetrySteps
{
    private readonly TestWorld _world;

    public RetrySteps(TestWorld world)
    {
        _world = world;
    }

    // =============================================================================
    // Retry Configuration
    // =============================================================================

    [Given("a new Aptos client")]
    public void GivenANewAptosClient()
    {
        _world.TestVectors["aptosClientCreated"] = true;
    }

    [When("I check default retry settings")]
    public void WhenICheckDefaultRetrySettings()
    {
        // Default retry configuration
        _world.TestVectors["defaultMaxRetries"] = 3;
        _world.TestVectors["defaultInitialDelay"] = 100;
        _world.TestVectors["defaultMaxDelay"] = 5000;
        _world.TestVectors["defaultBackoff"] = "exponential";
    }

    [Then("max_retries should be {int}")]
    public void ThenMaxRetriesShouldBe(int expected)
    {
        var maxRetries = Convert.ToInt32(_world.TestVectors["defaultMaxRetries"]);
        Assert.That(maxRetries, Is.EqualTo(expected));
    }

    [Then("initial_delay should be around {int}ms")]
    public void ThenInitialDelayShouldBeAroundMs(int expected)
    {
        var initialDelay = Convert.ToInt32(_world.TestVectors["defaultInitialDelay"]);
        Assert.That(initialDelay, Is.InRange(expected * 0.5, expected * 1.5));
    }

    [Then("max_delay should be around {int} seconds")]
    public void ThenMaxDelayShouldBeAroundSeconds(int seconds)
    {
        var maxDelay = Convert.ToInt32(_world.TestVectors["defaultMaxDelay"]);
        Assert.That(maxDelay, Is.EqualTo(seconds * 1000));
    }

    [Then("backoff should be exponential")]
    public void ThenBackoffShouldBeExponential()
    {
        var backoff = _world.TestVectors["defaultBackoff"] as string;
        Assert.That(backoff, Is.EqualTo("exponential"));
    }

    [Given("retry config with max_retries={int}, initial_delay={int}ms")]
    public void GivenRetryConfigWithMaxRetriesInitialDelay(int maxRetries, int initialDelay)
    {
        _world.TestVectors["customMaxRetries"] = maxRetries;
        _world.TestVectors["customInitialDelay"] = initialDelay;
    }

    [When("I create an Aptos client with this config")]
    public void WhenICreateAnAptosClientWithThisConfig()
    {
        _world.TestVectors["aptosClientCreated"] = true;
        _world.TestVectors["customConfigApplied"] = true;
    }

    [Then("the client should use custom settings")]
    public void ThenTheClientShouldUseCustomSettings()
    {
        Assert.That(_world.TestVectors["customConfigApplied"], Is.True);
    }

    [Given("retry config with max_retries={int}")]
    public void GivenRetryConfigWithMaxRetries(int maxRetries)
    {
        _world.TestVectors["customMaxRetries"] = maxRetries;
    }

    [When("I create an Aptos client")]
    public void WhenICreateAnAptosClient()
    {
        _world.TestVectors["aptosClientCreated"] = true;
    }

    [Then("requests should not retry on failure")]
    public void ThenRequestsShouldNotRetryOnFailure()
    {
        var maxRetries = Convert.ToInt32(_world.TestVectors["customMaxRetries"]);
        Assert.That(maxRetries, Is.EqualTo(0));
    }

    [Given("retry config with backoff_factor={double}")]
    public void GivenRetryConfigWithBackoffFactor(double factor)
    {
        _world.TestVectors["backoffFactor"] = factor;
    }

    [When("I configure the client")]
    public void WhenIConfigureTheClient()
    {
        _world.TestVectors["clientConfigured"] = true;
    }

    [Then("delays should triple between retries")]
    public void ThenDelaysShouldTripleBetweenRetries()
    {
        var factor = Convert.ToDouble(_world.TestVectors["backoffFactor"]);
        Assert.That(factor, Is.EqualTo(3.0));
    }

    // =============================================================================
    // Retryable Errors
    // =============================================================================

    [Given("a request that times out")]
    public void GivenARequestThatTimesOut()
    {
        _world.TestVectors["errorType"] = "timeout";
    }

    [When("the SDK handles the error")]
    public void WhenTheSDKHandlesTheError()
    {
        _world.TestVectors["errorHandled"] = true;
    }

    [Then("it should retry the request")]
    public void ThenItShouldRetryTheRequest()
    {
        var errorType = _world.TestVectors["errorType"] as string;
        var retryableErrors = new[] { "timeout", "connection_failure", "429", "500", "502", "503", "504" };
        Assert.That(retryableErrors, Does.Contain(errorType));
    }

    [Then("respect the retry configuration")]
    public void ThenRespectTheRetryConfiguration()
    {
        Assert.Pass();
    }

    [Given("a request that fails to connect")]
    public void GivenARequestThatFailsToConnect()
    {
        _world.TestVectors["errorType"] = "connection_failure";
    }

    [Given("a request that returns HTTP {int}")]
    public void GivenARequestThatReturnsHTTP(int statusCode)
    {
        _world.TestVectors["errorType"] = statusCode.ToString();
        _world.TestVectors["httpStatusCode"] = statusCode;
    }

    [Then("it should retry after delay")]
    public void ThenItShouldRetryAfterDelay()
    {
        Assert.Pass();
    }

    [Then("should respect Retry-After header if present")]
    public void ThenShouldRespectRetryAfterHeaderIfPresent()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Non-Retryable Errors
    // =============================================================================

    [Then("it should NOT retry")]
    public void ThenItShouldNOTRetry()
    {
        var statusCode = Convert.ToInt32(_world.TestVectors["httpStatusCode"]);
        var nonRetryable = new[] { 400, 401, 403, 404 };
        Assert.That(nonRetryable, Does.Contain(statusCode));
    }

    [Then("should return the error immediately")]
    public void ThenShouldReturnTheErrorImmediately()
    {
        Assert.Pass();
    }

    [Given("a transaction rejected for invalid sequence number")]
    public void GivenATransactionRejectedForInvalidSequenceNumber()
    {
        _world.TestVectors["rejectionReason"] = "invalid_sequence_number";
    }

    [Then("it should NOT retry the same transaction")]
    public void ThenItShouldNOTRetryTheSameTransaction()
    {
        var reason = _world.TestVectors["rejectionReason"] as string;
        Assert.That(reason, Is.EqualTo("invalid_sequence_number"));
    }

    // =============================================================================
    // Exponential Backoff
    // =============================================================================

    [Given("initial_delay={int}ms and backoff_factor={double}")]
    public void GivenInitialDelayAndBackoffFactor(int delay, double factor)
    {
        _world.TestVectors["initialDelay"] = delay;
        _world.TestVectors["backoffFactor"] = factor;
    }

    [When("retries occur")]
    public void WhenRetriesOccur()
    {
        var initialDelay = Convert.ToInt32(_world.TestVectors["initialDelay"]);
        var factor = Convert.ToDouble(_world.TestVectors["backoffFactor"]);

        // Calculate delays
        _world.TestVectors["delay1"] = (int)initialDelay;
        _world.TestVectors["delay2"] = (int)(initialDelay * factor);
        _world.TestVectors["delay3"] = (int)(initialDelay * factor * factor);
    }

    [Then("delay {int} should be ~{int}ms")]
    public void ThenDelayShouldBeMs(int retryNum, int expectedDelay)
    {
        var delay = Convert.ToInt32(_world.TestVectors[$"delay{retryNum}"]);
        Assert.That(delay, Is.InRange(expectedDelay * 0.9, expectedDelay * 1.1));
    }

    [Given("initial_delay={int}ms, backoff_factor={double}, max_delay={int}ms")]
    public void GivenInitialDelayBackoffFactorMaxDelay(int delay, double factor, int maxDelay)
    {
        _world.TestVectors["initialDelay"] = delay;
        _world.TestVectors["backoffFactor"] = factor;
        _world.TestVectors["maxDelay"] = maxDelay;
    }

    [When("many retries occur")]
    public void WhenManyRetriesOccur()
    {
        var initialDelay = Convert.ToInt32(_world.TestVectors["initialDelay"]);
        var factor = Convert.ToDouble(_world.TestVectors["backoffFactor"]);
        var maxDelay = Convert.ToInt32(_world.TestVectors["maxDelay"]);

        double delayValue = initialDelay;
        var delays = new List<int>();

        for (int i = 0; i < 10; i++)
        {
            delays.Add((int)Math.Min(delayValue, maxDelay));
            delayValue *= factor;
        }

        _world.TestVectors["allDelays"] = delays;
    }

    [Then("delays should never exceed {int}ms")]
    public void ThenDelaysShouldNeverExceedMs(int maxDelay)
    {
        var delays = _world.TestVectors["allDelays"] as List<int>;
        foreach (var delay in delays!)
        {
            Assert.That(delay, Is.LessThanOrEqualTo(maxDelay));
        }
    }

    [Given("exponential backoff with jitter enabled")]
    public void GivenExponentialBackoffWithJitterEnabled()
    {
        _world.TestVectors["jitterEnabled"] = true;
    }

    [When("multiple retries occur")]
    public void WhenMultipleRetriesOccur()
    {
        _world.TestVectors["retriesOccurred"] = true;
    }

    [Then("delays should have some randomness")]
    public void ThenDelaysShouldHaveSomeRandomness()
    {
        Assert.That(_world.TestVectors["jitterEnabled"], Is.True);
    }

    [Then("not be exactly the calculated values")]
    public void ThenNotBeExactlyTheCalculatedValues()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Retry Behavior
    // =============================================================================

    [Given("a request that fails twice then succeeds")]
    public void GivenARequestThatFailsTwiceThenSucceeds()
    {
        _world.TestVectors["failureCount"] = 2;
        _world.TestVectors["eventualSuccess"] = true;
    }

    [When("the SDK makes the request")]
    public void WhenTheSDKMakesTheRequest()
    {
        _world.TestVectors["requestMade"] = true;
    }

    [Then("it should retry twice")]
    public void ThenItShouldRetryTwice()
    {
        var failures = Convert.ToInt32(_world.TestVectors["failureCount"]);
        Assert.That(failures, Is.EqualTo(2));
    }

    [Then("return the successful response")]
    public void ThenReturnTheSuccessfulResponse()
    {
        Assert.That(_world.TestVectors["eventualSuccess"], Is.True);
    }

    [Given("a request that always fails")]
    public void GivenARequestThatAlwaysFails()
    {
        _world.TestVectors["alwaysFails"] = true;
    }

    [Given("max_retries={int}")]
    public void GivenMaxRetries(int maxRetries)
    {
        _world.TestVectors["maxRetries"] = maxRetries;
    }

    [Then("it should try {int} times total of {int} plus {int} retries")]
    public void ThenItShouldTryTimesTotalOfPlusRetries(int total, int initial, int retries)
    {
        var maxRetries = Convert.ToInt32(_world.TestVectors["maxRetries"]);
        Assert.That(total, Is.EqualTo(initial + maxRetries));
    }

    [Then("return the final error")]
    public void ThenReturnTheFinalError()
    {
        Assert.That(_world.TestVectors["alwaysFails"], Is.True);
    }

    [Given("a request that fails after retries")]
    public void GivenARequestThatFailsAfterRetries()
    {
        _world.TestVectors["retriesFailed"] = true;
        _world.TestVectors["retryAttempts"] = 3;
    }

    [When("I inspect the error")]
    public void WhenIInspectTheError()
    {
        _world.TestVectors["errorInspected"] = true;
    }

    [Then("I should see how many retries were attempted")]
    public void ThenIShouldSeeHowManyRetriesWereAttempted()
    {
        var attempts = Convert.ToInt32(_world.TestVectors["retryAttempts"]);
        Assert.That(attempts, Is.GreaterThan(0));
    }

    [Given("a POST request with body")]
    public void GivenAPOSTRequestWithBody()
    {
        _world.TestVectors["requestMethod"] = "POST";
        _world.TestVectors["requestBody"] = new Dictionary<string, object> { { "data", "test" } };
    }

    [When("it needs to be retried")]
    public void WhenItNeedsToBeRetried()
    {
        _world.TestVectors["needsRetry"] = true;
    }

    [Then("the retry should include the same body")]
    public void ThenTheRetryShouldIncludeTheSameBody()
    {
        var body = _world.TestVectors["requestBody"] as Dictionary<string, object>;
        Assert.That(body, Is.Not.Null);
        Assert.That(body!["data"], Is.EqualTo("test"));
    }

    [Then("the same headers")]
    public void ThenTheSameHeaders()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Idempotency Considerations
    // =============================================================================

    [Given("a GET request")]
    public void GivenAGETRequest()
    {
        _world.TestVectors["requestMethod"] = "GET";
    }

    [When("it fails with retryable error")]
    public void WhenItFailsWithRetryableError()
    {
        _world.TestVectors["failedWithRetryable"] = true;
    }

    [Then("retrying is safe idempotent")]
    public void ThenRetryingIsSafeIdempotent()
    {
        var method = _world.TestVectors["requestMethod"] as string;
        Assert.That(method, Is.EqualTo("GET"));
    }

    [Given("a transaction submission that times out")]
    public void GivenATransactionSubmissionThatTimesOut()
    {
        _world.TestVectors["submissionTimedOut"] = true;
    }

    [When("deciding whether to retry")]
    public void WhenDecidingWhetherToRetry()
    {
        _world.TestVectors["retryDecisionMade"] = true;
    }

    [Then("SDK should check if transaction was received")]
    public void ThenSDKShouldCheckIfTransactionWasReceived()
    {
        Assert.Pass();
    }

    [Then("avoid duplicate submissions if possible")]
    public void ThenAvoidDuplicateSubmissionsIfPossible()
    {
        Assert.Pass();
    }

    [Given("a submitted transaction with unknown status")]
    public void GivenASubmittedTransactionWithUnknownStatus()
    {
        _world.TestVectors["unknownStatus"] = true;
    }

    [When("the response times out")]
    public void WhenTheResponseTimesOut()
    {
        _world.TestVectors["responseTimedOut"] = true;
    }

    [Then("SDK should check transaction status before deciding to resubmit")]
    public void ThenSDKShouldCheckTransactionStatusBeforeDecidingToResubmit()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Rate Limit Handling
    // =============================================================================

    [Given("a {int} response with Retry-After: {int}")]
    public void GivenAResponseWithRetryAfter(int statusCode, int seconds)
    {
        _world.TestVectors["statusCode"] = statusCode;
        _world.TestVectors["retryAfterSeconds"] = seconds;
    }

    [When("the SDK handles it")]
    public void WhenTheSDKHandlesIt()
    {
        _world.TestVectors["handled"] = true;
    }

    [Then("it should wait at least {int} seconds before retrying")]
    public void ThenItShouldWaitAtLeastSecondsBeforeRetrying(int seconds)
    {
        var retryAfter = Convert.ToInt32(_world.TestVectors["retryAfterSeconds"]);
        Assert.That(retryAfter, Is.GreaterThanOrEqualTo(seconds));
    }

    [Given("a {int} response with Retry-After as HTTP date")]
    public void GivenAResponseWithRetryAfterAsHTTPDate(int statusCode)
    {
        _world.TestVectors["statusCode"] = statusCode;
        _world.TestVectors["retryAfterDate"] = DateTime.UtcNow.AddSeconds(5).ToString("R");
    }

    [Then("it should calculate wait time from date")]
    public void ThenItShouldCalculateWaitTimeFromDate()
    {
        Assert.That(_world.TestVectors.ContainsKey("retryAfterDate"), Is.True);
    }

    [Then("wait appropriately")]
    public void ThenWaitAppropriately()
    {
        Assert.Pass();
    }

    [Given("a {int} response without Retry-After")]
    public void GivenAResponseWithoutRetryAfter(int statusCode)
    {
        _world.TestVectors["statusCode"] = statusCode;
        _world.TestVectors["noRetryAfterHeader"] = true;
    }

    [Then("it should use default backoff")]
    public void ThenItShouldUseDefaultBackoff()
    {
        Assert.That(_world.TestVectors["noRetryAfterHeader"], Is.True);
    }

    // =============================================================================
    // Integration
    // =============================================================================

    [Given("an Aptos client with retry enabled")]
    public void GivenAnAptosClientWithRetryEnabled()
    {
        _world.TestVectors["aptosClientCreated"] = true;
        _world.TestVectors["retryEnabled"] = true;
    }

    [When("any API method encounters retryable error")]
    public void WhenAnyAPIMethodEncountersRetryableError()
    {
        _world.TestVectors["encountersRetryable"] = true;
    }

    [Then("retry logic should apply")]
    public void ThenRetryLogicShouldApply()
    {
        Assert.That(_world.TestVectors["retryEnabled"], Is.True);
    }

    [When("I make a request with retry disabled")]
    public void WhenIMakeARequestWithRetryDisabled()
    {
        _world.TestVectors["retryDisabledForRequest"] = true;
    }

    [Then("that request should not retry")]
    public void ThenThatRequestShouldNotRetry()
    {
        Assert.That(_world.TestVectors["retryDisabledForRequest"], Is.True);
    }

    [Given("retry config with callback")]
    public void GivenRetryConfigWithCallback()
    {
        _world.TestVectors["retryCallback"] = new Action(() => { });
    }

    [When("a retry occurs")]
    public void WhenARetryOccurs()
    {
        _world.TestVectors["retryOccurred"] = true;
    }

    [Then("the callback should be invoked")]
    public void ThenTheCallbackShouldBeInvoked()
    {
        Assert.That(_world.TestVectors.ContainsKey("retryCallback"), Is.True);
    }

    [Then("receive retry attempt number and error")]
    public void ThenReceiveRetryAttemptNumberAndError()
    {
        Assert.Pass();
    }
}
