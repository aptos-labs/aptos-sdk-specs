@account-management @preferred
Feature: Mnemonic-Based Key Derivation
  As an SDK user
  I want to derive accounts from mnemonic phrases
  So that I can backup and restore my accounts

  # =============================================================================
  # Mnemonic Generation
  # =============================================================================

  @preferred
  Scenario: Generate 12-word mnemonic
    When I generate a mnemonic with 12 words
    Then the phrase should contain exactly 12 words
    And the phrase should be valid BIP-39

  @preferred
  Scenario: Generate 24-word mnemonic
    When I generate a mnemonic with 24 words
    Then the phrase should contain exactly 24 words
    And the phrase should be valid BIP-39

  @preferred
  Scenario Outline: Generate mnemonic with various word counts
    When I generate a mnemonic with <words> words
    Then the phrase should contain exactly <words> words
    And the phrase should be valid BIP-39

    Examples:
      | words |
      | 12    |
      | 15    |
      | 18    |
      | 21    |
      | 24    |

  @preferred
  Scenario: Generated mnemonics are unique
    When I generate two 12-word mnemonics
    Then the phrases should be different

  @preferred
  Scenario: Mnemonic words are from BIP-39 wordlist
    When I generate a 12-word mnemonic
    Then all words should be in the BIP-39 English wordlist

  # =============================================================================
  # Mnemonic Parsing
  # =============================================================================

  @preferred
  Scenario: Parse valid mnemonic phrase
    Given the mnemonic phrase "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    When I parse the mnemonic
    Then the parsing should succeed

  @preferred
  Scenario: Mnemonic parsing is case-insensitive
    Given the mnemonic phrase "ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABOUT"
    When I parse the mnemonic
    Then the parsing should succeed

  @preferred
  Scenario: Reject invalid mnemonic word
    Given the mnemonic phrase "invalid word abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    When I parse the mnemonic
    Then the parsing should fail with an invalid mnemonic error

  @preferred
  Scenario: Reject mnemonic with wrong word count
    Given a mnemonic phrase with 11 words
    When I parse the mnemonic
    Then the parsing should fail with an invalid mnemonic error

  @preferred
  Scenario: Reject mnemonic with invalid checksum
    Given a mnemonic phrase with valid words but wrong checksum
    When I parse the mnemonic
    Then the parsing should fail with an invalid mnemonic error

  # =============================================================================
  # Ed25519 Account Derivation
  # =============================================================================

  @preferred
  Scenario: Derive Ed25519 account from mnemonic with default path
    Given a valid mnemonic phrase
    When I derive an Ed25519 account from the mnemonic
    Then the account should be valid
    And the derivation path used should be "m/44'/637'/0'/0'/0'"

  @preferred
  Scenario: Derive Ed25519 account with custom path
    Given a valid mnemonic phrase
    And derivation path "m/44'/637'/0'/0'/5'"
    When I derive an Ed25519 account with the custom path
    Then the account should be valid
    And the address should differ from default path

  @preferred
  Scenario: Same mnemonic produces same account
    Given a valid mnemonic phrase
    When I derive an Ed25519 account twice
    Then both accounts should have the same address

  @preferred
  Scenario: Different mnemonics produce different accounts
    Given two different mnemonic phrases
    When I derive Ed25519 accounts from each
    Then the addresses should be different

  @preferred
  Scenario: Different paths produce different accounts
    Given a valid mnemonic phrase
    When I derive accounts at paths "m/44'/637'/0'/0'/0'" and "m/44'/637'/0'/0'/1'"
    Then the addresses should be different

  @preferred
  Scenario: Derive multiple accounts from one mnemonic
    Given a valid mnemonic phrase
    When I derive accounts at indices 0, 1, 2, 3, 4
    Then I should have 5 different accounts
    And all addresses should be unique

  # =============================================================================
  # Secp256k1 Account Derivation
  # =============================================================================

  @preferred
  Scenario: Derive Secp256k1 account from mnemonic
    Given a valid mnemonic phrase
    When I derive a Secp256k1 account from the mnemonic
    Then the account should be valid
    And the signature scheme should be "secp256k1_ecdsa"

  @preferred
  Scenario: Ed25519 and Secp256k1 from same mnemonic have different addresses
    Given a valid mnemonic phrase
    When I derive an Ed25519 account
    And I derive a Secp256k1 account
    Then the addresses should be different

  # =============================================================================
  # Passphrase Support
  # =============================================================================

  @preferred
  Scenario: Derive account with passphrase
    Given a valid mnemonic phrase
    And a passphrase "mysecretpassphrase"
    When I derive an account with the passphrase
    Then the account should be valid

  @preferred
  Scenario: Different passphrases produce different accounts
    Given a valid mnemonic phrase
    When I derive an account with passphrase "pass1"
    And I derive an account with passphrase "pass2"
    Then the addresses should be different

  @preferred
  Scenario: No passphrase is same as empty passphrase
    Given a valid mnemonic phrase
    When I derive an account with no passphrase
    And I derive an account with empty string passphrase
    Then the addresses should be the same

  # =============================================================================
  # Test Vectors
  # =============================================================================

  @preferred
  Scenario: Known test vector - 12 word mnemonic
    Given mnemonic "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    When I derive an Ed25519 account with default path
    Then the address should match the expected value from test vectors
    And the public key should match the expected value from test vectors

  @preferred
  Scenario: Known test vector - with passphrase
    Given mnemonic "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    And passphrase "TREZOR"
    When I derive an Ed25519 account
    Then the address should match the expected value from test vectors

  @preferred
  Scenario: Known test vector - multiple indices
    Given mnemonic from test vectors
    When I derive accounts at indices 0 through 4
    Then each address should match the expected values from test vectors

  # =============================================================================
  # Derivation Path Validation
  # =============================================================================

  @preferred
  Scenario: Valid derivation path formats
    Given a valid mnemonic phrase
    When I derive with path "m/44'/637'/0'/0'/0'"
    Then the derivation should succeed

  @preferred
  Scenario: Reject invalid derivation path - missing m
    Given a valid mnemonic phrase
    When I try to derive with path "44'/637'/0'/0'/0'"
    Then the derivation should fail

  @preferred
  Scenario: Reject invalid derivation path - wrong coin type
    Given a valid mnemonic phrase
    When I try to derive with path "m/44'/60'/0'/0'/0'"
    Then the derivation should either fail or produce a different result than Aptos default

  @preferred
  Scenario: Reject invalid derivation path - non-hardened where required
    Given a valid mnemonic phrase
    When I try to derive with path "m/44/637/0/0/0"
    Then the derivation should fail or produce different result

  # =============================================================================
  # Security
  # =============================================================================

  @preferred
  Scenario: Mnemonic phrase can be retrieved
    Given a generated mnemonic
    When I get the phrase as string
    Then I should get the original words

  @preferred
  Scenario: Seed is zeroized after derivation
    Given a mnemonic phrase
    When I derive an account
    Then the intermediate seed should be zeroized from memory

