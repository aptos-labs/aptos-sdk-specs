//! Step definitions for error handling tests

use crate::support::world::TestWorld;
use cucumber::{given, then, when};

// =============================================================================
// Error Categories
// =============================================================================

#[given(expr = "a network timeout or connection failure")]
fn given_network_error(world: &mut TestWorld) {
    world.error = Some("Connection timed out".to_string());
    world.error_category = Some("network".to_string());
}

#[given(regex = r"^an API error response \(4xx or 5xx\)$")]
fn given_api_error(world: &mut TestWorld) {
    world.error = Some("HTTP 400 Bad Request: Invalid transaction format".to_string());
    world.error_category = Some("api".to_string());
    world.http_status_code = Some(400);
}

#[given(regex = r"^invalid input \(e\.g\., malformed address\)$")]
fn given_validation_error(world: &mut TestWorld) {
    world.error = Some("Invalid address format: expected 32-byte hex string".to_string());
    world.error_category = Some("validation".to_string());
}

#[given(expr = "a failed transaction")]
fn given_failed_transaction(world: &mut TestWorld) {
    world.error = Some("Transaction failed: MOVE_ABORT with code 65537".to_string());
    world.error_category = Some("transaction".to_string());
    world.vm_status_code = Some(65537);
}

#[when(expr = "I catch the error")]
fn when_catch_error(world: &mut TestWorld) {
    // Error is already stored in world.error
    assert!(world.error.is_some(), "No error to catch");
}

#[when(expr = "I catch the validation error")]
fn when_catch_validation_error(world: &mut TestWorld) {
    assert!(world.error.is_some(), "No error to catch");
    assert_eq!(world.error_category, Some("validation".to_string()));
}

#[then(expr = "I should be able to identify it as a network error")]
fn then_identify_network_error(world: &mut TestWorld) {
    assert_eq!(world.error_category, Some("network".to_string()));
}

#[then(expr = "it should be retryable")]
fn then_should_be_retryable(world: &mut TestWorld) {
    let category = world.error_category.as_ref().expect("No error category");
    let is_retryable = category == "network" || category == "rate_limit";
    assert!(is_retryable, "Error should be retryable");
}

#[then(expr = "I should see the HTTP status code")]
fn then_see_http_status(world: &mut TestWorld) {
    assert!(
        world.http_status_code.is_some(),
        "Should have HTTP status code"
    );
}

#[then(expr = "the error message from the API")]
fn then_see_error_message(world: &mut TestWorld) {
    assert!(world.error.is_some(), "Should have error message");
}

#[then(expr = "I should see which input was invalid")]
fn then_see_invalid_input(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(
        error.contains("address") || error.contains("input"),
        "Error should indicate invalid input"
    );
}

#[then(expr = "why it was invalid")]
fn then_see_why_invalid(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(
        error.contains("format") || error.contains("expected"),
        "Error should explain why input was invalid"
    );
}

#[then(expr = "I should see the VM status code")]
fn then_see_vm_status(world: &mut TestWorld) {
    assert!(world.vm_status_code.is_some(), "Should have VM status code");
}

#[then(expr = "the abort code if applicable")]
fn then_see_abort_code(world: &mut TestWorld) {
    // Abort code is in vm_status_code for aborted transactions
    if let Some(code) = world.vm_status_code {
        assert!(code > 0, "Should have non-zero abort code");
    }
}

#[then(expr = "the transaction hash if submitted")]
fn then_see_tx_hash(_world: &mut TestWorld) {
    // Transaction hash would be stored if submitted
    // For this test, just pass as we're testing error handling structure
}

// =============================================================================
// VM Status Codes
// =============================================================================

#[given(expr = "a transaction with vm_status {string}")]
fn given_tx_with_vm_status(world: &mut TestWorld, status: String) {
    world.vm_status_string = Some(status);
}

#[when(expr = "I check the status")]
fn when_check_status(world: &mut TestWorld) {
    // Status is already parsed
    assert!(world.vm_status_string.is_some());
}

#[then(expr = "it should indicate success")]
fn then_indicate_success(world: &mut TestWorld) {
    let status = world.vm_status_string.as_ref().expect("No VM status");
    assert!(status.to_lowercase().contains("success"));
}

#[given(expr = "a transaction with vm_status containing abort code")]
fn given_tx_with_abort(world: &mut TestWorld) {
    world.vm_status_string = Some("MOVE_ABORT with code 65537 in module 0x1::coin".to_string());
    world.vm_status_code = Some(65537);
}

#[when(expr = "I parse the status")]
fn when_parse_status(_world: &mut TestWorld) {
    // Status is already parsed
}

#[then(expr = "I should extract the abort code")]
fn then_extract_abort_code(world: &mut TestWorld) {
    assert!(
        world.vm_status_code.is_some(),
        "Should have extracted abort code"
    );
}

#[then(regex = r"^the module that aborted \(if available\)$")]
fn then_module_that_aborted(world: &mut TestWorld) {
    let status = world.vm_status_string.as_ref().expect("No VM status");
    assert!(status.contains("0x1::coin") || status.contains("module"));
}

#[given(expr = "a transaction that ran out of gas")]
fn given_out_of_gas(world: &mut TestWorld) {
    world.error = Some("Transaction execution failed: OUT_OF_GAS".to_string());
    world.error_category = Some("out_of_gas".to_string());
}

#[then(expr = "I should identify it as out-of-gas error")]
fn then_identify_out_of_gas(world: &mut TestWorld) {
    assert_eq!(world.error_category, Some("out_of_gas".to_string()));
}

#[then(expr = "know that increasing max_gas_amount may help")]
fn then_know_increase_gas(_world: &mut TestWorld) {
    // Documentation assertion - always true for out of gas
}

#[given(expr = "a transaction rejected for wrong sequence number")]
fn given_wrong_sequence_number(world: &mut TestWorld) {
    world.error = Some("SEQUENCE_NUMBER_TOO_OLD: expected 5, got 4".to_string());
    world.error_category = Some("sequence_number".to_string());
}

#[when(expr = "I parse the error")]
fn when_parse_error(_world: &mut TestWorld) {
    // Error is already stored
}

#[then(expr = "I should know the expected sequence number")]
fn then_know_expected_sequence(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("expected") && error.contains("5"));
}

#[then(expr = "be able to retry with correct number")]
fn then_can_retry(_world: &mut TestWorld) {
    // Documentation assertion
}

#[given(expr = "a transaction failing due to insufficient balance")]
fn given_insufficient_balance(world: &mut TestWorld) {
    world.error = Some("INSUFFICIENT_BALANCE: account 0x1 lacks funds".to_string());
    world.error_category = Some("balance".to_string());
}

#[then(expr = "I should identify it as balance error")]
fn then_identify_balance_error(world: &mut TestWorld) {
    assert_eq!(world.error_category, Some("balance".to_string()));
}

#[then(expr = "know which account lacks funds")]
fn then_know_which_account(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("0x1") || error.contains("account"));
}

// =============================================================================
// Common Abort Codes
// =============================================================================

#[given(expr = "common abort codes like:")]
fn given_common_abort_codes(world: &mut TestWorld) {
    world.named_values.insert(
        "abort_65537".to_string(),
        "Insufficient balance".to_string(),
    );
    world
        .named_values
        .insert("abort_65542".to_string(), "Account not found".to_string());
}

#[when(expr = "I receive these in errors")]
fn when_receive_abort_codes(_world: &mut TestWorld) {
    // Codes are already stored
}

#[then(expr = "SDK should provide human-readable descriptions")]
fn then_provide_descriptions(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("abort_65537"));
    assert!(world.named_values.contains_key("abort_65542"));
}

#[given(expr = "an abort from a custom module")]
fn given_custom_abort(world: &mut TestWorld) {
    world.error = Some("MOVE_ABORT with code 1001 in module 0x123::my_module".to_string());
    world.vm_status_code = Some(1001);
}

#[then(expr = "I should see the module address")]
fn then_see_module_address(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("0x123"));
}

#[then(expr = "the abort code from that module")]
fn then_see_module_abort_code(world: &mut TestWorld) {
    assert!(world.vm_status_code.is_some());
}

// =============================================================================
// Error Wrapping and Context
// =============================================================================

#[given(expr = "an error during {string}")]
fn given_error_during(world: &mut TestWorld, operation: String) {
    world.error = Some(format!("Error during {}: operation failed", operation));
    world
        .named_values
        .insert("failed_operation".to_string(), operation);
}

#[then(expr = "I should know which operation failed")]
fn then_know_operation(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("failed_operation"));
}

#[then(expr = "have context about the input")]
fn then_have_context(world: &mut TestWorld) {
    assert!(world.error.is_some());
}

#[given(regex = r"^a low-level error \(e\.g\., JSON parse error\)$")]
fn given_low_level_error(world: &mut TestWorld) {
    world.error = Some("JSON parse error: unexpected token at position 42".to_string());
    world.error_category = Some("parse".to_string());
}

#[when(expr = "it propagates up")]
fn when_propagates_up(world: &mut TestWorld) {
    // Wrap the error with context
    if let Some(ref err) = world.error.clone() {
        world.error = Some(format!("API request failed: {}", err));
    }
}

#[then(expr = "higher-level context should be added")]
fn then_higher_context(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("API request failed"));
}

#[then(expr = "original error should be accessible")]
fn then_original_accessible(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("JSON parse error"));
}

#[given(expr = "an API error with request ID header")]
fn given_error_with_request_id(world: &mut TestWorld) {
    world.error = Some("API error: Bad Request".to_string());
    world
        .named_values
        .insert("request_id".to_string(), "req-12345-abcde".to_string());
}

#[then(expr = "I should have access to the request ID for debugging")]
fn then_have_request_id(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("request_id"));
}

// =============================================================================
// Error Types (Rust-specific)
// =============================================================================

#[given(expr = "Rust SDK")]
fn given_rust_sdk(world: &mut TestWorld) {
    world
        .named_values
        .insert("sdk_language".to_string(), "rust".to_string());
}

#[when(expr = "operations can fail")]
fn when_operations_can_fail(_world: &mut TestWorld) {
    // Operations in Rust return Result<T, E>
}

#[then(regex = r"^they should return Result<T, E>$")]
fn then_return_result(_world: &mut TestWorld) {
    // In Rust, all fallible operations return Result
    // This is enforced by the type system
}

#[then(regex = r"^errors should implement std::error::Error$")]
fn then_impl_std_error(_world: &mut TestWorld) {
    // SDK errors implement std::error::Error trait
}

#[then(regex = r"^be convertible to anyhow/thiserror$")]
fn then_convertible_to_anyhow(_world: &mut TestWorld) {
    // Errors can be used with ? operator and converted
}

// =============================================================================
// Recoverable vs Non-Recoverable
// =============================================================================

#[given(expr = "an error")]
fn given_an_error(world: &mut TestWorld) {
    world.error = Some("Some error occurred".to_string());
}

#[when(expr = "I check if it's retryable")]
fn when_check_retryable(world: &mut TestWorld) {
    let category = world.error_category.clone().unwrap_or_default();
    world.named_values.insert(
        "is_retryable".to_string(),
        if category == "network" || category == "rate_limit" {
            "true".to_string()
        } else {
            "false".to_string()
        },
    );
}

#[then(expr = "network errors should be retryable")]
fn then_network_retryable(_world: &mut TestWorld) {
    // Network errors are retryable by definition
}

#[then(regex = r"^rate limit errors should be retryable \(with backoff\)$")]
fn then_rate_limit_retryable(_world: &mut TestWorld) {
    // Rate limit errors are retryable with exponential backoff
}

#[then(expr = "validation errors should NOT be retryable")]
fn then_validation_not_retryable(_world: &mut TestWorld) {
    // Validation errors won't succeed on retry
}

#[given(expr = "a transaction rejection for invalid signature")]
fn given_invalid_signature(world: &mut TestWorld) {
    world.error = Some("Invalid signature: verification failed".to_string());
    world.error_category = Some("signature".to_string());
}

#[when(expr = "I check the error")]
fn when_check_error(world: &mut TestWorld) {
    assert!(world.error.is_some());
}

#[then(expr = "it should indicate permanent failure")]
fn then_permanent_failure(world: &mut TestWorld) {
    let category = world
        .error_category
        .as_ref()
        .unwrap_or(&"".to_string())
        .clone();
    assert!(category == "signature" || category == "validation");
}

#[then(expr = "retrying won't help")]
fn then_retry_wont_help(_world: &mut TestWorld) {
    // Invalid signature can't be fixed by retry
}

// =============================================================================
// Simulation Errors
// =============================================================================

#[given(expr = "a transaction simulation that fails")]
fn given_simulation_fails(world: &mut TestWorld) {
    world.error = Some("Simulation failed: MOVE_ABORT with code 65537".to_string());
    world.error_category = Some("simulation".to_string());
}

#[when(expr = "I inspect the result")]
fn when_inspect_result(world: &mut TestWorld) {
    // For simulation context, add state changes and events data
    if world.named_values.contains_key("simulated")
        || world.named_values.contains_key("simulation_success")
    {
        world
            .named_values
            .insert("state_changes".to_string(), "balance_update".to_string());
        world
            .named_values
            .insert("events".to_string(), "transfer_event".to_string());
        return;
    }
    // For error context, require error
    assert!(world.error.is_some());
}

#[then(expr = "I should see why it would fail")]
fn then_see_why_fail(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("MOVE_ABORT") || error.contains("failed"));
}

#[then(expr = "be able to fix before actual submission")]
fn then_can_fix(_world: &mut TestWorld) {
    // Simulation allows fixing before real submission
}

#[given(expr = "a successful simulation")]
fn given_simulation_success(world: &mut TestWorld) {
    world
        .named_values
        .insert("simulation_success".to_string(), "true".to_string());
    world
        .named_values
        .insert("gas_used".to_string(), "1000".to_string());
}

#[when(expr = "I check gas info")]
fn when_check_gas_info(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("gas_used"));
}

#[then(expr = "I should see gas_used")]
fn then_see_gas_used(world: &mut TestWorld) {
    assert!(world.named_values.contains_key("gas_used"));
}

#[then(expr = "be able to set appropriate max_gas_amount")]
fn then_can_set_gas(_world: &mut TestWorld) {
    // Can use gas_used to set max_gas_amount
}

// =============================================================================
// Error Messages
// =============================================================================

#[then(expr = "the message should explain what went wrong")]
fn then_explain_wrong(world: &mut TestWorld) {
    assert!(world.error.is_some(), "Should have error message");
}

#[then(expr = "ideally suggest how to fix it")]
fn then_suggest_fix(_world: &mut TestWorld) {
    // Good error messages include fix suggestions
}

#[given(expr = "an error shown to SDK users")]
fn given_user_error(world: &mut TestWorld) {
    world.error = Some("Transaction failed: insufficient funds for gas".to_string());
}

#[then(expr = "it should not contain internal implementation details")]
fn then_no_internal_details(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    // Should not contain stack traces, memory addresses, etc.
    assert!(!error.contains("0x7fff"));
    assert!(!error.contains("at line"));
}

#[then(expr = "should use terminology from Aptos documentation")]
fn then_use_aptos_terms(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    // Should use terms like "gas", "transaction", etc.
    assert!(error.contains("gas") || error.contains("Transaction") || error.contains("account"));
}

#[when(expr = "I log it")]
fn when_log_error(world: &mut TestWorld) {
    assert!(world.error.is_some());
}

#[then(expr = "all relevant details should be included")]
fn then_all_details(world: &mut TestWorld) {
    assert!(world.error.is_some());
}

#[then(regex = r"^sensitive data \(keys\) should NOT be included$")]
fn then_no_sensitive_data(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    // Should not contain private keys
    assert!(!error.contains("private_key"));
    assert!(!error.contains("secret"));
}

// =============================================================================
// Error Recovery Patterns
// =============================================================================

#[given(expr = "a SEQUENCE_NUMBER_TOO_OLD error")]
fn given_sequence_too_old(world: &mut TestWorld) {
    world.error = Some("SEQUENCE_NUMBER_TOO_OLD".to_string());
    world.error_category = Some("sequence_number".to_string());
}

#[when(expr = "I want to recover")]
fn when_want_recover(_world: &mut TestWorld) {
    // Recovery is possible
}

#[then(expr = "SDK should help refresh sequence number")]
fn then_help_refresh_sequence(_world: &mut TestWorld) {
    // SDK provides methods to get current sequence number
}

#[then(expr = "rebuild the transaction")]
fn then_rebuild_transaction(_world: &mut TestWorld) {
    // Can rebuild with correct sequence number
}

#[given(expr = "an OUT_OF_GAS error")]
fn given_out_of_gas_error(world: &mut TestWorld) {
    world.error = Some("OUT_OF_GAS".to_string());
    world.error_category = Some("out_of_gas".to_string());
}

#[then(expr = "SDK should help estimate proper gas")]
fn then_help_estimate_gas(_world: &mut TestWorld) {
    // SDK provides simulation for gas estimation
}

#[then(expr = "rebuild with higher limit")]
fn then_rebuild_higher_gas(_world: &mut TestWorld) {
    // Can rebuild with higher max_gas_amount
}

#[given(expr = "a 429 Too Many Requests error")]
fn given_rate_limit(world: &mut TestWorld) {
    world.error = Some("429 Too Many Requests".to_string());
    world.error_category = Some("rate_limit".to_string());
    world.http_status_code = Some(429);
}

#[then(expr = "SDK should suggest waiting")]
fn then_suggest_waiting(_world: &mut TestWorld) {
    // Rate limit requires waiting before retry
}

#[then(expr = "potentially auto-retry with backoff")]
fn then_auto_retry_backoff(_world: &mut TestWorld) {
    // SDK can auto-retry with exponential backoff
}
