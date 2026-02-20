@api-clients
@required
Feature: Fullnode REST API Client
  As an SDK user
  I want to interact with the Aptos fullnode API
  So that I can query and submit data to the blockchain

  # =============================================================================
  # Client Configuration (no network required)
  # =============================================================================
  @required
  Scenario: Create client for testnet
    When I create a client with testnet configuration
    Then the client should be configured for testnet
    And the base URL should be "https://fullnode.testnet.aptoslabs.com/v1"

  @required
  Scenario: Create client for mainnet
    When I create a client with mainnet configuration
    Then the client should be configured for mainnet
    And the base URL should be "https://fullnode.mainnet.aptoslabs.com/v1"

  @required
  Scenario: Create client with custom URL
    Given a custom URL "https://my-node.example.com/v1"
    When I create a client with the custom URL
    Then the client should use that URL for requests

  @preferred
  Scenario: Configure client timeout
    When I create a client with 30 second timeout
    Then requests should timeout after 30 seconds

  # =============================================================================
  # Ledger Information (requires network)
  # =============================================================================
  @required
  @network
  Scenario: Get ledger info
    Given a connected client
    When I request ledger info
    Then I should receive chain_id
    And I should receive ledger_version
    And I should receive block_height

  @required
  @network
  Scenario: Chain ID from ledger info
    Given a client connected to testnet
    When I get the ledger info
    Then chain_id should be 2

  # =============================================================================
  # Account Queries (requires network)
  # =============================================================================
  @required
  @network
  Scenario: Get account info for existing account
    Given a client connected to testnet
    And a known existing account address
    When I get account info for the address
    Then I should receive sequence_number
    And I should receive authentication_key

  @required
  @network
  Scenario: Get account info for non-existent account
    Given a client connected to testnet
    And a random unused account address
    When I get account info for the address
    Then I should receive a 404 NotFound error

  @required
  @network
  Scenario: Get account resources
    Given a client connected to testnet
    And an account address with resources
    When I get account resources
    Then I should receive a list of resources
    And each resource should have a type and data

  @required
  @network
  Scenario: Get specific account resource
    Given a client connected to testnet
    And an account with APT balance
    When I get resource "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    Then I should receive the coin store resource
    And I should be able to read the balance

  @required
  @network
  Scenario: Get non-existent resource
    Given a client connected to testnet
    And an account address
    When I get a resource type that doesn't exist
    Then I should receive a 404 NotFound error

  @preferred
  @network
  Scenario: Get account modules
    Given a client connected to testnet
    And an account with published modules (e.g., 0x1)
    When I get account modules
    Then I should receive a list of modules
    And each module should have bytecode and ABI

  @preferred
  @network
  Scenario: Module ABI includes enum variant definitions
    Given a client connected to testnet
    And a module containing enum types
    When I get the module ABI
    Then enum structs should have is_enum set to true
    And enum structs should have a variants array
    And each variant should have a name and fields array
    And non-enum structs should have an empty variants array

  # =============================================================================
  # Transaction Queries (requires network)
  # =============================================================================
  @required
  @network
  Scenario: Get transaction by hash - existing
    Given a client connected to testnet
    And a known transaction hash
    When I get transaction by hash
    Then I should receive the transaction details
    And I should see the transaction type
    And I should see the success status

  @required
  @network
  Scenario: Get transaction by hash - not found
    Given a client connected to testnet
    And a non-existent transaction hash
    When I get transaction by hash
    Then I should receive a 404 NotFound error

  @required
  @network
  Scenario: Get transaction by version
    Given a client connected to testnet
    And a known ledger version
    When I get transaction by version
    Then I should receive the transaction at that version

  @preferred
  @network
  Scenario: Get account transactions
    Given a client connected to testnet
    And an account with transaction history
    When I get account transactions
    Then I should receive a list of transactions
    And transactions should be for that account

  @preferred
  @network
  Scenario: Get account transactions with pagination
    Given a client connected to testnet
    And an account with many transactions
    When I get account transactions with start=10 and limit=5
    Then I should receive at most 5 transactions
    And they should start from the specified offset

  # =============================================================================
  # Response Headers (requires network)
  # =============================================================================
  @required
  @network
  Scenario: Parse ledger state from response headers
    Given a client connected to testnet
    When I make any API request
    Then the response should include ledger state
    And ledger state should have chain_id
    And ledger state should have ledger_version
    And ledger state should have block_height

  @required
  @network
  Scenario: Ledger version increases
    Given a client connected to testnet
    When I get ledger info twice with delay
    Then the second ledger_version should be >= first

  # =============================================================================
  # Error Handling
  # =============================================================================
  @required
  @network
  Scenario: Handle network error
    Given a client configured for unreachable URL
    When I try to make a request
    Then I should receive a Network error

  @required
  @network
  Scenario: Handle timeout
    Given a client with 1ms timeout
    When I try to make a request
    Then I should receive a Timeout error

  @required
  Scenario: Parse API error response
    Given a malformed request
    When the API returns an error
    Then the error should contain the message
    And the error should contain the error_code
    And the error should contain the HTTP status

  @preferred
  Scenario: Handle rate limiting
    Given many rapid requests
    When the API returns 429
    Then the error should indicate rate limiting
    And the SDK should respect retry-after if present

  # =============================================================================
  # Test Vectors / Known Values (requires network)
  # =============================================================================
  @required
  @network
  Scenario: Query framework account
    Given a client connected to any network
    When I get account info for "0x1"
    Then the account should exist
    And it should have resources

  @required
  @network
  Scenario: Query AptosCoin type
    Given a client connected to any network
    When I get the CoinInfo resource for AptosCoin
    Then I should see name "Aptos Coin"
    And I should see symbol "APT"
    And I should see decimals 8
