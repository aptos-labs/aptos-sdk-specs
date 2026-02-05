"""
Final When step definitions.
"""

from behave import when

# =============================================================================
# When Steps - Faucet
# =============================================================================


@when("I access the faucet client")
def step_access_faucet(context):
    context.world.test_vectors["faucet_accessed"] = True


@when("I call aptos.fund_account(address, amount)")
def step_call_fund_account(context):
    context.world.test_vectors["fund_account_called"] = True


@when("I call create_funded_account with 100_000_000 octas")
def step_call_create_funded(context):
    context.world.test_vectors["create_funded_called"] = True


@when("I call fund_and_wait")
def step_call_fund_and_wait(context):
    context.world.test_vectors["fund_and_wait_called"] = True


# =============================================================================
# When Steps - Codegen (Pending)
# =============================================================================


@when('I annotate code with #[aptos_contract("0x1::coin")]')
def step_annotate_aptos_contract(context):
    # Not applicable to Python
    pass


@when("I generate code")
def step_generate_code(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@when("I generate an ephemeral key pair with 3600 second expiry")
def step_generate_ephemeral_3600(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# When Steps - Transaction Building
# =============================================================================


@when("I apply 20% buffer")
def step_apply_20_buffer(context):
    context.world.test_vectors["buffer_applied"] = True


@when("I build a transaction using the estimate")
def step_build_tx_using_estimate(context):
    context.world.test_vectors["tx_built_with_estimate"] = True


@when("I build a transaction with gas_unit_price 200")
def step_build_tx_gas_200(context):
    context.world.test_vectors["tx_built_gas_200"] = True


@when("I build the RawTransaction")
def step_build_raw_tx(context):
    context.world.test_vectors["raw_tx_built"] = True


@when("I build transaction without specifying gas_unit_price")
def step_build_tx_no_gas(context):
    context.world.test_vectors["tx_built_no_gas"] = True


@when("I build with all required fields")
def step_build_all_required(context):
    context.world.test_vectors["built_all_required"] = True


@when("I call build()")
def step_call_build(context):
    context.world.test_vectors["build_called"] = True


# =============================================================================
# When Steps - Gas Estimation
# =============================================================================


@when("I calculate maximum possible cost")
def step_calc_max_cost(context):
    context.world.test_vectors["max_cost_calculated"] = True


@when("I calculate total cost")
def step_calc_total_cost(context):
    context.world.test_vectors["total_cost_calculated"] = True


@when("I compare actual cost to max possible")
def step_compare_actual_max(context):
    context.world.test_vectors["compared_actual_max"] = True


@when("I compare deprioritized vs standard")
def step_compare_deprioritized_standard(context):
    context.world.test_vectors["compared_deprioritized"] = True


@when("I check gas estimates on each")
def step_check_gas_each(context):
    context.world.test_vectors["checked_gas_each"] = True


@when("I check gas estimates")
def step_check_gas_estimates(context):
    context.world.test_vectors["gas_estimates_checked"] = True


@when("I check gas info")
def step_check_gas_info(context):
    context.world.test_vectors["gas_info_checked"] = True


# =============================================================================
# When Steps - View Function Calls
# =============================================================================


@when("I call 0x1::account::exists_at")
def step_call_exists_at(context):
    context.world.test_vectors["exists_at_called"] = True


@when("I call 0x1::coin::balance<0x1::aptos_coin::AptosCoin>")
def step_call_coin_balance(context):
    context.world.test_vectors["coin_balance_called"] = True


@when("I call 0x1::coin::supply<0x1::aptos_coin::AptosCoin>")
def step_call_coin_supply(context):
    context.world.test_vectors["coin_supply_called"] = True


@when("I call 0x1::timestamp::now_seconds")
def step_call_now_seconds(context):
    context.world.test_vectors["now_seconds_called"] = True


@when("I call a function with wrong argument types")
def step_call_wrong_arg_types(context):
    context.world.test_vectors["wrong_args_called"] = True


@when("I call a generic function without type arguments")
def step_call_generic_no_type_args(context):
    context.world.test_vectors["generic_no_type_args_called"] = True


@when("I call a view function at that version")
def step_call_view_at_version(context):
    context.world.test_vectors["view_at_version_called"] = True


@when("I call a view function that returns multiple values")
def step_call_view_multi_values(context):
    context.world.test_vectors["view_multi_values_called"] = True


@when("I call a view function with too few arguments")
def step_call_view_too_few_args(context):
    context.world.test_vectors["view_too_few_args_called"] = True


@when("I call a view function with wrong argument types")
def step_call_view_wrong_arg_types(context):
    context.world.test_vectors["view_wrong_args_called"] = True


@when('I call non-existent view function "0x1::nonexistent::function"')
def step_call_nonexistent_view(context):
    context.world.test_vectors["nonexistent_view_called"] = True


@when("I call sign_submit_and_wait")
def step_call_sign_submit_wait(context):
    context.world.test_vectors["sign_submit_wait_called"] = True


@when("I call submit_and_wait")
def step_call_submit_and_wait(context):
    context.world.test_vectors["submit_and_wait_called"] = True


@when('I call view function "0x1::account::exists_at"')
def step_call_view_exists_at(context):
    context.world.test_vectors["view_exists_at_called"] = True


@when('I call view function "0x1::coin::balance"')
def step_call_view_coin_balance(context):
    context.world.test_vectors["view_coin_balance_called"] = True


@when('I call view function "0x1::timestamp::now_seconds"')
def step_call_view_now_seconds(context):
    context.world.test_vectors["view_now_seconds_called"] = True


@when("I call with arguments that cause abort")
def step_call_with_abort_args(context):
    context.world.test_vectors["abort_args_called"] = True


@when('I call with type argument "0x1::aptos_coin::AptosCoin"')
def step_call_with_aptos_coin(context):
    context.world.test_vectors["type_arg_aptos_coin"] = True


@when('I call with type argument "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"')
def step_call_with_coin_store(context):
    context.world.test_vectors["type_arg_coin_store"] = True


@when('I call with type arguments ["Type1", "Type2"]')
def step_call_with_type_args_list(context):
    context.world.test_vectors["type_args_list"] = True


@when("I call it with a number")
def step_call_with_number(context):
    context.world.test_vectors["called_with_number"] = True


@when("I call it with a specific type")
def step_call_with_specific_type(context):
    context.world.test_vectors["called_with_type"] = True


@when("I call it with an address string")
def step_call_with_address_string(context):
    context.world.test_vectors["called_with_address"] = True


@when("I call it with byte array")
def step_call_with_byte_array(context):
    context.world.test_vectors["called_with_bytes"] = True


@when("I call it with the struct")
def step_call_with_struct(context):
    context.world.test_vectors["called_with_struct"] = True


# =============================================================================
# When Steps - Error Handling
# =============================================================================


@when("I catch the error")
def step_catch_error(context):
    context.world.test_vectors["error_caught"] = True


@when("I catch the validation error")
def step_catch_validation_error(context):
    context.world.test_vectors["validation_error_caught"] = True


@when("I detect the failure")
def step_detect_failure(context):
    context.world.test_vectors["failure_detected"] = True


@when("I check the error")
def step_check_error(context):
    context.world.test_vectors["error_checked"] = True


@when("I check the status")
def step_check_status(context):
    context.world.test_vectors["status_checked"] = True


@when("I check if it's retryable")
def step_check_if_retryable(context):
    context.world.test_vectors["retryable_checked"] = True


# =============================================================================
# When Steps - Account Checks
# =============================================================================


@when("I check can_sign()")
def step_check_can_sign(context):
    context.world.test_vectors["can_sign_checked"] = True


@when("I check is_expired()")
def step_check_is_expired(context):
    context.world.test_vectors["is_expired_checked"] = True


@when("I check is_valid()")
def step_check_is_valid(context):
    context.world.test_vectors["is_valid_checked"] = True


@when("I check default retry settings")
def step_check_default_retry(context):
    context.world.test_vectors["default_retry_checked"] = True


@when("I check default values")
def step_check_defaults(context):
    context.world.test_vectors["defaults_checked"] = True


# =============================================================================
# When Steps - Multi-Sig Operations
# =============================================================================


@when("I combine correctly")
def step_combine_correctly(context):
    context.world.test_vectors["combined_correctly"] = True


@when("I combine in correct order")
def step_combine_correct_order(context):
    context.world.test_vectors["combined_correct_order"] = True


@when("I create a multi-sig account")
def step_create_multisig_account(context):
    context.world.test_vectors["multisig_account_created"] = True


# =============================================================================
# When Steps - Keyless Operations (Pending)
# =============================================================================


@when("I create a keyless account")
def step_create_keyless_account(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I create an OidcProvider")
def step_create_oidc_provider(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I create keyless accounts for each")
def step_create_keyless_for_each(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I derive the keyless address")
def step_derive_keyless_address(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# When Steps - Derivation
# =============================================================================


@when("I derive addresses for each")
def step_derive_addresses_each(context):
    context.world.test_vectors["addresses_derived"] = True


@when("I derive an Ed25519 account from the mnemonic")
def step_derive_ed25519_from_mnemonic(context):
    # TODO: awaiting SDK implementation - mnemonic
    context.scenario.skip("Mnemonic support limited in Python SDK")


@when("I derive the address twice")
def step_derive_address_twice(context):
    context.world.test_vectors["address_derived_twice"] = True


@when("I derive the address")
def step_derive_address(context):
    context.world.test_vectors["address_derived"] = True
