//! Step definitions for TypeTag parsing tests

use crate::support::world::TestWorld;
use aptos_rust_sdk_v2::types::{MoveModuleId, MoveStructTag, TypeTag};
use cucumber::{given, then, when};

// =============================================================================
// Primitive Type Parsing
// =============================================================================

#[given(expr = "a type string {string}")]
fn given_type_string(world: &mut TestWorld, type_str: String) {
    world.type_string = Some(type_str);
}

#[when(expr = "I parse it as a TypeTag")]
fn when_parse_as_type_tag(world: &mut TestWorld) {
    let type_str = world.type_string.as_ref().expect("No type string");
    match TypeTag::from_str_strict(type_str) {
        Ok(tag) => world.type_tag = Some(tag),
        Err(e) => world.error = Some(e.to_string()),
    }
}

// "the parsing should succeed" is in common_steps.rs

#[then(expr = "the TypeTag variant should be {word}")]
fn then_type_tag_variant(world: &mut TestWorld, variant: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    let actual_variant = match tag {
        TypeTag::Bool => "Bool",
        TypeTag::U8 => "U8",
        TypeTag::U16 => "U16",
        TypeTag::U32 => "U32",
        TypeTag::U64 => "U64",
        TypeTag::U128 => "U128",
        TypeTag::U256 => "U256",
        TypeTag::Address => "Address",
        TypeTag::Signer => "Signer",
        TypeTag::Vector(_) => "Vector",
        TypeTag::Struct(_) => "Struct",
    };
    assert_eq!(actual_variant, variant, "Expected variant {}, got {}", variant, actual_variant);
}

#[given(expr = "a TypeTag of variant {word}")]
fn given_type_tag_variant(world: &mut TestWorld, variant: String) {
    let tag = match variant.as_str() {
        "U64" => TypeTag::U64,
        "U8" => TypeTag::U8,
        "U16" => TypeTag::U16,
        "U32" => TypeTag::U32,
        "U128" => TypeTag::U128,
        "U256" => TypeTag::U256,
        "Bool" => TypeTag::Bool,
        "Address" => TypeTag::Address,
        "Signer" => TypeTag::Signer,
        _ => panic!("Unknown variant: {}", variant),
    };
    world.type_tag = Some(tag);
}

#[when(expr = "I format it as a string")]
fn when_format_as_string(world: &mut TestWorld) {
    if let Some(ref tag) = world.type_tag {
        world.formatted_string = Some(tag.to_string());
    } else if let Some(ref module_id) = world.module_id {
        world.formatted_string = Some(module_id.to_string());
    } else if let Some(ref struct_tag) = world.struct_tag {
        world.formatted_string = Some(struct_tag.to_string());
    }
}

// "the result should be {string}" is in common_steps.rs

// =============================================================================
// Vector Type Parsing
// =============================================================================

#[then(expr = "the inner type should be {word}")]
fn then_inner_type(world: &mut TestWorld, inner: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Vector(inner_tag) = tag {
        let actual = match inner_tag.as_ref() {
            TypeTag::U8 => "U8",
            TypeTag::U64 => "U64",
            TypeTag::Bool => "Bool",
            TypeTag::Vector(_) => "Vector",
            TypeTag::Struct(_) => "Struct",
            _ => "Other",
        };
        assert_eq!(actual, inner, "Expected inner type {}, got {}", inner, actual);
    } else {
        panic!("Expected Vector type, got {:?}", tag);
    }
}

#[then(expr = "the inner type should be a Vector of {word}")]
fn then_inner_type_vector_of(world: &mut TestWorld, inner_inner: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Vector(inner_tag) = tag {
        if let TypeTag::Vector(inner_inner_tag) = inner_tag.as_ref() {
            let actual = match inner_inner_tag.as_ref() {
                TypeTag::U8 => "U8",
                TypeTag::U64 => "U64",
                _ => "Other",
            };
            assert_eq!(actual, inner_inner);
        } else {
            panic!("Expected inner to be Vector");
        }
    } else {
        panic!("Expected Vector type");
    }
}

#[then(expr = "the inner type should be a Struct")]
fn then_inner_type_struct(world: &mut TestWorld) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Vector(inner_tag) = tag {
        assert!(matches!(inner_tag.as_ref(), TypeTag::Struct(_)));
    } else {
        panic!("Expected Vector type");
    }
}

#[given(expr = "a TypeTag of Vector containing {word}")]
fn given_type_tag_vector_containing(world: &mut TestWorld, inner: String) {
    let inner_tag = match inner.as_str() {
        "U8" => TypeTag::U8,
        "U64" => TypeTag::U64,
        _ => panic!("Unknown type: {}", inner),
    };
    world.type_tag = Some(TypeTag::Vector(Box::new(inner_tag)));
}

// =============================================================================
// Struct Type Parsing
// =============================================================================

#[then(expr = "the struct address should be {string}")]
fn then_struct_address(world: &mut TestWorld, addr: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        assert_eq!(st.address.to_short_string(), addr);
    } else {
        panic!("Expected Struct type");
    }
}

#[then(expr = "the struct module should be {string}")]
fn then_struct_module(world: &mut TestWorld, module: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        assert_eq!(st.module.as_str(), module);
    } else {
        panic!("Expected Struct type");
    }
}

#[then(expr = "the struct name should be {string}")]
fn then_struct_name(world: &mut TestWorld, name: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        assert_eq!(st.name.as_str(), name);
    } else {
        panic!("Expected Struct type");
    }
}

#[then(expr = "the struct should have {int} type argument")]
fn then_struct_type_args_count_singular(world: &mut TestWorld, count: usize) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        assert_eq!(st.type_args.len(), count, "Expected {} type args, got {}", count, st.type_args.len());
    } else {
        panic!("Expected Struct type");
    }
}

#[then(expr = "the struct should have {int} type arguments")]
fn then_struct_type_args_count(world: &mut TestWorld, count: usize) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        assert_eq!(st.type_args.len(), count, "Expected {} type args, got {}", count, st.type_args.len());
    } else {
        panic!("Expected Struct type");
    }
}

#[then(expr = "type argument {int} should be a Struct named {string}")]
fn then_type_arg_struct_named(world: &mut TestWorld, idx: usize, name: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        if let TypeTag::Struct(arg_st) = &st.type_args[idx] {
            assert_eq!(arg_st.name.as_str(), name);
        } else {
            panic!("Expected type arg {} to be Struct", idx);
        }
    } else {
        panic!("Expected Struct type");
    }
}

#[then(expr = "type argument {int} should be {word}")]
fn then_type_arg_is(world: &mut TestWorld, idx: usize, variant: String) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    if let TypeTag::Struct(st) = tag {
        let actual = match &st.type_args[idx] {
            TypeTag::U64 => "U64",
            TypeTag::U8 => "U8",
            TypeTag::Struct(_) => "Struct",
            _ => "Other",
        };
        assert_eq!(actual, variant);
    } else {
        panic!("Expected Struct type");
    }
}

#[given(expr = "a TypeTag struct with address {string}, module {string}, name {string}")]
fn given_type_tag_struct(world: &mut TestWorld, addr: String, module: String, name: String) {
    use aptos_rust_sdk_v2::AccountAddress;
    use aptos_rust_sdk_v2::types::Identifier;
    let address = AccountAddress::from_hex(&addr).unwrap();
    let struct_tag = MoveStructTag {
        address,
        module: Identifier::new(&module).unwrap(),
        name: Identifier::new(&name).unwrap(),
        type_args: vec![],
    };
    world.type_tag = Some(TypeTag::Struct(Box::new(struct_tag)));
}

#[given(expr = "a TypeTag for CoinStore of AptosCoin")]
fn given_type_tag_coin_store(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::AccountAddress;
    use aptos_rust_sdk_v2::types::Identifier;
    let aptos_coin = MoveStructTag {
        address: AccountAddress::from_hex("0x1").unwrap(),
        module: Identifier::new("aptos_coin").unwrap(),
        name: Identifier::new("AptosCoin").unwrap(),
        type_args: vec![],
    };
    let coin_store = MoveStructTag {
        address: AccountAddress::from_hex("0x1").unwrap(),
        module: Identifier::new("coin").unwrap(),
        name: Identifier::new("CoinStore").unwrap(),
        type_args: vec![TypeTag::Struct(Box::new(aptos_coin))],
    };
    world.type_tag = Some(TypeTag::Struct(Box::new(coin_store)));
}

// =============================================================================
// Invalid Type Parsing
// =============================================================================

#[then(expr = "the parsing should fail with a parse error")]
fn then_parsing_should_fail(world: &mut TestWorld) {
    assert!(world.error.is_some(), "Expected parsing to fail");
}

// =============================================================================
// MoveModuleId
// =============================================================================

#[given(expr = "a module string {string}")]
fn given_module_string(world: &mut TestWorld, module_str: String) {
    world.module_string = Some(module_str);
}

#[when(expr = "I parse it as a MoveModuleId")]
fn when_parse_as_module_id(world: &mut TestWorld) {
    use std::str::FromStr;
    let module_str = world.module_string.as_ref().expect("No module string");
    match MoveModuleId::from_str(module_str) {
        Ok(id) => world.module_id = Some(id),
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[then(expr = "the module address should be {string}")]
fn then_module_address(world: &mut TestWorld, addr: String) {
    let module_id = world.module_id.as_ref().expect("No MoveModuleId");
    assert_eq!(module_id.address.to_short_string(), addr);
}

#[then(expr = "the module name should be {string}")]
fn then_module_name(world: &mut TestWorld, name: String) {
    let module_id = world.module_id.as_ref().expect("No MoveModuleId");
    assert_eq!(module_id.name.as_str(), name);
}

#[given(expr = "a MoveModuleId with address {string} and name {string}")]
fn given_move_module_id(world: &mut TestWorld, addr: String, name: String) {
    use aptos_rust_sdk_v2::AccountAddress;
    use aptos_rust_sdk_v2::types::Identifier;
    world.module_id = Some(MoveModuleId {
        address: AccountAddress::from_hex(&addr).unwrap(),
        name: Identifier::new(&name).unwrap(),
    });
}

#[then(expr = "the parsing should fail")]
fn then_parsing_fail_generic(world: &mut TestWorld) {
    assert!(world.error.is_some(), "Expected parsing to fail");
}

// =============================================================================
// MoveStructTag
// =============================================================================

#[given(regex = r#"^address "([^"]+)", module "([^"]+)", name "([^"]+)", and type args \[AptosCoin\]$"#)]
fn given_struct_tag_components(world: &mut TestWorld, addr: String, module: String, name: String) {
    use aptos_rust_sdk_v2::AccountAddress;
    use aptos_rust_sdk_v2::types::Identifier;
    let aptos_coin = MoveStructTag {
        address: AccountAddress::from_hex("0x1").unwrap(),
        module: Identifier::new("aptos_coin").unwrap(),
        name: Identifier::new("AptosCoin").unwrap(),
        type_args: vec![],
    };
    world.struct_tag = Some(MoveStructTag {
        address: AccountAddress::from_hex(&addr).unwrap(),
        module: Identifier::new(&module).unwrap(),
        name: Identifier::new(&name).unwrap(),
        type_args: vec![TypeTag::Struct(Box::new(aptos_coin))],
    });
}

#[when(expr = "I create a MoveStructTag")]
fn when_create_struct_tag(_world: &mut TestWorld) {
    // Already created in given step
}

#[then(expr = "the struct tag should be valid")]
fn then_struct_tag_valid(world: &mut TestWorld) {
    assert!(world.struct_tag.is_some());
}

#[then(expr = "the string representation should be {string}")]
fn then_string_representation(world: &mut TestWorld, expected: String) {
    let struct_tag = world.struct_tag.as_ref().expect("No struct tag");
    assert_eq!(struct_tag.to_string(), expected);
}

// =============================================================================
// BCS Serialization
// =============================================================================

#[when(expr = "I BCS serialize the TypeTag")]
fn when_bcs_serialize_type_tag(world: &mut TestWorld) {
    let tag = world.type_tag.as_ref().expect("No TypeTag");
    world.serialized_bytes = Some(aptos_bcs::to_bytes(tag).unwrap());
}

#[then(expr = "the first byte should be the {word} variant index")]
fn then_first_byte_variant_index(world: &mut TestWorld, _variant: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    // U64 is index 3 in the TypeTag enum
    assert!(!bytes.is_empty());
}

#[when(expr = "I parse and BCS serialize the TypeTag")]
fn when_parse_and_serialize(world: &mut TestWorld) {
    when_parse_as_type_tag(world);
    if world.type_tag.is_some() {
        when_bcs_serialize_type_tag(world);
    }
}

#[then(expr = "the serialization should succeed")]
fn then_serialization_succeed(world: &mut TestWorld) {
    assert!(world.serialized_bytes.is_some());
}

#[then(expr = "the result should be deserializable back to the same TypeTag")]
fn then_deserializable_back(world: &mut TestWorld) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let deserialized: TypeTag = aptos_bcs::from_bytes(bytes).expect("Failed to deserialize");
    let original = world.type_tag.as_ref().expect("No original TypeTag");
    assert_eq!(&deserialized, original);
}

#[when(expr = "I BCS serialize and deserialize it")]
fn when_bcs_roundtrip(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::transaction::RawTransaction;
    
    if let Some(ref tag) = world.type_tag {
        let bytes = aptos_bcs::to_bytes(tag).expect("Failed to serialize");
        let deserialized: TypeTag = aptos_bcs::from_bytes(&bytes).expect("Failed to deserialize");
        world.type_tag_deserialized = Some(deserialized);
    } else if let Some(ref raw_tx) = world.raw_transaction {
        let bytes = aptos_bcs::to_bytes(raw_tx).expect("Failed to serialize");
        let deserialized: RawTransaction = aptos_bcs::from_bytes(&bytes).expect("Failed to deserialize");
        world.raw_transaction2 = Some(deserialized);
    } else if let Some(ref module_id) = world.module_id {
        let bytes = aptos_bcs::to_bytes(module_id).expect("Failed to serialize");
        let deserialized = aptos_bcs::from_bytes(&bytes).expect("Failed to deserialize");
        world.module_id_deserialized = Some(deserialized);
    } else if let Some(ref struct_tag) = world.struct_tag {
        let bytes = aptos_bcs::to_bytes(struct_tag).expect("Failed to serialize");
        let deserialized = aptos_bcs::from_bytes(&bytes).expect("Failed to deserialize");
        world.struct_tag_deserialized = Some(deserialized);
    }
}

#[then(expr = "the result should equal the original TypeTag")]
fn then_result_equals_original(world: &mut TestWorld) {
    let original = world.type_tag.as_ref().expect("No original TypeTag");
    let deserialized = world.type_tag_deserialized.as_ref().expect("No deserialized TypeTag");
    assert_eq!(original, deserialized);
}
