@cryptography
@optional
Feature: BLS12-381 Cryptography
  As an SDK user
  I want to use BLS12-381 signatures
  So that I can use aggregatable signatures for efficiency

  # =============================================================================
  # Key Generation
  # =============================================================================
  @optional
  Scenario: Generate random BLS key pair
    When I generate a random BLS12-381 key pair
    Then the private key should be 32 bytes
    And the public key should be 48 bytes

  @optional
  Scenario: Create key pair from 32-byte seed
    Given a 32-byte seed
    When I create a BLS12-381 key pair from the seed
    Then the key pair should be valid
    And creating again from same seed should produce same key pair

  @optional
  Scenario: Create key pair from hex string
    Given a hex-encoded BLS12-381 private key
    When I create a key pair from hex
    Then the key pair should be valid

  @optional
  Scenario: Reject invalid private key
    Given an invalid BLS private key (e.g., zero)
    When I try to create a key pair
    Then it should fail with an error

  # =============================================================================
  # Key Sizes
  # =============================================================================
  @optional
  Scenario: BLS public key size
    Given a BLS12-381 key pair
    When I get the public key bytes
    Then the size should be 48 bytes

  @optional
  Scenario: BLS signature size
    Given a BLS12-381 signature
    When I get the signature bytes
    Then the size should be 96 bytes

  # =============================================================================
  # Signing
  # =============================================================================
  @optional
  Scenario: Sign a message
    Given a BLS12-381 key pair
    And a message "hello world"
    When I sign the message
    Then the signature should be 96 bytes
    And the signature should be valid

  @optional
  Scenario: Signing is deterministic
    Given a BLS12-381 key pair
    And a message "test"
    When I sign the message twice
    Then both signatures should be identical

  @optional
  Scenario: Different messages produce different signatures
    Given a BLS12-381 key pair
    And messages "msg1" and "msg2"
    When I sign both messages
    Then the signatures should be different

  @optional
  Scenario: Different keys produce different signatures
    Given two different BLS12-381 key pairs
    And the same message
    When both keys sign the message
    Then the signatures should be different

  # =============================================================================
  # Verification
  # =============================================================================
  @optional
  Scenario: Verify valid signature
    Given a BLS12-381 key pair
    And a message and valid signature
    When I verify the signature
    Then verification should succeed

  @optional
  Scenario: Reject signature from wrong key
    Given two BLS12-381 key pairs
    And a message signed by first key
    When I verify with second key's public key
    Then verification should fail

  @optional
  Scenario: Reject signature for wrong message
    Given a BLS signature for "original"
    When I verify against "modified"
    Then verification should fail

  @optional
  Scenario: Reject malformed signature
    Given a malformed 96-byte signature
    When I try to verify
    Then verification should fail

  # =============================================================================
  # Signature Aggregation
  # =============================================================================
  @optional
  Scenario: Aggregate two signatures
    Given two BLS signatures for the same message
    And from two different key pairs
    When I aggregate the signatures
    Then I should get a single 96-byte signature

  @optional
  Scenario: Aggregate multiple signatures
    Given 5 BLS signatures for the same message
    When I aggregate all signatures
    Then I should get a single 96-byte signature

  @optional
  Scenario: Verify aggregated signature
    Given an aggregated signature from N signers
    And the aggregated public key
    And the original message
    When I verify the aggregated signature
    Then verification should succeed

  @optional
  Scenario: Aggregation is deterministic
    Given multiple signatures
    When I aggregate in different orders
    Then the aggregated signatures should be the same

  @optional
  Scenario: Cannot aggregate signatures for different messages
    Given signature1 for "message1"
    And signature2 for "message2"
    When I aggregate them
    Then verification against any single message should fail

  # =============================================================================
  # Public Key Aggregation
  # =============================================================================
  @optional
  Scenario: Aggregate two public keys
    Given two BLS public keys
    When I aggregate them
    Then I should get a single 48-byte public key

  @optional
  Scenario: Aggregate multiple public keys
    Given 5 BLS public keys
    When I aggregate all keys
    Then I should get a single 48-byte public key

  @optional
  Scenario: Aggregated key verification
    Given signatures from 3 signers on same message
    When I aggregate signatures and public keys
    And verify aggregated signature with aggregated public key
    Then verification should succeed

  # =============================================================================
  # Proof of Possession (PoP)
  # =============================================================================
  @optional
  Scenario: Generate proof of possession
    Given a BLS12-381 key pair
    When I generate a proof of possession
    Then the PoP should be 96 bytes

  @optional
  Scenario: Verify valid proof of possession
    Given a BLS public key and its PoP
    When I verify the PoP
    Then verification should succeed

  @optional
  Scenario: Reject invalid proof of possession
    Given a BLS public key
    And a PoP from a different key
    When I verify the PoP
    Then verification should fail

  @optional
  Scenario: PoP prevents rogue key attacks
    Given aggregated public keys with valid PoPs
    When I verify each PoP before aggregation
    Then rogue key attacks are prevented

  # =============================================================================
  # BLS Account
  # =============================================================================
  @optional
  Scenario: Create BLS account
    When I create a BLS12-381 account
    Then the account should have a valid address
    And the signature scheme should include BLS identifier

  @optional
  Scenario: BLS authentication key derivation
    Given a BLS12-381 public key
    When I derive the authentication key
    Then it should use the BLS scheme identifier

  @optional
  Scenario: Sign transaction with BLS account
    Given a BLS12-381 account
    And a RawTransaction
    When I sign the transaction
    Then I should get a SignedTransaction
    And the authenticator should use BLS

  # =============================================================================
  # Error Handling
  # =============================================================================
  @optional
  Scenario: Reject invalid public key bytes
    Given 47 bytes (wrong length)
    When I try to parse as BLS public key
    Then it should fail with invalid key error

  @optional
  Scenario: Reject invalid signature bytes
    Given 95 bytes (wrong length)
    When I try to parse as BLS signature
    Then it should fail with invalid signature error

  @optional
  Scenario: Reject point not on curve
    Given bytes that don't represent a valid curve point
    When I try to parse as BLS public key
    Then it should fail with invalid point error

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @optional
  Scenario: Known BLS key derivation test vector
    Given a known seed from test vectors
    When I derive a BLS key pair
    Then the public key should match expected value

  @optional
  Scenario: Known BLS signing test vector
    Given a known BLS key pair and message from test vectors
    When I sign the message
    Then the signature should match expected value

  @optional
  Scenario: Known BLS aggregation test vector
    Given signatures from test vectors
    When I aggregate them
    Then the result should match expected aggregated signature
