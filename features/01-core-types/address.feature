@core-types @required
Feature: Account Address Handling
  As an SDK user
  I want to parse and format account addresses
  So that I can work with Aptos accounts correctly

  # =============================================================================
  # Address Parsing - Valid Inputs
  # =============================================================================

  @required
  Scenario: Parse hex address with 0x prefix
    Given a hex string "0x1"
    When I parse it as an AccountAddress
    Then the parsing should succeed
    And the address bytes should have length 32
    And byte 31 should equal 1
    And bytes 0-30 should all be 0

  @required
  Scenario: Parse hex address without 0x prefix
    # TODO: This one is debatable, but works in TypeScript for some reason
    Given a hex string "1"
    When I parse it as an AccountAddress
    Then the parsing should succeed
    And the short string should be "0x1"

  @required
  Scenario: Parse full 64-character hex address
    # TODO: Optional 0x in front if it's full length?
    Given a hex string "0x0000000000000000000000000000000000000000000000000000000000000001"
    When I parse it as an AccountAddress
    Then the parsing should succeed
    And the short string should be "0x1"

  @required
  Scenario Outline: Parse various valid address formats
    Given a hex string "<input>"
    When I parse it as an AccountAddress
    Then the parsing should succeed
    And the short string should be "<short>"
    And the full hex should be "<full>"

    Examples:
      | input | short | full |
      | 0x1 | 0x1 | 0x0000000000000000000000000000000000000000000000000000000000000001 |
      | 0x10 | 0x10 | 0x0000000000000000000000000000000000000000000000000000000000000010 |
      | 0xff | 0xff | 0x00000000000000000000000000000000000000000000000000000000000000ff |
      | 0x100 | 0x100 | 0x0000000000000000000000000000000000000000000000000000000000000100 |
      | 0xabcdef | 0xabcdef | 0x0000000000000000000000000000000000000000000000000000000000abcdef |
      | 0x0000000000000000000000000000000000000000000000000000000000abcdef | 0xabcdef | 0x0000000000000000000000000000000000000000000000000000000000abcdef |

  @required
  Scenario: Parse uppercase hex address
    Given a hex string "0xABCDEF"
    When I parse it as an AccountAddress
    Then the parsing should succeed
    And the short string should be "0xabcdef"

  @required
  Scenario: Parse mixed case hex address
    Given a hex string "0xAbCdEf"
    When I parse it as an AccountAddress
    Then the parsing should succeed
    And the short string should be "0xabcdef"

  # =============================================================================
  # Address Parsing - Invalid Inputs
  # =============================================================================

  @required
  Scenario: Reject empty string
    Given a hex string ""
    When I parse it as an AccountAddress
    Then the parsing should fail with an invalid address error

  @required
  Scenario: Reject just 0x prefix
    Given a hex string "0x"
    When I parse it as an AccountAddress
    Then the parsing should fail with an invalid address error

  @required
  Scenario: Reject non-hex characters
    Given a hex string "0xGHIJKL"
    When I parse it as an AccountAddress
    Then the parsing should fail with an invalid hex error

  @required
  Scenario: Reject address too long
    Given a hex string "0x00000000000000000000000000000000000000000000000000000000000000001"
    When I parse it as an AccountAddress
    Then the parsing should fail with an invalid length error

  @required
  Scenario: Reject address with spaces
    Given a hex string "0x1 2 3"
    When I parse it as an AccountAddress
    Then the parsing should fail with an invalid hex error

  # =============================================================================
  # Address Formatting
  # =============================================================================

  @required
  Scenario: Format address to full hex
    Given an AccountAddress with value 1
    When I format it as full hex
    Then the result should be "0x0000000000000000000000000000000000000000000000000000000000000001"

  @required
  Scenario: Format address to short string
    Given an AccountAddress with value 1
    When I format it as short string
    Then the result should be "0x1"

  @required
  Scenario: Format zero address
    Given the ZERO address constant
    When I format it as full hex
    Then the result should be "0x0000000000000000000000000000000000000000000000000000000000000000"
    When I format it as short string
    Then the result should be "0x0"

  @required
  Scenario Outline: Short string format removes only leading zeros
    Given an AccountAddress from hex "<input>"
    When I format it as short string
    Then the result should be "<short>"

    Examples:
      | input | short |
      | 0x0000000000000000000000000000000000000000000000000000000000000010 | 0x10 |
      | 0x0000000000000000000000000000000000000000000000000000000000001000 | 0x1000 |
      | 0x1000000000000000000000000000000000000000000000000000000000000000 | 0x1000000000000000000000000000000000000000000000000000000000000000 |

  # =============================================================================
  # Standard Address Constants
  # =============================================================================

  @required
  Scenario: ZERO address constant
    Given the ZERO address constant
    Then all 32 bytes should be 0
    And the short string should be "0x0"

  @required
  Scenario: ONE address constant (framework)
    Given the ONE address constant
    Then byte 31 should equal 1
    And bytes 0-30 should all be 0
    And the short string should be "0x1"

  @required
  Scenario: THREE address constant (token)
    Given the THREE address constant
    Then byte 31 should equal 3
    And the short string should be "0x3"

  @required
  Scenario: FOUR address constant (objects)
    Given the FOUR address constant
    Then byte 31 should equal 4
    And the short string should be "0x4"

  # =============================================================================
  # Address Comparison
  # =============================================================================

  @required
  Scenario: Addresses parsed from equivalent inputs are equal
    Given an AccountAddress from hex "0x1"
    And another AccountAddress from hex "0x0000000000000000000000000000000000000000000000000000000000000001"
    Then the two addresses should be equal

  @required
  Scenario: Different addresses are not equal
    Given an AccountAddress from hex "0x1"
    And another AccountAddress from hex "0x2"
    Then the two addresses should not be equal

  # =============================================================================
  # BCS Serialization
  # =============================================================================

  @required
  Scenario: BCS serialize address
    Given an AccountAddress from hex "0x1"
    When I BCS serialize the address
    Then the result should be 32 bytes
    And byte 31 should equal 1
    And bytes 0-30 should all be 0

  @required
  Scenario: BCS deserialize address
    Given 32 bytes with value 1 in the last byte
    When I BCS deserialize as AccountAddress
    Then the short string should be "0x1"

  @required
  Scenario: BCS round-trip
    Given an AccountAddress from hex "0xabcdef1234567890"
    When I BCS serialize the address
    And I BCS deserialize the result as AccountAddress
    Then the result should equal the original address

