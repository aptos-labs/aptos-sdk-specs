@transaction-building
@required
Feature: Transaction Signing
  As an SDK user
  I want to sign transactions
  So that I can authorize operations on the blockchain

  # =============================================================================
  # Single Signer - Ed25519
  # =============================================================================
  @required
  Scenario: Sign transaction with Ed25519 account
    Given a valid RawTransaction
    And an Ed25519 account
    When I sign the transaction with the account
    Then I should get a SignedTransaction
    And the authenticator should be Ed25519 variant

  @required
  Scenario: SignedTransaction contains original transaction
    Given a signed transaction
    When I get the raw_transaction
    Then it should equal the original RawTransaction

  @required
  Scenario: SignedTransaction contains valid signature
    Given a RawTransaction
    And an Ed25519 account
    When I sign the transaction
    And I extract the signature from the authenticator
    Then the signature should verify against the signing message

  @required
  Scenario: Ed25519 authenticator contains public key
    Given a signed transaction with Ed25519
    When I get the authenticator
    Then it should contain the signer's public key
    And it should contain the signature

  @required
  Scenario: Signing is deterministic
    Given a RawTransaction
    And an Ed25519 account
    When I sign the transaction twice
    Then both SignedTransactions should be identical

  @required
  Scenario: Different accounts produce different signatures
    Given a RawTransaction
    And two different Ed25519 accounts
    When both accounts sign the transaction
    Then the signatures should be different

  # =============================================================================
  # Single Signer - Secp256k1
  # =============================================================================
  @preferred
  Scenario: Sign transaction with Secp256k1 account
    Given a valid RawTransaction
    And a Secp256k1 account
    When I sign the transaction with the account
    Then I should get a SignedTransaction
    And the authenticator should be Secp256k1Ecdsa variant

  @preferred
  Scenario: Secp256k1 authenticator contains public key
    Given a signed transaction with Secp256k1
    When I get the authenticator
    Then it should contain the signer's public key
    And it should contain the signature

  # =============================================================================
  # SignedTransaction Serialization
  # =============================================================================
  @required
  Scenario: BCS serialize SignedTransaction
    Given a SignedTransaction
    When I call to_bytes()
    Then the serialization should succeed
    And the result should be valid BCS

  @required
  Scenario: SignedTransaction serialization is deterministic
    Given the same SignedTransaction
    When I serialize it twice
    Then both results should be identical

  @required
  Scenario: BCS round-trip for SignedTransaction
    Given a SignedTransaction
    When I serialize and deserialize it
    Then the result should equal the original

  # =============================================================================
  # Transaction Hash
  # =============================================================================
  @required
  Scenario: Compute transaction hash
    Given a SignedTransaction
    When I compute the hash
    Then the result should be 32 bytes

  @required
  Scenario: Transaction hash is deterministic
    Given a SignedTransaction
    When I compute the hash twice
    Then both hashes should be identical

  @required
  Scenario: Different transactions have different hashes
    Given two different SignedTransactions
    When I compute their hashes
    Then the hashes should be different

  @required
  Scenario: Transaction hash uses correct domain separator
    Given a SignedTransaction
    When I compute the hash
    Then it should equal SHA3-256(SHA3-256("APTOS::Transaction") || bcs(SignedTransaction))

  # =============================================================================
  # TransactionAuthenticator
  # =============================================================================
  @required
  Scenario: Ed25519 authenticator structure
    Given an Ed25519 TransactionAuthenticator
    Then it should have a public_key field (32 bytes)
    And it should have a signature field (64 bytes)

  @preferred
  Scenario: Secp256k1 authenticator structure
    Given a Secp256k1 TransactionAuthenticator
    Then it should have a public_key field
    And it should have a signature field

  @required
  Scenario: BCS serialize TransactionAuthenticator
    Given a TransactionAuthenticator
    When I BCS serialize it
    Then the first byte should indicate the variant
    And the remaining bytes should contain the authenticator data

  # =============================================================================
  # Sign Helper Functions
  # =============================================================================
  @required
  Scenario: sign_transaction helper function
    Given a RawTransaction
    And an account implementing Account trait
    When I call sign_transaction(raw_txn, account)
    Then I should get a SignedTransaction

  @required
  Scenario: Account sign_transaction method
    Given an Ed25519 account
    And a RawTransaction
    When I call account.sign_transaction(raw_txn)
    Then I should get a SignedTransaction
    And the sender should match the account address

  # =============================================================================
  # Error Handling
  # =============================================================================
  @required
  Scenario: Signing with wrong sender fails gracefully
    Given a RawTransaction with sender "0x1"
    And an Ed25519 account with address "0x2"
    When I sign the transaction
    Then the signing should succeed (SDK doesn't validate sender match)
    But the transaction will fail on-chain

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @required
  Scenario: Known Ed25519 signing test vector
    Given a RawTransaction and Ed25519 key from test vectors
    When I sign the transaction
    Then the signature should match the expected value from test vectors
    And the transaction hash should match the expected value

  @preferred
  Scenario: Known Secp256k1 signing test vector
    Given a RawTransaction and Secp256k1 key from test vectors
    When I sign the transaction
    Then the signature should match the expected value from test vectors

  @required
  Scenario: Known SignedTransaction serialization test vector
    Given a SignedTransaction from test vectors
    When I serialize it to bytes
    Then the bytes should match the expected value from test vectors
