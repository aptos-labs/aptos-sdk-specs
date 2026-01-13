@cryptography @required
Feature: Hashing Functions
  As an SDK user
  I want to compute cryptographic hashes
  So that I can verify data integrity and derive keys

  # =============================================================================
  # SHA3-256
  # =============================================================================

  @required
  Scenario: Compute SHA3-256 of empty data
    Given empty bytes
    When I compute SHA3-256
    Then the result should be 32 bytes
    And the hex should be "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"

  @required
  Scenario: Compute SHA3-256 of "hello"
    Given bytes for string "hello"
    When I compute SHA3-256
    Then the hex should be "3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392"

  @required
  Scenario: SHA3-256 produces different hashes for different inputs
    Given bytes for "input1" and "input2"
    When I compute SHA3-256 for both
    Then the hashes should be different

  @required
  Scenario: SHA3-256 is deterministic
    Given bytes for string "test data"
    When I compute SHA3-256 twice
    Then both results should be identical

  @required
  Scenario: Compute SHA3-256 of multiple parts
    Given bytes ["hello", " ", "world"]
    When I compute SHA3-256 of all parts concatenated
    Then the result should equal SHA3-256 of "hello world"

  # =============================================================================
  # SHA2-256
  # =============================================================================

  @required
  Scenario: Compute SHA2-256 of empty data
    Given empty bytes
    When I compute SHA2-256
    Then the result should be 32 bytes
    And the hex should be "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

  @required
  Scenario: Compute SHA2-256 of "hello"
    Given bytes for string "hello"
    When I compute SHA2-256
    Then the hex should be "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

  @required
  Scenario: SHA2-256 differs from SHA3-256
    Given bytes for string "test"
    When I compute both SHA2-256 and SHA3-256
    Then the results should be different

  # =============================================================================
  # Domain-Separated Hashing
  # =============================================================================

  @required
  Scenario: Domain-separated hash for RawTransaction
    Given the domain string "APTOS::RawTransaction"
    And transaction data bytes
    When I compute domain-separated hash
    Then the result should be SHA3-256(SHA3-256(domain) || data)

  @required
  Scenario: Different domains produce different hashes
    Given the same data bytes
    And domains "APTOS::RawTransaction" and "APTOS::SignedTransaction"
    When I compute domain-separated hashes
    Then the results should be different

  @required
  Scenario: Domain hash prefix is computed correctly
    Given the domain string "APTOS::RawTransaction"
    When I compute the domain prefix
    Then the result should be SHA3-256 of the domain string bytes

  @required
  Scenario Outline: Known domain prefixes
    Given the domain string "<domain>"
    When I compute SHA3-256 of the domain
    Then the first 4 bytes should be "<prefix>"

    Examples:
      | domain | prefix |
      | APTOS::RawTransaction | known_prefix_1 |
      | APTOS::RawTransactionWithData | known_prefix_2 |

  # =============================================================================
  # HashValue Type
  # =============================================================================

  @required
  Scenario: Create HashValue from bytes
    Given 32 random bytes
    When I create a HashValue from the bytes
    Then the hash value should contain those bytes

  @required
  Scenario: Create HashValue from hex
    Given a 64-character hex string
    When I create a HashValue from hex
    Then the parsing should succeed

  @required
  Scenario: Reject invalid HashValue length
    Given 31 bytes
    When I try to create a HashValue
    Then it should fail with an invalid length error

  @required
  Scenario: HashValue ZERO constant
    Given the HashValue ZERO constant
    Then all 32 bytes should be zero

  @required
  Scenario: Format HashValue as hex
    Given a HashValue from known bytes
    When I format it as hex
    Then the result should start with "0x"
    And the hex length should be 66 characters

  @required
  Scenario: HashValue equality
    Given two HashValues from the same bytes
    Then they should be equal

  @required
  Scenario: HashValue from SHA3-256
    Given bytes for string "test"
    When I compute HashValue using sha3_256_of
    Then the result should equal a HashValue created from the expected hash

  # =============================================================================
  # HMAC-SHA512 (for BIP-39)
  # =============================================================================

  @preferred
  Scenario: Compute HMAC-SHA512 for BIP-39 seed derivation
    Given a mnemonic entropy and passphrase
    When I compute HMAC-SHA512 with key "mnemonic" + passphrase
    Then the result should be 64 bytes

  # =============================================================================
  # Performance Characteristics
  # =============================================================================

  @required
  Scenario: Hashing large data
    Given 1 megabyte of random data
    When I compute SHA3-256
    Then the operation should complete successfully
    And the result should be 32 bytes

