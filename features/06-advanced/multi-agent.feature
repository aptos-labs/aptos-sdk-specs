@advanced @optional
Feature: Multi-Agent Transactions
  As an SDK user
  I want to create transactions with multiple signers
  So that I can execute atomic multi-party operations

  # =============================================================================
  # Multi-Agent Transaction Creation
  # =============================================================================

  @optional
  Scenario: Create multi-agent transaction with one secondary signer
    Given a sender account
    And a secondary signer account
    And a RawTransaction
    When I create a multi-agent transaction
    Then the transaction should include both signers

  @optional
  Scenario: Create multi-agent transaction with multiple secondary signers
    Given a sender account
    And 3 secondary signer accounts
    And a RawTransaction
    When I create a multi-agent transaction
    Then the transaction should include all 4 signers

  @optional
  Scenario: Secondary signer addresses are preserved
    Given secondary signer addresses [A, B, C]
    When I build a multi-agent transaction
    Then the secondary_signer_addresses should be [A, B, C] in order

  # =============================================================================
  # Multi-Agent Signing Message
  # =============================================================================

  @optional
  Scenario: Multi-agent signing message differs from single signer
    Given the same RawTransaction
    When I generate single-signer signing message
    And I generate multi-agent signing message with secondary signers
    Then the single and multi-agent messages should be different

  @optional
  Scenario: Multi-agent signing message includes secondary addresses
    Given a RawTransaction
    And secondary signer addresses
    When I generate the multi-agent signing message
    Then it should include the raw transaction
    And it should include the secondary signer addresses

  @optional
  Scenario: Multi-agent signing message uses correct domain
    Given a multi-agent transaction
    When I generate the signing message
    Then it should start with SHA3-256("APTOS::RawTransactionWithData")

  @optional
  Scenario: All parties sign the same message
    Given a multi-agent transaction with sender and 2 secondary signers
    When each party generates their signing message
    Then all 3 messages should be identical

  # =============================================================================
  # Multi-Agent Signing
  # =============================================================================

  @optional
  Scenario: Sign multi-agent transaction
    Given a RawTransaction
    And sender account
    And 2 secondary signer accounts
    When I sign the multi-agent transaction with all parties
    Then I should get a SignedTransaction
    And the authenticator should be MultiAgent variant

  @optional
  Scenario: Multi-agent authenticator structure
    Given a signed multi-agent transaction
    When I inspect the authenticator
    Then it should contain sender authenticator
    And it should contain secondary_signer_addresses
    And it should contain secondary_signers list

  @optional
  Scenario: Multi-agent with mixed account types
    Given an Ed25519 sender
    And a Secp256k1 secondary signer
    And a RawTransaction
    When I sign the multi-agent transaction
    Then multi-agent signing should succeed
    And sender authenticator should be Ed25519
    And secondary authenticator should be Secp256k1

  # =============================================================================
  # Partial Signing Workflow
  # =============================================================================

  @optional
  Scenario: Collect signatures from multiple parties
    Given a RawTransaction for multi-agent
    And secondary signer addresses
    When sender signs their portion
    And secondary signer 1 signs their portion
    And secondary signer 2 signs their portion
    And I combine all signatures
    Then I should have a complete multi-agent authenticator

  @optional
  Scenario: Signatures can be collected in any order
    Given a multi-agent transaction
    When secondary signer 2 signs first
    And sender signs second
    And secondary signer 1 signs last
    And I combine in correct order
    Then the transaction should be valid

  @optional
  Scenario: Reject incomplete signature collection
    Given a multi-agent transaction with 2 secondary signers
    When sender signs
    And only 1 secondary signer signs
    And I try to submit
    Then submission should fail

  # =============================================================================
  # Error Cases
  # =============================================================================

  @optional
  Scenario: Reject mismatched secondary signer count
    Given 3 secondary signer addresses
    And only 2 secondary signatures
    When I try to create the authenticator
    Then it should fail with an error

  @optional
  Scenario: Reject empty secondary signers
    Given a multi-agent transaction with no secondary signers
    When I try to create multi-agent authenticator
    Then it should fail or produce single-signer transaction

  @optional
  Scenario: Secondary signer address must match signature
    Given secondary signer address A
    And signature from account B
    When I submit the transaction
    Then on-chain validation should fail

  # =============================================================================
  # BCS Serialization
  # =============================================================================

  @optional
  Scenario: Serialize multi-agent authenticator
    Given a multi-agent authenticator
    When I BCS serialize it
    Then the variant indicator should be MultiAgent
    And sender authenticator should be serialized
    And secondary addresses should be serialized as vector
    And secondary signers should be serialized as vector

  @optional
  Scenario: Multi-agent transaction serialization is deterministic
    Given the same multi-agent transaction
    When I serialize it twice
    Then both serializations should be identical

  # =============================================================================
  # Test Vectors
  # =============================================================================

  @optional
  Scenario: Known multi-agent signing message test vector
    Given a RawTransaction and secondary addresses from test vectors
    When I generate the multi-agent signing message
    Then the multi-agent message should match test vectors

  @optional
  Scenario: Known multi-agent transaction test vector
    Given a multi-agent transaction from test vectors
    When I serialize it
    Then the bytes should match expected value from test vectors

