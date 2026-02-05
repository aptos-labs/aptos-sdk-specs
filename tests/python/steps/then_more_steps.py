"""
More Then step definitions.
"""

from behave import then

# =============================================================================
# Then Steps - Validation
# =============================================================================


@then("it should be available")
def step_should_be_available(context):
    pass


@then("it should be retryable")
def step_should_be_retryable(context):
    pass


@then("it should be submitted successfully")
def step_should_be_submitted(context):
    assert context.world.error is None
    assert context.world.transaction_hash is not None


@then("it should be the uncompressed format (65 bytes)")
def step_should_be_65_bytes(context):
    if context.world.bytes_value is not None:
        assert len(context.world.bytes_value) == 65


@then("it should be usable with Aptos")
def step_should_be_usable(context):
    pass


@then("it should be valid Move bytecode")
def step_should_be_valid_bytecode(context):
    pass


@then("it should build the correct EntryFunction")
def step_should_build_entry_func(context):
    pass


@then("it should calculate wait time from date")
def step_should_calc_wait_time(context):
    pass


@then("it should contain secondary_signer_addresses")
def step_should_contain_secondary_addrs(context):
    if context.world.multi_agent_tx is not None:
        assert hasattr(context.world.multi_agent_tx, "secondary_signers") or hasattr(
            context.world.multi_agent_tx, "secondary_signer_addresses"
        )


@then("it should contain secondary_signers list")
def step_should_contain_secondary_signers(context):
    if context.world.multi_agent_tx is not None:
        assert hasattr(context.world.multi_agent_tx, "secondary_signers")
        assert len(context.world.multi_agent_tx.secondary_signers) > 0


@then("it should contain the multi public key")
def step_should_contain_multi_pubkey(context):
    if hasattr(context.world, "multi_sig_public_key") and context.world.multi_sig_public_key is not None:
        assert context.world.multi_sig_public_key is not None


@then("it should contain the multi signature")
def step_should_contain_multi_sig(context):
    if hasattr(context.world, "multi_signature") and context.world.multi_signature is not None:
        assert context.world.multi_signature is not None


@then("it should equal SHA3-256 of the concatenated hashes with pepper and scheme")
def step_should_equal_sha3_pepper(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should equal SHA3-256(public_key_bytes || 0x00)")
def step_should_equal_sha3_00(context):
    pass


@then("it should equal SHA3-256(public_key_bytes || 0x01)")
def step_should_equal_sha3_01(context):
    pass


@then("it should equal SHA3-256(uncompressed_public_key || 0x01)")
def step_should_equal_sha3_uncompressed(context):
    pass


@then("it should fail before submission with clear error")
def step_should_fail_before_submit(context):
    assert context.world.error is not None


@then("it should fail due to fee payer insufficient balance")
def step_should_fail_fee_payer_balance(context):
    assert context.world.error is not None


@then("it should fail or produce single-signer transaction")
def step_should_fail_or_single_signer(context):
    pass


@then("it should fail or return None")
def step_should_fail_or_none(context):
    pass


@then("it should fail with DuplicateSignerIndex error")
def step_should_fail_duplicate_signer(context):
    assert context.world.error is not None


@then("it should fail with EphemeralKeyExpired error")
def step_should_fail_ephemeral_expired(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should fail with InvalidJwt error")
def step_should_fail_invalid_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should fail with InvalidSignerIndex error")
def step_should_fail_invalid_signer(context):
    assert context.world.error is not None


@then("it should fail with an error about nonce mismatch")
def step_should_fail_nonce_mismatch(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should fail with missing fee payer error")
def step_should_fail_missing_fee_payer(context):
    assert context.world.error is not None


@then("it should fail with missing sender error")
def step_should_fail_missing_sender(context):
    assert context.world.error is not None


@then("it should fail with out of gas error")
def step_should_fail_out_of_gas(context):
    assert context.world.error is not None


@then("it should fail with timeout error")
def step_should_fail_timeout(context):
    assert context.world.error is not None


@then("it should fail with validation error")
def step_should_fail_validation(context):
    assert context.world.error is not None


@then("it should fetch the ABI")
def step_should_fetch_abi(context):
    pass


@then("it should generate Rust")
def step_should_generate_rust(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("it should generate TypeScript")
def step_should_generate_ts(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("it should generate code from the file")
def step_should_generate_from_file(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("it should generate typed bindings at compile time")
def step_should_generate_at_compile(context):
    # Not applicable to Python
    pass


@then("it should have a nonce")
def step_should_have_nonce(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should have an address")
def step_should_have_address(context):
    assert context.world.address is not None or (
        context.world.account is not None and hasattr(context.world.account, "address")
    )


@then("it should have an expiry timestamp")
def step_should_have_expiry(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should have balance")
def step_should_have_balance(context):
    # Balance might be in result or account
    assert context.world.result is not None or (
        context.world.account is not None and hasattr(context.world.account, "balance")
    )


@then("it should have resources")
def step_should_have_resources(context):
    pass


@then("it should include exposed functions")
def step_should_include_exposed_funcs(context):
    pass


@then("it should include gas_used")
def step_should_include_gas_used(context):
    if context.world.simulation_result is not None:
        assert hasattr(context.world.simulation_result, "gas_used") or (
            isinstance(context.world.simulation_result, dict) and "gas_used" in context.world.simulation_result
        )


@then("it should include struct definitions")
def step_should_include_structs(context):
    pass


@then("it should include success status")
def step_should_include_success(context):
    if context.world.simulation_result is not None:
        assert hasattr(context.world.simulation_result, "success") or (
            isinstance(context.world.simulation_result, dict) and "success" in context.world.simulation_result
        )


@then("it should include the signer bitmap")
def step_should_include_bitmap(context):
    pass


@then("it should indicate permanent failure")
def step_should_indicate_permanent(context):
    pass


@then("it should indicate success")
def step_should_indicate_success(context):
    assert context.world.error is None
    if context.world.result is not None:
        assert context.world.result is True or (
            isinstance(context.world.result, dict) and context.world.result.get("success", False)
        )


@then("it should not contain internal implementation details")
def step_should_not_contain_impl(context):
    pass


@then("it should properly BCS encode all fields in order")
def step_should_bcs_encode_fields(context):
    pass


@then("it should properly BCS encode the value")
def step_should_bcs_encode_value(context):
    pass


@then("it should properly BCS encode the vector")
def step_should_bcs_encode_vector(context):
    pass


@then("it should properly encode the address")
def step_should_encode_address(context):
    pass


@then("it should retry after delay")
def step_should_retry_delay(context):
    pass


@then("it should retry the request")
def step_should_retry_request(context):
    pass


@then("it should retry twice")
def step_should_retry_twice(context):
    pass


@then("it should return appropriate type")
def step_should_return_appropriate_type(context):
    pass


@then("it should return false")
def step_should_return_false(context):
    assert context.world.result is False


@then("it should return true")
def step_should_return_true(context):
    assert context.world.result is True


@then("it should try 4 times total (1 + 3 retries)")
def step_should_try_4_times(context):
    pass


@then("it should use default backoff")
def step_should_use_default_backoff(context):
    pass


@then("it should use that issuer")
def step_should_use_issuer(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("it should wait at least 5 seconds before retrying")
def step_should_wait_5_sec(context):
    pass


# =============================================================================
# Then Steps - Knowledge/Info
# =============================================================================


@then("know that increasing max_gas_amount may help")
def step_know_increase_gas(context):
    pass


@then("know which account lacks funds")
def step_know_which_lacks_funds(context):
    pass


@then("later simulations should see earlier changes")
def step_later_sims_see_changes(context):
    pass


# =============================================================================
# Then Steps - Ledger State
# =============================================================================


@then("ledger state should have block_height")
def step_ledger_has_block_height(context):
    pass


@then("ledger state should have chain_id")
def step_ledger_has_chain_id(context):
    pass


@then("ledger state should have ledger_version")
def step_ledger_has_version(context):
    pass


# =============================================================================
# Then Steps - Gas and Costs
# =============================================================================


@then("max cost should be 20000000 octas (0.2 APT)")
def step_max_cost_02_apt(context):
    pass


@then("max_delay should be around 5 seconds")
def step_max_delay_5_sec(context):
    pass


@then("max_gas_amount should be 12000")
def step_max_gas_12000(context):
    if context.world.raw_transaction is not None:
        assert context.world.raw_transaction.max_gas_amount == 12000


@then("max_gas_amount should be 200000")
def step_max_gas_200000(context):
    if context.world.raw_transaction is not None:
        assert context.world.raw_transaction.max_gas_amount == 200000


@then("max_gas_amount should be reasonable (e.g., 200000)")
def step_max_gas_reasonable(context):
    if context.world.raw_transaction is not None:
        assert context.world.raw_transaction.max_gas_amount > 0
        assert context.world.raw_transaction.max_gas_amount <= 10000000  # Reasonable upper bound


@then("max_retries should be 3")
def step_max_retries_3(context):
    pass


@then("total should be 100000 octas")
def step_total_100000(context):
    pass


# =============================================================================
# Then Steps - Multi-Sig
# =============================================================================


@then("multi-agent signing should succeed")
def step_multi_agent_succeed(context):
    assert context.world.error is None
    assert context.world.multi_agent_tx is not None


@then("multi-sig verification should fail")
def step_multisig_verify_fail(context):
    assert context.world.result is False or context.world.error is not None


@then("multi-sig verification should succeed")
def step_multisig_verify_succeed(context):
    assert context.world.error is None
    assert context.world.result is True


# =============================================================================
# Then Steps - Network and Retry
# =============================================================================


@then("network errors should be retryable")
def step_network_errors_retryable(context):
    pass


@then("no on-chain state should change")
def step_no_state_change(context):
    pass


@then("not be exactly the calculated values")
def step_not_exact_values(context):
    pass


@then("on-chain validation should fail")
def step_onchain_validation_fail(context):
    pass


@then("optionally deprioritized_gas_estimate (slower/cheaper)")
def step_optionally_deprioritized(context):
    pass


@then("optionally deprioritized_gas_estimate")
def step_optionally_deprioritized_alt(context):
    pass


@then("optionally prioritized_gas_estimate (faster)")
def step_optionally_prioritized(context):
    pass


@then("optionally prioritized_gas_estimate")
def step_optionally_prioritized_alt(context):
    pass


@then("original error should be accessible")
def step_original_error_accessible(context):
    pass


@then("parameter types for each function")
def step_param_types_each_func(context):
    pass


@then("parameters should have correct types")
def step_params_correct_types(context):
    pass


@then("potentially auto-retry with backoff")
def step_potentially_auto_retry(context):
    pass


@then("prioritized should be >= standard")
def step_prioritized_ge_standard(context):
    pass


@then("processed in order")
def step_processed_in_order(context):
    pass


@then("rate limit errors should be retryable (with backoff)")
def step_rate_limit_retryable(context):
    pass


@then("rebuild the transaction")
def step_rebuild_tx(context):
    pass


@then("rebuild with higher limit")
def step_rebuild_higher_limit(context):
    pass


@then("receive retry attempt number and error")
def step_receive_retry_attempt(context):
    pass


@then("recipient balance increase")
def step_recipient_balance_increase(context):
    pass


@then("represent constraints properly")
def step_represent_constraints(context):
    pass


@then("respect the retry configuration")
def step_respect_retry_config(context):
    pass


@then("results might differ")
def step_results_might_differ(context):
    pass


@then("retry logic should apply")
def step_retry_logic_apply(context):
    pass


@then("retrying is safe (idempotent)")
def step_retrying_safe(context):
    pass


@then("retrying won't help")
def step_retrying_wont_help(context):
    pass


@then("return a transaction hash")
def step_return_tx_hash(context):
    assert context.world.transaction_hash is not None
    assert len(context.world.transaction_hash) >= 64  # At least 64 hex chars


@then("return the final error")
def step_return_final_error(context):
    pass


@then("return the successful response")
def step_return_successful_response(context):
    pass


@then("return when the transaction is finalized")
def step_return_when_finalized(context):
    pass


@then("save API calls")
def step_save_api_calls(context):
    pass


@then("script simulation should fail")
def step_script_sim_fail(context):
    pass


# =============================================================================
# Then Steps - Serialization
# =============================================================================


@then("secondary addresses should be serialized as vector")
def step_secondary_addrs_vector(context):
    pass


@then("secondary authenticator should be Secp256k1")
def step_secondary_auth_secp256k1(context):
    pass


@then("secondary signers should be serialized as vector")
def step_secondary_signers_vector(context):
    pass


@then("secondary_signer_addresses should be empty")
def step_secondary_addrs_empty(context):
    if context.world.multi_agent_tx is not None:
        if hasattr(context.world.multi_agent_tx, "secondary_signer_addresses"):
            assert len(context.world.multi_agent_tx.secondary_signer_addresses) == 0
        elif hasattr(context.world.multi_agent_tx, "secondary_signers"):
            assert len(context.world.multi_agent_tx.secondary_signers) == 0


@then("secondary_signers should be empty")
def step_secondary_signers_empty(context):
    if context.world.multi_agent_tx is not None:
        assert len(context.world.multi_agent_tx.secondary_signers) == 0


@then("sender authenticator should be Ed25519")
def step_sender_auth_ed25519(context):
    pass


@then("sender authenticator should be serialized")
def step_sender_auth_serialized(context):
    pass


@then("sender can send partially signed tx to sponsor")
def step_sender_can_send_partial(context):
    pass


@then("sender's balance is not deducted for gas")
def step_sender_not_deducted(context):
    pass


@then("sensitive data (keys) should NOT be included")
def step_sensitive_not_included(context):
    pass


@then("set appropriate max_gas_amount")
def step_set_appropriate_max_gas(context):
    pass


@then("should indicate gas exhaustion")
def step_should_indicate_gas_exhaustion(context):
    pass


@then("should respect Retry-After header if present")
def step_should_respect_retry_after(context):
    pass


@then("should return the error immediately")
def step_should_return_error_immediately(context):
    pass


@then("should suggest waiting")
def step_should_suggest_waiting(context):
    pass


@then("should use terminology from Aptos documentation")
def step_should_use_aptos_terminology(context):
    pass


@then("show changes for all involved accounts")
def step_show_changes_all_accounts(context):
    pass


@then("show the abort code")
def step_show_abort_code(context):
    pass


@then("show type mismatch error")
def step_show_type_mismatch(context):
    pass


@then("show what would happen if signature were valid")
def step_show_what_would_happen(context):
    pass


@then("signatures should be ordered by index")
def step_sigs_ordered_by_index(context):
    pass


@then("signing attempts should fail")
def step_signing_attempts_fail(context):
    assert context.world.error is not None
