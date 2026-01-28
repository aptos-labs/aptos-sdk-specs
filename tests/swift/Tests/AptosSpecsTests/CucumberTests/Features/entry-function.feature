@transaction-building
@required
Feature: Entry Function Payload
  As an SDK user
  I want to construct entry function payloads
  So that I can call Move functions on-chain

  # =============================================================================
  # EntryFunction Creation
  # =============================================================================
  @required
  Scenario: Create EntryFunction with all components
    Given module ID "0x1::aptos_account"
    And function name "transfer"
    And no type arguments
    And arguments [recipient_address, amount]
    When I create an EntryFunction
    Then the payload should be valid
    And module should be "0x1::aptos_account"
    And function should be "transfer"

  @required
  Scenario: Create EntryFunction with type arguments
    Given module ID "0x1::coin"
    And function name "transfer"
    And type argument "0x1::aptos_coin::AptosCoin"
    And arguments [recipient_address, amount]
    When I create an EntryFunction
    Then the payload should have 1 type argument

  @required
  Scenario: Create EntryFunction with multiple type arguments
    Given module ID "0x1::some_module"
    And function name "swap"
    And type arguments ["0x1::coin_a::CoinA", "0x1::coin_b::CoinB"]
    When I create an EntryFunction
    Then the payload should have 2 type arguments

  # =============================================================================
  # APT Transfer
  # =============================================================================
  @required
  Scenario: Create APT transfer entry function
    Given recipient address "0xabc123..."
    And amount 1000000 (0.01 APT in octas)
    When I create an APT transfer entry function
    Then the module should be "0x1::aptos_account"
    And the function should be "transfer"
    And there should be 0 type arguments
    And there should be 2 arguments

  @required
  Scenario: APT transfer arguments are correctly encoded
    Given recipient address "0x1"
    And amount 1000000
    When I create an APT transfer entry function
    Then argument 0 should be BCS-encoded address (32 bytes)
    And argument 1 should be BCS-encoded u64 (8 bytes)

  @required
  Scenario: APT transfer uses aptos_account module
    When I create any APT transfer
    Then the module address should be "0x1"
    And the module name should be "aptos_account"
    And the function name should be "transfer"

  # =============================================================================
  # Coin Transfer
  # =============================================================================
  @required
  Scenario: Create coin transfer with type argument
    Given coin type "0x1::aptos_coin::AptosCoin"
    And recipient address "0xabc"
    And amount 500000
    When I create a coin transfer entry function
    Then the module should be "0x1::coin"
    And the function should be "transfer"
    And type argument 0 should be "0x1::aptos_coin::AptosCoin"

  @required
  Scenario: Coin transfer vs APT transfer produce different payloads
    Given the same recipient and amount
    When I create an APT transfer
    And I create a coin transfer for AptosCoin
    Then the payloads should be different in structure
    And APT transfer should use aptos_account module
    And coin transfer should use coin module

  # =============================================================================
  # Argument Encoding
  # =============================================================================
  @required
  Scenario: Encode address argument
    Given an AccountAddress "0x1"
    When I BCS encode it as an entry function argument
    Then the result should be 32 bytes

  @required
  Scenario: Encode u64 argument
    Given a u64 value 1000000
    When I BCS encode it as an entry function argument
    Then the result should be 8 bytes in little-endian

  @required
  Scenario: Encode bool argument
    Given a bool value true
    When I BCS encode it as an entry function argument
    Then the result should be 1 byte (0x01)

  @required
  Scenario: Encode vector<u8> argument
    Given bytes [1, 2, 3, 4, 5]
    When I BCS encode it as an entry function argument
    Then the result should be ULEB128 length + bytes

  @required
  Scenario: Encode string argument
    Given a string "hello"
    When I BCS encode it as an entry function argument
    Then the result should be ULEB128 length + UTF-8 bytes

  @required
  Scenario: Encode u128 argument
    Given a u128 value
    When I BCS encode it as an entry function argument
    Then the result should be 16 bytes in little-endian

  # =============================================================================
  # BCS Serialization
  # =============================================================================
  @required
  Scenario: BCS serialize EntryFunction
    Given an EntryFunction for APT transfer
    When I BCS serialize it
    Then the serialization should succeed
    And the result should include module ID, function name, type args, and args

  @required
  Scenario: EntryFunction serialization is deterministic
    Given the same EntryFunction created twice
    When I BCS serialize both
    Then the bytes should be identical

  @required
  Scenario: BCS round-trip for EntryFunction
    Given an EntryFunction with type arguments and arguments
    When I BCS serialize and deserialize it
    Then the result should equal the original

  # =============================================================================
  # TransactionPayload Wrapping
  # =============================================================================
  @required
  Scenario: Wrap EntryFunction in TransactionPayload
    Given an EntryFunction
    When I convert it to TransactionPayload
    Then the payload variant should be EntryFunction

  @required
  Scenario: TransactionPayload BCS serialization includes variant
    Given a TransactionPayload containing an EntryFunction
    When I BCS serialize it
    Then the first byte should indicate EntryFunction variant

  # =============================================================================
  # Edge Cases
  # =============================================================================
  @required
  Scenario: EntryFunction with empty type args
    Given an EntryFunction with no type arguments
    When I BCS serialize it
    Then type_args should serialize as empty vector (0x00)

  @required
  Scenario: EntryFunction with empty args
    Given an EntryFunction with no arguments (e.g., initialize)
    When I BCS serialize it
    Then args should serialize as empty vector (0x00)

  @required
  Scenario: EntryFunction with large u256 argument
    Given a u256 value near max
    When I encode it as an entry function argument
    Then the encoding should succeed
    And the result should be 32 bytes

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @required
  Scenario: Known APT transfer test vector
    Given recipient and amount from test vectors
    When I create an APT transfer entry function
    And I BCS serialize it
    Then the bytes should match the expected value from test vectors

  @required
  Scenario: Known coin transfer test vector
    Given coin type, recipient, and amount from test vectors
    When I create a coin transfer entry function
    And I BCS serialize it
    Then the bytes should match the expected value from test vectors
