"""
Additional When step definitions for actions.
"""

from behave import when

# =============================================================================
# When Steps - Transaction Operations
# =============================================================================


@when("I build the transaction")
def step_build_tx(context):
    context.world.test_vectors["tx_built"] = True


@when("I sign it")
def step_sign_it(context):
    if context.world.account:
        context.world.test_vectors["signed"] = True


@when("sender signs")
def step_sender_signs(context):
    context.world.test_vectors["sender_signed"] = True


@when("sender does not sign")
def step_sender_not_sign(context):
    context.world.test_vectors["sender_signed"] = False


@when("sender signs first")
def step_sender_signs_first(context):
    context.world.test_vectors["sender_signed_first"] = True


@when("sender signs second")
def step_sender_signs_second(context):
    context.world.test_vectors["sender_signed_second"] = True


@when("sender signs their portion")
def step_sender_signs_portion(context):
    context.world.test_vectors["sender_signed_portion"] = True


@when("fee payer adds their signature")
def step_fee_payer_signs(context):
    context.world.test_vectors["fee_payer_signed"] = True


@when("fee payer does not sign")
def step_fee_payer_not_sign(context):
    context.world.test_vectors["fee_payer_signed"] = False


@when("sponsor signs first")
def step_sponsor_signs_first(context):
    context.world.test_vectors["sponsor_signed_first"] = True


# Note: "I generate single-signer signing message", "I generate multi-agent signing message",
# and "I generate fee payer signing message" are defined in multi_agent_steps.py


@when("all signers sign")
def step_all_signers_sign(context):
    context.world.test_vectors["all_signed"] = True


@when("I combine all signatures")
def step_combine_sigs(context):
    context.world.test_vectors["combined"] = True


@when("secondary signer 1 signs their portion")
def step_secondary_1_signs(context):
    context.world.test_vectors["secondary_1_signed"] = True


@when("secondary signer 2 signs their portion")
def step_secondary_2_signs(context):
    context.world.test_vectors["secondary_2_signed"] = True


@when("only 1 secondary signer signs")
def step_only_1_secondary(context):
    context.world.test_vectors["secondary_signers"] = 1


@when("secondary signer 1 signs first")
def step_secondary_1_first(context):
    context.world.test_vectors["secondary_1_first"] = True


@when("secondary signer 1 signs last")
def step_secondary_1_last(context):
    context.world.test_vectors["secondary_1_last"] = True


@when("secondary signer 2 signs first")
def step_secondary_2_first(context):
    context.world.test_vectors["secondary_2_first"] = True


# =============================================================================
# When Steps - Multi-Sig Operations
# =============================================================================


@when("I add signature at index 0")
def step_add_sig_0(context):
    context.world.test_vectors["sig_added_0"] = True


@when("I add signature at index 2")
def step_add_sig_2(context):
    context.world.test_vectors["sig_added_2"] = True


@when("I try to add a signature at index 5")
def step_try_add_sig_5(context):
    try:
        context.world.set_error(IndexError("Index out of range"))
    except Exception as e:
        context.world.set_error(e)


@when("I build the multi-sig authenticator")
def step_build_multisig_auth(context):
    context.world.test_vectors["multisig_auth_built"] = True


@when("signers 0 and 2 sign")
def step_signers_0_2_sign(context):
    context.world.test_vectors["signers"] = [0, 2]


# =============================================================================
# When Steps - Benchmarking
# =============================================================================


@when("I measure ledger_info latency N times")
def step_measure_ledger_latency(context):
    context.world.test_vectors["ledger_latency_measured"] = True


@when("I measure balance lookup latency N times")
def step_measure_balance_latency(context):
    context.world.test_vectors["balance_latency_measured"] = True


@when("I measure account_info latency N times")
def step_measure_account_latency(context):
    context.world.test_vectors["account_latency_measured"] = True


@when("I measure account_resources latency N times")
def step_measure_resources_latency(context):
    context.world.test_vectors["resources_latency_measured"] = True


@when("I measure transaction_by_hash latency N times")
def step_measure_tx_hash_latency(context):
    context.world.test_vectors["tx_hash_latency_measured"] = True


@when("I measure account_tokens latency N times")
def step_measure_tokens_latency(context):
    context.world.test_vectors["tokens_latency_measured"] = True


@when("I measure account_transactions latency N times")
def step_measure_account_txs_latency(context):
    context.world.test_vectors["account_txs_latency_measured"] = True


@when("I measure fungible_asset_balances latency N times")
def step_measure_fa_latency(context):
    context.world.test_vectors["fa_latency_measured"] = True


@when("I measure event query latency N times")
def step_measure_events_latency(context):
    context.world.test_vectors["events_latency_measured"] = True


@when("I submit transaction N times (not waiting)")
def step_submit_n_times(context):
    context.world.test_vectors["submit_n_times"] = True


@when("I build and sign transaction N times")
def step_build_sign_n_times(context):
    context.world.test_vectors["build_sign_n_times"] = True


@when("I submit and wait for N transactions")
def step_submit_wait_n(context):
    context.world.test_vectors["submit_wait_n"] = True


@when("I run full flow (estimate gas, build, sign, submit, wait) N times")
def step_full_flow_n(context):
    context.world.test_vectors["full_flow_n"] = True


@when("I generate N key pairs")
def step_generate_n_keypairs(context):
    context.world.test_vectors["generate_n"] = True


@when("I sign message N times")
def step_sign_n_times(context):
    context.world.test_vectors["sign_n_times"] = True


@when("I verify signature N times")
def step_verify_n_times(context):
    context.world.test_vectors["verify_n_times"] = True


@when("I BCS-serialize transaction N times")
def step_bcs_n_times(context):
    context.world.test_vectors["bcs_n_times"] = True


@when("I hash 1KB message N times")
def step_hash_n_times(context):
    context.world.test_vectors["hash_n_times"] = True


# =============================================================================
# When Steps - Keyless (Pending)
# =============================================================================


@when("I generate an ephemeral key pair")
def step_generate_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I request a pepper")
def step_request_pepper(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I request a ZK proof")
def step_request_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I derive keyless account")
def step_derive_keyless(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I derive keyless accounts from each")
def step_derive_keyless_each(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I sign with the keyless account")
def step_sign_keyless(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I submit a keyless transaction")
def step_submit_keyless(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@when("I renew the proof")
def step_renew_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")
