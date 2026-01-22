# TypeScript Step Implementation Plan

> **Updated:** 2026-01-22
>
> **Current Status:** 578/739 scenarios (~78%)
> - Required (P0): ~300/306 (98%)
> - Preferred (P1): ~168/183 (92%)
> - Optional (P2): ~110/250 (44%)

## Summary of Missing Scenarios

Total undefined scenarios: 161 (down from 163)

### By Priority Level (After Updates)

| Priority | Missing | Feature Areas |
|----------|---------|---------------|
| Required | ~6 | Transaction submission (4), Error handling (2) |
| Preferred | ~15 | Simulation (13), Fee-payer (2) |
| Optional | ~140 | BLS12381 (35), Codegen (34), Indexer (~24), Multi-agent/Fee-payer/Multi-sig/Keyless (~47) |

---

## Completed Work

### Phase 1: Simulation Steps (simulation.steps.ts)
- [x] Added step definitions for basic simulation scenarios
- [x] Added gas estimation via simulation steps
- [x] Added state/event preview steps
- [x] Added failure preview steps
- [x] Added simulation options steps

### Phase 2: Gas Estimation Steps (gas-estimation.steps.ts)
- [x] Added `error should indicate insufficient balance` step
- [x] Added `When I request gas estimate` step

### Phase 3: Secp256k1 Steps (cryptography.steps.ts)
- [x] Added hex key creation steps
- [x] Added invalid key rejection steps
- [x] Added compressed/uncompressed public key steps
- [x] Added pre-hashed message signing steps
- [x] Added authentication key derivation steps
- [x] Added test vector steps

### Phase 4: Indexer Steps (indexer.steps.ts - NEW FILE)
- [x] Created new indexer.steps.ts file
- [x] Added client configuration steps
- [x] Added GraphQL query steps
- [x] Added token/NFT query steps
- [x] Added fungible asset steps
- [x] Added collection steps
- [x] Added event query steps
- [x] Added error handling steps

---

## Remaining Work

### Still Missing - Simulation (13 scenarios)
These scenarios have step definitions but patterns may not match exactly:
- [ ] Simulate valid transaction - step pattern mismatch
- [ ] Simulate without signing - step pattern mismatch
- [ ] Simulation result includes changes - step pattern mismatch
- [ ] Use simulation for gas estimation - step pattern mismatch
- [ ] Gas varies by transaction complexity - step pattern mismatch
- [ ] Preview balance changes - step pattern mismatch
- [ ] Preview resource changes - step pattern mismatch
- [ ] Preview events - step pattern mismatch
- [ ] Simulation shows abort - step pattern mismatch
- [ ] Simulation shows insufficient balance - step pattern mismatch
- [ ] Simulation shows type errors - step pattern mismatch
- [ ] Simulation catches access errors - step pattern mismatch
- [ ] Simulate multi-agent/fee payer transaction - step pattern mismatch

### Still Missing - Fee-payer & Multi-agent Edge Cases (~9 scenarios)
- [ ] Fee payer signing message includes fee payer address
- [ ] Fee payer signing message uses correct domain
- [ ] Sign fee payer transaction
- [ ] Signatures can be collected in any order
- [ ] Reject incomplete signature collection
- [ ] Reject mismatched secondary signer count
- [ ] Reject empty secondary signers
- [ ] Secondary signer address must match signature
- [ ] Multi-agent signing message uses correct domain

### Skip - SDK Limitations

#### BLS12-381 (35 scenarios) - @optional
**Status:** SDK does not support BLS12-381. These scenarios cannot be implemented.

#### Codegen (34 scenarios) - @optional
**Status:** Code generation is not a TypeScript SDK feature. Skip.

### Indexer - Partially Implemented
Step definitions added in `indexer.steps.ts` but some scenarios still have pattern mismatches:
- [ ] Check indexer processor status
- [ ] Indexer lag detection
- [ ] Handle indexer unavailable
- [ ] Handle query timeout
- [ ] Handle malformed response

### Multi-signature (~3 scenarios)
- [ ] Sign with enough private keys
- [ ] Collect signatures from multiple parties
- [ ] Multi-sig transaction authenticator structure

### Keyless (~3 scenarios)
- [ ] Sign message with keyless account
- [ ] Sign transaction with keyless account
- [ ] Reject signing with expired ephemeral key

---

## Commands

```bash
# Run all tests
bun test

# Dry run to see undefined steps
bun run cucumber-js --dry-run --format summary

# Run specific feature
bun run cucumber-js ../../features/06-advanced/simulation.feature

# Run with specific tags
bun run test:required
bun run test:preferred
```

---

## Summary

### What Was Done
1. **simulation.steps.ts** - Added ~50 new step definitions for simulation scenarios
2. **gas-estimation.steps.ts** - Added 2 missing step patterns
3. **cryptography.steps.ts** - Added ~30 new Secp256k1 step definitions
4. **indexer.steps.ts** - Created new file with ~60 step definitions

### What Remains
1. **BLS12381** (35) - Not supported by SDK, skip
2. **Codegen** (34) - Not a SDK feature, skip
3. **Pattern mismatches** (~30) - Step definitions exist but Gherkin patterns don't match
4. **Edge cases** (~20) - Multi-agent, fee-payer, multi-sig validation scenarios

### Recommendations
1. Run actual tests (not dry-run) to see which scenarios pass
2. Fix remaining pattern mismatches in simulation.steps.ts
3. Add validation edge cases for multi-agent/fee-payer
4. Consider marking BLS12381 and Codegen as "N/A" in FEATURE_COVERAGE.md
