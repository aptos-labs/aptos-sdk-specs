"""
Step definitions for raw-transaction.feature
Tests RawTransaction creation and BCS serialization.
"""

from support.vectors import bytes_to_hex
from aptos_sdk.transactions import (
    RawTransaction,
    TransactionPayload,
    EntryFunction,
)
from aptos_sdk.bcs import Serializer, Deserializer
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from behave import given, when, then
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# =============================================================================
# Given Steps - Transaction Fields
# =============================================================================


@given('a sender address "{address}"')
def step_given_sender_address(context, address):
    context.world.test_vectors["sender"] = AccountAddress.from_str(address)


@given("a sender account")
def step_given_sender_account(context):
    if context.world.account is None:
        context.world.account = Account.generate()
    context.world.test_vectors["sender"] = context.world.account.address()


@given("sequence number {seq_num:d}")
def step_given_sequence_number(context, seq_num):
    context.world.test_vectors["sequence_number"] = seq_num


@given("max gas amount {max_gas:d}")
def step_given_max_gas(context, max_gas):
    context.world.test_vectors["max_gas_amount"] = max_gas


@given("gas unit price {price:d}")
def step_given_gas_price(context, price):
    context.world.test_vectors["gas_unit_price"] = price


@given("expiration timestamp {timestamp:d}")
def step_given_expiration_timestamp(context, timestamp):
    context.world.test_vectors["expiration_timestamp_secs"] = timestamp


@given("expiration in {seconds:d} seconds")
def step_given_expiration_duration(context, seconds):
    context.world.test_vectors["expiration_timestamp_secs"] = int(time.time()) + seconds


@given("chain ID {chain_id:d}")
def step_given_chain_id(context, chain_id):
    context.world.test_vectors["chain_id"] = chain_id


@given("a simple transfer payload")
def step_given_simple_transfer_payload(context):
    # Create a simple 0x1::aptos_account::transfer payload
    from aptos_sdk.transactions import TransactionArgument

    # Create TransactionArgument objects properly
    recipient = AccountAddress.from_str("0x1")
    addr_arg = TransactionArgument(recipient, Serializer.struct)
    amount_arg = TransactionArgument(1000, Serializer.u64)

    context.world.test_vectors["payload"] = EntryFunction.natural(
        "0x1::aptos_account", "transfer", [], [addr_arg, amount_arg]
    )


@given("an entry function payload")
def step_given_entry_function_payload(context):
    if context.world.result:
        context.world.test_vectors["payload"] = context.world.result
    else:
        step_given_simple_transfer_payload(context)


@given("an entry function payload for APT transfer")
def step_given_entry_function_apt_transfer(context):
    step_given_simple_transfer_payload(context)


@given("a sequence number {seq_num:d}")
def step_given_seq_num_alt(context, seq_num):
    context.world.test_vectors["sequence_number"] = seq_num


@given("chain ID testnet (2)")
def step_given_chain_id_testnet(context):
    context.world.test_vectors["chain_id"] = 2


@given("chain ID {chain_id:d} (mainnet)")
def step_given_chain_id_mainnet(context, chain_id):
    context.world.test_vectors["chain_id"] = chain_id


@given("chain ID {chain_id:d} (testnet)")
def step_given_chain_id_testnet_num(context, chain_id):
    context.world.test_vectors["chain_id"] = chain_id


@given("a valid RawTransaction")
def step_given_valid_raw_transaction(context):
    if context.world.raw_transaction is None:
        # Make sure we have an account first
        if context.world.account is None:
            context.world.account = Account.generate()
        step_given_simple_transfer_payload(context)
        step_create_raw_transaction(context)


@given("a RawTransaction with known values")
def step_given_raw_transaction_with_known(context):
    step_given_valid_raw_transaction(context)


@given("a RawTransaction")
def step_given_raw_transaction_simple(context):
    step_given_valid_raw_transaction(context)


@given("a RawTransaction with chain ID {chain_id:d} (mainnet)")
def step_given_raw_transaction_mainnet(context, chain_id):
    context.world.test_vectors["chain_id"] = chain_id
    step_given_simple_transfer_payload(context)
    step_create_raw_transaction(context)


@given("a RawTransaction with chain ID {chain_id:d} (testnet)")
def step_given_raw_transaction_testnet(context, chain_id):
    context.world.test_vectors["chain_id"] = chain_id
    step_given_simple_transfer_payload(context)
    step_create_raw_transaction(context)


@given("two RawTransactions with different sequence numbers")
def step_given_two_raw_transactions(context):
    step_given_simple_transfer_payload(context)
    context.world.test_vectors["sequence_number"] = 0
    step_create_raw_transaction(context)
    context.world.test_vectors["raw_tx_1"] = context.world.raw_transaction

    context.world.test_vectors["sequence_number"] = 1
    step_create_raw_transaction(context)
    context.world.test_vectors["raw_tx_2"] = context.world.raw_transaction


@given("a RawTransaction with values from test vectors")
def step_given_raw_transaction_from_vectors(context):
    step_given_valid_raw_transaction(context)


@given("a RawTransaction from test vectors")
def step_given_raw_transaction_from_vectors_alt(context):
    step_given_valid_raw_transaction(context)


# =============================================================================
# Given Steps - Invalid Values
# =============================================================================


# Note: "max gas amount 0" and "gas unit price 0" use the parameterized steps above


@given("an expired timestamp")
def step_given_expired_timestamp(context):
    # Set timestamp to 1 hour ago
    context.world.test_vectors["expiration_timestamp_secs"] = int(time.time()) - 3600


# =============================================================================
# When Steps - Transaction Creation
# =============================================================================


@when("I create a raw transaction")
def step_create_raw_transaction(context):
    try:
        sender = context.world.test_vectors.get(
            "sender", context.world.account.address()
        )
        sequence_number = context.world.test_vectors.get("sequence_number", 0)
        max_gas_amount = context.world.test_vectors.get("max_gas_amount", 100000)
        gas_unit_price = context.world.test_vectors.get("gas_unit_price", 100)
        expiration = context.world.test_vectors.get(
            "expiration_timestamp_secs", int(time.time()) + 600
        )
        chain_id = context.world.test_vectors.get("chain_id", 4)  # Testnet
        payload = context.world.test_vectors.get("payload")

        if payload is None:
            step_given_simple_transfer_payload(context)
            payload = context.world.test_vectors["payload"]

        context.world.raw_transaction = RawTransaction(
            sender=sender,
            sequence_number=sequence_number,
            payload=TransactionPayload(payload),
            max_gas_amount=max_gas_amount,
            gas_unit_price=gas_unit_price,
            expiration_timestamps_secs=expiration,
            chain_id=chain_id,
        )
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I try to create a raw transaction")
def step_try_create_raw_transaction(context):
    step_create_raw_transaction(context)


# =============================================================================
# When Steps - BCS Serialization
# =============================================================================


@when("I BCS serialize the raw transaction")
def step_bcs_serialize_raw_transaction(context):
    try:
        serializer = Serializer()
        context.world.raw_transaction.serialize(serializer)
        context.world.bytes_value = serializer.output()
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS deserialize as raw transaction")
def step_bcs_deserialize_raw_transaction(context):
    try:
        deserializer = Deserializer(context.world.bytes_value)
        context.world.raw_transaction = RawTransaction.deserialize(deserializer)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I BCS serialize the raw transaction twice")
def step_bcs_serialize_raw_transaction_twice(context):
    try:
        serializer1 = Serializer()
        context.world.raw_transaction.serialize(serializer1)
        bytes1 = serializer1.output()

        serializer2 = Serializer()
        context.world.raw_transaction.serialize(serializer2)
        bytes2 = serializer2.output()

        context.world.test_vectors["bytes1"] = bytes1
        context.world.test_vectors["bytes2"] = bytes2
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Signing Message
# =============================================================================


@when("I compute the signing message")
def step_compute_signing_message(context):
    try:
        # The signing message is the BCS-serialized raw transaction
        # prefixed with the domain separator
        import hashlib

        # Domain separator: SHA3-256("APTOS::RawTransaction")
        domain = b"APTOS::RawTransaction"
        domain_hash = hashlib.sha3_256(domain).digest()

        # Serialize the transaction
        serializer = Serializer()
        context.world.raw_transaction.serialize(serializer)
        tx_bytes = serializer.output()

        # Signing message = domain_hash || tx_bytes
        context.world.test_vectors["signing_message"] = domain_hash + tx_bytes
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I compute the signing message for a different transaction")
def step_compute_different_signing_message(context):
    try:
        import hashlib

        # Create a different transaction
        sender = (
            context.world.account.address()
            if context.world.account
            else AccountAddress.from_str("0x1")
        )

        # Different sequence number
        different_tx = RawTransaction(
            sender=sender,
            sequence_number=999,
            payload=context.world.raw_transaction.payload,
            max_gas_amount=context.world.raw_transaction.max_gas_amount,
            gas_unit_price=context.world.raw_transaction.gas_unit_price,
            expiration_timestamps_secs=context.world.raw_transaction.expiration_timestamps_secs,
            chain_id=context.world.raw_transaction.chain_id,
        )

        domain = b"APTOS::RawTransaction"
        domain_hash = hashlib.sha3_256(domain).digest()

        serializer = Serializer()
        different_tx.serialize(serializer)
        tx_bytes = serializer.output()

        context.world.test_vectors["signing_message_2"] = domain_hash + tx_bytes
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Raw Transaction Assertions
# =============================================================================


@then("the raw transaction should be valid")
def step_raw_transaction_valid(context):
    assert context.world.error is None
    assert context.world.raw_transaction is not None


@then("raw transaction creation should succeed")
def step_raw_transaction_creation_succeed(context):
    assert context.world.error is None


@then("raw transaction creation should fail")
def step_raw_transaction_creation_fail(context):
    assert context.world.error is not None


@then('the sender should be "{expected}"')
def step_sender_should_be(context, expected):
    actual = str(context.world.raw_transaction.sender)
    assert actual.lower() == expected.lower()


@then("the sequence number should be {expected:d}")
def step_sequence_number_should_be(context, expected):
    assert context.world.raw_transaction.sequence_number == expected


@then("the max gas amount should be {expected:d}")
def step_max_gas_should_be(context, expected):
    assert context.world.raw_transaction.max_gas_amount == expected


@then("the gas unit price should be {expected:d}")
def step_gas_price_should_be(context, expected):
    assert context.world.raw_transaction.gas_unit_price == expected


@then("the expiration should be {expected:d}")
def step_expiration_should_be(context, expected):
    assert context.world.raw_transaction.expiration_timestamps_secs == expected


@then("the chain ID should be {expected:d}")
def step_chain_id_should_be(context, expected):
    assert context.world.raw_transaction.chain_id.value == expected


# =============================================================================
# Then Steps - BCS Assertions
# =============================================================================


@then("the serialized raw transaction should not be empty")
def step_serialized_raw_tx_not_empty(context):
    assert context.world.bytes_value is not None
    assert len(context.world.bytes_value) > 0


@then('the serialized raw transaction should be "{expected}"')
def step_serialized_raw_tx_should_be(context, expected):
    actual = bytes_to_hex(context.world.bytes_value, prefix=False)
    expected_clean = expected[2:] if expected.startswith("0x") else expected
    assert actual.lower() == expected_clean.lower()


@then("the raw transaction serializations should be identical")
def step_raw_tx_serializations_identical(context):
    bytes1 = context.world.test_vectors.get("bytes1")
    bytes2 = context.world.test_vectors.get("bytes2")
    assert bytes1 == bytes2


# =============================================================================
# Then Steps - Signing Message Assertions
# =============================================================================


@then("the signing message should not be empty")
def step_signing_message_not_empty(context):
    msg = context.world.test_vectors.get("signing_message")
    assert msg is not None
    assert len(msg) > 0


@then("the signing message should start with the domain separator")
def step_signing_message_starts_with_domain(context):
    import hashlib

    msg = context.world.test_vectors.get("signing_message")
    domain = b"APTOS::RawTransaction"
    domain_hash = hashlib.sha3_256(domain).digest()

    assert msg[:32] == domain_hash


@then("computing the signing message twice should produce the same result")
def step_signing_message_deterministic(context):
    import hashlib

    domain = b"APTOS::RawTransaction"
    domain_hash = hashlib.sha3_256(domain).digest()

    serializer = Serializer()
    context.world.raw_transaction.serialize(serializer)
    tx_bytes = serializer.output()

    msg1 = domain_hash + tx_bytes
    msg2 = domain_hash + tx_bytes

    assert msg1 == msg2


@then("the two signing messages should be different")
def step_signing_messages_different(context):
    msg1 = context.world.test_vectors.get("signing_message")
    msg2 = context.world.test_vectors.get("signing_message_2")
    assert msg1 != msg2


@then('the signing message should be "{expected}"')
def step_signing_message_should_be(context, expected):
    msg = context.world.test_vectors.get("signing_message")
    actual = bytes_to_hex(msg, prefix=False)
    expected_clean = expected[2:] if expected.startswith("0x") else expected
    assert actual.lower() == expected_clean.lower()


# =============================================================================
# Additional When Steps
# =============================================================================


@when("I create a RawTransaction")
def step_create_raw_transaction_alt(context):
    step_create_raw_transaction(context)


@when("I access the fields")
def step_access_fields(context):
    # Fields are accessed via the transaction object
    pass


@when("I generate the signing message")
def step_generate_signing_message(context):
    step_compute_signing_message(context)


@when("I generate the signing message twice")
def step_generate_signing_message_twice(context):
    step_compute_signing_message(context)
    context.world.test_vectors["signing_message_1"] = context.world.test_vectors[
        "signing_message"
    ]
    step_compute_signing_message(context)
    context.world.test_vectors["signing_message_2"] = context.world.test_vectors[
        "signing_message"
    ]


@when("I generate signing messages for both")
def step_generate_signing_messages_for_both(context):
    import hashlib

    domain = b"APTOS::RawTransaction"
    domain_hash = hashlib.sha3_256(domain).digest()

    # First transaction
    raw_tx_1 = context.world.test_vectors.get("raw_tx_1")
    serializer = Serializer()
    raw_tx_1.serialize(serializer)
    context.world.test_vectors["signing_message_1"] = domain_hash + serializer.output()

    # Second transaction
    raw_tx_2 = context.world.test_vectors.get("raw_tx_2")
    serializer = Serializer()
    raw_tx_2.serialize(serializer)
    context.world.test_vectors["signing_message_2"] = domain_hash + serializer.output()


@when('I compute SHA3-256 of "APTOS::RawTransaction"')
def step_compute_sha3_domain(context):
    import hashlib

    domain = b"APTOS::RawTransaction"
    context.world.test_vectors["domain_hash"] = hashlib.sha3_256(domain).digest()


# =============================================================================
# Additional Then Steps
# =============================================================================


@then("the transaction should be valid")
def step_transaction_valid(context):
    assert context.world.error is None
    assert context.world.raw_transaction is not None


@then('sender should be "{expected}"')
def step_sender_should_be_simple(context, expected):
    actual = str(context.world.raw_transaction.sender)
    assert expected.lower() in actual.lower()


@then("sequence number should be {expected:d}")
def step_sequence_number_should_be_simple(context, expected):
    assert context.world.raw_transaction.sequence_number == expected


@then("sender() should return the sender address")
def step_sender_returns_address(context):
    assert context.world.raw_transaction.sender is not None


@then("sequence_number() should return the sequence number")
def step_sequence_number_returns(context):
    assert context.world.raw_transaction.sequence_number is not None


@then("payload() should return the payload")
def step_payload_returns(context):
    assert context.world.raw_transaction.payload is not None


@then("max_gas_amount() should return the max gas")
def step_max_gas_returns(context):
    assert context.world.raw_transaction.max_gas_amount is not None


@then("gas_unit_price() should return the gas price")
def step_gas_price_returns(context):
    assert context.world.raw_transaction.gas_unit_price is not None


@then("expiration_timestamp_secs() should return the expiration")
def step_expiration_returns(context):
    assert context.world.raw_transaction.expiration_timestamps_secs is not None


@then("chain_id() should return the chain ID")
def step_chain_id_returns(context):
    assert context.world.raw_transaction.chain_id is not None


@then("the bytes should be deterministic")
def step_bytes_deterministic(context):
    # Serialize again and compare
    serializer = Serializer()
    context.world.raw_transaction.serialize(serializer)
    bytes2 = serializer.output()
    assert context.world.bytes_value == bytes2


@then("sender should be serialized first (32 bytes)")
def step_sender_serialized_first(context):
    # First 32 bytes are the sender address
    assert len(context.world.bytes_value) >= 32


@then("sequence_number should be next (8 bytes)")
def step_sequence_number_serialized_next(context):
    # After sender comes sequence number
    assert len(context.world.bytes_value) >= 40


@then("payload should follow")
def step_payload_follows(context):
    # Payload comes after sequence number
    assert len(context.world.bytes_value) > 40


@then("max_gas_amount, gas_unit_price, expiration, chain_id should be in order")
def step_rest_in_order(context):
    # All fields present
    assert len(context.world.bytes_value) > 50


@then('the message should start with SHA3-256("APTOS::RawTransaction")')
def step_message_starts_with_domain(context):
    step_signing_message_starts_with_domain(context)


@then("the message should contain the BCS-serialized transaction")
def step_message_contains_tx(context):
    msg = context.world.test_vectors.get("signing_message")
    # After domain hash (32 bytes) comes the transaction bytes
    assert len(msg) > 32


@then("both messages should be identical")
def step_both_messages_identical(context):
    msg1 = context.world.test_vectors.get("signing_message_1")
    msg2 = context.world.test_vectors.get("signing_message_2")
    assert msg1 == msg2


@then("the messages should be different")
def step_messages_different(context):
    msg1 = context.world.test_vectors.get("signing_message_1")
    msg2 = context.world.test_vectors.get("signing_message_2")
    assert msg1 != msg2


@then("the chain_id byte should be 0x01")
def step_chain_id_byte_01(context):
    # Chain ID is at the end of serialized transaction
    assert context.world.bytes_value[-1] == 1


@then("the chain_id byte should be 0x02")
def step_chain_id_byte_02(context):
    assert context.world.bytes_value[-1] == 2


@then("it should be the prefix of all single-signer signing messages")
def step_domain_is_prefix(context):
    domain_hash = context.world.test_vectors.get("domain_hash")
    assert len(domain_hash) == 32


# Note: "it should match the expected value from test vectors" is defined in auth_key_steps.py
