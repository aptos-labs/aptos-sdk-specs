@advanced @optional
Feature: Fee Payer (Sponsored) Transactions
  As an SDK user
  I want to create sponsored transactions
  So that a third party can pay gas fees on behalf of users

  # =============================================================================
  # Fee Payer Transaction Creation
  # =============================================================================

  @optional
  Scenario: Create fee payer transaction with sponsor
    Given a sender account
    And a fee payer (sponsor) account
    And a RawTransaction
    When I create a fee payer transaction
    Then the transaction should have the fee payer designated

  @optional
  Scenario: Create fee payer transaction with secondary signers
    Given a sender account
    And secondary signer accounts
    And a fee payer account
    And a RawTransaction
    When I create a fee payer transaction
    Then it should include all signers plus fee payer

  @optional
  Scenario: Fee payer address is preserved
    Given fee payer address "0xSPONSOR"
    When I build a fee payer transaction
    Then fee_payer_address should be "0xSPONSOR"

  # =============================================================================
  # Fee Payer Signing Message
  # =============================================================================

  @optional
  Scenario: Fee payer signing message differs from multi-agent
    Given the same RawTransaction and secondary signers
    When I generate multi-agent signing message
    And I generate fee payer signing message with sponsor
    Then the messages should be different

  @optional
  Scenario: Fee payer signing message includes fee payer address
    Given a RawTransaction
    And a fee payer address
    When I generate the fee payer signing message
    Then it should include the raw transaction
    And it should include secondary signer addresses
    And it should include the fee payer address

  @optional
  Scenario: Fee payer signing message uses correct domain
    Given a fee payer transaction
    When I generate the fee payer signing message
    Then it should start with SHA3-256("APTOS::RawTransactionWithData")

  @optional
  Scenario: All parties (including fee payer) sign the same message
    Given a fee payer transaction with sender, secondary, and sponsor
    When each party generates their signing message
    Then all messages should be identical

  # =============================================================================
  # Fee Payer Signing
  # =============================================================================

  @optional
  Scenario: Sign fee payer transaction
    Given a RawTransaction
    And sender account
    And fee payer account
    When I sign the fee payer transaction with both parties
    Then I should get a SignedTransaction
    And the authenticator should be FeePayer variant

  @optional
  Scenario: Fee payer authenticator structure
    Given a signed fee payer transaction
    When I inspect the authenticator
    Then it should contain sender authenticator
    And it should contain secondary_signer_addresses (may be empty)
    And it should contain secondary_signers (may be empty)
    And it should contain fee_payer_address
    And it should contain fee_payer_signer authenticator

  @optional
  Scenario: Fee payer with no secondary signers
    Given a sender account
    And a fee payer account
    And no secondary signers
    When I sign the fee payer transaction
    Then secondary_signer_addresses should be empty
    And secondary_signers should be empty
    And fee payer should be present

  @optional
  Scenario: Fee payer with mixed account types
    Given an Ed25519 sender
    And a Secp256k1 fee payer
    When I sign the fee payer transaction
    Then it should succeed
    And both authenticators should be correct types

  # =============================================================================
  # Sponsored Transaction Workflow
  # =============================================================================

  @optional
  Scenario: Sender initiates sponsored transaction
    Given a sender who wants sponsored transaction
    When sender creates RawTransaction
    And sender signs the fee payer signing message
    Then sender can send partially signed tx to sponsor

  @optional
  Scenario: Sponsor completes sponsored transaction
    Given a partially signed fee payer transaction from sender
    When sponsor reviews the transaction
    And sponsor signs the fee payer signing message
    And sponsor combines signatures into authenticator
    Then the transaction is ready for submission

  @optional
  Scenario: Signatures can be collected in any order
    Given a fee payer transaction
    When sponsor signs first
    And sender signs second
    And I combine correctly
    Then the fee payer transaction should be valid

  # =============================================================================
  # Gas Configuration
  # =============================================================================

  @optional
  Scenario: Fee payer pays gas regardless of sender gas fields
    Given sender creates transaction with max_gas_amount=100
    And fee payer has sufficient balance
    When transaction is submitted
    Then fee payer's balance is deducted for gas
    And sender's balance is not deducted for gas

  @optional
  Scenario: Transaction fails if fee payer has insufficient gas
    Given sender creates valid transaction
    And fee payer has zero balance
    When transaction is submitted
    Then it should fail due to fee payer insufficient balance

  # =============================================================================
  # Error Cases
  # =============================================================================

  @optional
  Scenario: Reject missing fee payer signature
    Given a fee payer transaction
    When sender signs
    But fee payer does not sign
    And I try to create the authenticator
    Then it should fail with missing fee payer error

  @optional
  Scenario: Reject missing sender signature
    Given a fee payer transaction
    When fee payer signs
    But sender does not sign
    And I try to create the authenticator
    Then it should fail with missing sender error

  @optional
  Scenario: Fee payer address must match signature
    Given fee payer address A
    And signature from account B
    When I submit the transaction
    Then on-chain validation should fail

  # =============================================================================
  # BCS Serialization
  # =============================================================================

  @optional
  Scenario: Serialize fee payer authenticator
    Given a fee payer authenticator
    When I BCS serialize it
    Then the variant indicator should be FeePayer
    And all components should be serialized in order

  @optional
  Scenario: Fee payer transaction serialization is deterministic
    Given the same fee payer transaction
    When I serialize it twice
    Then both serializations should be identical

  # =============================================================================
  # Test Vectors
  # =============================================================================

  @optional
  Scenario: Known fee payer signing message test vector
    Given a RawTransaction and fee payer address from test vectors
    When I generate the signing message
    Then it should match the expected value from test vectors

  @optional
  Scenario: Known fee payer transaction test vector
    Given a fee payer transaction from test vectors
    When I serialize it
    Then the bytes should match expected value from test vectors

