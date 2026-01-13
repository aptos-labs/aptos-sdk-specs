@api-clients @optional
Feature: Indexer GraphQL Client
  As an SDK user
  I want to query indexed blockchain data
  So that I can efficiently retrieve complex data like NFTs and token balances

  # =============================================================================
  # Client Configuration
  # =============================================================================

  @optional
  Scenario: Indexer client for mainnet
    When I create an indexer client for mainnet
    Then the base URL should be "https://indexer.mainnet.aptoslabs.com/v1/graphql"

  @optional
  Scenario: Indexer client for testnet
    When I create an indexer client for testnet
    Then the base URL should be "https://indexer.testnet.aptoslabs.com/v1/graphql"

  @optional
  Scenario: Custom indexer URL
    Given a custom indexer URL
    When I create an indexer client with the custom URL
    Then the client should use that URL

  @optional
  Scenario: Indexer client with API key
    Given an API key for the indexer
    When I create an indexer client with the key
    Then requests should include the API key header

  # =============================================================================
  # Raw GraphQL Queries
  # =============================================================================

  @optional
  Scenario: Execute raw GraphQL query
    Given an indexer client
    And a GraphQL query string
    When I execute the query
    Then I should receive the query result

  @optional
  Scenario: Execute query with variables
    Given an indexer client
    And a GraphQL query with variables
    And variable values
    When I execute the query with variables
    Then the variables should be substituted

  @optional
  Scenario: Handle GraphQL errors
    Given an invalid GraphQL query
    When I execute it
    Then I should receive a GraphQL error
    And the error should contain the error message

  # =============================================================================
  # Account Tokens (NFTs)
  # =============================================================================

  @optional
  Scenario: Get account current tokens
    Given an indexer client
    And an account address with NFTs
    When I query current tokens for the account
    Then I should receive a list of tokens
    And each token should have collection info
    And each token should have token_data_id

  @optional
  Scenario: Get account tokens with pagination
    Given an account with many NFTs
    When I query tokens with limit 10 and offset 0
    Then I should receive at most 10 tokens
    When I query with offset 10
    Then I should receive the next page

  @optional
  Scenario: Token data includes metadata
    Given an account with an NFT
    When I query the token
    Then I should see token_name
    And I should see collection_name
    And I should see token_uri
    And I should see amount

  @optional
  Scenario: Account with no tokens
    Given an account with no NFTs
    When I query current tokens
    Then I should receive an empty list

  # =============================================================================
  # Fungible Asset Balances
  # =============================================================================

  @optional
  Scenario: Get fungible asset balances
    Given an indexer client
    And an account address
    When I query fungible asset balances
    Then I should receive a list of balances
    And each should have asset_type
    And each should have amount

  @optional
  Scenario: Get specific fungible asset balance
    Given an account with APT
    When I query APT fungible asset balance
    Then I should receive the balance amount

  @optional
  Scenario: Fungible asset metadata
    Given a fungible asset query
    When I request metadata
    Then I should see name
    And I should see symbol
    And I should see decimals

  # =============================================================================
  # Transaction History
  # =============================================================================

  @optional
  Scenario: Get account transaction history
    Given an indexer client
    And an account with transaction history
    When I query account transactions
    Then I should receive a list of transactions
    And transactions should be ordered by version

  @optional
  Scenario: Transaction history with pagination
    Given an account with many transactions
    When I query with limit 25
    Then I should receive at most 25 transactions

  @optional
  Scenario: Transaction includes details
    Given an account transaction
    When I query it from indexer
    Then I should see version
    And I should see hash
    And I should see sender
    And I should see success status
    And I should see timestamp

  @optional
  Scenario: Filter transactions by type
    Given an account with various transaction types
    When I query only user transactions
    Then I should only receive user transactions

  # =============================================================================
  # Collection Queries
  # =============================================================================

  @optional
  Scenario: Get collection by address
    Given a collection address
    When I query the collection
    Then I should receive collection details
    And I should see collection_name
    And I should see creator_address
    And I should see current_supply

  @optional
  Scenario: Get tokens in collection
    Given a collection address
    When I query tokens in the collection
    Then I should receive tokens belonging to that collection

  @optional
  Scenario: Get collection metadata
    Given a collection
    When I query its metadata
    Then I should see uri
    And I should see description

  # =============================================================================
  # Event Queries
  # =============================================================================

  @optional
  Scenario: Query events by type
    Given an indexer client
    And an event type
    When I query events of that type
    Then I should receive matching events

  @optional
  Scenario: Query events by account
    Given an account address
    When I query events involving that account
    Then I should receive relevant events

  @optional
  Scenario: Event data structure
    Given an event query result
    Then each event should have sequence_number
    And each event should have type
    And each event should have data

  # =============================================================================
  # Coin Queries
  # =============================================================================

  @optional
  Scenario: Get coin balances (legacy)
    Given an account with coin balances
    When I query coin balances from indexer
    Then I should receive all coin types and amounts

  @optional
  Scenario: Get coin activities
    Given an account address
    When I query coin activities
    Then I should see deposits and withdrawals

  # =============================================================================
  # Processor Status
  # =============================================================================

  @optional
  Scenario: Check indexer processor status
    Given an indexer client
    When I query processor status
    Then I should see the last processed version
    And I can compare with fullnode ledger version

  @optional
  Scenario: Indexer lag detection
    Given indexer processor status
    And fullnode ledger version
    When I compare versions
    Then I can determine indexer lag

  # =============================================================================
  # Error Handling
  # =============================================================================

  @optional
  Scenario: Handle indexer unavailable
    Given an unreachable indexer endpoint
    When I try to query
    Then I should receive a network error

  @optional
  Scenario: Handle query timeout
    Given a very complex query
    And a short timeout
    When I execute the query
    Then I should receive a timeout error

  @optional
  Scenario: Handle malformed response
    Given an unexpected response format
    When I parse the response
    Then I should receive a parse error with context

