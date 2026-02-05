"""
Test vector loading utilities.
Loads JSON test vectors from the test-vectors directory.
"""

import json
import os
from typing import Dict, List, Optional

# Path to test vectors directory
VECTORS_DIR = os.path.join(os.path.dirname(__file__), "../../../test-vectors")

# Cached vectors
_address_vectors: Optional[Dict] = None
_mnemonic_vectors: Optional[Dict] = None
_signature_vectors: Optional[Dict] = None
_transaction_vectors: Optional[Dict] = None
_bcs_vectors: Optional[Dict] = None
_type_tag_vectors: Optional[Dict] = None
_multi_sig_vectors: Optional[Dict] = None


def load_vector_file(filename: str) -> Dict:
    """Load a test vector file."""
    filepath = os.path.join(VECTORS_DIR, filename)
    with open(filepath, "r") as f:
        return json.load(f)


# =============================================================================
# Address Vectors
# =============================================================================


def get_address_vectors() -> Dict:
    """Get address test vectors."""
    global _address_vectors
    if _address_vectors is None:
        _address_vectors = load_vector_file("addresses.json")
    return _address_vectors


def get_address_parsing_vectors() -> List[Dict]:
    """Get address parsing vectors."""
    return get_address_vectors().get("parsing_vectors", [])


def get_address_constants() -> List[Dict]:
    """Get address constants (ZERO, ONE, etc.)."""
    return get_address_vectors().get("constants", [])


def get_invalid_address_inputs() -> List[Dict]:
    """Get invalid address inputs."""
    return get_address_vectors().get("invalid_inputs", [])


# =============================================================================
# Mnemonic Vectors
# =============================================================================


def get_mnemonic_vectors() -> Dict:
    """Get mnemonic test vectors."""
    global _mnemonic_vectors
    if _mnemonic_vectors is None:
        _mnemonic_vectors = load_vector_file("mnemonics.json")
    return _mnemonic_vectors


def get_ed25519_derivation_vectors() -> List[Dict]:
    """Get Ed25519 derivation vectors."""
    return get_mnemonic_vectors().get("ed25519_derivation_vectors", [])


def get_secp256k1_derivation_vectors() -> List[Dict]:
    """Get Secp256k1 derivation vectors."""
    return get_mnemonic_vectors().get("secp256k1_derivation_vectors", [])


# =============================================================================
# Signature Vectors
# =============================================================================


def get_signature_vectors() -> Dict:
    """Get signature test vectors."""
    global _signature_vectors
    if _signature_vectors is None:
        _signature_vectors = load_vector_file("signatures.json")
    return _signature_vectors


def get_ed25519_signing_vectors() -> List[Dict]:
    """Get Ed25519 signing vectors."""
    return get_signature_vectors().get("ed25519", {}).get("signing", [])


def get_sha3_256_vectors() -> List[Dict]:
    """Get SHA3-256 hash vectors."""
    return get_signature_vectors().get("hashing", {}).get("sha3_256", [])


def get_sha2_256_vectors() -> List[Dict]:
    """Get SHA2-256 hash vectors."""
    return get_signature_vectors().get("hashing", {}).get("sha2_256", [])


# =============================================================================
# Transaction Vectors
# =============================================================================


def get_transaction_vectors() -> Dict:
    """Get transaction test vectors."""
    global _transaction_vectors
    if _transaction_vectors is None:
        _transaction_vectors = load_vector_file("transactions.json")
    return _transaction_vectors


def get_raw_transaction_vectors() -> List[Dict]:
    """Get raw transaction vectors."""
    return get_transaction_vectors().get("raw_transactions", [])


def get_signed_transaction_vectors() -> List[Dict]:
    """Get signed transaction vectors."""
    return get_transaction_vectors().get("signed_transactions", [])


# =============================================================================
# BCS Vectors
# =============================================================================


def get_bcs_vectors() -> Dict:
    """Get BCS encoding vectors."""
    global _bcs_vectors
    if _bcs_vectors is None:
        _bcs_vectors = load_vector_file("bcs.json")
    return _bcs_vectors


def get_bcs_primitive_vectors(type_name: str) -> List[Dict]:
    """Get BCS primitive vectors for a specific type."""
    bcs = get_bcs_vectors()
    return bcs.get("primitives", {}).get(type_name, [])


# =============================================================================
# Type Tag Vectors
# =============================================================================


def get_type_tag_vectors() -> Dict:
    """Get type tag test vectors."""
    global _type_tag_vectors
    if _type_tag_vectors is None:
        _type_tag_vectors = load_vector_file("type-tags.json")
    return _type_tag_vectors


def get_type_tag_parsing_vectors() -> List[Dict]:
    """Get type tag parsing vectors."""
    return get_type_tag_vectors().get("parsing_vectors", [])


# =============================================================================
# Multi-Sig Vectors
# =============================================================================


def get_multi_sig_vectors() -> Dict:
    """Get multi-signature test vectors."""
    global _multi_sig_vectors
    if _multi_sig_vectors is None:
        _multi_sig_vectors = load_vector_file("multi-sig.json")
    return _multi_sig_vectors


def get_multi_sig_test_vectors() -> List[Dict]:
    """Get multi-sig test vectors."""
    return get_multi_sig_vectors().get("test_vectors", [])


# =============================================================================
# Secp256k1 Vectors
# =============================================================================


def get_secp256k1_test_vectors() -> List[Dict]:
    """Get Secp256k1 test vectors from signatures.json."""
    return get_signature_vectors().get("secp256k1", {}).get("test_vectors", [])


# =============================================================================
# Utility Functions
# =============================================================================


def hex_to_bytes(hex_string: str) -> bytes:
    """Convert hex string to bytes."""
    clean_hex = hex_string[2:] if hex_string.startswith("0x") else hex_string
    return bytes.fromhex(clean_hex)


def bytes_to_hex(data: bytes, prefix: bool = True) -> str:
    """Convert bytes to hex string."""
    hex_str = data.hex()
    return f"0x{hex_str}" if prefix else hex_str


def normalize_hex(hex_string: str) -> str:
    """Normalize hex string to lowercase with 0x prefix."""
    clean = hex_string.lower()
    if not clean.startswith("0x"):
        clean = "0x" + clean
    return clean
