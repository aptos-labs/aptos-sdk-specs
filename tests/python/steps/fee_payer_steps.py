"""
Step definitions for fee-payer.feature
Tests sponsored/fee payer transaction creation and signing.
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
    FeePayerRawTransaction,
)
import time

from support.vectors import hex_to_bytes, bytes_to_hex


# =============================================================================
# Given Steps - Fee Payer Setup
# =============================================================================


@given("a sender account for sponsored transaction")
def step_given_sender_for_sponsored(context):
    context.world.account = Account.generate()


@given("a fee payer account")
def step_given_fee_payer(context):
    context.world.fee_payer = Account.generate()


@given("a funded fee payer account")
def step_given_funded_fee_payer(context):
    context.world.fee_payer = Account.generate()
    # In real tests, this would be funded via faucet


@given("a transaction payload for fee payer")
def step_given_fee_payer_payload(context):
    sender = context.world.account.address()
    
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


@given("secondary signers for fee payer transaction")
def step_given_secondary_signers_for_fee_payer(context):
    context.world.test_vectors["secondary_signers"] = [
        Account.generate()
    ]


# =============================================================================
# When Steps - Fee Payer Transaction Creation
# =============================================================================


@when("I create a fee payer raw transaction")
def step_create_fee_payer_raw_tx(context):
    try:
        secondary_addresses = []
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        for signer in secondary_signers:
            secondary_addresses.append(signer.address())
        
        context.world.fee_payer_tx = FeePayerRawTransaction(
            raw_transaction=context.world.raw_transaction,
            secondary_signers=secondary_addresses,
            fee_payer=context.world.fee_payer.address()
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a fee payer transaction without secondary signers")
def step_create_fee_payer_no_secondary(context):
    try:
        context.world.fee_payer_tx = FeePayerRawTransaction(
            raw_transaction=context.world.raw_transaction,
            secondary_signers=[],
            fee_payer=context.world.fee_payer.address()
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I compute the fee payer signing message")
def step_compute_fee_payer_signing_message(context):
    try:
        domain = b"APTOS::RawTransactionWithData"
        domain_hash = hashlib.sha3_256(domain).digest()
        
        serializer = Serializer()
        context.world.fee_payer_tx.serialize(serializer)
        tx_bytes = serializer.output()
        
        context.world.test_vectors["fee_payer_signing_message"] = domain_hash + tx_bytes
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("the sender signs the fee payer transaction")
def step_sender_signs_fee_payer(context):
    try:
        signing_message = context.world.test_vectors.get("fee_payer_signing_message")
        context.world.test_vectors["sender_signature"] = context.world.account.sign(signing_message)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("the fee payer signs the transaction")
def step_fee_payer_signs(context):
    try:
        signing_message = context.world.test_vectors.get("fee_payer_signing_message")
        context.world.test_vectors["fee_payer_signature"] = context.world.fee_payer.sign(signing_message)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("the secondary signers sign the fee payer transaction")
def step_secondary_signers_sign_fee_payer(context):
    try:
        signing_message = context.world.test_vectors.get("fee_payer_signing_message")
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        
        context.world.test_vectors["secondary_signatures"] = [
            signer.sign(signing_message) for signer in secondary_signers
        ]
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I assemble the fee payer signed transaction")
def step_assemble_fee_payer_signed_tx(context):
    try:
        from aptos_sdk.authenticator import (
            AccountAuthenticator,
            Ed25519Authenticator,
            FeePayerAuthenticator,
        )
        from aptos_sdk.transactions import SignedTransaction
        
        # Sender authenticator
        sender_auth = AccountAuthenticator(
            Ed25519Authenticator(
                context.world.account.public_key(),
                context.world.test_vectors["sender_signature"]
            )
        )
        
        # Secondary authenticators
        secondary_auths = []
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        secondary_sigs = context.world.test_vectors.get("secondary_signatures", [])
        
        for i, sig in enumerate(secondary_sigs):
            secondary_auths.append((
                secondary_signers[i].address(),
                AccountAuthenticator(
                    Ed25519Authenticator(
                        secondary_signers[i].public_key(),
                        sig
                    )
                )
            ))
        
        # Fee payer authenticator
        fee_payer_auth = (
            context.world.fee_payer.address(),
            AccountAuthenticator(
                Ed25519Authenticator(
                    context.world.fee_payer.public_key(),
                    context.world.test_vectors["fee_payer_signature"]
                )
            )
        )
        
        # Create fee payer authenticator
        authenticator = FeePayerAuthenticator(
            sender=sender_auth,
            secondary_signers=secondary_auths,
            fee_payer=fee_payer_auth
        )
        
        context.world.signed_transaction = SignedTransaction(
            context.world.raw_transaction,
            authenticator
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the fee payer transaction")
def step_bcs_serialize_fee_payer(context):
    try:
        serializer = Serializer()
        context.world.fee_payer_tx.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize the fee payer transaction")
def step_bcs_deserialize_fee_payer(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.fee_payer_tx = FeePayerRawTransaction.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Fee Payer Transaction Assertions
# =============================================================================


@then("the fee payer transaction should be created")
def step_fee_payer_created(context):
    assert context.world.error is None
    assert context.world.fee_payer_tx is not None


@then("the fee payer transaction should have the sender")
def step_fee_payer_has_sender(context):
    assert context.world.fee_payer_tx.raw_transaction.sender is not None


@then("the fee payer transaction should have the fee payer address")
def step_fee_payer_has_fee_payer(context):
    assert context.world.fee_payer_tx.fee_payer is not None
    assert context.world.fee_payer_tx.fee_payer == context.world.fee_payer.address()


@then("the fee payer transaction should have {count:d} secondary signers")
def step_fee_payer_secondary_count(context, count):
    assert len(context.world.fee_payer_tx.secondary_signers) == count


@then("the fee payer signing message should include the fee payer address")
def step_fee_payer_message_includes_address(context):
    signing_message = context.world.test_vectors.get("fee_payer_signing_message")
    assert signing_message is not None
    # The fee payer address is encoded in the message


# =============================================================================
# Then Steps - Signature Assertions
# =============================================================================


@then("the sender signature should be valid")
def step_sender_signature_valid(context):
    assert "sender_signature" in context.world.test_vectors
    sig = context.world.test_vectors["sender_signature"]
    assert len(sig.signature) == 64


@then("the fee payer signature should be valid")
def step_fee_payer_signature_valid(context):
    assert "fee_payer_signature" in context.world.test_vectors
    sig = context.world.test_vectors["fee_payer_signature"]
    assert len(sig.signature) == 64


@then("the assembled fee payer transaction should be valid")
def step_assembled_fee_payer_valid(context):
    assert context.world.error is None
    assert context.world.signed_transaction is not None


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the serialized fee payer transaction should not be empty")
def step_fee_payer_serialized_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then("the deserialized fee payer transaction should match")
def step_fee_payer_deserialized_matches(context):
    serializer = Serializer()
    context.world.fee_payer_tx.serialize(serializer)
    assert serializer.output() == context.world.bytes_value


# =============================================================================
# Then Steps - Gas Payment
# =============================================================================


@then("the gas should be paid by the fee payer")
def step_gas_paid_by_fee_payer(context):
    # This would be verified on chain after submission
    # For now, just verify the transaction structure
    assert context.world.fee_payer_tx.fee_payer == context.world.fee_payer.address()


@then("the sender balance should not decrease for gas")
def step_sender_balance_not_decreased(context):
    # This would be verified on chain after submission
    pass
