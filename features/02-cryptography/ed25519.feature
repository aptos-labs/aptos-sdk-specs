@cryptography
@required
Feature: Ed25519 Cryptography
  As an SDK user
  I want to use Ed25519 keys for signing
  So that I can authenticate transactions on Aptos

  # =============================================================================
  # Key Generation
  # =============================================================================
  @required
  Scenario: Generate random Ed25519 key pair
    When I generate a random Ed25519 key pair
    Then the private key should be 32 bytes
    And the public key should be 32 bytes
    And the key pair should be valid

  @required
  Scenario: Generate unique key pairs
    When I generate two random Ed25519 key pairs
    Then the private keys should be different
    And the public keys should be different

  @required
  Scenario: Create key pair from 32-byte seed
    Given a 32-byte seed
    When I create an Ed25519 key pair from the seed
    Then the key pair should be valid
    And creating again from the same seed should produce the same key pair

  @required
  Scenario: Create key pair from 64-byte private key
    Given a valid 64-byte Ed25519 private key (seed + public key)
    When I create an Ed25519 key pair from the bytes
    Then the key pair should be valid
    And the public key should match the embedded public key

  @required
  Scenario: Create key pair from hex string
    Given a hex-encoded Ed25519 private key "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    When I create an Ed25519 key pair from hex
    Then the key pair should be valid

  @required
  Scenario: Reject invalid private key length
    Given bytes of length 31
    When I try to create an Ed25519 key pair
    Then it should fail with an invalid private key error

  # =============================================================================
  # Signing
  # =============================================================================
  @required
  Scenario: Sign a message
    Given an Ed25519 key pair
    And a message "hello world"
    When I sign the message
    Then the signature should be 64 bytes
    And the signature should be valid for the message

  @required
  Scenario: Sign empty message
    Given an Ed25519 key pair
    And an empty message
    When I sign the message
    Then the signature should be 64 bytes
    And the signature should be valid

  @required
  Scenario: Sign produces deterministic signatures
    Given an Ed25519 key pair
    And a message "test message"
    When I sign the message twice
    Then both signatures should be identical

  @required
  Scenario: Different messages produce different signatures
    Given an Ed25519 key pair
    And messages "message1" and "message2"
    When I sign both messages
    Then the signatures should be different

  @required
  Scenario: Different keys produce different signatures
    Given two different Ed25519 key pairs
    And a message "same message"
    When both keys sign the message
    Then the signatures should be different

  # =============================================================================
  # Verification
  # =============================================================================
  @required
  Scenario: Verify valid signature
    Given an Ed25519 key pair
    And a message "test message"
    And a signature created by the key pair
    When I verify the signature
    Then verification should succeed

  @required
  Scenario: Reject signature from wrong key
    Given two different Ed25519 key pairs
    And a message signed by the first key
    When I verify with the second key's public key
    Then verification should fail

  @required
  Scenario: Reject signature for wrong message
    Given an Ed25519 key pair
    And a signature for message "original"
    When I verify the signature against message "modified"
    Then verification should fail

  @required
  Scenario: Reject malformed signature
    Given an Ed25519 public key
    And a message "test"
    And a signature with invalid bytes
    When I verify the signature
    Then verification should fail

  @required
  Scenario: Reject truncated signature
    Given an Ed25519 public key
    And a message "test"
    And a signature truncated to 63 bytes
    When I try to verify the signature
    Then it should fail with an invalid signature error

  # =============================================================================
  # Key Export
  # =============================================================================
  @required
  Scenario: Export public key bytes
    Given an Ed25519 key pair
    When I export the public key as bytes
    Then the result should be 32 bytes
    And it should match the original public key

  @required
  Scenario: Export private key bytes
    Given an Ed25519 key pair
    When I export the private key as bytes
    Then the result should be 32 or 64 bytes
    And recreating from the bytes should produce the same key pair

  @required
  Scenario: Export keys as hex
    Given an Ed25519 key pair
    When I export the private key as hex
    Then the result should start with "0x"
    And the hex length should be 66 or 130 characters

  # =============================================================================
  # Authentication Key Derivation
  # =============================================================================
  @required
  Scenario: Derive authentication key from Ed25519 public key
    Given an Ed25519 public key
    When I derive the authentication key
    Then the result should be 32 bytes
    And it should equal SHA3-256(public_key || 0x00)

  @required
  Scenario: Derive account address from authentication key
    Given an Ed25519 key pair
    When I derive the authentication key
    And I convert it to an account address
    Then the address should be 32 bytes
    And it should equal the authentication key bytes

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @required
  Scenario: Known test vector - key derivation
    Given private key hex "0x0000000000000000000000000000000000000000000000000000000000000001"
    When I create an Ed25519 key pair
    Then the public key hex should match the expected value from test vectors
    And the address should match the expected value from test vectors

  @required
  Scenario: Known test vector - signing
    Given a known Ed25519 key pair from test vectors
    And the message from test vectors
    When I sign the message
    Then the signature should match the expected value from test vectors

  # =============================================================================
  # Security Properties (Manual)
  # =============================================================================
  @required
  @manual
  @rust-only
  Scenario: Private key is zeroized on drop
    Given an Ed25519 key pair created in a scope
    When the key pair goes out of scope
    Then the private key memory should be zeroized

  @required
  @manual
  @rust-only
  Scenario: Private key does not appear in debug output
    Given an Ed25519 key pair
    When I format it for debug output
    Then the private key bytes should not appear in the output
