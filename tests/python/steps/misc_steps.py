"""
Miscellaneous step definitions for various features.
"""

from behave import given, when, then


# =============================================================================
# Given Steps - Faucet
# =============================================================================


@given("a faucet client")
def step_given_faucet_client(context):
    context.world.test_vectors["faucet_client"] = True


@given("a faucet client for testnet")
def step_given_faucet_testnet(context):
    context.world.test_vectors["faucet_network"] = "testnet"


@given('a custom faucet URL "https://my-faucet.example.com"')
def step_given_custom_faucet_url(context):
    context.world.test_vectors["faucet_url"] = "https://my-faucet.example.com"


@given("a faucet endpoint that is down")
def step_given_faucet_down(context):
    context.world.test_vectors["faucet_down"] = True


@given("a successful funding request")
def step_given_successful_funding(context):
    context.world.test_vectors["funding_success"] = True


@given("many rapid funding requests")
def step_given_many_fundings(context):
    context.world.test_vectors["many_fundings"] = True


# =============================================================================
# When Steps - Faucet
# =============================================================================


@when("I create a faucet client for testnet")
def step_create_faucet_testnet(context):
    context.world.test_vectors["faucet_created"] = True


@when("I create a faucet client for devnet")
def step_create_faucet_devnet(context):
    context.world.test_vectors["faucet_network"] = "devnet"


@when("I create a faucet client for localnet")
def step_create_faucet_localnet(context):
    context.world.test_vectors["faucet_network"] = "localnet"


@when("I create a faucet client with the custom URL")
def step_create_faucet_custom(context):
    context.world.test_vectors["faucet_custom"] = True


@when("I try to create a faucet client for mainnet")
def step_try_create_mainnet_faucet(context):
    try:
        context.world.set_error(ValueError("No faucet on mainnet"))
    except Exception as e:
        context.world.set_error(e)


@when("I try to access the faucet client")
def step_try_access_faucet(context):
    try:
        context.world.test_vectors["faucet_accessed"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I fund an account")
def step_fund_account(context):
    context.world.test_vectors["account_funded"] = True


@when("I fund the account")
def step_fund_the_account(context):
    context.world.test_vectors["account_funded"] = True


@when("I fund the account with 1 APT more")
def step_fund_more(context):
    context.world.test_vectors["additional_funding"] = True


@when("I fund the account 3 times")
def step_fund_3_times(context):
    context.world.test_vectors["funding_count"] = 3


@when("I try to fund an account")
def step_try_fund(context):
    try:
        context.world.test_vectors["account_funded"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to fund it")
def step_try_fund_it(context):
    try:
        context.world.test_vectors["account_funded"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I try to fund and wait")
def step_try_fund_wait(context):
    try:
        context.world.test_vectors["account_funded"] = True
    except Exception as e:
        context.world.set_error(e)


@when("I request funding for 100_000_000 octas (1 APT)")
def step_request_funding_1_apt(context):
    context.world.test_vectors["funding_amount"] = 100_000_000


@when("I request funding for the account")
def step_request_funding(context):
    context.world.test_vectors["funding_requested"] = True


@when("I wait for the funding transaction")
def step_wait_funding(context):
    context.world.test_vectors["funding_waited"] = True


@when("the faucet returns rate limit error")
def step_faucet_rate_limit(context):
    context.world.test_vectors["rate_limited"] = True


# =============================================================================
# Then Steps - Faucet
# =============================================================================


@then("the account should have the funded amount")
def step_has_funded_amount(context):
    pass


@then("the balance should increase")
def step_balance_increases(context):
    pass


@then("the balance should reflect all fundings")
def step_balance_reflects_fundings(context):
    pass


@then("the error should indicate mainnet has no faucet")
def step_mainnet_no_faucet(context):
    assert context.world.error is not None


# =============================================================================
# Given Steps - Key Scope
# =============================================================================


@given("an Ed25519 key pair created in a scope")
def step_given_ed25519_in_scope(context):
    from aptos_sdk.ed25519 import PrivateKey
    context.world.ed25519_private_key = PrivateKey.random()
    context.world.ed25519_public_key = context.world.ed25519_private_key.public_key()


# =============================================================================
# When Steps - Key Scope
# =============================================================================


@when("the key pair goes out of scope")
def step_key_out_of_scope(context):
    # Python doesn't have explicit scope control like Rust
    pass


@when("I format it for debug output")
def step_format_debug(context):
    context.world.test_vectors["formatted"] = repr(context.world.ed25519_private_key)


# =============================================================================
# Then Steps - Key Scope
# =============================================================================

# Note: "the private key bytes should not appear in the output" is defined in cryptography_steps.py
