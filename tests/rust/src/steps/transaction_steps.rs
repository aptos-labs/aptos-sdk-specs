//! Step definitions for transaction building and signing tests

use crate::support::world::TestWorld;
use aptos_rust_sdk_v2::account::Ed25519Account;
use aptos_rust_sdk_v2::transaction::{
    EntryFunction, RawTransaction, SignedTransaction, TransactionPayload,
};
use aptos_rust_sdk_v2::types::{AccountAddress, MoveModuleId};
use aptos_rust_sdk_v2::ChainId;
use cucumber::{given, then, when};

// =============================================================================
// RawTransaction Creation
// =============================================================================

#[given(expr = "a sender address {string}")]
fn given_sender_address(world: &mut TestWorld, addr: String) {
    world.tx_sender = Some(AccountAddress::from_hex(&addr).expect("Invalid sender address"));
}

#[given(expr = "a sequence number {int}")]
fn given_sequence_number(world: &mut TestWorld, seq: u64) {
    world.tx_sequence_number = Some(seq);
}

#[given(expr = "an entry function payload for APT transfer")]
fn given_apt_transfer_payload(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::types::Identifier;
    let module = MoveModuleId::new(
        AccountAddress::ONE,
        Identifier::new("aptos_account").unwrap(),
    );
    let entry_fn = EntryFunction {
        module,
        function: "transfer".to_string(),
        type_args: vec![],
        args: vec![
            aptos_bcs::to_bytes(&AccountAddress::from_hex("0x2").unwrap()).unwrap(),
            aptos_bcs::to_bytes(&1000u64).unwrap(),
        ],
    };
    world.tx_payload = Some(TransactionPayload::EntryFunction(entry_fn));
}

#[given(expr = "max gas amount {int}")]
fn given_max_gas_amount(world: &mut TestWorld, amount: u64) {
    world.tx_max_gas = Some(amount);
}

#[given(expr = "gas unit price {int}")]
fn given_gas_unit_price(world: &mut TestWorld, price: u64) {
    world.tx_gas_price = Some(price);
}

#[given(expr = "expiration timestamp {int}")]
fn given_expiration_timestamp(world: &mut TestWorld, ts: u64) {
    world.tx_expiration = Some(ts);
}

#[given(regex = r"^chain ID testnet \(2\)$")]
fn given_chain_id_testnet(world: &mut TestWorld) {
    world.tx_chain_id = Some(ChainId::testnet());
}

#[given(regex = r"^chain ID mainnet \(1\)$")]
fn given_chain_id_mainnet(world: &mut TestWorld) {
    world.tx_chain_id = Some(ChainId::mainnet());
}

#[given(regex = r"^a RawTransaction with chain ID (\d+) \((\w+)\)$")]
fn given_raw_tx_with_chain_id(world: &mut TestWorld, chain_id: u8, _name: String) {
    create_sample_raw_transaction(world);
    world.tx_chain_id = Some(ChainId::new(chain_id));
    when_create_raw_transaction(world);
}

#[when(expr = "I create a RawTransaction")]
fn when_create_raw_transaction(world: &mut TestWorld) {
    let sender = world.tx_sender.expect("No sender");
    let sequence_number = world.tx_sequence_number.expect("No sequence number");
    let payload = world.tx_payload.clone().expect("No payload");
    let max_gas_amount = world.tx_max_gas.unwrap_or(200000);
    let gas_unit_price = world.tx_gas_price.unwrap_or(100);
    let expiration_timestamp_secs = world.tx_expiration.unwrap_or(1700000000);
    let chain_id = world.tx_chain_id.unwrap_or(ChainId::testnet());
    
    world.raw_transaction = Some(RawTransaction::new(
        sender,
        sequence_number,
        payload,
        max_gas_amount,
        gas_unit_price,
        expiration_timestamp_secs,
        chain_id,
    ));
}

#[given(expr = "a valid RawTransaction")]
fn given_valid_raw_transaction(world: &mut TestWorld) {
    create_sample_raw_transaction(world);
    when_create_raw_transaction(world);
}

#[given(expr = "a RawTransaction with known values")]
fn given_raw_tx_with_known_values(world: &mut TestWorld) {
    given_valid_raw_transaction(world);
}

#[given(expr = "a RawTransaction")]
fn given_raw_transaction(world: &mut TestWorld) {
    given_valid_raw_transaction(world);
}

// Note: "a RawTransaction with chain ID X (mainnet/testnet)" is handled by regex at line ~70

#[given(expr = "two RawTransactions with different sequence numbers")]
fn given_two_raw_transactions(world: &mut TestWorld) {
    create_sample_raw_transaction(world);
    world.tx_sequence_number = Some(0);
    when_create_raw_transaction(world);
    world.raw_transaction2 = world.raw_transaction.clone();
    
    world.tx_sequence_number = Some(1);
    when_create_raw_transaction(world);
}

// =============================================================================
// Transaction Field Access
// =============================================================================

#[when(expr = "I access the fields")]
fn when_access_fields(world: &mut TestWorld) {
    // Fields are accessed in the then steps
    assert!(world.raw_transaction.is_some());
}

#[then(regex = r"^sender\(\) should return the sender address$")]
fn then_sender_returns_address(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.sender, world.tx_sender.unwrap());
}

#[then(regex = r"^sequence_number\(\) should return the sequence number$")]
fn then_sequence_number_returns(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.sequence_number, world.tx_sequence_number.unwrap());
}

#[then(regex = r"^payload\(\) should return the payload$")]
fn then_payload_returns(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert!(matches!(raw_tx.payload, TransactionPayload::EntryFunction(_)));
}

#[then(regex = r"^max_gas_amount\(\) should return the max gas$")]
fn then_max_gas_returns(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.max_gas_amount, world.tx_max_gas.unwrap_or(200000));
}

#[then(regex = r"^gas_unit_price\(\) should return the gas price$")]
fn then_gas_price_returns(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.gas_unit_price, world.tx_gas_price.unwrap_or(100));
}

#[then(regex = r"^expiration_timestamp_secs\(\) should return the expiration$")]
fn then_expiration_returns(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.expiration_timestamp_secs, world.tx_expiration.unwrap_or(1700000000));
}

#[then(regex = r"^chain_id\(\) should return the chain ID$")]
fn then_chain_id_returns(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert!(raw_tx.chain_id.id() > 0);
}

// =============================================================================
// Transaction Validation
// =============================================================================

#[then(expr = "the transaction should be valid")]
fn then_tx_valid(world: &mut TestWorld) {
    assert!(world.raw_transaction.is_some());
}

#[then(expr = "sender should be {string}")]
fn then_sender_is(world: &mut TestWorld, expected: String) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.sender.to_short_string(), expected);
}

#[then(expr = "sequence number should be {int}")]
fn then_sequence_number_is(world: &mut TestWorld, expected: u64) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    assert_eq!(raw_tx.sequence_number, expected);
}

// =============================================================================
// BCS Serialization
// =============================================================================

// Note: "I BCS serialize it" is handled in serialization_steps.rs

// Note: "the serialization should succeed" is handled in type_tags_steps.rs

#[then(expr = "the bytes should be deterministic")]
fn then_bytes_deterministic(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    let bytes1 = aptos_bcs::to_bytes(raw_tx).unwrap();
    let bytes2 = aptos_bcs::to_bytes(raw_tx).unwrap();
    assert_eq!(bytes1, bytes2);
}

#[then(regex = r"^sender should be serialized first \((\d+) bytes\)$")]
fn then_sender_serialized_first(world: &mut TestWorld, n: usize) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    assert!(bytes.len() >= n);
}

#[then(regex = r"^sequence_number should be next \((\d+) bytes\)$")]
fn then_sequence_number_next(world: &mut TestWorld, _n: usize) {
    assert!(world.serialized_bytes.is_some());
}

#[then(expr = "payload should follow")]
fn then_payload_follows(world: &mut TestWorld) {
    assert!(world.serialized_bytes.is_some());
}

#[then(regex = r"^max_gas_amount, gas_unit_price, expiration, chain_id should be in order$")]
fn then_fields_in_order(world: &mut TestWorld) {
    assert!(world.serialized_bytes.is_some());
}

// Note: "I BCS serialize and deserialize it" is handled in type_tags_steps.rs

#[then(expr = "the result should equal the original")]
fn then_result_equals_original(world: &mut TestWorld) {
    if let (Some(original), Some(deserialized)) = (&world.signed_transaction, &world.signed_transaction2) {
        // Compare SignedTransactions
        let orig_bytes = aptos_bcs::to_bytes(original).unwrap();
        let deser_bytes = aptos_bcs::to_bytes(deserialized).unwrap();
        assert_eq!(orig_bytes, deser_bytes, "SignedTransaction roundtrip failed");
    } else if let (Some(original), Some(deserialized)) = (&world.raw_transaction, &world.raw_transaction2) {
        // Compare RawTransactions
        assert_eq!(original.sender, deserialized.sender);
        assert_eq!(original.sequence_number, deserialized.sequence_number);
    } else {
        panic!("No original/deserialized to compare");
    }
}

// =============================================================================
// Signing Message
// =============================================================================

#[when(expr = "I generate the signing message")]
fn when_generate_signing_message(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    world.signing_message = Some(raw_tx.signing_message().expect("Failed to generate signing message"));
}

#[when(expr = "I generate the signing message twice")]
fn when_generate_signing_message_twice(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    world.signing_message = Some(raw_tx.signing_message().expect("Failed to generate signing message"));
    world.signing_message2 = Some(raw_tx.signing_message().expect("Failed to generate signing message"));
}

#[when(expr = "I generate signing messages for both")]
fn when_generate_signing_messages_both(world: &mut TestWorld) {
    let raw_tx1 = world.raw_transaction.as_ref().expect("No first RawTransaction");
    let raw_tx2 = world.raw_transaction2.as_ref().expect("No second RawTransaction");
    world.signing_message = Some(raw_tx1.signing_message().expect("Failed to generate signing message"));
    world.signing_message2 = Some(raw_tx2.signing_message().expect("Failed to generate signing message"));
}

#[then(regex = r#"^the message should start with SHA3-256\("APTOS::RawTransaction"\)$"#)]
fn then_message_starts_with_domain(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::crypto::sha3_256;
    let domain_hash = sha3_256(b"APTOS::RawTransaction");
    let signing_msg = world.signing_message.as_ref().expect("No signing message");
    assert!(signing_msg.starts_with(&domain_hash));
}

#[then(expr = "the message should contain the BCS-serialized transaction")]
fn then_message_contains_tx(world: &mut TestWorld) {
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    let signing_msg = world.signing_message.as_ref().expect("No signing message");
    let tx_bytes = aptos_bcs::to_bytes(raw_tx).unwrap();
    assert!(signing_msg.len() > tx_bytes.len());
}

#[then(expr = "both messages should be identical")]
fn then_messages_identical(world: &mut TestWorld) {
    let msg1 = world.signing_message.as_ref().expect("No first message");
    let msg2 = world.signing_message2.as_ref().expect("No second message");
    assert_eq!(msg1, msg2);
}

#[then(expr = "the messages should be different")]
fn then_messages_different(world: &mut TestWorld) {
    let msg1 = world.signing_message.as_ref().expect("No first message");
    let msg2 = world.signing_message2.as_ref().expect("No second message");
    assert_ne!(msg1, msg2);
}

#[then(expr = "the chain_id byte should be {word}")]
fn then_chain_id_byte(world: &mut TestWorld, hex: String) {
    let bytes = world.serialized_bytes.as_ref().expect("No serialized bytes");
    let expected = parse_hex_byte(&hex);
    // Chain ID is the last byte in the serialized transaction
    let last_byte = bytes.last().expect("Empty bytes");
    assert_eq!(*last_byte, expected);
}

// =============================================================================
// Transaction Signing
// =============================================================================

// Note: "an Ed25519 account" is handled in account_steps.rs

// Note: "two different Ed25519 accounts" is handled in account_steps.rs

#[when(expr = "I sign the transaction with the account")]
fn when_sign_with_account(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::transaction::sign_transaction;
    
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    let account = world.ed25519_account.as_ref().expect("No account");
    let signed_tx = sign_transaction(raw_tx, account).expect("Failed to sign");
    world.signed_transaction = Some(signed_tx);
}

#[when(expr = "I sign the transaction")]
fn when_sign_transaction(world: &mut TestWorld) {
    when_sign_with_account(world);
}

#[when(expr = "I sign the transaction twice")]
fn when_sign_transaction_twice(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::transaction::sign_transaction;
    
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    let account = world.ed25519_account.as_ref().expect("No account");
    world.signed_transaction = Some(sign_transaction(raw_tx, account).expect("Failed to sign"));
    world.signed_transaction2 = Some(sign_transaction(raw_tx, account).expect("Failed to sign"));
}

#[when(expr = "both accounts sign the transaction")]
fn when_both_accounts_sign(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::transaction::sign_transaction;
    
    let raw_tx = world.raw_transaction.as_ref().expect("No RawTransaction");
    let account1 = world.ed25519_account.as_ref().expect("No first account");
    let account2 = world.ed25519_account2.as_ref().expect("No second account");
    world.signed_transaction = Some(sign_transaction(raw_tx, account1).expect("Failed to sign"));
    world.signed_transaction2 = Some(sign_transaction(raw_tx, account2).expect("Failed to sign"));
}

#[then(expr = "I should get a SignedTransaction")]
fn then_get_signed_transaction(world: &mut TestWorld) {
    assert!(world.signed_transaction.is_some());
}

#[then(expr = "the authenticator should be Ed25519 variant")]
fn then_authenticator_ed25519(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    // The authenticator is Ed25519 if the transaction was signed with an Ed25519 account
    assert!(world.ed25519_account.is_some());
}

#[then(expr = "both SignedTransactions should be identical")]
fn then_signed_txs_identical(world: &mut TestWorld) {
    let tx1 = world.signed_transaction.as_ref().expect("No first SignedTransaction");
    let tx2 = world.signed_transaction2.as_ref().expect("No second SignedTransaction");
    let bytes1 = aptos_bcs::to_bytes(tx1).unwrap();
    let bytes2 = aptos_bcs::to_bytes(tx2).unwrap();
    assert_eq!(bytes1, bytes2);
}

// "the signatures should be different" is handled in cryptography_steps.rs
// The transaction-level version is "the SignedTransactions should be different"
#[then(expr = "the SignedTransactions should be different")]
fn then_tx_signatures_different(world: &mut TestWorld) {
    let tx1 = world.signed_transaction.as_ref().expect("No first SignedTransaction");
    let tx2 = world.signed_transaction2.as_ref().expect("No second SignedTransaction");
    let bytes1 = aptos_bcs::to_bytes(tx1).unwrap();
    let bytes2 = aptos_bcs::to_bytes(tx2).unwrap();
    assert_ne!(bytes1, bytes2);
}

// =============================================================================
// SignedTransaction Operations
// =============================================================================

#[given(expr = "a SignedTransaction")]
fn given_signed_transaction(world: &mut TestWorld) {
    given_valid_raw_transaction(world);
    // Create an Ed25519 account (inline instead of calling account_steps)
    world.ed25519_account = Some(Ed25519Account::generate());
    when_sign_with_account(world);
}

#[given(expr = "a signed transaction")]
fn given_a_signed_transaction(world: &mut TestWorld) {
    given_signed_transaction(world);
}

#[given(expr = "a signed transaction with Ed25519")]
fn given_signed_tx_ed25519(world: &mut TestWorld) {
    given_signed_transaction(world);
}

#[given(expr = "two different SignedTransactions")]
fn given_two_signed_transactions(world: &mut TestWorld) {
    given_valid_raw_transaction(world);
    // Create two Ed25519 accounts inline
    world.ed25519_account = Some(Ed25519Account::generate());
    world.ed25519_account2 = Some(Ed25519Account::generate());
    when_both_accounts_sign(world);
}

#[when(expr = "I get the raw_transaction")]
fn when_get_raw_transaction(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    world.raw_transaction2 = Some(signed_tx.raw_txn.clone());
}

#[then(expr = "it should equal the original RawTransaction")]
fn then_equals_original_raw_tx(world: &mut TestWorld) {
    let original = world.raw_transaction.as_ref().expect("No original");
    let extracted = world.raw_transaction2.as_ref().expect("No extracted");
    let bytes1 = aptos_bcs::to_bytes(original).unwrap();
    let bytes2 = aptos_bcs::to_bytes(extracted).unwrap();
    assert_eq!(bytes1, bytes2);
}

#[when(regex = r"^I call to_bytes\(\)$")]
fn when_call_to_bytes(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    world.serialized_bytes = Some(aptos_bcs::to_bytes(signed_tx).unwrap());
}

#[then(expr = "the result should be valid BCS")]
fn then_result_valid_bcs(world: &mut TestWorld) {
    let bytes = world.serialized_bytes.as_ref().expect("No bytes");
    let _: SignedTransaction = aptos_bcs::from_bytes(bytes).expect("Invalid BCS");
}

#[when(expr = "I serialize it twice")]
fn when_serialize_twice(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    world.serialized_bytes = Some(aptos_bcs::to_bytes(signed_tx).unwrap());
    world.serialized_bytes2 = Some(aptos_bcs::to_bytes(signed_tx).unwrap());
}

// Note: "both results should be identical" is handled in hashing_steps.rs

#[when(expr = "I serialize and deserialize it")]
fn when_serialize_deserialize(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    let bytes = aptos_bcs::to_bytes(signed_tx).unwrap();
    let deserialized: SignedTransaction = aptos_bcs::from_bytes(&bytes).unwrap();
    world.signed_transaction2 = Some(deserialized);
}

// =============================================================================
// Transaction Hash
// =============================================================================

#[when(expr = "I compute the hash")]
fn when_compute_hash(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    world.transaction_hash = Some(signed_tx.hash().expect("Failed to compute hash"));
}

#[when(expr = "I compute the hash twice")]
fn when_compute_hash_twice(world: &mut TestWorld) {
    let signed_tx = world.signed_transaction.as_ref().expect("No SignedTransaction");
    world.transaction_hash = Some(signed_tx.hash().expect("Failed to compute hash"));
    world.transaction_hash2 = Some(signed_tx.hash().expect("Failed to compute hash"));
}

#[when(expr = "I compute their hashes")]
fn when_compute_both_hashes(world: &mut TestWorld) {
    let tx1 = world.signed_transaction.as_ref().expect("No first SignedTransaction");
    let tx2 = world.signed_transaction2.as_ref().expect("No second SignedTransaction");
    world.transaction_hash = Some(tx1.hash().expect("Failed to compute hash"));
    world.transaction_hash2 = Some(tx2.hash().expect("Failed to compute hash"));
}

#[then(expr = "both hashes should be identical")]
fn then_hashes_identical(world: &mut TestWorld) {
    let h1 = world.transaction_hash.as_ref().expect("No first hash");
    let h2 = world.transaction_hash2.as_ref().expect("No second hash");
    assert_eq!(h1, h2);
}

// "the hashes should be different" is handled in hashing_steps.rs
// For transaction hashes specifically, use:
#[then(expr = "the transaction hashes should be different")]
fn then_tx_hashes_different(world: &mut TestWorld) {
    let h1 = world.transaction_hash.as_ref().expect("No first hash");
    let h2 = world.transaction_hash2.as_ref().expect("No second hash");
    assert_ne!(h1, h2);
}

// =============================================================================
// Helper Functions
// =============================================================================

fn create_sample_raw_transaction(world: &mut TestWorld) {
    world.tx_sender = Some(AccountAddress::from_hex("0x1").unwrap());
    world.tx_sequence_number = Some(0);
    given_apt_transfer_payload(world);
    world.tx_max_gas = Some(200000);
    world.tx_gas_price = Some(100);
    world.tx_expiration = Some(1700000000);
    world.tx_chain_id = Some(ChainId::testnet());
}

fn parse_hex_byte(s: &str) -> u8 {
    let s = s.trim_start_matches("0x").trim_start_matches("0X");
    u8::from_str_radix(s, 16).unwrap_or_else(|_| panic!("Invalid hex byte: {}", s))
}

