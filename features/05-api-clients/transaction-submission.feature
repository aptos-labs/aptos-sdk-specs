@api-clients @required
Feature: Transaction Submission
  As an SDK user
  I want to submit transactions to the blockchain
  So that I can execute on-chain operations

  # =============================================================================
  # Transaction Submission (requires network)
  # =============================================================================

  @required @network
  Scenario: Submit valid signed transaction
    Given a client connected to testnet
    And a funded account
    And a valid signed APT transfer transaction
    When I submit the transaction
    Then I should receive a pending transaction response
    And the response should contain the transaction hash

  @required @network
  Scenario: Submit transaction with correct content type
    Given a signed transaction for submission
    When I submit it to the API
    Then the request content type should be "application/x.aptos.signed_transaction+bcs"
    And the body should be BCS-serialized bytes

  @required @network
  Scenario: Submit transaction returns hash
    Given a valid signed transaction
    When I submit it successfully
    Then I should receive the transaction hash
    And the hash should be 64 hex characters with 0x prefix

  @required @network
  Scenario: Reject invalid transaction format
    Given malformed transaction bytes
    When I try to submit them
    Then I should receive a 400 Bad Request error

  @required @network
  Scenario: Reject transaction with invalid signature
    Given a signed transaction with corrupted signature
    When I try to submit it
    Then I should receive an error about invalid signature

  @required @network
  Scenario: Reject transaction with wrong chain ID
    Given a transaction signed for mainnet (chain_id=1)
    And a client connected to testnet (chain_id=2)
    When I try to submit the transaction
    Then I should receive an error about chain ID mismatch

  @required @network
  Scenario: Reject expired transaction
    Given a signed transaction with past expiration
    When I try to submit it
    Then I should receive an error about expired transaction

  # =============================================================================
  # Wait for Transaction (requires network)
  # =============================================================================

  @required @network
  Scenario: Wait for transaction success
    Given a submitted transaction hash
    When I wait for the transaction
    Then I should receive the final transaction result
    And the transaction should be committed or failed

  @required @network
  Scenario: Wait for transaction timeout
    Given a transaction hash that doesn't exist
    And a wait timeout of 5 seconds
    When I wait for the transaction
    Then I should receive a timeout error

  @required @network
  Scenario: Wait returns success status
    Given a successful transaction
    When I wait for it to complete
    Then the result should indicate success: true

  @required @network
  Scenario: Wait returns failure status
    Given a transaction that will fail (e.g., insufficient balance)
    When I wait for it to complete
    Then the result should indicate success: false
    And I should see the VM error

  @required @network
  Scenario: Wait polls until completion
    Given a newly submitted transaction
    When I wait for it
    Then the SDK should poll the API
    And return when the transaction is finalized

  # =============================================================================
  # Submit and Wait Convenience (requires network)
  # =============================================================================

  @required @network
  Scenario: Submit and wait for transaction
    Given a funded account
    And a valid transaction payload
    When I call submit_and_wait
    Then the transaction should be submitted
    And the method should return the final result

  @required @network
  Scenario: Sign, submit, and wait
    Given a funded account
    And a transaction payload
    When I call sign_submit_and_wait
    Then the transaction should be signed
    And submitted
    And waited upon
    And I should receive the final result

  # =============================================================================
  # Transaction Simulation (requires network)
  # =============================================================================

  @preferred @network
  Scenario: Simulate transaction
    Given a signed transaction for submission
    When I simulate the transaction
    Then I should receive simulation results
    And the results should include gas_used
    And the results should include success status

  @preferred @network
  Scenario: Simulate shows gas estimate
    Given a valid transaction
    When I simulate it
    Then I should see the estimated gas_used
    And I can use this to set max_gas_amount

  @preferred @network
  Scenario: Simulate shows VM error for failing tx
    Given a transaction that would fail
    When I simulate it
    Then I should see success: false
    And I should see the VM error details

  @preferred @network
  Scenario: Simulate with insufficient balance
    Given a transfer transaction for more than account balance
    When I simulate it
    Then I should see the failure reason
    And the error should indicate insufficient balance

  @preferred @network
  Scenario: Simulate doesn't require valid signature
    Given a transaction with invalid signature
    When I simulate it
    Then simulation should still work
    And show what would happen if signature were valid

  # =============================================================================
  # Gas Estimation (requires network)
  # =============================================================================

  @preferred @network
  Scenario: Get gas price estimate
    Given a client connected to testnet
    When I request gas price estimate
    Then I should receive gas_estimate
    And optionally prioritized_gas_estimate
    And optionally deprioritized_gas_estimate

  @preferred @network
  Scenario: Use gas estimate for transaction
    Given a gas price estimate
    When I build a transaction using the estimate
    And submit it
    Then the transaction should be accepted

  # =============================================================================
  # Sequence Number Handling (requires network)
  # =============================================================================

  @required @network
  Scenario: Get current sequence number
    Given a client connected to testnet
    And an account address
    When I get the account info
    Then I should receive the current sequence_number

  @required @network
  Scenario: Submit with correct sequence number
    Given an account with sequence_number 5
    When I submit a transaction with sequence_number 5
    Then the transaction should be accepted

  @required @network
  Scenario: Reject wrong sequence number
    Given an account with sequence_number 5
    When I submit a transaction with sequence_number 10
    Then I should receive an error about sequence number

  @required @network
  Scenario: Submit multiple transactions in sequence
    Given a funded account
    When I submit transactions with sequence numbers 0, 1, 2
    Then all should be accepted
    And processed in order

  # =============================================================================
  # Error Handling
  # =============================================================================

  @required @network
  Scenario: Handle submission network error
    Given a client with unreachable endpoint
    When I try to submit a transaction
    Then I should receive a Network error
    And I can retry the submission

  @required @network
  Scenario: Handle VM error in response
    Given a transaction that fails on-chain
    When I wait for it
    Then I should see vm_status in the result
    And I should be able to extract the error code

  @required
  Scenario: Transaction hash is predictable
    Given a signed transaction for submission
    When I compute its hash locally
    And compare with the hash from submission response
    Then they should match

