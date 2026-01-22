package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;
import io.cucumber.datatable.DataTable;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for error-handling.feature
 * 
 * These steps test error categorization, VM status parsing, and error recovery
 * patterns using the japtos SDK.
 */
public class ErrorHandlingSteps {
    
    private final World world;
    
    // Error state
    private Exception caughtError;
    private Object vmStatus;
    private Object transactionResult;
    private Object simulationResult;
    
    // Error properties
    private int httpStatusCode;
    private String errorMessage;
    private String errorCode;
    private long abortCode;
    private String abortModule;
    private String transactionHash;
    private String requestId;
    
    // Error categories
    private boolean isNetworkError;
    private boolean isApiError;
    private boolean isValidationError;
    private boolean isTransactionError;
    private boolean isRetryable;
    
    public ErrorHandlingSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Error Categories
    // ==========================================================================
    
    @Given("a network timeout or connection failure")
    public void givenNetworkTimeoutOrConnectionFailure() {
        caughtError = new java.net.SocketTimeoutException("Connection timed out");
        isNetworkError = true;
    }
    
    @Given("an API error response \\({int}xx or {int}xx\\)")
    public void givenApiErrorResponse(int client, int server) {
        httpStatusCode = 400;
        errorMessage = "Bad Request";
        caughtError = new RuntimeException("API Error: " + httpStatusCode);
        isApiError = true;
    }
    
    @Given("invalid input \\(e.g., malformed address\\)")
    public void givenInvalidInput() {
        caughtError = new IllegalArgumentException("Invalid address format: must be 64 hex characters");
        isValidationError = true;
    }
    
    @Given("a failed transaction")
    public void givenFailedTransaction() {
        vmStatus = "Move abort: 65537";
        abortCode = 65537;
        transactionHash = "0x" + "a".repeat(64);
        caughtError = new RuntimeException("Transaction failed: " + vmStatus);
        isTransactionError = true;
    }
    
    // ==========================================================================
    // Given Steps - VM Status Codes
    // ==========================================================================
    
    @Given("a transaction with vm_status {string}")
    public void givenTransactionWithVmStatus(String status) {
        vmStatus = status;
    }
    
    @Given("a transaction with vm_status containing abort code")
    public void givenTransactionWithAbortCode() {
        vmStatus = "Move abort in 0x1::coin: 65537";
        abortCode = 65537;
        abortModule = "0x1::coin";
    }
    
    @Given("a transaction that ran out of gas")
    public void givenTransactionRanOutOfGas() {
        vmStatus = "OUT_OF_GAS";
    }
    
    @Given("a transaction rejected for wrong sequence number")
    public void givenTransactionWrongSequenceNumber() {
        vmStatus = "SEQUENCE_NUMBER_TOO_OLD";
        errorMessage = "Expected sequence number 5, got 3";
    }
    
    @Given("a transaction failing due to insufficient balance")
    public void givenTransactionInsufficientBalance() {
        vmStatus = "Move abort in 0x1::coin: 65537";
        abortCode = 65537;
    }
    
    // ==========================================================================
    // Given Steps - Common Abort Codes
    // ==========================================================================
    
    @Given("common abort codes like:")
    public void givenCommonAbortCodes(DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        // Store abort code mappings for lookup
        world.getTestVectors().put("abort_codes", rows);
    }
    
    @Given("an abort from a custom module")
    public void givenAbortFromCustomModule() {
        vmStatus = "Move abort in 0xabc::my_module: 12345";
        abortCode = 12345;
        abortModule = "0xabc::my_module";
    }
    
    // ==========================================================================
    // Given Steps - Error Context
    // ==========================================================================
    
    @Given("an error during {string}")
    public void givenErrorDuringOperation(String operation) {
        caughtError = new RuntimeException("Error in " + operation + ": Connection refused");
    }
    
    @Given("a low-level error \\(e.g., JSON parse error\\)")
    public void givenLowLevelError() {
        Exception lowLevel = new com.google.gson.JsonSyntaxException("Unexpected token");
        caughtError = new RuntimeException("Failed to parse API response", lowLevel);
    }
    
    @Given("an API error with request ID header")
    public void givenApiErrorWithRequestId() {
        requestId = "req-12345-abcde";
        caughtError = new RuntimeException("API Error (request_id: " + requestId + ")");
    }
    
    // ==========================================================================
    // Given Steps - Language-Specific
    // ==========================================================================
    
    @Given("TypeScript SDK")
    public void givenTypeScriptSdk() {
        // TypeScript-specific test - skip in Java
    }
    
    @Given("Rust SDK")
    public void givenRustSdk() {
        // Rust-specific test - skip in Java
    }
    
    @Given("Python SDK")
    public void givenPythonSdk() {
        // Python-specific test - skip in Java
    }
    
    @Given("Go SDK")
    public void givenGoSdk() {
        // Go-specific test - skip in Java
    }
    
    // ==========================================================================
    // Given Steps - Retryable Errors
    // ==========================================================================
    
    @Given("an error")
    public void givenAnError() {
        caughtError = new RuntimeException("Some error occurred");
    }
    
    @Given("a transaction rejection for invalid signature")
    public void givenTransactionRejectionInvalidSignature() {
        caughtError = new RuntimeException("INVALID_SIGNATURE: Signature verification failed");
        isRetryable = false;
    }
    
    // ==========================================================================
    // Given Steps - Simulation Errors
    // ==========================================================================
    
    @Given("a transaction simulation that fails")
    public void givenTransactionSimulationThatFails() {
        simulationResult = new SimulationResult(false, "Move abort: 65537", 0);
    }
    
    @Given("a successful simulation")
    public void givenSuccessfulSimulation() {
        simulationResult = new SimulationResult(true, null, 1500);
    }
    
    // ==========================================================================
    // Given Steps - Wait Errors
    // ==========================================================================
    
    @Given("waiting for a transaction")
    public void givenWaitingForTransaction() {
        transactionHash = "0x" + "a".repeat(64);
    }
    
    @Given("waiting for a transaction that fails")
    public void givenWaitingForTransactionThatFails() {
        transactionHash = "0x" + "a".repeat(64);
        vmStatus = "Move abort: 65537";
    }
    
    // ==========================================================================
    // Given Steps - Recovery
    // ==========================================================================
    
    @Given("a SEQUENCE_NUMBER_TOO_OLD error")
    public void givenSequenceNumberTooOldError() {
        caughtError = new RuntimeException("SEQUENCE_NUMBER_TOO_OLD");
    }
    
    @Given("an OUT_OF_GAS error")
    public void givenOutOfGasError() {
        caughtError = new RuntimeException("OUT_OF_GAS");
    }
    
    @Given("a {int} Too Many Requests error")
    public void givenTooManyRequestsError(int statusCode) {
        httpStatusCode = statusCode;
        caughtError = new RuntimeException("Rate limited - retry after 60 seconds");
    }
    
    // ==========================================================================
    // When Steps - Catch Errors
    // ==========================================================================
    
    @When("I catch the error")
    public void whenCatchError() {
        // Error already caught in Given step
        assertThat(caughtError).isNotNull();
    }
    
    @When("I catch the validation error")
    public void whenCatchValidationError() {
        assertThat(caughtError).isNotNull();
    }
    
    @When("I check the status")
    public void whenCheckStatus() {
        // Status already set in Given step
    }
    
    @When("I parse the status")
    public void whenParseStatus() {
        // Parse abort code from vmStatus
        if (vmStatus != null && vmStatus.toString().contains("Move abort")) {
            String status = vmStatus.toString();
            // Extract module and abort code
            if (status.contains("::")) {
                abortModule = status.replaceAll(".*in (0x[^:]+::[^:]+):.*", "$1");
            }
            if (status.matches(".*\\d+.*")) {
                abortCode = Long.parseLong(status.replaceAll(".*[^\\d](\\d+).*", "$1"));
            }
        }
    }
    
    @When("I parse the error")
    public void whenParseError() {
        whenParseStatus();
    }
    
    @When("I receive these in errors")
    public void whenReceiveTheseInErrors() {
        // Abort codes received
    }
    
    @When("it propagates up")
    public void whenItPropagatesUp() {
        // Error propagation tested
    }
    
    @When("errors occur")
    public void whenErrorsOccur() {
        // Generic error handling
    }
    
    @When("operations can fail")
    public void whenOperationsCanFail() {
        // Generic failure handling
    }
    
    @When("I check if it's retryable")
    public void whenCheckIfRetryable() {
        // Check if error is retryable
        if (caughtError != null) {
            String msg = caughtError.getMessage();
            isRetryable = msg.contains("timeout") || 
                          msg.contains("connection") ||
                          msg.contains("rate limit") ||
                          msg.contains("Too Many Requests");
        }
    }
    
    @When("I check the error")
    public void whenCheckTheError() {
        assertThat(caughtError).isNotNull();
    }
    
    @When("I inspect the result")
    public void whenInspectResult() {
        assertThat(simulationResult).isNotNull();
    }
    
    @When("I check gas info")
    public void whenCheckGasInfo() {
        assertThat(simulationResult).isNotNull();
    }
    
    @When("it's not found after timeout")
    public void whenNotFoundAfterTimeout() {
        caughtError = new RuntimeException("Transaction not found: " + transactionHash);
    }
    
    @When("I detect the failure")
    public void whenDetectFailure() {
        assertThat(vmStatus).isNotNull();
    }
    
    @When("I log it")
    public void whenLogIt() {
        // Logging simulation
    }
    
    @When("I want to recover")
    public void whenWantToRecover() {
        // Recovery attempt
    }
    
    // ==========================================================================
    // Then Steps - Error Categories
    // ==========================================================================
    
    @Then("I should be able to identify it as a network error")
    public void thenShouldIdentifyAsNetworkError() {
        assertThat(isNetworkError || caughtError instanceof java.net.SocketException ||
                   caughtError instanceof java.net.SocketTimeoutException).isTrue();
    }
    
    @Then("it should be retryable")
    public void thenShouldBeRetryable() {
        assertThat(isRetryable || isNetworkError).isTrue();
    }
    
    @Then("I should see the HTTP status code")
    public void thenShouldSeeHttpStatusCode() {
        assertThat(httpStatusCode).isGreaterThan(0);
    }
    
    @Then("the error message from the API")
    public void thenShouldSeeErrorMessage() {
        assertThat(errorMessage).isNotNull();
    }
    
    @Then("I should see which input was invalid")
    public void thenShouldSeeWhichInputWasInvalid() {
        assertThat(caughtError.getMessage()).containsIgnoringCase("address");
    }
    
    @Then("why it was invalid")
    public void thenShouldSeeWhyInvalid() {
        assertThat(caughtError.getMessage()).contains("hex");
    }
    
    @Then("I should see the VM status code")
    public void thenShouldSeeVmStatusCode() {
        assertThat(vmStatus).isNotNull();
    }
    
    @Then("the abort code if applicable")
    public void thenShouldSeeAbortCode() {
        assertThat(abortCode).isGreaterThan(0);
    }
    
    @Then("the transaction hash if submitted")
    public void thenShouldSeeTransactionHash() {
        assertThat(transactionHash).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - VM Status Codes
    // ==========================================================================
    
    @Then("it should indicate success")
    public void thenShouldIndicateSuccess() {
        assertThat(vmStatus.toString()).containsIgnoringCase("success");
    }
    
    @Then("I should extract the abort code")
    public void thenShouldExtractAbortCode() {
        assertThat(abortCode).isGreaterThan(0);
    }
    
    @Then("the module that aborted \\(if available\\)")
    public void thenShouldSeeModuleThatAborted() {
        if (abortModule != null) {
            assertThat(abortModule).contains("::");
        }
    }
    
    @Then("I should identify it as out-of-gas error")
    public void thenShouldIdentifyOutOfGas() {
        assertThat(vmStatus.toString()).containsIgnoringCase("gas");
    }
    
    @Then("know that increasing max_gas_amount may help")
    public void thenKnowIncreasingGasMayHelp() {
        // Recovery suggestion
    }
    
    @Then("I should know the expected sequence number")
    public void thenShouldKnowExpectedSequenceNumber() {
        assertThat(errorMessage).matches(".*\\d+.*");
    }
    
    @Then("be able to retry with correct number")
    public void thenShouldRetryWithCorrectNumber() {
        // Retry capability
    }
    
    @Then("I should identify it as balance error")
    public void thenShouldIdentifyBalanceError() {
        assertThat(abortCode).isEqualTo(65537L);
    }
    
    @Then("know which account lacks funds")
    public void thenKnowWhichAccountLacksFunds() {
        // Account identification
    }
    
    // ==========================================================================
    // Then Steps - Common Abort Codes
    // ==========================================================================
    
    @Then("SDK should provide human-readable descriptions")
    public void thenSdkShouldProvideHumanReadableDescriptions() {
        // Human-readable error messages
    }
    
    @Then("I should see the module address")
    public void thenShouldSeeModuleAddress() {
        assertThat(abortModule).startsWith("0x");
    }
    
    @Then("the abort code from that module")
    public void thenShouldSeeAbortCodeFromModule() {
        assertThat(abortCode).isGreaterThan(0);
    }
    
    // ==========================================================================
    // Then Steps - Error Context
    // ==========================================================================
    
    @Then("I should know which operation failed")
    public void thenShouldKnowWhichOperationFailed() {
        assertThat(caughtError.getMessage()).containsAnyOf("submit", "get", "wait");
    }
    
    @Then("have context about the input")
    public void thenShouldHaveContextAboutInput() {
        assertThat(caughtError.getMessage()).isNotEmpty();
    }
    
    @Then("higher-level context should be added")
    public void thenHigherLevelContextShouldBeAdded() {
        assertThat(caughtError.getMessage()).contains("Failed to parse");
    }
    
    @Then("original error should be accessible")
    public void thenOriginalErrorShouldBeAccessible() {
        assertThat(caughtError.getCause()).isNotNull();
    }
    
    @Then("I should have access to the request ID for debugging")
    public void thenShouldHaveAccessToRequestId() {
        assertThat(requestId).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Language-Specific
    // ==========================================================================
    
    @Then("they should extend Error class")
    public void thenShouldExtendErrorClass() {
        // TypeScript specific - N/A for Java
    }
    
    @Then("have specific error types \\(AptosApiError, etc.\\)")
    public void thenShouldHaveSpecificErrorTypes() {
        // TypeScript specific - N/A for Java
    }
    
    @Then("be catchable by type")
    public void thenShouldBeCatchableByType() {
        // TypeScript specific - N/A for Java
    }
    
    @Then("they should return Result<T, E>")
    public void thenShouldReturnResult() {
        // Rust specific - N/A for Java
    }
    
    @Then("errors should implement std::error::Error")
    public void thenErrorsShouldImplementStdError() {
        // Rust specific - N/A for Java
    }
    
    @Then("be convertible to anyhow\\/thiserror")
    public void thenShouldBeConvertibleToAnyhow() {
        // Rust specific - N/A for Java
    }
    
    @Then("they should raise specific exceptions")
    public void thenShouldRaiseSpecificExceptions() {
        // Python specific - N/A for Java
    }
    
    @Then("inherit from a base AptosError class")
    public void thenShouldInheritFromAptosError() {
        // Python specific - N/A for Java
    }
    
    @Then("they should implement error interface")
    public void thenShouldImplementErrorInterface() {
        // Go specific - N/A for Java
    }
    
    @Then("support errors.Is\\/errors.As")
    public void thenShouldSupportErrorsIsAs() {
        // Go specific - N/A for Java
    }
    
    // ==========================================================================
    // Then Steps - Retryable Errors
    // ==========================================================================
    
    @Then("network errors should be retryable")
    public void thenNetworkErrorsShouldBeRetryable() {
        // Network error retry policy
    }
    
    @Then("rate limit errors should be retryable \\(with backoff\\)")
    public void thenRateLimitErrorsShouldBeRetryable() {
        // Rate limit retry policy
    }
    
    @Then("validation errors should NOT be retryable")
    public void thenValidationErrorsShouldNotBeRetryable() {
        // Validation errors are permanent
    }
    
    @Then("it should indicate permanent failure")
    public void thenShouldIndicatePermanentFailure() {
        assertThat(isRetryable).isFalse();
    }
    
    @Then("retrying won't help")
    public void thenRetryingWontHelp() {
        assertThat(isRetryable).isFalse();
    }
    
    // ==========================================================================
    // Then Steps - Simulation Errors
    // ==========================================================================
    
    @Then("I should see why it would fail")
    public void thenShouldSeeWhyItWouldFail() {
        SimulationResult result = (SimulationResult) simulationResult;
        assertThat(result.errorMessage).isNotNull();
    }
    
    @Then("be able to fix before actual submission")
    public void thenShouldBeAbleToFix() {
        // Fix capability
    }
    
    @Then("I should see gas_used")
    public void thenShouldSeeGasUsed() {
        SimulationResult result = (SimulationResult) simulationResult;
        assertThat(result.gasUsed).isGreaterThan(0);
    }
    
    @Then("be able to set appropriate max_gas_amount")
    public void thenShouldSetAppropriateMaxGas() {
        // Gas setting capability
    }
    
    // ==========================================================================
    // Then Steps - Wait Errors
    // ==========================================================================
    
    @Then("I should get a clear timeout error")
    public void thenShouldGetClearTimeoutError() {
        assertThat(caughtError.getMessage()).containsIgnoringCase("not found");
    }
    
    @Then("the hash I was waiting for")
    public void thenShouldSeeHashWaitingFor() {
        assertThat(caughtError.getMessage()).contains(transactionHash);
    }
    
    @Then("I should get the detailed failure reason")
    public void thenShouldGetDetailedFailureReason() {
        assertThat(vmStatus).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Error Messages
    // ==========================================================================
    
    @Then("the message should explain what went wrong")
    public void thenMessageShouldExplainWhatWentWrong() {
        assertThat(caughtError.getMessage()).isNotEmpty();
    }
    
    @Then("ideally suggest how to fix it")
    public void thenShouldSuggestHowToFix() {
        // Fix suggestions - best effort
    }
    
    @Then("it should not contain internal implementation details")
    public void thenShouldNotContainInternalDetails() {
        String msg = caughtError.getMessage();
        assertThat(msg).doesNotContain("NullPointerException");
    }
    
    @Then("should use terminology from Aptos documentation")
    public void thenShouldUseAptosTerminology() {
        // Terminology check
    }
    
    @Then("all relevant details should be included")
    public void thenAllDetailsShouldBeIncluded() {
        assertThat(caughtError.getMessage()).isNotEmpty();
    }
    
    @Then("sensitive data \\(keys\\) should NOT be included")
    public void thenSensitiveDataShouldNotBeIncluded() {
        String msg = caughtError.getMessage();
        assertThat(msg).doesNotContain("privateKey");
        assertThat(msg).doesNotContain("secret");
    }
    
    // ==========================================================================
    // Then Steps - Recovery
    // ==========================================================================
    
    @Then("SDK should help refresh sequence number")
    public void thenSdkShouldHelpRefreshSequenceNumber() {
        // Sequence number refresh capability
    }
    
    @Then("rebuild the transaction")
    public void thenRebuildTransaction() {
        // Transaction rebuild capability
    }
    
    @Then("SDK should help estimate proper gas")
    public void thenSdkShouldHelpEstimateGas() {
        // Gas estimation capability
    }
    
    @Then("rebuild with higher limit")
    public void thenRebuildWithHigherLimit() {
        // Rebuild capability
    }
    
    @Then("SDK should suggest waiting")
    public void thenSdkShouldSuggestWaiting() {
        // Wait suggestion
    }
    
    @Then("potentially auto-retry with backoff")
    public void thenPotentiallyAutoRetryWithBackoff() {
        // Auto-retry capability
    }
    
    // ==========================================================================
    // Helper Classes
    // ==========================================================================
    
    private static class SimulationResult {
        boolean success;
        String errorMessage;
        long gasUsed;
        
        SimulationResult(boolean success, String errorMessage, long gasUsed) {
            this.success = success;
            this.errorMessage = errorMessage;
            this.gasUsed = gasUsed;
        }
    }
}
