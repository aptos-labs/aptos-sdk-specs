@core-types
@required
Feature: BCS Serialization
  As an SDK user
  I want to serialize and deserialize data in BCS format
  So that I can communicate with the Aptos blockchain

  # =============================================================================
  # Boolean Serialization
  # =============================================================================
  @required
  Scenario Outline: Serialize boolean <value>
    Given a boolean value <value>
    When I BCS serialize it
    Then the result should be 1 byte
    And the byte should be <byte>

    Examples:
      | byte | value |
      | 0x00 | false |
      | 0x01 | true  |

  @required
  Scenario Outline: Deserialize boolean
    Given bytes [<byte>]
    When I BCS deserialize as boolean
    Then the result should be <value>

    Examples:
      | byte | value |
      | 0x00 | false |
      | 0x01 | true  |

  # =============================================================================
  # Integer Serialization
  # =============================================================================
  @required
  Scenario Outline: Serialize u8
    Given a u8 value <value>
    When I BCS serialize it
    Then the result should be 1 byte
    And the byte should be <encoded>

    Examples:
      | value | encoded |
      | 0     | 0x00    |
      | 1     | 0x01    |
      | 255   | 0xFF    |

  @required
  Scenario Outline: Serialize u16
    Given a u16 value <value>
    When I BCS serialize it
    Then the result should be 2 bytes in little-endian
    And the bytes should be <encoded>

    Examples:
      | value  | encoded      |
      | 0x00   | [0x00, 0x00] |
      | 0x01   | [0x01, 0x00] |
      | 0xFF   | [0xFF, 0x00] |
      | 0x1234 | [0x34, 0x12] |
      | 65535  | [0xFF, 0xFF] |

  @required
  Scenario Outline: Serialize u32
    Given a u32 value <value>
    When I BCS serialize it
    Then the result should be 4 bytes in little-endian
    And the bytes should be <encoded>

    Examples:
      | value      | encoded                  |
      | 0          | [0x00, 0x00, 0x00, 0x00] |
      | 1          | [0x01, 0x00, 0x00, 0x00] |
      | 0xFF       | [0xFF, 0x00, 0x00, 0x00] |
      | 0x1234     | [0x34, 0x12, 0x00, 0x00] |
      | 0x12345678 | [0x78, 0x56, 0x34, 0x12] |
      | 0xFFFFFFFF | [0xFF, 0xFF, 0xFF, 0xFF] |

  @required
  Scenario Outline: Serialize u64
    Given a u64 value <value>
    When I BCS serialize it
    Then the result should be 8 bytes in little-endian
    And the bytes should be <encoded>

    Examples:
      | value              | encoded                                          |
      | 0                  | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 1                  | [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 0xFF               | [0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 0x1234             | [0x34, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 0x12345678         | [0x78, 0x56, 0x34, 0x12, 0x00, 0x00, 0x00, 0x00] |
      | 0x123456789abcdef0 | [0xf0, 0xde, 0xbc, 0x9a, 0x78, 0x56, 0x34, 0x12] |
      | 0xFFFFFFFFFFFFFFFF | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] |

  @required
  Scenario Outline: Serialize u128
    Given a u128 value <value>
    When I BCS serialize it
    Then the result should be 16 bytes in little-endian
    And the bytes should be <encoded>

    Examples:
      | value                              | encoded                                                                                          |
      | 0                                  | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 1                                  | [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 0xFF                               | [0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 0x000102030405060708090A0B0C0D0E0F | [0x0F, 0x0E, 0x0D, 0x0C, 0x0B, 0x0A, 0x09, 0x08, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00] |

  @required
  Scenario Outline: Serialize u256
    Given a u256 value <value>
    When I BCS serialize it
    Then the result should be 32 bytes in little-endian
    And the bytes should be <encoded>

    Examples:
      | value                                                              | encoded                                                                                                                                                                                          |
      | 0                                                                  | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 1                                                                  | [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
      | 0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F | [0x1F, 0x1E, 0x1D, 0x1C, 0x1B, 0x1A, 0x19, 0x18, 0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10, 0x0F, 0x0E, 0x0D, 0x0C, 0x0B, 0x0A, 0x09, 0x08, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00] |

  # TODO: Ensure better supported by SDKs first
  # @required
  # Scenario Outline: Serialize i8
  #   Given an i8 value <value>
  #   When I BCS serialize it
  #   Then the result should be 1 bytes in little-endian (two's complement)
  #   And the bytes should be <encoded>
  #
  #   Examples:
  #     | value  | encoded        |
  #     | 0      | [0x00]         |
  #     | 1      | [0x01]         |
  #     | -1     | [0xFF]         |
  #     | 127    | [0x7F]         |
  #     | -128   | [0x80]         |
  #
  # @required
  # Scenario Outline: Serialize i16
  #   Given an i16 value <value>
  #   When I BCS serialize it
  #   Then the result should be 2 bytes in little-endian (two's complement)
  #   And the bytes should be <encoded>
  #
  #   Examples:
  #     | value   | encoded                |
  #     | 0       | [0x00, 0x00]           |
  #     | 1       | [0x01, 0x00]           |
  #     | -1      | [0xFF, 0xFF]           |
  #     | 32767   | [0xFF, 0x7F]           |
  #     | -32768  | [0x00, 0x80]           |
  #
  # @required
  # Scenario Outline: Serialize i32
  #   Given an i32 value <value>
  #   When I BCS serialize it
  #   Then the result should be 4 bytes in little-endian (two's complement)
  #   And the bytes should be <encoded>
  #
  #   Examples:
  #     | value         | encoded                          |
  #     | 0             | [0x00, 0x00, 0x00, 0x00]         |
  #     | 1             | [0x01, 0x00, 0x00, 0x00]         |
  #     | -1            | [0xFF, 0xFF, 0xFF, 0xFF]         |
  #     | 2147483647    | [0xFF, 0xFF, 0xFF, 0x7F]         |
  #     | -2147483648   | [0x00, 0x00, 0x00, 0x80]         |
  #
  # @required
  # Scenario Outline: Serialize i64
  #   Given an i64 value <value>
  #   When I BCS serialize it
  #   Then the result should be 8 bytes in little-endian (two's complement)
  #   And the bytes should be <encoded>
  #
  #   Examples:
  #     | value                  | encoded                                                    |
  #     | 0                      | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]          |
  #     | 1                      | [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]          |
  #     | -1                     | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]          |
  #     | 9223372036854775807    | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F]          |
  #     | -9223372036854775808   | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80]          |
  #
  # @required
  # Scenario Outline: Serialize i128
  #   Given an i128 value <value>
  #   When I BCS serialize it
  #   Then the result should be 16 bytes in little-endian (two's complement)
  #   And the bytes should be <encoded>
  #
  #   Examples:
  #     | value    | encoded                                                                                          |
  #     | 0        | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
  #     | 1        | [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
  #     | -1       | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] |
  #     | -170141183460469231731687303715884105727   | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F] |
  #     | 170141183460469231731687303715884105728  | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80] |
  #
  # @required
  # Scenario Outline: Serialize i256
  #   Given an i256 value <value>
  #   When I BCS serialize it
  #   Then the result should be 32 bytes in little-endian (two's complement)
  #   And the bytes should be <encoded>
  #
  #   Examples:
  #     | value    | encoded                                                                                                                                    |
  #     | 0        | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
  #     | 1        | [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] |
  #     | -1       | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] |
  #     | 115792089237316195423570985008687907853269984665640564039457584007913129639935 | [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F] |
  #     | -115792089237316195423570985008687907853269984665640564039457584007913129639936 | [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80] |
  # =============================================================================
  # ULEB128 Encoding
  # =============================================================================
  @required
  Scenario Outline: ULEB128 encode various lengths
    Given a length value <value>
    When I ULEB128 encode it
    Then the result should be <bytes>

    Examples:
      | value | bytes              |
      | 0     | [0x00]             |
      | 1     | [0x01]             |
      | 127   | [0x7f]             |
      | 128   | [0x80, 0x01]       |
      | 255   | [0xff, 0x01]       |
      | 16383 | [0xff, 0x7f]       |
      | 16384 | [0x80, 0x80, 0x01] |

  @required
  Scenario: ULEB128 round-trip
    Given a length value 12345
    When I ULEB128 encode and decode it
    Then the result should equal the original value

  # =============================================================================
  # Bytes/String Serialization
  # =============================================================================
  @required
  Scenario: Serialize empty bytes
    Given an empty byte array
    When I BCS serialize it
    Then the result should be [0x00]

  @required
  Scenario: Serialize short bytes
    Given bytes [0x01, 0x02, 0x03]
    When I BCS serialize it
    Then the first byte should be 0x03 (length)
    And the remaining bytes should be [0x01, 0x02, 0x03]

  @required
  Scenario: Serialize string
    Given a string "hello"
    When I BCS serialize it
    Then the first byte should be 0x05 (length)
    And the remaining bytes should be UTF-8 encoded "hello"

  @required
  Scenario: Serialize empty string
    Given a string ""
    When I BCS serialize it
    Then the result should be [0x00]

  @required
  Scenario: Serialize string with unicode
    Given a string "héllo"
    When I BCS serialize it
    Then the first byte should be 0x06 (UTF-8 byte length)

  # =============================================================================
  # Option Serialization
  # =============================================================================
  @required
  Scenario: Serialize None option
    Given an Option with no value
    When I BCS serialize it
    Then the result should be [0x00]

  @required
  Scenario: Serialize Some option with u64
    Given an Option containing u64 value 42
    When I BCS serialize it
    Then the first byte should be 0x01
    And the remaining 8 bytes should be the u64 value

  # =============================================================================
  # Sequence/Vector Serialization
  # =============================================================================
  @required
  Scenario: Serialize empty vector
    Given an empty vector of u8
    When I BCS serialize it
    Then the result should be [0x00]

  @required
  Scenario: Serialize vector of u8
    Given a vector [1, 2, 3] of u8
    When I BCS serialize it
    Then the first byte should be 0x03 (length)
    And the remaining bytes should be [0x01, 0x02, 0x03]

  @required
  Scenario: Serialize vector of u64
    Given a vector [1, 2] of u64
    When I BCS serialize it
    Then the first byte should be 0x02 (length)
    And the remaining bytes should be two u64 values in little-endian

  @required
  Scenario: Serialize nested vector
    Given a vector [[1, 2], [3, 4]] of vectors of u8
    When I BCS serialize it
    Then the first byte should be 0x02 (outer length)
    And each inner vector should be length-prefixed

  # =============================================================================
  # AccountAddress Serialization
  # =============================================================================
  @required
  Scenario: Serialize AccountAddress
    Given an AccountAddress "0x1"
    When I BCS serialize it
    Then the result should be exactly 32 bytes
    And byte 31 should be 0x01
    And bytes 0-30 should all be 0x00

  @required
  Scenario: Deserialize AccountAddress
    Given 32 bytes with byte 31 = 0x42
    When I BCS deserialize as AccountAddress
    Then the short string should be "0x42"

  # =============================================================================
  # Complex Type Serialization
  # =============================================================================
  @required
  Scenario: Serialize struct with multiple fields
    Given a struct with fields:
      | field  | type    | value |
      | sender | address | 0x1   |
      | amount | u64     | 1000  |
    When I BCS serialize it
    Then the fields should be serialized in order
    And the total length should be 40 bytes (32 + 8)

  # =============================================================================
  # Error Handling
  # =============================================================================
  @required
  Scenario: Fail to deserialize truncated data
    Given bytes [0x01, 0x02] intended for u64
    When I BCS deserialize as u64
    Then the deserialization should fail with an error

  @required
  Scenario: Fail to deserialize invalid boolean
    Given bytes [0x02]
    When I BCS deserialize as boolean
    Then the deserialization should fail with an error

  @required
  Scenario: Fail to deserialize sequence with invalid length
    Given bytes [0xff, 0xff, 0xff, 0xff, 0x0f]
    When I BCS deserialize as vector of u8
    Then the deserialization should fail with an error
