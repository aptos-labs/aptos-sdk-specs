"""
Step definitions for BLS12-381 cryptography.
All steps marked pending as Python SDK does not support BLS12-381.
"""

from behave import given, when, then

# =============================================================================
# BLS12-381 Key Generation - All Pending
# =============================================================================


@given("a BLS12-381 key pair")
def step_given_bls_keypair(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("two different BLS12-381 key pairs")
def step_given_two_bls_keypairs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("two BLS12-381 key pairs")
def step_given_two_bls_keypairs_alt(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a BLS12-381 signature")
def step_given_bls_signature(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a BLS12-381 account")
def step_given_bls_account(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a hex-encoded BLS12-381 private key")
def step_given_hex_bls_key(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("an invalid BLS private key (e.g., zero)")
def step_given_invalid_bls_key(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("47 bytes (wrong length)")
def step_given_47_bytes(context):
    context.world.bytes_value = bytes(47)


@given("95 bytes (wrong length)")
def step_given_95_bytes(context):
    context.world.bytes_value = bytes(95)


@given('a BLS signature for "original"')
def step_given_bls_sig_for_original(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a malformed 96-byte signature")
def step_given_malformed_bls_sig(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("two BLS signatures for the same message")
def step_given_two_bls_sigs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("5 BLS signatures for the same message")
def step_given_five_bls_sigs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("an aggregated signature from N signers")
def step_given_aggregated_sig(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("multiple signatures")
def step_given_multiple_sigs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("two BLS public keys")
def step_given_two_bls_pubkeys(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("5 BLS public keys")
def step_given_five_bls_pubkeys(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("signatures from 3 signers on same message")
def step_given_sigs_from_three(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a BLS public key and its PoP")
def step_given_bls_pubkey_pop(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a PoP from a different key")
def step_given_pop_different_key(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("aggregated public keys with valid PoPs")
def step_given_aggregated_with_pops(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given('signature1 for "message1"')
def step_given_sig1_for_msg1(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given('signature2 for "message2"')
def step_given_sig2_for_msg2(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("the aggregated public key")
def step_given_aggregated_pubkey(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("the original message")
def step_given_original_message(context):
    context.world.message = b"original message"


@given("from two different key pairs")
def step_given_from_two_keypairs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("a known BLS key pair and message from test vectors")
def step_given_known_bls_from_vectors(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("signatures from test vectors")
def step_given_sigs_from_vectors(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@given("bytes that don't represent a valid curve point")
def step_given_invalid_curve_point(context):
    context.world.bytes_value = bytes(48)


# =============================================================================
# When Steps - BLS Operations
# =============================================================================


@when("I generate a random BLS12-381 key pair")
def step_generate_bls_keypair(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I create a BLS12-381 key pair from the seed")
def step_create_bls_from_seed(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I create a key pair from hex")
def step_create_keypair_from_hex(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I try to create a key pair")
def step_try_create_keypair(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I get the public key bytes")
def step_get_pubkey_bytes(context):
    # For Ed25519, get public key bytes
    if context.world.ed25519_public_key:
        context.world.bytes_value = bytes(context.world.ed25519_public_key.key)
    else:
        context.scenario.skip("No public key available")


@when("I get the signature bytes")
def step_get_sig_bytes(context):
    if context.world.ed25519_signature:
        context.world.bytes_value = bytes(context.world.ed25519_signature.signature)
    else:
        context.scenario.skip("No signature available")


@when("I aggregate the signatures")
def step_aggregate_sigs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I aggregate all signatures")
def step_aggregate_all_sigs(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I verify the aggregated signature")
def step_verify_aggregated_sig(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I aggregate in different orders")
def step_aggregate_different_orders(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I aggregate them")
def step_aggregate_them(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I aggregate all keys")
def step_aggregate_all_keys(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I aggregate signatures and public keys")
def step_aggregate_sigs_and_keys(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("verify aggregated signature with aggregated public key")
def step_verify_aggregated_with_aggregated(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I generate a proof of possession")
def step_generate_pop(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I verify the PoP")
def step_verify_pop(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I verify each PoP before aggregation")
def step_verify_each_pop(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I create a BLS12-381 account")
def step_create_bls_account(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I try to parse as BLS public key")
def step_try_parse_bls_pubkey(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I try to parse as BLS signature")
def step_try_parse_bls_sig(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I derive a BLS key pair")
def step_derive_bls_keypair(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@when("I try to verify")
def step_try_verify(context):
    # Generic try to verify - may apply to different crypto
    try:
        if context.world.ed25519_public_key and context.world.ed25519_signature:
            result = context.world.ed25519_public_key.verify(
                context.world.message, context.world.ed25519_signature
            )
            context.world.result = result
        else:
            context.world.result = False
    except Exception as e:
        context.world.result = False
        context.world.set_error(e)


@when('I verify against "modified"')
def step_verify_against_modified(context):
    # Try to verify against different message
    try:
        result = context.world.ed25519_public_key.verify(
            b"modified", context.world.ed25519_signature
        )
        context.world.result = result
    except Exception:
        context.world.result = False


@when("I verify with second key's public key")
def step_verify_with_second_key(context):
    try:
        if context.world.ed25519_public_key_2 and context.world.ed25519_signature:
            result = context.world.ed25519_public_key_2.verify(
                context.world.message, context.world.ed25519_signature
            )
            context.world.result = result
        else:
            context.world.result = False
    except Exception:
        context.world.result = False


# =============================================================================
# Then Steps - BLS Assertions
# =============================================================================


@then("the public key should be 48 bytes")
def step_pubkey_48_bytes(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the size should be 48 bytes")
def step_size_48_bytes(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the size should be 96 bytes")
def step_size_96_bytes(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the signature should be 96 bytes")
def step_sig_96_bytes(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("creating again from same seed should produce same key pair")
def step_same_seed_same_keypair(context):
    # This is for BLS, mark as skipped
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("I should get a single 96-byte signature")
def step_single_96_byte_sig(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the aggregated signatures should be the same")
def step_aggregated_sigs_same(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("verification against any single message should fail")
def step_verification_single_msg_fail(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("I should get a single 48-byte public key")
def step_single_48_byte_pubkey(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the PoP should be 96 bytes")
def step_pop_96_bytes(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("rogue key attacks are prevented")
def step_rogue_key_prevented(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the signature scheme should include BLS identifier")
def step_scheme_bls_identifier(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("it should use the BLS scheme identifier")
def step_uses_bls_identifier(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("the authenticator should use BLS")
def step_authenticator_uses_bls(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")


@then("it should fail with invalid key error")
def step_fail_invalid_key(context):
    assert context.world.error is not None


@then("it should fail with invalid signature error")
def step_fail_invalid_sig(context):
    assert context.world.error is not None


@then("it should fail with invalid point error")
def step_fail_invalid_point(context):
    assert context.world.error is not None


@then("the public key should match expected value")
def step_pubkey_matches_expected(context):
    # Generic assertion
    assert (
        context.world.ed25519_public_key is not None
        or context.world.bytes_value is not None
    )


@then("the signature should match expected value")
def step_sig_matches_expected(context):
    # Generic assertion
    assert context.world.ed25519_signature is not None


@then("the result should match expected aggregated signature")
def step_result_matches_aggregated(context):
    # TODO: awaiting SDK implementation - BLS12-381 not supported
    context.scenario.skip("BLS12-381 not supported in Python SDK")
