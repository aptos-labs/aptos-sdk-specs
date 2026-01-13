@cryptography @preferred
Feature: Secp256k1 ECDSA Cryptography
  As an SDK user
  I want to use Secp256k1 keys for signing
  So that I can use Ethereum-compatible wallets with Aptos

  # =============================================================================
  # Key Generation
  # =============================================================================

  @preferred
  Scenario: Generate random Secp256k1 key pair
    When I generate a random Secp256k1 key pair
    Then the private key should be 32 bytes
    And the compressed public key should be 33 bytes
    And the uncompressed public key should be 65 bytes

  @preferred
  Scenario: Create key pair from 32-byte private key
    Given a 32-byte private key
    When I create a Secp256k1 key pair from the bytes
    Then the key pair should be valid
    And the public key should be derivable

  @preferred
  Scenario: Create key pair from hex string
    Given a hex-encoded Secp256k1 private key
    When I create a Secp256k1 key pair from hex
    Then the key pair should be valid

  @preferred
  Scenario: Reject invalid private key (zero)
    Given a 32-byte private key of all zeros
    When I try to create a Secp256k1 key pair
    Then it should fail with an invalid private key error

  @preferred
  Scenario: Reject invalid private key (greater than curve order)
    Given a 32-byte value greater than the secp256k1 curve order
    When I try to create a Secp256k1 key pair
    Then it should fail with an invalid private key error

  # =============================================================================
  # Public Key Formats
  # =============================================================================

  @preferred
  Scenario: Get compressed public key
    Given a Secp256k1 key pair
    When I get the compressed public key
    Then the result should be 33 bytes
    And the first byte should be 0x02 or 0x03

  @preferred
  Scenario: Get uncompressed public key
    Given a Secp256k1 key pair
    When I get the uncompressed public key
    Then the result should be 65 bytes
    And the first byte should be 0x04

  @preferred
  Scenario: Compressed and uncompressed represent same key
    Given a Secp256k1 key pair
    When I derive authentication key from compressed public key
    And I derive authentication key from uncompressed public key
    Then the authentication keys should match

  # =============================================================================
  # Signing
  # =============================================================================

  @preferred
  Scenario: Sign a message
    Given a Secp256k1 key pair
    And a message "hello world"
    When I sign the message
    Then the signature should be 64 bytes
    And the signature should be valid for the message

  @preferred
  Scenario: Sign produces deterministic signatures (RFC 6979)
    Given a Secp256k1 key pair
    And a message "test message"
    When I sign the message twice
    Then both signatures should be identical

  @preferred
  Scenario: Sign pre-hashed message
    Given a Secp256k1 key pair
    And a SHA256 hash of a message
    When I sign the pre-hashed message
    Then the signature should be valid

  # =============================================================================
  # Verification
  # =============================================================================

  @preferred
  Scenario: Verify valid signature
    Given a Secp256k1 key pair
    And a message "test message"
    And a signature created by the key pair
    When I verify the signature
    Then verification should succeed

  @preferred
  Scenario: Reject signature from wrong key
    Given two different Secp256k1 key pairs
    And a message signed by the first key
    When I verify with the second key's public key
    Then verification should fail

  @preferred
  Scenario: Reject malformed signature
    Given a Secp256k1 public key
    And a message "test"
    And a signature with invalid bytes
    When I verify the signature
    Then verification should fail

  # =============================================================================
  # Authentication Key Derivation
  # =============================================================================

  @preferred
  Scenario: Derive authentication key from Secp256k1 public key
    Given a Secp256k1 public key (uncompressed)
    When I derive the authentication key
    Then the result should be 32 bytes
    And it should equal SHA3-256(uncompressed_public_key || 0x01)

  @preferred
  Scenario: Authentication key uses scheme identifier 0x01
    Given a Secp256k1 key pair
    When I derive the authentication key
    Then the scheme identifier used should be 0x01

  # =============================================================================
  # Cross-SDK Compatibility
  # =============================================================================

  @preferred
  Scenario: Known test vector - key derivation
    Given a known Secp256k1 private key from test vectors
    When I derive the public key
    Then the compressed public key should match test vectors
    And the uncompressed public key should match test vectors

  @preferred
  Scenario: Known test vector - signing
    Given a known Secp256k1 key pair from test vectors
    And the message from test vectors
    When I sign the message
    Then the signature should match the expected value from test vectors

  @preferred
  Scenario: Known test vector - address derivation
    Given a known Secp256k1 private key from test vectors
    When I derive the account address
    Then the address should match the expected value from test vectors

