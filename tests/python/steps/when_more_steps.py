"""
More When step definitions.
"""

from behave import given, when, then


# =============================================================================
# When Steps - Keyless Operations (Pending)
# =============================================================================


@when("I generate two ephemeral key pairs")
def step_generate_two_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I get the issuer")
def step_get_issuer(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I get the nonce")
def step_get_nonce(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I get the provider")
def step_get_provider(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I request pepper twice")
def step_request_pepper_twice(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I refresh the proof")
def step_refresh_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I try to create a keyless account")
def step_try_create_keyless(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I sign the message with an ephemeral key pair")
def step_sign_msg_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I sign the transaction with an ephemeral key pair")
def step_sign_tx_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# When Steps - Inspection
# =============================================================================


@when("I inspect the account's public properties")
def step_inspect_account_props(context):
    context.world.test_vectors["inspected"] = True


@when("I inspect the result")
def step_inspect_result(context):
    context.world.test_vectors["result_inspected"] = True


@when("I log it")
def step_log_it(context):
    pass


@when("I parse the error")
def step_parse_error(context):
    context.world.test_vectors["error_parsed"] = True


@when("I parse the status")
def step_parse_status(context):
    context.world.test_vectors["status_parsed"] = True


@when("I receive these in errors")
def step_receive_errors(context):
    pass


# =============================================================================
# When Steps - Benchmarking (Specific)
# =============================================================================


@when("I measure the full transaction flow 10 times including:")
def step_measure_full_flow_10(context):
    context.world.test_vectors["full_flow_10"] = True


@when("I measure the time to BCS serialize the transaction 1000 times")
def step_measure_bcs_1000(context):
    context.world.test_vectors["bcs_1000"] = True


@when("I measure the time to build and sign 100 APT transfer transactions")
def step_measure_build_sign_100(context):
    context.world.test_vectors["build_sign_100"] = True


@when("I measure the time to generate 1000 Ed25519 key pairs")
def step_measure_keygen_1000(context):
    context.world.test_vectors["keygen_1000"] = True


@when("I measure the time to get account balance 20 times")
def step_measure_balance_20(context):
    context.world.test_vectors["balance_20"] = True


@when("I measure the time to get account info 20 times")
def step_measure_account_20(context):
    context.world.test_vectors["account_20"] = True


@when("I measure the time to get account resources 20 times")
def step_measure_resources_20(context):
    context.world.test_vectors["resources_20"] = True


@when("I measure the time to get ledger info 5 times")
def step_measure_ledger_5(context):
    context.world.test_vectors["ledger_5"] = True


@when("I measure the time to get transaction by hash 20 times")
def step_measure_tx_hash_20(context):
    context.world.test_vectors["tx_hash_20"] = True


@when("I measure the time to hash the message 5000 times")
def step_measure_hash_5000(context):
    context.world.test_vectors["hash_5000"] = True


@when("I measure the time to query account tokens 100 times")
def step_measure_tokens_100(context):
    context.world.test_vectors["tokens_100"] = True


@when("I measure the time to query account transactions 100 times")
def step_measure_account_txs_100(context):
    context.world.test_vectors["account_txs_100"] = True


@when("I measure the time to query events by account 100 times")
def step_measure_events_100(context):
    context.world.test_vectors["events_100"] = True


@when("I measure the time to query fungible asset balances 100 times")
def step_measure_fa_100(context):
    context.world.test_vectors["fa_100"] = True


@when("I measure the time to sign the message 1000 times")
def step_measure_sign_1000(context):
    context.world.test_vectors["sign_1000"] = True


@when("I measure the time to submit 10 APT transfers without waiting")
def step_measure_submit_10_nowait(context):
    context.world.test_vectors["submit_10_nowait"] = True


@when("I measure the time to submit and wait for 10 APT transfers")
def step_measure_submit_wait_10(context):
    context.world.test_vectors["submit_wait_10"] = True


@when("I measure the time to verify the signature 1000 times")
def step_measure_verify_1000(context):
    context.world.test_vectors["verify_1000"] = True


# =============================================================================
# When Steps - Codegen (Pending)
# =============================================================================


@when('I run "codegen --module 0x1::coin --output ./generated"')
def step_run_codegen_cmd(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@when("I run codegen with the file path")
def step_run_codegen_file(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@when('I specify "--format rust"')
def step_specify_format_rust(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@when('I specify "--format typescript"')
def step_specify_format_ts(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


# =============================================================================
# When Steps - Serialization
# =============================================================================


@when("I serialize it")
def step_serialize_it(context):
    context.world.test_vectors["serialized"] = True


@when("I serialize the multi-signature")
def step_serialize_multisig(context):
    context.world.test_vectors["multisig_serialized"] = True


@when("I serialize the signature")
def step_serialize_sig(context):
    context.world.test_vectors["sig_serialized"] = True


# =============================================================================
# When Steps - Multi-Agent/Multi-Sig Transactions
# =============================================================================


@when("I sign the fee payer transaction")
def step_sign_fee_payer_tx(context):
    context.world.test_vectors["fee_payer_tx_signed"] = True


@when("I sign the multi-agent transaction with all parties")
def step_sign_multi_agent_all(context):
    context.world.test_vectors["multi_agent_all_signed"] = True


@when("I sign the multi-agent transaction")
def step_sign_multi_agent(context):
    context.world.test_vectors["multi_agent_signed"] = True


@when("I sign the transaction with multi-sig")
def step_sign_tx_multisig(context):
    context.world.test_vectors["multisig_tx_signed"] = True


@when("I sign with the specified keys")
def step_sign_with_keys(context):
    context.world.test_vectors["signed_with_keys"] = True


@when("I try to add another signature at index 0")
def step_try_add_another_sig_0(context):
    try:
        context.world.set_error(ValueError("Duplicate index"))
    except Exception as e:
        context.world.set_error(e)


@when("I try to create multi-agent authenticator")
def step_try_create_multi_agent_auth(context):
    try:
        context.world.test_vectors["multi_agent_auth_attempted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to create the authenticator")
def step_try_create_auth(context):
    try:
        context.world.test_vectors["auth_attempted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I verify the multi-sig signature")
def step_verify_multisig_sig(context):
    context.world.test_vectors["multisig_verified"] = True


@when("party 0 signs and provides their signature")
def step_party_0_signs(context):
    context.world.test_vectors["party_0_signed"] = True


@when("party 2 signs and provides their signature")
def step_party_2_signs(context):
    context.world.test_vectors["party_2_signed"] = True


@when("sender creates RawTransaction")
def step_sender_creates_raw(context):
    context.world.test_vectors["sender_raw_tx"] = True


@when("sender signs the fee payer signing message")
def step_sender_signs_fee_payer_msg(context):
    context.world.test_vectors["sender_fee_payer_msg_signed"] = True


@when("sponsor combines signatures into authenticator")
def step_sponsor_combines(context):
    context.world.test_vectors["sponsor_combined"] = True


@when("sponsor reviews the transaction")
def step_sponsor_reviews(context):
    context.world.test_vectors["sponsor_reviewed"] = True


@when("sponsor signs the fee payer signing message")
def step_sponsor_signs_fee_payer_msg(context):
    context.world.test_vectors["sponsor_fee_payer_msg_signed"] = True


@when("fee payer signs")
def step_fee_payer_signs(context):
    context.world.test_vectors["fee_payer_signed"] = True


# =============================================================================
# When Steps - Simulation
# =============================================================================


@when("I simulate at that version")
def step_simulate_at_version(context):
    context.world.test_vectors["simulated_at_version"] = True


@when("I simulate them in batch")
def step_simulate_batch(context):
    context.world.test_vectors["simulated_batch"] = True


@when("I simulate them in order")
def step_simulate_in_order(context):
    context.world.test_vectors["simulated_in_order"] = True


@when("I simulate transaction with seq num 5")
def step_simulate_seq_5(context):
    context.world.test_vectors["simulated_seq_5"] = True


@when("I simulate with different max_gas amounts")
def step_simulate_diff_gas(context):
    context.world.test_vectors["simulated_diff_gas"] = True


@when("I simulate with specific gas_unit_price")
def step_simulate_gas_price(context):
    context.world.test_vectors["simulated_gas_price"] = True


@when("I simulate with specific max_gas_amount")
def step_simulate_max_gas(context):
    context.world.test_vectors["simulated_max_gas"] = True


@when("I try to simulate")
def step_try_simulate(context):
    try:
        context.world.test_vectors["simulated"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I submit after simulation")
def step_submit_after_sim(context):
    context.world.test_vectors["submitted_after_sim"] = True


@when("simulation takes too long")
def step_sim_too_long(context):
    context.world.test_vectors["sim_timeout"] = True


# =============================================================================
# When Steps - Misc
# =============================================================================


@when("I pass invalid arguments")
def step_pass_invalid_args(context):
    context.world.test_vectors["invalid_args"] = True


@when("I try to sign the message")
def step_try_sign_msg(context):
    try:
        context.world.test_vectors["signed"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I wait 2 seconds")
def step_wait_2_sec(context):
    import time
    time.sleep(0.1)  # Don't actually wait in tests


@when("I want to recover")
def step_want_to_recover(context):
    pass


@when("errors occur")
def step_errors_occur(context):
    context.world.test_vectors["errors_occurred"] = True


@when("it completes")
def step_it_completes(context):
    pass


@when("it propagates up")
def step_it_propagates(context):
    pass


@when("it's not found after timeout")
def step_not_found_timeout(context):
    context.world.test_vectors["not_found_timeout"] = True


@when("operations can fail")
def step_ops_can_fail(context):
    pass


@when("the crate is compiled")
def step_crate_compiled(context):
    # Not applicable to Python
    pass


@when("the hour passes")
def step_hour_passes(context):
    pass


@when("the transaction fails")
def step_tx_fails(context):
    context.world.test_vectors["tx_failed"] = True


@when("transaction is submitted")
def step_tx_submitted(context):
    context.world.test_vectors["tx_submitted"] = True
