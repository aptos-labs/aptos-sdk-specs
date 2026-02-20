@advanced
@optional
Feature: Code Generation from Move ABI
  As an SDK user
  I want to generate type-safe code from Move ABIs
  So that I can interact with smart contracts safely

  # =============================================================================
  # ABI Fetching
  # =============================================================================
  @optional
  Scenario: Fetch module ABI from chain
    Given a connected Aptos client
    And a module address and name "0x1::coin"
    When I fetch the module ABI
    Then I should receive the ABI definition
    And it should include exposed functions
    And it should include struct definitions

  @optional
  Scenario: Fetch ABI for multiple modules
    Given module addresses ["0x1::coin", "0x1::aptos_account"]
    When I fetch ABIs for all modules
    Then I should receive ABIs for each module

  @optional
  Scenario: Handle module not found
    Given a non-existent module address
    When I try to fetch the ABI
    Then I should receive a not found error

  # =============================================================================
  # ABI Parsing
  # =============================================================================
  @optional
  Scenario: Parse entry functions from ABI
    Given an ABI with entry functions
    When I parse the ABI
    Then I should extract function names
    And parameter types for each function
    And type parameters for generic functions

  @optional
  Scenario: Parse view functions from ABI
    Given an ABI with view functions
    When I parse the ABI
    Then I should identify view functions
    And their return types

  @optional
  Scenario: Parse struct definitions from ABI
    Given an ABI with struct definitions
    When I parse the ABI
    Then I should extract struct names
    And field names and types
    And abilities (copy, drop, store, key)

  @optional
  Scenario: Parse enum definitions from ABI
    Given an ABI with enum definitions
    When I parse the ABI
    Then I should identify enums via the is_enum flag
    And extract variant names for each enum
    And extract field names and types for each variant
    And abilities (copy, drop, store, key)

  @optional
  Scenario: Parse generic types
    Given an ABI with generic functions and structs
    When I parse the ABI
    Then I should handle type parameters correctly
    And represent constraints properly

  # =============================================================================
  # TypeScript Code Generation
  # =============================================================================
  @optional
  Scenario: Generate TypeScript types for structs
    Given a Move struct "CoinStore<CoinType>"
    When I generate TypeScript code
    Then I should get an interface with typed fields

  @optional
  Scenario: Generate TypeScript types for enums
    Given a Move enum "DrawCommand" with variants Fill, Stroke, Clear
    When I generate TypeScript code
    Then I should get a discriminated union type with variant interfaces

  @optional
  Scenario: Generate TypeScript function wrappers
    Given an entry function "transfer"
    When I generate TypeScript code
    Then I should get a typed function
    And parameters should have correct types
    And it should return appropriate type

  @optional
  Scenario: Generate TypeScript view function wrappers
    Given a view function "balance"
    When I generate TypeScript code
    Then I should get an async function
    And return type should match Move return type

  @optional
  Scenario: Map Move types to TypeScript
    Given Move types (u64, address, vector<u8>)
    When I generate TypeScript
    Then u64 should map to bigint or number
    And address should map to string or AccountAddress
    And vector<u8> should map to Uint8Array or string

  # =============================================================================
  # Rust Code Generation
  # =============================================================================
  @optional
  Scenario: Generate Rust types for structs
    Given a Move struct definition
    When I generate Rust code
    Then I should get a struct with typed fields
    And appropriate derive macros

  @optional
  Scenario: Generate Rust types for enums
    Given a Move enum definition with variants
    When I generate Rust code
    Then I should get a Rust enum with variant structs
    And appropriate derive macros

  @optional
  Scenario: Generate Rust function wrappers
    Given an entry function
    When I generate Rust code
    Then I should get a typed function
    And it should build the correct EntryFunction

  @optional
  Scenario: Map Move types to Rust
    Given Move types
    When I generate Rust
    Then u64 should map to u64
    And u128 should map to u128
    And address should map to AccountAddress
    And vector<u8> should map to Vec<u8>

  # =============================================================================
  # Python Code Generation
  # =============================================================================
  @optional
  Scenario: Generate Python types for structs
    Given a Move struct definition
    When I generate Python code
    Then I should get a dataclass or TypedDict

  @optional
  Scenario: Generate Python function wrappers
    Given an entry function
    When I generate Python code
    Then I should get a typed function with type hints

  # =============================================================================
  # Go Code Generation
  # =============================================================================
  @optional
  Scenario: Generate Go types for structs
    Given a Move struct definition
    When I generate Go code
    Then I should get a Go struct with tags

  @optional
  Scenario: Generate Go function wrappers
    Given an entry function
    When I generate Go code
    Then I should get a Go function

  # =============================================================================
  # Argument Encoding
  # =============================================================================
  @optional
  Scenario: Generated code handles enum encoding
    Given a generated function expecting an enum
    When I call it with a variant value
    Then it should properly BCS encode the variant tag and fields

  @optional
  Scenario: Generated code handles address encoding
    Given a generated function expecting address
    When I call it with an address string
    Then it should properly encode the address

  @optional
  Scenario: Generated code handles u64 encoding
    Given a generated function expecting u64
    When I call it with a number
    Then it should properly BCS encode the value

  @optional
  Scenario: Generated code handles vector encoding
    Given a generated function expecting vector<u8>
    When I call it with byte array
    Then it should properly BCS encode the vector

  @optional
  Scenario: Generated code handles struct encoding
    Given a generated function expecting a struct
    When I call it with the struct
    Then it should properly BCS encode all fields in order

  # =============================================================================
  # Type Safety
  # =============================================================================
  @optional
  Scenario: Compile-time type checking
    Given generated TypeScript/Rust code
    When I call a function with wrong argument types
    Then compilation should fail with type error

  @optional
  Scenario: Type inference for generics
    Given a generic function like transfer<CoinType>
    When I call it with a specific type
    Then the type parameter should be inferred or required

  @optional
  Scenario: Optional parameters handling
    Given a function with Option<T> parameter
    When I generate code
    Then the parameter should be optional in generated code

  # =============================================================================
  # CLI Code Generation
  # =============================================================================
  @optional
  Scenario: Generate code via CLI
    Given a CLI tool for code generation
    When I run "codegen --module 0x1::coin --output ./generated"
    Then it should fetch the ABI
    And generate code in the output directory

  @optional
  Scenario: CLI supports multiple output formats
    Given the codegen CLI
    When I specify "--format typescript"
    Then it should generate TypeScript
    When I specify "--format rust"
    Then it should generate Rust

  @optional
  Scenario: CLI from local ABI file
    Given a local ABI JSON file
    When I run codegen with the file path
    Then it should generate code from the file

  # =============================================================================
  # Macro-Based Generation (Rust)
  # =============================================================================
  @optional
  Scenario: Procedural macro for contract bindings
    Given a Rust procedural macro
    When I annotate code with #[aptos_contract("0x1::coin")]
    Then it should generate typed bindings at compile time

  @optional
  Scenario: Macro fetches ABI at build time
    Given the contract macro
    When the crate is compiled
    Then the macro should fetch current ABI
    And generate up-to-date bindings

  # =============================================================================
  # Error Handling in Generated Code
  # =============================================================================
  @optional
  Scenario: Generated code surfaces Move errors
    Given a generated function call that aborts
    When the transaction fails
    Then the error should indicate the abort code

  @optional
  Scenario: Generated code validates arguments
    Given a generated function with constraints
    When I pass invalid arguments
    Then it should fail before submission with clear error

  # =============================================================================
  # Documentation Generation
  # =============================================================================
  @optional
  Scenario: Generate documentation comments
    Given a Move module with doc comments
    When I generate code
    Then generated code should include documentation

  @optional
  Scenario: Include function signatures in docs
    Given generated code
    Then each function should have clear signature documentation
