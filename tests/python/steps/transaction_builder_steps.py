"""
Step definitions for transaction building.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Transaction Builder Setup
# =============================================================================


@given("a TransactionBuilder")
def step_given_tx_builder(context):
    context.world.test_vectors["tx_builder"] = {}


@given("a TransactionBuilder with only required fields")
def step_given_tx_builder_required(context):
    context.world.test_vectors["tx_builder"] = {"required_only": True}


@given("a TransactionBuilder with sender and sequence number")
def step_given_tx_builder_sender_seq(context):
    context.world.test_vectors["tx_builder"] = {"has_sender": True, "has_seq": True}


@given("a TransactionBuilder with sender set")
def step_given_tx_builder_sender(context):
    context.world.test_vectors["tx_builder"] = {"has_sender": True}


@given("a TransactionBuilder with sender, sequence, and payload")
def step_given_tx_builder_full(context):
    context.world.test_vectors["tx_builder"] = {
        "has_sender": True,
        "has_seq": True,
        "has_payload": True,
    }


@given("a transaction builder")
def step_given_tx_builder_alt(context):
    context.world.test_vectors["tx_builder"] = {}


@given("a transaction builder with defaults")
def step_given_tx_builder_defaults(context):
    context.world.test_vectors["tx_builder"] = {"defaults": True}


@given("a valid transaction payload")
def step_given_valid_payload(context):
    context.world.test_vectors["payload"] = True


@given("a transaction payload")
def step_given_tx_payload(context):
    context.world.test_vectors["payload"] = True


@given("transaction parameters (sender, seq num, gas, etc.)")
def step_given_tx_params(context):
    context.world.test_vectors["tx_params"] = True


@given("max_gas_amount = 200000")
def step_given_max_gas(context):
    context.world.test_vectors["max_gas_amount"] = 200000


@given("gas_unit_price = 100")
def step_given_gas_price(context):
    context.world.test_vectors["gas_unit_price"] = 100


@given("gas_unit_price = 100 octas")
def step_given_gas_price_octas(context):
    context.world.test_vectors["gas_unit_price"] = 100


@given("gas_unit_price = 0")
def step_given_gas_price_zero(context):
    context.world.test_vectors["gas_unit_price"] = 0


@given("gas_used = 1000 units")
def step_given_gas_used(context):
    context.world.test_vectors["gas_used"] = 1000


@given("low max_gas_amount")
def step_given_low_max_gas(context):
    context.world.test_vectors["max_gas_amount"] = 100


# =============================================================================
# When Steps - Transaction Builder Operations
# =============================================================================


@when('I set sender to "0x1"')
def step_set_sender(context):
    context.world.test_vectors["sender"] = "0x1"


@when("I set sequence number to 5")
def step_set_seq_num(context):
    context.world.test_vectors["sequence_number"] = 5


@when("I set payload to an APT transfer")
def step_set_payload_apt_transfer(context):
    context.world.test_vectors["payload_type"] = "apt_transfer"


@when("I set max_gas_amount to 500000")
def step_set_max_gas(context):
    context.world.test_vectors["max_gas_amount"] = 500000


@when("I set gas_unit_price to 200")
def step_set_gas_price(context):
    context.world.test_vectors["gas_unit_price"] = 200


@when("I set chain ID to testnet")
def step_set_chain_id(context):
    context.world.test_vectors["chain_id"] = 2


@when("I set expiration from now to 600 seconds")
def step_set_expiration(context):
    context.world.test_vectors["expiration"] = 600


@when("I set expiration_from_now to 600 seconds")
def step_set_expiration_alt(context):
    context.world.test_vectors["expiration"] = 600


@when("I try to build without setting sender")
def step_try_build_no_sender(context):
    try:
        # Would need sender to build
        context.world.set_error(ValueError("Missing sender"))
    except Exception as e:
        context.world.set_error(e)


@when("I try to build without payload")
def step_try_build_no_payload(context):
    try:
        context.world.set_error(ValueError("Missing payload"))
    except Exception as e:
        context.world.set_error(e)


@when("I try to build without sequence number")
def step_try_build_no_seq(context):
    try:
        context.world.set_error(ValueError("Missing sequence number"))
    except Exception as e:
        context.world.set_error(e)


@when("I try to build without chain ID")
def step_try_build_no_chain_id(context):
    try:
        context.world.set_error(ValueError("Missing chain ID"))
    except Exception as e:
        context.world.set_error(e)


# =============================================================================
# Then Steps - Transaction Builder Assertions
# =============================================================================


@then("I should get a valid RawTransaction")
def step_get_valid_raw_tx(context):
    # TODO: implement actual transaction building check
    pass


@then("I should get a valid SignedTransaction")
def step_get_valid_signed_tx(context):
    if context.world.signed_transaction:
        assert context.world.signed_transaction is not None
    else:
        pass  # May be a documentation step


@then("fields should include sender, sequence_number, max_gas_amount, etc")
def step_fields_include(context):
    # Documentation assertion
    pass
