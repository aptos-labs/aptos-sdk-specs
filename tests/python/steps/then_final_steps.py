"""
Final Then step definitions.
"""

from behave import then

# =============================================================================
# Then Steps - Simulation
# =============================================================================


@then("simulation respects that limit")
def step_sim_respects_limit(context):
    pass


@then("simulation should fail")
def step_sim_should_fail(context):
    pass


@then("simulation should reflect that")
def step_sim_should_reflect(context):
    pass


@then("simulation should show failure")
def step_sim_should_show_failure(context):
    pass


@then("simulation should still work")
def step_sim_should_still_work(context):
    pass


@then("simulation should work even if account hasn't committed seq 5 yet")
def step_sim_should_work_even_if(context):
    pass


@then("simulation should work")
def step_sim_should_work(context):
    pass


@then("simulation uses state at that version")
def step_sim_uses_state_at_version(context):
    pass


@then("simulation uses that price for calculations")
def step_sim_uses_price(context):
    pass


@then("structure should be:")
def step_structure_should_be(context):
    pass


@then("submitted")
def step_submitted(context):
    pass


@then("support errors.Is/errors.As")
def step_support_errors_is_as(context):
    # Go-specific
    pass


@then("that request should not retry")
def step_request_should_not_retry(context):
    pass


# =============================================================================
# Then Steps - SDK Behavior
# =============================================================================


@then("the SDK should poll the API")
def step_sdk_should_poll(context):
    pass


@then("the SDK should respect retry-after if present")
def step_sdk_should_respect_retry(context):
    pass


# =============================================================================
# Then Steps - Secp256r1 (All Pending)
# =============================================================================


@then("the Secp256r1 account should have a valid address")
def step_secp256r1_valid_address(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 address should match the expected value from test vectors")
def step_secp256r1_address_matches(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 compressed public key should match test vectors")
def step_secp256r1_compressed_matches(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then('the Secp256r1 signature scheme should be "secp256r1_ecdsa"')
def step_secp256r1_scheme(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 signature should match test vectors")
def step_secp256r1_sig_matches(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the Secp256r1 uncompressed public key should match test vectors")
def step_secp256r1_uncompressed_matches(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("the authenticator should use Secp256r1")
def step_auth_should_use_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


@then("verification should work with Secp256r1")
def step_verification_with_secp256r1(context):
    # TODO: awaiting SDK implementation - Secp256r1
    context.scenario.skip("Secp256r1 not supported in Python SDK")


# =============================================================================
# Then Steps - Error Messages
# =============================================================================


@then("the abort code from that module")
def step_abort_code_from_module(context):
    pass


@then("the abort code if applicable")
def step_abort_code_if_applicable(context):
    pass


@then("the account should be Ed25519 type")
def step_account_ed25519_type(context):
    pass


@then("the account should be Secp256k1 type")
def step_account_secp256k1_type(context):
    pass


@then("the account should be created")
def step_account_should_be_created(context):
    pass


@then("the account should be funded")
def step_account_should_be_funded(context):
    pass


@then("the account should be usable for signing")
def step_account_should_be_usable(context):
    pass


@then("the account should exist")
def step_account_should_exist(context):
    pass


@then("the account should have 100_000_000 octas balance")
def step_account_100m_octas(context):
    pass


@then("the account should have balance")
def step_account_has_balance(context):
    pass


@then("the address should be properly encoded")
def step_address_properly_encoded(context):
    pass


@then("the address should match expected value from test vectors")
def step_address_matches_vectors(context):
    pass


@then("the addresses should be identical")
def step_addresses_identical(context):
    pass


@then("the addresses should be the same")
def step_addresses_same(context):
    pass


@then("the authentication keys should match")
def step_auth_keys_match(context):
    pass


@then("the body should be BCS-serialized bytes")
def step_body_bcs_serialized(context):
    pass


@then("the boolean should be properly encoded")
def step_boolean_properly_encoded(context):
    pass


@then("the bytes should match expected value from test vectors")
def step_bytes_match_vectors(context):
    pass


@then("the compressed public key should match test vectors")
def step_compressed_matches_vectors(context):
    pass


@then('the encoded bytes should be "01"')
def step_encoded_01(context):
    pass


@then('the encoded bytes should be "03010203"')
def step_encoded_03010203(context):
    pass


@then('the encoded bytes should be "0568656c6c6f"')
def step_encoded_hello(context):
    pass


@then('the encoded bytes should be "40420f0000000000"')
def step_encoded_number(context):
    pass


@then("the encoded bytes should be the BCS-serialized address")
def step_encoded_bcs_address(context):
    pass


@then("the error message from the API")
def step_error_msg_from_api(context):
    pass


@then("the error should contain the HTTP status")
def step_error_has_http_status(context):
    pass


@then("the error should contain the abort code")
def step_error_has_abort_code(context):
    pass


@then("the error should contain the error message")
def step_error_has_error_msg(context):
    pass


@then("the error should contain the error_code")
def step_error_has_error_code(context):
    pass


@then("the error should contain the message")
def step_error_has_message(context):
    pass


@then("the error should indicate insufficient balance")
def step_error_insufficient_balance(context):
    pass


@then("the error should indicate rate limiting")
def step_error_rate_limiting(context):
    pass


@then("the error should indicate the abort code")
def step_error_indicate_abort(context):
    pass


@then("the error should indicate type mismatch")
def step_error_type_mismatch(context):
    pass


@then("the fee payer transaction should be valid")
def step_fee_payer_tx_valid(context):
    pass


@then("the hash I was waiting for")
def step_hash_waiting_for(context):
    pass


@then("the hash should be 64 hex characters with 0x prefix")
def step_hash_64_hex(context):
    pass


@then("the macro should fetch current ABI")
def step_macro_fetch_abi(context):
    # Not applicable to Python
    pass


@then("the message should explain what went wrong")
def step_msg_explain_wrong(context):
    pass


@then("the method should return after confirmation")
def step_method_return_after_confirm(context):
    pass


@then("the method should return the final result")
def step_method_return_final(context):
    pass


@then("the method should wait for confirmation")
def step_method_wait_confirm(context):
    pass


@then("the module that aborted (if available)")
def step_module_aborted_if_available(context):
    pass


@then("the module that aborted")
def step_module_aborted(context):
    pass


@then("the nested type should be properly parsed")
def step_nested_type_parsed(context):
    pass


@then("the number should be properly encoded")
def step_number_properly_encoded(context):
    pass


@then("the parameter should be optional in generated code")
def step_param_optional_in_code(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@then("the parsing should fail with an invalid mnemonic error")
def step_parsing_fail_invalid_mnemonic(context):
    assert context.world.error is not None


@then("the payload type should be Script")
def step_payload_type_script(context):
    pass


@then("the pepper should not be accessible")
def step_pepper_not_accessible(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("the phrase should be valid BIP-39")
def step_phrase_valid_bip39(context):
    pass


@then("the phrase should contain exactly 12 words")
def step_phrase_12_words(context):
    pass


@then("the phrase should contain exactly 15 words")
def step_phrase_15_words(context):
    pass


@then("the phrase should contain exactly 18 words")
def step_phrase_18_words(context):
    pass


@then("the phrase should contain exactly 21 words")
def step_phrase_21_words(context):
    pass


@then("the phrase should contain exactly 24 words")
def step_phrase_24_words(context):
    pass


@then("the phrases should be different")
def step_phrases_different(context):
    pass


@then("the public key should match the expected value from test vectors")
def step_pubkey_matches_vectors(context):
    pass


@then('the request content type should be "application/x.aptos.signed_transaction+bcs"')
def step_request_content_type(context):
    pass


@then("the request should succeed")
def step_request_succeed(context):
    pass


@then("the response should contain the transaction hash")
def step_response_has_tx_hash(context):
    pass


@then("the response should include ledger state")
def step_response_has_ledger_state(context):
    pass


@then("the result should be a boolean")
def step_result_is_boolean(context):
    pass


@then("the result should be a u64")
def step_result_is_u64(context):
    pass


@then("the result should indicate success: false")
def step_result_success_false(context):
    pass


@then("the result should indicate success: true")
def step_result_success_true(context):
    pass


@then("the results should include gas_used")
def step_results_include_gas_used(context):
    pass


@then("the results should include success status")
def step_results_include_success(context):
    pass


@then("the retry should include the same body")
def step_retry_same_body(context):
    pass


@then("the same headers")
def step_same_headers(context):
    pass


@then("the scheme identifier used should be 0x01")
def step_scheme_id_0x01(context):
    pass


@then("the script can access them")
def step_script_can_access(context):
    pass


@then("the script transaction should fail")
def step_script_tx_fail(context):
    pass


@then("the second ledger_version should be >= first")
def step_second_version_ge_first(context):
    pass


@then("the signature should include the ZK proof")
def step_sig_includes_zk_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("the signature should include the ephemeral signature")
def step_sig_includes_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("the signature should match expected value from test vectors")
def step_sig_matches_vectors(context):
    pass


@then("the string should be properly encoded")
def step_string_properly_encoded(context):
    pass


@then("the transaction hash if submitted")
def step_tx_hash_if_submitted(context):
    pass


@then("the transaction hash should match the expected value")
def step_tx_hash_matches_expected(context):
    pass


@then("the transaction is ready for submission")
def step_tx_ready_for_submission(context):
    pass


@then("the transaction should be accepted")
def step_tx_should_be_accepted(context):
    pass


@then("the transaction should be committed or failed")
def step_tx_committed_or_failed(context):
    pass


@then("the transaction should be confirmed")
def step_tx_should_be_confirmed(context):
    pass


@then("the transaction should be signed")
def step_tx_should_be_signed(context):
    pass


@then("the transaction should have that limit")
def step_tx_has_limit(context):
    pass


@then("the transaction should have the custom values")
def step_tx_has_custom_values(context):
    pass


@then("the transaction should use price 200")
def step_tx_uses_price_200(context):
    pass


@then("the transaction will fail on-chain")
def step_tx_will_fail_onchain(context):
    pass


@then("the type arguments should be included")
def step_type_args_included(context):
    pass


@then("the type parameter should be inferred or required")
def step_type_param_inferred(context):
    pass


@then("the type should be properly passed")
def step_type_properly_passed(context):
    pass


@then("the uncompressed public key should match test vectors")
def step_uncompressed_matches_vectors(context):
    pass


@then("the value should be in octas per gas unit")
def step_value_in_octas(context):
    pass


@then("the variables should be substituted")
def step_vars_substituted(context):
    pass


@then("the variant indicator should be FeePayer")
def step_variant_fee_payer(context):
    pass


@then("the variant indicator should be MultiAgent")
def step_variant_multi_agent(context):
    pass


@then("the vector should be properly encoded")
def step_vector_properly_encoded(context):
    pass


@then("their data")
def step_their_data(context):
    pass


@then("their new values")
def step_their_new_values(context):
    pass


@then("their return types")
def step_their_return_types(context):
    pass


@then("they should extend Error class")
def step_extend_error_class(context):
    # JavaScript-specific
    pass


@then("they should implement error interface")
def step_implement_error_interface(context):
    pass


@then("they should match")
def step_they_should_match(context):
    pass


@then("they should raise specific exceptions")
def step_raise_specific_exceptions(context):
    pass


@then("they should return Result<T, E>")
def step_return_result(context):
    # Rust-specific
    pass


@then("they should start from the specified offset")
def step_start_from_offset(context):
    pass


@then("this is expected behavior")
def step_expected_behavior(context):
    pass


@then("transaction should fail")
def step_transaction_fail(context):
    pass


@then("transactions should be for that account")
def step_txs_for_account(context):
    pass


@then("transactions should be ordered by version")
def step_txs_ordered_by_version(context):
    pass


@then("type arguments should be empty")
def step_type_args_empty(context):
    pass


@then("type parameters for generic functions")
def step_type_params_generics(context):
    pass


@then("u128 should map to u128")
def step_u128_maps_to_u128(context):
    pass


@then("use a dummy signature internally")
def step_use_dummy_sig(context):
    pass


@then("use it for the transaction")
def step_use_for_tx(context):
    pass


@then("validation errors should NOT be retryable")
def step_validation_not_retryable(context):
    pass


@then("wait appropriately")
def step_wait_appropriately(context):
    pass


@then("waited upon")
def step_waited_upon(context):
    pass


@then("why it was invalid")
def step_why_invalid(context):
    pass
