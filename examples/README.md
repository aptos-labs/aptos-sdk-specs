# Aptos SDK Examples

Standalone sample applications that demonstrate Aptos SDK features across multiple languages. Each
example is self-contained, runnable, and designed to be a starting point you can expand.

## Examples

| Example                             | Description                                | Languages      |
| ----------------------------------- | ------------------------------------------ | -------------- |
| [batch-transfer](./batch-transfer/) | Send N transactions in parallel with retry | TypeScript, Go |

## Design Principles

Each example:

- **Runs end-to-end** against devnet (no mocks)
- **Shows real patterns** (sequence number management, gas estimation, retry)
- **Has configurable parameters** (transaction count, network)
- **Produces structured output** (JSON summary for easy comparison across SDKs)

## Adding a New Example

1. Create `examples/<name>/` directory
2. Add `examples/<name>/README.md` explaining the scenario
3. Implement in each target language under `examples/<name>/<language>/`
4. Each language directory must be runnable with a single command

## Adding a New Language to an Existing Example

1. Create `examples/<name>/<language>/`
2. Follow the same 4-phase structure: Setup → Batch Submit → Track & Confirm → Verify & Report
3. Use the same CLI flags (`--count`, `--network`) for consistency
4. Output the same JSON summary schema for cross-SDK comparison
