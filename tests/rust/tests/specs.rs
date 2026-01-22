//! Main test runner for behavioral specifications.
//!
//! This runs all Gherkin feature files against the SDK using Cucumber.

use aptos_sdk_spec_tests::steps::*;
use aptos_sdk_spec_tests::support::TestWorld;
use cucumber::World;
use std::path::PathBuf;

fn features_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("..")
        .join("features")
}

#[tokio::main]
async fn main() {
    // Run Cucumber tests
    TestWorld::cucumber()
        .max_concurrent_scenarios(1) // Run scenarios sequentially for determinism
        .with_default_cli()
        .run_and_exit(features_dir())
        .await;
}

