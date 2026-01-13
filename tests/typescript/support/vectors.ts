import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

/**
 * Test vector loading utilities
 */

// Get directory path (works with Bun)
const __dirname = dirname(fileURLToPath(import.meta.url));
const VECTORS_DIR = join(__dirname, "../../../test-vectors");

interface AddressVector {
  name: string;
  description?: string;
  input: string;
  expected: {
    full_hex: string;
    short_string: string;
    bytes_hex?: string;
    last_byte?: number;
  };
}

interface MnemonicVector {
  name: string;
  description?: string;
  input: {
    mnemonic: string;
    passphrase: string;
    derivation_path: string;
  };
  expected: {
    seed_hex?: string;
    private_key_hex?: string;
    public_key_hex?: string;
    auth_key_hex?: string;
    address?: string;
  };
}

interface BcsVector {
  name: string;
  type: string;
  value: any;
  bcs_hex: string;
}

interface HashVector {
  name: string;
  input?: string;
  input_hex: string;
  expected_hex: string;
}

let addressVectors: any = null;
let mnemonicVectors: any = null;
let signatureVectors: any = null;
let transactionVectors: any = null;
let bcsVectors: any = null;
let typeTagVectors: any = null;

/**
 * Load a test vector file
 */
function loadVectorFile(filename: string): any {
  const filepath = join(VECTORS_DIR, filename);
  const content = readFileSync(filepath, "utf-8");
  return JSON.parse(content);
}

/**
 * Get address test vectors
 */
export function getAddressVectors(): typeof addressVectors {
  if (!addressVectors) {
    addressVectors = loadVectorFile("addresses.json");
  }
  return addressVectors;
}

/**
 * Get address parsing vectors
 */
export function getAddressParsingVectors(): AddressVector[] {
  return getAddressVectors().parsing_vectors;
}

/**
 * Get address constants (ZERO, ONE, etc.)
 */
export function getAddressConstants(): any[] {
  return getAddressVectors().constants;
}

/**
 * Get invalid address inputs
 */
export function getInvalidAddressInputs(): any[] {
  return getAddressVectors().invalid_inputs;
}

/**
 * Get mnemonic test vectors
 */
export function getMnemonicVectors(): typeof mnemonicVectors {
  if (!mnemonicVectors) {
    mnemonicVectors = loadVectorFile("mnemonics.json");
  }
  return mnemonicVectors;
}

/**
 * Get Ed25519 derivation vectors
 */
export function getEd25519DerivationVectors(): MnemonicVector[] {
  return getMnemonicVectors().ed25519_derivation_vectors;
}

/**
 * Get signature test vectors
 */
export function getSignatureVectors(): typeof signatureVectors {
  if (!signatureVectors) {
    signatureVectors = loadVectorFile("signatures.json");
  }
  return signatureVectors;
}

/**
 * Get SHA3-256 hash vectors
 */
export function getSha3256Vectors(): HashVector[] {
  return getSignatureVectors().hashing.sha3_256;
}

/**
 * Get SHA2-256 hash vectors
 */
export function getSha256Vectors(): HashVector[] {
  return getSignatureVectors().hashing.sha2_256;
}

/**
 * Get transaction test vectors
 */
export function getTransactionVectors(): typeof transactionVectors {
  if (!transactionVectors) {
    transactionVectors = loadVectorFile("transactions.json");
  }
  return transactionVectors;
}

/**
 * Get BCS encoding vectors
 */
export function getBcsVectors(): typeof bcsVectors {
  if (!bcsVectors) {
    bcsVectors = loadVectorFile("bcs.json");
  }
  return bcsVectors;
}

/**
 * Get BCS primitive vectors
 */
export function getBcsPrimitiveVectors(type: string): BcsVector[] {
  const bcs = getBcsVectors();
  return bcs.primitives[type] || [];
}

/**
 * Get type tag test vectors
 */
export function getTypeTagVectors(): typeof typeTagVectors {
  if (!typeTagVectors) {
    typeTagVectors = loadVectorFile("type-tags.json");
  }
  return typeTagVectors;
}

/**
 * Convert hex string to Uint8Array
 */
export function hexToBytes(hex: string): Uint8Array {
  const cleanHex = hex.startsWith("0x") ? hex.slice(2) : hex;
  const bytes = new Uint8Array(cleanHex.length / 2);
  for (let i = 0; i < bytes.length; i++) {
    bytes[i] = parseInt(cleanHex.slice(i * 2, i * 2 + 2), 16);
  }
  return bytes;
}

/**
 * Convert Uint8Array to hex string
 */
export function bytesToHex(bytes: Uint8Array, prefix = true): string {
  const hex = Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return prefix ? `0x${hex}` : hex;
}
