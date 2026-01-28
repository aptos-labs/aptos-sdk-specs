@account-management
@required
Feature: Single-Key Account Management
  As an SDK user
  I want to create and use single-key accounts
  So that I can interact with the Aptos blockchain

  # =============================================================================
  # Ed25519 Account Creation
  # =============================================================================
  @required
  Scenario: Generate random Ed25519 account
    When I generate a random Ed25519 account
    Then the account should have a valid address
    And the account should have a valid public key
    And the address should be 32 bytes

  @required
  Scenario: Generated accounts are unique
    When I generate two random Ed25519 accounts
    Then the addresses should be different
    And the public keys should be different

  @required
  Scenario: Create Ed25519 account from private key bytes
    Given a valid Ed25519 private key (32 bytes)
    When I create an Ed25519 account from the private key
    Then the account should be valid
    And recreating from the same key should produce the same address

  @required
  Scenario: Create Ed25519 account from hex string
    Given a hex-encoded Ed25519 private key "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    When I create an Ed25519 account from hex
    Then the account should be valid

  @required
  Scenario: Create Ed25519 account from hex string without 0x
    Given a hex-encoded Ed25519 private key "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    When I create an Ed25519 account from hex
    Then the account should be valid

  @required
  Scenario: Reject invalid private key length
    Given a byte array of length 31
    When I try to create an Ed25519 account
    Then it should fail with an invalid private key error

  @required
  Scenario: Reject invalid hex string
    Given an invalid hex string "0xGGGG"
    When I try to create an Ed25519 account from hex
    Then it should fail with an error

  # =============================================================================
  # Account Properties
  # =============================================================================
  @required
  Scenario: Get account address
    Given an Ed25519 account
    When I get the address
    Then it should be a valid AccountAddress
    And it should be 32 bytes

  @required
  Scenario: Get account public key
    Given an Ed25519 account
    When I get the public key
    Then it should be 32 bytes

  @required
  Scenario: Get signature scheme
    Given an Ed25519 account
    When I get the signature scheme
    Then it should be "ed25519"

  @required
  Scenario: Get authentication key
    Given an Ed25519 account
    When I get the authentication key
    Then it should be 32 bytes
    And it should equal SHA3-256(public_key || 0x00)

  @required
  Scenario: Address equals authentication key for new accounts
    Given a newly created Ed25519 account
    When I compare address and authentication key
    Then they should be equal

  # =============================================================================
  # Signing
  # =============================================================================
  @required
  Scenario: Sign arbitrary message
    Given an Ed25519 account
    And a message "hello world"
    When I sign the message
    Then the signature should be 64 bytes
    And the signature should verify against the public key

  @required
  Scenario: Sign empty message
    Given an Ed25519 account
    And an empty message
    When I sign the message
    Then it should succeed

  @required
  Scenario: Signing is deterministic
    Given an Ed25519 account
    And a message "test"
    When I sign the message twice
    Then both signatures should be identical

  @required
  Scenario: Different accounts produce different signatures
    Given two different Ed25519 accounts
    And the same message
    When both accounts sign the message
    Then the signatures should be different

  # =============================================================================
  # Secp256k1 Account (Preferred)
  # =============================================================================
  @preferred
  Scenario: Generate random Secp256k1 account
    When I generate a random Secp256k1 account
    Then the account should have a valid address
    And the signature scheme should be "secp256k1_ecdsa"

  @preferred
  Scenario: Create Secp256k1 account from private key
    Given a valid Secp256k1 private key (32 bytes)
    When I create a Secp256k1 account from the private key
    Then the account should be valid

  @preferred
  Scenario: Secp256k1 address differs from Ed25519 for same seed
    Given a 32-byte seed
    When I create an Ed25519 account from the seed
    And I create a Secp256k1 account from the seed
    Then the addresses should be different

  @preferred
  Scenario: Sign with Secp256k1 account
    Given a Secp256k1 account
    And a message "test message"
    When I sign the message
    Then the signature should be valid

  # =============================================================================
  # Account Interface Polymorphism
  # =============================================================================
  @required
  Scenario: Use Ed25519 account through Account interface
    Given an Ed25519 account as Account interface
    When I call address()
    Then it should return the correct address
    When I call sign(message)
    Then it should return a valid signature

  @preferred
  Scenario: Use Secp256k1 account through Account interface
    Given a Secp256k1 account as Account interface
    When I call address()
    Then it should return the correct address
    When I call sign(message)
    Then it should return a valid signature

  @preferred
  Scenario: Store different account types uniformly
    Given an Ed25519 account
    And a Secp256k1 account
    When I store both in a collection of Account references
    Then I should be able to iterate and sign with each

  # =============================================================================
  # AnyAccount Enum
  # =============================================================================
  @preferred
  Scenario: Create AnyAccount from Ed25519
    Given an Ed25519 account
    When I wrap it in AnyAccount
    Then the address should match
    And signing should produce the same signature

  @preferred
  Scenario: Create AnyAccount from Secp256k1
    Given a Secp256k1 account
    When I wrap it in AnyAccount
    Then the address should match
    And the signature scheme should be "secp256k1_ecdsa"

  @preferred
  Scenario: Runtime account type selection
    Given a key type string "ed25519" or "secp256k1"
    And a private key hex string
    When I create an AnyAccount based on the key type
    Then the account should be valid
    And should be usable for signing

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @required
  Scenario: Known Ed25519 account test vector
    Given private key "0x..." from test vectors
    When I create an Ed25519 account
    Then the address should be "0x..." as specified in test vectors
    And the public key should match test vectors

  @preferred
  Scenario: Known Secp256k1 account test vector
    Given private key "0x..." from test vectors
    When I create a Secp256k1 account
    Then the address should be "0x..." as specified in test vectors
