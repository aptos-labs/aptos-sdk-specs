"""
Step definitions for Secp256r1 (P-256) cryptography.
All steps marked pending as Python SDK does not support Secp256r1.
"""

from behave import given, when, then

# =============================================================================
# Secp256r1 Key Generation - All Pending
# =============================================================================


@given("a Secp256r1 key pair")
def step_given_secp256r1_keypair(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("two different Secp256r1 key pairs")
def step_given_two_secp256r1_keypairs(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a Secp256r1 account")
def step_given_secp256r1_account(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a hex-encoded Secp256r1 private key")
def step_given_hex_secp256r1_key(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a known Secp256r1 key pair from test vectors")
def step_given_known_secp256r1_keypair(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a known Secp256r1 private key from test vectors")
def step_given_known_secp256r1_privkey(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a 32-byte value greater than the P-256 curve order")
def step_given_invalid_p256_value(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a Secp256r1 public key (uncompressed)")
def step_given_secp256r1_pubkey_uncompressed(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a Secp256r1 signature created by the key pair")
def step_given_secp256r1_sig_by_keypair(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a Secp256r1 signature with invalid bytes")
def step_given_secp256r1_invalid_sig(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a Secp256r1 signature in DER format")
def step_given_secp256r1_der_sig(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a message signed by the first Secp256r1 key")
def step_given_msg_signed_by_first_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("a RawTransaction for Secp256r1 signing")
def step_given_raw_tx_for_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("the Secp256r1 message from test vectors")
def step_given_secp256r1_msg_from_vectors(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@given("the same 32-byte private key")
def step_given_same_32byte_privkey(context):
    import os

    context.world.bytes_value = os.urandom(32)


@given("a COSE-encoded P-256 public key from WebAuthn")
def step_given_cose_p256_pubkey(context):
    # TODO: awaiting SDK implementation - WebAuthn/Secp256r1 not supported
    context.scenario.skip("WebAuthn/Secp256r1 not supported in Python SDK")


@given("a WebAuthn assertion signature")
def step_given_webauthn_sig(context):
    # TODO: awaiting SDK implementation - WebAuthn not supported
    context.scenario.skip("WebAuthn not supported in Python SDK")


@given("the authenticator data and client data")
def step_given_authenticator_client_data(context):
    # TODO: awaiting SDK implementation - WebAuthn not supported
    context.scenario.skip("WebAuthn not supported in Python SDK")


# =============================================================================
# When Steps - Secp256r1 Operations
# =============================================================================


@when("I generate a random Secp256r1 key pair")
def step_generate_secp256r1_keypair(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I create a Secp256r1 key pair from the bytes")
def step_create_secp256r1_from_bytes(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I create a Secp256r1 key pair from hex")
def step_create_secp256r1_from_hex(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I try to create a Secp256r1 key pair")
def step_try_create_secp256r1_keypair(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I create a Secp256r1 account")
def step_create_secp256r1_account(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I derive the Secp256r1 authentication key")
def step_derive_secp256r1_auth_key(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I derive the Secp256r1 public key")
def step_derive_secp256r1_pubkey(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I get the Secp256r1 uncompressed public key")
def step_get_secp256r1_uncompressed_pubkey(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I sign the message with Secp256r1")
def step_sign_msg_with_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I sign the Secp256r1 message twice")
def step_sign_secp256r1_twice(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I sign the transaction with Secp256r1")
def step_sign_tx_with_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I verify the Secp256r1 signature")
def step_verify_secp256r1_sig(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I verify with the second Secp256r1 key's public key")
def step_verify_with_second_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I parse it as Secp256r1 public key")
def step_parse_as_secp256r1_pubkey(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I convert to raw (r,s) format")
def step_convert_to_raw_rs(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@when("I create Secp256k1 and Secp256r1 accounts")
def step_create_secp256k1_and_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


# =============================================================================
# Then Steps - Secp256r1 Assertions
# =============================================================================


@then("the Secp256r1 key pair should be valid")
def step_secp256r1_keypair_valid(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 result should be 33 bytes")
def step_secp256r1_result_33_bytes(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 result should be 65 bytes")
def step_secp256r1_result_65_bytes(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 first byte should be 0x02 or 0x03")
def step_secp256r1_first_byte_02_03(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 first byte should be 0x04")
def step_secp256r1_first_byte_04(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 signature should be 64 bytes")
def step_secp256r1_sig_64_bytes(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 signature should be valid for the message")
def step_secp256r1_sig_valid(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("both Secp256r1 signatures should be identical")
def step_both_secp256r1_sigs_identical(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 pre-hash signature should be valid")
def step_secp256r1_prehash_valid(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("Secp256r1 verification should succeed")
def step_secp256r1_verify_succeed(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("Secp256r1 verification should fail")
def step_secp256r1_verify_fail(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("I should get a valid Secp256r1 public key")
def step_get_valid_secp256r1_pubkey(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the scheme identifier used should be 0x02")
def step_scheme_id_0x02(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 and Secp256k1 addresses should be different")
def step_secp256r1_secp256k1_addrs_different(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the difference is due to scheme identifier")
def step_diff_due_to_scheme(context):
    # Documentation assertion
    pass


@then("I should get a valid public key")
def step_get_valid_pubkey(context):
    assert (
        context.world.ed25519_public_key is not None
        or context.world.public_key is not None
    )


@then("I should get a Secp256r1 SignedTransaction")
def step_get_secp256r1_signed_tx(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("it should equal SHA3-256(public_key_bytes || 0x02)")
def step_equals_sha3_256_02(context):
    # TODO: awaiting SDK implementation - Secp256r1 not supported
    context.scenario.skip("Secp256r1 not supported in Python SDK")
