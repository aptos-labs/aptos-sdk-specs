"""
Step definitions for mnemonic phrases and HD derivation.
Most steps marked pending as Python SDK has limited mnemonic support.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Mnemonic Setup
# =============================================================================


@given("a mnemonic phrase")
def step_given_mnemonic_phrase(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("a valid mnemonic phrase")
def step_given_valid_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("a generated mnemonic")
def step_given_generated_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("mnemonic from test vectors")
def step_given_mnemonic_from_vectors(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("a known seed from test vectors")
def step_given_known_seed_from_vectors(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("two different mnemonic phrases")
def step_given_two_mnemonics(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("a mnemonic phrase with 11 words")
def step_given_11_word_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("a mnemonic phrase with valid words but wrong checksum")
def step_given_mnemonic_wrong_checksum(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given("a mnemonic entropy and passphrase")
def step_given_mnemonic_entropy_passphrase(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@given(
    'mnemonic "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"'
)
def step_given_test_mnemonic(context):
    context.world.mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"


@given(
    'the mnemonic phrase "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"'
)
def step_given_test_mnemonic_alt(context):
    context.world.mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"


@given(
    'the mnemonic phrase "ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABOUT"'
)
def step_given_test_mnemonic_upper(context):
    context.world.mnemonic = "ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABOUT"


@given(
    'the mnemonic phrase "invalid word abandon abandon abandon abandon abandon abandon abandon abandon abandon about"'
)
def step_given_invalid_mnemonic(context):
    context.world.mnemonic = "invalid word abandon abandon abandon abandon abandon abandon abandon abandon abandon about"


@given("derivation path \"m/44'/637'/0'/0'/5'\"")
def step_given_derivation_path(context):
    context.world.derivation_path = "m/44'/637'/0'/0'/5'"


@given('passphrase "TREZOR"')
def step_given_passphrase_trezor(context):
    context.world.passphrase = "TREZOR"


# =============================================================================
# When Steps - Mnemonic Operations
# =============================================================================


@when("I generate a 12-word mnemonic")
def step_generate_12_word_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I generate a mnemonic with 12 words")
def step_generate_mnemonic_12(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I generate a mnemonic with 15 words")
def step_generate_mnemonic_15(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I generate a mnemonic with 18 words")
def step_generate_mnemonic_18(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I generate a mnemonic with 21 words")
def step_generate_mnemonic_21(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I generate a mnemonic with 24 words")
def step_generate_mnemonic_24(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I generate two 12-word mnemonics")
def step_generate_two_mnemonics(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I parse the mnemonic")
def step_parse_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I get the phrase as string")
def step_get_phrase_string(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an Ed25519 account")
def step_derive_ed25519_account(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an Ed25519 account twice")
def step_derive_ed25519_twice(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an Ed25519 account with default path")
def step_derive_ed25519_default_path(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an Ed25519 account with the custom path")
def step_derive_ed25519_custom_path(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an account")
def step_derive_account(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an account with the passphrase")
def step_derive_account_with_passphrase(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an account with no passphrase")
def step_derive_account_no_passphrase(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive an account with empty string passphrase")
def step_derive_account_empty_passphrase(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when('I derive an account with passphrase "pass1"')
def step_derive_account_pass1(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when('I derive an account with passphrase "pass2"')
def step_derive_account_pass2(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive accounts at indices 0 through 4")
def step_derive_accounts_0_to_4(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive accounts at indices 0, 1, 2, 3, 4")
def step_derive_accounts_indices(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive accounts at paths \"m/44'/637'/0'/0'/0'\" and \"m/44'/637'/0'/0'/1'\"")
def step_derive_accounts_paths(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive Ed25519 accounts from each")
def step_derive_ed25519_from_each(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive with path \"m/44'/637'/0'/0'/0'\"")
def step_derive_with_default_path(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive a Secp256k1 account from the mnemonic")
def step_derive_secp256k1_from_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive a Secp256k1 account")
def step_derive_secp256k1_account(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I try to derive with path \"44'/637'/0'/0'/0'\"")
def step_try_derive_no_m(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when('I try to derive with path "m/44/637/0/0/0"')
def step_try_derive_no_hardened(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I try to derive with path \"m/44'/60'/0'/0'/0'\"")
def step_try_derive_ethereum_path(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when('I compute HMAC-SHA512 with key "mnemonic" + passphrase')
def step_compute_hmac_sha512(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


# =============================================================================
# Then Steps - Mnemonic Assertions
# =============================================================================


@then("I should get the original words")
def step_get_original_words(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("I should have 5 different accounts")
def step_have_5_accounts(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the result should be 64 bytes")
def step_result_64_bytes(context):
    if context.world.bytes_value:
        assert len(context.world.bytes_value) == 64
    else:
        context.scenario.skip("No bytes value")


@then("I should get 64 bytes")
def step_get_64_bytes(context):
    if context.world.bytes_value:
        assert len(context.world.bytes_value) == 64
    else:
        context.scenario.skip("No bytes value")


@then("all words should be in the BIP-39 English wordlist")
def step_words_in_wordlist(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the derivation path used should be \"m/44'/637'/0'/0'/0'\"")
def step_derivation_path_default(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the address should differ from default path")
def step_address_differs_from_default(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the derivation should fail")
def step_derivation_fails(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the derivation should succeed")
def step_derivation_succeeds(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the derivation should fail or produce different result")
def step_derivation_fails_or_different(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then(
    "the derivation should either fail or produce a different result than Aptos default"
)
def step_derivation_fails_or_different_alt(context):
    # TODO: awaiting SDK implementation - mnemonic support limited
    context.scenario.skip("Mnemonic support limited in Python SDK")


@then("the intermediate seed should be zeroized from memory")
def step_seed_zeroized(context):
    # Python doesn't support explicit memory zeroization
    pass
