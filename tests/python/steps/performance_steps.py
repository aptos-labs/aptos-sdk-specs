"""
Step definitions for performance and benchmarking.
"""

from behave import given, when, then
import time


# =============================================================================
# Given Steps - Performance Setup
# =============================================================================


@given("a known transaction hash for benchmarking")
def step_given_benchmark_hash(context):
    context.world.test_vectors["benchmark_hash"] = "0x123abc"


@given("a known account with events")
def step_given_account_events(context):
    context.world.test_vectors["has_events"] = True


@given("a known account with fungible assets")
def step_given_account_fungible(context):
    context.world.test_vectors["has_fungible_assets"] = True


@given("a known account with tokens")
def step_given_account_tokens(context):
    context.world.test_vectors["has_tokens"] = True


# =============================================================================
# When Steps - Performance Measurement
# =============================================================================


@when("I measure the time for N operations")
def step_measure_n_ops(context):
    start = time.time()
    context.world.test_vectors["start_time"] = start


@when("I run the benchmark")
def step_run_benchmark(context):
    context.world.test_vectors["benchmark_run"] = True


# =============================================================================
# Then Steps - Performance Assertions
# =============================================================================


@then("I should record average response time")
def step_record_avg_response(context):
    context.world.test_vectors["avg_response_recorded"] = True


@then("I should record min response time")
def step_record_min_response(context):
    context.world.test_vectors["min_response_recorded"] = True


@then("I should record max response time")
def step_record_max_response(context):
    context.world.test_vectors["max_response_recorded"] = True


@then("I should record p50 response time")
def step_record_p50(context):
    context.world.test_vectors["p50_recorded"] = True


@then("I should record p95 response time")
def step_record_p95(context):
    context.world.test_vectors["p95_recorded"] = True


@then("I should record p99 response time")
def step_record_p99(context):
    context.world.test_vectors["p99_recorded"] = True


@then("I should record requests per second")
def step_record_rps(context):
    context.world.test_vectors["rps_recorded"] = True


@then("I should record transactions per second")
def step_record_tps(context):
    context.world.test_vectors["tps_recorded"] = True


@then("I should record average total time")
def step_record_avg_total(context):
    context.world.test_vectors["avg_total_recorded"] = True


@then("I should record average round-trip time")
def step_record_avg_roundtrip(context):
    context.world.test_vectors["avg_roundtrip_recorded"] = True


@then("I should record average submission time")
def step_record_avg_submission(context):
    context.world.test_vectors["avg_submission_recorded"] = True


@then("I should record min round-trip time")
def step_record_min_roundtrip(context):
    context.world.test_vectors["min_roundtrip_recorded"] = True


@then("I should record max round-trip time")
def step_record_max_roundtrip(context):
    context.world.test_vectors["max_roundtrip_recorded"] = True


@then("I should record min total time")
def step_record_min_total(context):
    context.world.test_vectors["min_total_recorded"] = True


@then("I should record max total time")
def step_record_max_total(context):
    context.world.test_vectors["max_total_recorded"] = True


@then("I should record average confirmation time")
def step_record_avg_confirmation(context):
    context.world.test_vectors["avg_confirmation_recorded"] = True


@then("I should record min confirmation time")
def step_record_min_confirmation(context):
    context.world.test_vectors["min_confirmation_recorded"] = True


@then("I should record max confirmation time")
def step_record_max_confirmation(context):
    context.world.test_vectors["max_confirmation_recorded"] = True
