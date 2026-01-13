@account-management @required
Feature: Authentication Key Handling
  As an SDK user
  I want to derive authentication keys from public keys
  So that I can correctly derive account addresses

  # =============================================================================
  # Ed25519 Authentication Key
  # =============================================================================

  @required
  Scenario: Derive authentication key from Ed25519 public key
    Given an Ed25519 public key
    When I derive the authentication key
    Then the result should be 32 bytes
    And it should equal SHA3-256(public_key_bytes || 0x00)

  @required
  Scenario: Authentication key uses Ed25519 scheme identifier
    Given an Ed25519 public key of 32 bytes
    When I prepare the authentication key input
    Then the input should be 33 bytes
    And the last byte should be 0x00

  @required
  Scenario: Same public key produces same authentication key
    Given an Ed25519 public key
    When I derive the authentication key twice
    Then both results should be identical

  @required
  Scenario: Different public keys produce different authentication keys
    Given two different Ed25519 public keys
    When I derive authentication keys from each
    Then the authentication keys should be different

  # =============================================================================
  # Secp256k1 Authentication Key
  # =============================================================================

  @preferred
  Scenario: Derive authentication key from Secp256k1 public key
    Given a Secp256k1 public key (uncompressed, 65 bytes)
    When I derive the authentication key
    Then the result should be 32 bytes
    And it should equal SHA3-256(public_key_bytes || 0x01)

  @preferred
  Scenario: Secp256k1 uses uncompressed public key
    Given a Secp256k1 key pair
    When I get the public key for authentication key derivation
    Then it should be the uncompressed format (65 bytes)
    And the first byte should be 0x04

  @preferred
  Scenario: Secp256k1 uses scheme identifier 0x01
    Given a Secp256k1 public key
    When I prepare the authentication key input
    Then the last byte should be 0x01

  # =============================================================================
  # Generic Authentication Key Derivation
  # =============================================================================

  @required
  Scenario: Derive authentication key from arbitrary public key and scheme
    Given public key bytes
    And a scheme identifier
    When I derive the authentication key using from_public_key
    Then the result should equal SHA3-256(public_key_bytes || scheme_id)

  @required
  Scenario Outline: Scheme identifiers for different key types
    Given a <key_type> public key
    When I derive the authentication key
    Then the scheme identifier should be <scheme_id>

    Examples:
      | key_type | scheme_id |
      | Ed25519 | 0x00 |
      | Secp256k1 | 0x01 |
      | Secp256r1 | 0x02 |
      | MultiEd25519 | 0x01 |
      | MultiKey | 0x03 |

  # =============================================================================
  # Authentication Key to Address
  # =============================================================================

  @required
  Scenario: Convert authentication key to account address
    Given an authentication key
    When I convert it to an account address
    Then the address bytes should equal the authentication key bytes

  @required
  Scenario: New account address equals authentication key
    Given an Ed25519 account that has never rotated keys
    When I compare the address to the authentication key
    Then they should be equal

  @required
  Scenario: Authentication key from_bytes
    Given 32 random bytes
    When I create an authentication key from the bytes
    Then the authentication key should contain those bytes
    And converting to address should give those same bytes

  # =============================================================================
  # Authentication Key Formatting
  # =============================================================================

  @required
  Scenario: Authentication key as bytes
    Given an authentication key
    When I get it as bytes
    Then I should get a 32-byte array

  @required
  Scenario: Authentication key to hex
    Given an authentication key
    When I format it as hex
    Then the result should be 64 hex characters with 0x prefix

  # =============================================================================
  # Cross-SDK Compatibility
  # =============================================================================

  @required
  Scenario: Known Ed25519 authentication key test vector
    Given Ed25519 public key from test vectors
    When I derive the authentication key
    Then it should match the expected value from test vectors

  @preferred
  Scenario: Known Secp256k1 authentication key test vector
    Given Secp256k1 public key from test vectors
    When I derive the authentication key
    Then it should match the expected value from test vectors

  # =============================================================================
  # Edge Cases
  # =============================================================================

  @required
  Scenario: Reject invalid authentication key length
    Given 31 bytes
    When I try to create an authentication key
    Then it should fail with an invalid length error

  @required
  Scenario: Handle all-zero authentication key
    Given 32 zero bytes
    When I create an authentication key
    Then it should succeed
    And converting to address should give the zero address

