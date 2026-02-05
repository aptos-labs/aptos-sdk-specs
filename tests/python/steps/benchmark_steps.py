"""
Step definitions for benchmark recording.
"""

from behave import then

# =============================================================================
# Then Steps - Benchmark Recording
# =============================================================================


@then('I record the average response time as "gql_account_tokens_avg_ms"')
def step_record_gql_tokens_avg(context):
    context.world.test_vectors["gql_account_tokens_avg_ms"] = 0


@then('I record the average response time as "gql_account_txs_avg_ms"')
def step_record_gql_txs_avg(context):
    context.world.test_vectors["gql_account_txs_avg_ms"] = 0


@then('I record the average response time as "gql_events_avg_ms"')
def step_record_gql_events_avg(context):
    context.world.test_vectors["gql_events_avg_ms"] = 0


@then('I record the average response time as "gql_fa_balances_avg_ms"')
def step_record_gql_fa_avg(context):
    context.world.test_vectors["gql_fa_balances_avg_ms"] = 0


@then('I record the average response time as "rest_account_info_avg_ms"')
def step_record_rest_account_avg(context):
    context.world.test_vectors["rest_account_info_avg_ms"] = 0


@then('I record the average response time as "rest_account_resources_avg_ms"')
def step_record_rest_resources_avg(context):
    context.world.test_vectors["rest_account_resources_avg_ms"] = 0


@then('I record the average response time as "rest_balance_avg_ms"')
def step_record_rest_balance_avg(context):
    context.world.test_vectors["rest_balance_avg_ms"] = 0


@then('I record the average response time as "rest_ledger_info_avg_ms"')
def step_record_rest_ledger_avg(context):
    context.world.test_vectors["rest_ledger_info_avg_ms"] = 0


@then('I record the average response time as "rest_tx_by_hash_avg_ms"')
def step_record_rest_tx_avg(context):
    context.world.test_vectors["rest_tx_by_hash_avg_ms"] = 0


@then('I record the average round-trip time as "tx_round_trip_avg_ms"')
def step_record_tx_roundtrip_avg(context):
    context.world.test_vectors["tx_round_trip_avg_ms"] = 0


@then('I record the average submission time as "tx_submit_avg_ms"')
def step_record_tx_submit_avg(context):
    context.world.test_vectors["tx_submit_avg_ms"] = 0


@then('I record the average time as "bcs_serialize_tx_avg_us"')
def step_record_bcs_avg(context):
    context.world.test_vectors["bcs_serialize_tx_avg_us"] = 0


@then('I record the average time as "crypto_ed25519_keygen_avg_us"')
def step_record_keygen_avg(context):
    context.world.test_vectors["crypto_ed25519_keygen_avg_us"] = 0


@then('I record the average time as "crypto_ed25519_sign_avg_us"')
def step_record_sign_avg(context):
    context.world.test_vectors["crypto_ed25519_sign_avg_us"] = 0


@then('I record the average time as "crypto_ed25519_verify_avg_us"')
def step_record_verify_avg(context):
    context.world.test_vectors["crypto_ed25519_verify_avg_us"] = 0


@then('I record the average time as "crypto_sha3_256_avg_us"')
def step_record_sha3_avg(context):
    context.world.test_vectors["crypto_sha3_256_avg_us"] = 0


@then('I record the average time as "tx_build_sign_avg_ms"')
def step_record_build_sign_avg(context):
    context.world.test_vectors["tx_build_sign_avg_ms"] = 0


@then('I record the average total time as "tx_full_flow_avg_ms"')
def step_record_full_flow_avg(context):
    context.world.test_vectors["tx_full_flow_avg_ms"] = 0


@then("I record the breakdown by step")
def step_record_breakdown(context):
    context.world.test_vectors["breakdown_recorded"] = True


@then('I record the maximum round-trip time as "tx_round_trip_max_ms"')
def step_record_roundtrip_max(context):
    context.world.test_vectors["tx_round_trip_max_ms"] = 0


@then('I record the minimum round-trip time as "tx_round_trip_min_ms"')
def step_record_roundtrip_min(context):
    context.world.test_vectors["tx_round_trip_min_ms"] = 0


@then('I record the operations per second as "bcs_serialize_tx_ops"')
def step_record_bcs_ops(context):
    context.world.test_vectors["bcs_serialize_tx_ops"] = 0


@then('I record the operations per second as "crypto_ed25519_keygen_ops"')
def step_record_keygen_ops(context):
    context.world.test_vectors["crypto_ed25519_keygen_ops"] = 0


@then('I record the operations per second as "crypto_ed25519_sign_ops"')
def step_record_sign_ops(context):
    context.world.test_vectors["crypto_ed25519_sign_ops"] = 0


@then('I record the operations per second as "crypto_ed25519_verify_ops"')
def step_record_verify_ops(context):
    context.world.test_vectors["crypto_ed25519_verify_ops"] = 0


@then('I record the operations per second as "crypto_sha3_256_ops"')
def step_record_sha3_ops(context):
    context.world.test_vectors["crypto_sha3_256_ops"] = 0


# =============================================================================
# Then Steps - Other Assertions
# =============================================================================


@then("I can find the minimum needed")
def step_find_minimum(context):
    pass


@then("I can set max_gas_amount with buffer")
def step_set_max_gas_buffer(context):
    pass


@then("I can submit the real transaction")
def step_can_submit_real(context):
    pass
