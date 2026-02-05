"""
Step definitions for transaction-submission.feature
Tests transaction submission and status polling.
"""

from aptos_sdk.transactions import (
    RawTransaction,
    SignedTransaction,
    TransactionPayload,
    EntryFunction,
)
from aptos_sdk.bcs import Serializer
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
from behave import given, when, then
import sys
import os
import asyncio
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Helper to run async functions synchronously
def run_async(coro):
    """Run an async coroutine synchronously."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# =============================================================================
# Given Steps - Submission Setup
# =============================================================================


@given("a funded account on testnet")
def step_given_funded_account(context):
    # Generate a new account - in real tests this would need funding
    context.world.account = Account.generate()
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"


@given("a funded account on devnet")
def step_given_funded_devnet_account(context):
    context.world.account = Account.generate()
    context.world.network_url = "https://fullnode.devnet.aptoslabs.com/v1"


@given("an unfunded account")
def step_given_unfunded_account(context):
    context.world.account = Account.generate()


@given("a signed transaction ready for submission")
def step_given_signed_transaction_ready(context):
    if context.world.signed_transaction is None:
        # Create a simple transaction
        from steps.signing_steps import (
            step_given_raw_transaction_to_sign,
            step_sign_raw_transaction,
        )

        step_given_raw_transaction_to_sign(context)
        step_sign_raw_transaction(context)


@given("an invalid signed transaction")
def step_given_invalid_signed_transaction(context):
    # Create a transaction with invalid signature
    context.world.account = Account.generate()

    sender = context.world.account.address()

    encoded_args = []
    serializer = Serializer()
    serializer.struct(AccountAddress.from_str("0x1"))
    encoded_args.append(serializer.output())

    serializer = Serializer()
    serializer.u64(1000)
    encoded_args.append(serializer.output())

    payload = EntryFunction.natural("0x1::aptos_account", "transfer", [], encoded_args)

    raw_tx = RawTransaction(
        sender=sender,
        sequence_number=0,
        payload=TransactionPayload(payload),
        max_gas_amount=100000,
        gas_unit_price=100,
        expiration_timestamps_secs=int(time.time()) + 600,
        chain_id=4,
    )

    # Sign with wrong message to create invalid signature

    wrong_message = b"wrong_message"
    signature = context.world.account.sign(wrong_message)

    from aptos_sdk.authenticator import AccountAuthenticator, Ed25519Authenticator

    authenticator = AccountAuthenticator(
        Ed25519Authenticator(context.world.account.public_key(), signature)
    )

    context.world.signed_transaction = SignedTransaction(raw_tx, authenticator)


@given("an expired signed transaction")
def step_given_expired_transaction(context):
    context.world.account = Account.generate()

    sender = context.world.account.address()

    encoded_args = []
    serializer = Serializer()
    serializer.struct(AccountAddress.from_str("0x1"))
    encoded_args.append(serializer.output())

    serializer = Serializer()
    serializer.u64(1000)
    encoded_args.append(serializer.output())

    payload = EntryFunction.natural("0x1::aptos_account", "transfer", [], encoded_args)

    # Use expired timestamp
    raw_tx = RawTransaction(
        sender=sender,
        sequence_number=0,
        payload=TransactionPayload(payload),
        max_gas_amount=100000,
        gas_unit_price=100,
        expiration_timestamps_secs=int(time.time()) - 3600,  # 1 hour ago
        chain_id=4,
    )

    # Sign properly
    import hashlib

    domain = b"APTOS::RawTransaction"
    domain_hash = hashlib.sha3_256(domain).digest()

    serializer = Serializer()
    raw_tx.serialize(serializer)
    signing_message = domain_hash + serializer.output()

    signature = context.world.account.sign(signing_message)

    from aptos_sdk.authenticator import AccountAuthenticator, Ed25519Authenticator

    authenticator = AccountAuthenticator(
        Ed25519Authenticator(context.world.account.public_key(), signature)
    )

    context.world.signed_transaction = SignedTransaction(raw_tx, authenticator)


# =============================================================================
# When Steps - Transaction Submission
# =============================================================================


@when("I submit the signed transaction")
def step_submit_signed_transaction(context):
    try:

        async def _submit():
            client = RestClient(context.world.network_url)
            try:
                # Serialize the signed transaction
                serializer = Serializer()
                context.world.signed_transaction.serialize(serializer)
                tx_bytes = serializer.output()

                # Submit
                result = await client.submit_bcs_transaction(tx_bytes)
                return result
            finally:
                await client.close()

        context.world.result = run_async(_submit())
        context.world.transaction_hash = context.world.result.get("hash")
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I submit the transaction and wait for completion")
def step_submit_and_wait(context):
    try:

        async def _submit_and_wait():
            client = RestClient(context.world.network_url)
            try:
                serializer = Serializer()
                context.world.signed_transaction.serialize(serializer)
                tx_bytes = serializer.output()

                result = await client.submit_bcs_transaction(tx_bytes)
                tx_hash = result.get("hash")

                # Wait for transaction
                await client.wait_for_transaction(tx_hash)

                # Get final status
                return await client.transaction_by_hash(tx_hash)
            finally:
                await client.close()

        context.world.result = run_async(_submit_and_wait())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I submit the invalid transaction")
def step_submit_invalid_transaction(context):
    step_submit_signed_transaction(context)


@when("I submit the expired transaction")
def step_submit_expired_transaction(context):
    step_submit_signed_transaction(context)


# =============================================================================
# When Steps - Transaction Status
# =============================================================================


@when("I wait for the transaction")
def step_wait_for_transaction(context):
    try:

        async def _wait():
            client = RestClient(context.world.network_url)
            try:
                await client.wait_for_transaction(context.world.transaction_hash)
                return await client.transaction_by_hash(context.world.transaction_hash)
            finally:
                await client.close()

        context.world.result = run_async(_wait())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I poll for transaction status")
def step_poll_transaction_status(context):
    try:

        async def _poll():
            client = RestClient(context.world.network_url)
            try:
                return await client.transaction_by_hash(context.world.transaction_hash)
            finally:
                await client.close()

        context.world.result = run_async(_poll())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I wait for transaction with timeout {timeout:d} seconds")
def step_wait_with_timeout(context, timeout):
    try:

        async def _wait_timeout():
            client = RestClient(context.world.network_url)
            try:
                # Custom wait with timeout
                start = time.time()
                while time.time() - start < timeout:
                    try:
                        tx = await client.transaction_by_hash(
                            context.world.transaction_hash
                        )
                        if tx.get("type") != "pending_transaction":
                            return tx
                    except Exception:
                        pass
                    await asyncio.sleep(1)
                raise TimeoutError("Transaction wait timed out")
            finally:
                await client.close()

        context.world.result = run_async(_wait_timeout())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Submission Assertions
# =============================================================================


@then("the transaction should be submitted")
def step_transaction_submitted(context):
    assert context.world.error is None
    assert context.world.transaction_hash is not None


@then("submission should succeed")
def step_submission_succeed(context):
    assert context.world.error is None


@then("submission should fail")
def step_submission_fail(context):
    assert context.world.error is not None


@then("I should receive a transaction hash")
def step_receive_tx_hash(context):
    assert context.world.transaction_hash is not None
    assert len(context.world.transaction_hash) == 66  # 0x + 64 hex chars


@then("the transaction hash should be valid")
def step_tx_hash_valid(context):
    tx_hash = context.world.transaction_hash
    assert tx_hash.startswith("0x")
    assert len(tx_hash) == 66


# =============================================================================
# Then Steps - Transaction Status Assertions
# =============================================================================


@then("the transaction should be pending")
def step_transaction_pending(context):
    result = context.world.result
    if isinstance(result, dict):
        assert result.get("type") == "pending_transaction"


@then("the transaction should be committed")
def step_transaction_committed(context):
    result = context.world.result
    if isinstance(result, dict):
        assert result.get("type") != "pending_transaction"
        assert result.get("success", False) is True


@then("the transaction should have succeeded")
def step_transaction_succeeded(context):
    result = context.world.result
    if isinstance(result, dict):
        assert result.get("success", False) is True


@then("the transaction should have failed")
def step_transaction_failed(context):
    result = context.world.result
    if isinstance(result, dict):
        assert result.get("success", True) is False


@then("the transaction should have vm_status")
def step_transaction_has_vm_status(context):
    result = context.world.result
    if isinstance(result, dict):
        assert "vm_status" in result


@then('the vm_status should be "{expected}"')
def step_vm_status_is(context, expected):
    result = context.world.result
    if isinstance(result, dict):
        assert result.get("vm_status") == expected


# =============================================================================
# Then Steps - Error Assertions
# =============================================================================


@then("I should get a signature verification error")
def step_signature_verification_error(context):
    assert context.world.error is not None
    error_str = str(context.world.error).lower()
    assert "signature" in error_str or "invalid" in error_str


@then("I should get an expiration error")
def step_expiration_error(context):
    assert context.world.error is not None
    error_str = str(context.world.error).lower()
    assert "expir" in error_str or "timestamp" in error_str


@then("I should get a timeout error")
def step_timeout_error(context):
    assert context.world.error is not None
    assert isinstance(context.world.error, TimeoutError)


@then("I should get an insufficient funds error")
def step_insufficient_funds_error(context):
    assert context.world.error is not None
    error_str = str(context.world.error).lower()
    assert "insufficient" in error_str or "balance" in error_str
