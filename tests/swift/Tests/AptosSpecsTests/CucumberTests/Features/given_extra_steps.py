"""
Additional Given step definitions for various scenarios.
"""

from behave import given, when, then


# =============================================================================
# Given Steps - Account Types
# =============================================================================


@given("an Ed25519 sender")
def step_given_ed25519_sender(context):
    from aptos_sdk.account import Account
    context.world.account = Account.generate()


@given("fee payer account")
def step_given_fee_payer_account(context):
    from aptos_sdk.account import Account
    context.world.fee_payer = Account.generate()


@given("fee payer address A")
def step_given_fee_payer_address_a(context):
    from aptos_sdk.account import Account
    context.world.test_vectors["fee_payer_address"] = "A"


@given("fee payer has sufficient balance")
def step_given_fee_payer_sufficient(context):
    context.world.test_vectors["fee_payer_balance"] = "sufficient"


@given("fee payer has zero balance")
def step_given_fee_payer_zero(context):
    context.world.test_vectors["fee_payer_balance"] = 0


@given("secondary signer address A")
def step_given_secondary_address_a(context):
    context.world.test_vectors["secondary_address"] = "A"


@given("signature from account B")
def step_given_sig_from_b(context):
    context.world.test_vectors["signature_from"] = "B"


@given("signatures added in order 2, 0, 1")
def step_given_sigs_order(context):
    context.world.test_vectors["sig_order"] = [2, 0, 1]


@given("only 2 secondary signatures")
def step_given_2_secondary_sigs(context):
    context.world.test_vectors["secondary_sigs"] = 2


@given("sender creates valid transaction")
def step_given_sender_creates_valid(context):
    context.world.test_vectors["sender_tx_valid"] = True


@given("sender creates transaction with max_gas_amount=100")
def step_given_sender_creates_tx_100(context):
    context.world.test_vectors["max_gas_amount"] = 100


# =============================================================================
# Given Steps - Errors
# =============================================================================


@given("an OUT_OF_GAS error")
def step_given_out_of_gas(context):
    context.world.test_vectors["error_type"] = "OUT_OF_GAS"


@given("an abort from a custom module")
def step_given_custom_abort(context):
    context.world.test_vectors["error_type"] = "custom_abort"


@given('an error during "submit_transaction"')
def step_given_error_submit(context):
    context.world.test_vectors["error_during"] = "submit_transaction"


@given("an error shown to SDK users")
def step_given_error_shown(context):
    context.world.test_vectors["error_shown"] = True


@given("an error")
def step_given_error(context):
    context.world.test_vectors["error"] = True


@given("invalid input (e.g., malformed address)")
def step_given_invalid_input(context):
    context.world.test_vectors["invalid_input"] = True


@given("common abort codes like:")
def step_given_common_abort_codes(context):
    context.world.test_vectors["common_abort_codes"] = True


# =============================================================================
# Given Steps - Ephemeral Keys (Keyless - Pending)
# =============================================================================


@given("an ephemeral key pair")
def step_given_ephemeral_key(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given('an ephemeral key pair with nonce "ABC"')
def step_given_ephemeral_nonce(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("an ephemeral key pair with 1 second expiry")
def step_given_ephemeral_1s(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("an ephemeral key with 1 hour expiry")
def step_given_ephemeral_1h(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("an invalid ephemeral key")
def step_given_invalid_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# Given Steps - JWT (Keyless - Pending)
# =============================================================================


@given("an expired JWT")
def step_given_expired_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("an invalid JWT")
def step_given_invalid_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the same JWT")
def step_given_same_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the same JWT claims")
def step_given_same_claims(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the same JWT claims and pepper")
def step_given_same_claims_pepper(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("two JWTs with different user IDs")
def step_given_two_jwt_diff_users(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given('audience (client_id) "my-app.apps.googleusercontent.com"')
def step_given_audience(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given('user ID (sub) "123456789"')
def step_given_user_id(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given('issuer "https://accounts.google.com"')
def step_given_issuer(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the same issuer and user ID")
def step_given_same_issuer_user(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the same user ID and pepper")
def step_given_same_user_pepper(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("different issuers (Google vs Apple)")
def step_given_diff_issuers(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("different client_ids (audiences)")
def step_given_diff_client_ids(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("different peppers")
def step_given_diff_peppers(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# Given Steps - Services (Keyless - Pending)
# =============================================================================


@given("the pepper service endpoint")
def step_given_pepper_endpoint(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the same pepper service")
def step_given_same_pepper_service(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the prover service endpoint")
def step_given_prover_endpoint(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("the prover service")
def step_given_prover_service(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# Given Steps - Codegen (Pending)
# =============================================================================


@given("generated code")
def step_given_generated_code(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@given("the codegen CLI")
def step_given_codegen_cli(context):
    # TODO: awaiting SDK implementation - codegen
    context.scenario.skip("Codegen not supported in Python SDK")


@given("the contract macro")
def step_given_contract_macro(context):
    # Not applicable to Python
    context.scenario.skip("Rust macros not applicable to Python SDK")


# =============================================================================
# Given Steps - Transaction State
# =============================================================================


@given("multiple transactions")
def step_given_multiple_txs(context):
    context.world.test_vectors["multiple_txs"] = True


@given("transactions with sequential sequence numbers")
def step_given_sequential_seqs(context):
    context.world.test_vectors["sequential_seqs"] = True


@given("current sequence number is 5")
def step_given_seq_num_5(context):
    context.world.test_vectors["sequence_number"] = 5


@given("blockchain state changes between simulate and submit")
def step_given_state_changes(context):
    context.world.test_vectors["state_changes"] = True


@given("waiting for a transaction")
def step_given_waiting_tx(context):
    context.world.test_vectors["waiting_tx"] = True


@given("waiting for a transaction that fails")
def step_given_waiting_tx_fails(context):
    context.world.test_vectors["waiting_tx_fails"] = True


# =============================================================================
# Given Steps - Multi-party Transactions
# =============================================================================


@given("the same fee payer transaction")
def step_given_same_fee_payer_tx(context):
    context.world.test_vectors["same_fee_payer_tx"] = True


@given("the same multi-agent transaction")
def step_given_same_multi_agent_tx(context):
    context.world.test_vectors["same_multi_agent_tx"] = True


@given("threshold from test vectors")
def step_given_threshold_vectors(context):
    context.world.test_vectors["threshold_from_vectors"] = True


@given("public keys from test vectors")
def step_given_pubkeys_vectors(context):
    context.world.test_vectors["pubkeys_from_vectors"] = True
