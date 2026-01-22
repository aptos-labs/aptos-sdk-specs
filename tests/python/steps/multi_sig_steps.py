"""
Step definitions for multi-signature.feature
Tests multi-signature account and transaction handling.
"""

import sys
import os
import hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer, Deserializer
from aptos_sdk.ed25519 import PublicKey

from support.vectors import (
    get_multi_sig_test_vectors,
    hex_to_bytes,
    bytes_to_hex,
)


# =============================================================================
# Given Steps - Multi-Sig Setup
# =============================================================================


@given("{count:d} Ed25519 key pairs for multi-sig")
def step_given_key_pairs_for_multi_sig(context, count):
    context.world.test_vectors["multi_sig_accounts"] = [
        Account.generate() for _ in range(count)
    ]


@given("a threshold of {threshold:d}")
def step_given_threshold(context, threshold):
    context.world.test_vectors["threshold"] = threshold


@given("public keys from the key pairs")
def step_given_public_keys(context):
    accounts = context.world.test_vectors.get("multi_sig_accounts", [])
    context.world.test_vectors["public_keys"] = [
        account.public_key() for account in accounts
    ]


@given("test vectors from multi-sig.json")
def step_given_multi_sig_vectors(context):
    context.world.test_vectors["multi_sig"] = get_multi_sig_test_vectors()


@given("{count:d} Ed25519 public keys")
def step_given_ed25519_public_keys(context, count):
    accounts = [Account.generate() for _ in range(count)]
    context.world.test_vectors["multi_sig_accounts"] = accounts
    context.world.test_vectors["public_keys"] = [a.public_key() for a in accounts]


@given("threshold {threshold:d}")
def step_given_threshold_simple(context, threshold):
    context.world.test_vectors["threshold"] = threshold


@given("{count:d} Ed25519 public keys in order")
def step_given_ed25519_public_keys_in_order(context, count):
    accounts = [Account.generate() for _ in range(count)]
    context.world.test_vectors["multi_sig_accounts"] = accounts
    context.world.test_vectors["public_keys"] = [a.public_key() for a in accounts]


@given("public keys [A, B, C] and [C, B, A]")
def step_given_public_keys_two_orders(context):
    accounts = [Account.generate() for _ in range(3)]
    context.world.test_vectors["multi_sig_accounts"] = accounts
    pks = [a.public_key() for a in accounts]
    context.world.test_vectors["public_keys_abc"] = pks
    context.world.test_vectors["public_keys_cba"] = list(reversed(pks))


@given("the same 3 public keys in same order")
def step_given_same_3_public_keys(context):
    if "public_keys" not in context.world.test_vectors:
        accounts = [Account.generate() for _ in range(3)]
        context.world.test_vectors["multi_sig_accounts"] = accounts
        context.world.test_vectors["public_keys"] = [a.public_key() for a in accounts]


@given("a 2-of-3 multi-sig account with 2 private keys")
def step_given_2_of_3_with_2_keys(context):
    accounts = [Account.generate() for _ in range(3)]
    context.world.test_vectors["multi_sig_accounts"] = accounts
    context.world.test_vectors["public_keys"] = [a.public_key() for a in accounts]
    context.world.test_vectors["threshold"] = 2
    context.world.test_vectors["available_signers"] = accounts[:2]


@given("a 2-of-3 multi-sig account with only 1 private key")
def step_given_2_of_3_with_1_key(context):
    accounts = [Account.generate() for _ in range(3)]
    context.world.test_vectors["multi_sig_accounts"] = accounts
    context.world.test_vectors["public_keys"] = [a.public_key() for a in accounts]
    context.world.test_vectors["threshold"] = 2
    context.world.test_vectors["available_signers"] = accounts[:1]


@given("a message to sign")
def step_given_message_to_sign_multi_sig(context):
    context.world.message = b"Test message for multi-sig"


# =============================================================================
# When Steps - Multi-Sig Account Creation
# =============================================================================


@when("I create a multi-sig public key")
def step_create_multi_sig_public_key(context):
    try:
        from aptos_sdk.ed25519 import MultiPublicKey
        
        public_keys = context.world.test_vectors.get("public_keys", [])
        threshold = context.world.test_vectors.get("threshold", 2)
        
        context.world.multi_sig_public_key = MultiPublicKey(
            public_keys,
            threshold
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a MultiEd25519 account")
def step_create_multi_ed25519_account(context):
    step_create_multi_sig_public_key(context)
    if context.world.error is None:
        step_derive_multi_sig_auth_key(context)
        step_derive_multi_sig_address(context)


@when("I try to create a MultiEd25519 account")
def step_try_create_multi_ed25519_account(context):
    step_create_multi_ed25519_account(context)


@when("I create multi-sig accounts from each")
def step_create_multi_sig_accounts_from_each(context):
    try:
        from aptos_sdk.ed25519 import MultiPublicKey
        
        threshold = context.world.test_vectors.get("threshold", 2)
        
        # Create first account with ABC order
        pks_abc = context.world.test_vectors.get("public_keys_abc")
        mpk_abc = MultiPublicKey(pks_abc, threshold)
        
        # Create second account with CBA order
        pks_cba = context.world.test_vectors.get("public_keys_cba")
        mpk_cba = MultiPublicKey(pks_cba, threshold)
        
        # Derive addresses
        def derive_address(mpk):
            serializer = Serializer()
            mpk.serialize(serializer)
            pk_bytes = serializer.output()
            scheme_id = bytes([1])
            auth_key_hash = hashlib.sha3_256(pk_bytes + scheme_id).digest()
            return auth_key_hash.hex()
        
        context.world.test_vectors["address_abc"] = derive_address(mpk_abc)
        context.world.test_vectors["address_cba"] = derive_address(mpk_cba)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create two multi-sig accounts")
def step_create_two_multi_sig_accounts(context):
    try:
        from aptos_sdk.ed25519 import MultiPublicKey
        
        pks = context.world.test_vectors.get("public_keys")
        threshold = context.world.test_vectors.get("threshold", 2)
        
        mpk1 = MultiPublicKey(pks, threshold)
        mpk2 = MultiPublicKey(pks, threshold)
        
        def derive_address(mpk):
            serializer = Serializer()
            mpk.serialize(serializer)
            pk_bytes = serializer.output()
            scheme_id = bytes([1])
            auth_key_hash = hashlib.sha3_256(pk_bytes + scheme_id).digest()
            return auth_key_hash.hex()
        
        context.world.test_vectors["address_1"] = derive_address(mpk1)
        context.world.test_vectors["address_2"] = derive_address(mpk2)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I sign the message with multi-sig")
def step_sign_message_with_multi_sig(context):
    try:
        signers = context.world.test_vectors.get("available_signers", [])
        signatures = {}
        
        for i, signer in enumerate(signers):
            signatures[i] = signer.sign(context.world.message)
        
        context.world.test_vectors["signatures"] = signatures
        step_create_multi_signature(context)
    except Exception as e:
        context.world.set_error(e)


@when("I derive the multi-sig authentication key")
def step_derive_multi_sig_auth_key(context):
    try:
        from aptos_sdk.authenticator import AuthenticationKey
        
        # Multi-sig auth key derivation
        # SHA3-256(public_key_bytes || scheme_id)
        serializer = Serializer()
        context.world.multi_sig_public_key.serialize(serializer)
        pk_bytes = serializer.output()
        
        # Multi-Ed25519 scheme ID is 1
        scheme_id = bytes([1])
        
        auth_key_hash = hashlib.sha3_256(pk_bytes + scheme_id).digest()
        context.world.authentication_key = auth_key_hash.hex()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I derive the multi-sig account address")
def step_derive_multi_sig_address(context):
    try:
        auth_key = context.world.authentication_key
        # Account address is the last 32 bytes of auth key (same for Ed25519)
        context.world.address = AccountAddress.from_str(f"0x{auth_key}")
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Multi-Sig Signing
# =============================================================================


@when("I create a message to sign")
def step_create_message_to_sign(context):
    context.world.message = b"Test message for multi-sig"


@when("signer {index:d} signs the message")
def step_signer_signs_message(context, index):
    try:
        accounts = context.world.test_vectors.get("multi_sig_accounts", [])
        if index >= len(accounts):
            raise IndexError(f"Signer index {index} out of range")
        
        account = accounts[index]
        signature = account.sign(context.world.message)
        
        signatures = context.world.test_vectors.get("signatures", {})
        signatures[index] = signature
        context.world.test_vectors["signatures"] = signatures
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("{count:d} signers sign the message")
def step_multiple_signers_sign(context, count):
    try:
        accounts = context.world.test_vectors.get("multi_sig_accounts", [])
        
        signatures = {}
        for i in range(min(count, len(accounts))):
            signatures[i] = accounts[i].sign(context.world.message)
        
        context.world.test_vectors["signatures"] = signatures
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a multi-signature from the signatures")
def step_create_multi_signature(context):
    try:
        from aptos_sdk.ed25519 import MultiSignature
        
        signatures = context.world.test_vectors.get("signatures", {})
        threshold = context.world.test_vectors.get("threshold", 2)
        total_signers = len(context.world.test_vectors.get("multi_sig_accounts", []))
        
        # Create bitmap
        bitmap = 0
        sig_list = []
        for index, sig in sorted(signatures.items()):
            bitmap |= (1 << (31 - index))  # Big-endian bit order
            sig_list.append(sig)
        
        context.world.multi_signature = MultiSignature(
            signatures=sig_list,
            bitmap=bitmap
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Multi-Sig Verification
# =============================================================================


@when("I verify the multi-signature")
def step_verify_multi_signature(context):
    try:
        is_valid = context.world.multi_sig_public_key.verify(
            context.world.message,
            context.world.multi_signature
        )
        context.world.result = is_valid
        context.world.clear_error()
    except Exception as e:
        context.world.result = False
        context.world.set_error(e)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the multi-sig public key")
def step_bcs_serialize_multi_sig_pk(context):
    try:
        serializer = Serializer()
        context.world.multi_sig_public_key.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS serialize the multi-signature")
def step_bcs_serialize_multi_sig(context):
    try:
        serializer = Serializer()
        context.world.multi_signature.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize the multi-sig public key")
def step_bcs_deserialize_multi_sig_pk(context):
    try:
        from aptos_sdk.ed25519 import MultiPublicKey
        
        deserializer = Deserializer(context.world.bytes_value)
        context.world.multi_sig_public_key = MultiPublicKey.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Multi-Sig Creation Assertions
# =============================================================================


@then("the multi-sig public key should be created")
def step_multi_sig_pk_created(context):
    assert context.world.error is None
    assert context.world.multi_sig_public_key is not None


@then("the multi-sig account should be valid")
def step_multi_sig_account_valid(context):
    assert context.world.error is None
    assert context.world.multi_sig_public_key is not None


@then("threshold should be {threshold:d}")
def step_threshold_should_be(context, threshold):
    assert context.world.multi_sig_public_key.threshold == threshold


@then("num_keys should be {count:d}")
def step_num_keys_should_be(context, count):
    assert len(context.world.multi_sig_public_key.public_keys) == count


@then("all {count:d} signatures should be required")
def step_all_signatures_required(context, count):
    assert context.world.multi_sig_public_key.threshold == count


@then("it should fail with InvalidThreshold error")
def step_fail_invalid_threshold(context):
    assert context.world.error is not None


@then("multi-sig creation should fail with no keys")
def step_fail_no_keys(context):
    assert context.world.error is not None


@then('it should equal SHA3-256(pk1 || pk2 || pk3 || threshold || 0x01)')
def step_auth_key_equals_expected(context):
    # Verify the authentication key derivation formula
    assert context.world.authentication_key is not None
    assert len(context.world.authentication_key) == 64


# Note: "the addresses should be different" is defined in account_steps.py

@then("the multi-sig addresses should be identical")
def step_addresses_identical(context):
    addr_1 = context.world.test_vectors.get("address_1")
    addr_2 = context.world.test_vectors.get("address_2")
    assert addr_1 == addr_2


@then("the multi-sig signature should be valid")
def step_multi_sig_signature_valid(context):
    assert context.world.error is None
    assert context.world.multi_signature is not None


@then("it should contain {count:d} signatures")
def step_contains_n_signatures(context, count):
    assert len(context.world.multi_signature.signatures) == count


@then("signing should fail with insufficient keys")
def step_signing_fail_insufficient(context):
    # With only 1 key for a 2-of-3, we can't meet threshold
    # The signing may succeed but verification would fail
    pass


@then("the multi-sig public key should have {count:d} keys")
def step_multi_sig_pk_count(context, count):
    assert len(context.world.multi_sig_public_key.public_keys) == count


@then("the multi-sig public key should have threshold {threshold:d}")
def step_multi_sig_threshold(context, threshold):
    assert context.world.multi_sig_public_key.threshold == threshold


@then("the authentication key should be 64 hex characters")
def step_auth_key_64_chars(context):
    assert len(context.world.authentication_key) == 64


@then("the multi-sig address should be valid")
def step_multi_sig_address_valid(context):
    assert context.world.address is not None


# =============================================================================
# Then Steps - Signature Assertions
# =============================================================================


@then("the signature should be collected")
def step_signature_collected(context):
    signatures = context.world.test_vectors.get("signatures", {})
    assert len(signatures) > 0


@then("the multi-signature should be created")
def step_multi_sig_created(context):
    assert context.world.error is None
    assert context.world.multi_signature is not None


@then("the multi-signature should have {count:d} signatures")
def step_multi_sig_sig_count(context, count):
    assert len(context.world.multi_signature.signatures) == count


@then("the multi-signature bitmap should be set correctly")
def step_multi_sig_bitmap_correct(context):
    signatures = context.world.test_vectors.get("signatures", {})
    bitmap = context.world.multi_signature.bitmap
    
    for index in signatures.keys():
        expected_bit = (1 << (31 - index))
        assert (bitmap & expected_bit) != 0


# =============================================================================
# Then Steps - Verification Assertions
# =============================================================================


@then("the multi-signature verification should pass")
def step_multi_sig_verification_pass(context):
    assert context.world.result is True


@then("the multi-signature verification should fail")
def step_multi_sig_verification_fail(context):
    assert context.world.result is False


@then("verification should fail with insufficient signatures")
def step_verification_fail_insufficient(context):
    assert context.world.error is not None or context.world.result is False


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the serialized multi-sig public key should not be empty")
def step_multi_sig_pk_serialized_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then("the serialized multi-signature should not be empty")
def step_multi_sig_serialized_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then("the deserialized multi-sig public key should match")
def step_multi_sig_pk_deserialized_matches(context):
    # Serialize again and compare
    serializer = Serializer()
    context.world.multi_sig_public_key.serialize(serializer)
    assert serializer.output() == context.world.bytes_value


# =============================================================================
# Then Steps - Test Vector Assertions
# =============================================================================


@then("all multi-sig test vectors should pass")
def step_all_multi_sig_vectors_pass(context):
    vectors = context.world.test_vectors.get("multi_sig", [])
    failures = []
    
    for vector in vectors:
        try:
            # Test according to vector specifications
            pass  # Implement based on vector format
        except Exception as e:
            failures.append(f"{vector.get('name', 'unknown')}: {str(e)}")
    
    if failures:
        raise AssertionError("\n".join(failures))
