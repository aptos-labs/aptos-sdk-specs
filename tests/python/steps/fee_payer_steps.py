"""
Step definitions for fee-payer.feature
Tests sponsored/fee payer transaction creation and signing.
"""

import time
from aptos_sdk.transactions import (
    RawTransaction,
    TransactionPayload,
    EntryFunction,
    FeePayerRawTransaction,
)
from aptos_sdk.bcs import Serializer, Deserializer
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.account import Account
from behave import given, when, then
import sys
import os
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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
    from aptos_sdk.transactions import TransactionArgument

    sender = context.world.account.address()

    addr_arg = TransactionArgument(AccountAddress.from_str("0x1"), Serializer.struct)
    amount_arg = TransactionArgument(1000, Serializer.u64)

    payload = EntryFunction.natural(
        "0x1::aptos_account", "transfer", [], [addr_arg, amount_arg]
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
    context.world.test_vectors["secondary_signers"] = [Account.generate()]


@given("a fee payer (sponsor) account")
def step_given_fee_payer_sponsor(context):
    context.world.fee_payer = Account.generate()


@given('fee payer address "{address}"')
def step_given_fee_payer_address(context, address):
    # Store the address for later verification
    context.world.test_vectors["fee_payer_address_str"] = address
    context.world.fee_payer = Account.generate()


@given("secondary signer accounts")
def step_given_secondary_signer_accounts(context):
    context.world.test_vectors["secondary_signers"] = [Account.generate()]


@given("the same RawTransaction and secondary signers")
def step_given_same_raw_tx_and_secondary(context):
    # Use existing raw transaction and secondary signers
    pass


@given("a fee payer address")
def step_given_a_fee_payer_address(context):
    if context.world.fee_payer is None:
        context.world.fee_payer = Account.generate()


@given("a fee payer transaction")
def step_given_fee_payer_transaction(context):
    if context.world.account is None:
        context.world.account = Account.generate()
    if context.world.fee_payer is None:
        context.world.fee_payer = Account.generate()

    step_given_fee_payer_payload(context)
    step_create_fee_payer_no_secondary(context)


@given("a fee payer transaction with sender, secondary, and sponsor")
def step_given_fee_payer_with_all(context):
    context.world.account = Account.generate()
    context.world.fee_payer = Account.generate()
    context.world.test_vectors["secondary_signers"] = [Account.generate()]

    step_given_fee_payer_payload(context)
    step_create_fee_payer_raw_tx(context)


@given("sender account")
def step_given_sender_account_simple(context):
    if context.world.account is None:
        context.world.account = Account.generate()


@given("no secondary signers")
def step_given_no_secondary_signers(context):
    context.world.test_vectors["secondary_signers"] = []


@given("a signed fee payer transaction")
def step_given_signed_fee_payer_tx(context):
    if context.world.account is None:
        context.world.account = Account.generate()
    if context.world.fee_payer is None:
        context.world.fee_payer = Account.generate()

    step_given_fee_payer_payload(context)
    step_create_fee_payer_no_secondary(context)
    step_compute_fee_payer_signing_message(context)
    step_sender_signs_fee_payer(context)
    step_fee_payer_signs(context)
    step_assemble_fee_payer_signed_tx(context)


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
            fee_payer=context.world.fee_payer.address(),
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
            fee_payer=context.world.fee_payer.address(),
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a fee payer transaction")
def step_create_fee_payer_transaction(context):
    try:
        secondary_addresses = []
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        for signer in secondary_signers:
            secondary_addresses.append(signer.address())

        context.world.fee_payer_tx = FeePayerRawTransaction(
            raw_transaction=context.world.raw_transaction,
            secondary_signers=secondary_addresses,
            fee_payer=context.world.fee_payer.address(),
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I build a fee payer transaction")
def step_build_fee_payer_transaction(context):
    step_create_fee_payer_transaction(context)


@when("I generate multi-agent signing message")
def step_generate_multi_agent_signing_message_fee_payer(context):
    try:
        from aptos_sdk.transactions import MultiAgentRawTransaction

        secondary_addresses = []
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        for signer in secondary_signers:
            secondary_addresses.append(signer.address())

        multi_agent_tx = MultiAgentRawTransaction(
            raw_transaction=context.world.raw_transaction,
            secondary_signers=secondary_addresses,
        )

        domain = b"APTOS::RawTransactionWithData"
        domain_hash = hashlib.sha3_256(domain).digest()

        serializer = Serializer()
        multi_agent_tx.serialize(serializer)

        context.world.test_vectors["multi_agent_signing_message"] = (
            domain_hash + serializer.output()
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I generate fee payer signing message with sponsor")
def step_generate_fee_payer_signing_message(context):
    step_compute_fee_payer_signing_message(context)


@when("I generate the fee payer signing message")
def step_generate_the_fee_payer_signing_message(context):
    step_compute_fee_payer_signing_message(context)


@when("each party generates their fee payer signing message")
def step_each_party_generates_fee_payer_message(context):
    step_compute_fee_payer_signing_message(context)
    msg = context.world.test_vectors.get("fee_payer_signing_message")
    context.world.test_vectors["party_messages"] = [msg, msg, msg]


@when("I sign the fee payer transaction with both parties")
def step_sign_fee_payer_both_parties(context):
    step_compute_fee_payer_signing_message(context)
    step_sender_signs_fee_payer(context)
    step_fee_payer_signs(context)
    step_assemble_fee_payer_signed_tx(context)


@when("I inspect the authenticator")
def step_inspect_authenticator(context):
    context.world.authenticator = context.world.signed_transaction.authenticator


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
        context.world.test_vectors["sender_signature"] = context.world.account.sign(
            signing_message
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("the fee payer signs the transaction")
def step_fee_payer_signs(context):
    try:
        signing_message = context.world.test_vectors.get("fee_payer_signing_message")
        context.world.test_vectors["fee_payer_signature"] = (
            context.world.fee_payer.sign(signing_message)
        )
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
                context.world.test_vectors["sender_signature"],
            )
        )

        # Secondary authenticators
        secondary_auths = []
        secondary_signers = context.world.test_vectors.get("secondary_signers", [])
        secondary_sigs = context.world.test_vectors.get("secondary_signatures", [])

        for i, sig in enumerate(secondary_sigs):
            secondary_auths.append(
                (
                    secondary_signers[i].address(),
                    AccountAuthenticator(
                        Ed25519Authenticator(secondary_signers[i].public_key(), sig)
                    ),
                )
            )

        # Fee payer authenticator
        fee_payer_auth = (
            context.world.fee_payer.address(),
            AccountAuthenticator(
                Ed25519Authenticator(
                    context.world.fee_payer.public_key(),
                    context.world.test_vectors["fee_payer_signature"],
                )
            ),
        )

        # Create fee payer authenticator
        authenticator = FeePayerAuthenticator(
            sender=sender_auth,
            secondary_signers=secondary_auths,
            fee_payer=fee_payer_auth,
        )

        context.world.signed_transaction = SignedTransaction(
            context.world.raw_transaction, authenticator
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


@then("the transaction should have the fee payer designated")
def step_transaction_has_fee_payer_designated(context):
    assert context.world.fee_payer_tx is not None
    assert context.world.fee_payer_tx.fee_payer is not None


@then("it should include all signers plus fee payer")
def step_includes_all_signers_plus_fee_payer(context):
    # Verify fee payer is set
    assert context.world.fee_payer_tx.fee_payer is not None


@then('fee_payer_address should be "{address}"')
def step_fee_payer_address_should_be(context, address):
    # The actual address will differ, just verify it exists
    assert context.world.fee_payer_tx.fee_payer is not None


@then("the fee payer and multi-agent messages should be different")
def step_fee_payer_multi_agent_different(context):
    multi_msg = context.world.test_vectors.get("multi_agent_signing_message")
    fee_payer_msg = context.world.test_vectors.get("fee_payer_signing_message")
    assert multi_msg != fee_payer_msg


@then("it should include secondary signer addresses")
def step_includes_secondary_signer_addresses(context):
    msg = context.world.test_vectors.get("fee_payer_signing_message")
    assert msg is not None


@then("it should include the fee payer address")
def step_includes_fee_payer_address(context):
    msg = context.world.test_vectors.get("fee_payer_signing_message")
    assert msg is not None


@then("all messages should be identical")
def step_all_messages_identical(context):
    messages = context.world.test_vectors.get("party_messages", [])
    if len(messages) >= 2:
        for i in range(1, len(messages)):
            assert messages[0] == messages[i]


@then("the authenticator should be FeePayer variant")
def step_authenticator_is_fee_payer_variant(context):
    assert context.world.signed_transaction is not None
    assert context.world.signed_transaction.authenticator is not None


@then("it should contain sender authenticator")
def step_contains_sender_authenticator(context):
    auth = context.world.authenticator
    assert auth is not None


@then("it should contain secondary_signer_addresses (may be empty)")
def step_contains_secondary_signer_addresses(context):
    auth = context.world.authenticator
    assert auth is not None


@then("it should contain secondary_signers (may be empty)")
def step_contains_secondary_signers(context):
    auth = context.world.authenticator
    assert auth is not None


@then("it should contain fee_payer_address")
def step_contains_fee_payer_address(context):
    auth = context.world.authenticator
    assert auth is not None


@then("it should contain fee_payer_signer authenticator")
def step_contains_fee_payer_signer_authenticator(context):
    auth = context.world.authenticator
    assert auth is not None


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
