@cryptography @optional
Feature: Secp256r1 (P-256) ECDSA Cryptography
  As an SDK user
  I want to use Secp256r1 keys for signing
  So that I can use WebAuthn/Passkey authentication with Aptos

  # =============================================================================
  # Key Generation
  # =============================================================================

  @optional
  Scenario: Generate random Secp256r1 key pair
    When I generate a random Secp256r1 key pair
    Then the private key should be 32 bytes
    And the compressed public key should be 33 bytes
    And the uncompressed public key should be 65 bytes

  @optional
  Scenario: Create key pair from 32-byte private key
    Given a 32-byte private key
    When I create a Secp256r1 key pair from the bytes
    Then the Secp256r1 key pair should be valid
    And the public key should be derivable

  @optional
  Scenario: Create key pair from hex string
    Given a hex-encoded Secp256r1 private key
    When I create a Secp256r1 key pair from hex
    Then the Secp256r1 key pair should be valid

  @optional
  Scenario: Reject invalid private key (zero)
    Given a 32-byte private key of all zeros
    When I try to create a Secp256r1 key pair
    Then it should fail with an invalid private key error

  @optional
  Scenario: Reject invalid private key (greater than curve order)
    Given a 32-byte value greater than the P-256 curve order
    When I try to create a Secp256r1 key pair
    Then it should fail with an invalid private key error

  # =============================================================================
  # Public Key Formats
  # =============================================================================

  @optional
  Scenario: Get compressed public key
    Given a Secp256r1 key pair
    When I get the compressed public key
    Then the Secp256r1 result should be 33 bytes
    And the Secp256r1 first byte should be 0x02 or 0x03

  @optional
  Scenario: Get uncompressed public key
    Given a Secp256r1 key pair
    When I get the Secp256r1 uncompressed public key
    Then the Secp256r1 result should be 65 bytes
    And the Secp256r1 first byte should be 0x04

  @optional
  Scenario: Parse compressed public key
    Given a 33-byte compressed Secp256r1 public key
    When I parse it
    Then I should get a valid Secp256r1 public key

  @optional
  Scenario: Parse uncompressed public key
    Given a 65-byte uncompressed Secp256r1 public key
    When I parse it
    Then I should get a valid Secp256r1 public key

  # =============================================================================
  # Signing
  # =============================================================================

  @optional
  Scenario: Sign a message
    Given a Secp256r1 key pair
    And a message "hello world"
    When I sign the message with Secp256r1
    Then the Secp256r1 signature should be 64 bytes
    And the Secp256r1 signature should be valid for the message

  @optional
  Scenario: Sign produces deterministic signatures (RFC 6979)
    Given a Secp256r1 key pair
    And a message "test message"
    When I sign the Secp256r1 message twice
    Then both Secp256r1 signatures should be identical

  @optional
  Scenario: Sign with SHA-256 pre-hash
    Given a Secp256r1 key pair
    And a message
    When I compute SHA-256 of the message
    And I sign the pre-hashed message
    Then the Secp256r1 pre-hash signature should be valid

  # =============================================================================
  # Verification
  # =============================================================================

  @optional
  Scenario: Verify valid signature
    Given a Secp256r1 key pair
    And a message "test message"
    And a Secp256r1 signature created by the key pair
    When I verify the Secp256r1 signature
    Then Secp256r1 verification should succeed

  @optional
  Scenario: Reject signature from wrong key
    Given two different Secp256r1 key pairs
    And a message signed by the first Secp256r1 key
    When I verify with the second Secp256r1 key's public key
    Then Secp256r1 verification should fail

  @optional
  Scenario: Reject malformed signature
    Given a generated Secp256r1 public key
    And a message "test"
    And a Secp256r1 signature with invalid bytes
    When I verify the Secp256r1 signature
    Then Secp256r1 verification should fail

  # =============================================================================
  # Authentication Key Derivation
  # =============================================================================

  @optional
  Scenario: Derive authentication key from Secp256r1 public key
    Given a Secp256r1 public key (uncompressed)
    When I derive the Secp256r1 authentication key
    Then the result should be 32 bytes
    And it should equal SHA3-256(public_key_bytes || 0x02)

  @optional
  Scenario: Secp256r1 uses scheme identifier 0x02
    Given a Secp256r1 key pair
    When I derive the Secp256r1 authentication key
    Then the scheme identifier used should be 0x02

  @optional
  Scenario: Secp256r1 address differs from Secp256k1
    Given the same 32-byte private key
    When I create Secp256k1 and Secp256r1 accounts
    Then the Secp256r1 and Secp256k1 addresses should be different
    And the difference is due to scheme identifier

  # =============================================================================
  # WebAuthn/Passkey Compatibility
  # =============================================================================

  @optional
  Scenario: Parse WebAuthn public key
    Given a COSE-encoded P-256 public key from WebAuthn
    When I parse it as Secp256r1 public key
    Then I should get a valid public key

  @optional
  Scenario: Verify WebAuthn assertion signature
    Given a WebAuthn assertion signature
    And the authenticator data and client data
    When I verify the signature
    Then verification should work with Secp256r1

  @optional
  Scenario: Signature format compatibility
    Given a Secp256r1 signature in DER format
    When I convert to raw (r,s) format
    Then I should get 64 bytes
    And it should be usable with Aptos

  # =============================================================================
  # Account Operations
  # =============================================================================

  @optional
  Scenario: Create Secp256r1 account
    When I create a Secp256r1 account
    Then the Secp256r1 account should have a valid address
    And the Secp256r1 signature scheme should be "secp256r1_ecdsa"

  @optional
  Scenario: Sign transaction with Secp256r1 account
    Given a Secp256r1 account
    And a RawTransaction for Secp256r1 signing
    When I sign the transaction with Secp256r1
    Then I should get a Secp256r1 SignedTransaction
    And the authenticator should use Secp256r1

  # =============================================================================
  # Test Vectors
  # =============================================================================

  @optional
  Scenario: Known Secp256r1 key derivation test vector
    Given a known Secp256r1 private key from test vectors
    When I derive the Secp256r1 public key
    Then the Secp256r1 compressed public key should match test vectors
    And the Secp256r1 uncompressed public key should match test vectors

  @optional
  Scenario: Known Secp256r1 signing test vector
    Given a known Secp256r1 key pair from test vectors
    And the Secp256r1 message from test vectors
    When I sign the message with Secp256r1
    Then the Secp256r1 signature should match test vectors

  @optional
  Scenario: Known Secp256r1 address test vector
    Given a known Secp256r1 private key from test vectors
    When I derive the account address
    Then the Secp256r1 address should match the expected value from test vectors

