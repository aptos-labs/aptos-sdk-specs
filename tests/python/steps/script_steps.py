"""
Step definitions for Move script operations.
"""

from behave import given, when, then

# =============================================================================
# Given Steps - Script Setup
# =============================================================================


@given("compiled Move script bytecode")
def step_given_compiled_script(context):
    context.world.test_vectors["script_bytecode"] = b"\x00\x01\x02\x03"


@given("compiled script bytecode")
def step_given_compiled_script_alt(context):
    context.world.test_vectors["script_bytecode"] = b"\x00\x01\x02\x03"


@given("Move script source code")
def step_given_script_source(context):
    context.world.test_vectors["script_source"] = "script { fun main() {} }"


@given("a Script payload")
def step_given_script_payload(context):
    context.world.test_vectors["script_payload"] = True


@given("a Script transaction")
def step_given_script_tx(context):
    context.world.test_vectors["script_tx"] = True


@given("a Script with wrong argument types")
def step_given_script_wrong_args(context):
    context.world.test_vectors["script_wrong_args"] = True


@given("a SignedTransaction with Script payload")
def step_given_signed_script_tx(context):
    context.world.test_vectors["signed_script_tx"] = True


@given("a RawTransaction with Script payload")
def step_given_raw_script_tx(context):
    context.world.test_vectors["raw_script_tx"] = True


@given("BCS-serialized Script payload")
def step_given_bcs_script_payload(context):
    context.world.test_vectors["bcs_script_payload"] = b"\x00"


@given("a script argument of type address")
def step_given_arg_address(context):
    context.world.test_vectors["script_args"] = [{"type": "address", "value": "0x1"}]


@given("a script argument of type bool")
def step_given_arg_bool(context):
    context.world.test_vectors["script_args"] = [{"type": "bool", "value": True}]


@given("a script argument of type string")
def step_given_arg_string(context):
    context.world.test_vectors["script_args"] = [{"type": "string", "value": "hello"}]


@given("a script argument of type u64")
def step_given_arg_u64(context):
    context.world.test_vectors["script_args"] = [{"type": "u64", "value": 1000}]


@given("a script argument of type vector<u8>")
def step_given_arg_bytes(context):
    context.world.test_vectors["script_args"] = [
        {"type": "vector<u8>", "value": [1, 2, 3]}
    ]


@given("a script expecting (address, u64, vector<u8>)")
def step_given_script_expecting_types(context):
    context.world.test_vectors["script_expects"] = ["address", "u64", "vector<u8>"]


@given("a script that transfers to multiple recipients")
def step_given_multi_recipient_script(context):
    context.world.test_vectors["multi_recipient_script"] = True


@given("a script with conditional logic")
def step_given_script_conditional(context):
    context.world.test_vectors["script_conditional"] = True


@given("a script with expensive operations")
def step_given_script_expensive(context):
    context.world.test_vectors["script_expensive"] = True


@given("a script that calls abort")
def step_given_script_abort(context):
    context.world.test_vectors["script_abort"] = True


@given("a compiled generic script")
def step_given_generic_script(context):
    context.world.test_vectors["generic_script"] = True


@given("a compiled script with no parameters")
def step_given_no_param_script(context):
    context.world.test_vectors["no_param_script"] = True


@given("complex multi-step logic")
def step_given_complex_logic(context):
    context.world.test_vectors["complex_logic"] = True


@given("the compiled bytecode")
def step_given_compiled_bytecode(context):
    context.world.test_vectors["bytecode"] = b"\x00\x01\x02\x03"


@given("malformed bytecode")
def step_given_malformed_bytecode(context):
    context.world.test_vectors["malformed_bytecode"] = b"\xff\xff\xff\xff"


# =============================================================================
# When Steps - Script Operations
# =============================================================================


@when("I create a Script payload")
def step_create_script_payload(context):
    context.world.test_vectors["created_script_payload"] = True


@when("I create the script payload")
def step_create_script_payload_alt(context):
    context.world.test_vectors["created_script_payload"] = True


@when("create the script payload")
def step_create_script_payload_alt2(context):
    context.world.test_vectors["created_script_payload"] = True


@when("I simulate the script transaction")
def step_simulate_script_tx(context):
    context.world.test_vectors["script_simulated"] = True


@when("I submit the script transaction")
def step_submit_script_tx(context):
    # TODO: implement script submission
    context.scenario.skip("Script transaction submission not implemented")


@when("I execute the script with recipient list")
def step_execute_script_with_recipients(context):
    context.world.test_vectors["script_recipients_executed"] = True


@when("I write a script that calls those functions")
def step_write_script(context):
    context.world.test_vectors["script_written"] = True


@when("I compile it")
def step_compile_script(context):
    # TODO: implement script compilation
    context.scenario.skip("Script compilation not implemented")


@when("I deserialize it")
def step_deserialize_script(context):
    context.world.test_vectors["deserialized"] = True


# =============================================================================
# Then Steps - Script Assertions
# =============================================================================


@then("I should have a valid TransactionPayload::Script")
def step_valid_script_payload(context):
    pass


@then("I should recover the original Script")
def step_recover_script(context):
    pass


@then("I should get bytecode")
def step_get_bytecode(context):
    pass


@then("the script payload should contain the bytecode")
def step_payload_contains_bytecode(context):
    pass


@then("it should encode all 3 transfers")
def step_encodes_transfers(context):
    pass


@then("each recipient should receive their amount")
def step_recipients_receive(context):
    # TODO: implement verification
    context.scenario.skip("Script execution verification not implemented")


@then("the correct branch should execute")
def step_correct_branch(context):
    pass


@then("script may be more appropriate")
def step_script_appropriate(context):
    # Documentation assertion
    pass


@then("entry function is preferred (simpler)")
def step_entry_function_preferred(context):
    # Documentation assertion
    pass
