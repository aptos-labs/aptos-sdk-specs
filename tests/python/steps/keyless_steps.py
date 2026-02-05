"""
Step definitions for keyless accounts and ZK proofs.
All steps marked pending as Python SDK may have limited keyless support.
"""

from behave import given, then

# =============================================================================
# Given Steps - Keyless Setup (Most Pending)
# =============================================================================


@given("a keyless account")
def step_given_keyless_account(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a valid keyless account")
def step_given_valid_keyless(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a keyless account from Google JWT")
def step_given_keyless_google(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a keyless account with valid proof")
def step_given_keyless_valid_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a keyless account with expired ZK proof")
def step_given_keyless_expired_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a keyless account with expired ephemeral key")
def step_given_keyless_expired_key(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a keyless account with expiring proof")
def step_given_keyless_expiring_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a valid JWT")
def step_given_valid_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a valid JWT from Google")
def step_given_valid_jwt_google(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given('a JWT with nonce "XYZ"')
def step_given_jwt_nonce(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a new JWT")
def step_given_new_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a malformed JWT string")
def step_given_malformed_jwt(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("JWT claims and pepper from test vectors")
def step_given_jwt_claims_vectors(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a pepper")
def step_given_pepper(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a pepper value")
def step_given_pepper_value(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a pepper from the pepper service")
def step_given_pepper_service(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a ZK proof from the prover service")
def step_given_zk_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a freshly generated ephemeral key pair")
def step_given_fresh_ephemeral(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("OidcProvider Google")
def step_given_oidc_google(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("OidcProvider Apple")
def step_given_oidc_apple(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@given("a custom OIDC issuer URL")
def step_given_custom_oidc(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


# =============================================================================
# Then Steps - Keyless Assertions (All Pending)
# =============================================================================


@then("the authenticator should be Keyless variant")
def step_auth_is_keyless(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("the account should have a new valid proof")
def step_account_has_proof(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("the ephemeral key pair should be valid")
def step_ephemeral_valid(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")


@then("the nonces should be different")
def step_nonces_different(context):
    # TODO: awaiting SDK implementation - keyless
    context.scenario.skip("Keyless not supported in Python SDK")
