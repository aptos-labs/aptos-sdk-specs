@api-clients
@preferred
Feature: View Function Execution
  As an SDK user
  I want to execute view functions
  So that I can read on-chain state without transactions

  # =============================================================================
  # Basic View Function Calls
  # =============================================================================
  @preferred
  Scenario: Execute simple view function
    Given a client connected to testnet
    When I call view function "0x1::coin::balance"
    And with type arguments ["0x1::aptos_coin::AptosCoin"]
    And arguments ["0x1"]
    Then the call should succeed
    And I should receive return values

  @preferred
  Scenario: Execute view function without type arguments
    Given a client connected to testnet
    When I call view function "0x1::account::exists_at"
    And with no type arguments
    And arguments ["0x1"]
    Then the call should succeed
    And the result should be a boolean

  @preferred
  Scenario: Execute view function without arguments
    Given a client connected to testnet
    When I call view function "0x1::timestamp::now_seconds"
    And with no type arguments
    And no arguments
    Then the call should succeed
    And the result should be a u64

  @preferred
  Scenario: Execute view function with multiple return values
    Given a client connected to testnet
    When I call a view function that returns multiple values
    Then I should receive all return values in order

  # =============================================================================
  # Argument Encoding
  # =============================================================================
  @preferred
  Scenario: Pass address argument
    Given a view function expecting an address
    When I pass address "0x1" as argument
    Then the address should be properly encoded

  @preferred
  Scenario: Pass u64 argument
    Given a view function expecting a u64
    When I pass number 1000000 as argument
    Then the number should be properly encoded

  @preferred
  Scenario: Pass string argument
    Given a view function expecting a string
    When I pass "hello world" as argument
    Then the string should be properly encoded

  @preferred
  Scenario: Pass vector argument
    Given a view function expecting vector<u8>
    When I pass bytes [1, 2, 3, 4, 5] as argument
    Then the vector should be properly encoded

  @preferred
  Scenario: Pass bool argument
    Given a view function expecting a bool
    When I pass true as argument
    Then the boolean should be properly encoded

  # =============================================================================
  # Type Argument Handling
  # =============================================================================
  @preferred
  Scenario: Single type argument
    Given a view function with one type parameter
    When I call with type argument "0x1::aptos_coin::AptosCoin"
    Then the type should be properly passed

  @preferred
  Scenario: Multiple type arguments
    Given a view function with multiple type parameters
    When I call with type arguments ["Type1", "Type2"]
    Then both types should be properly passed

  @preferred
  Scenario: Nested type argument
    Given a view function with generic type
    When I call with type argument "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    Then the nested type should be properly parsed

  # =============================================================================
  # Return Value Parsing
  # =============================================================================
  @preferred
  Scenario: Parse u64 return value
    Given a view function returning u64
    When I execute the call
    Then I should be able to parse the result as u64

  @preferred
  Scenario: Parse string return value
    Given a view function returning a String
    When I execute the call
    Then I should be able to parse the result as string

  @preferred
  Scenario: Parse bool return value
    Given a view function returning bool
    When I execute the call
    Then I should be able to parse the result as boolean

  @preferred
  Scenario: Parse vector return value
    Given a view function returning vector<u8>
    When I execute the call
    Then I should be able to parse the result as byte array

  @preferred
  Scenario: Parse struct return value
    Given a view function returning a struct
    When I execute the call
    Then I should be able to access struct fields

  # =============================================================================
  # Error Cases
  # =============================================================================
  @preferred
  Scenario: View function not found
    Given a client connected to testnet
    When I call non-existent view function "0x1::nonexistent::function"
    Then I should receive an error
    And the error should indicate function not found

  @preferred
  Scenario: Invalid arguments
    Given a client connected to testnet
    When I call a view function with wrong argument types
    Then I should receive an error
    And the error should indicate type mismatch

  @preferred
  Scenario: Wrong number of arguments
    Given a client connected to testnet
    When I call a view function with too few arguments
    Then I should receive an error

  @preferred
  Scenario: Wrong number of type arguments
    Given a client connected to testnet
    When I call a generic function without type arguments
    Then I should receive an error

  @preferred
  Scenario: View function aborts
    Given a view function that can abort
    When I call with arguments that cause abort
    Then I should receive an error
    And the error should contain the abort code

  # =============================================================================
  # Common View Functions
  # =============================================================================
  @preferred
  Scenario: Get coin balance
    Given a client connected to testnet
    And an account with APT balance
    When I call 0x1::coin::balance<0x1::aptos_coin::AptosCoin>
    And with the account address as argument
    Then I should receive the balance as u64

  @preferred
  Scenario: Check account exists
    Given a client connected to testnet
    When I call 0x1::account::exists_at
    And with address "0x1" as argument
    Then I should receive true

  @preferred
  Scenario: Get current timestamp
    Given a client connected to testnet
    When I call 0x1::timestamp::now_seconds
    Then I should receive current blockchain timestamp

  @preferred
  Scenario: Get coin supply
    Given a client connected to testnet
    When I call 0x1::coin::supply<0x1::aptos_coin::AptosCoin>
    Then I should receive the total supply

  # =============================================================================
  # At Specific Ledger Version
  # =============================================================================
  @preferred
  Scenario: Execute view function at specific version
    Given a client connected to testnet
    And a known past ledger version
    When I call a view function at that version
    Then I should receive the state as of that version

  @preferred
  Scenario: View function at too old version
    Given a client connected to testnet
    And a ledger version older than oldest available
    When I try to call a view function at that version
    Then I should receive an error about unavailable state
