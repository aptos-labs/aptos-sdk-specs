"""
Step definitions for faucet.feature
Tests faucet client for funding accounts on testnet/devnet.
"""

from aptos_sdk.account_address import AccountAddress
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient, FaucetClient
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
# Given Steps - Faucet Configuration
# =============================================================================


@given("a testnet faucet client")
def step_given_testnet_faucet(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"
    context.world.faucet_url = "https://faucet.testnet.aptoslabs.com"


@given("a devnet faucet client")
def step_given_devnet_faucet(context):
    context.world.network_url = "https://fullnode.devnet.aptoslabs.com/v1"
    context.world.faucet_url = "https://faucet.devnet.aptoslabs.com"


@given('a faucet URL "{url}"')
def step_given_faucet_url(context, url):
    context.world.faucet_url = url


@given("an invalid faucet URL")
def step_given_invalid_faucet_url(context):
    context.world.faucet_url = "https://invalid.faucet.example.com"


@given("a new account to fund")
def step_given_new_account_to_fund(context):
    context.world.account = Account.generate()


@given("an existing account to fund")
def step_given_existing_account_to_fund(context):
    if context.world.account is None:
        context.world.account = Account.generate()


# =============================================================================
# When Steps - Funding
# =============================================================================


@when("I request funds from the faucet")
def step_request_funds(context):
    try:

        async def _fund():
            client = RestClient(context.world.network_url)
            faucet = FaucetClient(context.world.faucet_url, client)
            try:
                result = await faucet.fund_account(
                    context.world.account.address(), 100_000_000  # 1 APT
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_fund())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I request {amount:d} octas from the faucet")
def step_request_specific_amount(context, amount):
    try:

        async def _fund():
            client = RestClient(context.world.network_url)
            faucet = FaucetClient(context.world.faucet_url, client)
            try:
                result = await faucet.fund_account(
                    context.world.account.address(), amount
                )
                return result
            finally:
                await client.close()

        context.world.result = run_async(_fund())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when('I fund address "{address}"')
def step_fund_address(context, address):
    try:

        async def _fund():
            client = RestClient(context.world.network_url)
            faucet = FaucetClient(context.world.faucet_url, client)
            try:
                addr = AccountAddress.from_str(address)
                result = await faucet.fund_account(addr, 100_000_000)
                return result
            finally:
                await client.close()

        context.world.result = run_async(_fund())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I request funds multiple times")
def step_request_funds_multiple(context):
    try:

        async def _fund_multiple():
            client = RestClient(context.world.network_url)
            faucet = FaucetClient(context.world.faucet_url, client)
            results = []
            try:
                for _ in range(3):
                    result = await faucet.fund_account(
                        context.world.account.address(), 100_000_000
                    )
                    results.append(result)
                return results
            finally:
                await client.close()

        context.world.result = run_async(_fund_multiple())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Balance Check
# =============================================================================


@when("I check the account balance")
def step_check_balance(context):
    try:

        async def _get_balance():
            client = RestClient(context.world.network_url)
            try:
                balance = await client.account_balance(context.world.account.address())
                return balance
            finally:
                await client.close()

        context.world.result = run_async(_get_balance())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I check the balance before funding")
def step_check_balance_before(context):
    try:

        async def _get_balance():
            client = RestClient(context.world.network_url)
            try:
                balance = await client.account_balance(context.world.account.address())
                return balance
            except Exception:
                return 0  # Account doesn't exist yet
            finally:
                await client.close()

        context.world.test_vectors["balance_before"] = run_async(_get_balance())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I check the balance after funding")
def step_check_balance_after(context):
    try:

        async def _get_balance():
            client = RestClient(context.world.network_url)
            try:
                balance = await client.account_balance(context.world.account.address())
                return balance
            finally:
                await client.close()

        context.world.test_vectors["balance_after"] = run_async(_get_balance())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Funding Assertions
# =============================================================================


@then("the funding should succeed")
def step_funding_succeed(context):
    assert context.world.error is None


@then("the funding should fail")
def step_funding_fail(context):
    assert context.world.error is not None


@then("I should receive transaction hashes")
def step_receive_fund_tx_hashes(context):
    assert context.world.result is not None
    # Faucet returns transaction hashes
    if isinstance(context.world.result, list):
        assert len(context.world.result) > 0


@then("the account should exist on chain")
def step_account_exists(context):
    try:

        async def _check_exists():
            client = RestClient(context.world.network_url)
            try:
                await client.account(context.world.account.address())
                return True
            except Exception:
                return False
            finally:
                await client.close()

        exists = run_async(_check_exists())
        assert exists, "Account should exist on chain"
    except Exception as e:
        assert False, f"Failed to check account: {e}"


@then("the account balance should be greater than 0")
def step_balance_greater_than_zero(context):
    assert context.world.result is not None
    assert int(context.world.result) > 0


@then("the account balance should be at least {amount:d}")
def step_balance_at_least(context, amount):
    assert context.world.result is not None
    assert int(context.world.result) >= amount


@then("the balance should have increased")
def step_balance_increased(context):
    before = context.world.test_vectors.get("balance_before", 0)
    after = context.world.test_vectors.get("balance_after", 0)
    assert int(after) > int(before)


@then("all funding requests should succeed")
def step_all_funding_succeed(context):
    assert context.world.error is None
    assert context.world.result is not None
    if isinstance(context.world.result, list):
        assert len(context.world.result) == 3


# =============================================================================
# Then Steps - Error Assertions
# =============================================================================


@then("I should get a rate limit error")
def step_rate_limit_error(context):
    assert context.world.error is not None
    error_str = str(context.world.error).lower()
    assert "rate" in error_str or "limit" in error_str or "429" in error_str


@then("I should get a faucet unavailable error")
def step_faucet_unavailable_error(context):
    assert context.world.error is not None


@then("I should get an invalid address error")
def step_invalid_address_faucet_error(context):
    assert context.world.error is not None
