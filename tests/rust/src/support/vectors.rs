//! Test vector loading utilities.
//!
//! Loads deterministic test vectors from the shared JSON files.

use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

/// Get the path to the test vectors directory.
fn vectors_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("..")
        .join("test-vectors")
}

// =============================================================================
// Address Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct AddressVectors {
    pub version: String,
    pub description: String,
    pub parsing_vectors: Vec<AddressParsingVector>,
    pub constants: Vec<AddressConstant>,
    pub invalid_inputs: Vec<InvalidAddressInput>,
    pub bcs_serialization: Vec<BcsSerializationVector>,
}

#[derive(Debug, Deserialize)]
pub struct AddressParsingVector {
    pub name: String,
    pub description: String,
    pub input: String,
    pub expected: AddressExpected,
}

#[derive(Debug, Deserialize)]
pub struct AddressExpected {
    pub full_hex: String,
    pub short_string: String,
    #[serde(default)]
    pub bytes_hex: Option<String>,
    #[serde(default)]
    pub last_byte: Option<u8>,
    #[serde(default)]
    pub last_two_bytes_hex: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct AddressConstant {
    pub name: String,
    pub description: String,
    pub expected: AddressConstantExpected,
}

#[derive(Debug, Deserialize)]
pub struct AddressConstantExpected {
    pub full_hex: String,
    pub short_string: String,
    #[serde(default)]
    pub bytes: Option<Vec<u8>>,
}

#[derive(Debug, Deserialize)]
pub struct InvalidAddressInput {
    pub name: String,
    pub input: String,
    pub expected_error: Option<String>,
    pub reason: String,
    #[serde(default)]
    pub note: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct BcsSerializationVector {
    pub name: String,
    pub description: String,
    pub input: String,
    pub expected: BcsExpected,
}

#[derive(Debug, Deserialize)]
pub struct BcsExpected {
    pub bcs_hex: String,
    pub length: usize,
}

impl AddressVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("addresses.json");
        let content = fs::read_to_string(&path)?;
        let vectors: AddressVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}

// =============================================================================
// Signature Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct SignatureVectors {
    pub version: String,
    pub ed25519: Vec<Ed25519TestVector>,
    #[serde(default)]
    pub secp256k1: Vec<Secp256k1TestVector>,
}

#[derive(Debug, Deserialize)]
pub struct Ed25519TestVector {
    pub name: String,
    pub description: String,
    pub private_key_hex: String,
    pub public_key_hex: String,
    #[serde(default)]
    pub address_hex: Option<String>,
    #[serde(default)]
    pub message_hex: Option<String>,
    #[serde(default)]
    pub signature_hex: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct Secp256k1TestVector {
    pub name: String,
    pub description: String,
    pub private_key_hex: String,
    pub public_key_hex: String,
    #[serde(default)]
    pub address_hex: Option<String>,
    #[serde(default)]
    pub message_hex: Option<String>,
    #[serde(default)]
    pub signature_hex: Option<String>,
}

impl SignatureVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("signatures.json");
        let content = fs::read_to_string(&path)?;
        let vectors: SignatureVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}

// =============================================================================
// Mnemonic Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct MnemonicVectors {
    pub version: String,
    pub derivation_vectors: Vec<MnemonicDerivationVector>,
}

#[derive(Debug, Deserialize)]
pub struct MnemonicDerivationVector {
    pub name: String,
    pub description: String,
    pub mnemonic: String,
    pub passphrase: String,
    pub derivation_path: String,
    pub expected: MnemonicExpected,
}

#[derive(Debug, Deserialize)]
pub struct MnemonicExpected {
    pub private_key_hex: String,
    pub public_key_hex: String,
    pub address_hex: String,
}

impl MnemonicVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("mnemonics.json");
        let content = fs::read_to_string(&path)?;
        let vectors: MnemonicVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}

// =============================================================================
// Type Tag Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct TypeTagVectors {
    pub version: String,
    pub primitives: Vec<TypeTagVector>,
    pub vectors: Vec<TypeTagVector>,
    pub structs: Vec<TypeTagVector>,
    pub invalid: Vec<InvalidTypeTagVector>,
}

#[derive(Debug, Deserialize)]
pub struct TypeTagVector {
    pub name: String,
    pub input: String,
    pub expected: TypeTagExpected,
}

#[derive(Debug, Deserialize)]
pub struct TypeTagExpected {
    pub canonical: String,
    #[serde(default)]
    pub bcs_hex: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct InvalidTypeTagVector {
    pub name: String,
    pub input: String,
    pub reason: String,
}

impl TypeTagVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("type-tags.json");
        let content = fs::read_to_string(&path)?;
        let vectors: TypeTagVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}

// =============================================================================
// BCS Serialization Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct BcsVectors {
    pub version: String,
    pub primitives: Vec<BcsPrimitiveVector>,
    #[serde(default)]
    pub strings: Vec<BcsStringVector>,
    #[serde(default)]
    pub sequences: Vec<BcsSequenceVector>,
}

#[derive(Debug, Deserialize)]
pub struct BcsPrimitiveVector {
    pub name: String,
    #[serde(rename = "type")]
    pub type_name: String,
    pub value: serde_json::Value,
    pub expected_hex: String,
}

#[derive(Debug, Deserialize)]
pub struct BcsStringVector {
    pub name: String,
    pub value: String,
    pub expected_hex: String,
}

#[derive(Debug, Deserialize)]
pub struct BcsSequenceVector {
    pub name: String,
    #[serde(rename = "type")]
    pub type_name: String,
    pub value: Vec<serde_json::Value>,
    pub expected_hex: String,
}

impl BcsVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("bcs.json");
        let content = fs::read_to_string(&path)?;
        let vectors: BcsVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}

// =============================================================================
// Transaction Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct TransactionVectors {
    pub version: String,
    #[serde(default)]
    pub raw_transactions: Vec<RawTransactionVector>,
    #[serde(default)]
    pub signed_transactions: Vec<SignedTransactionVector>,
}

#[derive(Debug, Deserialize)]
pub struct RawTransactionVector {
    pub name: String,
    pub description: String,
    pub fields: RawTransactionFields,
    pub expected: TransactionExpected,
}

#[derive(Debug, Deserialize)]
pub struct RawTransactionFields {
    pub sender: String,
    pub sequence_number: u64,
    pub max_gas_amount: u64,
    pub gas_unit_price: u64,
    pub expiration_timestamp_secs: u64,
    pub chain_id: u8,
    pub payload_type: String,
    #[serde(default)]
    pub payload_module: Option<String>,
    #[serde(default)]
    pub payload_function: Option<String>,
    #[serde(default)]
    pub payload_type_args: Option<Vec<String>>,
    #[serde(default)]
    pub payload_args: Option<Vec<String>>,
}

#[derive(Debug, Deserialize)]
pub struct TransactionExpected {
    #[serde(default)]
    pub bcs_hex: Option<String>,
    #[serde(default)]
    pub signing_message_hex: Option<String>,
    #[serde(default)]
    pub hash: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct SignedTransactionVector {
    pub name: String,
    pub description: String,
    pub private_key_hex: String,
    pub raw_transaction_bcs: String,
    pub expected: SignedTransactionExpected,
}

#[derive(Debug, Deserialize)]
pub struct SignedTransactionExpected {
    pub bcs_hex: String,
    pub hash: String,
}

impl TransactionVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("transactions.json");
        let content = fs::read_to_string(&path)?;
        let vectors: TransactionVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}

// =============================================================================
// Multi-Signature Test Vectors
// =============================================================================

#[derive(Debug, Deserialize)]
pub struct MultiSigVectors {
    pub version: String,
    #[serde(default)]
    pub multi_ed25519: Vec<MultiEd25519Vector>,
    #[serde(default)]
    pub multi_key: Vec<MultiKeyVector>,
}

#[derive(Debug, Deserialize)]
pub struct MultiEd25519Vector {
    pub name: String,
    pub description: String,
    pub public_keys_hex: Vec<String>,
    pub threshold: u8,
    pub expected: MultiSigExpected,
}

#[derive(Debug, Deserialize)]
pub struct MultiKeyVector {
    pub name: String,
    pub description: String,
    pub keys: Vec<MultiKeyEntry>,
    pub threshold: u8,
    pub expected: MultiSigExpected,
}

#[derive(Debug, Deserialize)]
pub struct MultiKeyEntry {
    pub key_type: String,
    pub public_key_hex: String,
}

#[derive(Debug, Deserialize)]
pub struct MultiSigExpected {
    pub public_key_bcs_hex: String,
    pub address_hex: String,
}

impl MultiSigVectors {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let path = vectors_dir().join("multi-sig.json");
        let content = fs::read_to_string(&path)?;
        let vectors: MultiSigVectors = serde_json::from_str(&content)?;
        Ok(vectors)
    }
}
