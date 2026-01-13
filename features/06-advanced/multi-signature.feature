@advanced
@optional
Feature: Multi-Signature Accounts
  As an SDK user
  I want to create and use multi-signature accounts
  So that I can require multiple approvals for transactions

  # =============================================================================
  # MultiEd25519 Account Creation
  # =============================================================================
  @optional
  Scenario: Create 2-of-3 multi-sig account
    Given 3 Ed25519 public keys
    And threshold 2
    When I create a MultiEd25519 account
    Then the multi-sig account should be valid
    And threshold should be 2
    And num_keys should be 3

  @optional
  Scenario: Create 1-of-1 multi-sig account
    Given 1 Ed25519 public key
    And threshold 1
    When I create a MultiEd25519 account
    Then the multi-sig account should be valid

  @optional
  Scenario: Create multi-sig with all keys required
    Given 5 Ed25519 public keys
    And threshold 5
    When I create a MultiEd25519 account
    Then the multi-sig account should be valid
    And all 5 signatures should be required

  @optional
  Scenario: Reject threshold of 0
    Given 3 Ed25519 public keys
    And threshold 0
    When I try to create a MultiEd25519 account
    Then it should fail with InvalidThreshold error

  @optional
  Scenario: Reject threshold greater than key count
    Given 3 Ed25519 public keys
    And threshold 4
    When I try to create a MultiEd25519 account
    Then it should fail with InvalidThreshold error

  @optional
  Scenario: Reject empty key list
    Given 0 Ed25519 public keys
    When I try to create a MultiEd25519 account
    Then multi-sig creation should fail with no keys

  # =============================================================================
  # Authentication Key Derivation
  # =============================================================================
  @optional
  Scenario: Multi-sig authentication key derivation
    Given 3 Ed25519 public keys in order
    And threshold 2
    When I derive the authentication key
    Then it should equal SHA3-256(pk1 || pk2 || pk3 || threshold || 0x01)

  @optional
  Scenario: Key order affects authentication key
    Given public keys [A, B, C] and [C, B, A]
    And threshold 2
    When I create multi-sig accounts from each
    Then the addresses should be different

  @optional
  Scenario: Same keys same order produce same address
    Given the same 3 public keys in same order
    And threshold 2
    When I create two multi-sig accounts
    Then the addresses should be identical

  # =============================================================================
  # Signing
  # =============================================================================
  @optional
  Scenario: Sign with enough private keys
    Given a 2-of-3 multi-sig account with 2 private keys
    And a message to sign
    When I sign the message with multi-sig
    Then the multi-sig signature should be valid
    And it should contain 2 signatures

  @optional
  Scenario: Cannot sign without enough keys
    Given a 2-of-3 multi-sig account with only 1 private key
    When I check can_sign()
    Then it should return false

  @optional
  Scenario: Collect signatures from multiple parties
    Given a 2-of-3 multi-sig with public keys only
    And a message to sign
    When party 0 signs and provides their signature
    And party 2 signs and provides their signature
    And I aggregate the signatures
    Then I should have a valid multi-signature

  @optional
  Scenario: Reject duplicate signer indices
    Given a multi-sig signature builder
    When I add signature at index 0
    And I try to add another signature at index 0
    Then it should fail with DuplicateSignerIndex error

  @optional
  Scenario: Reject invalid signer index
    Given a 3-key multi-sig
    When I try to add a signature at index 5
    Then it should fail with InvalidSignerIndex error

  # =============================================================================
  # Multi-Sig Signature Structure
  # =============================================================================
  @optional
  Scenario: Multi-sig signature contains indices
    Given a 2-of-3 multi-sig signature from keys 0 and 2
    When I serialize the signature
    Then it should include the signer bitmap
    And the bitmap should indicate positions 0 and 2

  @optional
  Scenario: Signatures are ordered by index
    Given signatures added in order 2, 0, 1
    When I serialize the multi-signature
    Then signatures should be ordered by index

  # =============================================================================
  # Signing Transactions
  # =============================================================================
  @optional
  Scenario: Sign transaction with multi-sig account
    Given a 2-of-3 multi-sig account with 2 private keys
    And a RawTransaction for multi-sig signing
    When I sign the transaction with multi-sig
    Then I should get a multi-sig SignedTransaction
    And the authenticator should be MultiEd25519 variant

  @optional
  Scenario: Multi-sig transaction authenticator structure
    Given a signed multi-sig transaction
    When I inspect the authenticator
    Then it should contain the multi public key
    And it should contain the multi signature

  # =============================================================================
  # Verification
  # =============================================================================
  @optional
  Scenario: Verify multi-sig signature
    Given a 2-of-3 multi-sig public key
    And a message and valid 2-of-3 signature
    When I verify the multi-sig signature
    Then multi-sig verification should succeed

  @optional
  Scenario: Reject signature with insufficient signers
    Given a 2-of-3 multi-sig public key
    And a signature with only 1 signer
    When I verify the multi-sig signature
    Then multi-sig verification should fail

  @optional
  Scenario: Reject signature with wrong signers
    Given a 2-of-3 multi-sig public key
    And a signature from different keys
    When I verify the multi-sig signature
    Then multi-sig verification should fail

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @optional
  Scenario: Known multi-sig address test vector
    Given public keys from test vectors
    And threshold from test vectors
    When I create a multi-sig account
    Then the address should match expected value from test vectors

  @optional
  Scenario: Known multi-sig signature test vector
    Given a multi-sig account and message from test vectors
    When I sign with the specified keys
    Then the signature should match expected value from test vectors
