//! Step definitions for account management feature tests.

use crate::support::TestWorld;
use aptos_rust_sdk_v2::account::{Account, AuthenticationKey, Ed25519Account};
use aptos_rust_sdk_v2::crypto::ED25519_SCHEME;
use cucumber::{given, then, when};

// =============================================================================
// Given Steps - Ed25519 Account
// =============================================================================

#[given("an Ed25519 account")]
fn given_ed25519_account(world: &mut TestWorld) {
    world.ed25519_account = Some(Ed25519Account::generate());
}

#[given("a newly generated Ed25519 account")]
fn given_new_ed25519_account(world: &mut TestWorld) {
    world.ed25519_account = Some(Ed25519Account::generate());
}

#[given("two different Ed25519 accounts")]
fn given_two_ed25519_accounts(world: &mut TestWorld) {
    world.ed25519_account = Some(Ed25519Account::generate());
    world.ed25519_account2 = Some(Ed25519Account::generate());
}

#[given(expr = "an Ed25519 account from private key hex {string}")]
fn given_ed25519_account_from_hex(world: &mut TestWorld, hex: String) {
    match Ed25519Account::from_private_key_hex(&hex) {
        Ok(account) => world.ed25519_account = Some(account),
        Err(e) => world.set_error(e),
    }
}

#[given(expr = "an Ed25519 account from private key bytes")]
fn given_ed25519_account_from_bytes(world: &mut TestWorld) {
    if let Some(ref bytes) = world.bytes {
        match Ed25519Account::from_private_key_bytes(bytes) {
            Ok(account) => world.ed25519_account = Some(account),
            Err(e) => world.set_error(e),
        }
    }
}

#[given(expr = "a mnemonic phrase {string}")]
fn given_mnemonic_phrase(world: &mut TestWorld, mnemonic: String) {
    world.string_value = Some(mnemonic);
}

#[given(expr = "derivation path {string}")]
fn given_derivation_path(world: &mut TestWorld, path: String) {
    // The SDK uses index-based derivation, not path-based
    // Parse the last number from the path as the index
    let index = path
        .split('/')
        .last()
        .and_then(|s| s.trim_end_matches('\'').parse::<u32>().ok())
        .unwrap_or(0);
    world
        .named_values
        .insert("derivation_index".to_string(), index.to_string());
}

// =============================================================================
// When Steps - Ed25519 Account
// =============================================================================

#[when("I generate a new Ed25519 account")]
fn when_generate_ed25519_account(world: &mut TestWorld) {
    world.ed25519_account = Some(Ed25519Account::generate());
}

#[when("I create an Ed25519 account from the private key")]
fn when_create_from_private_key(world: &mut TestWorld) {
    if let Some(ref hex) = world.hex_string {
        match Ed25519Account::from_private_key_hex(hex) {
            Ok(account) => world.ed25519_account = Some(account),
            Err(e) => world.set_error(e),
        }
    } else if let Some(ref bytes) = world.bytes {
        match Ed25519Account::from_private_key_bytes(bytes) {
            Ok(account) => world.ed25519_account = Some(account),
            Err(e) => world.set_error(e),
        }
    }
}

#[when("I derive an Ed25519 account from the mnemonic")]
fn when_derive_from_mnemonic(world: &mut TestWorld) {
    if let Some(ref mnemonic) = world.string_value {
        // Default to index 0 if no derivation path specified
        let index = world
            .named_values
            .get("derivation_index")
            .and_then(|s| s.parse().ok())
            .unwrap_or(0u32);
        match Ed25519Account::from_mnemonic(mnemonic, index) {
            Ok(account) => world.ed25519_account = Some(account),
            Err(e) => world.set_error(e),
        }
    }
}

#[when("I get the account address")]
fn when_get_account_address(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        world.address = Some(account.address());
    }
}

#[when("I get the public key")]
fn when_get_public_key(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        world.bytes = Some(account.public_key_bytes().to_vec());
    }
}

#[when("I sign a message with the account")]
fn when_sign_with_account(world: &mut TestWorld) {
    if let (Some(account), Some(message)) = (world.ed25519_account.as_ref(), world.message.as_ref())
    {
        match account.sign(message) {
            Ok(signature_bytes) => world.bytes = Some(signature_bytes),
            Err(e) => world.set_error(e),
        }
    }
}

#[when("I derive the authentication key from the account")]
fn when_derive_auth_key_from_account(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        let auth_key = account.authentication_key();
        world.auth_key_bytes = Some(auth_key.to_bytes().to_vec());
    }
}

// =============================================================================
// Then Steps - Ed25519 Account
// =============================================================================

#[then("the account should be valid")]
fn then_account_valid(world: &mut TestWorld) {
    assert!(world.ed25519_account.is_some());
}

#[then("the account address should be 32 bytes")]
fn then_account_address_32_bytes(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        assert_eq!(account.address().to_bytes().len(), 32);
    }
}

#[then("the account public key should be 32 bytes")]
fn then_account_public_key_32_bytes(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        assert_eq!(account.public_key_bytes().len(), 32);
    }
}

#[then("the two accounts should have different addresses")]
fn then_accounts_different_addresses(world: &mut TestWorld) {
    if let (Some(acc1), Some(acc2)) = (
        world.ed25519_account.as_ref(),
        world.ed25519_account2.as_ref(),
    ) {
        assert_ne!(acc1.address(), acc2.address());
    }
}

#[then("the two accounts should have different public keys")]
fn then_accounts_different_public_keys(world: &mut TestWorld) {
    if let (Some(acc1), Some(acc2)) = (
        world.ed25519_account.as_ref(),
        world.ed25519_account2.as_ref(),
    ) {
        assert_ne!(acc1.public_key_bytes(), acc2.public_key_bytes());
    }
}

#[then("recreating from the same private key should produce the same account")]
fn then_same_private_key_same_account(world: &mut TestWorld) {
    if let (Some(ref hex), Some(acc1)) = (world.hex_string.as_ref(), world.ed25519_account.as_ref())
    {
        let acc2 = Ed25519Account::from_private_key_hex(hex).unwrap();
        assert_eq!(acc1.address(), acc2.address());
        assert_eq!(acc1.public_key_bytes(), acc2.public_key_bytes());
    }
}

#[then("recreating from the same mnemonic should produce the same account")]
fn then_same_mnemonic_same_account(world: &mut TestWorld) {
    if let (Some(ref mnemonic), Some(acc1)) =
        (world.string_value.as_ref(), world.ed25519_account.as_ref())
    {
        let index = world
            .named_values
            .get("derivation_index")
            .and_then(|s| s.parse().ok())
            .unwrap_or(0u32);
        let acc2 = Ed25519Account::from_mnemonic(mnemonic, index).unwrap();
        assert_eq!(acc1.address(), acc2.address());
    }
}

#[then("the signature scheme should be Ed25519")]
fn then_signature_scheme_ed25519(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        assert_eq!(account.signature_scheme(), ED25519_SCHEME);
    }
}

#[then("the authentication key should be derived from the public key")]
fn then_auth_key_from_public_key(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        let auth_key = account.authentication_key();
        // The authentication key should be SHA3-256(public_key || scheme_byte)
        use aptos_rust_sdk_v2::crypto::derive_authentication_key;
        let derived = derive_authentication_key(&account.public_key_bytes(), ED25519_SCHEME);
        assert_eq!(auth_key.to_bytes(), derived);
    }
}

#[then("the account address should equal the authentication key")]
fn then_address_equals_auth_key(world: &mut TestWorld) {
    if let Some(ref account) = world.ed25519_account {
        let auth_key = account.authentication_key();
        let address = auth_key.to_address();
        assert_eq!(account.address(), address);
    }
}

#[then(expr = "the account address should be {string}")]
fn then_account_address_is(world: &mut TestWorld, expected: String) {
    if let Some(ref account) = world.ed25519_account {
        let addr_str = account.address().to_short_string();
        assert_eq!(addr_str, expected);
    }
}

#[then("it should fail with an invalid mnemonic error")]
fn then_invalid_mnemonic_error(world: &mut TestWorld) {
    assert!(world.has_error(), "Expected invalid mnemonic error");
}

#[then("it should fail with an invalid derivation path error")]
fn then_invalid_derivation_path_error(world: &mut TestWorld) {
    assert!(world.has_error(), "Expected invalid derivation path error");
}
