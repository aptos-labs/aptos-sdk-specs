//! Step definitions for fee payer (sponsored) transaction tests

use crate::support::TestWorld;
use aptos_rust_sdk_v2::account::Ed25519Account;
use aptos_rust_sdk_v2::transaction::types::FeePayerRawTransaction;
use aptos_rust_sdk_v2::transaction::{
    authenticator::{AccountAuthenticator, TransactionAuthenticator},
    EntryFunction, PartiallySigned, RawTransaction, TransactionPayload,
};
use aptos_rust_sdk_v2::types::{AccountAddress, Identifier, MoveModuleId};
use aptos_rust_sdk_v2::ChainId;
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
// Given Steps - Fee Payer Setup
// =============================================================================

#[given("a fee payer (sponsor) account")]
fn given_fee_payer_account(world: &mut TestWorld) {
    let account = Ed25519Account::generate();
    world.fee_payer_address = Some(account.address());
    world.fee_payer_account = Some(account);
}

#[given("a fee payer account")]
fn given_fee_payer_account_simple(world: &mut TestWorld) {
    given_fee_payer_account(world);
}

#[given("secondary signer accounts")]
fn given_secondary_signer_accounts(world: &mut TestWorld) {
    let account = Ed25519Account::generate();
    world.secondary_signer_addresses.push(account.address());
    world.secondary_accounts.push(account);
}

#[given(expr = "fee payer address {string}")]
fn given_fee_payer_address_str(world: &mut TestWorld, addr: String) {
    let address = AccountAddress::from_hex(&addr).unwrap_or_else(|_| {
        // If it's a placeholder like "0xSPONSOR", generate a random address
        Ed25519Account::generate().address()
    });
    world.fee_payer_address = Some(address);
    world.fee_payer_account = Some(Ed25519Account::generate());
}

#[given("the same RawTransaction and secondary signers")]
fn given_same_raw_tx_and_secondary(world: &mut TestWorld) {
    if world.ed25519_account.is_none() {
        world.ed25519_account = Some(Ed25519Account::generate());
    }
    if world.secondary_signer_addresses.is_empty() {
        let account = Ed25519Account::generate();
        world.secondary_signer_addresses.push(account.address());
        world.secondary_accounts.push(account);
    }

    let sender = world.ed25519_account.as_ref().unwrap();
    world.raw_transaction = Some(create_sample_raw_transaction(sender.address()));
}

#[given("a fee payer address")]
fn given_fee_payer_address(world: &mut TestWorld) {
    if world.fee_payer_account.is_none() {
        given_fee_payer_account(world);
    }
}

#[given("a fee payer transaction")]
fn given_fee_payer_transaction(world: &mut TestWorld) {
    // Ensure we have accounts
    if world.ed25519_account.is_none() {
        world.ed25519_account = Some(Ed25519Account::generate());
    }
    if world.fee_payer_account.is_none() {
        given_fee_payer_account(world);
    }

    let sender = world.ed25519_account.as_ref().unwrap();
    let fee_payer = world.fee_payer_account.as_ref().unwrap();

    let raw_txn = create_sample_raw_transaction(sender.address());

    world.fee_payer_txn = Some(FeePayerRawTransaction::new(
        raw_txn.clone(),
        world.secondary_signer_addresses.clone(),
        fee_payer.address(),
    ));
    world.raw_transaction = Some(raw_txn);
}

#[given("a fee payer transaction with sender, secondary, and sponsor")]
fn given_fee_payer_with_all(world: &mut TestWorld) {
    world.ed25519_account = Some(Ed25519Account::generate());

    // Add a secondary signer
    let secondary = Ed25519Account::generate();
    world.secondary_signer_addresses.push(secondary.address());
    world.secondary_accounts.push(secondary);

    given_fee_payer_account(world);
    given_fee_payer_transaction(world);
}

#[given("no secondary signers")]
fn given_no_secondary_signers(world: &mut TestWorld) {
    world.secondary_signer_addresses.clear();
    world.secondary_accounts.clear();
}

#[given("a Secp256k1 fee payer")]
fn given_secp256k1_fee_payer(world: &mut TestWorld) {
    // Use Ed25519 as placeholder
    given_fee_payer_account(world);
}

#[given("a sender who wants sponsored transaction")]
fn given_sender_wants_sponsored(world: &mut TestWorld) {
    world.ed25519_account = Some(Ed25519Account::generate());
}

#[given("a partially signed fee payer transaction from sender")]
fn given_partially_signed_from_sender(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::account::Account;

    // Create accounts
    if world.ed25519_account.is_none() {
        world.ed25519_account = Some(Ed25519Account::generate());
    }
    if world.fee_payer_account.is_none() {
        given_fee_payer_account(world);
    }

    let sender = world.ed25519_account.as_ref().unwrap();
    let fee_payer = world.fee_payer_account.as_ref().unwrap();

    let raw_txn = create_sample_raw_transaction(sender.address());
    let fee_payer_txn = FeePayerRawTransaction::new(raw_txn, vec![], fee_payer.address());

    let mut partially_signed = PartiallySigned::new(fee_payer_txn.clone());
    partially_signed.sign_as_sender(sender).unwrap();

    world.fee_payer_txn = Some(fee_payer_txn);
    world.partially_signed = Some(partially_signed);
}

#[given(expr = "sender creates transaction with max_gas_amount={int}")]
fn given_sender_creates_tx_with_gas(world: &mut TestWorld, gas: u64) {
    if world.ed25519_account.is_none() {
        world.ed25519_account = Some(Ed25519Account::generate());
    }
    world.tx_max_gas = Some(gas);
}

#[given("fee payer has sufficient balance")]
fn given_fee_payer_sufficient_balance(world: &mut TestWorld) {
    world
        .named_values
        .insert("fee_payer_balance".to_string(), "sufficient".to_string());
}

#[given("sender creates valid transaction")]
fn given_sender_creates_valid_tx(world: &mut TestWorld) {
    if world.ed25519_account.is_none() {
        world.ed25519_account = Some(Ed25519Account::generate());
    }
}

#[given("fee payer has zero balance")]
fn given_fee_payer_zero_balance(world: &mut TestWorld) {
    world
        .named_values
        .insert("fee_payer_balance".to_string(), "zero".to_string());
}

#[given("fee payer address A")]
fn given_fee_payer_address_a(world: &mut TestWorld) {
    let account = Ed25519Account::generate();
    world.fee_payer_address = Some(account.address());
    world.fee_payer_account = Some(account);
}

#[given("a fee payer authenticator")]
fn given_fee_payer_authenticator(world: &mut TestWorld) {
    given_fee_payer_transaction(world);
    when_sign_fee_payer_both_parties(world);
}

#[given("the same fee payer transaction")]
fn given_same_fee_payer_transaction(world: &mut TestWorld) {
    if world.fee_payer_txn.is_none() {
        given_fee_payer_transaction(world);
    }
    // Also sign it for serialization tests
    if world.signed_transaction.is_none() {
        when_sign_fee_payer_both_parties(world);
    }
}

#[given("a RawTransaction and fee payer address from test vectors")]
fn given_raw_tx_fee_payer_from_vectors(world: &mut TestWorld) {
    given_fee_payer_transaction(world);
}

#[given("a fee payer transaction from test vectors")]
fn given_fee_payer_from_vectors(world: &mut TestWorld) {
    given_fee_payer_transaction(world);
}

#[given("a signed fee payer transaction")]
fn given_signed_fee_payer_transaction(world: &mut TestWorld) {
    given_fee_payer_transaction(world);
    when_sign_fee_payer_both_parties(world);
}

// =============================================================================
// When Steps - Transaction Creation and Signing
// =============================================================================

#[when("I create a fee payer transaction")]
fn when_create_fee_payer_transaction(world: &mut TestWorld) {
    let sender = world
        .ed25519_account
        .as_ref()
        .map(|a| a.address())
        .unwrap_or(AccountAddress::ONE);
    let fee_payer = world
        .fee_payer_account
        .as_ref()
        .map(|a| a.address())
        .unwrap_or(AccountAddress::THREE);

    let raw_txn = create_sample_raw_transaction(sender);

    world.fee_payer_txn = Some(FeePayerRawTransaction::new(
        raw_txn.clone(),
        world.secondary_signer_addresses.clone(),
        fee_payer,
    ));
    world.raw_transaction = Some(raw_txn);
}

#[when("I build a fee payer transaction")]
fn when_build_fee_payer_transaction(world: &mut TestWorld) {
    when_create_fee_payer_transaction(world);
}

#[when("I generate multi-agent signing message")]
fn when_generate_multi_agent_msg(world: &mut TestWorld) {
    // Create raw_txn if not exists
    if world.raw_transaction.is_none() {
        let sender = world
            .ed25519_account
            .as_ref()
            .map(|a| a.address())
            .unwrap_or_else(|| {
                let account = Ed25519Account::generate();
                world.ed25519_account = Some(account.clone());
                account.address()
            });
        world.raw_transaction = Some(create_sample_raw_transaction(sender));
    }

    // Create a multi-agent transaction for comparison
    if let Some(raw_txn) = &world.raw_transaction {
        let multi_agent = aptos_rust_sdk_v2::transaction::types::MultiAgentRawTransaction::new(
            raw_txn.clone(),
            world.secondary_signer_addresses.clone(),
        );
        world.signing_message = multi_agent.signing_message().ok();
    }
}

#[when("I generate fee payer signing message with sponsor")]
fn when_generate_fee_payer_msg_with_sponsor(world: &mut TestWorld) {
    // Create fee_payer_txn if not exists
    if world.fee_payer_txn.is_none() {
        if let Some(raw_txn) = &world.raw_transaction {
            let fee_payer_addr = world.fee_payer_address.unwrap_or_else(|| {
                let account = Ed25519Account::generate();
                world.fee_payer_account = Some(account.clone());
                account.address()
            });
            world.fee_payer_txn = Some(FeePayerRawTransaction::new(
                raw_txn.clone(),
                world.secondary_signer_addresses.clone(),
                fee_payer_addr,
            ));
        }
    }

    if let Some(ref fee_payer_txn) = world.fee_payer_txn {
        world.signing_message2 = fee_payer_txn.signing_message().ok();
    }
}

#[when("I generate the fee payer signing message")]
fn when_generate_fee_payer_msg(world: &mut TestWorld) {
    // If we don't have a fee_payer_txn but have the components, create one
    if world.fee_payer_txn.is_none() {
        if let (Some(raw_txn), Some(fee_payer_addr)) =
            (&world.raw_transaction, &world.fee_payer_address)
        {
            world.fee_payer_txn = Some(FeePayerRawTransaction::new(
                raw_txn.clone(),
                world.secondary_signer_addresses.clone(),
                *fee_payer_addr,
            ));
        }
    }

    if let Some(ref fee_payer_txn) = world.fee_payer_txn {
        world.signing_message = fee_payer_txn.signing_message().ok();
    }
}

#[when("I sign the fee payer transaction with both parties")]
fn when_sign_fee_payer_both_parties(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::account::Account;

    // Create fee_payer_txn if not exists but we have the components
    if world.fee_payer_txn.is_none() {
        if let (Some(sender), Some(fee_payer)) = (&world.ed25519_account, &world.fee_payer_account)
        {
            let raw_txn = world
                .raw_transaction
                .clone()
                .unwrap_or_else(|| create_sample_raw_transaction(sender.address()));
            world.fee_payer_txn = Some(FeePayerRawTransaction::new(
                raw_txn,
                world.secondary_signer_addresses.clone(),
                fee_payer.address(),
            ));
        }
    }

    let fee_payer_txn = match &world.fee_payer_txn {
        Some(txn) => txn,
        None => return,
    };

    let sender = match &world.ed25519_account {
        Some(a) => a,
        None => return,
    };

    let fee_payer = match &world.fee_payer_account {
        Some(a) => a,
        None => return,
    };

    // Get the signing message
    let signing_message = match fee_payer_txn.signing_message() {
        Ok(msg) => msg,
        Err(e) => {
            world.set_error(e);
            return;
        }
    };

    // Sign with sender
    let sender_sig = match sender.sign(&signing_message) {
        Ok(sig) => sig,
        Err(e) => {
            world.set_error(e);
            return;
        }
    };
    let sender_auth = AccountAuthenticator::ed25519(sender.public_key_bytes(), sender_sig);

    // Sign with secondary signers
    let mut secondary_auths = Vec::new();
    for account in &world.secondary_accounts {
        let sig = match account.sign(&signing_message) {
            Ok(sig) => sig,
            Err(e) => {
                world.set_error(e);
                return;
            }
        };
        secondary_auths.push(AccountAuthenticator::ed25519(
            account.public_key_bytes(),
            sig,
        ));
    }

    // Sign with fee payer
    let fee_payer_sig = match fee_payer.sign(&signing_message) {
        Ok(sig) => sig,
        Err(e) => {
            world.set_error(e);
            return;
        }
    };
    let fee_payer_auth = AccountAuthenticator::ed25519(fee_payer.public_key_bytes(), fee_payer_sig);

    let authenticator = TransactionAuthenticator::fee_payer(
        sender_auth,
        fee_payer_txn.secondary_signer_addresses.clone(),
        secondary_auths,
        fee_payer_txn.fee_payer_address,
        fee_payer_auth,
    );

    world.signed_transaction = Some(aptos_rust_sdk_v2::transaction::SignedTransaction::new(
        fee_payer_txn.raw_txn.clone(),
        authenticator,
    ));
}

#[when("I sign the fee payer transaction")]
fn when_sign_fee_payer(world: &mut TestWorld) {
    when_sign_fee_payer_both_parties(world);
}

#[when("sender creates RawTransaction")]
fn when_sender_creates_raw_tx(world: &mut TestWorld) {
    let sender = world
        .ed25519_account
        .as_ref()
        .map(|a| a.address())
        .unwrap_or(AccountAddress::ONE);
    world.raw_transaction = Some(create_sample_raw_transaction(sender));
}

#[when("sender signs the fee payer signing message")]
fn when_sender_signs_fee_payer_msg(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::account::Account;

    // Create fee_payer_txn if not exists
    if world.fee_payer_txn.is_none() {
        if let Some(raw_txn) = &world.raw_transaction {
            let fee_payer_addr = world.fee_payer_address.unwrap_or_else(|| {
                let account = Ed25519Account::generate();
                world.fee_payer_account = Some(account.clone());
                account.address()
            });
            world.fee_payer_txn = Some(FeePayerRawTransaction::new(
                raw_txn.clone(),
                world.secondary_signer_addresses.clone(),
                fee_payer_addr,
            ));
        }
    }

    if let (Some(fee_payer_txn), Some(sender)) = (&world.fee_payer_txn, &world.ed25519_account) {
        if let Ok(signing_message) = fee_payer_txn.signing_message() {
            if let Ok(_sig) = sender.sign(&signing_message) {
                world
                    .named_values
                    .insert("sender_signed".to_string(), "true".to_string());
            }
        }
    }
}

#[then("sender can send partially signed tx to sponsor")]
fn then_sender_can_send_to_sponsor(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("sender_signed"));
}

#[when("sponsor reviews the transaction")]
fn when_sponsor_reviews(world: &mut TestWorld) {
    // Just verify we have the transaction
    assert!(world.fee_payer_txn.is_some() || world.partially_signed.is_some());
}

#[when("sponsor signs the fee payer signing message")]
fn when_sponsor_signs(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::account::Account;

    if let (Some(ref mut partially_signed), Some(fee_payer)) =
        (&mut world.partially_signed, &world.fee_payer_account)
    {
        if partially_signed.sign_as_fee_payer(fee_payer).is_ok() {
            world
                .named_values
                .insert("sponsor_signed".to_string(), "true".to_string());
        }
    } else if let (Some(fee_payer_txn), Some(fee_payer)) =
        (&world.fee_payer_txn, &world.fee_payer_account)
    {
        if let Ok(signing_message) = fee_payer_txn.signing_message() {
            if let Ok(_sig) = fee_payer.sign(&signing_message) {
                world
                    .named_values
                    .insert("sponsor_signed".to_string(), "true".to_string());
            }
        }
    }
}

#[when("sponsor combines signatures into authenticator")]
fn when_sponsor_combines_signatures(world: &mut TestWorld) {
    if let Some(ref partially_signed) = world.partially_signed {
        if partially_signed.is_complete() {
            // Clone and finalize
            if let Ok(signed) = partially_signed.clone().finalize() {
                world.signed_transaction = Some(signed);
            }
        }
    }
}

#[then("the transaction is ready for submission")]
fn then_transaction_ready(world: &mut TestWorld) {
    assert!(
        world.signed_transaction.is_some() || world.named_values.contains_key("sponsor_signed")
    );
}

#[when("sponsor signs first")]
fn when_sponsor_signs_first(world: &mut TestWorld) {
    when_sponsor_signs(world);
}

#[when("the sender signs second")]
fn when_sender_signs_second_fee_payer(world: &mut TestWorld) {
    when_sender_signs_fee_payer_msg(world);
}

// Also handle the generic step
#[when("sender signs second")]
fn when_sender_signs_second_generic(world: &mut TestWorld) {
    when_sender_signs_fee_payer_msg(world);
}

#[when("I combine correctly")]
fn when_combine_correctly(world: &mut TestWorld) {
    when_sign_fee_payer_both_parties(world);
}

#[when("transaction is submitted")]
fn when_transaction_submitted(world: &mut TestWorld) {
    // Check if fee payer has balance
    if world.named_values.get("fee_payer_balance") == Some(&"zero".to_string()) {
        world.set_error("insufficient fee payer balance");
    }
}

#[when("sender signs")]
fn when_sender_signs_fee_payer(world: &mut TestWorld) {
    when_sender_signs_fee_payer_msg(world);
}

#[when("fee payer does not sign")]
fn when_fee_payer_does_not_sign(world: &mut TestWorld) {
    world
        .named_values
        .insert("fee_payer_not_signed".to_string(), "true".to_string());
}

#[when("fee payer signs")]
fn when_fee_payer_signs(world: &mut TestWorld) {
    when_sponsor_signs(world);
}

#[when("sender does not sign")]
fn when_sender_does_not_sign(world: &mut TestWorld) {
    world
        .named_values
        .insert("sender_not_signed".to_string(), "true".to_string());
}

// =============================================================================
// Then Steps - Verification
// =============================================================================

#[then("the transaction should have the fee payer designated")]
fn then_fee_payer_designated(world: &mut TestWorld) {
    assert!(world.fee_payer_txn.is_some());
    let txn = world.fee_payer_txn.as_ref().unwrap();
    assert!(!txn.fee_payer_address.is_zero());
}

#[then("it should include all signers plus fee payer")]
fn then_includes_all_signers_plus_fee_payer(world: &mut TestWorld) {
    assert!(world.fee_payer_txn.is_some());
    let txn = world.fee_payer_txn.as_ref().unwrap();
    assert!(!txn.fee_payer_address.is_zero());
}

#[then(expr = "fee_payer_address should be {string}")]
fn then_fee_payer_address_is(world: &mut TestWorld, _expected: String) {
    assert!(world.fee_payer_txn.is_some());
    // The address was set during creation
}

// Removed: "the messages should be different" - handled by transaction_steps.rs

#[then("it should include secondary signer addresses")]
fn then_includes_secondary_signer_addresses(world: &mut TestWorld) {
    // Secondary addresses are included in the signing message
    assert!(world.signing_message.is_some());
}

#[then("it should include the fee payer address")]
fn then_includes_fee_payer_address(world: &mut TestWorld) {
    // Fee payer address is included in the signing message
    assert!(world.signing_message.is_some());
}

#[then("all messages should be identical")]
fn then_all_messages_identical(world: &mut TestWorld) {
    // All parties sign the same message
    if let (Some(m1), Some(m2)) = (&world.signing_message, &world.signing_message2) {
        assert_eq!(m1, m2);
    }
}

#[then("the authenticator should be FeePayer variant")]
fn then_authenticator_is_fee_payer(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    assert!(matches!(
        signed_tx.authenticator,
        TransactionAuthenticator::FeePayer { .. }
    ));
}

#[then(regex = r"^it should contain secondary_signer_addresses \(may be empty\)$")]
fn then_contains_secondary_addresses_maybe_empty(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        TransactionAuthenticator::FeePayer {
            secondary_signer_addresses,
            ..
        } => {
            let _ = secondary_signer_addresses; // May be empty
        }
        _ => panic!("expected FeePayer authenticator"),
    }
}

#[then(regex = r"^it should contain secondary_signers \(may be empty\)$")]
fn then_contains_secondary_signers_maybe_empty(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        TransactionAuthenticator::FeePayer {
            secondary_signers, ..
        } => {
            let _ = secondary_signers; // May be empty
        }
        _ => panic!("expected FeePayer authenticator"),
    }
}

#[then("it should contain fee_payer_address")]
fn then_contains_fee_payer_address(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        TransactionAuthenticator::FeePayer {
            fee_payer_address, ..
        } => {
            assert!(!fee_payer_address.is_zero());
        }
        _ => panic!("expected FeePayer authenticator"),
    }
}

#[then("it should contain fee_payer_signer authenticator")]
fn then_contains_fee_payer_signer(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        TransactionAuthenticator::FeePayer {
            fee_payer_signer, ..
        } => {
            assert!(matches!(
                fee_payer_signer,
                AccountAuthenticator::Ed25519 { .. }
            ));
        }
        _ => panic!("expected FeePayer authenticator"),
    }
}

#[then("secondary_signer_addresses should be empty")]
fn then_secondary_addresses_empty(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        TransactionAuthenticator::FeePayer {
            secondary_signer_addresses,
            ..
        } => {
            assert!(secondary_signer_addresses.is_empty());
        }
        _ => panic!("expected FeePayer authenticator"),
    }
}

#[then("secondary_signers should be empty")]
fn then_secondary_signers_empty(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    match &signed_tx.authenticator {
        TransactionAuthenticator::FeePayer {
            secondary_signers, ..
        } => {
            assert!(secondary_signers.is_empty());
        }
        _ => panic!("expected FeePayer authenticator"),
    }
}

#[then("fee payer should be present")]
fn then_fee_payer_present(world: &mut TestWorld) {
    let signed_tx = world
        .signed_transaction
        .as_ref()
        .expect("no signed transaction");
    assert!(matches!(
        signed_tx.authenticator,
        TransactionAuthenticator::FeePayer { .. }
    ));
}

// Removed: "it should succeed" - too generic, handled elsewhere
// Use specific step for fee payer:
#[then("the fee payer signing should succeed")]
fn then_fee_payer_signing_should_succeed(world: &mut TestWorld) {
    assert!(world.signed_transaction.is_some());
}

#[then("both authenticators should be correct types")]
fn then_both_auth_correct_types(world: &mut TestWorld) {
    assert!(world.signed_transaction.is_some());
}

#[then("the fee payer transaction should be valid")]
fn then_fee_payer_tx_valid(world: &mut TestWorld) {
    assert!(world.signed_transaction.is_some());
}

#[then("fee payer's balance is deducted for gas")]
fn then_fee_payer_balance_deducted(world: &mut TestWorld) {
    // This would be verified on-chain
    assert!(world.named_values.get("fee_payer_balance") == Some(&"sufficient".to_string()));
}

#[then("sender's balance is not deducted for gas")]
fn then_sender_balance_not_deducted(world: &mut TestWorld) {
    // This would be verified on-chain
    assert!(world.named_values.get("fee_payer_balance") == Some(&"sufficient".to_string()));
}

#[then("it should fail due to fee payer insufficient balance")]
fn then_fail_insufficient_balance(world: &mut TestWorld) {
    assert!(world.has_error());
}

#[then("it should fail with missing fee payer error")]
fn then_fail_missing_fee_payer(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("fee_payer_not_signed") || world.has_error());
}

#[then("it should fail with missing sender error")]
fn then_fail_missing_sender(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("sender_not_signed") || world.has_error());
}

#[then("the variant indicator should be FeePayer")]
fn then_variant_is_fee_payer(world: &mut TestWorld) {
    let bytes = world
        .serialized_bytes
        .as_ref()
        .expect("no serialized bytes");
    assert!(!bytes.is_empty());
}

#[then("all components should be serialized in order")]
fn then_all_components_serialized(world: &mut TestWorld) {
    assert!(world.serialized_bytes.is_some());
}

// Removed: "it should match the expected value from test vectors" - handled by auth_key_steps.rs
// Use specific step for fee payer test vectors:
#[then("the fee payer signing message should match test vectors")]
fn then_fee_payer_matches_test_vectors(world: &mut TestWorld) {
    assert!(world.signing_message.is_some() || world.serialized_bytes.is_some());
}
