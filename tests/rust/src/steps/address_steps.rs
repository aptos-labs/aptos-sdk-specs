//! Step definitions for address feature tests.

use crate::support::TestWorld;
use aptos_sdk::types::AccountAddress;
use cucumber::{given, then, when};

// =============================================================================
// Given Steps
// =============================================================================

#[given(expr = "a hex string {string}")]
fn given_hex_string(world: &mut TestWorld, hex: String) {
    world.hex_string = Some(hex);
}

#[given("the ZERO address constant")]
fn given_zero_constant(world: &mut TestWorld) {
    world.address = Some(AccountAddress::ZERO);
}

#[given("the ONE address constant")]
fn given_one_constant(world: &mut TestWorld) {
    world.address = Some(AccountAddress::ONE);
}

#[given("the THREE address constant")]
fn given_three_constant(world: &mut TestWorld) {
    world.address = Some(AccountAddress::THREE);
}

#[given("the FOUR address constant")]
fn given_four_constant(world: &mut TestWorld) {
    world.address = Some(AccountAddress::FOUR);
}

#[given(expr = "an AccountAddress with value {int}")]
fn given_address_with_value(world: &mut TestWorld, value: u64) {
    let mut bytes = [0u8; 32];
    bytes[24..32].copy_from_slice(&value.to_be_bytes());
    world.address = Some(AccountAddress::new(bytes));
}

#[given(expr = "an AccountAddress from hex {string}")]
fn given_address_from_hex(world: &mut TestWorld, hex: String) {
    match AccountAddress::from_hex(&hex) {
        Ok(addr) => world.address = Some(addr),
        Err(e) => world.set_error(e),
    }
}

#[given(expr = "another AccountAddress from hex {string}")]
fn given_another_address_from_hex(world: &mut TestWorld, hex: String) {
    match AccountAddress::from_hex(&hex) {
        Ok(addr) => world.address2 = Some(addr),
        Err(e) => world.set_error(e),
    }
}

#[given(expr = "{int} bytes with value {int} in the last byte")]
fn given_bytes_with_last_byte(world: &mut TestWorld, size: usize, value: u8) {
    let mut bytes = vec![0u8; size];
    if !bytes.is_empty() {
        *bytes.last_mut().unwrap() = value;
    }
    world.bytes = Some(bytes);
}

// =============================================================================
// When Steps
// =============================================================================

#[when("I parse it as an AccountAddress")]
fn when_parse_address(world: &mut TestWorld) {
    if let Some(ref hex) = world.hex_string {
        match AccountAddress::from_hex(hex) {
            Ok(addr) => {
                world.address = Some(addr);
                world.address_result = Some(Ok(addr));
            }
            Err(e) => {
                world.address_result = Some(Err(e.to_string()));
            }
        }
    }
}

#[when("I format it as full hex")]
fn when_format_full_hex(world: &mut TestWorld) {
    if let Some(addr) = world.address {
        world.formatted_string = Some(addr.to_long_string());
    }
}

#[when("I format it as short string")]
fn when_format_short_string(world: &mut TestWorld) {
    if let Some(addr) = world.address {
        world.formatted_string = Some(addr.to_short_string());
    }
}

#[when("I BCS serialize the address")]
fn when_bcs_serialize_address(world: &mut TestWorld) {
    if let Some(addr) = world.address {
        world.bcs_bytes = Some(addr.to_bytes().to_vec());
    }
}

#[when("I BCS deserialize as AccountAddress")]
fn when_bcs_deserialize_address(world: &mut TestWorld) {
    // Try bytes_value first (from serialization tests)
    if let Some(ref bytes) = world.bytes_value {
        match <[u8; 32]>::try_from(bytes.as_slice()) {
            Ok(arr) => {
                let addr = AccountAddress::new(arr);
                world.address = Some(addr);
                world.account_address = Some(addr);
            }
            Err(e) => world.set_error(e),
        }
        return;
    }

    if let Some(ref bytes) = world.bytes {
        match <[u8; 32]>::try_from(bytes.as_slice()) {
            Ok(arr) => world.address = Some(AccountAddress::new(arr)),
            Err(e) => world.set_error(e),
        }
    } else if let Some(ref bcs_bytes) = world.bcs_bytes {
        match <[u8; 32]>::try_from(bcs_bytes.as_slice()) {
            Ok(arr) => {
                world.address2 = world.address; // Save original
                world.address = Some(AccountAddress::new(arr));
            }
            Err(e) => world.set_error(e),
        }
    }
}

#[when("I BCS deserialize the result as AccountAddress")]
fn when_bcs_deserialize_result(world: &mut TestWorld) {
    when_bcs_deserialize_address(world);
}

// =============================================================================
// Then Steps
// =============================================================================

// "the parsing should succeed" is in common_steps.rs

#[then("the parsing should fail with an invalid address error")]
fn then_parsing_fails_invalid_address(world: &mut TestWorld) {
    assert!(
        world
            .address_result
            .as_ref()
            .map(|r| r.is_err())
            .unwrap_or(false),
        "Expected parsing to fail with invalid address error"
    );
}

#[then("the parsing should fail with an invalid hex error")]
fn then_parsing_fails_invalid_hex(world: &mut TestWorld) {
    assert!(
        world
            .address_result
            .as_ref()
            .map(|r| r.is_err())
            .unwrap_or(false),
        "Expected parsing to fail with invalid hex error"
    );
}

#[then("the parsing should fail with an invalid length error")]
fn then_parsing_fails_invalid_length(world: &mut TestWorld) {
    assert!(
        world
            .address_result
            .as_ref()
            .map(|r| r.is_err())
            .unwrap_or(false),
        "Expected parsing to fail with invalid length error"
    );
}

#[then(expr = "the address bytes should have length {int}")]
fn then_address_bytes_length(world: &mut TestWorld, length: usize) {
    if let Some(addr) = world.address {
        assert_eq!(addr.to_bytes().len(), length);
    }
}

#[then(expr = "byte {int} should equal {int}")]
fn then_byte_equals(world: &mut TestWorld, index: usize, value: u8) {
    if let Some(addr) = world.address {
        let bytes = addr.to_bytes();
        assert_eq!(
            bytes[index], value,
            "byte {} should be {} but was {}",
            index, value, bytes[index]
        );
    } else if let Some(ref bytes) = world.bcs_bytes {
        assert_eq!(
            bytes[index], value,
            "byte {} should be {} but was {}",
            index, value, bytes[index]
        );
    }
}

#[then(expr = "bytes {int}-{int} should all be {int}")]
fn then_bytes_range_all_equal(world: &mut TestWorld, start: usize, end: usize, value: u8) {
    if let Some(addr) = world.address {
        let bytes = addr.to_bytes();
        for i in start..=end {
            assert_eq!(
                bytes[i], value,
                "byte {} should be {} but was {}",
                i, value, bytes[i]
            );
        }
    } else if let Some(ref bytes) = world.bcs_bytes {
        for i in start..=end {
            assert_eq!(
                bytes[i], value,
                "byte {} should be {} but was {}",
                i, value, bytes[i]
            );
        }
    }
}

#[then(expr = "all {int} bytes should be {int}")]
fn then_all_bytes_equal(world: &mut TestWorld, count: usize, value: u8) {
    if let Some(addr) = world.address {
        let bytes = addr.to_bytes();
        assert_eq!(bytes.len(), count);
        for (i, &b) in bytes.iter().enumerate() {
            assert_eq!(b, value, "byte {} should be {} but was {}", i, value, b);
        }
    }
}

#[then(expr = "the short string should be {string}")]
fn then_short_string_is(world: &mut TestWorld, expected: String) {
    // Check both address fields
    if let Some(addr) = world.address {
        assert_eq!(addr.to_short_string(), expected);
    } else if let Some(addr) = world.account_address {
        assert_eq!(addr.to_short_string(), expected);
    } else {
        panic!("No address set");
    }
}

#[then(expr = "the full hex should be {string}")]
fn then_full_hex_is(world: &mut TestWorld, expected: String) {
    if let Some(addr) = world.address {
        assert_eq!(addr.to_long_string(), expected);
    }
}

// "the result should be {string}" is in common_steps.rs
// "the result should be {int} bytes" is in common_steps.rs

#[then("the two addresses should be equal")]
fn then_addresses_equal(world: &mut TestWorld) {
    assert_eq!(world.address, world.address2);
}

#[then("the two addresses should not be equal")]
fn then_addresses_not_equal(world: &mut TestWorld) {
    assert_ne!(world.address, world.address2);
}

#[then("the result should equal the original address")]
fn then_result_equals_original(world: &mut TestWorld) {
    assert!(world.address.is_some() && world.address2.is_some());
    assert_eq!(world.address, world.address2);
}
