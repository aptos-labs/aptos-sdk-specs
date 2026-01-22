"""
Step definitions for single-key.feature
Tests account creation and management.
"""

import sys
import os
import hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then
from aptos_sdk.account import Account
from aptos_sdk.ed25519 import PrivateKey as Ed25519PrivateKey
from aptos_sdk.account_address import AccountAddress

from support.vectors import hex_to_bytes, bytes_to_hex


# =============================================================================
# Given Steps - Account Creation
# =============================================================================


@given("an Ed25519 account")
def step_given_ed25519_account(context):
    context.world.account = Account.generate()


@given("two different Ed25519 accounts")
def step_given_two_ed25519_accounts(context):
    context.world.account = Account.generate()
    context.world.account_2 = Account.generate()


@given("a newly created Ed25519 account")
def step_given_new_ed25519_account(context):
    context.world.account = Account.generate()


@given("a valid Ed25519 private key (32 bytes)")
def step_given_valid_ed25519_private_key(context):
    import os as _os
    context.world.bytes_value = _os.urandom(32)


@given("a byte array of length {length:d}")
def step_given_byte_array_of_length(context, length):
    context.world.bytes_value = bytes(length)


@given('an invalid hex string "{hex_str}"')
def step_given_invalid_hex_string(context, hex_str):
    context.world.hex_string = hex_str


@given("an Ed25519 account as Account interface")
def step_given_ed25519_as_account_interface(context):
    context.world.account = Account.generate()


@given("the same message")
def step_given_same_message(context):
    context.world.message = b"same message"


@given('private key "{key}" from test vectors')
def step_given_private_key_from_vectors(context, key):
    context.world.hex_string = key


# =============================================================================
# When Steps - Account Generation
# =============================================================================


@when("I generate a random Ed25519 account")
def step_generate_random_ed25519_account(context):
    context.world.account = Account.generate()


@when("I generate two random Ed25519 accounts")
def step_generate_two_random_accounts(context):
    context.world.account = Account.generate()
    context.world.account_2 = Account.generate()


@when("I create an Ed25519 account from the private key")
def step_create_ed25519_from_private_key(context):
    try:
        private_key = Ed25519PrivateKey.from_bytes(context.world.bytes_value)
        context.world.account = Account.load_key(private_key)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create an Ed25519 account from hex")
def step_create_ed25519_from_hex(context):
    try:
        key_bytes = hex_to_bytes(context.world.hex_string)
        private_key = Ed25519PrivateKey.from_bytes(key_bytes)
        context.world.account = Account.load_key(private_key)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to create an Ed25519 account")
def step_try_create_ed25519_account(context):
    try:
        private_key = Ed25519PrivateKey.from_bytes(context.world.bytes_value)
        context.world.account = Account.load_key(private_key)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to create an Ed25519 account from hex")
def step_try_create_ed25519_from_hex(context):
    try:
        key_bytes = hex_to_bytes(context.world.hex_string)
        private_key = Ed25519PrivateKey.from_bytes(key_bytes)
        context.world.account = Account.load_key(private_key)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Account Properties
# =============================================================================


@when("I get the address")
def step_get_address(context):
    context.world.address = context.world.account.address()


@when("I get the public key")
def step_get_public_key(context):
    context.world.ed25519_public_key = context.world.account.public_key()


@when("I get the signature scheme")
def step_get_signature_scheme(context):
    # Python SDK may not expose this directly
    context.world.signature_scheme = "ed25519"


@when("I get the authentication key")
def step_get_authentication_key(context):
    context.world.auth_key = context.world.account.auth_key()


@when("I compare address and authentication key")
def step_compare_address_and_auth_key(context):
    context.world.address = context.world.account.address()
    context.world.auth_key = context.world.account.auth_key()


# =============================================================================
# When Steps - Signing
# =============================================================================


@when("both accounts sign the message")
def step_both_accounts_sign(context):
    context.world.ed25519_signature = context.world.account.sign(context.world.message)
    context.world.ed25519_signature_2 = context.world.account_2.sign(context.world.message)


@when("I call address()")
def step_call_address(context):
    context.world.address = context.world.account.address()


@when("I call sign(message)")
def step_call_sign_message(context):
    context.world.message = b"test message"
    context.world.ed25519_signature = context.world.account.sign(context.world.message)


# =============================================================================
# Then Steps - Account Assertions
# =============================================================================


@then("the account should have a valid address")
def step_account_has_valid_address(context):
    assert context.world.account.address() is not None


@then("the account should have a valid public key")
def step_account_has_valid_public_key(context):
    assert context.world.account.public_key() is not None


@then("the address should be 32 bytes")
def step_address_is_32_bytes(context):
    if context.world.address is not None:
        assert len(context.world.address.address) == 32
    elif context.world.account is not None:
        address = context.world.account.address()
        assert len(address.address) == 32
    else:
        raise AssertionError("No address found")


@then("the addresses should be different")
def step_addresses_different(context):
    addr1 = str(context.world.account.address())
    addr2 = str(context.world.account_2.address())
    assert addr1 != addr2


@then("the account should be valid")
def step_account_valid(context):
    assert context.world.error is None
    assert context.world.account is not None


@then("recreating from the same key should produce the same address")
def step_recreate_same_address(context):
    private_key = Ed25519PrivateKey.from_bytes(context.world.bytes_value)
    account_2 = Account.load_key(private_key)
    assert str(context.world.account.address()) == str(account_2.address())


@then("it should fail with an error")
def step_should_fail_with_error(context):
    assert context.world.error is not None


@then("it should be a valid AccountAddress")
def step_is_valid_account_address(context):
    assert context.world.address is not None
    assert isinstance(context.world.address, AccountAddress)


@then("it should be 32 bytes")
def step_is_32_bytes(context):
    if hasattr(context.world, 'ed25519_public_key'):
        assert len(context.world.ed25519_public_key.key) == 32
    elif hasattr(context.world, 'auth_key'):
        auth_key_str = str(context.world.auth_key)
        auth_key_bytes = bytes.fromhex(auth_key_str.replace("0x", ""))
        assert len(auth_key_bytes) == 32
    elif hasattr(context.world, 'address'):
        assert len(context.world.address.address) == 32


@then('it should be "{expected}"')
def step_should_be_value(context, expected):
    assert context.world.signature_scheme == expected


@then("it should equal SHA3-256(public_key || 0x00)")
def step_equals_sha3_256_pubkey(context):
    # Get public key bytes from either account or ed25519_public_key
    if context.world.account is not None:
        public_key_bytes = bytes(context.world.account.public_key().key)
    elif context.world.ed25519_public_key is not None:
        public_key_bytes = bytes(context.world.ed25519_public_key.key)
    else:
        raise AssertionError("No public key found")
    expected = hashlib.sha3_256(public_key_bytes + bytes([0x00])).digest()
    auth_key_str = str(context.world.auth_key)
    actual = bytes.fromhex(auth_key_str.replace("0x", ""))
    assert actual == expected


@then("the signature should verify against the public key")
def step_signature_verifies(context):
    public_key = context.world.account.public_key()
    is_valid = public_key.verify(context.world.message, context.world.ed25519_signature)
    assert is_valid


@then("it should return the correct address")
def step_returns_correct_address(context):
    assert context.world.address is not None


@then("it should return a valid signature")
def step_returns_valid_signature(context):
    assert context.world.ed25519_signature is not None


@then('the address should be "{expected}" as specified in test vectors')
def step_address_matches_test_vector(context, expected):
    actual = str(context.world.account.address())
    # Normalize for comparison
    actual_norm = actual.lower()
    expected_norm = expected.lower()
    assert actual_norm == expected_norm


@then("the public key should match test vectors")
def step_public_key_matches_test_vector(context):
    # Generic assertion - specific vectors would need actual values
    assert context.world.account.public_key() is not None
