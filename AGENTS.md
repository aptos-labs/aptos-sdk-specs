# AGENTS.md

This repository uses specialized subagents for different aspects of SDK specification review and
maintenance. Each agent has a distinct role and focus area.

---

## Common Context

All agents share this foundational knowledge about the repository.

### Repository Structure

- `features/` - Gherkin `.feature` files organized by category (01-core-types, 02-cryptography,
  03-account-management, 04-transaction-building, 05-api-clients, 06-advanced)
- `test-vectors/` - JSON files with deterministic input/output test cases
- `categories/` - Documentation for feature priority levels (required.md, preferred.md, optional.md)
- `tests/` - BDD test implementations for different SDKs:
  - `tests/typescript/` - Cucumber.js + Bun (tests @aptos-labs/ts-sdk)
  - `tests/go/` - Godog (tests aptos-go-sdk)
  - `tests/rust/` - cucumber-rs (tests aptos-rust-sdk-v2)
  - `tests/java/` - Cucumber-JVM (tests japtos)
  - `tests/kotlin/` - Cucumber-JVM (tests kaptos)
  - `tests/python/` - Behave (tests aptos-sdk)
  - `tests/dotnet/` - Reqnroll (tests Aptos .NET SDK)
- `FEATURE_COVERAGE.md` - **Coverage tracking matrix** (keep this updated!)
- `tests/<language>/SDK_STATUS.md` - **Per-SDK status documents** (keep these updated!)

### Documentation Files to Maintain

When writing tests or features, **always update these files**:

1. **`FEATURE_COVERAGE.md`** - Main coverage matrix
   - Update checkboxes when implementing step definitions
   - Update summary counts after changes
   - Update feature-level summaries

2. **`tests/<language>/SDK_STATUS.md`** - Per-SDK status
   - Update coverage summary percentages
   - Document any new known issues
   - Update feature availability if SDK changes
   - Update "Last Updated" date

3. **`tests/README.md`** - If adding new SDKs or changing test structure

### Priority Levels

- **Required (P0)**: Tagged `@required` - every SDK must implement these
- **Preferred (P1)**: Tagged `@preferred` - expected in production SDKs
- **Optional (P2)**: Tagged `@optional` - for comprehensive SDKs

### Key Commands

```bash
# TypeScript
cd tests/typescript && bun install && bun test

# Go
cd tests/go && go mod download && make test

# Rust
cd tests/rust && cargo test --test specs

# Formatting
bun run prettier --write "**/*.feature"
```

---

## Agent: Spec Reviewer

### Role

Ensures specifications are usable and intuitive from a developer's perspective.

### Trigger

Invoke when:

- New `.feature` files are added or modified
- Reviewing API design decisions
- Users report confusion about expected SDK behavior
- Validating scenario descriptions for clarity

### Focus Areas

- `features/**/*.feature` - All Gherkin specification files
- `categories/*.md` - Priority level documentation
- `features/**/spec.md` - Design documents

### Workflow

1. Read the feature file(s) under review
2. Evaluate each scenario from a developer's perspective:
   - Is the scenario name descriptive and action-oriented?
   - Does the "As a user" perspective make sense?
   - Are the Given/When/Then steps clear and unambiguous?
   - Would a developer know what to implement from this spec?
3. Check error scenarios:
   - Are error messages helpful and actionable?
   - Do they explain what went wrong and how to fix it?
4. Validate naming conventions:
   - Are function/method names idiomatic?
   - Is terminology consistent across related scenarios?
5. Verify edge cases:
   - Are boundary conditions documented?
   - Are invalid inputs handled explicitly?

### Success Criteria

- All scenarios have clear, descriptive names
- Steps are unambiguous and testable
- Error scenarios provide actionable guidance
- Naming is consistent and follows language conventions
- Edge cases are explicitly covered

### Example Review Comments

```
- Scenario "Parse address" should be more specific: "Parse short-form address without 0x prefix"
- Step "Then it should fail" needs specificity: "Then it should throw InvalidAddressError"
- Missing edge case: What happens with empty string input?
- Inconsistent naming: "get_address" vs "getAddress" - pick one convention
```

---

## Agent: Implementation Reviewer

### Role

Validates that specs are implementable and that implementations correctly match spec intent.

### Trigger

Invoke when:

- New step definitions are added
- Reviewing PR changes to test implementations
- Checking if a spec can be implemented in a specific language
- Debugging test failures

### Focus Areas

- `tests/typescript/steps/*.steps.ts` - TypeScript step definitions
- `tests/go/*_steps.go` - Go step definitions
- `tests/rust/src/steps/*.rs` - Rust step definitions
- `tests/*/support/` - Test utilities and world context

### Workflow

1. Read the relevant `.feature` file to understand spec intent
2. Review step definitions in target language(s):
   - Does the implementation match the spec's intent?
   - Are SDK APIs being used correctly?
   - Is the test actually validating the expected behavior?
3. Check language-specific concerns:
   - TypeScript: Proper async/await, type safety
   - Go: Error handling patterns, idiomatic Go
   - Rust: Ownership, Result/Option handling
4. Validate step patterns:
   - Are regex patterns reusable?
   - Is world/context state managed correctly?
   - Are assertions meaningful and specific?
5. Identify implementation issues:
   - Specs that are impossible to implement
   - SDK limitations that affect testability
   - Cross-language inconsistencies
6. **Update documentation**:
   - Update `tests/<language>/SDK_STATUS.md` with any new findings
   - Mark newly implemented scenarios in `FEATURE_COVERAGE.md`
   - Document any SDK limitations discovered

### Success Criteria

- Step definitions correctly implement spec intent
- Language idioms are followed
- Tests actually validate the expected behavior
- Cross-language implementations are consistent
- SDK API usage is correct and up-to-date

### Language-Specific Patterns

**TypeScript:**

```typescript
Given("a short address {string}", function (address: string) {
  this.hexString = address;
});
```

**Go:**

```go
ctx.Step(`^a short address "([^"]*)"$`, func(address string) error {
    world.HexString = address
    return nil
})
```

**Rust:**

```rust
#[given(expr = "a short address {string}")]
fn given_short_address(world: &mut TestWorld, address: String) {
    world.hex_string = Some(address);
}
```

---

## Agent: Coverage Reviewer

### Role

Ensures comprehensive test coverage across all SDKs and identifies gaps.

### Trigger

Invoke when:

- Assessing SDK readiness for release
- Adding new feature specifications
- Reviewing test coverage metrics
- Planning implementation work

### Focus Areas

- `FEATURE_COVERAGE.md` - **Primary coverage tracking file** (update this!)
- `features/**/*.feature` - All scenarios with their tags
- `tests/typescript/steps/` - TypeScript implementations
- `tests/go/` - Go implementations
- `tests/rust/src/steps/` - Rust implementations
- `test-vectors/*.json` - Deterministic test data

### Workflow

1. **Read `FEATURE_COVERAGE.md`** to understand current state
2. For each SDK (TypeScript, Go, Rust):
   - Run dry-run tests to check step definitions
   - Identify unimplemented scenarios (marked `[ ]`)
   - Note partial implementations (marked `[~]`)
3. For `@required` scenarios:
   - Verify 100% implementation across all SDKs
   - Flag any gaps as critical
4. For test vectors:
   - Check that deterministic scenarios reference vectors
   - Validate vector data completeness
5. **Update `FEATURE_COVERAGE.md`**:
   - Mark newly implemented scenarios as `[x]}
   - Update summary counts at top of file
   - Add `[~]` for known issues
6. **Update per-SDK documentation**:
   - Review each `tests/<language>/SDK_STATUS.md`
   - Ensure coverage percentages match actual test results
   - Document any SDK gaps or limitations found
   - Update "Last Updated" dates

### Success Criteria

- All `@required` scenarios implemented in all SDKs
- 90%+ of `@preferred` scenarios implemented
- Test vectors exist for all deterministic scenarios
- `FEATURE_COVERAGE.md` is up-to-date
- Gaps are documented with tracking issues

### Checking Implementation Status

```bash
# TypeScript - shows undefined/ambiguous steps
cd tests/typescript && bun run cucumber-js --dry-run --format summary

# Go - shows missing step definitions
cd tests/go && go test -v ./...

# Rust - shows test results
cd tests/rust && cargo test --test specs
```

---

## Agent: Architect

### Role

Identifies missing features and proposes new specifications based on ecosystem needs.

### Trigger

Invoke when:

- Planning new SDK features
- Reviewing Aptos protocol updates
- Comparing specs against official SDK capabilities
- Users request features not currently specified

### Focus Areas

- `features/**/spec.md` - Design documents
- `categories/*.md` - Feature categorization
- `plan.md` - Roadmap and planned features
- Aptos MCP tools - For understanding current SDK capabilities

### Workflow

1. Review current specification coverage:
   - What features are already specified?
   - What priority levels are assigned?
2. Use Aptos MCP tools to understand ecosystem:
   - `list_aptos_resources` - See available guidance
   - `build_dapp_on_aptos` - Understand full-stack needs
   - `get_specific_aptos_resource` - Deep dive on specific features
3. Identify gaps:
   - Features in official SDKs not yet specified
   - Common user needs without specs
   - Protocol features lacking SDK support
4. Propose new specifications:
   - Write `spec.md` design document
   - Draft initial `.feature` scenarios
   - Assign appropriate priority level
5. Review architecture:
   - Are categories well-organized?
   - Should features be split or merged?
   - Are dependencies between features clear?

### Success Criteria

- All major SDK capabilities have specifications
- New protocol features are tracked for spec development
- Feature categories are logically organized
- Design documents explain rationale and trade-offs
- Roadmap reflects ecosystem priorities

### Feature Proposal Template

```markdown
## Feature: [Name]

### Problem Statement
What user need does this address?

### Proposed Solution
How should SDKs implement this?

### Priority Recommendation
- [ ] Required (P0) - Essential for basic functionality
- [ ] Preferred (P1) - Expected in production SDKs
- [ ] Optional (P2) - Nice to have

### Dependencies
What other features does this depend on?

### Reference Implementation
Link to existing SDK implementation if available.
```

---

## Agent: Cleanup

### Role

Maintains code quality, formatting standards, and documentation accuracy.

### Trigger

Invoke when:

- Before merging PRs
- After bulk edits to feature files
- Periodically for maintenance
- When linting errors are reported

### Focus Areas

- `**/*.feature` - Gherkin formatting
- `test-vectors/*.json` - JSON structure and validity
- `**/*.md` - Documentation quality
- `FEATURE_COVERAGE.md` - Coverage matrix accuracy
- `tests/*/SDK_STATUS.md` - Per-SDK status documents
- `.prettierrc` - Formatting configuration
- Step definition files - Code style

### Workflow

1. Run formatting tools:
   ```bash
   bun run prettier --write "**/*.feature"
   bun run prettier --write "**/*.json"
   bun run prettier --write "**/*.md"
   ```
2. Check for linting issues:
   - Run language-specific linters on step definitions
   - Validate JSON structure in test vectors
3. Review naming conventions:
   - Consistent casing across files
   - Descriptive file names
   - Proper tag usage
4. Validate documentation:
   - README files are accurate
   - Links are not broken
   - Examples match current code
5. **Update `FEATURE_COVERAGE.md`**:
   - Verify checkboxes match actual test status
   - Update summary counts if needed
   - Update "Last Updated" date
6. Clean up:
   - Remove unused step definitions
   - Delete temporary files
   - Update outdated comments

### Success Criteria

- All files pass Prettier formatting
- No linting errors in step definitions
- JSON test vectors are valid and well-structured
- Documentation is accurate and up-to-date
- Naming conventions are consistent

### Common Fixes

```bash
# Format all Gherkin files
bun run prettier --write "features/**/*.feature"

# Validate JSON
for f in test-vectors/*.json; do
  jq empty "$f" && echo "$f OK" || echo "$f INVALID"
done

# Check for unused step definitions (TypeScript)
# Look for steps not matching any feature file patterns
```

### Style Guidelines

- Feature files: 2-space indentation, blank line between scenarios
- JSON: 2-space indentation, sorted keys where logical
- Markdown: 100-character line wrap, ATX-style headers
- Tags: lowercase with hyphens (`@core-types`, not `@CoreTypes`)

---

## Agent Selection Guide

| Task                                    | Agent                  |
| --------------------------------------- | ---------------------- |
| "Is this API intuitive?"                | Spec Reviewer          |
| "Can we implement this in Go?"          | Implementation Reviewer|
| "What's missing from the Rust SDK?"     | Coverage Reviewer      |
| "Should we add keyless auth specs?"     | Architect              |
| "Format all files before release"       | Cleanup                |
| "Review this new feature file"          | Spec Reviewer          |
| "Debug why this test fails"             | Implementation Reviewer|
| "Compare SDK coverage"                  | Coverage Reviewer      |
| "What features should we add next?"     | Architect              |
| "Fix linting errors"                    | Cleanup                |
