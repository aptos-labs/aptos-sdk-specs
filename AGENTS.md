# Repository Guidelines

## Project Structure & Module Organization

- `features/` holds Gherkin specs grouped by domain (e.g., `features/01-core-types/`). Each folder
  includes a `spec.md` plus `*.feature` files.
- `test-vectors/` contains deterministic JSON vectors (`addresses.json`, `transactions.json`, etc.)
  referenced by tests.
- `tests/` hosts executable BDD test implementations per language: `tests/typescript/`, `tests/go/`,
  and `tests/rust/`.
- `categories/` lists required/preferred/optional feature tiers and `feature-matrix.md` tracks
  coverage.

## Build, Test, and Development Commands

Run tests from `tests/` subdirectories:

- TypeScript (Bun + Cucumber): `cd tests/typescript && bun install && bun test`
- Go (Godog): `cd tests/go && go mod download && make test`
- Rust (cucumber-rs): `cd tests/rust && cargo test --test specs`
- Tag subsets are supported (example): `bun run test:required` or `make test-cryptography`.

## Coding Style & Naming Conventions

- Keep formatting consistent with neighboring files; no repo-wide formatter config is enforced here.
- Feature files use descriptive scenario names and tags like `@required` or `@cryptography`.
- Step definitions follow language patterns: `*.steps.ts`, `*_steps.go`, and Rust modules in
  `tests/rust/src/steps/`.
- Test vectors are snake_case JSON keys; keep new vectors deterministic and documented in
  `test-vectors/README.md`.

## Testing Guidelines

- Frameworks: Cucumber.js (TypeScript), Godog (Go), cucumber-rs (Rust).
- Coverage targets follow `tests/README.md` (P0 required at 100%).
- Add or update `.feature` files alongside step definitions and vectors so tests stay in sync.

## Commit & Pull Request Guidelines

- Commit history favors short, imperative subjects with optional scopes like `[ci]` or `[README]`
  and PR refs (e.g., `Add ... (#6)`).
- PRs should describe spec changes, list affected features/tests, and link related issues or SDKs
  when relevant.

## Agent-Specific Notes

- New behaviors should include a `spec.md`, matching `*.feature` scenarios, and test vectors when
  deterministic.
