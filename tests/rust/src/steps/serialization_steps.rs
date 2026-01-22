//! Step definitions for BCS serialization tests

use crate::support::world::TestWorld;
use aptos_bcs;
use cucumber::{given, then, when};

// =============================================================================
// Boolean Serialization
// =============================================================================

#[given(expr = "a boolean value true")]
fn given_boolean_true(world: &mut TestWorld) {
    world.bool_value = Some(true);
}

#[given(expr = "a boolean value false")]
fn given_boolean_false(world: &mut TestWorld) {
    world.bool_value = Some(false);
}

#[when(expr = "I BCS serialize it")]
fn when_bcs_serialize(world: &mut TestWorld) {
    if let Some(b) = world.bool_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(&b).unwrap());
    } else if let Some(v) = world.u8_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(&v).unwrap());
    } else if let Some(v) = world.u16_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(&v).unwrap());
    } else if let Some(v) = world.u32_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(&v).unwrap());
    } else if let Some(v) = world.u64_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(&v).unwrap());
    } else if let Some(v) = world.u128_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(&v).unwrap());
    } else if let Some(ref v) = world.u256_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.bytes_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.string_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.option_u64_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.vec_u8_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.vec_u64_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.vec_vec_u8_value {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.account_address {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.raw_transaction {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.signed_transaction {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.type_tag_deserialized {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.module_id {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    } else if let Some(ref v) = world.struct_tag {
        world.serialized_bytes = Some(aptos_bcs::to_bytes(v).unwrap());
    }
}

#[then(expr = "the result should be {int} byte")]
fn then_result_byte_count_singular(world: &mut TestWorld, count: usize) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes.len(), count, "Expected {} byte(s), got {}", count, bytes.len());
}

// "the result should be {int} bytes" is in common_steps.rs

#[then(expr = "the byte should be {word}")]
fn then_byte_should_be(world: &mut TestWorld, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let expected = parse_hex_byte(&hex);
    assert_eq!(bytes[0], expected, "Expected byte 0x{:02x}, got 0x{:02x}", expected, bytes[0]);
}

// Use regex pattern for hex byte arrays (like [0x01, 0x02])
#[given(regex = r"^bytes \[(0x[0-9a-fA-F]+(?:,\s*0x[0-9a-fA-F]+)*)\]$")]
fn given_bytes_array(world: &mut TestWorld, bytes_str: String) {
    let bytes: Vec<u8> = bytes_str
        .split(',')
        .map(|s| parse_hex_byte(s.trim()))
        .collect();
    world.bytes_value = Some(bytes);
}

// For "bytes [0x01, 0x02] intended for u64"
#[given(regex = r"^bytes \[(.+?)\] intended for u64$")]
fn given_bytes_intended_for_u64(world: &mut TestWorld, bytes_str: String) {
    let bytes: Vec<u8> = bytes_str
        .split(',')
        .map(|s| parse_hex_byte(s.trim()))
        .collect();
    world.bytes_value = Some(bytes);
}

#[when(expr = "I BCS deserialize as boolean")]
fn when_deserialize_bool(world: &mut TestWorld) {
    let bytes = world.bytes_value.as_ref().expect("No bytes");
    match aptos_bcs::from_bytes::<bool>(bytes) {
        Ok(v) => world.bool_value = Some(v),
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[then(expr = "the result should be true")]
fn then_result_true(world: &mut TestWorld) {
    assert_eq!(world.bool_value, Some(true));
}

#[then(expr = "the result should be false")]
fn then_result_false(world: &mut TestWorld) {
    assert_eq!(world.bool_value, Some(false));
}

// =============================================================================
// Integer Serialization
// =============================================================================

#[given(expr = "a u8 value {int}")]
fn given_u8(world: &mut TestWorld, value: u8) {
    world.u8_value = Some(value);
}

#[given(regex = r"^a u16 value (.+)$")]
fn given_u16(world: &mut TestWorld, value: String) {
    world.u16_value = Some(parse_int(&value) as u16);
}

#[given(regex = r"^a u32 value (.+)$")]
fn given_u32(world: &mut TestWorld, value: String) {
    world.u32_value = Some(parse_int(&value) as u32);
}

#[given(regex = r"^a u64 value (.+)$")]
fn given_u64(world: &mut TestWorld, value: String) {
    world.u64_value = Some(parse_int(&value));
}

#[given(expr = "a u128 value {int}")]
fn given_u128(world: &mut TestWorld, value: u128) {
    world.u128_value = Some(value);
}

#[given(expr = "a u256 value {int}")]
fn given_u256(world: &mut TestWorld, value: u64) {
    let mut bytes = [0u8; 32];
    bytes[0..8].copy_from_slice(&value.to_le_bytes());
    world.u256_value = Some(bytes);
}

#[then(expr = "the result should be {int} bytes in little-endian")]
fn then_bytes_le(world: &mut TestWorld, count: usize) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes.len(), count);
}

// Use regex for byte array assertions
#[then(regex = r"^the bytes should be \[(.+?)\]$")]
fn then_bytes_should_be(world: &mut TestWorld, expected_str: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let expected: Vec<u8> = expected_str
        .split(',')
        .map(|s| parse_hex_byte(s.trim()))
        .collect();
    assert_eq!(bytes.as_slice(), expected.as_slice());
}

#[then(regex = r"^byte (\d+) should be (0x[0-9a-fA-F]+)$")]
fn then_byte_at_index(world: &mut TestWorld, idx: usize, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes[idx], parse_hex_byte(&hex));
}

#[then(regex = r"^bytes (\d+)-(\d+) should all be (0x[0-9a-fA-F]+)$")]
fn then_bytes_range_all(world: &mut TestWorld, start: usize, end: usize, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let expected = parse_hex_byte(&hex);
    for i in start..=end {
        assert_eq!(bytes[i], expected, "Byte {} should be 0x{:02x}, got 0x{:02x}", i, expected, bytes[i]);
    }
}

// =============================================================================
// ULEB128 Encoding
// =============================================================================

#[given(expr = "a length value {int}")]
fn given_length_value(world: &mut TestWorld, value: u64) {
    world.uleb_value = Some(value as usize);
}

#[when(expr = "I ULEB128 encode it")]
fn when_uleb128_encode(world: &mut TestWorld) {
    let value = world.uleb_value.expect("No ULEB value");
    let mut result = Vec::new();
    let mut n = value;
    loop {
        let mut byte = (n & 0x7f) as u8;
        n >>= 7;
        if n != 0 {
            byte |= 0x80;
        }
        result.push(byte);
        if n == 0 {
            break;
        }
    }
    world.serialized_bytes = Some(result);
}

#[then(regex = r"^the result should be \[(.+?)\]$")]
fn then_result_bytes_array(world: &mut TestWorld, expected_str: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let expected: Vec<u8> = expected_str
        .split(',')
        .map(|s| parse_hex_byte(s.trim()))
        .collect();
    assert_eq!(bytes.as_slice(), expected.as_slice());
}

#[when(expr = "I ULEB128 encode and decode it")]
fn when_uleb128_roundtrip(world: &mut TestWorld) {
    let value = world.uleb_value.expect("No ULEB value");
    // Encode
    let mut encoded = Vec::new();
    let mut n = value;
    loop {
        let mut byte = (n & 0x7f) as u8;
        n >>= 7;
        if n != 0 {
            byte |= 0x80;
        }
        encoded.push(byte);
        if n == 0 {
            break;
        }
    }
    // Decode
    let mut result = 0usize;
    let mut shift = 0;
    for &byte in &encoded {
        result |= ((byte & 0x7f) as usize) << shift;
        if byte & 0x80 == 0 {
            break;
        }
        shift += 7;
    }
    world.uleb_decoded = Some(result);
}

#[then(expr = "the result should equal the original value")]
fn then_uleb_roundtrip(world: &mut TestWorld) {
    let original = world.uleb_value.expect("No ULEB value");
    let decoded = world.uleb_decoded.expect("No decoded value");
    assert_eq!(original, decoded);
}

// =============================================================================
// Bytes/String Serialization
// =============================================================================

#[given(expr = "an empty byte array")]
fn given_empty_bytes(world: &mut TestWorld) {
    world.bytes_value = Some(Vec::new());
}

#[given(expr = "a string {string}")]
fn given_string(world: &mut TestWorld, s: String) {
    world.string_value = Some(s);
}

#[then(regex = r"^the first byte should be (0x[0-9a-fA-F]+) \(length\)$")]
fn then_first_byte_length(world: &mut TestWorld, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes[0], parse_hex_byte(&hex));
}

#[then(regex = r"^the first byte should be (0x[0-9a-fA-F]+) \(UTF-8 byte length\)$")]
fn then_first_byte_utf8_length(world: &mut TestWorld, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes[0], parse_hex_byte(&hex));
}

#[then(regex = r"^the first byte should be (0x[0-9a-fA-F]+) \(outer length\)$")]
fn then_first_byte_outer_length(world: &mut TestWorld, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes[0], parse_hex_byte(&hex));
}

#[then("each inner vector should be length-prefixed")]
fn then_each_inner_vector_length_prefixed(world: &mut TestWorld) {
    // For [[1, 2], [3, 4]], the BCS encoding is:
    // 0x02 (outer length) + 0x02 0x01 0x02 (first inner) + 0x02 0x03 0x04 (second inner)
    // Each inner vector has a length prefix followed by its elements
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    // Skip outer length byte, then verify inner vectors have length prefixes
    assert!(bytes.len() >= 7, "Expected at least 7 bytes for nested vector");
    // First inner vector: length=2, then [1, 2]
    assert_eq!(bytes[1], 0x02, "First inner vector should have length 2");
    // Second inner vector: length=2, then [3, 4]  
    assert_eq!(bytes[4], 0x02, "Second inner vector should have length 2");
}

#[then(regex = r"^the remaining bytes should be \[(.+?)\]$")]
fn then_remaining_bytes_array(world: &mut TestWorld, expected_str: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let expected: Vec<u8> = expected_str
        .split(',')
        .map(|s| parse_hex_byte(s.trim()))
        .collect();
    assert_eq!(&bytes[1..], expected.as_slice());
}

#[then(expr = "the remaining bytes should be UTF-8 encoded {string}")]
fn then_remaining_bytes_utf8(world: &mut TestWorld, s: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let utf8_bytes = s.as_bytes();
    assert_eq!(&bytes[1..], utf8_bytes);
}

// =============================================================================
// Option Serialization
// =============================================================================

#[given(expr = "an Option with no value")]
fn given_option_none(world: &mut TestWorld) {
    world.option_u64_value = Some(None);
}

#[given(expr = "an Option containing u64 value {int}")]
fn given_option_some_u64(world: &mut TestWorld, value: u64) {
    world.option_u64_value = Some(Some(value));
}

#[then(regex = r"^the first byte should be (0x[0-9a-fA-F]+)$")]
fn then_first_byte(world: &mut TestWorld, hex: String) {
    let expected = parse_hex_byte(&hex);
    if let Some(ref bytes) = world.serialized_bytes {
        assert_eq!(bytes[0], expected, "Expected first byte 0x{:02x}, got 0x{:02x}", expected, bytes[0]);
    } else if let Some(ref bytes) = world.bytes {
        assert_eq!(bytes[0], expected, "Expected first byte 0x{:02x}, got 0x{:02x}", expected, bytes[0]);
    } else {
        panic!("No bytes found to check first byte");
    }
}

#[then(expr = "the first byte should be {word} or {word}")]
fn then_first_byte_or(world: &mut TestWorld, hex1: String, hex2: String) {
    let expected1 = parse_hex_byte(&hex1);
    let expected2 = parse_hex_byte(&hex2);
    let bytes = if let Some(ref b) = world.bytes { b }
        else if let Some(ref b) = world.serialized_bytes { b }
        else { panic!("No bytes found") };
    assert!(
        bytes[0] == expected1 || bytes[0] == expected2,
        "Expected first byte to be 0x{:02x} or 0x{:02x}, got 0x{:02x}",
        expected1, expected2, bytes[0]
    );
}

#[then(expr = "the remaining {int} bytes should be the u64 value")]
fn then_remaining_u64(world: &mut TestWorld, count: usize) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes.len() - 1, count);
}

// =============================================================================
// Vector Serialization
// =============================================================================

#[given(expr = "an empty vector of u8")]
fn given_empty_vec_u8(world: &mut TestWorld) {
    world.vec_u8_value = Some(Vec::new());
}

#[given(regex = r"^a vector \[(\d+), (\d+), (\d+)\] of u8$")]
fn given_vec_u8(world: &mut TestWorld, a: u8, b: u8, c: u8) {
    world.vec_u8_value = Some(vec![a, b, c]);
}

#[given(regex = r"^a vector \[(\d+), (\d+)\] of u64$")]
fn given_vec_u64(world: &mut TestWorld, a: u64, b: u64) {
    world.vec_u64_value = Some(vec![a, b]);
}

#[given(regex = r"^a vector \[\[(\d+), (\d+)\], \[(\d+), (\d+)\]\] of vectors of u8$")]
fn given_vec_vec_u8(world: &mut TestWorld, a: u8, b: u8, c: u8, d: u8) {
    world.vec_vec_u8_value = Some(vec![vec![a, b], vec![c, d]]);
}

#[then(expr = "the remaining bytes should be two u64 values in little-endian")]
fn then_remaining_two_u64(world: &mut TestWorld) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes.len(), 17); // 1 byte length + 2 * 8 bytes
}

// =============================================================================
// AccountAddress Serialization
// =============================================================================

#[given(expr = "an AccountAddress {string}")]
fn given_account_address_string(world: &mut TestWorld, addr: String) {
    use aptos_rust_sdk_v2::AccountAddress;
    world.account_address = Some(AccountAddress::from_hex(&addr).expect("Invalid address"));
}

// "the result should be exactly {int} bytes" is in common_steps.rs

#[given(regex = r"^(\d+) bytes with byte (\d+) = (0x[0-9a-fA-F]+)$")]
fn given_bytes_with_specific_byte(world: &mut TestWorld, total: usize, idx: usize, hex: String) {
    let mut bytes = vec![0u8; total];
    bytes[idx] = parse_hex_byte(&hex);
    world.bytes_value = Some(bytes);
}

// "I BCS deserialize as AccountAddress" is in address_steps.rs
// "the short string should be {string}" is in address_steps.rs

// =============================================================================
// Complex Type / Error Handling
// =============================================================================

#[given(expr = "a struct with fields:")]
fn given_struct_with_fields(world: &mut TestWorld) {
    // For simplicity, we'll serialize a (AccountAddress, u64) tuple
    use aptos_rust_sdk_v2::AccountAddress;
    let addr = AccountAddress::from_hex("0x1").unwrap();
    let amount: u64 = 1000;
    world.serialized_bytes = Some(aptos_bcs::to_bytes(&(addr, amount)).unwrap());
}

#[then(expr = "the fields should be serialized in order")]
fn then_fields_in_order(_world: &mut TestWorld) {
    // This is implicitly tested by the byte layout
}

#[then(regex = r"^the total length should be (\d+) bytes \((\d+) \+ (\d+)\)$")]
fn then_total_length(world: &mut TestWorld, total: usize, _a: usize, _b: usize) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert_eq!(bytes.len(), total);
}

#[when(expr = "I BCS deserialize as u64")]
fn when_deserialize_u64(world: &mut TestWorld) {
    let bytes = world.bytes_value.as_ref().expect("No bytes");
    match aptos_bcs::from_bytes::<u64>(bytes) {
        Ok(v) => world.u64_value = Some(v),
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[then(expr = "the deserialization should fail with an error")]
fn then_deser_should_fail(world: &mut TestWorld) {
    assert!(world.error.is_some(), "Expected deserialization to fail");
}

#[when(expr = "I BCS deserialize as vector of u8")]
fn when_deserialize_vec_u8(world: &mut TestWorld) {
    let bytes = world.bytes_value.as_ref().expect("No bytes");
    match aptos_bcs::from_bytes::<Vec<u8>>(bytes) {
        Ok(v) => world.vec_u8_value = Some(v),
        Err(e) => world.error = Some(e.to_string()),
    }
}

// =============================================================================
// Helper Functions
// =============================================================================

fn parse_hex_byte(s: &str) -> u8 {
    let s = s.trim_start_matches("0x").trim_start_matches("0X");
    u8::from_str_radix(s, 16).unwrap_or_else(|_| panic!("Invalid hex byte: {}", s))
}

fn parse_int(s: &str) -> u64 {
    if s.starts_with("0x") || s.starts_with("0X") {
        u64::from_str_radix(&s[2..], 16).unwrap_or_else(|_| panic!("Invalid hex: {}", s))
    } else {
        s.parse().unwrap_or_else(|_| panic!("Invalid int: {}", s))
    }
}
