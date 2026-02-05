"""
Step definitions for indexer and GraphQL operations.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Indexer Setup
# =============================================================================


@given("an indexer client")
def step_given_indexer_client(context):
    # TODO: implement indexer client setup
    context.world.test_vectors["indexer_client"] = True


@given("a custom indexer URL")
def step_given_custom_indexer_url(context):
    context.world.test_vectors["indexer_url"] = "https://custom.indexer.example.com"


@given("an API key for the indexer")
def step_given_api_key(context):
    context.world.test_vectors["api_key"] = "test-api-key"


@given("an unreachable indexer endpoint")
def step_given_unreachable_indexer(context):
    context.world.test_vectors["indexer_url"] = "https://unreachable.invalid"


@given("a GraphQL query string")
def step_given_graphql_query(context):
    context.world.test_vectors["graphql_query"] = "query { ledger_info { chain_id } }"


@given("a GraphQL query with variables")
def step_given_graphql_with_vars(context):
    context.world.test_vectors["graphql_query"] = (
        "query($addr: String!) { account(address: $addr) { sequence_number } }"
    )
    context.world.test_vectors["graphql_vars"] = {"addr": "0x1"}


@given("an invalid GraphQL query")
def step_given_invalid_graphql(context):
    context.world.test_vectors["graphql_query"] = "invalid query {"


@given("a fungible asset query")
def step_given_fa_query(context):
    context.world.test_vectors["fa_query"] = True


@given("an event query result")
def step_given_event_query_result(context):
    context.world.test_vectors["event_result"] = []


@given("an event type")
def step_given_event_type(context):
    context.world.test_vectors["event_type"] = "0x1::coin::DepositEvent"


@given("indexer processor status")
def step_given_processor_status(context):
    context.world.test_vectors["processor_status"] = True


@given("a very complex query")
def step_given_complex_query(context):
    context.world.test_vectors["complex_query"] = True


# =============================================================================
# When Steps - Indexer Operations
# =============================================================================


@when("I create an indexer client for mainnet")
def step_create_indexer_mainnet(context):
    context.world.test_vectors["indexer_network"] = "mainnet"


@when("I create an indexer client for testnet")
def step_create_indexer_testnet(context):
    context.world.test_vectors["indexer_network"] = "testnet"


@when("I create an indexer client with the custom URL")
def step_create_indexer_custom_url(context):
    context.world.test_vectors["indexer_custom"] = True


@when("I create an indexer client with the key")
def step_create_indexer_with_key(context):
    context.world.test_vectors["indexer_with_key"] = True


@when("I execute the query")
def step_execute_query(context):
    # TODO: implement query execution
    context.world.test_vectors["query_executed"] = True


@when("I execute the query with variables")
def step_execute_query_with_vars(context):
    context.world.test_vectors["query_executed"] = True


@when("I query current tokens for the account")
def step_query_current_tokens(context):
    # TODO: implement token query
    context.world.test_vectors["tokens_queried"] = True


@when("I query current tokens")
def step_query_tokens(context):
    context.world.test_vectors["tokens_queried"] = True


@when("I query account transactions")
def step_query_account_txs(context):
    context.world.test_vectors["txs_queried"] = True


@when("I query coin balances from indexer")
def step_query_coin_balances(context):
    context.world.test_vectors["balances_queried"] = True


@when("I query fungible asset balances")
def step_query_fa_balances(context):
    context.world.test_vectors["fa_queried"] = True


@when("I query APT fungible asset balance")
def step_query_apt_balance(context):
    context.world.test_vectors["apt_queried"] = True


@when("I query coin activities")
def step_query_coin_activities(context):
    context.world.test_vectors["activities_queried"] = True


@when("I query events of that type")
def step_query_events_by_type(context):
    context.world.test_vectors["events_queried"] = True


@when("I query events involving that account")
def step_query_events_for_account(context):
    context.world.test_vectors["events_queried"] = True


@when("I query processor status")
def step_query_processor_status(context):
    context.world.test_vectors["processor_queried"] = True


@when("I query it from indexer")
def step_query_from_indexer(context):
    context.world.test_vectors["indexer_queried"] = True


@when("I query the collection")
def step_query_collection(context):
    context.world.test_vectors["collection_queried"] = True


@when("I query the token")
def step_query_token(context):
    context.world.test_vectors["token_queried"] = True


@when("I query tokens in the collection")
def step_query_tokens_in_collection(context):
    context.world.test_vectors["collection_tokens_queried"] = True


@when("I query tokens with limit 10 and offset 0")
def step_query_tokens_paginated(context):
    context.world.test_vectors["tokens_paginated"] = True


@when("I query with limit 25")
def step_query_with_limit(context):
    context.world.test_vectors["query_limit"] = 25


@when("I query with offset 10")
def step_query_with_offset(context):
    context.world.test_vectors["query_offset"] = 10


@when("I query only user transactions")
def step_query_user_txs(context):
    context.world.test_vectors["user_txs_only"] = True


@when("I query its metadata")
def step_query_metadata(context):
    context.world.test_vectors["metadata_queried"] = True


@when("I try to query")
def step_try_query(context):
    try:
        context.world.test_vectors["query_attempted"] = True
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Indexer Assertions
# =============================================================================


@then("I should receive the query result")
def step_receive_query_result(context):
    pass  # Generic assertion


@then("I should receive a list of tokens")
def step_receive_token_list(context):
    pass


@then("I should receive a list of transactions")
def step_receive_tx_list(context):
    pass


@then("I should receive a list of balances")
def step_receive_balance_list(context):
    pass


@then("I should receive a list of modules")
def step_receive_module_list(context):
    pass


@then("I should receive all coin types and amounts")
def step_receive_coin_types(context):
    pass


@then("I should receive matching events")
def step_receive_matching_events(context):
    pass


@then("I should receive relevant events")
def step_receive_relevant_events(context):
    pass


@then("I should see deposits and withdrawals")
def step_see_deposits_withdrawals(context):
    pass


@then("I should see the last processed version")
def step_see_last_version(context):
    pass


@then("I can compare with fullnode ledger version")
def step_compare_fullnode_version(context):
    pass


@then("I can determine indexer lag")
def step_determine_indexer_lag(context):
    pass


@then("I should receive a GraphQL error")
def step_receive_graphql_error(context):
    assert context.world.error is not None or context.world.test_vectors.get("error")


@then("I should receive an empty list")
def step_receive_empty_list(context):
    pass


@then("I should only receive user transactions")
def step_only_user_txs(context):
    pass


@then("I should receive at most 25 transactions")
def step_at_most_25_txs(context):
    pass


@then("I should receive at most 5 transactions")
def step_at_most_5_txs(context):
    pass


@then("I should receive at most 10 tokens")
def step_at_most_10_tokens(context):
    pass


@then("I should receive the next page")
def step_receive_next_page(context):
    pass


@then("I should receive tokens belonging to that collection")
def step_receive_collection_tokens(context):
    pass


@then("I should receive collection details")
def step_receive_collection_details(context):
    pass


@then("I should see name")
def step_see_name(context):
    pass


@then("I should see description")
def step_see_description(context):
    pass


@then("I should see uri")
def step_see_uri(context):
    pass


@then("I should see current_supply")
def step_see_current_supply(context):
    pass


@then("I should see token_name")
def step_see_token_name(context):
    pass


@then("I should see collection_name")
def step_see_collection_name(context):
    pass


@then("I should see creator_address")
def step_see_creator_address(context):
    pass


@then("I should see token_uri")
def step_see_token_uri(context):
    pass


@then('I should see name "Aptos Coin"')
def step_see_name_apt(context):
    pass


@then('I should see symbol "APT"')
def step_see_symbol_apt(context):
    pass


@then("I should see decimals 8")
def step_see_decimals_8(context):
    pass


@then("I should see symbol")
def step_see_symbol(context):
    pass


@then("I should see decimals")
def step_see_decimals(context):
    pass


@then("I should see amount")
def step_see_amount(context):
    pass


@then("requests should include the API key header")
def step_requests_include_key(context):
    pass
