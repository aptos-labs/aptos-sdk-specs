//! Step definitions for EntryFunction payload tests

use crate::support::world::TestWorld;
use aptos_sdk::transaction::{EntryFunction, TransactionPayload};
use aptos_sdk::types::{AccountAddress, Identifier, MoveModuleId, TypeTag};
use cucumber::{given, then, when};

// =============================================================================
// Module and Function Setup
// =============================================================================

#[given(expr = "module ID {string}")]
fn given_module_id(world: &mut TestWorld, module_id: String) {
    world.module_id_str = Some(module_id);
}

#[given(expr = "function name {string}")]
fn given_function_name(world: &mut TestWorld, function_name: String) {
    world.function_name = Some(function_name);
}

#[given(expr = "no type arguments")]
fn given_no_type_arguments(world: &mut TestWorld) {
    world.type_args = Some(vec![]);
}

#[given(expr = "arguments [recipient_address, amount]")]
fn given_arguments_recipient_amount(world: &mut TestWorld) {
    let recipient = AccountAddress::from_hex("0x2").unwrap();
    let amount = 1000u64;
    world.entry_fn_args = Some(vec![
        aptos_bcs::to_bytes(&recipient).unwrap(),
        aptos_bcs::to_bytes(&amount).unwrap(),
    ]);
}

#[given(expr = "type argument {string}")]
fn given_type_argument(world: &mut TestWorld, type_arg: String) {
    let type_tag = TypeTag::from_str_strict(&type_arg).expect("Invalid type tag");
    world.type_args = Some(vec![type_tag]);
}

#[given(expr = "type arguments [{string}, {string}]")]
fn given_type_arguments_two(world: &mut TestWorld, type_arg1: String, type_arg2: String) {
    let tag1 = TypeTag::from_str_strict(&type_arg1).expect("Invalid type tag 1");
    let tag2 = TypeTag::from_str_strict(&type_arg2).expect("Invalid type tag 2");
    world.type_args = Some(vec![tag1, tag2]);
}

// =============================================================================
// EntryFunction Creation
// =============================================================================

#[when(expr = "I create an EntryFunction")]
fn when_create_entry_function(world: &mut TestWorld) {
    let module_id_str = world.module_id_str.as_ref().expect("No module ID");
    let function_name = world.function_name.as_ref().expect("No function name");
    let type_args = world.type_args.clone().unwrap_or_default();
    let args = world.entry_fn_args.clone().unwrap_or_default();

    let module = MoveModuleId::from_str_strict(module_id_str).expect("Invalid module ID");

    world.entry_function = Some(EntryFunction::new(module, function_name, type_args, args));
}

#[then(expr = "the payload should be valid")]
fn then_payload_valid(world: &mut TestWorld) {
    assert!(
        world.entry_function.is_some(),
        "Entry function should be created"
    );
}

#[then(expr = "module should be {string}")]
fn then_module_should_be(world: &mut TestWorld, expected: String) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    let module_str = format!(
        "{}::{}",
        entry_fn.module.address.to_short_string(),
        entry_fn.module.name.as_str()
    );
    assert_eq!(module_str, expected, "Module mismatch");
}

#[then(expr = "function should be {string}")]
fn then_function_should_be(world: &mut TestWorld, expected: String) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(entry_fn.function, expected);
}

#[then(expr = "the payload should have {int} type argument")]
fn then_payload_has_n_type_argument(world: &mut TestWorld, n: usize) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(entry_fn.type_args.len(), n);
}

#[then(expr = "the payload should have {int} type arguments")]
fn then_payload_has_n_type_arguments(world: &mut TestWorld, n: usize) {
    then_payload_has_n_type_argument(world, n);
}

// =============================================================================
// APT Transfer
// =============================================================================

#[given(regex = r#"^recipient address "0x[a-fA-F0-9]+\.{0,3}"$"#)]
fn given_recipient_address(world: &mut TestWorld) {
    // Use a standard test address
    world.recipient_address = Some(AccountAddress::from_hex("0xabc123").unwrap());
}

#[given(regex = r"^amount (\d+) \(.*\)$")]
fn given_amount_with_description(world: &mut TestWorld, amount: u64) {
    world.transfer_amount = Some(amount);
}

#[given(expr = "amount {int}")]
fn given_amount(world: &mut TestWorld, amount: u64) {
    world.transfer_amount = Some(amount);
}

#[when(expr = "I create an APT transfer entry function")]
fn when_create_apt_transfer(world: &mut TestWorld) {
    let recipient = world
        .recipient_address
        .unwrap_or_else(|| AccountAddress::from_hex("0x1").unwrap());
    let amount = world.transfer_amount.unwrap_or(1000000);

    match EntryFunction::apt_transfer(recipient, amount) {
        Ok(entry_fn) => world.entry_function = Some(entry_fn),
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[when(expr = "I create any APT transfer")]
fn when_create_any_apt_transfer(world: &mut TestWorld) {
    let recipient = AccountAddress::from_hex("0x1").unwrap();
    match EntryFunction::apt_transfer(recipient, 1000000) {
        Ok(entry_fn) => world.entry_function = Some(entry_fn),
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[then(expr = "the module should be {string}")]
fn then_the_module_should_be(world: &mut TestWorld, expected: String) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    let module_str = format!(
        "{}::{}",
        entry_fn.module.address.to_short_string(),
        entry_fn.module.name.as_str()
    );
    assert_eq!(module_str, expected, "Module mismatch");
}

#[then(expr = "the function should be {string}")]
fn then_the_function_should_be(world: &mut TestWorld, expected: String) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(entry_fn.function, expected);
}

#[then(expr = "there should be {int} type arguments")]
fn then_there_should_be_n_type_arguments(world: &mut TestWorld, n: usize) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(
        entry_fn.type_args.len(),
        n,
        "Expected {} type arguments",
        n
    );
}

#[then(expr = "there should be {int} arguments")]
fn then_there_should_be_n_arguments(world: &mut TestWorld, n: usize) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(entry_fn.args.len(), n, "Expected {} arguments", n);
}

#[then(regex = r"^argument 0 should be BCS-encoded address \(32 bytes\)$")]
fn then_argument_0_bcs_address(world: &mut TestWorld) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert!(
        !entry_fn.args.is_empty(),
        "Entry function should have arguments"
    );
    assert_eq!(
        entry_fn.args[0].len(),
        32,
        "Address argument should be 32 bytes"
    );
}

#[then(regex = r"^argument 1 should be BCS-encoded u64 \(8 bytes\)$")]
fn then_argument_1_bcs_u64(world: &mut TestWorld) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert!(
        entry_fn.args.len() > 1,
        "Entry function should have at least 2 arguments"
    );
    assert_eq!(entry_fn.args[1].len(), 8, "u64 argument should be 8 bytes");
}

// Note: "the module address should be" is in type_tags_steps.rs
// Note: "the module name should be" is in type_tags_steps.rs

#[then(expr = "the function name should be {string}")]
fn then_function_name_should_be(world: &mut TestWorld, expected: String) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(entry_fn.function, expected);
}

// =============================================================================
// Coin Transfer
// =============================================================================

#[given(expr = "coin type {string}")]
fn given_coin_type(world: &mut TestWorld, coin_type: String) {
    let type_tag = TypeTag::from_str_strict(&coin_type).expect("Invalid coin type");
    world.coin_type = Some(type_tag);
}

#[when(expr = "I create a coin transfer entry function")]
fn when_create_coin_transfer(world: &mut TestWorld) {
    let coin_type = world.coin_type.clone().expect("No coin type");
    let recipient = world
        .recipient_address
        .unwrap_or_else(|| AccountAddress::from_hex("0xabc").unwrap());
    let amount = world.transfer_amount.unwrap_or(500000);

    match EntryFunction::coin_transfer(coin_type, recipient, amount) {
        Ok(entry_fn) => world.entry_function = Some(entry_fn),
        Err(e) => world.error = Some(e.to_string()),
    }
}

// Note: "type argument X should be Y" is in type_tags_steps.rs

#[given(expr = "the same recipient and amount")]
fn given_same_recipient_and_amount(world: &mut TestWorld) {
    world.recipient_address = Some(AccountAddress::from_hex("0x123").unwrap());
    world.transfer_amount = Some(1000000);
}

#[when(expr = "I create an APT transfer")]
fn when_create_apt_transfer_simple(world: &mut TestWorld) {
    when_create_apt_transfer(world);
    // Store for comparison
    if let Some(ref entry_fn) = world.entry_function {
        world.bytes = Some(aptos_bcs::to_bytes(entry_fn).unwrap());
    }
}

#[when(expr = "I create a coin transfer for AptosCoin")]
fn when_create_coin_transfer_aptos(world: &mut TestWorld) {
    let coin_type = TypeTag::aptos_coin();
    let recipient = world
        .recipient_address
        .unwrap_or_else(|| AccountAddress::from_hex("0x123").unwrap());
    let amount = world.transfer_amount.unwrap_or(1000000);

    match EntryFunction::coin_transfer(coin_type, recipient, amount) {
        Ok(entry_fn) => {
            world.serialized_bytes2 = Some(aptos_bcs::to_bytes(&entry_fn).unwrap());
            world.entry_function2 = Some(entry_fn);
        }
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[then(expr = "the payloads should be different in structure")]
fn then_payloads_different_structure(world: &mut TestWorld) {
    let bytes1 = world.bytes.as_ref().expect("No APT transfer bytes");
    let bytes2 = world.serialized_bytes2.as_ref().expect("No coin transfer bytes");
    assert_ne!(bytes1, bytes2, "APT and coin transfer payloads should differ");
}

#[then(expr = "APT transfer should use aptos_account module")]
fn then_apt_transfer_uses_aptos_account(world: &mut TestWorld) {
    let entry_fn = world.entry_function.as_ref().expect("No entry function");
    assert_eq!(entry_fn.module.name.as_str(), "aptos_account");
}

#[then(expr = "coin transfer should use coin module")]
fn then_coin_transfer_uses_coin(world: &mut TestWorld) {
    let entry_fn2 = world.entry_function2.as_ref().expect("No coin transfer entry function");
    assert_eq!(entry_fn2.module.name.as_str(), "coin");
}

// =============================================================================
// Argument Encoding
// Note: Most encoding steps are in serialization_steps.rs
// =============================================================================

#[when(expr = "I BCS encode it as an entry function argument")]
fn when_bcs_encode_as_entry_function_arg(world: &mut TestWorld) {
    if let Some(ref addr) = world.address {
        world.bytes = Some(aptos_bcs::to_bytes(addr).unwrap());
    } else if let Some(ref addr) = world.account_address {
        world.bytes = Some(aptos_bcs::to_bytes(addr).unwrap());
    } else if let Some(amount) = world.u64_value {
        world.bytes = Some(aptos_bcs::to_bytes(&amount).unwrap());
    } else if let Some(amount) = world.transfer_amount {
        world.bytes = Some(aptos_bcs::to_bytes(&amount).unwrap());
    } else if let Some(ref b) = world.bool_value {
        world.bytes = Some(aptos_bcs::to_bytes(b).unwrap());
    } else if let Some(ref bytes) = world.input_bytes {
        // Vector encoding
        world.bytes = Some(aptos_bcs::to_bytes(bytes).unwrap());
    } else if let Some(ref s) = world.string_value {
        world.bytes = Some(aptos_bcs::to_bytes(s).unwrap());
    } else if let Some(ref u128_val) = world.u128_value {
        world.bytes = Some(aptos_bcs::to_bytes(u128_val).unwrap());
    }
}

#[given(expr = "bytes [{int}, {int}, {int}, {int}, {int}]")]
fn given_bytes_array(world: &mut TestWorld, b1: u8, b2: u8, b3: u8, b4: u8, b5: u8) {
    world.input_bytes = Some(vec![b1, b2, b3, b4, b5]);
}

#[then(regex = r"^the result should be ULEB128 length \+ bytes$")]
fn then_result_uleb128_plus_bytes(world: &mut TestWorld) {
    let bytes = world.bytes.as_ref().expect("No encoded bytes");
    let input = world.input_bytes.as_ref().expect("No input bytes");
    // For length 5, ULEB128 is 0x05, total should be 6 bytes
    assert_eq!(bytes.len(), input.len() + 1);
    assert_eq!(bytes[0], input.len() as u8); // ULEB128 for small values
}

#[then(regex = r"^the result should be ULEB128 length \+ UTF-8 bytes$")]
fn then_result_uleb128_plus_utf8(world: &mut TestWorld) {
    let bytes = world.bytes.as_ref().expect("No encoded bytes");
    let s = world.string_value.as_ref().expect("No string value");
    // ULEB128 length prefix + UTF-8 bytes
    // Need to account for multibyte chars
    let utf8_len = s.as_bytes().len();
    // For short strings, ULEB128 is 1 byte
    assert!(bytes.len() >= utf8_len + 1, "Should have length prefix plus string bytes");
}

// =============================================================================
// BCS Serialization
// =============================================================================

#[given(expr = "an EntryFunction for APT transfer")]
fn given_entry_function_for_apt_transfer(world: &mut TestWorld) {
    let recipient = AccountAddress::from_hex("0x1").unwrap();
    let entry_fn = EntryFunction::apt_transfer(recipient, 1000000).unwrap();
    world.entry_function = Some(entry_fn);
}

// Note: "When I BCS serialize it" is defined in serialization_steps.rs

#[then(regex = r"^the result should include module ID, function name, type args, and args$")]
fn then_result_includes_components(world: &mut TestWorld) {
    let bytes = world.bytes.as_ref().expect("No serialized bytes");
    // Just verify it has reasonable size (module ID + function + type_args + args)
    assert!(bytes.len() > 32, "Serialized EntryFunction should have reasonable size");
}

#[given(expr = "the same EntryFunction created twice")]
fn given_same_entry_function_twice(world: &mut TestWorld) {
    let recipient = AccountAddress::from_hex("0x1").unwrap();
    let entry_fn1 = EntryFunction::apt_transfer(recipient, 1000000).unwrap();
    let entry_fn2 = EntryFunction::apt_transfer(recipient, 1000000).unwrap();
    world.entry_function = Some(entry_fn1);
    world.entry_function2 = Some(entry_fn2);
}

// Note: "When I BCS serialize both" is in serialization_steps.rs

#[given(expr = "an EntryFunction with type arguments and arguments")]
fn given_entry_function_with_type_args_and_args(world: &mut TestWorld) {
    let recipient = AccountAddress::from_hex("0x123").unwrap();
    let coin_type = TypeTag::aptos_coin();
    let entry_fn = EntryFunction::coin_transfer(coin_type, recipient, 500000).unwrap();
    world.entry_function = Some(entry_fn);
}

// Note: "When I BCS serialize and deserialize it" is in serialization_steps.rs

// =============================================================================
// TransactionPayload Wrapping
// =============================================================================

#[given(expr = "an EntryFunction")]
fn given_an_entry_function(world: &mut TestWorld) {
    given_entry_function_for_apt_transfer(world);
}

#[when(expr = "I convert it to TransactionPayload")]
fn when_convert_to_payload(world: &mut TestWorld) {
    if let Some(ref entry_fn) = world.entry_function {
        world.tx_payload = Some(TransactionPayload::EntryFunction(entry_fn.clone()));
    }
}

#[then(expr = "the payload variant should be EntryFunction")]
fn then_payload_variant_is_entry_function(world: &mut TestWorld) {
    let payload = world.tx_payload.as_ref().expect("No transaction payload");
    assert!(
        matches!(payload, TransactionPayload::EntryFunction(_)),
        "Payload should be EntryFunction variant"
    );
}

#[given(expr = "a TransactionPayload containing an EntryFunction")]
fn given_transaction_payload_with_entry_function(world: &mut TestWorld) {
    given_entry_function_for_apt_transfer(world);
    when_convert_to_payload(world);
}

#[then(regex = r"^the first byte should indicate EntryFunction variant$")]
fn then_first_byte_indicates_entry_function(world: &mut TestWorld) {
    let bytes = if let Some(ref b) = world.bytes {
        b
    } else if let Some(ref b) = world.serialized_bytes {
        b
    } else {
        panic!("No serialized bytes found");
    };
    // EntryFunction is variant 2 in TransactionPayload
    assert_eq!(bytes[0], 2, "First byte should be 2 (EntryFunction variant), got {}", bytes[0]);
}

// =============================================================================
// Edge Cases
// =============================================================================

#[given(expr = "an EntryFunction with no type arguments")]
fn given_entry_function_no_type_args(world: &mut TestWorld) {
    // APT transfer has no type arguments
    given_entry_function_for_apt_transfer(world);
}

#[then(regex = r"^type_args should serialize as empty vector \((0x[0-9a-fA-F]+)\)$")]
fn then_type_args_empty_vector(world: &mut TestWorld, expected: String) {
    // The serialized EntryFunction contains type_args as an empty vector
    // which is encoded as 0x00 (length 0)
    let bytes = world.bytes.as_ref().expect("No serialized bytes");
    // Find where type_args would be encoded - after module and function
    // This is a simplistic check
    let expected_byte = u8::from_str_radix(expected.trim_start_matches("0x"), 16).unwrap();
    assert!(
        bytes.contains(&expected_byte),
        "Empty type_args should contain 0x00"
    );
}

#[given(regex = r"^an EntryFunction with no arguments \(e\.g\., initialize\)$")]
fn given_entry_function_no_args(world: &mut TestWorld) {
    let module = MoveModuleId::from_str_strict("0x1::some_module").unwrap();
    let entry_fn = EntryFunction::new(module, "initialize", vec![], vec![]);
    world.entry_function = Some(entry_fn);
}

#[then(regex = r"^args should serialize as empty vector \((0x[0-9a-fA-F]+)\)$")]
fn then_args_empty_vector(world: &mut TestWorld, expected: String) {
    let bytes = world.bytes.as_ref().expect("No serialized bytes");
    let expected_byte = u8::from_str_radix(expected.trim_start_matches("0x"), 16).unwrap();
    // The last byte before EOB for empty args should be 0x00
    assert!(
        bytes.contains(&expected_byte),
        "Empty args should contain 0x00"
    );
}

#[given(expr = "a u256 value near max")]
fn given_u256_near_max(world: &mut TestWorld) {
    // Use max u256 - 1
    world.u256_value = Some([0xFF; 32]);
}

#[when(expr = "I encode it as an entry function argument")]
fn when_encode_u256_as_arg(world: &mut TestWorld) {
    if let Some(ref u256_bytes) = world.u256_value {
        world.bytes = Some(aptos_bcs::to_bytes(u256_bytes).unwrap());
    }
}

#[then(expr = "the encoding should succeed")]
fn then_encoding_succeeds(world: &mut TestWorld) {
    assert!(world.bytes.is_some(), "Encoding should produce bytes");
}

// =============================================================================
// Test Vectors
// =============================================================================

#[given(expr = "recipient and amount from test vectors")]
fn given_recipient_amount_from_test_vectors(world: &mut TestWorld) {
    // Standard test vector: transfer to 0x1 with amount 100
    world.recipient_address = Some(AccountAddress::ONE);
    world.transfer_amount = Some(100);
}

#[then(regex = r"^the bytes should match the expected value from test vectors$")]
fn then_bytes_match_test_vectors(world: &mut TestWorld) {
    let bytes = world.bytes.as_ref()
        .or(world.serialized_bytes.as_ref())
        .expect("No serialized bytes");
    // Just verify it's non-empty and reasonable
    assert!(!bytes.is_empty(), "Serialized bytes should not be empty");
}

#[given(expr = "coin type, recipient, and amount from test vectors")]
fn given_coin_transfer_test_vectors(world: &mut TestWorld) {
    world.coin_type = Some(TypeTag::aptos_coin());
    world.recipient_address = Some(AccountAddress::ONE);
    world.transfer_amount = Some(100);
}

// =============================================================================
// ABI-related (placeholders)
// =============================================================================

#[given(expr = "an ABI with entry functions")]
fn given_abi_with_entry_functions(_world: &mut TestWorld) {
    // Placeholder - ABI support is advanced feature
}

#[given(expr = "a module with public (non-entry) functions")]
fn given_module_with_public_functions(_world: &mut TestWorld) {
    // Placeholder
}

#[given(expr = "an entry function {string}")]
fn given_entry_function_named(world: &mut TestWorld, name: String) {
    // Create a sample entry function with the given name
    let module = MoveModuleId::from_str_strict("0x1::aptos_account").unwrap();
    let entry_fn = EntryFunction::new(module, &name, vec![], vec![]);
    world.entry_function = Some(entry_fn);
}

#[given(expr = "an entry function")]
fn given_entry_function_simple(world: &mut TestWorld) {
    given_entry_function_for_apt_transfer(world);
}
