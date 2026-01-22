//! Common step definitions shared across features

use crate::support::world::TestWorld;
use cucumber::then;

/// Generic "the parsing should succeed" that works for addresses, type tags, module IDs, hash values, and mnemonics
#[then("the parsing should succeed")]
fn then_parsing_should_succeed(world: &mut TestWorld) {
    // Check if this is an address parsing test
    if let Some(ref result) = world.address_result {
        assert!(
            result.is_ok(),
            "Address parsing should succeed but got error: {:?}",
            result
        );
        return;
    }
    
    // Check if this is a type tag parsing test
    if world.type_tag.is_some() {
        return;
    }
    
    // Check if this is a module ID parsing test
    if world.module_id.is_some() {
        return;
    }
    
    // Check if this is a hash value parsing test
    if world.hash_value.is_some() {
        return;
    }
    
    // Check if this is a mnemonic parsing test
    if world.named_values.contains_key("mnemonic_parsed") {
        return;
    }
    
    // If we have an error, the parsing failed
    if world.error.is_some() || world.last_error.is_some() {
        panic!("Parsing should succeed but got error: {:?} / {:?}", world.error, world.last_error);
    }
    
    panic!("No parsing result found");
}

/// Generic "the result should be {string}" for formatted output
#[then(expr = "the result should be {string}")]
fn then_result_should_be(world: &mut TestWorld, expected: String) {
    // Check formatted string first (from type tags)
    if let Some(ref actual) = world.formatted_string {
        assert_eq!(actual, &expected, "Expected '{}', got '{}'", expected, actual);
        return;
    }
    
    // Check address formatting
    if let Some(ref addr) = world.address {
        let actual = addr.to_string();
        assert_eq!(actual, expected, "Expected '{}', got '{}'", expected, actual);
        return;
    }
    
    panic!("No result found to compare");
}

/// Generic "the result should be {int} bytes" for byte count assertions
#[then(expr = "the result should be {int} bytes")]
fn then_result_should_be_n_bytes(world: &mut TestWorld, n: usize) {
    check_bytes_length(world, n);
}

/// Generic "the result should be exactly {int} bytes" (alias)
#[then(expr = "the result should be exactly {int} bytes")]
fn then_result_should_be_exactly_n_bytes(world: &mut TestWorld, n: usize) {
    check_bytes_length(world, n);
}

fn check_bytes_length(world: &TestWorld, n: usize) {
    // Check various byte storage locations
    if let Some(ref bytes) = world.serialized_bytes {
        assert_eq!(bytes.len(), n, "Expected {} bytes, got {}", n, bytes.len());
        return;
    }
    if let Some(ref bytes) = world.bcs_bytes {
        assert_eq!(bytes.len(), n, "Expected {} bytes, got {}", n, bytes.len());
        return;
    }
    if let Some(ref bytes) = world.bytes {
        assert_eq!(bytes.len(), n, "Expected {} bytes, got {}", n, bytes.len());
        return;
    }
    if let Some(ref bytes) = world.auth_key_bytes {
        assert_eq!(bytes.len(), n, "Expected {} bytes, got {}", n, bytes.len());
        return;
    }
    if let Some(ref bytes) = world.bytes_value {
        assert_eq!(bytes.len(), n, "Expected {} bytes, got {}", n, bytes.len());
        return;
    }
    if let Some(ref hash) = world.transaction_hash {
        assert_eq!(hash.as_ref().len(), n, "Expected {} bytes, got {}", n, hash.as_ref().len());
        return;
    }
    if let Some(ref hash) = world.hash_result {
        assert_eq!(hash.len(), n, "Expected {} bytes, got {}", n, hash.len());
        return;
    }
    
    panic!("No byte result found to check length");
}

/// Generic "the result should start with {string}"
#[then(expr = "the result should start with {string}")]
fn then_result_starts_with(world: &mut TestWorld, prefix: String) {
    // Check both formatted_string and string_value
    if let Some(ref formatted) = world.formatted_string {
        assert!(formatted.starts_with(&prefix), "Expected to start with '{}', got '{}'", prefix, formatted);
        return;
    }
    if let Some(ref s) = world.string_value {
        assert!(s.starts_with(&prefix), "Expected to start with '{}' but got '{}'", prefix, s);
        return;
    }
    panic!("No string result found to check prefix");
}

