//! Test world - holds state between Cucumber steps.

use aptos_rust_sdk_v2::account::{Ed25519Account, MultiEd25519Account};
use aptos_rust_sdk_v2::api::{FaucetClient, FullnodeClient};
use aptos_rust_sdk_v2::crypto::{
    Ed25519PrivateKey, Ed25519PublicKey, Ed25519Signature, MultiEd25519PublicKey,
    MultiEd25519Signature, Secp256k1PrivateKey, Secp256k1PublicKey, Secp256k1Signature,
    Secp256r1PrivateKey, Secp256r1PublicKey, Secp256r1Signature,
};
use aptos_rust_sdk_v2::transaction::authenticator::TransactionAuthenticator;
use aptos_rust_sdk_v2::transaction::types::{FeePayerRawTransaction, MultiAgentRawTransaction};
use aptos_rust_sdk_v2::transaction::{
    PartiallySigned, RawTransaction, SignedTransaction, TransactionPayload,
};
use aptos_rust_sdk_v2::types::{AccountAddress, HashValue, MoveModuleId, MoveStructTag, TypeTag};
use aptos_rust_sdk_v2::ChainId;
use cucumber::World;
use std::collections::HashMap;

/// The test world holds state between Cucumber steps within a scenario.
#[derive(Debug, Default, World)]
pub struct TestWorld {
    // ==========================================================================
    // Address State
    // ==========================================================================
    /// The current hex string input.
    pub hex_string: Option<String>,

    /// The parsed address result.
    pub address_result: Option<Result<AccountAddress, String>>,

    /// The current address.
    pub address: Option<AccountAddress>,

    /// A second address for comparison.
    pub address2: Option<AccountAddress>,

    /// BCS serialized bytes.
    pub bcs_bytes: Option<Vec<u8>>,

    /// Formatted string result.
    pub formatted_string: Option<String>,

    /// Account address.
    pub account_address: Option<AccountAddress>,

    // ==========================================================================
    // Cryptography State
    // ==========================================================================
    /// Ed25519 private key.
    pub ed25519_private_key: Option<Ed25519PrivateKey>,

    /// Ed25519 public key.
    pub ed25519_public_key: Option<Ed25519PublicKey>,

    /// A second Ed25519 key pair for comparison.
    pub ed25519_private_key2: Option<Ed25519PrivateKey>,
    pub ed25519_public_key2: Option<Ed25519PublicKey>,

    /// Current message to sign.
    pub message: Option<Vec<u8>>,

    /// Second message for comparison.
    pub message2: Option<Vec<u8>>,

    /// Ed25519 signature.
    pub ed25519_signature: Option<Ed25519Signature>,

    /// Second signature for comparison.
    pub ed25519_signature2: Option<Ed25519Signature>,

    /// Hash value.
    pub hash_value: Option<HashValue>,

    /// Seed bytes for key derivation.
    pub seed_bytes: Option<Vec<u8>>,

    /// Error from the last operation.
    pub last_error: Option<String>,

    /// Generic error storage.
    pub error: Option<String>,

    // ==========================================================================
    // Account State
    // ==========================================================================
    /// Ed25519 account.
    pub ed25519_account: Option<Ed25519Account>,

    /// Second Ed25519 account.
    pub ed25519_account2: Option<Ed25519Account>,

    /// Authentication key bytes.
    pub auth_key_bytes: Option<Vec<u8>>,

    // ==========================================================================
    // Type Tag State
    // ==========================================================================
    /// Type tag string input.
    pub type_tag_string: Option<String>,

    /// Type string input.
    pub type_string: Option<String>,

    /// Module string input.
    pub module_string: Option<String>,

    /// Parsed type tag result.
    pub type_tag_result: Option<Result<TypeTag, String>>,

    /// Current type tag.
    pub type_tag: Option<TypeTag>,

    /// Deserialized type tag (for roundtrip tests).
    pub type_tag_deserialized: Option<TypeTag>,

    /// Move module ID.
    pub module_id: Option<MoveModuleId>,
    /// Deserialized move module ID.
    pub module_id_deserialized: Option<MoveModuleId>,

    /// Move struct tag.
    pub struct_tag: Option<MoveStructTag>,
    /// Deserialized move struct tag.
    pub struct_tag_deserialized: Option<MoveStructTag>,

    // ==========================================================================
    // Secp256k1 State
    // ==========================================================================
    /// Secp256k1 private key.
    pub secp256k1_private_key: Option<Secp256k1PrivateKey>,
    /// Secp256k1 public key.
    pub secp256k1_public_key: Option<Secp256k1PublicKey>,
    /// Second Secp256k1 private key.
    pub secp256k1_private_key2: Option<Secp256k1PrivateKey>,
    /// Second Secp256k1 public key.
    pub secp256k1_public_key2: Option<Secp256k1PublicKey>,
    /// Secp256k1 signature.
    pub secp256k1_signature: Option<Secp256k1Signature>,
    /// Second Secp256k1 signature.
    pub secp256k1_signature2: Option<Secp256k1Signature>,

    // ==========================================================================
    // Secp256r1 State
    // ==========================================================================
    /// Secp256r1 private key.
    pub secp256r1_private_key: Option<Secp256r1PrivateKey>,
    /// Secp256r1 public key.
    pub secp256r1_public_key: Option<Secp256r1PublicKey>,
    /// Second Secp256r1 private key.
    pub secp256r1_private_key2: Option<Secp256r1PrivateKey>,
    /// Second Secp256r1 public key.
    pub secp256r1_public_key2: Option<Secp256r1PublicKey>,
    /// Secp256r1 signature.
    pub secp256r1_signature: Option<Secp256r1Signature>,
    /// Second Secp256r1 signature.
    pub secp256r1_signature2: Option<Secp256r1Signature>,

    /// Private key bytes (for creating keys from bytes).
    pub private_key_bytes: Option<Vec<u8>>,

    // ==========================================================================
    // Transaction State
    // ==========================================================================
    /// Raw transaction bytes.
    pub raw_transaction_bytes: Option<Vec<u8>>,

    /// Signed transaction bytes.
    pub signed_transaction_bytes: Option<Vec<u8>>,

    /// Transaction hash.
    pub transaction_hash: Option<HashValue>,

    /// Second transaction hash.
    pub transaction_hash2: Option<HashValue>,

    /// Raw transaction.
    pub raw_transaction: Option<RawTransaction>,

    /// Second raw transaction.
    pub raw_transaction2: Option<RawTransaction>,

    /// Signed transaction.
    pub signed_transaction: Option<SignedTransaction>,

    /// Second signed transaction.
    pub signed_transaction2: Option<SignedTransaction>,

    /// Transaction sender.
    pub tx_sender: Option<AccountAddress>,

    /// Transaction sequence number.
    pub tx_sequence_number: Option<u64>,

    /// Transaction payload.
    pub tx_payload: Option<TransactionPayload>,

    /// Transaction max gas.
    pub tx_max_gas: Option<u64>,

    /// Transaction gas price.
    pub tx_gas_price: Option<u64>,

    /// Transaction expiration.
    pub tx_expiration: Option<u64>,

    /// Transaction chain ID.
    pub tx_chain_id: Option<ChainId>,

    /// Signing message bytes.
    pub signing_message: Option<Vec<u8>>,

    /// Second signing message.
    pub signing_message2: Option<Vec<u8>>,

    /// Second serialized bytes.
    pub serialized_bytes2: Option<Vec<u8>>,

    // ==========================================================================
    // Multi-Agent Transaction State
    // ==========================================================================
    /// Multi-agent raw transaction.
    pub multi_agent_txn: Option<MultiAgentRawTransaction>,

    /// Secondary signer addresses.
    pub secondary_signer_addresses: Vec<AccountAddress>,

    /// Secondary signer accounts.
    pub secondary_accounts: Vec<Ed25519Account>,

    // ==========================================================================
    // Fee Payer Transaction State
    // ==========================================================================
    /// Fee payer raw transaction.
    pub fee_payer_txn: Option<FeePayerRawTransaction>,

    /// Fee payer address.
    pub fee_payer_address: Option<AccountAddress>,

    /// Fee payer account.
    pub fee_payer_account: Option<Ed25519Account>,

    /// Partially signed transaction.
    #[world(skip)]
    pub partially_signed: Option<PartiallySigned>,

    // ==========================================================================
    // Multi-Signature State
    // ==========================================================================
    /// Multi-Ed25519 account.
    #[world(skip)]
    pub multi_ed25519_account: Option<MultiEd25519Account>,

    /// Multi-Ed25519 public key.
    pub multi_ed25519_public_key: Option<MultiEd25519PublicKey>,

    /// Multi-Ed25519 signature.
    pub multi_ed25519_signature: Option<MultiEd25519Signature>,

    /// Ed25519 public keys for multi-sig creation.
    pub ed25519_public_keys: Vec<Ed25519PublicKey>,

    /// Ed25519 private keys for multi-sig creation.
    pub ed25519_private_keys: Vec<Ed25519PrivateKey>,

    /// Multi-sig threshold.
    pub multi_sig_threshold: Option<u8>,

    /// Individual signature contributions.
    pub signature_contributions: Vec<(u8, Ed25519Signature)>,

    // ==========================================================================
    // Serialization State
    // ==========================================================================
    /// Boolean value for serialization tests.
    pub bool_value: Option<bool>,

    /// u8 value.
    pub u8_value: Option<u8>,

    /// u16 value.
    pub u16_value: Option<u16>,

    /// u32 value.
    pub u32_value: Option<u32>,

    /// u64 value.
    pub u64_value: Option<u64>,

    /// u128 value.
    pub u128_value: Option<u128>,

    /// u256 value (as 32 bytes).
    pub u256_value: Option<[u8; 32]>,

    /// Bytes value.
    pub bytes_value: Option<Vec<u8>>,

    /// Vector of u8.
    pub vec_u8_value: Option<Vec<u8>>,

    /// Vector of u64.
    pub vec_u64_value: Option<Vec<u64>>,

    /// Vector of vectors of u8.
    pub vec_vec_u8_value: Option<Vec<Vec<u8>>>,

    /// Option<u64> value.
    pub option_u64_value: Option<Option<u64>>,

    /// Serialized bytes result.
    pub serialized_bytes: Option<Vec<u8>>,

    /// ULEB128 value.
    pub uleb_value: Option<usize>,

    /// ULEB128 decoded value.
    pub uleb_decoded: Option<usize>,

    // ==========================================================================
    // Hashing State
    // ==========================================================================
    /// Input bytes for hashing.
    pub hash_input: Option<Vec<u8>>,

    /// Second input for comparison.
    pub hash_input2: Option<Vec<u8>>,

    /// Multiple parts for concatenated hashing.
    pub hash_parts: Option<Vec<Vec<u8>>>,

    /// Hash result.
    pub hash_result: Option<[u8; 32]>,

    /// Second hash result for comparison.
    pub hash_result2: Option<[u8; 32]>,

    /// Domain string for domain-separated hashing.
    pub domain_string: Option<String>,

    /// Second domain string.
    pub domain_string2: Option<String>,

    /// Second hash value for comparison.
    pub hash_value2: Option<HashValue>,

    // ==========================================================================
    // API Client State
    // ==========================================================================
    /// Fullnode REST API client.
    #[world(skip)]
    pub fullnode_client: Option<FullnodeClient>,

    /// Faucet client.
    #[world(skip)]
    pub faucet_client: Option<FaucetClient>,

    // ==========================================================================
    // Generic State
    // ==========================================================================
    /// Generic bytes storage.
    pub bytes: Option<Vec<u8>>,

    /// Generic string storage.
    pub string_value: Option<String>,

    /// Boolean result.
    pub bool_result: Option<bool>,

    /// Named values for complex scenarios.
    pub named_values: HashMap<String, String>,
}

impl TestWorld {
    /// Clear all state for a new scenario.
    pub fn reset(&mut self) {
        *self = Self::default();
    }

    /// Store an error message.
    pub fn set_error(&mut self, err: impl ToString) {
        self.last_error = Some(err.to_string());
    }

    /// Check if there was an error.
    pub fn has_error(&self) -> bool {
        self.last_error.is_some() || self.error.is_some()
    }

    /// Get the last error message.
    pub fn get_error(&self) -> Option<&str> {
        self.last_error.as_deref()
    }

    /// Clear the last error.
    pub fn clear_error(&mut self) {
        self.last_error = None;
    }
}
