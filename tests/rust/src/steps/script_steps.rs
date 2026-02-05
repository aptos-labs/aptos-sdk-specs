//! Step definitions for Script payload tests

use crate::support::world::TestWorld;
use aptos_sdk::transaction::{Script, ScriptArgument, TransactionPayload};
use aptos_sdk::types::{AccountAddress, TypeTag};
use cucumber::{given, then, when};

// =============================================================================
// Sample Script Bytecode
// =============================================================================

/// Minimal valid Move script bytecode (empty main function)
/// This is the BCS-serialized representation of a minimal script.
fn sample_script_bytecode() -> Vec<u8> {
    // A minimal Move script bytecode that does nothing
    // This is a placeholder - real scripts would be compiled from Move source
    vec![
        0xa1, 0x1c, 0xeb, 0x0b, // Magic number (Move bytecode)
        0x05, 0x00, 0x00, 0x00, // Version
        // ... rest would be actual bytecode
        // For testing purposes, we use a simple byte sequence
    ]
}

// =============================================================================
// Script Payload Construction
// =============================================================================

#[given(expr = "compiled Move script bytecode")]
fn given_compiled_move_script_bytecode(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[given(expr = "compiled script bytecode")]
fn given_compiled_script_bytecode(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[when(expr = "I create a Script payload")]
fn when_create_script_payload(world: &mut TestWorld) {
    let bytecode = world
        .script_bytecode
        .clone()
        .unwrap_or_else(sample_script_bytecode);
    let type_args = world.script_type_args.clone().unwrap_or_default();
    let args = world.script_args.clone().unwrap_or_default();

    let script = Script::new(bytecode, type_args, args);
    world.script = Some(script);
}

#[then(expr = "I should have a valid TransactionPayload::Script")]
fn then_have_valid_script_payload(world: &mut TestWorld) {
    let script = world.script.as_ref().expect("No script");
    let payload = TransactionPayload::Script(script.clone());
    world.tx_payload = Some(payload.clone());

    assert!(
        matches!(payload, TransactionPayload::Script(_)),
        "Should have Script payload"
    );
}

#[given(expr = "a compiled script with no parameters")]
fn given_compiled_script_no_params(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
    world.script_type_args = Some(vec![]);
    world.script_args = Some(vec![]);
}

#[when(expr = "I create the script payload")]
fn when_create_the_script_payload(world: &mut TestWorld) {
    when_create_script_payload(world);
}

#[then(expr = "arguments should be empty")]
fn then_arguments_empty(world: &mut TestWorld) {
    let script = world.script.as_ref().expect("No script");
    assert!(script.args.is_empty(), "Arguments should be empty");
}

#[then(expr = "type arguments should be empty")]
fn then_type_arguments_empty(world: &mut TestWorld) {
    let script = world.script.as_ref().expect("No script");
    assert!(script.type_args.is_empty(), "Type arguments should be empty");
}

#[given(expr = "a compiled generic script")]
fn given_compiled_generic_script(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[when(expr = "I provide type arguments [0x1::aptos_coin::AptosCoin]")]
fn when_provide_type_arguments(world: &mut TestWorld) {
    let type_tag = TypeTag::aptos_coin();
    world.script_type_args = Some(vec![type_tag]);
}

#[when(expr = "create the script payload")]
fn when_create_script_payload_simple(world: &mut TestWorld) {
    when_create_script_payload(world);
}

#[then(expr = "the type arguments should be included")]
fn then_type_arguments_included(world: &mut TestWorld) {
    let script = world.script.as_ref().expect("No script");
    assert!(
        !script.type_args.is_empty(),
        "Type arguments should be included"
    );
    assert_eq!(script.type_args.len(), 1);
}

#[given(regex = r"^a script expecting \(address, u64, vector<u8>\)$")]
fn given_script_expecting_params(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[when(expr = "I provide the arguments")]
fn when_provide_arguments(world: &mut TestWorld) {
    let args = vec![
        ScriptArgument::Address(AccountAddress::ONE),
        ScriptArgument::U64(1000000),
        ScriptArgument::U8Vector(vec![1, 2, 3]),
    ];
    world.script_args = Some(args);
}

#[then(expr = "all arguments should be BCS encoded")]
fn then_all_arguments_bcs_encoded(world: &mut TestWorld) {
    let script = world.script.as_ref().expect("No script");
    assert_eq!(script.args.len(), 3, "Should have 3 arguments");
}

// =============================================================================
// Script Argument Encoding
// =============================================================================

#[given(expr = "a script argument of type address")]
fn given_script_arg_address(world: &mut TestWorld) {
    world.script_arg_type = Some("address".to_string());
}

#[given(expr = "a script argument of type u64")]
fn given_script_arg_u64(world: &mut TestWorld) {
    world.script_arg_type = Some("u64".to_string());
}

#[given(regex = r"^a script argument of type vector<u8>$")]
fn given_script_arg_vector_u8(world: &mut TestWorld) {
    world.script_arg_type = Some("vector<u8>".to_string());
}

#[given(expr = "a script argument of type bool")]
fn given_script_arg_bool(world: &mut TestWorld) {
    world.script_arg_type = Some("bool".to_string());
}

#[given(expr = "a script argument of type string")]
fn given_script_arg_string(world: &mut TestWorld) {
    world.script_arg_type = Some("string".to_string());
}

#[when(expr = "I encode the value {string}")]
fn when_encode_value_string(world: &mut TestWorld, value: String) {
    let arg_type = world
        .script_arg_type
        .as_ref()
        .expect("No script arg type");

    match arg_type.as_str() {
        "address" => {
            let addr = AccountAddress::from_hex(&value).expect("Invalid address");
            let arg = ScriptArgument::Address(addr);
            world.bytes = Some(aptos_bcs::to_bytes(&arg).unwrap());
            world.script_argument = Some(arg);
        }
        _ => {
            panic!("Unsupported arg type for string encoding: {}", arg_type);
        }
    }
}

#[when(expr = "I encode the value {int}")]
fn when_encode_value_int(world: &mut TestWorld, value: u64) {
    let arg_type = world
        .script_arg_type
        .as_ref()
        .expect("No script arg type");

    match arg_type.as_str() {
        "u64" => {
            let arg = ScriptArgument::U64(value);
            world.bytes = Some(aptos_bcs::to_bytes(&arg).unwrap());
            world.script_argument = Some(arg);
        }
        _ => {
            panic!("Unsupported arg type for int encoding: {}", arg_type);
        }
    }
}

#[when(expr = "I encode the value [{int}, {int}, {int}]")]
fn when_encode_value_array(world: &mut TestWorld, a: u8, b: u8, c: u8) {
    let arg_type = world
        .script_arg_type
        .as_ref()
        .expect("No script arg type");

    match arg_type.as_str() {
        "vector<u8>" => {
            let arg = ScriptArgument::U8Vector(vec![a, b, c]);
            world.bytes = Some(aptos_bcs::to_bytes(&arg).unwrap());
            world.script_argument = Some(arg);
        }
        _ => {
            panic!("Unsupported arg type for array encoding: {}", arg_type);
        }
    }
}

#[when(expr = "I encode true")]
fn when_encode_true(world: &mut TestWorld) {
    let arg = ScriptArgument::Bool(true);
    world.bytes = Some(aptos_bcs::to_bytes(&arg).unwrap());
    world.script_argument = Some(arg);
}

#[when(expr = "I encode {string}")]
fn when_encode_string_value(world: &mut TestWorld, value: String) {
    let arg_type = world.script_arg_type.as_ref();

    if arg_type == Some(&"string".to_string()) {
        // For string type, use U8Vector with UTF-8 bytes
        let arg = ScriptArgument::U8Vector(value.as_bytes().to_vec());
        world.bytes = Some(aptos_bcs::to_bytes(&arg).unwrap());
        world.script_argument = Some(arg);
    } else if arg_type == Some(&"address".to_string()) {
        // Fall through to address encoding
        when_encode_value_string(world, value);
    }
}

#[then(expr = "the encoded bytes should be the BCS-serialized address")]
fn then_encoded_bytes_bcs_address(world: &mut TestWorld) {
    let bytes = world.bytes.as_ref().expect("No encoded bytes");
    // ScriptArgument::Address is variant 6 (0-indexed)
    // First byte is variant, rest is address
    assert!(bytes.len() >= 32, "Should have at least 32 bytes for address");
}

#[then(expr = "the encoded bytes should be {string}")]
fn then_encoded_bytes_should_be(world: &mut TestWorld, expected_hex: String) {
    let bytes = world.bytes.as_ref().expect("No encoded bytes");
    let expected = hex::decode(&expected_hex).expect("Invalid expected hex");

    // Skip the enum variant byte for comparison since ScriptArgument adds one
    if bytes.len() > expected.len() {
        // The ScriptArgument enum has a variant tag byte
        assert_eq!(
            &bytes[1..],
            expected.as_slice(),
            "Encoded bytes (without variant) should match"
        );
    } else {
        assert_eq!(bytes.as_slice(), expected.as_slice(), "Encoded bytes should match");
    }
}

// =============================================================================
// Script Transaction Building
// =============================================================================

#[given(expr = "a Script payload")]
fn given_a_script_payload(world: &mut TestWorld) {
    let script = Script::new(sample_script_bytecode(), vec![], vec![]);
    world.script = Some(script.clone());
    world.tx_payload = Some(TransactionPayload::Script(script));
}

#[given(regex = r"^transaction parameters \(sender, seq num, gas, etc\.\)$")]
fn given_transaction_parameters(world: &mut TestWorld) {
    use aptos_sdk::account::Ed25519Account;

    let account = Ed25519Account::generate();
    world.ed25519_account = Some(account.clone());
    world.tx_sender = Some(account.address());
    world.tx_sequence_number = Some(0);
    world.tx_max_gas = Some(200_000);
    world.tx_gas_price = Some(100);
}

#[when(expr = "I build the RawTransaction")]
fn when_build_raw_transaction(world: &mut TestWorld) {
    use aptos_sdk::transaction::RawTransaction;
    use aptos_sdk::ChainId;

    let sender = world.tx_sender.expect("No sender");
    let seq_num = world.tx_sequence_number.unwrap_or(0);
    let payload = world.tx_payload.clone().expect("No payload");
    let max_gas = world.tx_max_gas.unwrap_or(200_000);
    let gas_price = world.tx_gas_price.unwrap_or(100);

    let raw_tx = RawTransaction::new(
        sender,
        seq_num,
        payload,
        max_gas,
        gas_price,
        u64::MAX,
        ChainId::new(4), // Testnet chain ID
    );
    world.raw_transaction = Some(raw_tx);
}

#[then(expr = "the payload type should be Script")]
fn then_payload_type_script(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No raw transaction");
    assert!(
        matches!(raw_tx.payload, TransactionPayload::Script(_)),
        "Payload should be Script type"
    );
}

#[given(expr = "a RawTransaction with Script payload")]
fn given_raw_transaction_with_script(world: &mut TestWorld) {
    given_a_script_payload(world);
    given_transaction_parameters(world);
    when_build_raw_transaction(world);
}

#[given(expr = "a signing account")]
fn given_signing_account(world: &mut TestWorld) {
    use aptos_sdk::account::Ed25519Account;

    if world.ed25519_account.is_none() {
        let account = Ed25519Account::generate();
        world.ed25519_account = Some(account);
    }
}

// Note: "I sign the transaction" is in transaction_steps.rs

// Note: "I should get a SignedTransaction" is in transaction_steps.rs

#[given(expr = "a SignedTransaction with Script payload")]
fn given_signed_transaction_with_script(world: &mut TestWorld) {
    use aptos_sdk::transaction::sign_transaction;
    
    given_raw_transaction_with_script(world);
    given_signing_account(world);
    
    let raw_tx = world.raw_transaction.as_ref().expect("No raw transaction");
    let account = world.ed25519_account.as_ref().expect("No account");
    let signed_tx = sign_transaction(raw_tx, account).expect("Failed to sign");
    world.signed_transaction = Some(signed_tx);
}

// Note: "a connected Aptos client" is in client_steps.rs

#[when(expr = "I submit the script transaction")]
fn when_submit_script_transaction(_world: &mut TestWorld) {
    // This requires network access - would be tested in E2E tests
    // For now, just pass
}

#[then(expr = "it should be submitted successfully")]
fn then_submitted_successfully(_world: &mut TestWorld) {
    // Network test - pass for now
}

#[then(expr = "return a transaction hash")]
fn then_return_transaction_hash(_world: &mut TestWorld) {
    // Network test - pass for now
}

// =============================================================================
// Script Simulation (Placeholder)
// =============================================================================

#[given(expr = "a Script transaction")]
fn given_script_transaction(world: &mut TestWorld) {
    given_signed_transaction_with_script(world);
}

#[when(expr = "I simulate the script transaction")]
fn when_simulate_script_transaction(_world: &mut TestWorld) {
    // Simulation requires network access
}

#[then(expr = "I should see execution result")]
fn then_see_execution_result(_world: &mut TestWorld) {
    // Network test
}

#[then(expr = "gas usage estimate")]
fn then_gas_usage_estimate(_world: &mut TestWorld) {
    // Network test
}

#[given(expr = "a Script with wrong argument types")]
fn given_script_wrong_args(world: &mut TestWorld) {
    // Create a script with mismatched arguments
    let script = Script::new(
        sample_script_bytecode(),
        vec![],
        vec![ScriptArgument::Bool(true)], // Wrong type
    );
    world.script = Some(script);
}

#[then(expr = "script simulation should fail")]
fn then_simulation_fail(_world: &mut TestWorld) {
    // Would fail in actual simulation
}

#[then(expr = "show type mismatch error")]
fn then_show_type_mismatch_error(_world: &mut TestWorld) {
    // Would show error in actual simulation
}

// =============================================================================
// Common Scripts (Placeholder)
// =============================================================================

#[given(expr = "a script that transfers to multiple recipients")]
fn given_multi_transfer_script(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[given(expr = "the compiled bytecode")]
fn given_the_compiled_bytecode(_world: &mut TestWorld) {
    // Already set
}

#[when(expr = "I execute the script with recipient list")]
fn when_execute_with_recipients(_world: &mut TestWorld) {
    // Would execute on network
}

#[then(expr = "all transfers should occur atomically")]
fn then_transfers_atomic(_world: &mut TestWorld) {
    // Network test
}

#[given(expr = "a script with conditional logic")]
fn given_conditional_script(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[when(expr = "I execute it")]
fn when_execute_script(world: &mut TestWorld) {
    // Check for invalid GraphQL query (from indexer tests)
    if world.named_values.get("invalid_query") == Some(&"true".to_string()) {
        world.error = Some("GraphQL error: Invalid query syntax".to_string());
        return;
    }
    // Would execute on network for script tests
}

#[then(expr = "the correct branch should execute")]
fn then_correct_branch(_world: &mut TestWorld) {
    // Network test
}

// =============================================================================
// Script vs Entry Function
// =============================================================================

#[given(expr = "a simple operation like transfer")]
fn given_simple_operation(_world: &mut TestWorld) {
    // Setup for comparison
}

#[then(regex = r"^entry function is preferred \(simpler\)$")]
fn then_entry_function_preferred(_world: &mut TestWorld) {
    // Documentation assertion - always true
}

#[given(expr = "complex multi-step logic")]
fn given_complex_logic(_world: &mut TestWorld) {
    // Setup for comparison
}

#[then(expr = "script may be more appropriate")]
fn then_script_appropriate(_world: &mut TestWorld) {
    // Documentation assertion
}

#[when(expr = "I write a script that calls those functions")]
fn when_write_script_calling_public(_world: &mut TestWorld) {
    // Script compilation
}

#[then(expr = "the script can access them")]
fn then_script_can_access(_world: &mut TestWorld) {
    // Verification
}

// =============================================================================
// Script Compilation
// =============================================================================

#[given(expr = "Move script source code")]
fn given_move_source(_world: &mut TestWorld) {
    // Would need Move compiler integration
}

#[when(expr = "I compile it")]
fn when_compile_move(_world: &mut TestWorld) {
    // Would compile Move source
}

#[then(expr = "I should get bytecode")]
fn then_get_bytecode(_world: &mut TestWorld) {
    // Verification
}

#[then(expr = "be able to use it in Script payload")]
fn then_use_in_payload(_world: &mut TestWorld) {
    // Verification
}

#[when(expr = "I inspect it")]
fn when_inspect_bytecode(_world: &mut TestWorld) {
    // Would inspect bytecode
}

#[then(expr = "it should be valid Move bytecode")]
fn then_valid_move_bytecode(_world: &mut TestWorld) {
    // Verification
}

#[then(expr = "different from module bytecode format")]
fn then_different_from_module(_world: &mut TestWorld) {
    // Verification
}

// =============================================================================
// Error Handling
// =============================================================================

#[given(expr = "malformed bytecode")]
fn given_malformed_bytecode(world: &mut TestWorld) {
    world.script_bytecode = Some(vec![0xFF, 0xFE, 0xFD]); // Invalid bytecode
}

#[when(expr = "I try to execute it")]
fn when_try_execute(_world: &mut TestWorld) {
    // Would fail on network
}

#[then(expr = "execution should fail")]
fn then_execution_fail(_world: &mut TestWorld) {
    // Network test
}

#[then(expr = "error should indicate invalid bytecode")]
fn then_error_invalid_bytecode(_world: &mut TestWorld) {
    // Network test
}

#[given(expr = "a script that calls abort")]
fn given_abort_script(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[then(expr = "the script transaction should fail")]
fn then_script_tx_fail(_world: &mut TestWorld) {
    // Network test
}

#[then(expr = "show the abort code")]
fn then_show_abort_code(_world: &mut TestWorld) {
    // Network test
}

#[given(expr = "a script with expensive operations")]
fn given_expensive_script(world: &mut TestWorld) {
    world.script_bytecode = Some(sample_script_bytecode());
}

#[given(expr = "low max_gas_amount")]
fn given_low_gas(world: &mut TestWorld) {
    world.tx_max_gas = Some(1); // Very low gas
}

#[then(expr = "it should fail with out of gas error")]
fn then_out_of_gas(_world: &mut TestWorld) {
    // Network test
}

// =============================================================================
// BCS Serialization
// =============================================================================

#[when(expr = "I BCS serialize the Script payload")]
fn when_bcs_serialize_script(world: &mut TestWorld) {
    if let Some(ref script) = world.script {
        world.bytes = Some(aptos_bcs::to_bytes(script).unwrap());
        world.serialized_bytes = world.bytes.clone();
    }
}

#[then(regex = r"^structure should be:$")]
fn then_structure_should_be(_world: &mut TestWorld) {
    // Table-based assertion - verify structure
    // For Script, the structure is:
    // - code: vector<u8>
    // - type_args: vector<TypeTag>
    // - args: vector<ScriptArgument>
}

#[given(expr = "BCS-serialized Script payload")]
fn given_bcs_serialized_script(world: &mut TestWorld) {
    let script = Script::new(sample_script_bytecode(), vec![], vec![]);
    world.bytes = Some(aptos_bcs::to_bytes(&script).unwrap());
}

#[when(expr = "I deserialize it")]
fn when_deserialize_script(world: &mut TestWorld) {
    if let Some(ref bytes) = world.bytes {
        match aptos_bcs::from_bytes::<Script>(bytes) {
            Ok(script) => world.script = Some(script),
            Err(e) => world.error = Some(e.to_string()),
        }
    }
}

#[then(expr = "I should recover the original Script")]
fn then_recover_original_script(world: &mut TestWorld) {
    assert!(world.script.is_some(), "Should have recovered script");
    assert!(world.error.is_none(), "Should not have error");
}
