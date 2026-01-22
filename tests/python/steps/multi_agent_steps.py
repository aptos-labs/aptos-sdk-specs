"""
Step definitions for multi-agent.feature
Tests multi-agent transaction creation and signing.
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
    TransactionPayload,
    EntryFunction,
    MultiAgentRawTransaction,
)
import time

from support.vectors import hex_to_bytes, bytes_to_hex


# =============================================================================
# Given Steps - Multi-Agent Setup
# =============================================================================


@given("a primary sender account")
def step_given_primary_sender(context):
    context.world.account = Account.generate()


@given("a secondary signer account")
def step_given_secondary_signer(context):
    context.world.account_2 = Account.generate()


@given("multiple secondary signer accounts")
def step_given_multiple_secondary_signers(context):
    context.world.test_vectors["secondary_signers"] = [
        Account.generate(),
        Account.generate(),
        Account.generate()
    ]


@given("a multi-agent transaction payload")
def step_given_multi_agent_payload(context):
    sender = context.world.account.address()
    secondary = context.world.account_2.address() if context.world.account_2 else Account.generate().address()
    
    # Create a payload that requires multiple signers
    encoded_args = []
    
    # First signer's address
    serializer = Serializer()
    serializer.struct(secondary)
    encoded_args.append(serializer.output())
    
    # Amount
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


# =============================================================================
# When Steps - Multi-Agent Transaction Creation
# =============================================================================


@when("I create a multi-agent raw transaction")
def step_create_multi_agent_raw_tx(context):
    try:
        secondary_addresses = []
        if context.world.account_2:
            secondary_addresses.append(context.world.account_2.address())
        
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        for signer in secondary_signers:
            secondary_addresses.append(signer.address())
        
        context.world.multi_agent_tx = MultiAgentRawTransaction(
            raw_transaction=context.world.raw_transaction,
            secondary_signers=secondary_addresses
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I compute the multi-agent signing message")
def step_compute_multi_agent_signing_message(context):
    try:
        # Multi-agent signing message includes secondary signer addresses
        domain = b"APTOS::RawTransactionWithData"
        domain_hash = hashlib.sha3_256(domain).digest()
        
        # Serialize the multi-agent transaction
        serializer = Serializer()
        context.world.multi_agent_tx.serialize(serializer)
        tx_bytes = serializer.output()
        
        context.world.test_vectors["multi_agent_signing_message"] = domain_hash + tx_bytes
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("the primary sender signs the transaction")
def step_primary_sender_signs(context):
    try:
        signing_message = context.world.test_vectors.get("multi_agent_signing_message")
        context.world.test_vectors["primary_signature"] = context.world.account.sign(signing_message)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("the secondary signer signs the transaction")
def step_secondary_signer_signs(context):
    try:
        signing_message = context.world.test_vectors.get("multi_agent_signing_message")
        context.world.test_vectors["secondary_signature"] = context.world.account_2.sign(signing_message)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("all secondary signers sign the transaction")
def step_all_secondary_signers_sign(context):
    try:
        signing_message = context.world.test_vectors.get("multi_agent_signing_message")
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        
        context.world.test_vectors["secondary_signatures"] = [
            signer.sign(signing_message) for signer in secondary_signers
        ]
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I assemble the multi-agent signed transaction")
def step_assemble_multi_agent_signed_tx(context):
    try:
        from aptos_sdk.authenticator import (
            AccountAuthenticator,
            Ed25519Authenticator,
            MultiAgentAuthenticator,
        )
        from aptos_sdk.transactions import SignedTransaction
        
        # Primary authenticator
        primary_auth = AccountAuthenticator(
            Ed25519Authenticator(
                context.world.account.public_key(),
                context.world.test_vectors["primary_signature"]
            )
        )
        
        # Secondary authenticators
        secondary_auths = []
        
        if "secondary_signature" in context.world.test_vectors:
            secondary_auths.append((
                context.world.account_2.address(),
                AccountAuthenticator(
                    Ed25519Authenticator(
                        context.world.account_2.public_key(),
                        context.world.test_vectors["secondary_signature"]
                    )
                )
            ))
        
        if "secondary_signatures" in context.world.test_vectors:
            secondary_signers = context.world.test_vectors.get("secondary_signers", [])
            for i, sig in enumerate(context.world.test_vectors["secondary_signatures"]):
                secondary_auths.append((
                    secondary_signers[i].address(),
                    AccountAuthenticator(
                        Ed25519Authenticator(
                            secondary_signers[i].public_key(),
                            sig
                        )
                    )
                ))
        
        # Create multi-agent authenticator
        multi_agent_auth = MultiAgentAuthenticator(
            sender=primary_auth,
            secondary_signers=secondary_auths
        )
        
        context.world.signed_transaction = SignedTransaction(
            context.world.raw_transaction,
            multi_agent_auth
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the multi-agent transaction")
def step_bcs_serialize_multi_agent(context):
    try:
        serializer = Serializer()
        context.world.multi_agent_tx.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize the multi-agent transaction")
def step_bcs_deserialize_multi_agent(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.multi_agent_tx = MultiAgentRawTransaction.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Multi-Agent Transaction Assertions
# =============================================================================


@then("the multi-agent transaction should be created")
def step_multi_agent_created(context):
    assert context.world.error is None
    assert context.world.multi_agent_tx is not None


@then("the multi-agent transaction should have the primary sender")
def step_multi_agent_has_primary_sender(context):
    assert context.world.multi_agent_tx.raw_transaction.sender is not None


@then("the multi-agent transaction should have {count:d} secondary signers")
def step_multi_agent_secondary_count(context, count):
    assert len(context.world.multi_agent_tx.secondary_signers) == count


@then("the multi-agent signing message should be different from single signer")
def step_multi_agent_different_signing_message(context):
    # Single signer message
    domain = b"APTOS::RawTransaction"
    domain_hash = hashlib.sha3_256(domain).digest()
    
    serializer = Serializer()
    context.world.raw_transaction.serialize(serializer)
    single_message = domain_hash + serializer.output()
    
    multi_message = context.world.test_vectors.get("multi_agent_signing_message")
    
    assert single_message != multi_message


# =============================================================================
# Then Steps - Signature Assertions
# =============================================================================


@then("the primary signature should be valid")
def step_primary_signature_valid(context):
    assert "primary_signature" in context.world.test_vectors
    sig = context.world.test_vectors["primary_signature"]
    assert len(sig.signature) == 64


@then("the secondary signature should be valid")
def step_secondary_signature_valid(context):
    assert "secondary_signature" in context.world.test_vectors
    sig = context.world.test_vectors["secondary_signature"]
    assert len(sig.signature) == 64


@then("all secondary signatures should be valid")
def step_all_secondary_signatures_valid(context):
    sigs = context.world.test_vectors.get("secondary_signatures", [])
    assert len(sigs) > 0
    for sig in sigs:
        assert len(sig.signature) == 64


@then("the assembled transaction should be valid")
def step_assembled_tx_valid(context):
    assert context.world.error is None
    assert context.world.signed_transaction is not None


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the serialized multi-agent transaction should not be empty")
def step_multi_agent_serialized_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then("the deserialized multi-agent transaction should match")
def step_multi_agent_deserialized_matches(context):
    # Serialize again and compare
    serializer = Serializer()
    context.world.multi_agent_tx.serialize(serializer)
    assert serializer.output() == context.world.bytes_value
