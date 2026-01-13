# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## Project Overview

This repository contains language-agnostic behavioral specifications for Aptos SDK implementations.
It uses Gherkin (BDD) scenarios to define expected behaviors and JSON test vectors for deterministic
validation. The goal is to ensure consistent behavior across all official and community Aptos SDKs.

## Repository Structure

- `features/` - Gherkin `.feature` files organized by category (01-core-types, 02-cryptography,
  etc.)
- `test-vectors/` - JSON files with deterministic input/output test cases
- `categories/` - Documentation for feature priority levels (required.md, preferred.md, optional.md)
- `tests/` - BDD test implementations for different SDKs (TypeScript, Go, Rust)

## Running Tests

### TypeScript (tests @aptos-labs/ts-sdk)

```bash
cd tests/typescript
bun install
bun test                      # All tests
bun run test:required         # Only @required (P0) tests
bun run test:core-types       # Only @core-types tests
```

### Go (tests aptos-go-sdk)

```bash
cd tests/go
go mod download
make test                     # All tests
make test-required            # Only @required tests
```

### Rust (tests aptos-rust-sdk-v2)

```bash
cd tests/rust
cargo test --test specs       # All tests
make test-required            # Only @required tests
```

## Feature Priority Levels

- **Required (P0)**: Must-have features, tagged `@required` - every SDK needs these
- **Preferred (P1)**: Recommended features, tagged `@preferred` - expected in production SDKs
- **Optional (P2)**: Extended features, tagged `@optional` - for comprehensive SDKs

## Test Tags

Scenarios are tagged for selective execution:

- Priority: `@required`, `@preferred`, `@optional`
- Category: `@core-types`, `@cryptography`, `@accounts`, `@transactions`, `@api-clients`,
  `@advanced`

## Writing Specifications

When adding new specifications:

1. Add design document in appropriate `features/XX-category/spec.md`
2. Write Gherkin scenarios in `.feature` files with appropriate tags
3. For deterministic behaviors, add test vectors to `test-vectors/*.json`
4. Update `feature-matrix.md` if adding new SDK-level features
5. Update category documents (required.md, preferred.md, optional.md) as needed

## Test Vector Format

```json
{
  "version": "1.x",
  "description": "What these vectors test",
  "category_name": [
    {
      "name": "vector_name",
      "description": "What this specific vector tests",
      "input": { ... },
      "expected": { ... }
    }
  ]
}
```

## Formatting

Uses Prettier with `prettier-plugin-gherkin` for Gherkin files.
