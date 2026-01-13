@transaction-building @required
Feature: Raw Transaction Construction
  As an SDK user
  I want to construct raw transactions
  So that I can prepare transactions for signing

  # =============================================================================
  # RawTransaction Creation
  # =============================================================================

  @required
  Scenario: Create RawTransaction with all fields
    Given a sender address "0x1"
    And a sequence number 0
    And an entry function payload for APT transfer
    And max gas amount 200000
    And gas unit price 100
    And expiration timestamp 1700000000
    And chain ID testnet (2)
    When I create a RawTransaction
    Then the transaction should be valid
    And sender should be "0x1"
    And sequence number should be 0

  @required
  Scenario: RawTransaction fields are accessible
    Given a valid RawTransaction
    When I access the fields
    Then sender() should return the sender address
    And sequence_number() should return the sequence number
    And payload() should return the payload
    And max_gas_amount() should return the max gas
    And gas_unit_price() should return the gas price
    And expiration_timestamp_secs() should return the expiration
    And chain_id() should return the chain ID

  # =============================================================================
  # BCS Serialization
  # =============================================================================

  @required
  Scenario: BCS serialize RawTransaction
    Given a RawTransaction with known values
    When I BCS serialize it
    Then the serialization should succeed
    And the bytes should be deterministic

  @required
  Scenario: BCS serialization field order
    Given a RawTransaction
    When I BCS serialize it
    Then sender should be serialized first (32 bytes)
    And sequence_number should be next (8 bytes)
    And payload should follow
    And max_gas_amount, gas_unit_price, expiration, chain_id should be in order

  @required
  Scenario: BCS round-trip for RawTransaction
    Given a valid RawTransaction
    When I BCS serialize and deserialize it
    Then the result should equal the original

  # =============================================================================
  # Signing Message
  # =============================================================================

  @required
  Scenario: Generate signing message for single signer
    Given a valid RawTransaction
    When I generate the signing message
    Then the message should start with SHA3-256("APTOS::RawTransaction")
    And the message should contain the BCS-serialized transaction

  @required
  Scenario: Signing message is deterministic
    Given a valid RawTransaction
    When I generate the signing message twice
    Then both messages should be identical

  @required
  Scenario: Different transactions have different signing messages
    Given two RawTransactions with different sequence numbers
    When I generate signing messages for both
    Then the messages should be different

  @required
  Scenario: Signing message domain separator
    When I compute SHA3-256 of "APTOS::RawTransaction"
    Then the result should be 32 bytes
    And it should be the prefix of all single-signer signing messages

  # =============================================================================
  # Transaction Builder (Preferred)
  # =============================================================================

  @preferred
  Scenario: Build transaction with builder pattern
    Given a TransactionBuilder
    When I set sender to "0x1"
    And I set sequence number to 5
    And I set payload to an APT transfer
    And I set chain ID to testnet
    And I set expiration from now to 600 seconds
    And I call build()
    Then I should get a valid RawTransaction

  @preferred
  Scenario: Builder uses default gas values
    Given a TransactionBuilder with only required fields
    When I build the transaction
    Then max_gas_amount should be 200000
    And gas_unit_price should be 100

  @preferred
  Scenario: Builder allows custom gas values
    Given a TransactionBuilder
    When I set max_gas_amount to 500000
    And I set gas_unit_price to 200
    And I build with all required fields
    Then the transaction should have the custom values

  @preferred
  Scenario: Builder fails without required fields
    Given a TransactionBuilder
    When I try to build without setting sender
    Then build should fail with MissingSender error

  @preferred
  Scenario: Builder fails without sequence number
    Given a TransactionBuilder with sender set
    When I try to build without sequence number
    Then build should fail with MissingSequenceNumber error

  @preferred
  Scenario: Builder fails without payload
    Given a TransactionBuilder with sender and sequence number
    When I try to build without payload
    Then build should fail with MissingPayload error

  @preferred
  Scenario: Builder fails without chain ID
    Given a TransactionBuilder with sender, sequence, and payload
    When I try to build without chain ID
    Then build should fail with MissingChainId error

  @preferred
  Scenario: expiration_from_now calculates correctly
    Given current time is T
    And a TransactionBuilder
    When I set expiration_from_now to 600 seconds
    And I build the transaction
    Then expiration_timestamp_secs should be approximately T + 600

  # =============================================================================
  # Chain ID Handling
  # =============================================================================

  @required
  Scenario: Transaction with mainnet chain ID
    Given a RawTransaction with chain ID 1 (mainnet)
    When I BCS serialize it
    Then the chain_id byte should be 0x01

  @required
  Scenario: Transaction with testnet chain ID
    Given a RawTransaction with chain ID 2 (testnet)
    When I BCS serialize it
    Then the chain_id byte should be 0x02

  # =============================================================================
  # Test Vectors
  # =============================================================================

  @required
  Scenario: Known transaction serialization test vector
    Given a RawTransaction with values from test vectors
    When I BCS serialize it
    Then the bytes should match the expected value from test vectors

  @required
  Scenario: Known signing message test vector
    Given a RawTransaction from test vectors
    When I generate the signing message
    Then it should match the expected value from test vectors

