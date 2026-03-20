@advanced
@preferred
Feature: Transaction Simulation
  As an SDK user
  I want to simulate transactions before submission
  So that I can preview results and estimate gas

  # =============================================================================
  # Basic Simulation
  # =============================================================================
  @preferred
  Scenario: Simulate valid transaction
    Given a valid transaction
    When I simulate it
    Then I should get a simulation result
    And it should include gas_used
    And it should include success status

  @preferred
  Scenario: Simulate without signing
    Given a transaction I haven't signed yet
    When I simulate it
    Then simulation should work
    And use a dummy signature internally

  @preferred
  Scenario: Simulation result includes changes
    Given a transaction simulation
    When I inspect the result
    Then I should see state changes that would occur
    And events that would be emitted

  # =============================================================================
  # Gas Estimation
  # =============================================================================
  @preferred
  Scenario: Use simulation for gas estimation
    Given a transaction
    When I simulate it
    Then gas_used tells me actual consumption
    And I can set max_gas_amount with buffer

  @preferred
  Scenario: Simulation shows max_gas_amount needed
    Given a complex transaction
    When I simulate with different max_gas amounts
    Then I can find the minimum needed

  @preferred
  Scenario: Gas varies by transaction complexity
    Given a simple transfer
    And a complex smart contract call
    When I simulate both
    Then the complex call should use more gas

  # =============================================================================
  # Preview State Changes
  # =============================================================================
  @preferred
  Scenario: Preview balance changes
    Given a transfer transaction
    When I simulate it
    Then I should see sender balance decrease
    And recipient balance increase

  @preferred
  Scenario: Preview resource changes
    Given a transaction that modifies resources
    When I simulate it
    Then I should see which resources change
    And their new values

  @preferred
  Scenario: Preview events
    Given a transaction that emits events
    When I simulate it
    Then I should see which events would emit
    And their data

  # =============================================================================
  # Failure Preview
  # =============================================================================
  @preferred
  Scenario: Simulation shows abort
    Given a transaction that would abort
    When I simulate it
    Then simulation should show failure
    And include the abort code
    And the module that aborted

  @preferred
  Scenario: Simulation shows insufficient balance
    Given a transfer exceeding sender's balance
    When I simulate it
    Then simulation should fail
    And indicate insufficient funds

  @preferred
  Scenario: Simulation shows type errors
    Given a transaction with wrong type arguments
    When I simulate it
    Then simulation should fail
    And indicate the type mismatch

  @preferred
  Scenario: Simulation catches access errors
    Given a transaction accessing non-existent resource
    When I simulate it
    Then simulation should fail
    And indicate resource not found

  # =============================================================================
  # Simulation Options
  # =============================================================================
  @preferred
  Scenario: Simulate at specific version
    Given a historical ledger version
    When I simulate at that version
    Then simulation uses state at that version

  @preferred
  Scenario: Simulate with gas override
    Given a transaction
    When I simulate with specific max_gas_amount
    Then simulation respects that limit

  @preferred
  Scenario: Simulate with gas price override
    Given a transaction
    When I simulate with specific gas_unit_price
    Then simulation uses that price for calculations

  # =============================================================================
  # Multi-Agent Simulation
  # =============================================================================
  @preferred
  Scenario: Simulate multi-agent tx with senderPublicKey + secondarySignersPublicKeys
    Given a multi-agent simulation transaction with 1 secondary signer
    And sender public key is provided for simulation
    And secondary signer public keys are provided for simulation
    When I simulate the multi-agent transaction
    Then simulation should work
    And auth-key checks should run for all provided signers

  @preferred
  Scenario: Simulate multi-agent tx with no public keys (skip auth-key checks)
    Given a multi-agent transaction
    And no signer public keys are provided for simulation
    When I simulate the multi-agent transaction
    Then simulation should work
    And auth-key checks should be skipped

  @preferred
  Scenario: Simulate multi-agent tx with partial auth-key checks using undefined placeholders
    Given a multi-agent simulation transaction with 3 secondary signers
    And sender public key is provided for simulation
    And secondary signer public keys include undefined placeholders
    When I simulate the multi-agent transaction
    Then simulation should work
    And auth-key checks should run only for provided signer slots

  @preferred
  Scenario: Reject simulation input when secondary signer key mapping is malformed
    Given a multi-agent simulation transaction with 2 secondary signers
    And secondary signer public key mapping has wrong length
    When I try to simulate
    Then I should get validation error before simulation even runs

  @preferred
  Scenario: Simulation result includes changes/events across involved accounts
    Given a multi-agent transaction
    And a simulation result covering sender and secondary accounts
    When I inspect the multi-agent simulation result
    Then simulation should work
    And show changes for all involved accounts
    And it should include events for involved accounts

  @preferred
  Scenario: Simulate multi-agent + fee payer transaction with skipped auth-key checks
    Given a fee payer transaction with sender, secondary, and sponsor
    And no signer public keys are provided for simulation
    When I simulate the multi-agent fee-payer transaction
    Then simulation should work
    And gas should be charged to fee payer
    And simulation should reflect that

  @preferred
  Scenario: Simulate multi-agent + fee payer transaction with explicit signer key checks
    Given a fee payer transaction with sender, secondary, and sponsor
    And sender, secondary, and fee payer public keys are provided for simulation
    When I simulate the multi-agent fee-payer transaction
    Then simulation should work
    And gas should be charged to fee payer
    And auth-key checks should run for all provided signers
    And simulation should reflect that

  # =============================================================================
  # Simulation vs Execution
  # =============================================================================
  @preferred
  Scenario: Simulation does not commit changes
    Given a simulation
    When it completes
    Then no on-chain state should change
    And I can submit the real transaction

  @preferred
  Scenario: Simulation results may differ from execution
    Given blockchain state changes between simulate and submit
    When I submit after simulation
    Then results might differ
    And this is expected behavior

  @preferred
  Scenario: Simulation with current sequence number
    Given current sequence number is 5
    When I simulate transaction with seq num 5
    Then simulation should work even if account hasn't committed seq 5 yet

  # =============================================================================
  # Batch Simulation
  # =============================================================================
  @optional
  Scenario: Simulate multiple transactions
    Given multiple transactions
    When I simulate them in batch
    Then I should get results for each
    And save API calls

  @optional
  Scenario: Simulate transaction sequence
    Given transactions with sequential sequence numbers
    When I simulate them in order
    Then later simulations should see earlier changes

  # =============================================================================
  # Error Cases
  # =============================================================================
  @preferred
  Scenario: Simulation network error
    Given API is unavailable
    When I try to simulate
    Then I should get a network error not a simulation failure

  @preferred
  Scenario: Invalid transaction for simulation
    Given a malformed transaction
    When I try to simulate
    Then I should get validation error before simulation even runs

  @preferred
  Scenario: Simulation timeout
    Given a very complex transaction
    When simulation takes too long
    Then I should get timeout error with suggestion to increase timeout
