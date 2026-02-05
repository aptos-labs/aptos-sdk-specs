"""
Step definitions for SDK-specific tests and language variations.
"""

from behave import given

# =============================================================================
# Given Steps - SDK Types
# =============================================================================


@given("Go SDK")
def step_given_go_sdk(context):
    context.world.test_vectors["sdk_type"] = "go"


@given("Python SDK")
def step_given_python_sdk(context):
    context.world.test_vectors["sdk_type"] = "python"


@given("Rust SDK")
def step_given_rust_sdk(context):
    context.world.test_vectors["sdk_type"] = "rust"


@given("TypeScript SDK")
def step_given_ts_sdk(context):
    context.world.test_vectors["sdk_type"] = "typescript"


# =============================================================================
# Given Steps - Transaction Scenarios
# =============================================================================


@given("a transaction")
def step_given_transaction(context):
    context.world.test_vectors["transaction"] = True


@given("a transfer transaction")
def step_given_transfer_tx(context):
    context.world.test_vectors["transfer_tx"] = True


@given("a simple transfer")
def step_given_simple_transfer(context):
    context.world.test_vectors["simple_transfer"] = True


@given("a complex transaction")
def step_given_complex_tx(context):
    context.world.test_vectors["complex_tx"] = True


@given("a very complex transaction")
def step_given_very_complex_tx(context):
    context.world.test_vectors["very_complex_tx"] = True


@given("a failed transaction")
def step_given_failed_tx(context):
    context.world.test_vectors["failed_tx"] = True


@given("a simulation")
def step_given_simulation(context):
    context.world.test_vectors["simulation"] = True


@given("a successful simulation")
def step_given_successful_sim(context):
    context.world.test_vectors["successful_simulation"] = True


@given("a transaction simulation")
def step_given_tx_simulation(context):
    context.world.test_vectors["tx_simulation"] = True


@given("a transaction simulation that fails")
def step_given_tx_sim_fails(context):
    context.world.test_vectors["tx_sim_fails"] = True


@given("a malformed transaction")
def step_given_malformed_tx(context):
    context.world.test_vectors["malformed_tx"] = True


@given("a transfer exceeding sender's balance")
def step_given_transfer_exceeds(context):
    context.world.test_vectors["transfer_exceeds"] = True


@given("a transaction I haven't signed yet")
def step_given_unsigned_tx(context):
    context.world.test_vectors["unsigned_tx"] = True


@given("a transaction accessing non-existent resource")
def step_given_tx_nonexistent_resource(context):
    context.world.test_vectors["nonexistent_resource_tx"] = True


@given("a transaction that emits events")
def step_given_tx_emits_events(context):
    context.world.test_vectors["tx_emits_events"] = True


@given("a transaction that modifies resources")
def step_given_tx_modifies_resources(context):
    context.world.test_vectors["tx_modifies_resources"] = True


@given("a transaction that would abort")
def step_given_tx_would_abort(context):
    context.world.test_vectors["tx_would_abort"] = True


@given("a transaction that ran out of gas")
def step_given_tx_out_of_gas(context):
    context.world.test_vectors["tx_out_of_gas"] = True


@given("a transaction with wrong type arguments")
def step_given_tx_wrong_type_args(context):
    context.world.test_vectors["tx_wrong_type_args"] = True


@given('a transaction with vm_status "success"')
def step_given_tx_vm_success(context):
    context.world.test_vectors["vm_status"] = "success"


@given("a transaction with vm_status containing abort code")
def step_given_tx_vm_abort(context):
    context.world.test_vectors["vm_abort_code"] = True


@given("a transaction failing due to insufficient balance")
def step_given_tx_insufficient_balance(context):
    context.world.test_vectors["insufficient_balance"] = True


@given("a transaction rejected for wrong sequence number")
def step_given_tx_wrong_seq(context):
    context.world.test_vectors["wrong_seq_number"] = True


@given("a transaction rejection for invalid signature")
def step_given_tx_invalid_sig(context):
    context.world.test_vectors["invalid_signature"] = True


# =============================================================================
# Given Steps - Errors
# =============================================================================


@given("API is unavailable")
def step_given_api_unavailable(context):
    context.world.test_vectors["api_unavailable"] = True


@given("a 429 Too Many Requests error")
def step_given_429_error(context):
    context.world.test_vectors["http_status"] = 429


@given("a SEQUENCE_NUMBER_TOO_OLD error")
def step_given_seq_too_old(context):
    context.world.test_vectors["seq_too_old"] = True


@given("an API error response (4xx or 5xx)")
def step_given_api_error(context):
    context.world.test_vectors["api_error"] = True


@given("an API error with request ID header")
def step_given_api_error_request_id(context):
    context.world.test_vectors["request_id_error"] = True


@given("a low-level error (e.g., JSON parse error)")
def step_given_low_level_error(context):
    context.world.test_vectors["low_level_error"] = True


@given("a network timeout or connection failure")
def step_given_network_failure(context):
    context.world.test_vectors["network_failure"] = True


# =============================================================================
# Given Steps - Benchmarking
# =============================================================================


@given("a funded Ed25519 account for benchmarking")
def step_given_funded_ed25519_benchmark(context):
    from aptos_sdk.account import Account

    context.world.account = Account.generate()
    context.world.test_vectors["benchmark_account"] = True


@given("an Ed25519 key pair for benchmarking")
def step_given_ed25519_benchmark(context):
    from aptos_sdk.ed25519 import PrivateKey

    context.world.ed25519_private_key = PrivateKey.random()
    context.world.ed25519_public_key = context.world.ed25519_private_key.public_key()


@given("a sample raw transaction for benchmarking")
def step_given_sample_tx_benchmark(context):
    context.world.test_vectors["sample_tx"] = True


@given("a known funded account address")
def step_given_known_funded_address(context):
    context.world.test_vectors["known_funded_address"] = "0x1"


# =============================================================================
# Given Steps - Other
# =============================================================================


@given("a 256-byte message")
def step_given_256_byte_message(context):
    context.world.message = bytes(256)


@given("a signed 256-byte message")
def step_given_signed_256_byte(context):
    context.world.message = bytes(256)
    if context.world.ed25519_private_key:
        context.world.ed25519_signature = context.world.ed25519_private_key.sign(
            context.world.message
        )


@given("a configured Aptos client for devnet")
def step_given_client_devnet(context):
    context.world.test_vectors["network"] = "devnet"


@given("a historical ledger version")
def step_given_historical_version(context):
    context.world.test_vectors["historical_version"] = 1000


@given("a CLI tool for code generation")
def step_given_cli_codegen(context):
    # TODO: awaiting SDK implementation - codegen CLI
    context.scenario.skip("Codegen CLI not supported in Python SDK")


@given("a Rust procedural macro")
def step_given_rust_macro(context):
    # Not applicable to Python
    context.scenario.skip("Rust macros not applicable to Python SDK")


@given("a Move module with doc comments")
def step_given_move_doc_comments(context):
    context.world.test_vectors["module_with_docs"] = True


@given("a local ABI JSON file")
def step_given_local_abi(context):
    context.world.test_vectors["local_abi"] = True


@given("a function with Option<T> parameter")
def step_given_option_param(context):
    context.world.test_vectors["option_param"] = True


@given("a generic function like transfer<CoinType>")
def step_given_generic_function(context):
    context.world.test_vectors["generic_function"] = True


@given("a generated function with constraints")
def step_given_func_constraints(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@given("a generated function call that aborts")
def step_given_func_aborts(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@given('a passphrase "mysecretpassphrase"')
def step_given_passphrase(context):
    context.world.passphrase = "mysecretpassphrase"
