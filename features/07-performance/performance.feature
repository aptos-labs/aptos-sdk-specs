@performance
@optional
Feature: SDK Performance Benchmarks
  As a developer
  I want to measure SDK performance across common operations
  So that I can choose the best SDK for my use case and identify optimization opportunities

  Background:
    Given a configured Aptos client for devnet

  # =============================================================================
  # REST API Read Performance
  # =============================================================================
  @rest-api
  @read
  Scenario: Benchmark - Get ledger info
    When I measure the time to get ledger info 5 times
    Then I record the average response time as "rest_ledger_info_avg_ms"
    And I record the p95 response time as "rest_ledger_info_p95_ms"
    And I record the requests per second as "rest_ledger_info_rps"

  @rest-api
  @read
  Scenario: Benchmark - Get account info
    Given a known funded account address
    When I measure the time to get account info 20 times
    Then I record the average response time as "rest_account_info_avg_ms"
    And I record the p95 response time as "rest_account_info_p95_ms"
    And I record the requests per second as "rest_account_info_rps"

  @rest-api
  @read
  Scenario: Benchmark - Get account resources
    Given a known funded account address
    When I measure the time to get account resources 20 times
    Then I record the average response time as "rest_account_resources_avg_ms"
    And I record the p95 response time as "rest_account_resources_p95_ms"
    And I record the requests per second as "rest_account_resources_rps"

  @rest-api
  @read
  Scenario: Benchmark - Get transaction by hash
    Given a known transaction hash for benchmarking
    When I measure the time to get transaction by hash 20 times
    Then I record the average response time as "rest_tx_by_hash_avg_ms"
    And I record the p95 response time as "rest_tx_by_hash_p95_ms"
    And I record the requests per second as "rest_tx_by_hash_rps"

  @rest-api
  @read
  Scenario: Benchmark - Get account balance via view function
    Given a known funded account address
    When I measure the time to get account balance 20 times
    Then I record the average response time as "rest_balance_avg_ms"
    And I record the p95 response time as "rest_balance_p95_ms"
    And I record the requests per second as "rest_balance_rps"

  # =============================================================================
  # GraphQL/Indexer Read Performance
  # =============================================================================
  @graphql
  @read
  Scenario: Benchmark - Query account tokens via indexer
    Given a known account with tokens
    When I measure the time to query account tokens 100 times
    Then I record the average response time as "gql_account_tokens_avg_ms"
    And I record the p95 response time as "gql_account_tokens_p95_ms"
    And I record the requests per second as "gql_account_tokens_rps"

  @graphql
  @read
  Scenario: Benchmark - Query account transactions via indexer
    Given a known funded account address
    When I measure the time to query account transactions 100 times
    Then I record the average response time as "gql_account_txs_avg_ms"
    And I record the p95 response time as "gql_account_txs_p95_ms"
    And I record the requests per second as "gql_account_txs_rps"

  @graphql
  @read
  Scenario: Benchmark - Query fungible asset balances via indexer
    Given a known account with fungible assets
    When I measure the time to query fungible asset balances 100 times
    Then I record the average response time as "gql_fa_balances_avg_ms"
    And I record the p95 response time as "gql_fa_balances_p95_ms"
    And I record the requests per second as "gql_fa_balances_rps"

  @graphql
  @read
  Scenario: Benchmark - Query events via indexer
    Given a known account with events
    When I measure the time to query events by account 100 times
    Then I record the average response time as "gql_events_avg_ms"
    And I record the p95 response time as "gql_events_p95_ms"
    And I record the requests per second as "gql_events_rps"

  # =============================================================================
  # Transaction Submission Performance
  # =============================================================================
  @transaction
  @submit
  Scenario: Benchmark - Submit transaction (no wait)
    Given a funded Ed25519 account for benchmarking
    When I measure the time to submit 10 APT transfers without waiting
    Then I record the average submission time as "tx_submit_avg_ms"
    And I record the p95 submission time as "tx_submit_p95_ms"
    And I record the transactions per second as "tx_submit_tps"

  @transaction
  @submit
  Scenario: Benchmark - Build and sign transaction
    Given a funded Ed25519 account for benchmarking
    When I measure the time to build and sign 100 APT transfer transactions
    Then I record the average time as "tx_build_sign_avg_ms"
    And I record the p95 time as "tx_build_sign_p95_ms"
    And I record the operations per second as "tx_build_sign_ops"

  # =============================================================================
  # Transaction Round-Trip Performance
  # =============================================================================
  @transaction
  @round-trip
  Scenario: Benchmark - Submit and wait for transaction
    Given a funded Ed25519 account for benchmarking
    When I measure the time to submit and wait for 10 APT transfers
    Then I record the average round-trip time as "tx_round_trip_avg_ms"
    And I record the p95 round-trip time as "tx_round_trip_p95_ms"
    And I record the minimum round-trip time as "tx_round_trip_min_ms"
    And I record the maximum round-trip time as "tx_round_trip_max_ms"

  @transaction
  @round-trip
  Scenario: Benchmark - Full transaction flow with gas estimation
    Given a funded Ed25519 account for benchmarking
    When I measure the full transaction flow 10 times including:
      | Step              |
      | Build transaction |
      | Simulate for gas  |
      | Sign transaction  |
      | Submit            |
      | Wait for result   |
    Then I record the average total time as "tx_full_flow_avg_ms"
    And I record the breakdown by step

  # =============================================================================
  # Cryptographic Operations Performance
  # =============================================================================
  @crypto
  @local
  Scenario: Benchmark - Ed25519 key generation
    When I measure the time to generate 1000 Ed25519 key pairs
    Then I record the average time as "crypto_ed25519_keygen_avg_us"
    And I record the operations per second as "crypto_ed25519_keygen_ops"

  @crypto
  @local
  Scenario: Benchmark - Ed25519 signing
    Given an Ed25519 key pair for benchmarking
    And a 256-byte message
    When I measure the time to sign the message 1000 times
    Then I record the average time as "crypto_ed25519_sign_avg_us"
    And I record the operations per second as "crypto_ed25519_sign_ops"

  @crypto
  @local
  Scenario: Benchmark - Ed25519 verification
    Given an Ed25519 key pair for benchmarking
    And a signed 256-byte message
    When I measure the time to verify the signature 1000 times
    Then I record the average time as "crypto_ed25519_verify_avg_us"
    And I record the operations per second as "crypto_ed25519_verify_ops"

  @crypto
  @local
  Scenario: Benchmark - BCS serialization of transaction
    Given a sample raw transaction for benchmarking
    When I measure the time to BCS serialize the transaction 1000 times
    Then I record the average time as "bcs_serialize_tx_avg_us"
    And I record the operations per second as "bcs_serialize_tx_ops"

  @crypto
  @local
  Scenario: Benchmark - SHA3-256 hashing
    Given a 256-byte message
    When I measure the time to hash the message 5000 times
    Then I record the average time as "crypto_sha3_256_avg_us"
    And I record the operations per second as "crypto_sha3_256_ops"
