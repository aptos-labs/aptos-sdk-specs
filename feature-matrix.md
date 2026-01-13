# SDK Feature Matrix

This document compares feature availability across official Aptos SDK implementations.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Fully implemented |
| 🔶 | Partially implemented |
| ❌ | Not implemented |
| 📋 | Planned |

## Reference SDKs

| SDK | Repository | Primary Language |
|-----|------------|------------------|
| **TS** | [aptos-ts-sdk](https://github.com/aptos-labs/aptos-ts-sdk) | TypeScript |
| **PY** | [aptos-python-sdk](https://github.com/aptos-labs/aptos-python-sdk) | Python |
| **GO** | [aptos-go-sdk](https://github.com/aptos-labs/aptos-go-sdk) | Go |
| **NET** | [aptos-dotnet-sdk](https://github.com/aptos-labs/aptos-dotnet-sdk) | C# |

---

## Core Types (P0)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| AccountAddress parsing | ✅ | ✅ | ✅ | ✅ | All support 0x prefix |
| AccountAddress formatting | ✅ | ✅ | ✅ | ✅ | Short and full formats |
| ChainId | ✅ | ✅ | ✅ | ✅ | |
| TypeTag parsing | ✅ | ✅ | ✅ | ✅ | |
| MoveStructTag | ✅ | ✅ | ✅ | ✅ | |
| U256 support | ✅ | ✅ | ✅ | ✅ | BigInt in TS/PY |
| HashValue | ✅ | ✅ | ✅ | ✅ | |

---

## Cryptography

### Required (P0)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Ed25519 key generation | ✅ | ✅ | ✅ | ✅ | |
| Ed25519 signing | ✅ | ✅ | ✅ | ✅ | |
| Ed25519 verification | ✅ | ✅ | ✅ | ✅ | |
| SHA3-256 | ✅ | ✅ | ✅ | ✅ | |
| SHA2-256 | ✅ | ✅ | ✅ | ✅ | For BIP-39 |
| Authentication key | ✅ | ✅ | ✅ | ✅ | |

### Preferred (P1)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Secp256k1 ECDSA | ✅ | ✅ | ✅ | ✅ | |
| BIP-39 mnemonics | ✅ | ✅ | ✅ | ✅ | |
| BIP-44 derivation | ✅ | ✅ | ✅ | ✅ | |

### Optional (P2)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Secp256r1 (P-256) | ✅ | 🔶 | ✅ | ✅ | WebAuthn support |
| BLS12-381 | 🔶 | ❌ | ❌ | ❌ | Limited support |
| Multi-Ed25519 | ✅ | ✅ | ✅ | ✅ | |
| MultiKey | ✅ | 🔶 | 🔶 | 🔶 | Mixed key types |

---

## Account Management

### Required (P0)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Ed25519 account | ✅ | ✅ | ✅ | ✅ | |
| From private key | ✅ | ✅ | ✅ | ✅ | |
| From hex string | ✅ | ✅ | ✅ | ✅ | |
| Random generation | ✅ | ✅ | ✅ | ✅ | |
| Get address | ✅ | ✅ | ✅ | ✅ | |
| Sign message | ✅ | ✅ | ✅ | ✅ | |

### Preferred (P1)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| From mnemonic | ✅ | ✅ | ✅ | ✅ | |
| Custom derivation path | ✅ | ✅ | ✅ | ✅ | |
| Secp256k1 account | ✅ | ✅ | ✅ | ✅ | |

### Optional (P2)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Multi-sig account | ✅ | ✅ | ✅ | 🔶 | |
| MultiKey account | ✅ | 🔶 | 🔶 | 🔶 | |
| Keyless account | ✅ | ❌ | ❌ | ❌ | TS only currently |

---

## Transaction Building

### Required (P0)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| RawTransaction | ✅ | ✅ | ✅ | ✅ | |
| EntryFunction payload | ✅ | ✅ | ✅ | ✅ | |
| APT transfer | ✅ | ✅ | ✅ | ✅ | |
| BCS serialization | ✅ | ✅ | ✅ | ✅ | |
| Single-signer signing | ✅ | ✅ | ✅ | ✅ | |
| SignedTransaction | ✅ | ✅ | ✅ | ✅ | |

### Preferred (P1)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Transaction builder | ✅ | ✅ | ✅ | ✅ | Fluent API |
| Transaction simulation | ✅ | ✅ | ✅ | ✅ | |
| Gas estimation | ✅ | ✅ | ✅ | ✅ | |

### Optional (P2)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Script payload | ✅ | ✅ | ✅ | 🔶 | |
| Multi-agent | ✅ | ✅ | ✅ | ✅ | |
| Fee payer | ✅ | ✅ | ✅ | ✅ | |
| Batch transactions | ✅ | 🔶 | 🔶 | ❌ | |

---

## API Clients

### Required (P0)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Fullnode client | ✅ | ✅ | ✅ | ✅ | |
| Ledger info | ✅ | ✅ | ✅ | ✅ | |
| Account info | ✅ | ✅ | ✅ | ✅ | |
| Account resources | ✅ | ✅ | ✅ | ✅ | |
| Submit transaction | ✅ | ✅ | ✅ | ✅ | |
| Wait for transaction | ✅ | ✅ | ✅ | ✅ | |
| Get transaction by hash | ✅ | ✅ | ✅ | ✅ | |

### Preferred (P1)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| View functions | ✅ | ✅ | ✅ | ✅ | |
| Gas estimation | ✅ | ✅ | ✅ | ✅ | |
| Faucet client | ✅ | ✅ | ✅ | ✅ | |
| Account modules | ✅ | ✅ | ✅ | ✅ | |
| Events by handle | ✅ | ✅ | ✅ | ✅ | |

### Optional (P2)

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Indexer GraphQL | ✅ | ✅ | 🔶 | 🔶 | |
| Block queries | ✅ | ✅ | ✅ | ✅ | |
| Table queries | ✅ | ✅ | ✅ | 🔶 | |
| WebSocket | ❌ | ❌ | ❌ | ❌ | None yet |

---

## Advanced Features

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Code generation | ✅ | ❌ | 🔶 | ❌ | |
| Type-safe bindings | ✅ | ❌ | ❌ | ❌ | TS has codegen |
| Auto-retry | ✅ | ✅ | ✅ | ✅ | |
| Request timeout | ✅ | ✅ | ✅ | ✅ | |

---

## Error Handling

| Feature | TS | PY | GO | NET | Notes |
|---------|----|----|----|----|-------|
| Typed errors | ✅ | ✅ | ✅ | ✅ | |
| Error codes | ✅ | ✅ | ✅ | ✅ | |
| Error context | ✅ | 🔶 | ✅ | 🔶 | |
| VM error parsing | ✅ | ✅ | ✅ | 🔶 | |

---

## Platform Support

| Platform | TS | PY | GO | NET | Notes |
|----------|----|----|----|----|-------|
| Linux | ✅ | ✅ | ✅ | ✅ | |
| macOS | ✅ | ✅ | ✅ | ✅ | |
| Windows | ✅ | ✅ | ✅ | ✅ | |
| Browser | ✅ | ❌ | ❌ | 🔶 | TS native, .NET via Blazor |
| iOS | 🔶 | ❌ | ❌ | ✅ | .NET MAUI |
| Android | 🔶 | ❌ | ❌ | ✅ | .NET MAUI |

---

## Summary by Priority

### P0 (Required) Compliance

| SDK | Status | Notes |
|-----|--------|-------|
| TypeScript | ✅ 100% | Reference implementation |
| Python | ✅ 100% | |
| Go | ✅ 100% | |
| .NET | ✅ 100% | |

### P1 (Preferred) Compliance

| SDK | Status | Notes |
|-----|--------|-------|
| TypeScript | ✅ 100% | |
| Python | ✅ ~95% | Minor gaps |
| Go | ✅ ~95% | Minor gaps |
| .NET | ✅ ~90% | Some features partial |

### P2 (Optional) Compliance

| SDK | Status | Notes |
|-----|--------|-------|
| TypeScript | ✅ ~85% | Most advanced |
| Python | 🔶 ~60% | Core optional features |
| Go | 🔶 ~60% | Core optional features |
| .NET | 🔶 ~50% | Growing |

---

## Notes

1. **TypeScript SDK** is considered the reference implementation with the most complete feature set
2. Feature availability is based on latest stable releases
3. This matrix should be updated as SDKs evolve
4. "Partial" implementation means the feature exists but may lack some capabilities

