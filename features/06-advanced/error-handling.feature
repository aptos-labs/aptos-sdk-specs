@advanced @required
Feature: Error Handling
  As an SDK user
  I want consistent and informative error handling
  So that I can properly handle failures and debug issues

  # =============================================================================
  # Error Categories
  # =============================================================================

  @required
  Scenario: Network errors are distinguishable
    Given a network timeout or connection failure
    When I catch the error
    Then I should be able to identify it as a network error
    And it should be retryable

  @required
  Scenario: API errors include status code
    Given an API error response (4xx or 5xx)
    When I catch the error
    Then I should see the HTTP status code
    And the error message from the API

  @required
  Scenario: Validation errors are informative
    Given invalid input (e.g., malformed address)
    When I catch the validation error
    Then I should see which input was invalid
    And why it was invalid

  @required
  Scenario: Transaction errors include details
    Given a failed transaction
    When I catch the error
    Then I should see the VM status code
    And the abort code if applicable
    And the transaction hash if submitted

  # =============================================================================
  # VM Status Codes
  # =============================================================================

  @required
  Scenario: Parse success status
    Given a transaction with vm_status "success"
    When I check the status
    Then it should indicate success

  @required
  Scenario: Parse execution failure
    Given a transaction with vm_status containing abort code
    When I parse the status
    Then I should extract the abort code
    And the module that aborted (if available)

  @required
  Scenario: Parse out of gas failure
    Given a transaction that ran out of gas
    When I parse the status
    Then I should identify it as out-of-gas error
    And know that increasing max_gas_amount may help

  @required
  Scenario: Parse sequence number error
    Given a transaction rejected for wrong sequence number
    When I parse the error
    Then I should know the expected sequence number
    And be able to retry with correct number

  @required
  Scenario: Parse insufficient balance error
    Given a transaction failing due to insufficient balance
    When I parse the error
    Then I should identify it as balance error
    And know which account lacks funds

  # =============================================================================
  # Common Abort Codes
  # =============================================================================

  @preferred
  Scenario: Recognize standard abort codes
    Given common abort codes like:
      | Code   | Module        | Meaning              |
      | 65537  | coin          | Insufficient balance |
      | 65542  | account       | Account not found    |
    When I receive these in errors
    Then SDK should provide human-readable descriptions

  @preferred
  Scenario: Custom module abort codes
    Given an abort from a custom module
    When I parse the error
    Then I should see the module address
    And the abort code from that module

  # =============================================================================
  # Error Wrapping and Context
  # =============================================================================

  @required
  Scenario: Errors include operation context
    Given an error during "submit_transaction"
    When I catch the error
    Then I should know which operation failed
    And have context about the input

  @required
  Scenario: Errors are chainable
    Given a low-level error (e.g., JSON parse error)
    When it propagates up
    Then higher-level context should be added
    And original error should be accessible

  @preferred
  Scenario: Errors include request ID
    Given an API error with request ID header
    When I catch the error
    Then I should have access to the request ID for debugging

  # =============================================================================
  # Error Types (Language-Specific)
  # =============================================================================

  @required
  Scenario: TypeScript uses typed errors
    Given TypeScript SDK
    When errors occur
    Then they should extend Error class
    And have specific error types (AptosApiError, etc.)
    And be catchable by type

  @required
  Scenario: Rust uses Result types
    Given Rust SDK
    When operations can fail
    Then they should return Result<T, E>
    And errors should implement std::error::Error
    And be convertible to anyhow/thiserror

  @required
  Scenario: Python uses exceptions
    Given Python SDK
    When errors occur
    Then they should raise specific exceptions
    And inherit from a base AptosError class

  @required
  Scenario: Go uses error interface
    Given Go SDK
    When errors occur
    Then they should implement error interface
    And support errors.Is/errors.As

  # =============================================================================
  # Recoverable vs Non-Recoverable
  # =============================================================================

  @required
  Scenario: Identify retryable errors
    Given an error
    When I check if it's retryable
    Then network errors should be retryable
    And rate limit errors should be retryable (with backoff)
    And validation errors should NOT be retryable

  @required
  Scenario: Identify permanent failures
    Given a transaction rejection for invalid signature
    When I check the error
    Then it should indicate permanent failure
    And retrying won't help

  # =============================================================================
  # Simulation Errors
  # =============================================================================

  @required
  Scenario: Simulation failure with details
    Given a transaction simulation that fails
    When I inspect the result
    Then I should see why it would fail
    And be able to fix before actual submission

  @required
  Scenario: Simulation gas estimation
    Given a successful simulation
    When I check gas info
    Then I should see gas_used
    And be able to set appropriate max_gas_amount

  # =============================================================================
  # Wait for Transaction Errors
  # =============================================================================

  @required
  Scenario: Transaction not found during wait
    Given waiting for a transaction
    When it's not found after timeout
    Then I should get a clear timeout error
    And the hash I was waiting for

  @required
  Scenario: Transaction failed during wait
    Given waiting for a transaction that fails
    When I detect the failure
    Then I should get the detailed failure reason

  # =============================================================================
  # Error Messages
  # =============================================================================

  @required
  Scenario: Error messages are actionable
    Given an error
    Then the message should explain what went wrong
    And ideally suggest how to fix it

  @preferred
  Scenario: No internal jargon in user-facing errors
    Given an error shown to SDK users
    Then it should not contain internal implementation details
    And should use terminology from Aptos documentation

  @preferred
  Scenario: Errors are loggable
    Given an error
    When I log it
    Then all relevant details should be included
    And sensitive data (keys) should NOT be included

  # =============================================================================
  # Error Recovery Patterns
  # =============================================================================

  @preferred
  Scenario: Sequence number recovery
    Given a SEQUENCE_NUMBER_TOO_OLD error
    When I want to recover
    Then SDK should help refresh sequence number
    And rebuild the transaction

  @preferred
  Scenario: Gas estimation recovery
    Given an OUT_OF_GAS error
    When I want to recover
    Then SDK should help estimate proper gas
    And rebuild with higher limit

  @preferred
  Scenario: Rate limit recovery
    Given a 429 Too Many Requests error
    When I want to recover
    Then SDK should suggest waiting
    And potentially auto-retry with backoff

