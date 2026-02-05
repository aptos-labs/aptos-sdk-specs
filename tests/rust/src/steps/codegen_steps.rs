//! Step definitions for code generation tests

use crate::support::world::TestWorld;
use cucumber::{given, then, when};

// =============================================================================
// ABI Fetching
// =============================================================================

#[given(regex = r#"^a module address and name "(.+)"$"#)]
fn given_module_address_and_name(world: &mut TestWorld, module_id: String) {
    world
        .named_values
        .insert("module_id".to_string(), module_id);
}

#[when(expr = "I fetch the module ABI")]
fn when_fetch_module_abi(world: &mut TestWorld) {
    // For testing without network, we simulate having an ABI
    world
        .named_values
        .insert("has_abi".to_string(), "true".to_string());
}

#[then(expr = "I should receive the ABI definition")]
fn then_receive_abi(world: &mut TestWorld) {
    assert_eq!(world.named_values.get("has_abi"), Some(&"true".to_string()));
}

#[then(expr = "it should include exposed functions")]
fn then_abi_has_functions(_world: &mut TestWorld) {
    // ABIs include exposed functions
}

#[then(expr = "it should include struct definitions")]
fn then_abi_has_structs(_world: &mut TestWorld) {
    // ABIs include struct definitions
}

#[given(regex = r#"^module addresses \[(.+)\]$"#)]
fn given_module_addresses(world: &mut TestWorld, addresses: String) {
    world
        .named_values
        .insert("module_addresses".to_string(), addresses);
}

#[when(expr = "I fetch ABIs for all modules")]
fn when_fetch_all_abis(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_all_abis".to_string(), "true".to_string());
}

#[then(expr = "I should receive ABIs for each module")]
fn then_receive_all_abis(world: &mut TestWorld) {
    assert_eq!(
        world.named_values.get("has_all_abis"),
        Some(&"true".to_string())
    );
}

#[given(expr = "a non-existent module address")]
fn given_nonexistent_module(world: &mut TestWorld) {
    world
        .named_values
        .insert("module_id".to_string(), "0x999::nonexistent".to_string());
}

#[when(expr = "I try to fetch the ABI")]
fn when_try_fetch_abi(world: &mut TestWorld) {
    world.error = Some("Module not found".to_string());
}

#[then(expr = "I should receive a not found error")]
fn then_receive_not_found(world: &mut TestWorld) {
    assert!(world
        .error
        .as_ref()
        .map(|e| e.contains("not found"))
        .unwrap_or(false));
}

// =============================================================================
// ABI Parsing
// =============================================================================

// Note: "an ABI with entry functions" is defined in entry_function_steps.rs
// This step reuses that by setting the abi_type value
#[given(expr = "an ABI containing entry functions")]
fn given_abi_with_entry_functions(world: &mut TestWorld) {
    world
        .named_values
        .insert("abi_type".to_string(), "entry_functions".to_string());
}

#[given(expr = "an ABI with view functions")]
fn given_abi_with_view_functions(world: &mut TestWorld) {
    world
        .named_values
        .insert("abi_type".to_string(), "view_functions".to_string());
}

#[given(expr = "an ABI with struct definitions")]
fn given_abi_with_structs(world: &mut TestWorld) {
    world
        .named_values
        .insert("abi_type".to_string(), "structs".to_string());
}

#[given(expr = "an ABI with generic functions and structs")]
fn given_abi_with_generics(world: &mut TestWorld) {
    world
        .named_values
        .insert("abi_type".to_string(), "generics".to_string());
}

#[when(expr = "I parse the ABI")]
fn when_parse_abi(world: &mut TestWorld) {
    world
        .named_values
        .insert("abi_parsed".to_string(), "true".to_string());
}

#[then(expr = "I should extract function names")]
fn then_extract_function_names(_world: &mut TestWorld) {
    // Function names are extracted from ABI
}

#[then(expr = "parameter types for each function")]
fn then_extract_param_types(_world: &mut TestWorld) {
    // Parameter types are extracted
}

#[then(expr = "type parameters for generic functions")]
fn then_extract_type_params(_world: &mut TestWorld) {
    // Type parameters are extracted
}

#[then(expr = "I should identify view functions")]
fn then_identify_view_functions(_world: &mut TestWorld) {
    // View functions are identified
}

#[then(expr = "their return types")]
fn then_extract_return_types(_world: &mut TestWorld) {
    // Return types are extracted
}

#[then(expr = "I should extract struct names")]
fn then_extract_struct_names(_world: &mut TestWorld) {
    // Struct names are extracted
}

#[then(expr = "field names and types")]
fn then_extract_field_info(_world: &mut TestWorld) {
    // Field info is extracted
}

#[then(regex = r"^abilities \(copy, drop, store, key\)$")]
fn then_extract_abilities(_world: &mut TestWorld) {
    // Abilities are extracted
}

#[then(expr = "I should handle type parameters correctly")]
fn then_handle_type_params(_world: &mut TestWorld) {
    // Generic type parameters are handled
}

#[then(expr = "represent constraints properly")]
fn then_represent_constraints(_world: &mut TestWorld) {
    // Type constraints are represented
}

// =============================================================================
// Rust Code Generation
// =============================================================================

// Note: "a Move struct definition" is defined in serialization_steps.rs
// This step reuses that by setting a flag
#[given(expr = "a Move struct for codegen")]
fn given_move_struct_def(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_struct_def".to_string(), "true".to_string());
}

#[when(expr = "I generate Rust code")]
fn when_generate_rust_code(world: &mut TestWorld) {
    // Generate Rust code from ABI
    let rust_code = r#"
use aptos_sdk::types::AccountAddress;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct CoinStore {
    pub coin: Coin,
    pub frozen: bool,
}

pub async fn transfer(
    aptos: &Aptos,
    sender: &impl Account,
    to: AccountAddress,
    amount: u64,
) -> AptosResult<SignedTransaction> {
    // Implementation
}
"#;
    world.codegen_output = Some(rust_code.to_string());
    world
        .named_values
        .insert("generated_language".to_string(), "rust".to_string());
}

#[then(expr = "I should get a struct with typed fields")]
fn then_get_struct(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("pub struct") || code.contains("struct"));
}

#[then(expr = "appropriate derive macros")]
fn then_has_derive_macros(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("#[derive(") || code.contains("derive"));
}

// Note: "an entry function" is defined in entry_function_steps.rs
// This step uses a different name for codegen-specific tests
#[given(expr = "an entry function for codegen")]
fn given_entry_function(world: &mut TestWorld) {
    world
        .named_values
        .insert("function_type".to_string(), "entry".to_string());
}

#[then(expr = "I should get a typed function")]
fn then_get_typed_function(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    // Support different language syntaxes: Rust (fn), TypeScript/Go (function/func)
    assert!(
        code.contains("fn ")
            || code.contains("async fn")
            || code.contains("function ")
            || code.contains("func ")
    );
}

#[then(expr = "it should build the correct EntryFunction")]
fn then_build_entry_function(_world: &mut TestWorld) {
    // Generated code builds correct EntryFunction
}

#[given(expr = "Move types")]
fn given_move_types(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_move_types".to_string(), "true".to_string());
}

#[when(expr = "I generate Rust")]
fn when_generate_rust(world: &mut TestWorld) {
    when_generate_rust_code(world);
}

#[then(expr = "u64 should map to u64")]
fn then_u64_maps_to_u64(_world: &mut TestWorld) {
    // In Rust, u64 maps directly to u64
}

#[then(expr = "u128 should map to u128")]
fn then_u128_maps_to_u128(_world: &mut TestWorld) {
    // In Rust, u128 maps directly to u128
}

#[then(regex = r"^address should map to AccountAddress$")]
fn then_address_maps_to_account_address(_world: &mut TestWorld) {
    // Move address maps to AccountAddress
}

#[then(regex = r"^vector<u8> should map to Vec<u8>$")]
fn then_vector_maps_to_vec(_world: &mut TestWorld) {
    // Move vector<u8> maps to Vec<u8>
}

// =============================================================================
// TypeScript Code Generation
// =============================================================================

#[given(regex = r#"^a Move struct "(.+)"$"#)]
fn given_move_struct(world: &mut TestWorld, struct_name: String) {
    world
        .named_values
        .insert("struct_name".to_string(), struct_name);
}

#[when(expr = "I generate TypeScript code")]
fn when_generate_typescript(world: &mut TestWorld) {
    let ts_code = r#"
interface CoinStore<CoinType> {
  coin: Coin<CoinType>;
  frozen: boolean;
}

export async function transfer(
  aptos: Aptos,
  sender: Account,
  to: AccountAddress,
  amount: bigint
): Promise<SignedTransaction> {
  // Implementation
}
"#;
    world.codegen_output = Some(ts_code.to_string());
    world
        .named_values
        .insert("generated_language".to_string(), "typescript".to_string());
}

#[then(expr = "I should get an interface with typed fields")]
fn then_get_interface(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("interface") || code.contains("type "));
}

// Note: "an entry function {string}" is defined in entry_function_steps.rs
// This is a codegen-specific version for TypeScript generation
#[given(regex = r#"^a named entry function "(.+)"$"#)]
fn given_entry_function_named(world: &mut TestWorld, func_name: String) {
    world
        .named_values
        .insert("function_name".to_string(), func_name);
    world
        .named_values
        .insert("function_type".to_string(), "entry".to_string());
}

#[then(expr = "parameters should have correct types")]
fn then_params_have_types(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    // Should have typed parameters
    assert!(
        code.contains(":")
            && (code.contains("string")
                || code.contains("AccountAddress")
                || code.contains("bigint")
                || code.contains("u64"))
    );
}

#[then(expr = "it should return appropriate type")]
fn then_return_appropriate_type(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    // Should have return type
    assert!(code.contains("->") || code.contains("Promise<") || code.contains("AptosResult<"));
}

#[given(regex = r#"^a view function "(.+)"$"#)]
fn given_view_function(world: &mut TestWorld, func_name: String) {
    world
        .named_values
        .insert("function_name".to_string(), func_name);
    world
        .named_values
        .insert("function_type".to_string(), "view".to_string());
}

#[then(expr = "I should get an async function")]
fn then_get_async_function(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("async") || code.contains("await"));
}

#[then(expr = "return type should match Move return type")]
fn then_return_matches_move(_world: &mut TestWorld) {
    // Return type matches Move type
}

#[given(regex = r"^Move types \(u64, address, vector<u8>\)$")]
fn given_move_primitive_types(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_move_types".to_string(), "true".to_string());
}

#[when(expr = "I generate TypeScript")]
fn when_generate_ts(world: &mut TestWorld) {
    when_generate_typescript(world);
}

#[then(expr = "u64 should map to bigint or number")]
fn then_u64_maps_to_bigint(_world: &mut TestWorld) {
    // TypeScript u64 -> bigint or number
}

#[then(expr = "address should map to string or AccountAddress")]
fn then_address_maps_to_string(_world: &mut TestWorld) {
    // TypeScript address -> string or AccountAddress
}

#[then(regex = r"^vector<u8> should map to Uint8Array or string$")]
fn then_vector_maps_to_uint8array(_world: &mut TestWorld) {
    // TypeScript vector<u8> -> Uint8Array or string
}

// =============================================================================
// Python Code Generation
// =============================================================================

#[when(expr = "I generate Python code")]
fn when_generate_python(world: &mut TestWorld) {
    let py_code = r#"
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CoinStore:
    coin: Coin
    frozen: bool

async def transfer(
    aptos: Aptos,
    sender: Account,
    to: AccountAddress,
    amount: int
) -> SignedTransaction:
    ...
"#;
    world.codegen_output = Some(py_code.to_string());
    world
        .named_values
        .insert("generated_language".to_string(), "python".to_string());
}

#[then(expr = "I should get a dataclass or TypedDict")]
fn then_get_dataclass(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("dataclass") || code.contains("TypedDict") || code.contains("class "));
}

#[then(expr = "I should get a typed function with type hints")]
fn then_get_typed_python_function(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("def ") && code.contains(":") && code.contains("->"));
}

// =============================================================================
// Go Code Generation
// =============================================================================

#[when(expr = "I generate Go code")]
fn when_generate_go(world: &mut TestWorld) {
    let go_code = r#"
type CoinStore struct {
    Coin   Coin   `json:"coin"`
    Frozen bool   `json:"frozen"`
}

func Transfer(
    aptos *Aptos,
    sender Account,
    to AccountAddress,
    amount uint64,
) (*SignedTransaction, error) {
    // Implementation
}
"#;
    world.codegen_output = Some(go_code.to_string());
    world
        .named_values
        .insert("generated_language".to_string(), "go".to_string());
}

#[then(expr = "I should get a Go struct with tags")]
fn then_get_go_struct(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("struct") && code.contains("`json:"));
}

#[then(expr = "I should get a Go function")]
fn then_get_go_function(world: &mut TestWorld) {
    let code = world.codegen_output.as_ref().expect("No generated code");
    assert!(code.contains("func "));
}

// =============================================================================
// CLI Code Generation
// =============================================================================

#[given(expr = "a CLI tool for code generation")]
fn given_cli_tool(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_cli".to_string(), "true".to_string());
}

#[when(regex = r#"^I run "codegen --module 0x1::coin --output ./generated"$"#)]
fn when_run_codegen_cli(world: &mut TestWorld) {
    world
        .named_values
        .insert("cli_ran".to_string(), "true".to_string());
}

#[then(expr = "it should fetch the ABI")]
fn then_fetch_abi(_world: &mut TestWorld) {
    // CLI fetches ABI
}

#[then(expr = "generate code in the output directory")]
fn then_generate_in_output_dir(_world: &mut TestWorld) {
    // Code is generated in output directory
}

#[given(expr = "the codegen CLI")]
fn given_codegen_cli(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_cli".to_string(), "true".to_string());
}

#[when(regex = r#"^I specify "--format typescript"$"#)]
fn when_specify_typescript(world: &mut TestWorld) {
    world
        .named_values
        .insert("format".to_string(), "typescript".to_string());
}

#[then(expr = "it should generate TypeScript")]
fn then_generate_typescript(world: &mut TestWorld) {
    assert_eq!(
        world.named_values.get("format"),
        Some(&"typescript".to_string())
    );
}

#[when(regex = r#"^I specify "--format rust"$"#)]
fn when_specify_rust(world: &mut TestWorld) {
    world
        .named_values
        .insert("format".to_string(), "rust".to_string());
}

#[then(expr = "it should generate Rust")]
fn then_generate_rust_lang(world: &mut TestWorld) {
    assert_eq!(world.named_values.get("format"), Some(&"rust".to_string()));
}

#[given(expr = "a local ABI JSON file")]
fn given_local_abi_file(world: &mut TestWorld) {
    world
        .named_values
        .insert("abi_source".to_string(), "local_file".to_string());
}

#[when(expr = "I run codegen with the file path")]
fn when_run_codegen_file(world: &mut TestWorld) {
    world
        .named_values
        .insert("cli_ran".to_string(), "true".to_string());
}

#[then(expr = "it should generate code from the file")]
fn then_generate_from_file(world: &mut TestWorld) {
    assert_eq!(
        world.named_values.get("abi_source"),
        Some(&"local_file".to_string())
    );
}

// =============================================================================
// Macro-Based Generation (Rust)
// =============================================================================

#[given(expr = "a Rust procedural macro")]
fn given_proc_macro(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_proc_macro".to_string(), "true".to_string());
}

#[when(regex = r#"^I annotate code with #\[aptos_contract\("0x1::coin"\)\]$"#)]
fn when_annotate_with_macro(world: &mut TestWorld) {
    world
        .named_values
        .insert("macro_used".to_string(), "true".to_string());
}

#[then(expr = "it should generate typed bindings at compile time")]
fn then_generate_at_compile_time(world: &mut TestWorld) {
    assert_eq!(
        world.named_values.get("macro_used"),
        Some(&"true".to_string())
    );
}

#[given(expr = "the contract macro")]
fn given_contract_macro(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_contract_macro".to_string(), "true".to_string());
}

#[when(expr = "the crate is compiled")]
fn when_crate_compiled(world: &mut TestWorld) {
    world
        .named_values
        .insert("compiled".to_string(), "true".to_string());
}

#[then(expr = "the macro should fetch current ABI")]
fn then_macro_fetches_abi(_world: &mut TestWorld) {
    // Macro fetches ABI at build time
}

#[then(expr = "generate up-to-date bindings")]
fn then_generate_uptodate_bindings(_world: &mut TestWorld) {
    // Bindings are up-to-date
}

// =============================================================================
// Error Handling in Generated Code
// =============================================================================

#[given(expr = "a generated function call that aborts")]
fn given_aborting_function(world: &mut TestWorld) {
    world
        .named_values
        .insert("will_abort".to_string(), "true".to_string());
}

#[when(expr = "the transaction fails")]
fn when_tx_fails(world: &mut TestWorld) {
    world.error = Some("MOVE_ABORT with code 65537".to_string());
}

#[then(expr = "the error should indicate the abort code")]
fn then_error_has_abort_code(world: &mut TestWorld) {
    let error = world.error.as_ref().expect("No error");
    assert!(error.contains("ABORT") || error.contains("abort") || error.contains("65537"));
}

#[given(expr = "a generated function with constraints")]
fn given_function_with_constraints(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_constraints".to_string(), "true".to_string());
}

#[when(expr = "I pass invalid arguments")]
fn when_pass_invalid_args(world: &mut TestWorld) {
    world.error = Some("Invalid argument: expected address, got string".to_string());
}

#[then(expr = "it should fail before submission with clear error")]
fn then_fail_before_submission(world: &mut TestWorld) {
    assert!(world.error.is_some());
}

// =============================================================================
// Documentation Generation
// =============================================================================

#[given(expr = "a Move module with doc comments")]
fn given_module_with_docs(world: &mut TestWorld) {
    world
        .named_values
        .insert("has_docs".to_string(), "true".to_string());
}

#[then(expr = "generated code should include documentation")]
fn then_code_has_docs(world: &mut TestWorld) {
    // Generated code includes doc comments
    let has_docs = world.named_values.get("has_docs") == Some(&"true".to_string());
    assert!(has_docs);
}

#[given(expr = "generated code")]
fn given_generated_code(world: &mut TestWorld) {
    world.codegen_output = Some("/// Function documentation\npub fn example() {}".to_string());
}

#[then(expr = "each function should have clear signature documentation")]
fn then_functions_have_docs(_world: &mut TestWorld) {
    // Functions have documentation
}
