@core-types
@required
Feature: TypeTag Handling
  As an SDK user
  I want to work with Move type representations
  So that I can specify type arguments for generic functions

  # =============================================================================
  # Primitive Type Parsing
  # =============================================================================
  @required
  Scenario Outline: Parse primitive types
    Given a type string "<type_string>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the TypeTag variant should be <variant>

    Examples:
      | type_string | variant |
      | bool        | Bool    |
      | u8          | U8      |
      | u16         | U16     |
      | u32         | U32     |
      | u64         | U64     |
      | u128        | U128    |
      | u256        | U256    |
      | address     | Address |
      | signer      | Signer  |

  @required
  Scenario: Format primitive types
    Given a TypeTag of variant U64
    When I format it as a string
    Then the result should be "u64"

  # =============================================================================
  # Vector Type Parsing
  # =============================================================================
  @required
  Scenario: Parse vector of u8
    Given a type string "vector<u8>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the TypeTag variant should be Vector
    And the inner type should be U8

  @required
  Scenario: Parse nested vector
    Given a type string "vector<vector<u8>>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the TypeTag variant should be Vector
    And the inner type should be a Vector of U8

  @required
  Scenario: Parse vector of struct
    Given a type string "vector<0x1::aptos_coin::AptosCoin>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the TypeTag variant should be Vector
    And the inner type should be a Struct

  @required
  Scenario: Format vector type
    Given a TypeTag of Vector containing U8
    When I format it as a string
    Then the result should be "vector<u8>"

  # =============================================================================
  # Struct Type Parsing
  # =============================================================================
  @required
  Scenario: Parse simple struct type
    Given a type string "0x1::aptos_coin::AptosCoin"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the TypeTag variant should be Struct
    And the struct address should be "0x1"
    And the struct module should be "aptos_coin"
    And the struct name should be "AptosCoin"
    And the struct should have 0 type arguments

  @required
  Scenario: Parse struct with type argument
    Given a type string "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the TypeTag variant should be Struct
    And the struct address should be "0x1"
    And the struct module should be "coin"
    And the struct name should be "CoinStore"
    And the struct should have 1 type argument
    And type argument 0 should be a Struct named "AptosCoin"

  @required
  Scenario: Parse struct with multiple type arguments
    Given a type string "0x1::some_module::Pair<u64, 0x1::aptos_coin::AptosCoin>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the struct should have 2 type arguments
    And type argument 0 should be U64
    And type argument 1 should be a Struct named "AptosCoin"

  @required
  Scenario: Parse struct with full address
    Given a type string "0x0000000000000000000000000000000000000000000000000000000000000001::coin::Coin<0x1::aptos_coin::AptosCoin>"
    When I parse it as a TypeTag
    Then the parsing should succeed
    And the struct address should be "0x1"

  @required
  Scenario: Format struct type without type args
    Given a TypeTag struct with address "0x1", module "aptos_coin", name "AptosCoin"
    When I format it as a string
    Then the result should be "0x1::aptos_coin::AptosCoin"

  @required
  Scenario: Format struct type with type args
    Given a TypeTag for CoinStore of AptosCoin
    When I format it as a string
    Then the result should be "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"

  # =============================================================================
  # Invalid Type Parsing
  # =============================================================================
  @required
  Scenario: Reject empty type string
    Given a type string ""
    When I parse it as a TypeTag
    Then the parsing should fail with a parse error

  @required
  Scenario: Reject unknown primitive
    Given a type string "int"
    When I parse it as a TypeTag
    Then the parsing should fail with a parse error

  @required
  Scenario: Reject malformed vector
    Given a type string "vector<>"
    When I parse it as a TypeTag
    Then the parsing should fail with a parse error

  @required
  Scenario: Reject unclosed vector bracket
    Given a type string "vector<u8"
    When I parse it as a TypeTag
    Then the parsing should fail with a parse error

  @required
  Scenario: Reject invalid struct format
    Given a type string "0x1::module"
    When I parse it as a TypeTag
    Then the parsing should fail with a parse error

  @required
  Scenario: Reject struct with invalid address
    Given a type string "invalid::module::Struct"
    When I parse it as a TypeTag
    Then the parsing should fail with a parse error

  # =============================================================================
  # MoveModuleId
  # =============================================================================
  @required
  Scenario: Parse module ID
    Given a module string "0x1::coin"
    When I parse it as a MoveModuleId
    Then the parsing should succeed
    And the module address should be "0x1"
    And the module name should be "coin"

  @required
  Scenario: Format module ID
    Given a MoveModuleId with address "0x1" and name "aptos_coin"
    When I format it as a string
    Then the result should be "0x1::aptos_coin"

  @required
  Scenario: Reject invalid module ID
    Given a module string "0x1"
    When I parse it as a MoveModuleId
    Then the parsing should fail

  # =============================================================================
  # MoveStructTag
  # =============================================================================
  @required
  Scenario: Create MoveStructTag from components
    Given address "0x1", module "coin", name "CoinStore", and type args [AptosCoin]
    When I create a MoveStructTag
    Then the struct tag should be valid
    And the string representation should be "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"

  # =============================================================================
  # BCS Serialization
  # =============================================================================
  @required
  Scenario: BCS serialize primitive TypeTag
    Given a TypeTag of variant U64
    When I BCS serialize the TypeTag
    Then the first byte should be the U64 variant index

  @required
  Scenario: BCS serialize struct TypeTag
    Given a type string "0x1::aptos_coin::AptosCoin"
    When I parse and BCS serialize the TypeTag
    Then the serialization should succeed
    And the result should be deserializable back to the same TypeTag

  @required
  Scenario: BCS round-trip for complex TypeTag
    Given a type string "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"
    When I parse it as a TypeTag
    And I BCS serialize and deserialize it
    Then the result should equal the original TypeTag
