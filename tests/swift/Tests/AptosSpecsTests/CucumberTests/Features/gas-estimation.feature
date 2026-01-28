@api-clients
@preferred
Feature: Gas Estimation
  As an SDK user
  I want to estimate gas costs for transactions
  So that I can set appropriate gas parameters

  # =============================================================================
  # Gas Price Estimation
  # =============================================================================
  @preferred
  Scenario: Get current gas price estimate
    Given a connected Aptos client
    When I request gas price estimate
    Then I should receive gas_estimate
    And the value should be in octas per gas unit

  @preferred
  Scenario: Gas estimate includes priority options
    Given a connected Aptos client
    When I request gas price estimate
    Then I should receive gas_estimate (standard)
    And optionally prioritized_gas_estimate (faster)
    And optionally deprioritized_gas_estimate (slower/cheaper)

  @preferred
  Scenario: Prioritized gas is higher than standard
    Given gas price estimates
    When I compare prioritized vs standard
    Then prioritized should be >= standard

  @preferred
  Scenario: Deprioritized gas is lower than standard
    Given gas price estimates
    When I compare deprioritized vs standard
    Then deprioritized should be <= standard

  @preferred
  Scenario: Gas estimates are positive
    Given gas price estimates
    Then all estimates should be greater than 0

  # =============================================================================
  # Transaction Simulation for Gas
  # =============================================================================
  @preferred
  Scenario: Simulate transaction for gas usage
    Given a valid transaction
    When I simulate the transaction
    Then I should receive gas_used
    And gas_used represents actual consumption

  @preferred
  Scenario: Use simulation for max_gas_amount
    Given a transaction simulation result
    When I extract gas_used
    Then I can use it to set max_gas_amount with buffer

  @preferred
  Scenario: Simulation gas vs actual gas
    Given a simulated and executed transaction
    When I compare gas values
    Then actual gas should be similar to simulated
    And actual should not exceed max_gas_amount

  @preferred
  Scenario: Complex transaction uses more gas
    Given a simple transfer transaction
    And a complex smart contract call
    When I simulate both
    Then the complex call should use more gas

  # =============================================================================
  # Gas Configuration
  # =============================================================================
  @preferred
  Scenario: Default gas parameters
    Given a transaction builder with defaults
    When I check default values
    Then max_gas_amount should be reasonable (e.g., 200000)
    And gas_unit_price should be reasonable (e.g., 100)

  @preferred
  Scenario: Override gas unit price
    Given current gas estimate is 150
    When I build a transaction with gas_unit_price 200
    Then the transaction should use price 200

  @preferred
  Scenario: Override max gas amount
    Given a transaction builder
    When I set max_gas_amount to 500000
    Then the transaction should have that limit

  @preferred
  Scenario: Gas price affects transaction priority
    Given two transactions with different gas prices
    When both are submitted
    Then higher gas price should be processed first (usually)

  # =============================================================================
  # Gas Calculation
  # =============================================================================
  @preferred
  Scenario: Calculate total gas cost
    Given gas_used = 1000 units
    And gas_unit_price = 100 octas
    When I calculate total cost
    Then total should be 100000 octas

  @preferred
  Scenario: Estimate maximum cost
    Given max_gas_amount = 200000
    And gas_unit_price = 100
    When I calculate maximum possible cost
    Then max cost should be 20000000 octas (0.2 APT)

  @preferred
  Scenario: Actual cost vs maximum
    Given a completed transaction
    When I compare actual cost to max possible
    Then actual should be <= max possible
    And difference is refunded

  # =============================================================================
  # Insufficient Gas Handling
  # =============================================================================
  @preferred
  Scenario: Transaction fails with insufficient max gas
    Given a transaction requiring 50000 gas
    When I submit with max_gas_amount = 10000
    Then transaction should fail
    And error should indicate out of gas

  @preferred
  Scenario: Account has insufficient balance for gas
    Given an account with 1000 octas
    And a transaction requiring 10000 octas gas
    When I try to submit
    Then submission should fail
    And error should indicate insufficient balance

  @preferred
  Scenario: Simulation catches insufficient gas
    Given a transaction with very low max_gas_amount
    When I simulate it
    Then simulation should show failure
    And should indicate gas exhaustion

  # =============================================================================
  # Dynamic Gas Adjustment
  # =============================================================================
  @preferred
  Scenario: Auto-estimate gas for transaction
    Given an Aptos client with auto-gas enabled
    When I submit a transaction without specifying gas
    Then SDK should simulate first
    And set appropriate max_gas_amount

  @preferred
  Scenario: Apply buffer to gas estimate
    Given simulated gas_used = 10000
    When I apply 20% buffer
    Then max_gas_amount should be 12000

  @preferred
  Scenario: Fetch current gas price before submission
    Given an Aptos client
    When I build transaction without specifying gas_unit_price
    Then SDK should fetch current estimate
    And use it for the transaction

  # =============================================================================
  # Network Conditions
  # =============================================================================
  @preferred
  Scenario: Gas prices vary by network load
    Given network is under high load
    When I check gas estimates
    Then estimates should be higher than usual

  @preferred
  Scenario: Different networks have different gas
    Given mainnet and testnet clients
    When I check gas estimates on each
    Then values may differ between networks

  # =============================================================================
  # Error Cases
  # =============================================================================
  @preferred
  Scenario: Handle gas estimation failure
    Given a network error during estimation
    When I request gas estimate
    Then I should receive an appropriate error

  @preferred
  Scenario: Handle invalid gas parameters
    Given gas_unit_price = 0
    When I try to submit transaction
    Then it should fail with validation error
