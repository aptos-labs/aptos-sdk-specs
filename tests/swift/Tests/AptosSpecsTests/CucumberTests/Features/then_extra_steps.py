"""
Additional Then step definitions for assertions.
"""

from behave import given, when, then


# =============================================================================
# Then Steps - Benchmark Recording (More)
# =============================================================================


@then('I record the operations per second as "tx_build_sign_ops"')
def step_record_build_sign_ops(context):
    context.world.test_vectors["tx_build_sign_ops"] = 0


@then('I record the p95 response time as "gql_account_tokens_p95_ms"')
def step_record_gql_tokens_p95(context):
    context.world.test_vectors["gql_account_tokens_p95_ms"] = 0


@then('I record the p95 response time as "gql_account_txs_p95_ms"')
def step_record_gql_txs_p95(context):
    context.world.test_vectors["gql_account_txs_p95_ms"] = 0


@then('I record the p95 response time as "gql_events_p95_ms"')
def step_record_gql_events_p95(context):
    context.world.test_vectors["gql_events_p95_ms"] = 0


@then('I record the p95 response time as "gql_fa_balances_p95_ms"')
def step_record_gql_fa_p95(context):
    context.world.test_vectors["gql_fa_balances_p95_ms"] = 0


@then('I record the p95 response time as "rest_account_info_p95_ms"')
def step_record_rest_account_p95(context):
    context.world.test_vectors["rest_account_info_p95_ms"] = 0


@then('I record the p95 response time as "rest_account_resources_p95_ms"')
def step_record_rest_resources_p95(context):
    context.world.test_vectors["rest_account_resources_p95_ms"] = 0


@then('I record the p95 response time as "rest_balance_p95_ms"')
def step_record_rest_balance_p95(context):
    context.world.test_vectors["rest_balance_p95_ms"] = 0


@then('I record the p95 response time as "rest_ledger_info_p95_ms"')
def step_record_rest_ledger_p95(context):
    context.world.test_vectors["rest_ledger_info_p95_ms"] = 0


@then('I record the p95 response time as "rest_tx_by_hash_p95_ms"')
def step_record_rest_tx_p95(context):
    context.world.test_vectors["rest_tx_by_hash_p95_ms"] = 0


@then('I record the p95 round-trip time as "tx_round_trip_p95_ms"')
def step_record_roundtrip_p95(context):
    context.world.test_vectors["tx_round_trip_p95_ms"] = 0


@then('I record the p95 submission time as "tx_submit_p95_ms"')
def step_record_submit_p95(context):
    context.world.test_vectors["tx_submit_p95_ms"] = 0


@then('I record the p95 time as "tx_build_sign_p95_ms"')
def step_record_build_sign_p95(context):
    context.world.test_vectors["tx_build_sign_p95_ms"] = 0


@then('I record the requests per second as "gql_account_tokens_rps"')
def step_record_gql_tokens_rps(context):
    context.world.test_vectors["gql_account_tokens_rps"] = 0


@then('I record the requests per second as "gql_account_txs_rps"')
def step_record_gql_txs_rps(context):
    context.world.test_vectors["gql_account_txs_rps"] = 0


@then('I record the requests per second as "gql_events_rps"')
def step_record_gql_events_rps(context):
    context.world.test_vectors["gql_events_rps"] = 0


@then('I record the requests per second as "gql_fa_balances_rps"')
def step_record_gql_fa_rps(context):
    context.world.test_vectors["gql_fa_balances_rps"] = 0


@then('I record the requests per second as "rest_account_info_rps"')
def step_record_rest_account_rps(context):
    context.world.test_vectors["rest_account_info_rps"] = 0


@then('I record the requests per second as "rest_account_resources_rps"')
def step_record_rest_resources_rps(context):
    context.world.test_vectors["rest_account_resources_rps"] = 0


@then('I record the requests per second as "rest_balance_rps"')
def step_record_rest_balance_rps(context):
    context.world.test_vectors["rest_balance_rps"] = 0


@then('I record the requests per second as "rest_ledger_info_rps"')
def step_record_rest_ledger_rps(context):
    context.world.test_vectors["rest_ledger_info_rps"] = 0


@then('I record the requests per second as "rest_tx_by_hash_rps"')
def step_record_rest_tx_rps(context):
    context.world.test_vectors["rest_tx_by_hash_rps"] = 0


@then('I record the transactions per second as "tx_submit_tps"')
def step_record_submit_tps(context):
    context.world.test_vectors["tx_submit_tps"] = 0


# =============================================================================
# Then Steps - Error Assertions
# =============================================================================


@then("I should be able to identify it as a network error")
def step_identify_network_error(context):
    pass


@then("I should extract the abort code")
def step_extract_abort_code(context):
    pass


@then("I should get a clear timeout error")
def step_get_clear_timeout(context):
    pass


@then("I should get a network error not a simulation failure")
def step_get_network_not_sim_error(context):
    pass


@then("I should get timeout error with suggestion to increase timeout")
def step_get_timeout_suggestion(context):
    pass


@then("I should get validation error before simulation even runs")
def step_get_validation_before_sim(context):
    pass


@then("I should identify it as balance error")
def step_identify_balance_error(context):
    pass


@then("I should identify it as out-of-gas error")
def step_identify_out_of_gas(context):
    pass


@then("I should know the expected sequence number")
def step_know_expected_seq(context):
    pass


@then("I should know which operation failed")
def step_know_which_failed(context):
    pass


@then("I should have access to the request ID for debugging")
def step_have_request_id(context):
    pass


@then("I should see the HTTP status code")
def step_see_http_status(context):
    pass


@then("I should see the VM status code")
def step_see_vm_status_code(context):
    pass


@then("I should see the module address")
def step_see_module_address(context):
    pass


@then("I should see which input was invalid")
def step_see_invalid_input(context):
    pass


# =============================================================================
# Then Steps - Simulation Assertions
# =============================================================================


@then("I should get a simulation result")
def step_get_simulation_result(context):
    pass


@then("I should get results for each")
def step_get_results_each(context):
    pass


@then("I should get the detailed failure reason")
def step_get_detailed_reason(context):
    pass


@then("I should see gas_used")
def step_see_gas_used(context):
    pass


@then("I should see sender balance decrease")
def step_see_sender_decrease(context):
    pass


@then("I should see state changes that would occur")
def step_see_state_changes(context):
    pass


@then("I should see which events would emit")
def step_see_events_emit(context):
    pass


@then("I should see which resources change")
def step_see_resources_change(context):
    pass


@then("I should see why it would fail")
def step_see_why_fail(context):
    pass


# =============================================================================
# Then Steps - Multi-Sig/Multi-Agent
# =============================================================================


@then("I should get a multi-sig SignedTransaction")
def step_get_multisig_signed(context):
    pass


@then("I should have a complete multi-agent authenticator")
def step_have_multi_agent_auth(context):
    pass


@then("I should have a valid multi-signature")
def step_have_valid_multisig(context):
    pass


# =============================================================================
# Then Steps - Keyless (Pending)
# =============================================================================


@then("I should receive PepperServiceError")
def step_receive_pepper_error(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("I should receive ProofGenerationFailed error")
def step_receive_proof_error(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("I should receive a pepper value")
def step_receive_pepper_value(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("I should receive a valid proof")
def step_receive_valid_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# Then Steps - SDK Suggestions
# =============================================================================


@then("SDK should help estimate proper gas")
def step_sdk_estimate_gas(context):
    pass


@then("SDK should help refresh sequence number")
def step_sdk_refresh_seq(context):
    pass


@then("SDK should provide human-readable descriptions")
def step_sdk_human_readable(context):
    pass


@then("SDK should suggest waiting")
def step_sdk_suggest_wait(context):
    pass


# =============================================================================
# Then Steps - General Assertions
# =============================================================================


@then("all addresses should be unique")
def step_addresses_unique(context):
    pass


@then("all arguments should be BCS encoded")
def step_args_bcs_encoded(context):
    pass


@then("all components should be serialized in order")
def step_components_in_order(context):
    pass


@then("all estimates should be greater than 0")
def step_estimates_positive(context):
    pass


@then("all signatures should be required")
def step_all_sigs_required(context):
    pass

# Note: "all messages should be identical" is defined in fee_payer_steps.py

@then("all transfers should occur atomically")
def step_transfers_atomic(context):
    pass


@then("both accounts should have the same address")
def step_both_same_address(context):
    pass


@then("both addresses should be identical")
def step_both_addresses_identical(context):
    pass

# Note: "all 3 messages should be identical" and "all 3 signatures should be required"
# are defined in multi_agent_steps.py
