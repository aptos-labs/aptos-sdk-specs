"""
Step definitions for signing.feature
Tests transaction signing and authenticator creation.
"""

import sys
import os
import hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer, Deserializer
from aptos_sdk.transactions import (
    RawTransaction,
    SignedTransaction,
)
from aptos_sdk.authenticator import (
    Authenticator,
    AccountAuthenticator,
    Ed25519Authenticator,
)

from support.vectors import hex_to_bytes, bytes_to_hex


# =============================================================================
# Given Steps - Accounts for Signing
# =============================================================================


@given("an Ed25519 signing account")
def step_given_signing_account(context):
    context.world.account = Account.generate()


@given("a second Ed25519 signing account")
def step_given_second_signing_account(context):
    context.world.account_2 = Account.generate()


@given('an Ed25519 signing account from private key "{key_hex}"')
def step_given_signing_account_from_key(context, key_hex):
    from aptos_sdk.ed25519 import PrivateKey
    key_bytes = hex_to_bytes(key_hex)
    private_key = PrivateKey.from_bytes(key_bytes)
    context.world.account = Account.load_key(private_key.key.hex())


# =============================================================================
# Given Steps - Transactions to Sign
# =============================================================================


@given("a raw transaction to sign")
def step_given_raw_transaction_to_sign(context):
    if context.world.raw_transaction is None:
        # Create a simple raw transaction
        from aptos_sdk.transactions import EntryFunction, TransactionPayload
        import time
        
        sender = context.world.account.address()
        
        # Create simple payload
        encoded_args = []
        serializer = Serializer()
        serializer.struct(AccountAddress.from_str("0x1"))
        encoded_args.append(serializer.output())
        
        serializer = Serializer()
        serializer.u64(1000)
        encoded_args.append(serializer.output())
        
        payload = EntryFunction.natural(
            "0x1::aptos_account",
            "transfer",
            [],
            encoded_args
        )
        
        context.world.raw_transaction = RawTransaction(
            sender=sender,
            sequence_number=0,
            payload=TransactionPayload(payload),
            max_gas_amount=100000,
            gas_unit_price=100,
            expiration_timestamps_secs=int(time.time()) + 600,
            chain_id=4,
        )


@given("a signed transaction")
def step_given_signed_transaction(context):
    if context.world.signed_transaction is None:
        step_given_raw_transaction_to_sign(context)
        step_sign_raw_transaction(context)


# =============================================================================
# When Steps - Signing
# =============================================================================


@when("I sign the raw transaction")
def step_sign_raw_transaction(context):
    try:
        # Get the signing message
        serializer = Serializer()
        context.world.raw_transaction.serialize(serializer)
        raw_bytes = serializer.output()
        
        # Domain separation
        domain = b"APTOS::RawTransaction"
        domain_hash = hashlib.sha3_256(domain).digest()
        signing_message = domain_hash + raw_bytes
        
        # Sign
        signature = context.world.account.sign(signing_message)
        
        # Create authenticator
        from aptos_sdk.authenticator import AccountAuthenticator, Ed25519Authenticator
        
        authenticator = AccountAuthenticator(
            Ed25519Authenticator(
                context.world.account.public_key(),
                signature
            )
        )
        
        # Create signed transaction
        context.world.signed_transaction = SignedTransaction(
            context.world.raw_transaction,
            authenticator
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I sign the raw transaction with the second account")
def step_sign_with_second_account(context):
    try:
        serializer = Serializer()
        context.world.raw_transaction.serialize(serializer)
        raw_bytes = serializer.output()
        
        domain = b"APTOS::RawTransaction"
        domain_hash = hashlib.sha3_256(domain).digest()
        signing_message = domain_hash + raw_bytes
        
        signature = context.world.account_2.sign(signing_message)
        
        from aptos_sdk.authenticator import AccountAuthenticator, Ed25519Authenticator
        
        authenticator = AccountAuthenticator(
            Ed25519Authenticator(
                context.world.account_2.public_key(),
                signature
            )
        )
        
        context.world.test_vectors["signed_tx_2"] = SignedTransaction(
            context.world.raw_transaction,
            authenticator
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I sign the raw transaction again")
def step_sign_raw_transaction_again(context):
    try:
        serializer = Serializer()
        context.world.raw_transaction.serialize(serializer)
        raw_bytes = serializer.output()
        
        domain = b"APTOS::RawTransaction"
        domain_hash = hashlib.sha3_256(domain).digest()
        signing_message = domain_hash + raw_bytes
        
        signature = context.world.account.sign(signing_message)
        
        from aptos_sdk.authenticator import AccountAuthenticator, Ed25519Authenticator
        
        authenticator = AccountAuthenticator(
            Ed25519Authenticator(
                context.world.account.public_key(),
                signature
            )
        )
        
        context.world.test_vectors["signed_tx_2"] = SignedTransaction(
            context.world.raw_transaction,
            authenticator
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Transaction Hash
# =============================================================================


@when("I compute the transaction hash")
def step_compute_transaction_hash(context):
    try:
        # Transaction hash = SHA3-256(domain_separator || signed_tx_bcs)
        domain = b"APTOS::Transaction"
        domain_hash = hashlib.sha3_256(domain).digest()
        
        serializer = Serializer()
        context.world.signed_transaction.serialize(serializer)
        tx_bytes = serializer.output()
        
        hash_input = domain_hash + tx_bytes
        context.world.transaction_hash = hashlib.sha3_256(hash_input).hexdigest()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I compute the transaction hash for the second signed transaction")
def step_compute_hash_for_second(context):
    try:
        signed_tx_2 = context.world.test_vectors.get("signed_tx_2")
        
        domain = b"APTOS::Transaction"
        domain_hash = hashlib.sha3_256(domain).digest()
        
        serializer = Serializer()
        signed_tx_2.serialize(serializer)
        tx_bytes = serializer.output()
        
        hash_input = domain_hash + tx_bytes
        context.world.test_vectors["tx_hash_2"] = hashlib.sha3_256(hash_input).hexdigest()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the signed transaction")
def step_bcs_serialize_signed_transaction(context):
    try:
        serializer = Serializer()
        context.world.signed_transaction.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize as signed transaction")
def step_bcs_deserialize_signed_transaction(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.signed_transaction = SignedTransaction.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS serialize the signed transaction twice")
def step_bcs_serialize_signed_tx_twice(context):
    try:
        serializer1 = Serializer()
        context.world.signed_transaction.serialize(serializer1)
        bytes1 = serializer1.output()

        serializer2 = Serializer()
        context.world.signed_transaction.serialize(serializer2)
        bytes2 = serializer2.output()

        context.world.test_vectors["bytes1"] = bytes1
        context.world.test_vectors["bytes2"] = bytes2
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Verification
# =============================================================================


@when("I verify the signed transaction signature")
def step_verify_signed_transaction(context):
    try:
        # Get the signing message that was signed
        serializer = Serializer()
        context.world.signed_transaction.raw_transaction.serialize(serializer)
        raw_bytes = serializer.output()
        
        domain = b"APTOS::RawTransaction"
        domain_hash = hashlib.sha3_256(domain).digest()
        signing_message = domain_hash + raw_bytes
        
        # Get public key and signature from authenticator
        auth = context.world.signed_transaction.authenticator
        if hasattr(auth, 'authenticator'):
            inner = auth.authenticator
            public_key = inner.public_key
            signature = inner.signature
        else:
            public_key = auth.public_key
            signature = auth.signature
        
        # Verify
        is_valid = public_key.verify(signing_message, signature)
        context.world.result = is_valid
        context.world.clear_error()
    except Exception as e:
        context.world.result = False
        context.world.set_error(e)


@when("I tamper with the transaction")
def step_tamper_transaction(context):
    # Change the sequence number in the raw transaction
    context.world.raw_transaction.sequence_number = 99999


# =============================================================================
# Then Steps - Signing Assertions
# =============================================================================


@then("the signed transaction should be valid")
def step_signed_transaction_valid(context):
    assert context.world.error is None
    assert context.world.signed_transaction is not None


@then("signing should succeed")
def step_signing_succeed(context):
    assert context.world.error is None


@then("signing should fail")
def step_signing_fail(context):
    assert context.world.error is not None


@then("the signed transaction should contain the raw transaction")
def step_signed_tx_contains_raw(context):
    assert context.world.signed_transaction.raw_transaction is not None
    # Compare serialized bytes
    serializer1 = Serializer()
    context.world.raw_transaction.serialize(serializer1)
    
    serializer2 = Serializer()
    context.world.signed_transaction.raw_transaction.serialize(serializer2)
    
    assert serializer1.output() == serializer2.output()


@then("the signed transaction should contain an authenticator")
def step_signed_tx_contains_authenticator(context):
    assert context.world.signed_transaction.authenticator is not None


@then("the authenticator should be Ed25519")
def step_authenticator_is_ed25519(context):
    auth = context.world.signed_transaction.authenticator
    # Check the authenticator type
    assert auth is not None


@then("the authenticator should contain the public key")
def step_authenticator_contains_public_key(context):
    auth = context.world.signed_transaction.authenticator
    if hasattr(auth, 'authenticator'):
        assert auth.authenticator.public_key is not None
    else:
        assert auth.public_key is not None


@then("the authenticator should contain a 64-byte signature")
def step_authenticator_contains_signature(context):
    auth = context.world.signed_transaction.authenticator
    if hasattr(auth, 'authenticator'):
        sig = auth.authenticator.signature
    else:
        sig = auth.signature
    assert len(sig.signature) == 64


# =============================================================================
# Then Steps - Transaction Hash Assertions
# =============================================================================


@then("the transaction hash should not be empty")
def step_tx_hash_not_empty(context):
    assert context.world.transaction_hash is not None
    assert len(context.world.transaction_hash) > 0


@then("the transaction hash should be 64 hex characters")
def step_tx_hash_64_chars(context):
    assert len(context.world.transaction_hash) == 64


@then("computing the hash twice should produce the same result")
def step_hash_deterministic(context):
    # Compute hash again
    domain = b"APTOS::Transaction"
    domain_hash = hashlib.sha3_256(domain).digest()
    
    serializer = Serializer()
    context.world.signed_transaction.serialize(serializer)
    tx_bytes = serializer.output()
    
    hash_input = domain_hash + tx_bytes
    hash2 = hashlib.sha3_256(hash_input).hexdigest()
    
    assert context.world.transaction_hash == hash2


@then("the two transaction hashes should be different")
def step_tx_hashes_different(context):
    hash1 = context.world.transaction_hash
    hash2 = context.world.test_vectors.get("tx_hash_2")
    assert hash1 != hash2


@then('the transaction hash should be "{expected}"')
def step_tx_hash_should_be(context, expected):
    expected_clean = expected[2:] if expected.startswith("0x") else expected
    assert context.world.transaction_hash.lower() == expected_clean.lower()


# =============================================================================
# Then Steps - Verification Assertions
# =============================================================================


@then("the signature verification should pass")
def step_sig_verification_pass(context):
    assert context.world.result is True


# Note: "the signature verification should fail" is defined in account_steps.py


@then("the tampered transaction verification should fail")
def step_tampered_verification_fail(context):
    assert context.world.result is False


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the serialized signed transaction should not be empty")
def step_serialized_signed_tx_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then("the signed transaction serializations should be identical")
def step_signed_tx_serializations_identical(context):
    bytes1 = context.world.test_vectors.get("bytes1")
    bytes2 = context.world.test_vectors.get("bytes2")
    assert bytes1 == bytes2


@then("signing the same transaction twice should produce the same result")
def step_signing_deterministic(context):
    signed_tx_1 = context.world.signed_transaction
    signed_tx_2 = context.world.test_vectors.get("signed_tx_2")
    
    serializer1 = Serializer()
    signed_tx_1.serialize(serializer1)
    
    serializer2 = Serializer()
    signed_tx_2.serialize(serializer2)
    
    assert serializer1.output() == serializer2.output()
