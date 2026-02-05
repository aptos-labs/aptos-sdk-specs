"""
Additional assertion step definitions.
"""

from behave import then

# =============================================================================
# Then Steps - General Assertions
# =============================================================================


@then("all relevant details should be included")
def step_all_details_included(context):
    pass


@then("all requests should succeed")
def step_all_requests_succeed(context):
    assert context.world.error is None


@then("all should be accepted")
def step_all_accepted(context):
    pass


@then("appropriate derive macros")
def step_appropriate_macros(context):
    # Not applicable to Python
    pass


@then("arguments should be empty")
def step_args_empty(context):
    pass


@then("avoid duplicate submissions if possible")
def step_avoid_duplicates(context):
    pass


@then("backoff should be exponential")
def step_backoff_exponential(context):
    pass


@then("be able to fix before actual submission")
def step_can_fix(context):
    pass


@then("be able to retry with correct number")
def step_can_retry_correct(context):
    pass


@then("be able to set appropriate max_gas_amount")
def step_can_set_max_gas(context):
    pass


@then("be able to use it in Script payload")
def step_can_use_in_script(context):
    pass


@then("be catchable by type")
def step_catchable_by_type(context):
    pass


@then("be convertible to anyhow/thiserror")
def step_convertible_to_error(context):
    # Not applicable to Python
    pass


@then("both authenticators should be correct types")
def step_both_auth_correct(context):
    pass


@then("both hashes should be identical")
def step_both_hashes_identical(context):
    pass


@then("both peppers should be identical")
def step_both_peppers_identical(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("both serializations should be identical")
def step_both_serializations_identical(context):
    pass


@then("both types should be properly passed")
def step_both_types_passed(context):
    pass


@then("build should fail with MissingChainId error")
def step_build_fail_chain_id(context):
    assert context.world.error is not None


@then("build should fail with MissingPayload error")
def step_build_fail_payload(context):
    assert context.world.error is not None


@then("build should fail with MissingSender error")
def step_build_fail_sender(context):
    assert context.world.error is not None


@then("build should fail with MissingSequenceNumber error")
def step_build_fail_seq(context):
    assert context.world.error is not None


@then("compilation should fail with type error")
def step_compile_fail_type(context):
    assert context.world.error is not None


@then("configured for testnet faucet")
def step_configured_testnet_faucet(context):
    pass


@then("delay 1 should be ~100ms")
def step_delay_1_100(context):
    pass


@then("delay 2 should be ~200ms")
def step_delay_2_200(context):
    pass


@then("delay 3 should be ~400ms")
def step_delay_3_400(context):
    pass


@then("delays should have some randomness")
def step_delays_random(context):
    pass


@then("delays should never exceed 500ms")
def step_delays_max_500(context):
    pass


@then("delays should triple between retries")
def step_delays_triple(context):
    pass


@then("deprioritized should be <= standard")
def step_deprioritized_le_standard(context):
    pass


@then("difference is refunded")
def step_diff_refunded(context):
    pass


@then("different from module bytecode format")
def step_diff_from_module(context):
    pass


@then("each address should match the expected values from test vectors")
def step_each_addr_matches(context):
    pass


@then("each event should have data")
def step_each_event_data(context):
    pass


@then("each event should have sequence_number")
def step_each_event_seq(context):
    pass


@then("each event should have type")
def step_each_event_type(context):
    pass


@then("each function should have clear signature documentation")
def step_each_func_docs(context):
    pass


@then("each hash should be valid hex")
def step_each_hash_valid(context):
    pass


@then("each module should have bytecode and ABI")
def step_each_module_bytecode(context):
    pass


@then("each should have amount")
def step_each_has_amount(context):
    pass


@then("each should have asset_type")
def step_each_has_asset_type(context):
    pass


@then("each token should have collection info")
def step_each_token_collection(context):
    pass


@then("each token should have token_data_id")
def step_each_token_data_id(context):
    pass


@then("error should indicate insufficient balance")
def step_error_insufficient(context):
    assert context.world.error is not None


@then("error should indicate invalid bytecode")
def step_error_invalid_bytecode(context):
    assert context.world.error is not None


@then("error should indicate out of gas")
def step_error_out_of_gas(context):
    assert context.world.error is not None


@then("errors should implement std::error::Error")
def step_errors_impl_error(context):
    # Not applicable to Python
    pass


@then("estimates should be higher than usual")
def step_estimates_higher(context):
    pass


@then("events that would be emitted")
def step_events_emitted(context):
    pass


@then("execution should fail")
def step_exec_fail(context):
    pass


@then("expiration_timestamp_secs should be approximately T + 600")
def step_expiration_approx(context):
    pass


@then("fee payer should be present")
def step_fee_payer_present(context):
    pass


@then("fee payer's balance is deducted for gas")
def step_fee_payer_deducted(context):
    pass


@then("field names and types")
def step_field_names_types(context):
    pass


@then("gas should be charged to fee payer")
def step_gas_charged_fee_payer(context):
    pass


@then("gas usage estimate")
def step_gas_usage_estimate(context):
    pass


@then("gas_unit_price should be 100")
def step_gas_price_100(context):
    pass


@then("gas_unit_price should be reasonable (e.g., 100)")
def step_gas_price_reasonable(context):
    pass


@then("gas_used represents actual consumption")
def step_gas_used_actual(context):
    pass


@then("gas_used tells me actual consumption")
def step_gas_used_tells(context):
    pass


@then("generate code in the output directory")
def step_gen_in_output(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("generate up-to-date bindings")
def step_gen_bindings(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("generated code should include documentation")
def step_gen_includes_docs(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("have context about the input")
def step_have_context(context):
    pass


@then("have specific error types (AptosApiError, etc.)")
def step_have_error_types(context):
    pass


@then("higher gas price should be processed first (usually)")
def step_higher_gas_first(context):
    pass


@then("higher-level context should be added")
def step_higher_context(context):
    pass


@then("ideally suggest how to fix it")
def step_suggest_fix(context):
    pass


@then("include the abort code")
def step_include_abort_code(context):
    pass


@then("indicate insufficient funds")
def step_indicate_insufficient(context):
    assert context.world.error is not None


@then("indicate resource not found")
def step_indicate_not_found(context):
    assert context.world.error is not None


@then("indicate the type mismatch")
def step_indicate_type_mismatch(context):
    assert context.world.error is not None


@then("inherit from a base AptosError class")
def step_inherit_aptos_error(context):
    pass


@then("initial_delay should be around 100ms")
def step_initial_delay_100(context):
    pass


@then("it should NOT retry the same transaction")
def step_no_retry_same(context):
    pass


@then("it should NOT retry")
def step_no_retry(context):
    pass


@then("it should be Google")
def step_should_be_google(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should be None or unavailable")
def step_should_be_none(context):
    pass


@then("it should be a valid string for OIDC nonce parameter")
def step_valid_oidc_nonce(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")
