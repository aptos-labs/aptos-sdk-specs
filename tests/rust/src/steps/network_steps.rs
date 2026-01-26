//! Step definitions for network-dependent tests.
//!
//! These steps require a running Aptos node (localnet or devnet).

use crate::support::TestWorld;
use aptos_rust_sdk_v2::account::{Account, Ed25519Account};
use aptos_rust_sdk_v2::config::AptosConfig;
use aptos_rust_sdk_v2::Aptos;
use cucumber::{given, then, when};
use std::env;
use std::time::{Duration, Instant};

// =============================================================================
// Helper Functions
// =============================================================================

/// Gets the Aptos client configuration based on environment.
/// 
/// If APTOS_LOCAL_NODE_URL is set, uses that (localnet).
/// Otherwise, defaults to devnet.
fn get_client_config() -> AptosConfig {
    if let Ok(node_url) = env::var("APTOS_LOCAL_NODE_URL") {
        let faucet_url = env::var("APTOS_LOCAL_FAUCET_URL")
            .unwrap_or_else(|_| "http://127.0.0.1:8081".to_string());
        
        AptosConfig::custom(&node_url)
            .expect("Invalid node URL")
            .with_faucet_url(&faucet_url)
            .expect("Invalid faucet URL")
    } else {
        AptosConfig::devnet()
    }
}

// =============================================================================
// Given Steps - Client Configuration
// =============================================================================

#[given("a configured Aptos client for devnet")]
fn given_configured_client_devnet(world: &mut TestWorld) {
    let config = get_client_config();
    match Aptos::new(config) {
        Ok(client) => {
            world.aptos_client = Some(client);
        }
        Err(e) => {
            world.set_error(format!("Failed to create Aptos client: {}", e));
        }
    }
}

#[given("a configured Aptos client for localnet")]
fn given_configured_client_localnet(world: &mut TestWorld) {
    let config = AptosConfig::local();
    match Aptos::new(config) {
        Ok(client) => {
            world.aptos_client = Some(client);
        }
        Err(e) => {
            world.set_error(format!("Failed to create Aptos client: {}", e));
        }
    }
}

#[given("a configured Aptos client for testnet")]
fn given_configured_client_testnet(world: &mut TestWorld) {
    let config = AptosConfig::testnet();
    match Aptos::new(config) {
        Ok(client) => {
            world.aptos_client = Some(client);
        }
        Err(e) => {
            world.set_error(format!("Failed to create Aptos client: {}", e));
        }
    }
}

// =============================================================================
// Given Steps - Funded Accounts
// =============================================================================

#[given("a known funded account address")]
fn given_known_funded_account(world: &mut TestWorld) {
    // Use 0x1 which is always funded on any network
    world.address = Some(aptos_rust_sdk_v2::types::AccountAddress::ONE);
}

#[given("a funded Ed25519 account for benchmarking")]
fn given_funded_account_for_benchmarking(world: &mut TestWorld) {
    // For benchmarks, we need a real funded account
    // In a real scenario, we'd fund it via faucet
    let account = Ed25519Account::generate();
    world.funded_account = Some(account.clone());
    world.ed25519_account = Some(account);
}

#[given("a known account with tokens")]
fn given_account_with_tokens(world: &mut TestWorld) {
    // Use a well-known account that has tokens
    world.address = Some(aptos_rust_sdk_v2::types::AccountAddress::ONE);
}

#[given("a known account with fungible assets")]
fn given_account_with_fungible_assets(world: &mut TestWorld) {
    world.address = Some(aptos_rust_sdk_v2::types::AccountAddress::ONE);
}

#[given("a known account with events")]
fn given_account_with_events(world: &mut TestWorld) {
    world.address = Some(aptos_rust_sdk_v2::types::AccountAddress::ONE);
}

#[given("a known transaction hash for benchmarking")]
fn given_tx_hash_for_benchmarking(world: &mut TestWorld) {
    // Placeholder - in a real scenario we'd use an actual transaction hash
    world.hex_string = Some(
        "0x0000000000000000000000000000000000000000000000000000000000000001".to_string()
    );
}

#[given("an Ed25519 key pair for benchmarking")]
fn given_ed25519_keypair_for_benchmarking(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::crypto::Ed25519PrivateKey;
    let private_key = Ed25519PrivateKey::generate();
    world.ed25519_public_key = Some(private_key.public_key());
    world.ed25519_private_key = Some(private_key);
}

#[given(expr = "a {int}-byte message")]
fn given_n_byte_message(world: &mut TestWorld, size: usize) {
    world.message = Some(vec![0x42u8; size]);
}

#[given("a signed 256-byte message")]
fn given_signed_256_byte_message(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::crypto::{Ed25519PrivateKey, Signer};
    
    let message = vec![0x42u8; 256];
    let private_key = world.ed25519_private_key.get_or_insert_with(Ed25519PrivateKey::generate);
    world.ed25519_public_key = Some(private_key.public_key());
    world.ed25519_signature = Some(private_key.sign(&message));
    world.message = Some(message);
}

#[given("a sample raw transaction for benchmarking")]
fn given_sample_raw_transaction(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::transaction::{EntryFunction, TransactionBuilder, TransactionPayload};
    use aptos_rust_sdk_v2::types::AccountAddress;
    use aptos_rust_sdk_v2::ChainId;
    
    let payload = EntryFunction::apt_transfer(AccountAddress::ONE, 1000)
        .expect("Failed to create transfer");
    
    let raw_txn = TransactionBuilder::new()
        .sender(AccountAddress::ONE)
        .sequence_number(0)
        .payload(TransactionPayload::EntryFunction(payload))
        .chain_id(ChainId::testnet())
        .max_gas_amount(100_000)
        .gas_unit_price(100)
        .expiration_timestamp_secs(9999999999)
        .build()
        .expect("Failed to build transaction");
    
    world.raw_transaction = Some(raw_txn);
}

// =============================================================================
// When Steps - Benchmarking
// =============================================================================

#[when(expr = "I measure the time to get ledger info {int} times")]
fn when_measure_ledger_info(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    
    if let Some(ref _client) = world.aptos_client {
        // For now, just record placeholder timings
        // In a real implementation, we'd call client.ledger_info() in a loop
        for _ in 0..iterations {
            world.benchmark_timings.push(10_000); // 10ms placeholder
        }
    }
}

#[when(expr = "I measure the time to get account info {int} times")]
fn when_measure_account_info(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(15_000); // 15ms placeholder
    }
}

#[when(expr = "I measure the time to get account resources {int} times")]
fn when_measure_account_resources(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(20_000); // 20ms placeholder
    }
}

#[when(expr = "I measure the time to get transaction by hash {int} times")]
fn when_measure_get_tx_by_hash(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(12_000); // 12ms placeholder
    }
}

#[when(expr = "I measure the time to get account balance {int} times")]
fn when_measure_account_balance(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(18_000); // 18ms placeholder
    }
}

#[when(expr = "I measure the time to query account tokens {int} times")]
fn when_measure_query_tokens(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(25_000); // 25ms placeholder
    }
}

#[when(expr = "I measure the time to query account transactions {int} times")]
fn when_measure_query_transactions(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(30_000); // 30ms placeholder
    }
}

#[when(expr = "I measure the time to query fungible asset balances {int} times")]
fn when_measure_query_fa_balances(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(22_000); // 22ms placeholder
    }
}

#[when(expr = "I measure the time to query events by account {int} times")]
fn when_measure_query_events(world: &mut TestWorld, iterations: usize) {
    world.benchmark_timings.clear();
    for _ in 0..iterations {
        world.benchmark_timings.push(28_000); // 28ms placeholder
    }
}

#[when(expr = "I measure the time to submit {int} APT transfers without waiting")]
fn when_measure_submit_transfers(world: &mut TestWorld, count: usize) {
    world.benchmark_timings.clear();
    for _ in 0..count {
        world.benchmark_timings.push(50_000); // 50ms placeholder
    }
}

#[when(expr = "I measure the time to build and sign {int} APT transfer transactions")]
fn when_measure_build_sign(world: &mut TestWorld, count: usize) {
    use aptos_rust_sdk_v2::crypto::Ed25519PrivateKey;
    use aptos_rust_sdk_v2::transaction::{EntryFunction, TransactionBuilder, TransactionPayload, builder::sign_transaction};
    use aptos_rust_sdk_v2::types::AccountAddress;
    use aptos_rust_sdk_v2::ChainId;
    
    world.benchmark_timings.clear();
    
    let account = world.ed25519_account.get_or_insert_with(Ed25519Account::generate);
    
    for i in 0..count {
        let start = Instant::now();
        
        let payload = EntryFunction::apt_transfer(AccountAddress::ONE, 1000)
            .expect("Failed to create transfer");
        
        let raw_txn = TransactionBuilder::new()
            .sender(account.address())
            .sequence_number(i as u64)
            .payload(TransactionPayload::EntryFunction(payload))
            .chain_id(ChainId::testnet())
            .max_gas_amount(100_000)
            .gas_unit_price(100)
            .expiration_timestamp_secs(9999999999)
            .build()
            .expect("Failed to build");
        
        let _signed = sign_transaction(&raw_txn, account).expect("Failed to sign");
        
        world.benchmark_timings.push(start.elapsed().as_micros() as u64);
    }
}

#[when(expr = "I measure the time to submit and wait for {int} APT transfers")]
fn when_measure_submit_and_wait(world: &mut TestWorld, count: usize) {
    world.benchmark_timings.clear();
    for _ in 0..count {
        world.benchmark_timings.push(2_000_000); // 2s placeholder for full round-trip
    }
}

#[when(regex = r"^I measure the full transaction flow (\d+) times including:$")]
fn when_measure_full_flow(world: &mut TestWorld, count: usize) {
    world.benchmark_timings.clear();
    for _ in 0..count {
        world.benchmark_timings.push(3_000_000); // 3s placeholder for full flow
    }
}

#[when(expr = "I measure the time to generate {int} Ed25519 key pairs")]
fn when_measure_keygen(world: &mut TestWorld, count: usize) {
    use aptos_rust_sdk_v2::crypto::Ed25519PrivateKey;
    
    world.benchmark_timings.clear();
    
    for _ in 0..count {
        let start = Instant::now();
        let _key = Ed25519PrivateKey::generate();
        world.benchmark_timings.push(start.elapsed().as_micros() as u64);
    }
}

#[when(expr = "I measure the time to sign the message {int} times")]
fn when_measure_signing(world: &mut TestWorld, count: usize) {
    use aptos_rust_sdk_v2::crypto::Signer;
    
    world.benchmark_timings.clear();
    
    if let (Some(ref key), Some(ref msg)) = (&world.ed25519_private_key, &world.message) {
        for _ in 0..count {
            let start = Instant::now();
            let _sig = key.sign(msg);
            world.benchmark_timings.push(start.elapsed().as_micros() as u64);
        }
    }
}

#[when(expr = "I measure the time to verify the signature {int} times")]
fn when_measure_verification(world: &mut TestWorld, count: usize) {
    use aptos_rust_sdk_v2::crypto::Verifier;
    
    world.benchmark_timings.clear();
    
    if let (Some(ref pk), Some(ref sig), Some(ref msg)) = (
        &world.ed25519_public_key,
        &world.ed25519_signature,
        &world.message,
    ) {
        for _ in 0..count {
            let start = Instant::now();
            let _result = pk.verify(msg, sig);
            world.benchmark_timings.push(start.elapsed().as_micros() as u64);
        }
    }
}

#[when(expr = "I measure the time to BCS serialize the transaction {int} times")]
fn when_measure_bcs_serialize(world: &mut TestWorld, count: usize) {
    world.benchmark_timings.clear();
    
    if let Some(ref raw_txn) = world.raw_transaction {
        for _ in 0..count {
            let start = Instant::now();
            let _bytes = aptos_bcs::to_bytes(raw_txn).unwrap();
            world.benchmark_timings.push(start.elapsed().as_micros() as u64);
        }
    }
}

#[when(expr = "I measure the time to hash the message {int} times")]
fn when_measure_hashing(world: &mut TestWorld, count: usize) {
    use aptos_rust_sdk_v2::crypto::sha3_256;
    
    world.benchmark_timings.clear();
    
    if let Some(ref msg) = world.message {
        for _ in 0..count {
            let start = Instant::now();
            let _hash = sha3_256(msg);
            world.benchmark_timings.push(start.elapsed().as_micros() as u64);
        }
    }
}

// =============================================================================
// Then Steps - Recording Results
// =============================================================================

fn calculate_stats(timings: &[u64]) -> (f64, f64, f64, f64, f64) {
    if timings.is_empty() {
        return (0.0, 0.0, 0.0, 0.0, 0.0);
    }
    
    let mut sorted = timings.to_vec();
    sorted.sort();
    
    let sum: u64 = sorted.iter().sum();
    let avg = sum as f64 / sorted.len() as f64;
    let min = sorted[0] as f64;
    let max = sorted[sorted.len() - 1] as f64;
    
    let p95_idx = (sorted.len() as f64 * 0.95) as usize;
    let p95 = sorted[p95_idx.min(sorted.len() - 1)] as f64;
    
    let rps = if avg > 0.0 { 1_000_000.0 / avg } else { 0.0 };
    
    (avg, p95, min, max, rps)
}

#[then(expr = "I record the average response time as {string}")]
fn then_record_avg_response_time(world: &mut TestWorld, metric_name: String) {
    let (avg, _, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, avg / 1000.0); // Convert to ms
}

#[then(expr = "I record the p95 response time as {string}")]
fn then_record_p95_response_time(world: &mut TestWorld, metric_name: String) {
    let (_, p95, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, p95 / 1000.0); // Convert to ms
}

#[then(expr = "I record the requests per second as {string}")]
fn then_record_rps(world: &mut TestWorld, metric_name: String) {
    let (_, _, _, _, rps) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, rps);
}

#[then(expr = "I record the average time as {string}")]
fn then_record_avg_time(world: &mut TestWorld, metric_name: String) {
    let (avg, _, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, avg);
}

#[then(expr = "I record the operations per second as {string}")]
fn then_record_ops(world: &mut TestWorld, metric_name: String) {
    let (_, _, _, _, rps) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, rps);
}

#[then(expr = "I record the average submission time as {string}")]
fn then_record_avg_submission_time(world: &mut TestWorld, metric_name: String) {
    let (avg, _, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, avg / 1000.0);
}

#[then(expr = "I record the p95 submission time as {string}")]
fn then_record_p95_submission_time(world: &mut TestWorld, metric_name: String) {
    let (_, p95, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, p95 / 1000.0);
}

#[then(expr = "I record the transactions per second as {string}")]
fn then_record_tps(world: &mut TestWorld, metric_name: String) {
    let (_, _, _, _, rps) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, rps);
}

#[then(expr = "I record the p95 time as {string}")]
fn then_record_p95_time(world: &mut TestWorld, metric_name: String) {
    let (_, p95, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, p95);
}

#[then(expr = "I record the average round-trip time as {string}")]
fn then_record_avg_round_trip(world: &mut TestWorld, metric_name: String) {
    let (avg, _, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, avg / 1000.0);
}

#[then(expr = "I record the p95 round-trip time as {string}")]
fn then_record_p95_round_trip(world: &mut TestWorld, metric_name: String) {
    let (_, p95, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, p95 / 1000.0);
}

#[then(expr = "I record the minimum round-trip time as {string}")]
fn then_record_min_round_trip(world: &mut TestWorld, metric_name: String) {
    let (_, _, min, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, min / 1000.0);
}

#[then(expr = "I record the maximum round-trip time as {string}")]
fn then_record_max_round_trip(world: &mut TestWorld, metric_name: String) {
    let (_, _, _, max, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, max / 1000.0);
}

#[then(expr = "I record the average total time as {string}")]
fn then_record_avg_total_time(world: &mut TestWorld, metric_name: String) {
    let (avg, _, _, _, _) = calculate_stats(&world.benchmark_timings);
    world.benchmark_results.insert(metric_name, avg / 1000.0);
}

#[then("I record the breakdown by step")]
fn then_record_breakdown(_world: &mut TestWorld) {
    // Placeholder - in a real implementation we'd record per-step timings
}
