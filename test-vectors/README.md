# Test Vectors

This directory contains deterministic test vectors for validating SDK implementations. All values in
these files should produce identical results across all SDK implementations.

## Overview

Test vectors provide known input/output pairs that every SDK implementation must pass. They ensure
cryptographic operations, serialization, and address handling are consistent across languages.

## Files

### Core Types

- **`addresses.json`** - Address parsing, formatting, and BCS serialization vectors
- **`type-tags.json`** - TypeTag parsing and serialization (primitives, vectors, structs)
- **`bcs.json`** - Comprehensive BCS encoding vectors for all primitive types

### Cryptography

- **`signatures.json`** - Ed25519 and Secp256k1 key derivation, signing, verification
- **`mnemonics.json`** - BIP-39/BIP-44 mnemonic derivation for Aptos (coin type 637)

### Transactions

- **`transactions.json`** - Transaction building, signing messages, BCS structure
- **`multi-sig.json`** - Multi-Ed25519, multi-agent, and fee payer transaction vectors

## Usage

Each test vector file follows this structure:

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

### Implementing Tests

1. Parse the JSON test vector file
2. For each vector in the relevant category:
   - Extract the `input` values
   - Perform the operation being tested
   - Compare result to `expected` values
3. All vectors must pass for SDK conformance

### Example: Address Parsing Test (Pseudocode)

```python
vectors = load_json("addresses.json")
for v in vectors["parsing_vectors"]:
    address = parse_address(v["input"])
    assert address.to_full_hex() == v["expected"]["full_hex"]
    assert address.to_short_string() == v["expected"]["short_string"]
```

### Example: BCS Encoding Test (Pseudocode)

```typescript
const vectors = loadJson("bcs.json");
for (const v of vectors.primitives.u64) {
  const encoded = bcsEncode(BigInt(v.value), "u64");
  expect(toHex(encoded)).toBe(v.bcs_hex);
}
```

## Key Invariants

### Addresses

- All addresses are exactly 32 bytes when serialized
- Short form removes leading zeros (e.g., `0x1` not `0x000...001`)
- Parsing is case-insensitive for hex characters
- `0x` prefix is optional for parsing

### BCS Encoding

- Little-endian byte order for multi-byte integers
- ULEB128 for lengths (vectors, strings)
- Structs serialized in field declaration order
- Enums have variant index prefix (ULEB128)

### Cryptographic Keys

- Ed25519 private keys: 32 bytes (seed), public keys: 32 bytes, signatures: 64 bytes
- Secp256k1 private keys: 32 bytes, public keys: 33 (compressed) or 65 (uncompressed), signatures:
  64 bytes
- Authentication key: SHA3-256(public_key_bytes || scheme_identifier)

### Mnemonic Derivation

- Uses BIP-39 English wordlist
- Aptos coin type: 637 (hardened: 637')
- Default path: `m/44'/637'/0'/0'/0'`
- Different indexes produce different addresses

## Contributing

When adding new test vectors:

1. Include at least 3-5 vectors per category
2. Test edge cases (empty, max values, special characters)
3. Include invalid input vectors with expected errors
4. Document any implementation-specific behaviors
5. Verify vectors against at least two SDK implementations

## Version History

- **1.0** - Initial test vectors
- **1.1** - Expanded with actual computed values and more edge cases
