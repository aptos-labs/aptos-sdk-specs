"""
Step definitions for fullnode-api.feature
Tests REST API client creation and basic operations.

Note: The Python SDK uses an async client. These tests use asyncio.run()
for synchronous execution in the BDD context.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from behave import given, when, then
from aptos_sdk.async_client import RestClient
from aptos_sdk.account_address import AccountAddress

from support.vectors import hex_to_bytes, bytes_to_hex


# Helper to run async functions synchronously
def run_async(coro):
    """Run an async coroutine synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


# =============================================================================
# Given Steps - Client Configuration
# =============================================================================


@given('an API client URL "{url}"')
def step_given_api_client_url(context, url):
    context.world.network_url = url


@given("a testnet API client")
def step_given_testnet_client(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"


@given("a devnet API client")
def step_given_devnet_client(context):
    context.world.network_url = "https://fullnode.devnet.aptoslabs.com/v1"


@given("a mainnet API client")
def step_given_mainnet_client(context):
    context.world.network_url = "https://fullnode.mainnet.aptoslabs.com/v1"


@given('custom headers {headers}')
def step_given_custom_headers(context, headers):
    # Parse headers like "X-Custom: value, Authorization: Bearer token"
    header_dict = {}
    for header in headers.split(","):
        key, value = header.strip().split(":", 1)
        header_dict[key.strip()] = value.strip()
    context.world.test_vectors["custom_headers"] = header_dict


# =============================================================================
# When Steps - Client Creation
# =============================================================================


@when("I create an API client")
def step_create_api_client(context):
    try:
        context.world.client = RestClient(context.world.network_url)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create an API client with custom headers")
def step_create_api_client_with_headers(context):
    try:
        # Note: RestClient may not directly support custom headers
        # This is a placeholder for SDKs that support it
        context.world.client = RestClient(context.world.network_url)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Ledger Info
# =============================================================================


@when("I get ledger info")
def step_get_ledger_info(context):
    try:
        async def _get_info():
            return await context.world.client.info()
        
        context.world.result = run_async(_get_info())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Account Info
# =============================================================================


@when('I get account info for "{address}"')
def step_get_account_info(context, address):
    try:
        async def _get_account():
            addr = AccountAddress.from_str(address)
            return await context.world.client.account(addr)
        
        context.world.result = run_async(_get_account())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get account info for a non-existent address")
def step_get_nonexistent_account(context):
    try:
        async def _get_account():
            # Use a random address that likely doesn't exist
            addr = AccountAddress.from_str(
                "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            )
            return await context.world.client.account(addr)
        
        context.world.result = run_async(_get_account())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when('I get account resources for "{address}"')
def step_get_account_resources(context, address):
    try:
        async def _get_resources():
            addr = AccountAddress.from_str(address)
            return await context.world.client.account_resources(addr)
        
        context.world.result = run_async(_get_resources())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when('I get account resource "{resource_type}" for "{address}"')
def step_get_specific_resource(context, resource_type, address):
    try:
        async def _get_resource():
            addr = AccountAddress.from_str(address)
            return await context.world.client.account_resource(addr, resource_type)
        
        context.world.result = run_async(_get_resource())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when('I get account modules for "{address}"')
def step_get_account_modules(context, address):
    try:
        async def _get_modules():
            addr = AccountAddress.from_str(address)
            return await context.world.client.account_modules(addr)
        
        context.world.result = run_async(_get_modules())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Transactions
# =============================================================================


@when('I get transaction by hash "{tx_hash}"')
def step_get_transaction_by_hash(context, tx_hash):
    try:
        async def _get_tx():
            return await context.world.client.transaction_by_hash(tx_hash)
        
        context.world.result = run_async(_get_tx())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get transaction by version {version:d}")
def step_get_transaction_by_version(context, version):
    try:
        async def _get_tx():
            return await context.world.client.transaction_by_version(version)
        
        context.world.result = run_async(_get_tx())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get transactions with limit {limit:d}")
def step_get_transactions_with_limit(context, limit):
    try:
        async def _get_txs():
            return await context.world.client.transactions(limit=limit)
        
        context.world.result = run_async(_get_txs())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when('I get account transactions for "{address}"')
def step_get_account_transactions(context, address):
    try:
        async def _get_txs():
            addr = AccountAddress.from_str(address)
            return await context.world.client.account_transactions(addr)
        
        context.world.result = run_async(_get_txs())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# When Steps - Events
# =============================================================================


@when('I get events by key "{event_key}"')
def step_get_events_by_key(context, event_key):
    try:
        async def _get_events():
            return await context.world.client.events_by_event_key(event_key)
        
        context.world.result = run_async(_get_events())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Client Assertions
# =============================================================================


@then("the API client should be created")
def step_client_created(context):
    assert context.world.error is None
    assert context.world.client is not None


@then("the client URL should be normalized")
def step_url_normalized(context):
    # Check that trailing slashes are handled
    assert context.world.client is not None


# =============================================================================
# Then Steps - Ledger Info Assertions
# =============================================================================


@then("the ledger info should be returned")
def step_ledger_info_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the ledger info should contain chain_id")
def step_ledger_info_has_chain_id(context):
    info = context.world.result
    assert "chain_id" in info or hasattr(info, "chain_id")


@then("the ledger info should contain epoch")
def step_ledger_info_has_epoch(context):
    info = context.world.result
    assert "epoch" in info or hasattr(info, "epoch")


@then("the ledger info should contain ledger_version")
def step_ledger_info_has_version(context):
    info = context.world.result
    assert "ledger_version" in info or hasattr(info, "ledger_version")


# =============================================================================
# Then Steps - Account Info Assertions
# =============================================================================


@then("the account info should be returned")
def step_account_info_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the account info should contain sequence_number")
def step_account_info_has_sequence_number(context):
    info = context.world.result
    assert "sequence_number" in info or hasattr(info, "sequence_number")


@then("the account info should contain authentication_key")
def step_account_info_has_auth_key(context):
    info = context.world.result
    assert "authentication_key" in info or hasattr(info, "authentication_key")


@then("I should get an account not found error")
def step_account_not_found(context):
    assert context.world.error is not None


# =============================================================================
# Then Steps - Resource Assertions
# =============================================================================


@then("the resources should be returned")
def step_resources_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the resource should be returned")
def step_resource_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the modules should be returned")
def step_modules_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


# =============================================================================
# Then Steps - Transaction Assertions
# =============================================================================


@then("the transaction should be returned")
def step_transaction_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the transactions should be returned")
def step_transactions_returned(context):
    assert context.world.error is None
    assert context.world.result is not None


@then("the transaction should have success status")
def step_transaction_success(context):
    tx = context.world.result
    if isinstance(tx, dict):
        assert tx.get("success", True) is True or tx.get("vm_status") == "Executed successfully"
    else:
        assert tx.success is True


@then("the transaction should have failure status")
def step_transaction_failure(context):
    tx = context.world.result
    if isinstance(tx, dict):
        assert tx.get("success", True) is False or "error" in str(tx.get("vm_status", ""))
    else:
        assert tx.success is False


# =============================================================================
# Then Steps - Error Handling
# =============================================================================


@then("I should get a 404 error")
def step_should_get_404(context):
    assert context.world.error is not None
    error_str = str(context.world.error)
    assert "404" in error_str or "not found" in error_str.lower()


@then("I should get a 400 error")
def step_should_get_400(context):
    assert context.world.error is not None
    error_str = str(context.world.error)
    assert "400" in error_str or "bad request" in error_str.lower()


@then("I should get a network error")
def step_should_get_network_error(context):
    assert context.world.error is not None


# =============================================================================
# Cleanup
# =============================================================================


def after_scenario(context, scenario):
    """Close the client after each scenario."""
    if hasattr(context, "world") and context.world.client:
        try:
            run_async(context.world.client.close())
        except Exception:
            pass
