@api-clients @preferred
Feature: Automatic Retry and Backoff
  As an SDK user
  I want automatic retry for transient failures
  So that my application is resilient to temporary issues

  # =============================================================================
  # Retry Configuration
  # =============================================================================

  @preferred
  Scenario: Default retry configuration
    Given a new Aptos client
    When I check default retry settings
    Then max_retries should be 3
    And initial_delay should be around 100ms
    And max_delay should be around 5 seconds
    And backoff should be exponential

  @preferred
  Scenario: Custom retry configuration
    Given retry config with max_retries=5, initial_delay=200ms
    When I create an Aptos client with this config
    Then the client should use custom settings

  @preferred
  Scenario: Disable retries
    Given retry config with max_retries=0
    When I create an Aptos client
    Then requests should not retry on failure

  @preferred
  Scenario: Custom backoff factor
    Given retry config with backoff_factor=3.0
    When I configure the client
    Then delays should triple between retries

  # =============================================================================
  # Retryable Errors
  # =============================================================================

  @preferred
  Scenario: Retry on network timeout
    Given a request that times out
    When the SDK handles the error
    Then it should retry the request
    And respect the retry configuration

  @preferred
  Scenario: Retry on connection failure
    Given a request that fails to connect
    When the SDK handles the error
    Then it should retry the request

  @preferred
  Scenario: Retry on 429 Too Many Requests
    Given a request that returns HTTP 429
    When the SDK handles the error
    Then it should retry after delay
    And should respect Retry-After header if present

  @preferred
  Scenario: Retry on 500 Internal Server Error
    Given a request that returns HTTP 500
    When the SDK handles the error
    Then it should retry the request

  @preferred
  Scenario: Retry on 502 Bad Gateway
    Given a request that returns HTTP 502
    When the SDK handles the error
    Then it should retry the request

  @preferred
  Scenario: Retry on 503 Service Unavailable
    Given a request that returns HTTP 503
    When the SDK handles the error
    Then it should retry the request

  @preferred
  Scenario: Retry on 504 Gateway Timeout
    Given a request that returns HTTP 504
    When the SDK handles the error
    Then it should retry the request

  # =============================================================================
  # Non-Retryable Errors
  # =============================================================================

  @preferred
  Scenario: No retry on 400 Bad Request
    Given a request that returns HTTP 400
    When the SDK handles the error
    Then it should NOT retry
    And should return the error immediately

  @preferred
  Scenario: No retry on 401 Unauthorized
    Given a request that returns HTTP 401
    When the SDK handles the error
    Then it should NOT retry

  @preferred
  Scenario: No retry on 403 Forbidden
    Given a request that returns HTTP 403
    When the SDK handles the error
    Then it should NOT retry

  @preferred
  Scenario: No retry on 404 Not Found
    Given a request that returns HTTP 404
    When the SDK handles the error
    Then it should NOT retry

  @preferred
  Scenario: No retry on transaction rejection
    Given a transaction rejected for invalid sequence number
    When the SDK handles the error
    Then it should NOT retry the same transaction

  # =============================================================================
  # Exponential Backoff
  # =============================================================================

  @preferred
  Scenario: Exponential backoff delays
    Given initial_delay=100ms and backoff_factor=2.0
    When retries occur
    Then delay 1 should be ~100ms
    And delay 2 should be ~200ms
    And delay 3 should be ~400ms

  @preferred
  Scenario: Backoff respects max delay
    Given initial_delay=100ms, backoff_factor=2.0, max_delay=500ms
    When many retries occur
    Then delays should never exceed 500ms

  @preferred
  Scenario: Jitter in backoff
    Given exponential backoff with jitter enabled
    When multiple retries occur
    Then delays should have some randomness
    And not be exactly the calculated values

  # =============================================================================
  # Retry Behavior
  # =============================================================================

  @preferred
  Scenario: Success after retry
    Given a request that fails twice then succeeds
    When the SDK makes the request
    Then it should retry twice
    And return the successful response

  @preferred
  Scenario: Exhaust all retries
    Given a request that always fails
    And max_retries=3
    When the SDK makes the request
    Then it should try 4 times total (1 + 3 retries)
    And return the final error

  @preferred
  Scenario: Error includes retry information
    Given a request that fails after retries
    When I inspect the error
    Then I should see how many retries were attempted

  @preferred
  Scenario: Retry preserves request
    Given a POST request with body
    When it needs to be retried
    Then the retry should include the same body
    And the same headers

  # =============================================================================
  # Idempotency Considerations
  # =============================================================================

  @preferred
  Scenario: Safe to retry GET requests
    Given a GET request
    When it fails with retryable error
    Then retrying is safe (idempotent)

  @preferred
  Scenario: Transaction submission retry considerations
    Given a transaction submission that times out
    When deciding whether to retry
    Then SDK should check if transaction was received
    And avoid duplicate submissions if possible

  @preferred
  Scenario: Check transaction status before retry
    Given a submitted transaction with unknown status
    When the response times out
    Then SDK should check transaction status before deciding to resubmit

  # =============================================================================
  # Rate Limit Handling
  # =============================================================================

  @preferred
  Scenario: Respect Retry-After header
    Given a 429 response with Retry-After: 5
    When the SDK handles it
    Then it should wait at least 5 seconds before retrying

  @preferred
  Scenario: Retry-After as date
    Given a 429 response with Retry-After as HTTP date
    When the SDK handles it
    Then it should calculate wait time from date
    And wait appropriately

  @preferred
  Scenario: No Retry-After header
    Given a 429 response without Retry-After
    When the SDK handles it
    Then it should use default backoff

  # =============================================================================
  # Integration
  # =============================================================================

  @preferred
  Scenario: Retry works for all API methods
    Given an Aptos client with retry enabled
    When any API method encounters retryable error
    Then retry logic should apply

  @preferred
  Scenario: Disable retry for specific request
    Given an Aptos client with retry enabled
    When I make a request with retry disabled
    Then that request should not retry

  @preferred
  Scenario: Retry callbacks for monitoring
    Given retry config with callback
    When a retry occurs
    Then the callback should be invoked
    And receive retry attempt number and error

