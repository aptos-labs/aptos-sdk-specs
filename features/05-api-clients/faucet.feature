@api-clients @preferred
Feature: Faucet Client
  As an SDK user
  I want to fund accounts with test tokens
  So that I can test my applications on testnet/devnet

  # =============================================================================
  # Faucet Configuration (no network required)
  # =============================================================================

  @preferred
  Scenario: Faucet client for testnet
    When I create a faucet client for testnet
    Then the base URL should be "https://faucet.testnet.aptoslabs.com"

  @preferred
  Scenario: Faucet client for devnet
    When I create a faucet client for devnet
    Then the base URL should be "https://faucet.devnet.aptoslabs.com"

  @preferred
  Scenario: Faucet client for localnet
    When I create a faucet client for localnet
    Then the base URL should be "http://localhost:8081"

  @preferred
  Scenario: Custom faucet URL
    Given a custom faucet URL "https://my-faucet.example.com"
    When I create a faucet client with the custom URL
    Then the client should use that URL

  @preferred
  Scenario: No faucet for mainnet
    When I try to create a faucet client for mainnet
    Then it should fail or return None
    And the error should indicate mainnet has no faucet

  # =============================================================================
  # Funding Accounts (requires network)
  # =============================================================================

  @preferred @network
  Scenario: Fund account with default amount
    Given a faucet client for testnet
    And a new account address
    When I request funding for the account
    Then the request should succeed
    And I should receive transaction hash(es)

  @preferred @network
  Scenario: Fund account with specific amount
    Given a faucet client for testnet
    And a new account address
    When I request funding for 100_000_000 octas (1 APT)
    Then the request should succeed

  @preferred @network
  Scenario: Fund account creates account if not exists
    Given a faucet client for testnet
    And an address that doesn't exist on-chain
    When I fund the account
    Then the account should be created
    And the account should have balance

  @preferred @network
  Scenario: Fund existing account adds to balance
    Given a faucet client for testnet
    And an existing account with 1 APT
    When I fund the account with 1 APT more
    Then the balance should increase

  @preferred @network
  Scenario: Multiple funding requests
    Given a faucet client for testnet
    And a new account address
    When I fund the account 3 times
    Then all requests should succeed
    And the balance should reflect all fundings

  # =============================================================================
  # Wait for Funding (requires network)
  # =============================================================================

  @preferred @network
  Scenario: Wait for funding transaction
    Given a faucet client
    When I fund an account
    And I wait for the funding transaction
    Then the transaction should be confirmed
    And the account should have the funded amount

  @preferred @network
  Scenario: Fund and wait convenience method
    Given a faucet client
    And a new account address
    When I call fund_and_wait
    Then the method should return after confirmation
    And the account should have balance

  @preferred @network
  Scenario: Funding timeout
    Given a faucet client
    And a very short timeout (1ms)
    When I try to fund and wait
    Then it should fail with timeout error

  # =============================================================================
  # Create Funded Account (requires network)
  # =============================================================================

  @preferred @network
  Scenario: Create new funded account
    Given an Aptos client with faucet
    When I call create_funded_account with 100_000_000 octas
    Then I should receive a new account
    And the account should have 100_000_000 octas balance
    And the account should be usable for signing

  @preferred @network
  Scenario: Create funded Ed25519 account
    Given an Aptos client with faucet
    When I create a funded Ed25519 account
    Then the account should be Ed25519 type
    And it should have balance

  @preferred @network
  Scenario: Create funded Secp256k1 account
    Given an Aptos client with faucet
    When I create a funded Secp256k1 account
    Then the account should be Secp256k1 type
    And it should have balance

  # =============================================================================
  # Error Handling
  # =============================================================================

  @preferred
  Scenario: Handle faucet rate limiting
    Given many rapid funding requests
    When the faucet returns rate limit error
    Then the error should indicate rate limiting
    And should suggest waiting

  @preferred @network
  Scenario: Handle faucet unavailable
    Given a faucet endpoint that is down
    When I try to fund an account
    Then I should receive a network error

  @preferred
  Scenario: Handle invalid address format
    Given an invalid address string
    When I try to fund it
    Then I should receive a validation error

  @preferred @network
  Scenario: Faucet returns transaction hashes
    Given a successful funding request
    When I inspect the response
    Then I should see one or more transaction hashes
    And each hash should be valid hex

  # =============================================================================
  # Integration with Aptos Client (mostly no network)
  # =============================================================================

  @preferred
  Scenario: Access faucet through Aptos client
    Given an Aptos client configured for testnet
    When I access the faucet client
    Then it should be available
    And configured for testnet faucet

  @preferred
  Scenario: Aptos client without faucet
    Given an Aptos client configured for mainnet
    When I try to access the faucet client
    Then it should be None or unavailable

  @preferred @network
  Scenario: High-level fund_account method
    Given an Aptos client for testnet
    And a new account address
    When I call aptos.fund_account(address, amount)
    Then the account should be funded
    And the method should wait for confirmation

