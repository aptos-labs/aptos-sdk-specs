@advanced
@optional
Feature: Keyless Accounts (OIDC Authentication)
  As an SDK user
  I want to use OIDC authentication for accounts
  So that users can authenticate without managing cryptographic keys

  # =============================================================================
  # Ephemeral Key Pair
  # =============================================================================
  @optional
  Scenario: Generate ephemeral key pair
    When I generate an ephemeral key pair with 3600 second expiry
    Then the ephemeral key pair should be valid
    And it should have an expiry timestamp
    And it should have a nonce

  @optional
  Scenario: Ephemeral key pair generates unique nonce
    When I generate two ephemeral key pairs
    Then the nonces should be different

  @optional
  Scenario: Check ephemeral key expiry
    Given an ephemeral key pair with 1 second expiry
    When I wait 2 seconds
    And I check is_expired()
    Then it should return true

  @optional
  Scenario: Fresh ephemeral key is not expired
    Given a freshly generated ephemeral key pair
    When I check is_expired()
    Then it should return false

  @optional
  Scenario: Get ephemeral nonce for OIDC flow
    Given an ephemeral key pair
    When I get the nonce
    Then it should be a valid string for OIDC nonce parameter

  # =============================================================================
  # Keyless Account Creation
  # =============================================================================
  @optional
  Scenario: Create keyless account from JWT
    Given an ephemeral key pair
    And a valid JWT from Google
    And a pepper from the pepper service
    And a ZK proof from the prover service
    When I create a keyless account
    Then the account should be valid
    And it should have an address

  @optional
  Scenario: Keyless account has correct provider
    Given a keyless account from Google JWT
    When I get the provider
    Then it should be Google

  @optional
  Scenario: Keyless account address is deterministic
    Given the same JWT claims and pepper
    When I derive the address twice
    Then both addresses should be identical

  @optional
  Scenario: Different users have different addresses
    Given two JWTs with different user IDs
    And the same pepper service
    When I create keyless accounts for each
    Then the addresses should be different

  # =============================================================================
  # Address Derivation
  # =============================================================================
  @optional
  Scenario: Keyless address derivation formula
    Given issuer "https://accounts.google.com"
    And audience (client_id) "my-app.apps.googleusercontent.com"
    And user ID (sub) "123456789"
    And a pepper value
    When I derive the keyless address
    Then it should equal SHA3-256 of the concatenated hashes with pepper and scheme

  @optional
  Scenario: Different issuers produce different addresses
    Given the same user ID and pepper
    But different issuers (Google vs Apple)
    When I derive addresses for each
    Then the addresses should be different

  @optional
  Scenario: Different audiences produce different addresses
    Given the same issuer and user ID
    But different client_ids (audiences)
    When I derive addresses for each
    Then the addresses should be different

  @optional
  Scenario: Pepper affects address
    Given the same JWT claims
    But different peppers
    When I derive addresses for each
    Then the addresses should be different

  # =============================================================================
  # Signing
  # =============================================================================
  @optional
  Scenario: Sign message with keyless account
    Given a valid keyless account
    And a message to sign
    When I sign the message with an ephemeral key pair
    Then the signature should include the ephemeral signature
    And the signature should include the ZK proof

  @optional
  Scenario: Sign transaction with keyless account
    Given a valid keyless account
    And a RawTransaction
    When I sign the transaction with an ephemeral key pair
    Then I should get a SignedTransaction
    And the authenticator should be Keyless variant

  @optional
  Scenario: Reject signing with expired ephemeral key
    Given a keyless account with expired ephemeral key
    And a message to sign
    When I try to sign the message
    Then it should fail with EphemeralKeyExpired error

  # =============================================================================
  # Proof Management
  # =============================================================================
  @optional
  Scenario: Check if keyless account is valid
    Given a keyless account with valid proof
    When I check is_valid()
    Then it should return true

  @optional
  Scenario: Keyless account with expired proof
    Given a keyless account with expired ZK proof
    When I check is_valid()
    Then it should return false

  @optional
  Scenario: Refresh proof
    Given a keyless account with expiring proof
    And a new JWT
    And the prover service
    When I refresh the proof
    Then the account should have a new valid proof

  # =============================================================================
  # OIDC Providers
  # =============================================================================
  @optional
  Scenario: Google provider configuration
    Given OidcProvider Google
    When I get the issuer
    Then it should be "https://accounts.google.com"

  @optional
  Scenario: Apple provider configuration
    Given OidcProvider Apple
    When I get the issuer
    Then it should be "https://appleid.apple.com"

  @optional
  Scenario: Custom OIDC provider
    Given a custom OIDC issuer URL
    When I create an OidcProvider
    Then it should use that issuer

  # =============================================================================
  # Pepper Service
  # =============================================================================
  @optional
  Scenario: Get pepper for JWT
    Given a valid JWT
    And the pepper service endpoint
    When I request a pepper
    Then I should receive a pepper value

  @optional
  Scenario: Same JWT produces same pepper
    Given the same JWT
    When I request pepper twice
    Then both peppers should be identical

  @optional
  Scenario: Handle pepper service error
    Given an invalid JWT
    When I request a pepper
    Then I should receive PepperServiceError

  # =============================================================================
  # Prover Service
  # =============================================================================
  @optional
  Scenario: Generate ZK proof
    Given a valid JWT
    And an ephemeral key pair
    And a pepper
    And the prover service endpoint
    When I request a ZK proof
    Then I should receive a valid proof

  @optional
  Scenario: Handle prover service error
    Given an invalid ephemeral key
    When I request a ZK proof
    Then I should receive ProofGenerationFailed error

  # =============================================================================
  # Error Cases
  # =============================================================================
  @optional
  Scenario: Reject invalid JWT format
    Given a malformed JWT string
    When I try to create a keyless account
    Then it should fail with InvalidJwt error

  @optional
  Scenario: Reject JWT with wrong nonce
    Given an ephemeral key pair with nonce "ABC"
    And a JWT with nonce "XYZ"
    When I try to create a keyless account
    Then it should fail with an error about nonce mismatch

  @optional
  Scenario: Reject expired JWT
    Given an expired JWT
    When I try to create a keyless account
    Then it should fail with an error

  # =============================================================================
  # Security Considerations
  # =============================================================================
  @optional
  Scenario: Ephemeral key expiry is enforced
    Given an ephemeral key with 1 hour expiry
    When the hour passes
    Then signing attempts should fail

  @optional
  Scenario: Pepper is not exposed in account
    Given a keyless account
    When I inspect the account's public properties
    Then the pepper should not be accessible

  # =============================================================================
  # Test Vectors
  # =============================================================================
  @optional
  Scenario: Known keyless address test vector
    Given JWT claims and pepper from test vectors
    When I derive the address
    Then it should match the expected value from test vectors
