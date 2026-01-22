//! Step definitions specific to Secp256k1 and Secp256r1 key types
//!
//! Note: Common steps like "I sign the message", "I verify the signature", etc.
//! are defined in cryptography_steps.rs and handle all key types.

use crate::support::world::TestWorld;
use aptos_rust_sdk_v2::crypto::{
    Secp256k1PrivateKey, Secp256r1PrivateKey,
};
use cucumber::{given, when, then};

// =============================================================================
// Secp256k1 Key Generation
// =============================================================================

#[when(expr = "I generate a random Secp256k1 key pair")]
fn when_generate_secp256k1_keypair(world: &mut TestWorld) {
    let private_key = Secp256k1PrivateKey::generate();
    let public_key = private_key.public_key();
    world.secp256k1_private_key = Some(private_key);
    world.secp256k1_public_key = Some(public_key);
}

#[given(expr = "a 32-byte value greater than the secp256k1 curve order")]
fn given_large_secp256k1_private_key(world: &mut TestWorld) {
    // The secp256k1 curve order is n = FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    // Setting all bytes to 0xFF is greater than n
    world.private_key_bytes = Some(vec![0xFF; 32]);
}

#[given(expr = "a 32-byte value greater than the P-256 curve order")]
fn given_large_secp256r1_private_key(world: &mut TestWorld) {
    world.private_key_bytes = Some(vec![0xFF; 32]);
}

#[when(expr = "I create a Secp256k1 key pair from the bytes")]
fn when_create_secp256k1_from_bytes(world: &mut TestWorld) {
    let bytes = world.private_key_bytes.as_ref().expect("No private key bytes");
    match Secp256k1PrivateKey::from_bytes(bytes) {
        Ok(private_key) => {
            let public_key = private_key.public_key();
            world.secp256k1_private_key = Some(private_key);
            world.secp256k1_public_key = Some(public_key);
        }
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[given(expr = "a hex-encoded Secp256k1 private key")]
fn given_hex_secp256k1_private_key(world: &mut TestWorld) {
    // Use a known valid private key
    world.hex_string = Some("0x".to_string() + &"ab".repeat(32));
}

#[when(expr = "I create a Secp256k1 key pair from hex")]
fn when_create_secp256k1_from_hex(world: &mut TestWorld) {
    let hex = world.hex_string.as_ref().expect("No hex string");
    let hex_clean = hex.trim_start_matches("0x");
    match hex::decode(hex_clean) {
        Ok(bytes) => {
            match Secp256k1PrivateKey::from_bytes(&bytes) {
                Ok(private_key) => {
                    let public_key = private_key.public_key();
                    world.secp256k1_private_key = Some(private_key);
                    world.secp256k1_public_key = Some(public_key);
                }
                Err(e) => world.error = Some(e.to_string()),
            }
        }
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[when(expr = "I try to create a Secp256k1 key pair")]
fn when_try_create_secp256k1(world: &mut TestWorld) {
    when_create_secp256k1_from_bytes(world);
}

#[given(expr = "a Secp256k1 key pair")]
fn given_secp256k1_keypair(world: &mut TestWorld) {
    let private_key = Secp256k1PrivateKey::generate();
    let public_key = private_key.public_key();
    world.secp256k1_private_key = Some(private_key);
    world.secp256k1_public_key = Some(public_key);
}

#[given(expr = "two different Secp256k1 key pairs")]
fn given_two_secp256k1_keypairs(world: &mut TestWorld) {
    let private_key1 = Secp256k1PrivateKey::generate();
    let public_key1 = private_key1.public_key();
    let private_key2 = Secp256k1PrivateKey::generate();
    let public_key2 = private_key2.public_key();
    
    world.secp256k1_private_key = Some(private_key1);
    world.secp256k1_public_key = Some(public_key1);
    world.secp256k1_private_key2 = Some(private_key2);
    world.secp256k1_public_key2 = Some(public_key2);
}

// =============================================================================
// Secp256r1 Key Generation
// =============================================================================

#[when(expr = "I generate a random Secp256r1 key pair")]
fn when_generate_secp256r1_keypair(world: &mut TestWorld) {
    let private_key = Secp256r1PrivateKey::generate();
    let public_key = private_key.public_key();
    world.secp256r1_private_key = Some(private_key);
    world.secp256r1_public_key = Some(public_key);
}

#[when(expr = "I create a Secp256r1 key pair from the bytes")]
fn when_create_secp256r1_from_bytes(world: &mut TestWorld) {
    let bytes = world.private_key_bytes.as_ref().expect("No private key bytes");
    match Secp256r1PrivateKey::from_bytes(bytes) {
        Ok(private_key) => {
            let public_key = private_key.public_key();
            world.secp256r1_private_key = Some(private_key);
            world.secp256r1_public_key = Some(public_key);
        }
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[given(expr = "a hex-encoded Secp256r1 private key")]
fn given_hex_secp256r1_private_key(world: &mut TestWorld) {
    world.hex_string = Some("0x".to_string() + &"ab".repeat(32));
}

#[when(expr = "I create a Secp256r1 key pair from hex")]
fn when_create_secp256r1_from_hex(world: &mut TestWorld) {
    let hex = world.hex_string.as_ref().expect("No hex string");
    let hex_clean = hex.trim_start_matches("0x");
    match hex::decode(hex_clean) {
        Ok(bytes) => {
            match Secp256r1PrivateKey::from_bytes(&bytes) {
                Ok(private_key) => {
                    let public_key = private_key.public_key();
                    world.secp256r1_private_key = Some(private_key);
                    world.secp256r1_public_key = Some(public_key);
                }
                Err(e) => world.error = Some(e.to_string()),
            }
        }
        Err(e) => world.error = Some(e.to_string()),
    }
}

#[when(expr = "I try to create a Secp256r1 key pair")]
fn when_try_create_secp256r1(world: &mut TestWorld) {
    when_create_secp256r1_from_bytes(world);
}

#[given(expr = "a Secp256r1 key pair")]
fn given_secp256r1_keypair(world: &mut TestWorld) {
    let private_key = Secp256r1PrivateKey::generate();
    let public_key = private_key.public_key();
    world.secp256r1_private_key = Some(private_key);
    world.secp256r1_public_key = Some(public_key);
}

#[given(expr = "two different Secp256r1 key pairs")]
fn given_two_secp256r1_keypairs(world: &mut TestWorld) {
    let private_key1 = Secp256r1PrivateKey::generate();
    let public_key1 = private_key1.public_key();
    let private_key2 = Secp256r1PrivateKey::generate();
    let public_key2 = private_key2.public_key();
    
    world.secp256r1_private_key = Some(private_key1);
    world.secp256r1_public_key = Some(public_key1);
    world.secp256r1_private_key2 = Some(private_key2);
    world.secp256r1_public_key2 = Some(public_key2);
}

// =============================================================================
// Public Key Operations
// =============================================================================

#[when(expr = "I get the compressed public key")]
fn when_get_compressed_public_key(world: &mut TestWorld) {
    if let Some(ref pk) = world.secp256k1_public_key {
        world.bytes = Some(pk.to_bytes().to_vec());
    } else if let Some(ref pk) = world.secp256r1_public_key {
        world.bytes = Some(pk.to_bytes().to_vec());
    }
}

#[when(expr = "I get the uncompressed public key")]
fn when_get_uncompressed_public_key(world: &mut TestWorld) {
    if let Some(ref pk) = world.secp256k1_public_key {
        world.bytes = Some(pk.to_uncompressed_bytes().to_vec());
    } else if let Some(ref pk) = world.secp256r1_public_key {
        world.bytes = Some(pk.to_uncompressed_bytes().to_vec());
    }
}

// =============================================================================
// Secp-specific Then Steps
// =============================================================================

#[then(expr = "the compressed public key should be {int} bytes")]
fn then_compressed_public_key_bytes(world: &mut TestWorld, n: usize) {
    if let Some(ref pk) = world.secp256k1_public_key {
        assert_eq!(pk.to_bytes().len(), n);
    } else if let Some(ref pk) = world.secp256r1_public_key {
        assert_eq!(pk.to_bytes().len(), n);
    }
}

#[then(expr = "the uncompressed public key should be {int} bytes")]
fn then_uncompressed_public_key_bytes(world: &mut TestWorld, n: usize) {
    if let Some(ref pk) = world.secp256k1_public_key {
        assert_eq!(pk.to_uncompressed_bytes().len(), n);
    } else if let Some(ref pk) = world.secp256r1_public_key {
        assert_eq!(pk.to_uncompressed_bytes().len(), n);
    }
}

// Note: "the first byte should be" steps are handled in serialization_steps.rs

// =============================================================================
// Authentication Key for Secp keys
// =============================================================================

#[given(regex = r"^a Secp256k1 public key \(uncompressed\)$")]
fn given_secp256k1_uncompressed(world: &mut TestWorld) {
    given_secp256k1_keypair(world);
}

#[given(regex = r"^a Secp256r1 public key \(uncompressed\)$")]
fn given_secp256r1_uncompressed(world: &mut TestWorld) {
    given_secp256r1_keypair(world);
}

#[when(expr = "I derive the Secp authentication key")]
fn when_derive_secp_auth_key(world: &mut TestWorld) {
    use aptos_rust_sdk_v2::crypto::derive_authentication_key;
    
    if let Some(ref pk) = world.secp256k1_public_key {
        let auth_key = derive_authentication_key(&pk.to_uncompressed_bytes(), 0x01);
        world.auth_key_bytes = Some(auth_key.to_vec());
    } else if let Some(ref pk) = world.secp256r1_public_key {
        let auth_key = derive_authentication_key(&pk.to_uncompressed_bytes(), 0x02);
        world.auth_key_bytes = Some(auth_key.to_vec());
    }
}

#[then(regex = r"^it should equal SHA3-256\(uncompressed_public_key \|\| (0x[0-9a-fA-F]+)\)$")]
fn then_auth_key_equals(world: &mut TestWorld, scheme: String) {
    use aptos_rust_sdk_v2::crypto::sha3_256;
    
    let scheme_byte = parse_hex_byte(&scheme);
    let auth_key = world.auth_key_bytes.as_ref().expect("No auth key");
    
    let pk_bytes = if let Some(ref pk) = world.secp256k1_public_key {
        pk.to_uncompressed_bytes().to_vec()
    } else if let Some(ref pk) = world.secp256r1_public_key {
        pk.to_uncompressed_bytes().to_vec()
    } else {
        panic!("No public key");
    };
    
    let mut combined = pk_bytes;
    combined.push(scheme_byte);
    let expected = sha3_256(&combined);
    
    assert_eq!(auth_key.as_slice(), expected.as_slice());
}

#[then(regex = r"^the scheme identifier used should be (0x[0-9a-fA-F]+)$")]
fn then_scheme_identifier(_world: &mut TestWorld, _scheme: String) {
    // This is verified by the auth key derivation
}

// =============================================================================
// Helper Functions
// =============================================================================

fn parse_hex_byte(s: &str) -> u8 {
    let s = s.trim_start_matches("0x").trim_start_matches("0X");
    u8::from_str_radix(s, 16).unwrap_or_else(|_| panic!("Invalid hex byte: {}", s))
}
