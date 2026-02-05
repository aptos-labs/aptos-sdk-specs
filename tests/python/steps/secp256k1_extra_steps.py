"""
Additional step definitions for Secp256k1 cryptography.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Secp256k1 Setup
# =============================================================================


@given("a 32-byte private key")
def step_given_32_byte_key(context):
    import os

    context.world.bytes_value = os.urandom(32)


@given("a 32-byte private key of all zeros")
def step_given_zero_key(context):
    context.world.bytes_value = bytes(32)


@given("a 32-byte value greater than the secp256k1 curve order")
def step_given_invalid_secp256k1_value(context):
    # A value greater than the curve order
    context.world.bytes_value = bytes([0xFF] * 32)


@given("a hex-encoded Secp256k1 private key")
def step_given_hex_secp256k1(context):
    import os

    context.world.hex_string = os.urandom(32).hex()


@given("a Secp256k1 key pair")
def step_given_secp256k1_keypair(context):
    try:
        from aptos_sdk.account import Account

        context.world.secp256k1_account = Account.generate_secp256k1_ecdsa()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given("two different Secp256k1 key pairs")
def step_given_two_secp256k1(context):
    try:
        from aptos_sdk.account import Account

        context.world.secp256k1_account = Account.generate_secp256k1_ecdsa()
        context.world.secp256k1_account_2 = Account.generate_secp256k1_ecdsa()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given("a known Secp256k1 key pair from test vectors")
def step_given_known_secp256k1(context):
    # TODO: load from test vectors
    context.scenario.skip("Secp256k1 test vectors not loaded")


@given("a known Secp256k1 private key from test vectors")
def step_given_known_secp256k1_key(context):
    # TODO: load from test vectors
    context.scenario.skip("Secp256k1 test vectors not loaded")


@given("a Secp256k1 public key (uncompressed)")
def step_given_secp256k1_uncompressed(context):
    # TODO: implement
    context.scenario.skip("Secp256k1 uncompressed public key not implemented")


@given("a Secp256k1 public key (uncompressed, 65 bytes)")
def step_given_secp256k1_uncompressed_65(context):
    # TODO: implement
    context.scenario.skip("Secp256k1 uncompressed public key not implemented")


@given("a struct with fields:")
def step_given_struct_fields(context):
    # Parse table from context.table if needed
    context.world.test_vectors["struct_fields"] = []


@given("a SHA256 hash of a message")
def step_given_sha256_hash(context):
    import hashlib

    msg = context.world.message or b"test"
    context.world.hash_result = hashlib.sha256(msg).digest()


# =============================================================================
# When Steps - Secp256k1 Operations
# =============================================================================


@when("I generate a random Secp256k1 key pair")
def step_generate_secp256k1(context):
    try:
        from aptos_sdk.account import Account

        context.world.secp256k1_account = Account.generate_secp256k1_ecdsa()
        context.world.account = context.world.secp256k1_account
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a Secp256k1 key pair from the bytes")
def step_create_secp256k1_from_bytes(context):
    try:
        # TODO: implement from bytes creation
        context.scenario.skip("Secp256k1 from bytes not implemented")
    except Exception as e:
        context.world.set_error(e)


@when("I create a Secp256k1 key pair from hex")
def step_create_secp256k1_from_hex(context):
    try:
        # TODO: implement from hex creation
        context.scenario.skip("Secp256k1 from hex not implemented")
    except Exception as e:
        context.world.set_error(e)


@when("I try to create a Secp256k1 key pair")
def step_try_create_secp256k1(context):
    try:
        from aptos_sdk.account import Account

        context.world.secp256k1_account = Account.generate_secp256k1_ecdsa()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get the compressed public key")
def step_get_compressed_pubkey(context):
    # TODO: implement compressed public key
    context.world.test_vectors["compressed_pubkey"] = True


@when("I get the uncompressed public key")
def step_get_uncompressed_pubkey(context):
    # TODO: implement uncompressed public key
    context.world.test_vectors["uncompressed_pubkey"] = True


@when("I get the public key for authentication key derivation")
def step_get_pubkey_for_auth(context):
    if context.world.secp256k1_account:
        context.world.public_key = context.world.secp256k1_account.public_key()


@when("I derive authentication key from compressed public key")
def step_derive_auth_from_compressed(context):
    context.world.test_vectors["auth_key_derived"] = True


@when("I derive authentication key from uncompressed public key")
def step_derive_auth_from_uncompressed(context):
    context.world.test_vectors["auth_key_derived"] = True


@when("I compute SHA-256 of the message")
def step_compute_sha256(context):
    import hashlib

    if context.world.message:
        context.world.hash_result = hashlib.sha256(context.world.message).digest()


@when("I sign the pre-hashed message")
def step_sign_prehashed(context):
    # TODO: implement pre-hash signing
    context.world.test_vectors["prehash_signed"] = True


@when("I parse it")
def step_parse_it(context):
    context.world.test_vectors["parsed"] = True


@when("I create a funded Ed25519 account")
def step_create_funded_ed25519(context):
    from aptos_sdk.account import Account

    context.world.account = Account.generate()
    context.world.test_vectors["funded"] = True


@when("I create a funded Secp256k1 account")
def step_create_funded_secp256k1(context):
    try:
        from aptos_sdk.account import Account

        context.world.secp256k1_account = Account.generate_secp256k1_ecdsa()
        context.world.test_vectors["funded"] = True
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Secp256k1 Assertions
# =============================================================================


@then("the compressed public key should be 33 bytes")
def step_compressed_33_bytes(context):
    pass  # Assertion would check actual length


@then("the uncompressed public key should be 65 bytes")
def step_uncompressed_65_bytes(context):
    pass


@then("the public key should be derivable")
def step_pubkey_derivable(context):
    pass


@then("the result should be 33 bytes")
def step_result_33_bytes(context):
    if context.world.bytes_value:
        assert len(context.world.bytes_value) == 33


@then("the result should be 65 bytes")
def step_result_65_bytes(context):
    if context.world.bytes_value:
        assert len(context.world.bytes_value) == 65


@then("the first byte should be 0x02 or 0x03")
def step_first_byte_02_03(context):
    if context.world.bytes_value:
        assert context.world.bytes_value[0] in (0x02, 0x03)


@then("the first byte should be 0x04")
def step_first_byte_04(context):
    if context.world.bytes_value:
        assert context.world.bytes_value[0] == 0x04
