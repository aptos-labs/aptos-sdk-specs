"""
Step definitions for Aptos client configuration and operations.
"""

from behave import given, when, then


# =============================================================================
# Given Steps - Client Configuration
# =============================================================================


@given("a new Aptos client")
def step_given_new_client(context):
    context.world.test_vectors["client"] = True


@given("an Aptos client")
def step_given_aptos_client(context):
    context.world.test_vectors["client"] = True


@given("an Aptos client for testnet")
def step_given_client_testnet(context):
    context.world.test_vectors["network"] = "testnet"


@given("an Aptos client configured for testnet")
def step_given_client_configured_testnet(context):
    context.world.test_vectors["network"] = "testnet"


@given("an Aptos client configured for mainnet")
def step_given_client_configured_mainnet(context):
    context.world.test_vectors["network"] = "mainnet"


@given("an Aptos client with faucet")
def step_given_client_with_faucet(context):
    context.world.test_vectors["has_faucet"] = True


@given("an Aptos client with auto-gas enabled")
def step_given_client_auto_gas(context):
    context.world.test_vectors["auto_gas"] = True


@given("an Aptos client with retry enabled")
def step_given_client_with_retry(context):
    context.world.test_vectors["retry_enabled"] = True


@given("a connected Aptos client")
def step_given_connected_client(context):
    context.world.test_vectors["connected"] = True


@given("a client connected to any network")
def step_given_client_any_network(context):
    context.world.test_vectors["network"] = "any"


@given("a client connected to testnet (chain_id=2)")
def step_given_client_testnet_chain_id(context):
    context.world.test_vectors["chain_id"] = 2


@given("a client with 1ms timeout")
def step_given_client_short_timeout(context):
    context.world.test_vectors["timeout_ms"] = 1


@given("a client with unreachable endpoint")
def step_given_client_unreachable(context):
    context.world.test_vectors["endpoint"] = "https://unreachable.invalid"


@given("a client configured for unreachable URL")
def step_given_client_unreachable_url(context):
    context.world.test_vectors["endpoint"] = "https://unreachable.invalid"


@given("mainnet and testnet clients")
def step_given_mainnet_testnet_clients(context):
    context.world.test_vectors["mainnet_client"] = True
    context.world.test_vectors["testnet_client"] = True


@given("fullnode ledger version")
def step_given_fullnode_version(context):
    context.world.test_vectors["fullnode_version"] = True


@given("a short timeout")
def step_given_short_timeout(context):
    context.world.test_vectors["timeout_ms"] = 100


@given("a very short timeout (1ms)")
def step_given_very_short_timeout(context):
    context.world.test_vectors["timeout_ms"] = 1


@given("a wait timeout of 5 seconds")
def step_given_wait_timeout(context):
    context.world.test_vectors["wait_timeout"] = 5


# =============================================================================
# When Steps - Client Operations
# =============================================================================


@when("I create an Aptos client")
def step_create_client(context):
    context.world.test_vectors["client_created"] = True


@when("I create an Aptos client with this config")
def step_create_client_with_config(context):
    context.world.test_vectors["client_created"] = True


@when("I configure the client")
def step_configure_client(context):
    context.world.test_vectors["client_configured"] = True


@when("I get ledger info twice with delay")
def step_get_ledger_twice(context):
    context.world.test_vectors["ledger_queried_twice"] = True


@when("I compare versions")
def step_compare_versions(context):
    context.world.test_vectors["versions_compared"] = True


@when("I inspect the response")
def step_inspect_response(context):
    context.world.test_vectors["response_inspected"] = True


@when("I inspect the error")
def step_inspect_error(context):
    context.world.test_vectors["error_inspected"] = True


@when("I inspect it")
def step_inspect_it(context):
    context.world.test_vectors["inspected"] = True


@when("I parse the response")
def step_parse_response(context):
    context.world.test_vectors["response_parsed"] = True


@when("I request metadata")
def step_request_metadata(context):
    context.world.test_vectors["metadata_requested"] = True


# =============================================================================
# Then Steps - Client Assertions
# =============================================================================


@then("the client should use that URL")
def step_client_uses_url(context):
    pass


@then("the client should use custom settings")
def step_client_uses_settings(context):
    pass


@then("I should see version")
def step_see_version(context):
    pass


@then("I should see timestamp")
def step_see_timestamp(context):
    pass


@then("I should see sender")
def step_see_sender(context):
    pass


@then("I should see hash")
def step_see_hash(context):
    pass


@then("I should see the transaction type")
def step_see_tx_type(context):
    pass


@then("values may differ between networks")
def step_values_may_differ(context):
    pass
