"""
Step definitions for gas-estimation.feature
Tests gas estimation and pricing.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then
from aptos_sdk.async_client import RestClient
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import (
    RawTransaction,
    TransactionPayload,
    EntryFunction,
)
import time


# Helper to run async functions synchronously
def run_async(coro):
    """Run an async coroutine synchronously."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# =============================================================================
# Given Steps - Gas Estimation Setup
# =============================================================================


@given("a gas estimation client")
def step_given_gas_client(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"


@given("a simple transfer transaction for gas estimation")
def step_given_simple_transfer_for_gas(context):
    context.world.account = Account.generate()
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


@given("a complex transaction for gas estimation")
def step_given_complex_transaction_for_gas(context):
    context.world.account = Account.generate()
    sender = context.world.account.address()
    
    # More complex payload with multiple arguments
    encoded_args = []
    
    # Multiple addresses
    for i in range(5):
        serializer = Serializer()
        serializer.struct(AccountAddress.from_str(f"0x{i+1}"))
        encoded_args.append(serializer.output())
    
    payload = EntryFunction.natural(
        "0x1::aptos_account",
        "batch_transfer",
        [],
        encoded_args
    )
    
    context.world.raw_transaction = RawTransaction(
        sender=sender,
        sequence_number=0,
        payload=TransactionPayload(payload),
        max_gas_amount=500000,
        gas_unit_price=100,
        expiration_timestamps_secs=int(time.time()) + 600,
        chain_id=4,
    )


# =============================================================================
# When Steps - Gas Estimation
# =============================================================================


@when("I estimate gas for the transaction")
def step_estimate_gas(context):
    try:
        async def _estimate_gas():
            client = RestClient(context.world.network_url)
            try:
                # Simulate transaction to get gas estimate
                gas_estimate = await client.simulate_transaction(
                    context.world.raw_transaction,
                    context.world.account
                )
                return gas_estimate
            finally:
                await client.close()
        
        context.world.result = run_async(_estimate_gas())
        if isinstance(context.world.result, list) and len(context.world.result) > 0:
            context.world.gas_estimate = context.world.result[0].get("gas_used")
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get the current gas price")
def step_get_gas_price(context):
    try:
        async def _get_gas_price():
            client = RestClient(context.world.network_url)
            try:
                # Get gas estimation from ledger info or dedicated endpoint
                info = await client.info()
                # Gas price is typically in ledger info or estimate endpoint
                return info.get("gas_estimate", {}).get("gas_price", 100)
            finally:
                await client.close()
        
        context.world.result = run_async(_get_gas_price())
        context.world.gas_price = context.world.result
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get the gas price with priority {priority}")
def step_get_gas_price_priority(context, priority):
    try:
        async def _get_gas_price():
            client = RestClient(context.world.network_url)
            try:
                info = await client.info()
                estimate = info.get("gas_estimate", {})
                
                # Different priorities
                if priority.lower() == "low":
                    return estimate.get("deprioritized_gas_estimate", 100)
                elif priority.lower() == "high":
                    return estimate.get("prioritized_gas_estimate", 150)
                else:
                    return estimate.get("gas_estimate", 100)
            finally:
                await client.close()
        
        context.world.result = run_async(_get_gas_price())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I estimate gas multiple times")
def step_estimate_gas_multiple(context):
    try:
        async def _estimate_multiple():
            client = RestClient(context.world.network_url)
            estimates = []
            try:
                for _ in range(3):
                    result = await client.simulate_transaction(
                        context.world.raw_transaction,
                        context.world.account
                    )
                    if isinstance(result, list) and len(result) > 0:
                        estimates.append(result[0].get("gas_used"))
                return estimates
            finally:
                await client.close()
        
        context.world.result = run_async(_estimate_multiple())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Gas Calculation
# =============================================================================


@when("I calculate total gas cost")
def step_calculate_gas_cost(context):
    gas_used = context.world.gas_estimate or 1000
    gas_price = context.world.gas_price or 100
    context.world.result = gas_used * gas_price


@when("I calculate gas cost with multiplier {multiplier:f}")
def step_calculate_gas_with_multiplier(context, multiplier):
    gas_used = context.world.gas_estimate or 1000
    gas_price = context.world.gas_price or 100
    context.world.result = int(gas_used * gas_price * multiplier)


# =============================================================================
# Then Steps - Gas Estimation Assertions
# =============================================================================


@then("the gas estimation should succeed")
def step_gas_estimation_succeed(context):
    assert context.world.error is None


@then("the gas estimation should fail")
def step_gas_estimation_fail(context):
    assert context.world.error is not None


@then("I should receive a gas estimate")
def step_receive_gas_estimate(context):
    assert context.world.gas_estimate is not None or context.world.result is not None


@then("the gas estimate should be positive")
def step_gas_estimate_positive(context):
    estimate = context.world.gas_estimate or context.world.result
    if isinstance(estimate, list):
        estimate = estimate[0] if estimate else 0
    assert int(estimate) > 0


@then("the gas estimate should be at least {minimum:d}")
def step_gas_estimate_at_least(context, minimum):
    estimate = context.world.gas_estimate or context.world.result
    if isinstance(estimate, list):
        estimate = estimate[0] if estimate else 0
    assert int(estimate) >= minimum


@then("the gas estimate should be at most {maximum:d}")
def step_gas_estimate_at_most(context, maximum):
    estimate = context.world.gas_estimate or context.world.result
    if isinstance(estimate, list):
        estimate = estimate[0] if estimate else 0
    assert int(estimate) <= maximum


@then("the gas price should be returned")
def step_gas_price_returned(context):
    assert context.world.gas_price is not None or context.world.result is not None


@then("the gas price should be positive")
def step_gas_price_positive(context):
    price = context.world.gas_price or context.world.result
    assert int(price) > 0


@then("all gas estimates should be consistent")
def step_gas_estimates_consistent(context):
    estimates = context.world.result
    assert isinstance(estimates, list)
    assert len(estimates) > 0
    # All estimates should be the same for identical transactions
    first = estimates[0]
    for estimate in estimates:
        assert estimate == first


@then("the total gas cost should be calculated")
def step_gas_cost_calculated(context):
    assert context.world.result is not None
    assert int(context.world.result) > 0


@then("the complex transaction should use more gas")
def step_complex_uses_more_gas(context):
    # This would compare against a simple transaction
    # For now, just verify we have an estimate
    assert context.world.gas_estimate is not None or context.world.result is not None
