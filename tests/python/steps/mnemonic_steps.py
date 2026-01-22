"""
Step definitions for mnemonic-derivation.feature
Tests BIP-39 mnemonic generation and HD key derivation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then

# Try to import mnemonic support from SDK or use fallback
try:
    from aptos_sdk.account import Account
    from aptos_sdk.ed25519 import PrivateKey
except ImportError:
    pass

# Fallback to bip-utils or mnemonic library
try:
    from mnemonic import Mnemonic
    BIP39_AVAILABLE = True
except ImportError:
    BIP39_AVAILABLE = False

from support.vectors import (
    get_ed25519_derivation_vectors,
    hex_to_bytes,
    bytes_to_hex,
)


# =============================================================================
# Given Steps - Mnemonic Generation
# =============================================================================


@given("I generate a 12-word mnemonic")
def step_generate_12_word_mnemonic(context):
    if not BIP39_AVAILABLE:
        context.world.set_error(ImportError("mnemonic library not available"))
        return
    
    try:
        mnemo = Mnemonic("english")
        context.world.mnemonic = mnemo.generate(strength=128)  # 12 words
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given("I generate a 24-word mnemonic")
def step_generate_24_word_mnemonic(context):
    if not BIP39_AVAILABLE:
        context.world.set_error(ImportError("mnemonic library not available"))
        return
    
    try:
        mnemo = Mnemonic("english")
        context.world.mnemonic = mnemo.generate(strength=256)  # 24 words
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given("I generate another mnemonic")
def step_generate_another_mnemonic(context):
    if not BIP39_AVAILABLE:
        context.world.set_error(ImportError("mnemonic library not available"))
        return
    
    try:
        mnemo = Mnemonic("english")
        context.world.test_vectors["mnemonic_2"] = mnemo.generate(strength=128)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Given Steps - Mnemonic Parsing
# =============================================================================


@given('a mnemonic phrase "{phrase}"')
def step_given_mnemonic_phrase(context, phrase):
    context.world.mnemonic = phrase


@given('an invalid mnemonic word "{word}"')
def step_given_invalid_mnemonic_word(context, word):
    # Replace a valid word with an invalid one
    context.world.mnemonic = f"{word} abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"


@given("a mnemonic with wrong word count")
def step_given_wrong_word_count(context):
    context.world.mnemonic = "abandon abandon abandon"


@given("a mnemonic with invalid checksum")
def step_given_invalid_checksum(context):
    # Valid words but wrong checksum
    context.world.mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"


# =============================================================================
# Given Steps - Derivation Path
# =============================================================================


@given("the default derivation path")
def step_given_default_derivation_path(context):
    context.world.derivation_path = "m/44'/637'/0'/0'/0'"


@given('a derivation path "{path}"')
def step_given_derivation_path(context, path):
    context.world.derivation_path = path


@given('an invalid derivation path "{path}"')
def step_given_invalid_derivation_path(context, path):
    context.world.derivation_path = path


# =============================================================================
# Given Steps - Passphrase
# =============================================================================


@given("no passphrase")
def step_given_no_passphrase(context):
    context.world.passphrase = ""


@given('a passphrase "{passphrase}"')
def step_given_passphrase(context, passphrase):
    context.world.passphrase = passphrase


@given("an empty passphrase")
def step_given_empty_passphrase(context):
    context.world.passphrase = ""


# =============================================================================
# Given Steps - Test Vectors
# =============================================================================


@given("test vectors from mnemonics.json")
def step_given_mnemonic_test_vectors(context):
    context.world.test_vectors["ed25519_derivation"] = get_ed25519_derivation_vectors()


# =============================================================================
# When Steps - Mnemonic Validation
# =============================================================================


@when("I validate the mnemonic")
def step_validate_mnemonic(context):
    if not BIP39_AVAILABLE:
        context.world.set_error(ImportError("mnemonic library not available"))
        return
    
    try:
        mnemo = Mnemonic("english")
        is_valid = mnemo.check(context.world.mnemonic)
        context.world.result = is_valid
        if not is_valid:
            context.world.set_error(ValueError("Invalid mnemonic"))
        else:
            context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to parse the mnemonic")
def step_try_parse_mnemonic(context):
    step_validate_mnemonic(context)


# =============================================================================
# When Steps - Account Derivation
# =============================================================================


@when("I derive an Ed25519 account from the mnemonic")
def step_derive_ed25519_from_mnemonic(context):
    if not BIP39_AVAILABLE:
        context.world.set_error(ImportError("mnemonic library not available"))
        return
    
    try:
        mnemo = Mnemonic("english")
        passphrase = context.world.passphrase or ""
        
        # Generate seed
        seed = mnemo.to_seed(context.world.mnemonic, passphrase)
        
        # Parse derivation path
        path = context.world.derivation_path or "m/44'/637'/0'/0'/0'"
        
        # Derive key using SLIP-10 Ed25519
        # This is a simplified implementation
        from hashlib import pbkdf2_hmac
        import hmac
        import hashlib
        
        # SLIP-10 Ed25519 derivation
        def derive_ed25519_slip10(seed, path):
            # Parse path
            if not path.startswith("m/"):
                raise ValueError("Path must start with m/")
            
            parts = path[2:].split("/")
            
            # Initialize with seed
            I = hmac.new(b"ed25519 seed", seed, hashlib.sha512).digest()
            key = I[:32]
            chain_code = I[32:]
            
            for part in parts:
                if part.endswith("'"):
                    index = int(part[:-1]) + 0x80000000
                else:
                    index = int(part)
                
                # Child key derivation
                data = b"\x00" + key + index.to_bytes(4, "big")
                I = hmac.new(chain_code, data, hashlib.sha512).digest()
                key = I[:32]
                chain_code = I[32:]
            
            return key
        
        private_key_bytes = derive_ed25519_slip10(seed, path)
        
        # Create account from private key
        private_key = PrivateKey.from_bytes(private_key_bytes)
        context.world.account = Account.load_key(private_key.key.hex())
        context.world.test_vectors["derived_key"] = private_key_bytes
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I derive another account from the same mnemonic")
def step_derive_another_from_same_mnemonic(context):
    # Save the first account
    context.world.test_vectors["account_1"] = context.world.account
    step_derive_ed25519_from_mnemonic(context)
    context.world.test_vectors["account_2"] = context.world.account


@when("I derive an account with index {index:d}")
def step_derive_account_with_index(context, index):
    context.world.derivation_path = f"m/44'/637'/0'/0'/{index}'"
    step_derive_ed25519_from_mnemonic(context)
    context.world.test_vectors[f"account_{index}"] = context.world.account


# =============================================================================
# Then Steps - Mnemonic Assertions
# =============================================================================


@then("I should have a valid mnemonic")
def step_should_have_valid_mnemonic(context):
    assert context.world.error is None
    assert context.world.mnemonic is not None


@then("the mnemonic should have 12 words")
def step_mnemonic_12_words(context):
    words = context.world.mnemonic.split()
    assert len(words) == 12


@then("the mnemonic should have 24 words")
def step_mnemonic_24_words(context):
    words = context.world.mnemonic.split()
    assert len(words) == 24


@then("all words should be in the BIP-39 wordlist")
def step_all_words_in_wordlist(context):
    if not BIP39_AVAILABLE:
        return
    
    mnemo = Mnemonic("english")
    wordlist = mnemo.wordlist
    words = context.world.mnemonic.split()
    
    for word in words:
        assert word.lower() in wordlist, f"Word '{word}' not in BIP-39 wordlist"


@then("the two mnemonics should be different")
def step_mnemonics_different(context):
    mnemonic_1 = context.world.mnemonic
    mnemonic_2 = context.world.test_vectors.get("mnemonic_2")
    assert mnemonic_1 != mnemonic_2


@then("mnemonic validation should succeed")
def step_mnemonic_validation_succeed(context):
    assert context.world.error is None
    assert context.world.result is True


@then("mnemonic validation should fail")
def step_mnemonic_validation_fail(context):
    assert context.world.error is not None or context.world.result is False


@then("mnemonic parsing should fail")
def step_mnemonic_parsing_fail(context):
    assert context.world.error is not None


# =============================================================================
# Then Steps - Derivation Assertions
# =============================================================================


@then("I should have a valid derived account")
def step_should_have_derived_account(context):
    assert context.world.error is None
    assert context.world.account is not None


@then("derivation should succeed")
def step_derivation_succeed(context):
    assert context.world.error is None


@then("derivation should fail")
def step_derivation_fail(context):
    assert context.world.error is not None


@then("deriving from the same mnemonic twice should produce the same account")
def step_same_mnemonic_same_account(context):
    # Derive again
    account_1_addr = str(context.world.test_vectors.get("account_1").address())
    step_derive_ed25519_from_mnemonic(context)
    account_2_addr = str(context.world.account.address())
    
    assert account_1_addr == account_2_addr


@then("different mnemonics should produce different accounts")
def step_different_mnemonics_different_accounts(context):
    addr1 = str(context.world.account.address())
    
    # Derive from second mnemonic
    original_mnemonic = context.world.mnemonic
    context.world.mnemonic = context.world.test_vectors.get("mnemonic_2")
    step_derive_ed25519_from_mnemonic(context)
    addr2 = str(context.world.account.address())
    
    # Restore
    context.world.mnemonic = original_mnemonic
    
    assert addr1 != addr2


@then("different paths should produce different accounts")
def step_different_paths_different_accounts(context):
    account_1 = context.world.test_vectors.get("account_1")
    account_2 = context.world.test_vectors.get("account_2")
    
    assert str(account_1.address()) != str(account_2.address())


@then("accounts at different indices should be different")
def step_different_indices_different_accounts(context):
    account_0 = context.world.test_vectors.get("account_0")
    account_1 = context.world.test_vectors.get("account_1")
    
    assert str(account_0.address()) != str(account_1.address())


@then('the derived address should be "{expected}"')
def step_derived_address_should_be(context, expected):
    actual = str(context.world.account.address())
    assert actual.lower() == expected.lower()


@then('the derived private key should be "{expected}"')
def step_derived_private_key_should_be(context, expected):
    actual = bytes_to_hex(context.world.test_vectors.get("derived_key"))
    expected_clean = expected.lower()
    if not expected_clean.startswith("0x"):
        expected_clean = "0x" + expected_clean
    assert actual.lower() == expected_clean


# =============================================================================
# Then Steps - Passphrase Assertions
# =============================================================================


@then("different passphrases should produce different accounts")
def step_different_passphrases_different_accounts(context):
    # Derive with passphrase 1
    addr1 = str(context.world.account.address())
    
    # Derive with different passphrase
    original_passphrase = context.world.passphrase
    context.world.passphrase = "different_passphrase"
    step_derive_ed25519_from_mnemonic(context)
    addr2 = str(context.world.account.address())
    
    # Restore
    context.world.passphrase = original_passphrase
    
    assert addr1 != addr2


@then("no passphrase should equal empty passphrase")
def step_no_passphrase_equals_empty(context):
    # Both should derive to the same account
    context.world.passphrase = ""
    step_derive_ed25519_from_mnemonic(context)
    addr1 = str(context.world.account.address())
    
    context.world.passphrase = None
    step_derive_ed25519_from_mnemonic(context)
    addr2 = str(context.world.account.address())
    
    assert addr1 == addr2


# =============================================================================
# Then Steps - Mnemonic Retrieval
# =============================================================================


@then("the mnemonic phrase should be retrievable")
def step_mnemonic_retrievable(context):
    assert context.world.mnemonic is not None
    assert len(context.world.mnemonic) > 0
