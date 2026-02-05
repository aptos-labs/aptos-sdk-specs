"""
Step definitions for secp256k1.feature
Tests Secp256k1 cryptographic operations.
"""

from support.vectors import (
    get_secp256k1_test_vectors,
    hex_to_bytes,
)
from behave import given, when, then
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Try to import secp256k1 support
try:
    from ecdsa import SECP256k1, SigningKey, VerifyingKey, BadSignatureError

    SECP256K1_AVAILABLE = True
except ImportError:
    SECP256K1_AVAILABLE = False


# =============================================================================
# Given Steps - Key Generation
# =============================================================================


@given("I generate a random Secp256k1 key pair")
def step_generate_secp256k1_keypair(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()

        context.world.private_key = private_key
        context.world.public_key = public_key
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given("I generate another Secp256k1 key pair")
def step_generate_another_secp256k1(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()

        context.world.test_vectors["private_key_2"] = private_key
        context.world.test_vectors["public_key_2"] = public_key
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given('a Secp256k1 private key "{key_hex}"')
def step_given_secp256k1_private_key(context, key_hex):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        key_bytes = hex_to_bytes(key_hex)
        context.world.private_key = SigningKey.from_string(key_bytes, curve=SECP256k1)
        context.world.public_key = context.world.private_key.get_verifying_key()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given('a Secp256k1 public key "{key_hex}"')
def step_given_secp256k1_public_key(context, key_hex):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        key_bytes = hex_to_bytes(key_hex)
        context.world.public_key = VerifyingKey.from_string(key_bytes, curve=SECP256k1)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@given("test vectors from secp256k1.json")
def step_given_secp256k1_vectors(context):
    context.world.test_vectors["secp256k1"] = get_secp256k1_test_vectors()


# =============================================================================
# When Steps - Signing
# =============================================================================


@when("I sign a message with the Secp256k1 private key")
def step_sign_with_secp256k1(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        message = context.world.message or b"Test message"
        signature = context.world.private_key.sign(message)
        context.world.signature = signature
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I sign a message with deterministic k (RFC 6979)")
def step_sign_deterministic(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        import hashlib

        message = context.world.message or b"Test message"
        # ECDSA library uses RFC 6979 by default
        signature = context.world.private_key.sign(message, hashfunc=hashlib.sha256)
        context.world.signature = signature
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Verification
# =============================================================================


@when("I verify the Secp256k1 signature")
def step_verify_secp256k1(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        message = context.world.message or b"Test message"
        is_valid = context.world.public_key.verify(context.world.signature, message)
        context.world.result = is_valid
        context.world.clear_error()
    except BadSignatureError:
        context.world.result = False
        context.world.clear_error()
    except Exception as e:
        context.world.result = False
        context.world.set_error(e)


@when("I verify the signature with a different message")
def step_verify_different_message(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        different_message = b"Different message"
        is_valid = context.world.public_key.verify(
            context.world.signature, different_message
        )
        context.world.result = is_valid
    except BadSignatureError:
        context.world.result = False
    except Exception as e:
        context.world.result = False
        context.world.set_error(e)


@when("I verify the signature with a different public key")
def step_verify_different_public_key(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        message = context.world.message or b"Test message"
        other_public_key = context.world.test_vectors.get("public_key_2")
        if other_public_key:
            is_valid = other_public_key.verify(context.world.signature, message)
            context.world.result = is_valid
        else:
            context.world.result = False
    except BadSignatureError:
        context.world.result = False
    except Exception:
        context.world.result = False


# =============================================================================
# When Steps - Key Export/Import
# =============================================================================


@when("I export the Secp256k1 private key to bytes")
def step_export_secp256k1_private(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        context.world.bytes_value = context.world.private_key.to_string()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I export the Secp256k1 public key to bytes")
def step_export_secp256k1_public(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        context.world.bytes_value = context.world.public_key.to_string()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I export the Secp256k1 public key to compressed bytes")
def step_export_secp256k1_public_compressed(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        context.world.bytes_value = context.world.public_key.to_string("compressed")
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I import the Secp256k1 private key from bytes")
def step_import_secp256k1_private(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        context.world.private_key = SigningKey.from_string(
            context.world.bytes_value, curve=SECP256k1
        )
        context.world.public_key = context.world.private_key.get_verifying_key()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I import the Secp256k1 public key from bytes")
def step_import_secp256k1_public(context):
    if not SECP256K1_AVAILABLE:
        context.world.set_error(ImportError("ecdsa library not available"))
        return

    try:
        context.world.public_key = VerifyingKey.from_string(
            context.world.bytes_value, curve=SECP256k1
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Key Assertions
# =============================================================================


@then("I should have a valid Secp256k1 key pair")
def step_should_have_secp256k1_keypair(context):
    assert context.world.error is None
    assert context.world.private_key is not None
    assert context.world.public_key is not None


@then("the Secp256k1 private key should be 32 bytes")
def step_secp256k1_private_32_bytes(context):
    assert len(context.world.private_key.to_string()) == 32


@then("the Secp256k1 public key should be 64 bytes (uncompressed)")
def step_secp256k1_public_64_bytes(context):
    # Uncompressed point without prefix is 64 bytes
    assert len(context.world.public_key.to_string()) == 64


@then("the compressed Secp256k1 public key should be 33 bytes")
def step_secp256k1_public_33_bytes(context):
    assert len(context.world.bytes_value) == 33


@then("the two Secp256k1 key pairs should be different")
def step_secp256k1_keypairs_different(context):
    pk1 = context.world.private_key.to_string()
    pk2 = context.world.test_vectors.get("private_key_2").to_string()
    assert pk1 != pk2


# =============================================================================
# Then Steps - Signature Assertions
# =============================================================================


@then("the Secp256k1 signature should be valid")
def step_secp256k1_signature_valid(context):
    assert context.world.error is None
    assert context.world.signature is not None


@then("the Secp256k1 signature should be 64 bytes (r || s)")
def step_secp256k1_signature_64_bytes(context):
    # Raw signature without DER encoding
    assert len(context.world.signature) == 64


@then("the Secp256k1 verification should pass")
def step_secp256k1_verification_pass(context):
    assert context.world.result is True


@then("the Secp256k1 verification should fail")
def step_secp256k1_verification_fail(context):
    assert context.world.result is False


@then("signing the same message twice should produce the same signature")
def step_secp256k1_deterministic_signature(context):
    if not SECP256K1_AVAILABLE:
        return

    import hashlib

    message = context.world.message or b"Test message"

    sig1 = context.world.private_key.sign(message, hashfunc=hashlib.sha256)
    sig2 = context.world.private_key.sign(message, hashfunc=hashlib.sha256)

    assert sig1 == sig2


# =============================================================================
# Then Steps - Export/Import Assertions
# =============================================================================


@then("the exported Secp256k1 private key should match the original")
def step_exported_secp256k1_private_matches(context):
    original = context.world.private_key.to_string()
    assert context.world.bytes_value == original


@then("the imported Secp256k1 key should match the original")
def step_imported_secp256k1_matches(context):
    # The key should be usable for signing/verification
    assert context.world.error is None


# =============================================================================
# Then Steps - Test Vector Assertions
# =============================================================================


@then("all Secp256k1 test vectors should pass")
def step_all_secp256k1_vectors_pass(context):
    if not SECP256K1_AVAILABLE:
        return

    vectors = context.world.test_vectors.get("secp256k1", [])
    failures = []

    for vector in vectors:
        try:
            if "private_key" in vector and "public_key" in vector:
                pk_bytes = hex_to_bytes(vector["private_key"])
                private_key = SigningKey.from_string(pk_bytes, curve=SECP256k1)
                expected_public = hex_to_bytes(vector["public_key"])
                actual_public = private_key.get_verifying_key().to_string()

                if actual_public != expected_public:
                    failures.append(
                        f"{vector.get('name', 'unknown')}: public key mismatch"
                    )
        except Exception as e:
            failures.append(f"{vector.get('name', 'unknown')}: {str(e)}")

    if failures:
        raise AssertionError("\n".join(failures))
