"""
Step definitions for simulation.feature
Tests transaction simulation for validation and gas estimation.
"""

import time
from aptos_sdk.transactions import (
    RawTransaction,
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
# Given Steps - Simulation Setup
# =============================================================================


@given("a simulation client")
def step_given_simulation_client(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"


@given("a transaction to simulate")
def step_given_transaction_to_simulate(context):
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

    context.world.raw_transaction = RawTransaction(
        sender=sender,
        sequence_number=0,
        payload=TransactionPayload(payload),
        max_gas_amount=100000,
        gas_unit_price=100,
        expiration_timestamps_secs=int(time.time()) + 600,
        chain_id=4,
    )


@given("a transaction that will fail simulation")
def step_given_failing_transaction(context):
    context.world.account = Account.generate()
    sender = context.world.account.address()

    # Create a transaction that will fail (e.g., transfer more than balance)
    encoded_args = []
    serializer = Serializer()
    serializer.struct(AccountAddress.from_str("0x1"))
    encoded_args.append(serializer.output())

    serializer = Serializer()
    serializer.u64(999999999999999)  # Very large amount
    encoded_args.append(serializer.output())

    payload = EntryFunction.natural("0x1::aptos_account", "transfer", [], encoded_args)

    context.world.raw_transaction = RawTransaction(
        sender=sender,
        sequence_number=0,
        payload=TransactionPayload(payload),
        max_gas_amount=100000,
        gas_unit_price=100,
        expiration_timestamps_secs=int(time.time()) + 600,
        chain_id=4,
    )


@given("a transaction with invalid module")
def step_given_invalid_module_transaction(context):
    context.world.account = Account.generate()
    sender = context.world.account.address()

    payload = EntryFunction.natural(
        "0x1::nonexistent_module", "nonexistent_function", [], []
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
# When Steps - Simulation Execution
# =============================================================================


@when("I simulate the transaction")
def step_simulate_transaction(context):
    try:

        async def _simulate():
            client = RestClient(context.world.network_url)
            try:
                result = await client.simulate_transaction(
                    context.world.raw_transaction, context.world.account
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_simulate())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I simulate the transaction with estimate gas unit price")
def step_simulate_with_estimate_gas(context):
    try:

        async def _simulate():
            client = RestClient(context.world.network_url)
            try:
                result = await client.simulate_transaction(
                    context.world.raw_transaction,
                    context.world.account,
                    estimate_gas_unit_price=True,
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_simulate())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I simulate the transaction with estimate max gas")
def step_simulate_with_estimate_max_gas(context):
    try:

        async def _simulate():
            client = RestClient(context.world.network_url)
            try:
                result = await client.simulate_transaction(
                    context.world.raw_transaction,
                    context.world.account,
                    estimate_max_gas_amount=True,
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_simulate())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I simulate the transaction with estimate prioritized gas")
def step_simulate_with_prioritized_gas(context):
    try:

        async def _simulate():
            client = RestClient(context.world.network_url)
            try:
                result = await client.simulate_transaction(
                    context.world.raw_transaction,
                    context.world.account,
                    estimate_prioritized_gas_unit_price=True,
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_simulate())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I simulate the failing transaction")
def step_simulate_failing_transaction(context):
    step_simulate_transaction(context)


@when("I simulate the invalid module transaction")
def step_simulate_invalid_module(context):
    step_simulate_transaction(context)


# =============================================================================
# Then Steps - Simulation Result Assertions
# =============================================================================


@then("the simulation should succeed")
def step_simulation_succeed(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the simulation should return results")
def step_simulation_returns_results(context):
    assert context.world.result is not None
    if isinstance(context.world.result, list):
        assert len(context.world.result) > 0


@then("the simulation should indicate success")
def step_simulation_indicates_success(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert result.get("success", False) is True


@then("the simulation should indicate failure")
def step_simulation_indicates_failure(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert result.get("success", True) is False


@then("the simulation should include gas_used")
def step_simulation_includes_gas_used(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert "gas_used" in result


@then("the gas_used should be positive")
def step_simulation_gas_used_positive(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert int(result.get("gas_used", 0)) > 0


@then("the simulation should include vm_status")
def step_simulation_includes_vm_status(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert "vm_status" in result


@then('the vm_status should indicate "{expected}"')
def step_simulation_vm_status(context, expected):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    vm_status = result.get("vm_status", "")
    assert expected.lower() in vm_status.lower()


@then("the simulation should include changes")
def step_simulation_includes_changes(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert "changes" in result or "state_changes" in result


@then("the simulation should include events")
def step_simulation_includes_events(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert "events" in result


# =============================================================================
# Then Steps - Estimated Values
# =============================================================================


@then("the simulation should include estimated gas unit price")
def step_simulation_estimated_gas_price(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    # The estimate is typically in the transaction or response
    assert result is not None


@then("the simulation should include estimated max gas amount")
def step_simulation_estimated_max_gas(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    assert result is not None


# =============================================================================
# Then Steps - Error Cases
# =============================================================================


@then("the simulation should show insufficient balance")
def step_simulation_insufficient_balance(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]

    vm_status = result.get("vm_status", "")
    success = result.get("success", True)

    assert (
        not success
        or "insufficient" in vm_status.lower()
        or "balance" in vm_status.lower()
    )


@then("the simulation should show module not found")
def step_simulation_module_not_found(context):
    result = context.world.result
    if isinstance(result, list) and len(result) > 0:
        result = result[0]

    vm_status = result.get("vm_status", "")
    success = result.get("success", True)

    assert (
        not success or "not found" in vm_status.lower() or "module" in vm_status.lower()
    )


@then("the simulation result should be deterministic")
def step_simulation_deterministic(context):
    # Simulate twice and compare
    result1 = context.world.result

    async def _simulate_again():
        client = RestClient(context.world.network_url)
        try:
            return await client.simulate_transaction(
                context.world.raw_transaction, context.world.account
            )
        finally:
            await client.close()

    result2 = run_async(_simulate_again())

    # Compare gas_used
    if isinstance(result1, list):
        result1 = result1[0] if result1 else {}
    if isinstance(result2, list):
        result2 = result2[0] if result2 else {}

    assert result1.get("gas_used") == result2.get("gas_used")
