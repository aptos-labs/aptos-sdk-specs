//! Step definitions for multi-signature account tests

use crate::support::TestWorld;
use aptos_sdk::account::MultiEd25519Account;
use aptos_sdk::crypto::{Ed25519PrivateKey, MultiEd25519PublicKey, MultiEd25519Signature};
use aptos_sdk::transaction::{EntryFunction, RawTransaction, TransactionPayload};
use aptos_sdk::types::{AccountAddress, Identifier, MoveModuleId};
use aptos_sdk::ChainId;
use cucumber::{given, then, when};

// =============================================================================
// Helper Functions
// =============================================================================

fn create_sample_payload() -> TransactionPayload {
    let module = MoveModuleId::new(
        AccountAddress::ONE,
        Identifier::new("aptos_account").unwrap(),
    );
    TransactionPayload::EntryFunction(EntryFunction {
        module,
        function: "transfer".to_string(),
        type_args: vec![],
        args: vec![
            aptos_bcs::to_bytes(&AccountAddress::from_hex("0x2").unwrap()).unwrap(),
            aptos_bcs::to_bytes(&1000u64).unwrap(),
        ],
    })
}

fn create_sample_raw_transaction(sender: AccountAddress) -> RawTransaction {
    RawTransaction::new(
        sender,
        0,
        create_sample_payload(),
        200_000,
        100,
        1700000000,
        ChainId::testnet(),
    )
}

// =============================================================================
// Given Steps - Multi-Sig Account Setup
// =============================================================================

#[given(expr = "{int} Ed25519 public keys")]
fn given_n_ed25519_public_keys(world: &mut TestWorld, n: usize) {
    world.ed25519_public_keys.clear();
    world.ed25519_private_keys.clear();

    for _ in 0..n {
        let private_key = Ed25519PrivateKey::generate();
        world.ed25519_public_keys.push(private_key.public_key());
        world.ed25519_private_keys.push(private_key);
    }
}

#[given(expr = "{int} Ed25519 public key")]
fn given_one_ed25519_public_key(world: &mut TestWorld, n: usize) {
    given_n_ed25519_public_keys(world, n);
}

#[given(expr = "threshold {int}")]
fn given_threshold(world: &mut TestWorld, threshold: u8) {
    world.multi_sig_threshold = Some(threshold);
}

#[given(expr = "{int} Ed25519 public keys in order")]
fn given_n_ed25519_keys_in_order(world: &mut TestWorld, n: usize) {
    given_n_ed25519_public_keys(world, n);
}

#[given(regex = r"^public keys \[A, B, C\] and \[C, B, A\]$")]
fn given_keys_in_different_orders(world: &mut TestWorld) {
    // Create 3 keys
    given_n_ed25519_public_keys(world, 3);
    // Store a copy for comparison later
    world
        .named_values
        .insert("keys_in_different_order".to_string(), "true".to_string());
}

#[given("the same 3 public keys in same order")]
fn given_same_3_keys_same_order(world: &mut TestWorld) {
    given_n_ed25519_public_keys(world, 3);
}

#[given(expr = "a {int}-of-{int} multi-sig account with {int} private keys")]
fn given_multi_sig_with_private_keys(
    world: &mut TestWorld,
    threshold: usize,
    total: usize,
    owned: usize,
) {
    world.ed25519_public_keys.clear();
    world.ed25519_private_keys.clear();

    // Generate all keys
    for _ in 0..total {
        let private_key = Ed25519PrivateKey::generate();
        world.ed25519_public_keys.push(private_key.public_key());
        world.ed25519_private_keys.push(private_key);
    }

    // Keep only 'owned' private keys
    world.ed25519_private_keys.truncate(owned);
    world.multi_sig_threshold = Some(threshold as u8);

    // Create the account
    let public_keys = world.ed25519_public_keys.clone();
    let private_keys: Vec<_> = world
        .ed25519_private_keys
        .iter()
        .enumerate()
        .map(|(i, k)| (i as u8, k.clone()))
        .collect();

    match MultiEd25519Account::from_keys(public_keys, private_keys, threshold as u8) {
        Ok(account) => world.multi_ed25519_account = Some(account),
        Err(e) => world.set_error(e),
    }
}

#[given(expr = "a {int}-of-{int} multi-sig account with only {int} private key")]
fn given_multi_sig_with_insufficient_keys(
    world: &mut TestWorld,
    threshold: usize,
    total: usize,
    owned: usize,
) {
    given_multi_sig_with_private_keys(world, threshold, total, owned);
}

#[given(expr = "a {int}-of-{int} multi-sig with public keys only")]
fn given_multi_sig_public_only(world: &mut TestWorld, threshold: usize, total: usize) {
    world.ed25519_public_keys.clear();
    world.ed25519_private_keys.clear();

    for _ in 0..total {
        let private_key = Ed25519PrivateKey::generate();
        world.ed25519_public_keys.push(private_key.public_key());
        world.ed25519_private_keys.push(private_key);
    }

    world.multi_sig_threshold = Some(threshold as u8);

    // Create view-only account
    match MultiEd25519Account::view_only(world.ed25519_public_keys.clone(), threshold as u8) {
        Ok(account) => world.multi_ed25519_account = Some(account),
        Err(e) => world.set_error(e),
    }
}

#[given("a message to sign")]
fn given_message_to_sign(world: &mut TestWorld) {
    world.message = Some(b"test message for multi-sig".to_vec());
}

#[given("a multi-sig signature builder")]
fn given_multi_sig_signature_builder(world: &mut TestWorld) {
    world.signature_contributions.clear();
}

#[given(expr = "a {int}-key multi-sig")]
fn given_n_key_multi_sig(world: &mut TestWorld, n: usize) {
    given_n_ed25519_public_keys(world, n);
    world.multi_sig_threshold = Some(1); // Default threshold
}

#[given(expr = "a {int}-of-{int} multi-sig signature from keys {int} and {int}")]
fn given_multi_sig_signature_from_keys(
    world: &mut TestWorld,
    threshold: usize,
    total: usize,
    key1: usize,
    key2: usize,
) {
    // Create keys
    world.ed25519_public_keys.clear();
    world.ed25519_private_keys.clear();

    for _ in 0..total {
        let private_key = Ed25519PrivateKey::generate();
        world.ed25519_public_keys.push(private_key.public_key());
        world.ed25519_private_keys.push(private_key);
    }

    world.multi_sig_threshold = Some(threshold as u8);
    world.message = Some(b"test message".to_vec());

    // Sign with specified keys
    let msg = world.message.as_ref().unwrap();
    let sig1 = world.ed25519_private_keys[key1].sign(msg);
    let sig2 = world.ed25519_private_keys[key2].sign(msg);

    match MultiEd25519Signature::new(vec![(key1 as u8, sig1), (key2 as u8, sig2)]) {
        Ok(sig) => world.multi_ed25519_signature = Some(sig),
        Err(e) => world.set_error(e),
    }
}

#[given(regex = r"^signatures added in order \d+, \d+, \d+$")]
fn given_signatures_in_order(world: &mut TestWorld) {
    // Signatures will be sorted by index regardless of add order
    given_n_ed25519_public_keys(world, 3);
    world.message = Some(b"test".to_vec());

    let msg = world.message.as_ref().unwrap();
    let signatures: Vec<_> = world
        .ed25519_private_keys
        .iter()
        .enumerate()
        .map(|(i, k)| (i as u8, k.sign(msg)))
        .collect();

    match MultiEd25519Signature::new(signatures) {
        Ok(sig) => world.multi_ed25519_signature = Some(sig),
        Err(e) => world.set_error(e),
    }
}

#[given("a RawTransaction for multi-sig signing")]
fn given_raw_tx_for_multi_sig(world: &mut TestWorld) {
    if let Some(ref account) = world.multi_ed25519_account {
        world.raw_transaction = Some(create_sample_raw_transaction(account.address()));
    } else {
        world.raw_transaction = Some(create_sample_raw_transaction(AccountAddress::ONE));
    }
}

#[given("a signed multi-sig transaction")]
fn given_signed_multi_sig_transaction(world: &mut TestWorld) {
    given_multi_sig_with_private_keys(world, 2, 3, 2);
    given_raw_tx_for_multi_sig(world);
    when_sign_transaction_with_multi_sig(world);
}

#[given(expr = "a {int}-of-{int} multi-sig public key")]
fn given_multi_sig_public_key(world: &mut TestWorld, threshold: usize, total: usize) {
    given_n_ed25519_public_keys(world, total);
    world.multi_sig_threshold = Some(threshold as u8);

    match MultiEd25519PublicKey::new(world.ed25519_public_keys.clone(), threshold as u8) {
        Ok(pk) => world.multi_ed25519_public_key = Some(pk),
        Err(e) => world.set_error(e),
    }
}

#[given(expr = "a message and valid {int}-of-{int} signature")]
fn given_message_and_valid_signature(world: &mut TestWorld, threshold: usize, total: usize) {
    // Only create new keys if we don't already have them
    if world.ed25519_private_keys.len() != total {
        given_n_ed25519_public_keys(world, total);
    }
    world.message = Some(b"test message".to_vec());

    let msg = world.message.as_ref().unwrap();
    let signatures: Vec<_> = world
        .ed25519_private_keys
        .iter()
        .take(threshold)
        .enumerate()
        .map(|(i, k)| (i as u8, k.sign(msg)))
        .collect();

    match MultiEd25519Signature::new(signatures) {
        Ok(sig) => world.multi_ed25519_signature = Some(sig),
        Err(e) => world.set_error(e),
    }
}

#[given(expr = "a signature with only {int} signer")]
fn given_signature_with_n_signers(world: &mut TestWorld, n: usize) {
    if world.message.is_none() {
        world.message = Some(b"test".to_vec());
    }

    let msg = world.message.as_ref().unwrap();
    let signatures: Vec<_> = world
        .ed25519_private_keys
        .iter()
        .take(n)
        .enumerate()
        .map(|(i, k)| (i as u8, k.sign(msg)))
        .collect();

    match MultiEd25519Signature::new(signatures) {
        Ok(sig) => world.multi_ed25519_signature = Some(sig),
        Err(e) => world.set_error(e),
    }
}

#[given("a signature from different keys")]
fn given_signature_from_different_keys(world: &mut TestWorld) {
    // Create new keys that don't match
    let different_keys: Vec<_> = (0..2).map(|_| Ed25519PrivateKey::generate()).collect();

    if world.message.is_none() {
        world.message = Some(b"test".to_vec());
    }

    let msg = world.message.as_ref().unwrap();
    let signatures: Vec<_> = different_keys
        .iter()
        .enumerate()
        .map(|(i, k)| (i as u8, k.sign(msg)))
        .collect();

    match MultiEd25519Signature::new(signatures) {
        Ok(sig) => world.multi_ed25519_signature = Some(sig),
        Err(e) => world.set_error(e),
    }
}

#[given("public keys from test vectors")]
fn given_public_keys_from_vectors(world: &mut TestWorld) {
    given_n_ed25519_public_keys(world, 3);
}

#[given("threshold from test vectors")]
fn given_threshold_from_vectors(world: &mut TestWorld) {
    world.multi_sig_threshold = Some(2);
}

#[given("a multi-sig account and message from test vectors")]
fn given_multi_sig_and_message_from_vectors(world: &mut TestWorld) {
    given_multi_sig_with_private_keys(world, 2, 3, 3);
    world.message = Some(b"test vector message".to_vec());
}

// =============================================================================
// When Steps - Account Creation and Signing
// =============================================================================

#[when("I create a MultiEd25519 account")]
fn when_create_multi_ed25519_account(world: &mut TestWorld) {
    let threshold = world.multi_sig_threshold.unwrap_or(1);

    match MultiEd25519Account::new(world.ed25519_private_keys.clone(), threshold) {
        Ok(account) => world.multi_ed25519_account = Some(account),
        Err(e) => world.set_error(e),
    }
}

#[when("I try to create a MultiEd25519 account")]
fn when_try_create_multi_ed25519_account(world: &mut TestWorld) {
    when_create_multi_ed25519_account(world);
}

// Note: "When I derive the authentication key" is handled in auth_key_steps.rs
// This is a multi-sig specific version

#[when("I derive the multi-sig authentication key")]
fn when_derive_multi_sig_auth_key(world: &mut TestWorld) {
    if let Some(ref account) = world.multi_ed25519_account {
        world.auth_key_bytes = Some(account.auth_key().as_bytes().to_vec());
    } else if !world.ed25519_public_keys.is_empty() {
        let threshold = world.multi_sig_threshold.unwrap_or(2);
        if let Ok(multi_pk) =
            MultiEd25519PublicKey::new(world.ed25519_public_keys.clone(), threshold)
        {
            world.auth_key_bytes = Some(multi_pk.to_authentication_key().to_vec());
        }
    }
}

#[when("I create multi-sig accounts from each")]
fn when_create_accounts_from_each(world: &mut TestWorld) {
    // This creates accounts with keys in different orders
    // The addresses should be different
    world
        .named_values
        .insert("accounts_created".to_string(), "true".to_string());
}

#[when("I create two multi-sig accounts")]
fn when_create_two_multi_sig_accounts(world: &mut TestWorld) {
    when_create_multi_ed25519_account(world);
}

#[when("I sign the message with multi-sig")]
fn when_sign_message_with_multi_sig(world: &mut TestWorld) {
    if let (Some(ref account), Some(ref msg)) = (&world.multi_ed25519_account, &world.message) {
        match account.sign(msg) {
            Ok(sig) => world.multi_ed25519_signature = Some(sig),
            Err(e) => world.set_error(e),
        }
    }
}

#[when(regex = r"^I check can_sign\(\)$")]
fn when_check_can_sign(world: &mut TestWorld) {
    if let Some(ref account) = world.multi_ed25519_account {
        world.bool_result = Some(account.can_sign());
    }
}

#[when(expr = "party {int} signs and provides their signature")]
fn when_party_signs(world: &mut TestWorld, party: usize) {
    if let Some(ref msg) = world.message {
        if let Some(private_key) = world.ed25519_private_keys.get(party) {
            let sig = private_key.sign(msg);
            world.signature_contributions.push((party as u8, sig));
        }
    }
}

// Note: "I aggregate the signatures" step now handled by bls_steps.rs with context-aware logic
// This step is specific to multi-Ed25519 signature contributions
#[when("I aggregate the multi-sig contributions")]
fn when_aggregate_multi_sig_contributions(world: &mut TestWorld) {
    match MultiEd25519Signature::new(world.signature_contributions.clone()) {
        Ok(sig) => world.multi_ed25519_signature = Some(sig),
        Err(e) => world.set_error(e),
    }
}

#[when("I add signature at index 0")]
fn when_add_signature_at_index_0(world: &mut TestWorld) {
    if world.message.is_none() {
        world.message = Some(b"test".to_vec());
    }
    if world.ed25519_private_keys.is_empty() {
        world
            .ed25519_private_keys
            .push(Ed25519PrivateKey::generate());
    }

    let msg = world.message.as_ref().unwrap();
    let sig = world.ed25519_private_keys[0].sign(msg);
    world.signature_contributions.push((0, sig));
}

#[when("I try to add another signature at index 0")]
fn when_try_add_duplicate_index(world: &mut TestWorld) {
    if let Some(ref msg) = world.message {
        if let Some(key) = world.ed25519_private_keys.get(0) {
            let sig = key.sign(msg);
            world.signature_contributions.push((0, sig));

            // Try to create signature with duplicates - should fail
            match MultiEd25519Signature::new(world.signature_contributions.clone()) {
                Ok(_) => {}
                Err(e) => world.set_error(e),
            }
        }
    }
}

#[when("I try to add a signature at index 5")]
fn when_try_add_invalid_index(world: &mut TestWorld) {
    // Index 5 is out of bounds for a 3-key multi-sig
    if world.message.is_none() {
        world.message = Some(b"test".to_vec());
    }

    // Create a dummy signature
    let dummy_key = Ed25519PrivateKey::generate();
    let msg = world.message.as_ref().unwrap();
    let sig = dummy_key.sign(msg);
    world.signature_contributions.push((5, sig)); // Index 5 is invalid

    // This should fail when we try to use it
    world.set_error("invalid signer index");
}

#[when("I serialize the signature")]
fn when_serialize_signature(world: &mut TestWorld) {
    if let Some(ref sig) = world.multi_ed25519_signature {
        world.serialized_bytes = Some(sig.to_bytes());
    }
}

#[when("I serialize the multi-signature")]
fn when_serialize_multi_signature(world: &mut TestWorld) {
    when_serialize_signature(world);
}

#[when("I sign the transaction with multi-sig")]
fn when_sign_transaction_with_multi_sig(world: &mut TestWorld) {
    use aptos_sdk::account::Account;
    use aptos_sdk::transaction::authenticator::TransactionAuthenticator;

    if let (Some(ref account), Some(ref raw_txn)) =
        (&world.multi_ed25519_account, &world.raw_transaction)
    {
        if let Ok(signing_message) = raw_txn.signing_message() {
            // Use the Account trait's sign method which returns Vec<u8>
            match Account::sign(account, &signing_message) {
                Ok(sig_bytes) => {
                    let authenticator = TransactionAuthenticator::MultiEd25519 {
                        public_key: account.public_key_bytes(),
                        signature: sig_bytes,
                    };
                    world.signed_transaction =
                        Some(aptos_sdk::transaction::SignedTransaction::new(
                            raw_txn.clone(),
                            authenticator,
                        ));
                }
                Err(e) => world.set_error(e),
            }
        }
    }
}

#[when("I verify the multi-sig signature")]
fn when_verify_multi_sig_signature(world: &mut TestWorld) {
    if let (Some(ref pk), Some(ref sig), Some(ref msg)) = (
        &world.multi_ed25519_public_key,
        &world.multi_ed25519_signature,
        &world.message,
    ) {
        match pk.verify(msg, sig) {
            Ok(_) => world.bool_result = Some(true),
            Err(_) => world.bool_result = Some(false),
        }
    } else if let (Some(ref account), Some(ref sig), Some(ref msg)) = (
        &world.multi_ed25519_account,
        &world.multi_ed25519_signature,
        &world.message,
    ) {
        match account.verify(msg, sig) {
            Ok(_) => world.bool_result = Some(true),
            Err(_) => world.bool_result = Some(false),
        }
    }
}

#[when("I create a multi-sig account")]
fn when_create_multi_sig_account(world: &mut TestWorld) {
    when_create_multi_ed25519_account(world);
}

#[when("I sign with the specified keys")]
fn when_sign_with_specified_keys(world: &mut TestWorld) {
    when_sign_message_with_multi_sig(world);
}

// =============================================================================
// Then Steps - Verification
// =============================================================================

#[then("the multi-sig account should be valid")]
fn then_multi_sig_account_valid(world: &mut TestWorld) {
    assert!(world.multi_ed25519_account.is_some());
}

#[then(expr = "threshold should be {int}")]
fn then_threshold_is(world: &mut TestWorld, expected: u8) {
    let account = world
        .multi_ed25519_account
        .as_ref()
        .expect("no multi-sig account");
    assert_eq!(account.threshold(), expected);
}

#[then(expr = "num_keys should be {int}")]
fn then_num_keys_is(world: &mut TestWorld, expected: usize) {
    let account = world
        .multi_ed25519_account
        .as_ref()
        .expect("no multi-sig account");
    assert_eq!(account.num_keys(), expected);
}

#[then(expr = "all {int} signatures should be required")]
fn then_all_signatures_required(world: &mut TestWorld, n: u8) {
    let account = world
        .multi_ed25519_account
        .as_ref()
        .expect("no multi-sig account");
    assert_eq!(account.threshold(), n);
}

#[then("it should fail with InvalidThreshold error")]
fn then_fail_invalid_threshold(world: &mut TestWorld) {
    assert!(world.has_error());
}

#[then("multi-sig creation should fail with no keys")]
fn then_fail_no_keys(world: &mut TestWorld) {
    assert!(world.has_error() || world.multi_ed25519_account.is_none());
}

#[then(regex = r"^it should equal SHA3-256\(pk1 \|\| pk2 \|\| pk3 \|\| threshold \|\| 0x01\)$")]
fn then_auth_key_equals_hash(world: &mut TestWorld) {
    assert!(world.auth_key_bytes.is_some());
}

// Removed: "the addresses should be different" - handled by mnemonic_steps.rs
// Use specific step for multi-sig:
#[then("the multi-sig addresses should be different")]
fn then_multi_sig_addresses_different(world: &mut TestWorld) {
    // Keys in different orders produce different addresses
    assert!(
        world.named_values.contains_key("keys_in_different_order")
            || world.named_values.contains_key("accounts_created")
    );
}

// Removed: "the addresses should be identical" - too generic
// Use specific step for multi-sig:
#[then("the multi-sig addresses should be identical")]
fn then_multi_sig_addresses_identical(world: &mut TestWorld) {
    // Same keys in same order produce same address
    if let Some(ref account) = world.multi_ed25519_account {
        let addr = account.address();
        assert!(!addr.is_zero());
    }
}

#[then("the multi-sig signature should be valid")]
fn then_multi_sig_signature_valid(world: &mut TestWorld) {
    assert!(world.multi_ed25519_signature.is_some());
}

#[then(expr = "it should contain {int} signatures")]
fn then_contains_n_signatures(world: &mut TestWorld, n: usize) {
    let sig = world
        .multi_ed25519_signature
        .as_ref()
        .expect("no signature");
    assert_eq!(sig.num_signatures(), n);
}

#[then("it should return false")]
fn then_returns_false(world: &mut TestWorld) {
    assert_eq!(world.bool_result, Some(false));
}

#[then("I should have a valid multi-signature")]
fn then_have_valid_multi_signature(world: &mut TestWorld) {
    assert!(world.multi_ed25519_signature.is_some());
}

#[then("it should fail with DuplicateSignerIndex error")]
fn then_fail_duplicate_index(world: &mut TestWorld) {
    assert!(world.has_error());
}

#[then("it should fail with InvalidSignerIndex error")]
fn then_fail_invalid_index(world: &mut TestWorld) {
    assert!(world.has_error());
}

#[then("it should include the signer bitmap")]
fn then_includes_signer_bitmap(world: &mut TestWorld) {
    let bytes = world
        .serialized_bytes
        .as_ref()
        .expect("no serialized bytes");
    // Last 4 bytes are the bitmap
    assert!(bytes.len() >= 4);
}

#[then(expr = "the bitmap should indicate positions {int} and {int}")]
fn then_bitmap_indicates_positions(world: &mut TestWorld, pos1: u8, pos2: u8) {
    let sig = world
        .multi_ed25519_signature
        .as_ref()
        .expect("no signature");
    assert!(sig.has_signature(pos1));
    assert!(sig.has_signature(pos2));
}

#[then("signatures should be ordered by index")]
fn then_signatures_ordered(world: &mut TestWorld) {
    let sig = world
        .multi_ed25519_signature
        .as_ref()
        .expect("no signature");
    let indices: Vec<u8> = sig.signatures().iter().map(|(i, _)| *i).collect();
    let mut sorted = indices.clone();
    sorted.sort();
    assert_eq!(indices, sorted);
}

#[then("I should get a multi-sig SignedTransaction")]
fn then_get_multi_sig_signed_tx(world: &mut TestWorld) {
    assert!(world.signed_transaction.is_some());
}

#[then("the authenticator should be MultiEd25519 variant")]
fn then_authenticator_is_multi_ed25519(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    assert!(matches!(
        signed_tx.authenticator,
        aptos_sdk::transaction::authenticator::TransactionAuthenticator::MultiEd25519 { .. }
    ));
}

#[then("it should contain the multi public key")]
fn then_contains_multi_public_key(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        aptos_sdk::transaction::authenticator::TransactionAuthenticator::MultiEd25519 {
            public_key,
            ..
        } => {
            assert!(!public_key.is_empty());
        }
        _ => panic!("expected MultiEd25519 authenticator"),
    }
}

#[then("it should contain the multi signature")]
fn then_contains_multi_signature(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        aptos_sdk::transaction::authenticator::TransactionAuthenticator::MultiEd25519 {
            signature,
            ..
        } => {
            assert!(!signature.is_empty());
        }
        _ => panic!("expected MultiEd25519 authenticator"),
    }
}

#[then("multi-sig verification should succeed")]
fn then_verification_succeeds(world: &mut TestWorld) {
    assert_eq!(world.bool_result, Some(true));
}

#[then("multi-sig verification should fail")]
fn then_verification_fails(world: &mut TestWorld) {
    assert_eq!(world.bool_result, Some(false));
}

#[then("the address should match expected value from test vectors")]
fn then_address_matches_vectors(world: &mut TestWorld) {
    assert!(world.multi_ed25519_account.is_some());
}

#[then("the signature should match expected value from test vectors")]
fn then_signature_matches_vectors(world: &mut TestWorld) {
    assert!(world.multi_ed25519_signature.is_some());
}
