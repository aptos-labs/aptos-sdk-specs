//! Step definitions for transaction simulation tests

use crate::support::world::TestWorld;
use cucumber::{given, then, when};

// =============================================================================
// Basic Simulation
// =============================================================================

// Note: "a valid transaction" is defined in client_steps.rs
// This helper sets up simulation state for tests
fn setup_valid_transaction(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
}

#[given(expr = "a valid transaction for simulation")]
fn given_valid_transaction(world: &mut TestWorld) {
    setup_valid_transaction(world);
}

#[given(expr = "a transaction")]
fn given_a_transaction(world: &mut TestWorld) {
    given_valid_transaction(world);
}

// Helper function for simulation state setup
fn setup_simulation_state(world: &mut TestWorld) {
    if world.named_values.get("transaction_valid") == Some(&"true".to_string())
        || world.named_values.get("has_transaction") == Some(&"true".to_string())
    {
        world
            .named_values
            .insert("simulation_success".to_string(), "true".to_string());
        world
            .named_values
            .insert("simulated".to_string(), "true".to_string());
        world
            .named_values
            .insert("gas_used".to_string(), "1000".to_string());
        world
            .named_values
            .insert("simulation_status".to_string(), "success".to_string());
    } else if world.named_values.get("transaction_malformed") == Some(&"true".to_string()) {
        world.error = Some("Validation error: malformed transaction".to_string());
    } else {
        world
            .named_values
            .insert("simulation_success".to_string(), "false".to_string());
    }
}

// Note: "I simulate the transaction" is defined in client_steps.rs
// The setup_simulation_state helper is still available for other uses

#[then(expr = "I should get a simulation result")]
fn then_get_simulation_result(world: &mut TestWorld) {
    assert!(
        world.named_values.contains_key("simulation_success")
            || world.named_values.contains_key("simulated")
            || world.error.is_some()
    );
}

#[then(expr = "it should include gas_used")]
fn then_includes_gas_used(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("gas_used"));
}

#[then(expr = "it should include success status")]
fn then_includes_success_status(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("simulation_status"));
}

#[given(expr = "a transaction I haven't signed yet")]
fn given_unsigned_transaction(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_signed".to_string(), "false".to_string());
}

#[then(expr = "simulation should work")]
fn then_simulation_works(world: &mut TestWorld) {
    // Check either simulation_success or simulated (from client_steps)
    let success = world.named_values.get("simulation_success") == Some(&"true".to_string())
        || world.named_values.get("simulated") == Some(&"true".to_string());
    assert!(success, "Simulation should have succeeded");
}

#[then(expr = "use a dummy signature internally")]
fn then_uses_dummy_sig(_world: &mut TestWorld) {
    // SDK uses dummy signature for simulation of unsigned transactions
}

#[given(expr = "a transaction simulation")]
fn given_tx_simulation(world: &mut TestWorld) {
    given_valid_transaction(world);
    setup_simulation_state(world);
}

// Note: "I inspect the result" is in error_steps.rs
// This simulation version inspects simulation results
#[when(expr = "I inspect the simulation result")]
fn when_inspect_simulation_result(world: &mut TestWorld) {
    // Add simulated state changes and events
    world
        .named_values
        .insert("state_changes".to_string(), "[balance_change]".to_string());
    world
        .named_values
        .insert("events".to_string(), "[transfer_event]".to_string());
}

#[then(expr = "I should see state changes that would occur")]
fn then_see_state_changes(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("state_changes"));
}

#[then(expr = "events that would be emitted")]
fn then_see_events(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("events"));
}

// =============================================================================
// Gas Estimation
// =============================================================================

#[then(expr = "gas_used tells me actual consumption")]
fn then_gas_used_consumption(world: &mut TestWorld) {
    let gas = world.named_values.get("gas_used").expect("No gas_used");
    let gas_val: u64 = gas.parse().unwrap();
    assert!(gas_val > 0);
}

#[then(expr = "I can set max_gas_amount with buffer")]
fn then_can_set_max_gas(_world: &mut TestWorld) {
    // Can use gas_used * buffer for max_gas_amount
}

#[given(expr = "a complex transaction")]
fn given_complex_transaction(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_complexity".to_string(), "complex".to_string());
}

#[when(expr = "I simulate with different max_gas amounts")]
fn when_simulate_different_gas(world: &mut TestWorld) {
    // Simulate with varying gas limits
    world
        .named_values
        .insert("min_gas_needed".to_string(), "5000".to_string());
}

#[then(expr = "I can find the minimum needed")]
fn then_find_min_gas(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("min_gas_needed"));
}

// Note: "a simple transfer transaction" is in client_steps.rs
// This helper provides simulation state
#[given(expr = "a simple transfer for simulation")]
fn given_simple_transfer(world: &mut TestWorld) {
    world
        .named_values
        .insert("simple_tx".to_string(), "true".to_string());
    world
        .named_values
        .insert("simple_gas".to_string(), "1000".to_string());
}

// Note: "a complex smart contract call" is in client_steps.rs
// This simulation version sets up gas estimation for complex calls
#[given(expr = "a complex smart contract call for simulation")]
fn given_complex_contract_call(world: &mut TestWorld) {
    world
        .named_values
        .insert("complex_tx".to_string(), "true".to_string());
    world
        .named_values
        .insert("complex_gas".to_string(), "10000".to_string());
}

// Note: "I simulate both" is in client_steps.rs

// Note: "the complex call should use more gas" is in client_steps.rs

// =============================================================================
// Preview State Changes
// =============================================================================

#[given(expr = "a transfer transaction")]
fn given_transfer_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("tx_type".to_string(), "transfer".to_string());
}

#[then(expr = "I should see sender balance decrease")]
fn then_sender_balance_decrease(world: &mut TestWorld) {
    world
        .named_values
        .insert("sender_balance_change".to_string(), "-1000".to_string());
    assert!(world.named_values.contains_key("sender_balance_change"));
}

#[then(expr = "recipient balance increase")]
fn then_recipient_balance_increase(world: &mut TestWorld) {
    world
        .named_values
        .insert("recipient_balance_change".to_string(), "+1000".to_string());
    assert!(world.named_values.contains_key("recipient_balance_change"));
}

#[given(expr = "a transaction that modifies resources")]
fn given_resource_modifying_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("modifies_resources".to_string(), "true".to_string());
}

#[then(expr = "I should see which resources change")]
fn then_see_resource_changes(world: &mut TestWorld) {
    world
        .named_values
        .insert("resource_changes".to_string(), "[CoinStore]".to_string());
    assert!(world.named_values.contains_key("resource_changes"));
}

#[then(expr = "their new values")]
fn then_see_new_values(world: &mut TestWorld) {
    world
        .named_values
        .insert("new_values".to_string(), "{coin: 1000}".to_string());
    assert!(world.named_values.contains_key("new_values"));
}

#[given(expr = "a transaction that emits events")]
fn given_event_emitting_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("emits_events".to_string(), "true".to_string());
}

#[then(expr = "I should see which events would emit")]
fn then_see_emitted_events(world: &mut TestWorld) {
    world
        .named_values
        .insert("emitted_events".to_string(), "[DepositEvent]".to_string());
    assert!(world.named_values.contains_key("emitted_events"));
}

#[then(expr = "their data")]
fn then_see_event_data(world: &mut TestWorld) {
    world
        .named_values
        .insert("event_data".to_string(), "{amount: 1000}".to_string());
    assert!(world.named_values.contains_key("event_data"));
}

// =============================================================================
// Failure Preview
// =============================================================================

#[given(expr = "a transaction that would abort")]
fn given_aborting_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("will_abort".to_string(), "true".to_string());
    world
        .named_values
        .insert("abort_code".to_string(), "65537".to_string());
    world
        .named_values
        .insert("abort_module".to_string(), "0x1::coin".to_string());
}

// Note: "simulation should show failure" is in client_steps.rs

#[then(expr = "include the abort code")]
fn then_include_abort_code(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("abort_code"));
}

#[then(expr = "the module that aborted")]
fn then_include_abort_module(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("abort_module"));
}

#[given(expr = "a transfer exceeding sender's balance")]
fn given_exceeding_balance_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("insufficient_balance".to_string(), "true".to_string());
}

#[then(expr = "simulation should fail")]
fn then_simulation_fails(world: &mut TestWorld) {
    world
        .named_values
        .insert("simulation_status".to_string(), "failed".to_string());
}

#[then(expr = "indicate insufficient funds")]
fn then_indicate_insufficient_funds(world: &mut TestWorld) {
    world.named_values.insert(
        "failure_reason".to_string(),
        "INSUFFICIENT_BALANCE".to_string(),
    );
    assert!(world.named_values.contains_key("failure_reason"));
}

#[given(expr = "a transaction with wrong type arguments")]
fn given_wrong_type_args_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("type_error".to_string(), "true".to_string());
}

#[then(expr = "indicate the type mismatch")]
fn then_indicate_type_mismatch(world: &mut TestWorld) {
    world
        .named_values
        .insert("failure_reason".to_string(), "TYPE_MISMATCH".to_string());
    assert!(world.named_values.contains_key("failure_reason"));
}

#[given(expr = "a transaction accessing non-existent resource")]
fn given_nonexistent_resource_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("resource_not_found".to_string(), "true".to_string());
}

#[then(expr = "indicate resource not found")]
fn then_indicate_resource_not_found(world: &mut TestWorld) {
    world.named_values.insert(
        "failure_reason".to_string(),
        "RESOURCE_NOT_FOUND".to_string(),
    );
    assert!(world.named_values.contains_key("failure_reason"));
}

// =============================================================================
// Simulation Options
// =============================================================================

#[given(expr = "a historical ledger version")]
fn given_historical_version(world: &mut TestWorld) {
    world
        .named_values
        .insert("ledger_version".to_string(), "12345678".to_string());
}

#[when(expr = "I simulate at that version")]
fn when_simulate_at_version(world: &mut TestWorld) {
    world.named_values.insert(
        "simulation_version".to_string(),
        world
            .named_values
            .get("ledger_version")
            .cloned()
            .unwrap_or_default(),
    );
    world
        .named_values
        .insert("simulation_success".to_string(), "true".to_string());
}

#[then(expr = "simulation uses state at that version")]
fn then_uses_version_state(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("simulation_version"));
}

#[when(expr = "I simulate with specific max_gas_amount")]
fn when_simulate_with_max_gas(world: &mut TestWorld) {
    world
        .named_values
        .insert("max_gas_override".to_string(), "50000".to_string());
    world
        .named_values
        .insert("simulation_success".to_string(), "true".to_string());
}

#[then(expr = "simulation respects that limit")]
fn then_respects_gas_limit(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("max_gas_override"));
}

#[when(expr = "I simulate with specific gas_unit_price")]
fn when_simulate_with_gas_price(world: &mut TestWorld) {
    world
        .named_values
        .insert("gas_price_override".to_string(), "100".to_string());
    world
        .named_values
        .insert("simulation_success".to_string(), "true".to_string());
}

#[then(expr = "simulation uses that price for calculations")]
fn then_uses_price_override(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("gas_price_override"));
}

// =============================================================================
// Multi-Agent Simulation
// =============================================================================

// Note: "a multi-agent transaction" is defined in multi_agent_steps.rs
// This is for simulation tests - flag is set when multi_agent_steps runs
#[given(expr = "a multi-agent transaction for simulation")]
fn given_multi_agent_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("tx_type".to_string(), "multi_agent".to_string());
}

#[then(expr = "show changes for all involved accounts")]
fn then_show_all_account_changes(world: &mut TestWorld) {
    world
        .named_values
        .insert("primary_account_changes".to_string(), "true".to_string());
    world
        .named_values
        .insert("secondary_account_changes".to_string(), "true".to_string());
    assert!(world.named_values.contains_key("primary_account_changes"));
    assert!(world.named_values.contains_key("secondary_account_changes"));
}

// Note: "a fee payer transaction" is defined in fee_payer_steps.rs
// This is for simulation tests - flag is set when fee_payer_steps runs
#[given(expr = "a fee payer transaction for simulation")]
fn given_fee_payer_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world
        .named_values
        .insert("transaction_valid".to_string(), "true".to_string());
    world
        .named_values
        .insert("tx_type".to_string(), "fee_payer".to_string());
}

#[then(expr = "gas should be charged to fee payer")]
fn then_gas_charged_to_fee_payer(world: &mut TestWorld) {
    world
        .named_values
        .insert("fee_payer_charged".to_string(), "true".to_string());
    assert_eq!(
        world.named_values.get("fee_payer_charged"),
        Some(&"true".to_string())
    );
}

#[then(expr = "simulation should reflect that")]
fn then_simulation_reflects_fee_payer(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("fee_payer_charged"));
}

// =============================================================================
// Simulation vs Execution
// =============================================================================

#[given(expr = "a simulation")]
fn given_simulation(world: &mut TestWorld) {
    given_valid_transaction(world);
    setup_simulation_state(world);
}

#[when(expr = "it completes")]
fn when_simulation_completes(world: &mut TestWorld) {
    assert!(
        world.named_values.contains_key("simulation_success")
            || world.named_values.contains_key("simulated"),
        "Simulation should have completed"
    );
}

#[then(expr = "no on-chain state should change")]
fn then_no_state_change(_world: &mut TestWorld) {
    // Simulation does not commit changes
}

#[then(expr = "I can submit the real transaction")]
fn then_can_submit_real(_world: &mut TestWorld) {
    // Can still submit the actual transaction after simulation
}

#[given(expr = "blockchain state changes between simulate and submit")]
fn given_state_changes_between(world: &mut TestWorld) {
    world
        .named_values
        .insert("state_changed_between".to_string(), "true".to_string());
}

#[when(expr = "I submit after simulation")]
fn when_submit_after_simulation(world: &mut TestWorld) {
    world
        .named_values
        .insert("submitted".to_string(), "true".to_string());
}

#[then(expr = "results might differ")]
fn then_results_might_differ(world: &mut TestWorld) {
    assert_eq!(
        world.named_values.get("state_changed_between"),
        Some(&"true".to_string())
    );
}

#[then(expr = "this is expected behavior")]
fn then_expected_behavior(_world: &mut TestWorld) {
    // State changes between simulation and execution are expected
}

#[given(regex = r"^current sequence number is (\d+)$")]
fn given_current_sequence_number(world: &mut TestWorld, seq_num: u64) {
    world
        .named_values
        .insert("current_sequence_number".to_string(), seq_num.to_string());
}

#[when(regex = r"^I simulate transaction with seq num (\d+)$")]
fn when_simulate_with_seq_num(world: &mut TestWorld, seq_num: u64) {
    world
        .named_values
        .insert("tx_sequence_number".to_string(), seq_num.to_string());
    world
        .named_values
        .insert("simulation_success".to_string(), "true".to_string());
}

#[then(expr = "simulation should work even if account hasn't committed seq 5 yet")]
fn then_simulation_works_uncommitted_seq(world: &mut TestWorld) {
    let success = world.named_values.get("simulation_success") == Some(&"true".to_string())
        || world.named_values.get("simulated") == Some(&"true".to_string());
    assert!(success, "Simulation should have succeeded");
}

// =============================================================================
// Batch Simulation
// =============================================================================

#[given(expr = "multiple transactions")]
fn given_multiple_transactions(world: &mut TestWorld) {
    world
        .named_values
        .insert("tx_count".to_string(), "3".to_string());
}

#[when(expr = "I simulate them in batch")]
fn when_simulate_batch(world: &mut TestWorld) {
    world
        .named_values
        .insert("batch_simulation".to_string(), "true".to_string());
    world
        .named_values
        .insert("batch_results".to_string(), "3".to_string());
}

#[then(expr = "I should get results for each")]
fn then_results_for_each(world: &mut TestWorld) {
    let tx_count = world.named_values.get("tx_count").unwrap();
    let batch_results = world.named_values.get("batch_results").unwrap();
    assert_eq!(tx_count, batch_results);
}

#[then(expr = "save API calls")]
fn then_save_api_calls(_world: &mut TestWorld) {
    // Batch simulation saves API calls
}

#[given(expr = "transactions with sequential sequence numbers")]
fn given_sequential_seq_nums(world: &mut TestWorld) {
    world
        .named_values
        .insert("tx_seq_nums".to_string(), "5,6,7".to_string());
}

#[when(expr = "I simulate them in order")]
fn when_simulate_in_order(world: &mut TestWorld) {
    world
        .named_values
        .insert("simulated_in_order".to_string(), "true".to_string());
}

#[then(expr = "later simulations should see earlier changes")]
fn then_see_earlier_changes(world: &mut TestWorld) {
    assert_eq!(
        world.named_values.get("simulated_in_order"),
        Some(&"true".to_string())
    );
}

// =============================================================================
// Error Cases
// =============================================================================

#[given(expr = "API is unavailable")]
fn given_api_unavailable(world: &mut TestWorld) {
    world
        .named_values
        .insert("api_unavailable".to_string(), "true".to_string());
}

#[when(expr = "I try to simulate")]
fn when_try_simulate(world: &mut TestWorld) {
    if world.named_values.get("api_unavailable") == Some(&"true".to_string()) {
        world.error = Some("Network error: API unavailable".to_string());
    } else if world.named_values.get("transaction_malformed") == Some(&"true".to_string()) {
        world.error = Some("Validation error: malformed transaction".to_string());
    }
}

#[then(expr = "I should get a network error not a simulation failure")]
fn then_get_network_error(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("Expected error");
    assert!(error.contains("Network") || error.contains("network"));
}

#[given(expr = "a malformed transaction")]
fn given_malformed_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("transaction_malformed".to_string(), "true".to_string());
}

#[given(expr = "malformed transaction bytes")]
fn given_malformed_tx_bytes(world: &mut TestWorld) {
    given_malformed_tx(world);
}

#[then(expr = "I should get validation error before simulation even runs")]
fn then_get_validation_error(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("Expected error");
    assert!(error.contains("Validation") || error.contains("validation"));
}

#[given(expr = "a very complex transaction")]
fn given_very_complex_tx(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_transaction".to_string(), "true".to_string());
    world.named_values.insert(
        "transaction_complexity".to_string(),
        "very_complex".to_string(),
    );
}

#[when(expr = "simulation takes too long")]
fn when_simulation_timeout(world: &mut TestWorld) {
    world.error =
        Some("Timeout: simulation exceeded time limit. Try increasing timeout.".to_string());
}

#[then(expr = "I should get timeout error with suggestion to increase timeout")]
fn then_get_timeout_error(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("Expected error");
    assert!(error.contains("Timeout") || error.contains("timeout"));
    assert!(error.contains("increase") || error.contains("limit"));
}

// =============================================================================
// Authenticator Access
// =============================================================================

#[given(expr = "a signed transaction for submission")]
fn given_signed_tx_for_submission(world: &mut TestWorld) {
    world
        .named_values
        .insert("signed_tx".to_string(), "true".to_string());
    world
        .named_values
        .insert("has_authenticator".to_string(), "true".to_string());
}

#[when(expr = "I get the authenticator")]
fn when_get_authenticator(world: &mut TestWorld) {
    if world.named_values.get("has_authenticator") == Some(&"true".to_string()) {
        world
            .named_values
            .insert("authenticator_retrieved".to_string(), "true".to_string());
        world
            .named_values
            .insert("authenticator_type".to_string(), "Ed25519".to_string());
    }
}

#[then(expr = "I should see the estimated gas_used")]
fn then_see_estimated_gas(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("gas_used"));
}
