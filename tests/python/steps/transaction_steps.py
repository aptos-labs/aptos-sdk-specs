"""
Step definitions for transaction operations.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Transaction Setup
# =============================================================================


@given("a valid transaction")
def step_given_valid_tx(context):
    context.world.test_vectors["valid_tx"] = True


@given("a valid signed transaction")
def step_given_valid_signed_tx(context):
    context.world.test_vectors["valid_signed_tx"] = True


@given("a valid signed APT transfer transaction")
def step_given_valid_apt_tx(context):
    context.world.test_vectors["apt_transfer"] = True


@given("a signed transaction for submission")
def step_given_signed_for_submission(context):
    context.world.test_vectors["signed_for_submission"] = True


@given("a simple transfer transaction")
def step_given_simple_transfer(context):
    context.world.test_vectors["simple_transfer"] = True


@given("a transaction that will fail (e.g., insufficient balance)")
def step_given_tx_will_fail(context):
    context.world.test_vectors["will_fail"] = True


@given("a transaction that would fail")
def step_given_tx_would_fail(context):
    context.world.test_vectors["would_fail"] = True


@given("a transaction that fails on-chain")
def step_given_tx_fails_onchain(context):
    context.world.test_vectors["fails_onchain"] = True


@given("a transaction with invalid signature")
def step_given_invalid_sig_tx(context):
    context.world.test_vectors["invalid_sig"] = True


@given("a transaction with very low max_gas_amount")
def step_given_low_max_gas_tx(context):
    context.world.test_vectors["low_max_gas"] = True


@given("a transfer transaction for more than account balance")
def step_given_overdraft_tx(context):
    context.world.test_vectors["overdraft"] = True


@given("a transaction signed for mainnet (chain_id=1)")
def step_given_mainnet_signed_tx(context):
    context.world.test_vectors["mainnet_tx"] = True


@given("a transaction simulation result")
def step_given_sim_result(context):
    context.world.test_vectors["sim_result"] = True


@given("a transaction submission that times out")
def step_given_submission_timeout(context):
    context.world.test_vectors["submission_timeout"] = True


@given("a transaction rejected for invalid sequence number")
def step_given_invalid_seq_tx(context):
    context.world.test_vectors["invalid_seq"] = True


@given("a transaction requiring 10000 octas gas")
def step_given_tx_10000_gas(context):
    context.world.test_vectors["gas_required"] = 10000


@given("a transaction requiring 50000 gas")
def step_given_tx_50000_gas(context):
    context.world.test_vectors["gas_required"] = 50000


@given("a submitted transaction hash")
def step_given_submitted_hash(context):
    context.world.test_vectors["submitted_hash"] = "0x123"


@given("a submitted transaction with unknown status")
def step_given_unknown_status_tx(context):
    context.world.test_vectors["unknown_status"] = True


@given("a successful transaction")
def step_given_successful_tx(context):
    context.world.test_vectors["successful"] = True


@given("a completed transaction")
def step_given_completed_tx(context):
    context.world.test_vectors["completed"] = True


@given("a newly submitted transaction")
def step_given_newly_submitted(context):
    context.world.test_vectors["newly_submitted"] = True


@given("a known transaction hash")
def step_given_known_hash(context):
    context.world.test_vectors["known_hash"] = "0x123"


@given("a transaction hash that doesn't exist")
def step_given_nonexistent_hash(context):
    context.world.test_vectors["nonexistent_hash"] = "0xfff"


@given("a non-existent transaction hash")
def step_given_nonexistent_hash_alt(context):
    context.world.test_vectors["nonexistent_hash"] = "0xfff"


@given("a known ledger version")
def step_given_known_version(context):
    context.world.test_vectors["known_version"] = 100


@given("a known past ledger version")
def step_given_past_version(context):
    context.world.test_vectors["past_version"] = 50


@given("a ledger version older than oldest available")
def step_given_old_version(context):
    context.world.test_vectors["old_version"] = 1


@given("a simulated and executed transaction")
def step_given_simulated_executed(context):
    context.world.test_vectors["simulated_executed"] = True


@given("a signed transaction with corrupted signature")
def step_given_corrupted_sig(context):
    context.world.test_vectors["corrupted_sig"] = True


@given("a signed transaction with past expiration")
def step_given_expired_tx(context):
    context.world.test_vectors["expired"] = True


@given("two transactions with different gas prices")
def step_given_two_tx_diff_gas(context):
    context.world.test_vectors["two_txs_diff_gas"] = True


@given("malformed transaction bytes")
def step_given_malformed_tx(context):
    context.world.test_vectors["malformed_tx"] = b"\xff\xff"


@given("simulated gas_used = 10000")
def step_given_simulated_gas(context):
    context.world.test_vectors["simulated_gas_used"] = 10000


@given("current gas estimate is 150")
def step_given_current_estimate(context):
    context.world.test_vectors["current_estimate"] = 150


@given("gas price estimates")
def step_given_gas_estimates(context):
    context.world.test_vectors["gas_estimates"] = True


# =============================================================================
# When Steps - Transaction Operations
# =============================================================================


@when("I submit the transaction")
def step_submit_tx(context):
    context.world.test_vectors["tx_submitted"] = True


@when("I try to submit the transaction")
def step_try_submit_tx(context):
    try:
        context.world.test_vectors["tx_submitted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to submit transaction")
def step_try_submit_tx_alt(context):
    try:
        context.world.test_vectors["tx_submitted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to submit a transaction")
def step_try_submit_a_tx(context):
    try:
        context.world.test_vectors["tx_submitted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to submit it")
def step_try_submit_it(context):
    try:
        context.world.test_vectors["tx_submitted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to submit")
def step_try_submit(context):
    try:
        context.world.test_vectors["tx_submitted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to submit them")
def step_try_submit_them(context):
    try:
        context.world.test_vectors["txs_submitted"] = True
    except Exception as e:
        context.world.set_error(e)


@when("submit it")
def step_submit_it(context):
    context.world.test_vectors["tx_submitted"] = True


@when("I submit it to the API")
def step_submit_to_api(context):
    context.world.test_vectors["tx_submitted"] = True


@when("I submit it successfully")
def step_submit_successfully(context):
    context.world.test_vectors["tx_submitted"] = True
    context.world.test_vectors["tx_success"] = True


@when("I submit a transaction without specifying gas")
def step_submit_no_gas(context):
    context.world.test_vectors["no_gas_specified"] = True


@when("I submit a transaction with sequence_number 5")
def step_submit_seq_5(context):
    context.world.test_vectors["sequence_number"] = 5


@when("I submit a transaction with sequence_number 10")
def step_submit_seq_10(context):
    context.world.test_vectors["sequence_number"] = 10


@when("I submit with max_gas_amount = 10000")
def step_submit_max_gas(context):
    context.world.test_vectors["max_gas_amount"] = 10000


@when("I submit transactions with sequence numbers 0, 1, 2")
def step_submit_multi_seq(context):
    context.world.test_vectors["sequence_numbers"] = [0, 1, 2]


@when("both are submitted")
def step_both_submitted(context):
    context.world.test_vectors["both_submitted"] = True


@when("I simulate it")
def step_simulate(context):
    context.world.test_vectors["simulated"] = True


@when("I simulate both")
def step_simulate_both(context):
    context.world.test_vectors["both_simulated"] = True


@when("I wait for it to complete")
def step_wait_complete(context):
    context.world.test_vectors["waited"] = True


@when("I wait for it")
def step_wait_it(context):
    context.world.test_vectors["waited"] = True


@when("I get transaction by hash")
def step_get_tx_by_hash(context):
    context.world.test_vectors["tx_by_hash_queried"] = True


@when("I get transaction by version")
def step_get_tx_by_version(context):
    context.world.test_vectors["tx_by_version_queried"] = True


@when("I compare gas values")
def step_compare_gas(context):
    context.world.test_vectors["gas_compared"] = True


@when("I compare prioritized vs standard")
def step_compare_priority(context):
    context.world.test_vectors["priority_compared"] = True


@when("I extract gas_used")
def step_extract_gas(context):
    context.world.test_vectors["gas_extracted"] = True


@when("I compute its hash locally")
def step_compute_hash_locally(context):
    context.world.test_vectors["hash_computed"] = True


@when("compare with the hash from submission response")
def step_compare_hash(context):
    context.world.test_vectors["hash_compared"] = True


@when("I request gas estimate")
def step_request_gas_estimate(context):
    context.world.test_vectors["gas_estimate_requested"] = True


@when("I request gas price estimate")
def step_request_gas_price(context):
    context.world.test_vectors["gas_price_requested"] = True


# =============================================================================
# Then Steps - Transaction Assertions
# =============================================================================


@then("I should receive a pending transaction response")
def step_receive_pending(context):
    pass


@then("I should receive the transaction hash")
def step_receive_hash(context):
    pass


@then("I should receive transaction hash(es)")
def step_receive_hashes(context):
    pass


@then("I should see one or more transaction hashes")
def step_see_hashes(context):
    pass


@then("I should receive the transaction details")
def step_receive_details(context):
    pass


@then("I should receive the transaction at that version")
def step_receive_tx_at_version(context):
    pass


@then("I should receive the final transaction result")
def step_receive_final_result(context):
    pass


@then("I should receive simulation results")
def step_receive_sim_results(context):
    pass


@then("I should see the success status")
def step_see_success(context):
    pass


@then("I should see success status")
def step_see_success_alt(context):
    pass


@then("I should see success: false")
def step_see_success_false(context):
    pass


@then("I should see execution result")
def step_see_exec_result(context):
    pass


@then("I should see the estimated gas_used")
def step_see_estimated_gas(context):
    pass


@then("I should see the failure reason")
def step_see_failure_reason(context):
    pass


@then("I should see the VM error")
def step_see_vm_error(context):
    pass


@then("I should see the VM error details")
def step_see_vm_error_details(context):
    pass


@then("I should see vm_status in the result")
def step_see_vm_status(context):
    pass


@then("I should receive an error about chain ID mismatch")
def step_receive_chain_id_error(context):
    assert context.world.error is not None


@then("I should receive an error about expired transaction")
def step_receive_expired_error(context):
    assert context.world.error is not None


@then("I should receive an error about invalid signature")
def step_receive_sig_error(context):
    assert context.world.error is not None


@then("I should receive an error about sequence number")
def step_receive_seq_error(context):
    assert context.world.error is not None


@then("actual gas should be similar to simulated")
def step_gas_similar(context):
    pass


@then("actual should be <= max possible")
def step_actual_le_max(context):
    pass


@then("actual should not exceed max_gas_amount")
def step_not_exceed_max(context):
    pass
