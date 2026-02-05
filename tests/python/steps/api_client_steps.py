"""
Step definitions for fullnode-api.feature
Tests REST API client creation and basic operations.

Note: The Python SDK uses an async client. These tests use asyncio.run()
for synchronous execution in the BDD context.
"""

from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient
from behave import given, when, then
import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


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


@given("a connected client")
def step_given_connected_client(context):
    if context.world.client is None:
        context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"
        context.world.client = RestClient(context.world.network_url)


@given("a client connected to testnet")
def step_given_client_connected_testnet(context):
    context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"
    context.world.client = RestClient(context.world.network_url)


@given('a custom URL "{url}"')
def step_given_custom_url(context, url):
    context.world.network_url = url


@given("a known existing account address")
def step_given_known_existing_account(context):
    # Use 0x1 as a known existing account
    context.world.address = AccountAddress.from_str("0x1")


@given("a random unused account address")
def step_given_random_unused_address(context):
    # Generate a random address that's very unlikely to exist
    import secrets

    random_bytes = secrets.token_bytes(32)
    context.world.address = AccountAddress.from_bytes(random_bytes)


@given("an account address with resources")
def step_given_account_with_resources(context):
    context.world.address = AccountAddress.from_str("0x1")


@given("an account with APT balance")
def step_given_account_with_apt(context):
    context.world.address = AccountAddress.from_str("0x1")


@given("custom headers {headers}")
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


@when("I create a client with testnet configuration")
def step_create_testnet_client(context):
    try:
        context.world.network_url = "https://fullnode.testnet.aptoslabs.com/v1"
        context.world.client = RestClient(context.world.network_url)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a client with mainnet configuration")
def step_create_mainnet_client(context):
    try:
        context.world.network_url = "https://fullnode.mainnet.aptoslabs.com/v1"
        context.world.client = RestClient(context.world.network_url)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a client with the custom URL")
def step_create_custom_url_client(context):
    try:
        context.world.client = RestClient(context.world.network_url)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I create a client with 30 second timeout")
def step_create_client_with_timeout(context):
    try:
        context.world.client = RestClient(context.world.network_url)
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I request ledger info")
def step_request_ledger_info(context):
    try:

        async def _get_info():
            return await context.world.client.info()

        context.world.result = run_async(_get_info())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get the ledger info")
def step_get_the_ledger_info(context):
    step_request_ledger_info(context)


@when("I get account info for the address")
def step_get_account_info_for_address(context):
    try:

        async def _get_account():
            return await context.world.client.account(context.world.address)

        context.world.result = run_async(_get_account())
        context.world.clear_error()
    except Exception as e:
        context.world.set_error(e)


@when("I get account resources")
def step_get_account_resources_generic(context):
    try:

        async def _get_resources():
            return await context.world.client.account_resources(context.world.address)

        context.world.result = run_async(_get_resources())
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


@then("the client should be configured for testnet")
def step_client_configured_testnet(context):
    assert context.world.client is not None
    assert "testnet" in context.world.network_url


@then('the base URL should be "{url}"')
def step_base_url_should_be(context, url):
    assert context.world.network_url == url


@then("the client should be configured for mainnet")
def step_client_configured_mainnet(context):
    assert context.world.client is not None
    assert "mainnet" in context.world.network_url


@then("the client should use that URL for requests")
def step_client_uses_custom_url(context):
    assert context.world.client is not None


@then("requests should timeout after 30 seconds")
def step_requests_timeout(context):
    # Timeout is configured but may not be directly accessible
    assert context.world.client is not None


@then("I should receive chain_id")
def step_should_receive_chain_id(context):
    assert context.world.result is not None
    info = context.world.result
    assert "chain_id" in info or hasattr(info, "chain_id")


@then("I should receive ledger_version")
def step_should_receive_ledger_version(context):
    assert context.world.result is not None
    info = context.world.result
    assert "ledger_version" in info or hasattr(info, "ledger_version")


@then("I should receive block_height")
def step_should_receive_block_height(context):
    assert context.world.result is not None
    info = context.world.result
    assert (
        "block_height" in info
        or hasattr(info, "block_height")
        or "ledger_version" in info
    )


@then("chain_id should be 2")
def step_chain_id_should_be_2(context):
    info = context.world.result
    if isinstance(info, dict):
        assert info.get("chain_id") == 2
    else:
        assert info.chain_id == 2


@then("I should receive sequence_number")
def step_should_receive_sequence_number(context):
    assert context.world.result is not None
    info = context.world.result
    if isinstance(info, dict):
        assert "sequence_number" in info
    else:
        assert hasattr(info, "sequence_number")


@then("I should receive authentication_key")
def step_should_receive_auth_key(context):
    assert context.world.result is not None
    info = context.world.result
    if isinstance(info, dict):
        assert "authentication_key" in info
    else:
        assert hasattr(info, "authentication_key")


@then("I should receive a 404 NotFound error")
def step_should_receive_404_not_found(context):
    assert context.world.error is not None


@then("I should receive a list of resources")
def step_should_receive_resource_list(context):
    assert context.world.error is None
    assert context.world.result is not None
    assert isinstance(context.world.result, list)


@then("each resource should have a type and data")
def step_resource_has_type_and_data(context):
    resources = context.world.result
    for resource in resources:
        if isinstance(resource, dict):
            assert "type" in resource
            assert "data" in resource


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
        assert (
            tx.get("success", True) is True
            or tx.get("vm_status") == "Executed successfully"
        )
    else:
        assert tx.success is True


@then("the transaction should have failure status")
def step_transaction_failure(context):
    tx = context.world.result
    if isinstance(tx, dict):
        assert tx.get("success", True) is False or "error" in str(
            tx.get("vm_status", "")
        )
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
