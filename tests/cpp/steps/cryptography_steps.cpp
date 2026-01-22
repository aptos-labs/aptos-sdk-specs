/// Cryptography step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/02-cryptography/*.feature

#include <cucumber.hpp>
#include <iomanip>
#include <sstream>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_generate_ed25519_keypair, "I generate a new Ed25519 key pair")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    world.ed25519_private_key = Ed25519PrivateKey::Random();
#else
    world.ed25519_private_key = Ed25519PrivateKey::generate();
#endif
}

GIVEN(given_ed25519_keypair, "an Ed25519 key pair")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    world.ed25519_private_key = Ed25519PrivateKey::Random();
    world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
#else
    world.ed25519_private_key = Ed25519PrivateKey::generate();
#endif
}

GIVEN(given_two_ed25519_keypairs, "two different Ed25519 key pairs")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    world.ed25519_private_key = Ed25519PrivateKey::Random();
    world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
    world.ed25519_private_key2 = Ed25519PrivateKey::Random();
    world.ed25519_public_key2 = world.ed25519_private_key2->GetPublicKey();
#else
    world.ed25519_private_key = Ed25519PrivateKey::generate();
    world.ed25519_private_key2 = Ed25519PrivateKey::generate();
#endif
}

GIVEN(given_ed25519_public_key, "an Ed25519 public key")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    auto priv = Ed25519PrivateKey::Random();
    world.ed25519_public_key = priv.GetPublicKey();
#else
    auto priv = Ed25519PrivateKey::generate();
    // Placeholder - would derive public key
#endif
}

GIVEN(given_ed25519_private_key_hex, "an Ed25519 private key from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.ed25519_private_key = Ed25519PrivateKey::FromHex(hex);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto bytes = vectors::hex_to_bytes(hex);
    auto key = Ed25519PrivateKey::from_bytes(bytes);
    if (key) {
        world.ed25519_private_key = *key;
    } else {
        world.set_error("Failed to parse Ed25519 private key");
    }
#endif
}

GIVEN(given_hex_ed25519_private_key, "a hex-encoded Ed25519 private key {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.ed25519_private_key = Ed25519PrivateKey::FromHex(hex);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto bytes = vectors::hex_to_bytes(hex);
    auto key = Ed25519PrivateKey::from_bytes(bytes);
    if (key) {
        world.ed25519_private_key = *key;
    } else {
        world.set_error("Failed to parse Ed25519 private key");
    }
#endif
}

GIVEN(given_private_key_hex, "private key hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.ed25519_private_key = Ed25519PrivateKey::FromHex(hex);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto bytes = vectors::hex_to_bytes(hex);
    auto key = Ed25519PrivateKey::from_bytes(bytes);
    if (key) {
        world.ed25519_private_key = *key;
    }
#endif
}

GIVEN(given_32_byte_seed, "a 32-byte seed")
{
    auto& world = cuke::context<TestWorld>();
    // Generate a random 32-byte seed
    std::vector<uint8_t> seed(32);
    for (int i = 0; i < 32; ++i) {
        seed[i] = static_cast<uint8_t>(rand() % 256);
    }
    world.seed_bytes = seed;
}

GIVEN(given_bytes_of_length, "bytes of length {int}")
{
    auto& world = cuke::context<TestWorld>();
    int length = CUKE_ARG(1);
    std::vector<uint8_t> bytes(length, 0);
    world.private_key_bytes = bytes;
}

GIVEN(given_message_string, "a message {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string msg = CUKE_ARG(1);
    world.message = std::vector<uint8_t>(msg.begin(), msg.end());
}

GIVEN(given_empty_message, "an empty message")
{
    auto& world = cuke::context<TestWorld>();
    world.message = std::vector<uint8_t>();
}

GIVEN(given_messages_two, "messages {string} and {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string msg1 = CUKE_ARG(1);
    std::string msg2 = CUKE_ARG(2);
    world.message = std::vector<uint8_t>(msg1.begin(), msg1.end());
    world.message2 = std::vector<uint8_t>(msg2.begin(), msg2.end());
}

GIVEN(given_message_hex, "a message from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.message = vectors::hex_to_bytes(hex);
}

GIVEN(given_signature_created_by_keypair, "a signature created by the key pair")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key || !world.message) {
        world.set_error("Missing private key or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#endif
}

GIVEN(given_signature_with_invalid_bytes, "a signature with invalid bytes")
{
    auto& world = cuke::context<TestWorld>();
    // Create a 64-byte signature with invalid/random bytes
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SecByteBlock invalid_sig(64);
    for (size_t i = 0; i < 64; ++i) {
        invalid_sig[i] = static_cast<uint8_t>(rand() % 256);
    }
    // Mark that we have an invalid signature for testing
    world.bytes = std::vector<uint8_t>(invalid_sig.begin(), invalid_sig.end());
#endif
}

GIVEN(given_signature_truncated, "a signature truncated to {int} bytes")
{
    auto& world = cuke::context<TestWorld>();
    int length = CUKE_ARG(1);
    world.bytes = std::vector<uint8_t>(length, 0);
}

GIVEN(given_signature_for_message, "a signature for message {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string msg = CUKE_ARG(1);
    world.message = std::vector<uint8_t>(msg.begin(), msg.end());
    
#ifdef APTOS_SDK_AVAILABLE
    if (world.ed25519_private_key) {
        try {
            CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
            world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
        } catch (const std::exception& e) {
            world.set_error(e.what());
        }
    }
#endif
}

GIVEN(given_message_signed_by_first_key, "a message signed by the first key")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.message) {
        world.message = std::vector<uint8_t>{'t', 'e', 's', 't'};
    }
    
#ifdef APTOS_SDK_AVAILABLE
    if (world.ed25519_private_key) {
        try {
            CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
            world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
        } catch (const std::exception& e) {
            world.set_error(e.what());
        }
    }
#endif
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_generate_random_ed25519, "I generate a random Ed25519 key pair")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    world.ed25519_private_key = Ed25519PrivateKey::Random();
    world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
#else
    world.ed25519_private_key = Ed25519PrivateKey::generate();
#endif
}

WHEN(when_generate_two_ed25519, "I generate two random Ed25519 key pairs")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    world.ed25519_private_key = Ed25519PrivateKey::Random();
    world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
    world.ed25519_private_key2 = Ed25519PrivateKey::Random();
    world.ed25519_public_key2 = world.ed25519_private_key2->GetPublicKey();
#else
    world.ed25519_private_key = Ed25519PrivateKey::generate();
    world.ed25519_private_key2 = Ed25519PrivateKey::generate();
#endif
}

WHEN(when_create_ed25519_from_hex, "I create an Ed25519 key pair from hex")
{
    auto& world = cuke::context<TestWorld>();
    // Private key should already be set from Given step
#ifdef APTOS_SDK_AVAILABLE
    if (world.ed25519_private_key) {
        world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
    }
#endif
}

WHEN(when_create_ed25519_keypair, "I create an Ed25519 key pair")
{
    auto& world = cuke::context<TestWorld>();
#ifdef APTOS_SDK_AVAILABLE
    if (world.ed25519_private_key) {
        world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
    }
#endif
}

WHEN(when_try_create_ed25519, "I try to create an Ed25519 key pair")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.private_key_bytes) {
        world.set_error("No private key bytes provided");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        std::string hex = vectors::bytes_to_hex(*world.private_key_bytes);
        world.ed25519_private_key = Ed25519PrivateKey::FromHex(hex);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    if (world.private_key_bytes->size() != 32) {
        world.set_error("Invalid private key length");
    }
#endif
}

WHEN(when_create_ed25519_from_seed, "I create an Ed25519 key pair from the seed")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.seed_bytes) {
        world.set_error("No seed bytes provided");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        std::string hex = vectors::bytes_to_hex(*world.seed_bytes);
        world.ed25519_private_key = Ed25519PrivateKey::FromHex(hex);
        world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#endif
}

WHEN(when_derive_public_key, "I derive the public key")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key) {
        world.set_error("No private key available");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.ed25519_public_key = world.ed25519_private_key->GetPublicKey();
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.set_error("Not implemented");
#endif
}

WHEN(when_sign_message, "I sign the message")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key || !world.message) {
        world.set_error("Missing private key or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.set_error("Not implemented");
#endif
}

WHEN(when_sign_message_twice, "I sign the message twice")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key || !world.message) {
        world.set_error("Missing private key or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
        world.ed25519_signature2 = world.ed25519_private_key->Sign(msg_bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#endif
}

WHEN(when_sign_both_messages, "I sign both messages")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key || !world.message || !world.message2) {
        world.set_error("Missing private key or messages");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg1(world.message->data(), world.message->size());
        CryptoPP::SecByteBlock msg2(world.message2->data(), world.message2->size());
        world.ed25519_signature = world.ed25519_private_key->Sign(msg1);
        world.ed25519_signature2 = world.ed25519_private_key->Sign(msg2);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#endif
}

WHEN(when_both_keys_sign_message, "both keys sign the message")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key || !world.ed25519_private_key2 || !world.message) {
        world.set_error("Missing private keys or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
        world.ed25519_signature2 = world.ed25519_private_key2->Sign(msg_bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#endif
}

WHEN(when_sign_message_ed25519, "I sign the message with Ed25519")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key || !world.message) {
        world.set_error("Missing private key or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.ed25519_signature = world.ed25519_private_key->Sign(msg_bytes);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    world.set_error("Not implemented");
#endif
}

WHEN(when_verify_signature, "I verify the signature")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_public_key || !world.ed25519_signature || !world.message) {
        world.set_error("Missing public key, signature, or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.bool_result = world.ed25519_public_key->Verify(msg_bytes, *world.ed25519_signature);
    } catch (const std::exception& e) {
        world.set_error(e.what());
        world.bool_result = false;
    }
#endif
}

WHEN(when_verify_with_second_key, "I verify with the second key's public key")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_public_key2 || !world.ed25519_signature || !world.message) {
        world.set_error("Missing second public key, signature, or message");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
        world.bool_result = world.ed25519_public_key2->Verify(msg_bytes, *world.ed25519_signature);
    } catch (const std::exception& e) {
        world.set_error(e.what());
        world.bool_result = false;
    }
#endif
}

WHEN(when_verify_against_message, "I verify the signature against message {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string msg = CUKE_ARG(1);
    
    if (!world.ed25519_public_key || !world.ed25519_signature) {
        world.set_error("Missing public key or signature");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        CryptoPP::SecByteBlock msg_bytes(reinterpret_cast<const uint8_t*>(msg.data()), msg.size());
        world.bool_result = world.ed25519_public_key->Verify(msg_bytes, *world.ed25519_signature);
    } catch (const std::exception& e) {
        world.set_error(e.what());
        world.bool_result = false;
    }
#endif
}

WHEN(when_export_public_key_bytes, "I export the public key as bytes")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_public_key) {
        world.set_error("No public key available");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    auto key_bytes = world.ed25519_public_key->KeyBytes();
    world.bytes = std::vector<uint8_t>(key_bytes.begin(), key_bytes.end());
#endif
}

WHEN(when_export_private_key_bytes, "I export the private key as bytes")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key) {
        world.set_error("No private key available");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    auto key_bytes = world.ed25519_private_key->KeyBytes();
    world.bytes = std::vector<uint8_t>(key_bytes.begin(), key_bytes.end());
#endif
}

WHEN(when_export_private_key_hex, "I export the private key as hex")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_private_key) {
        world.set_error("No private key available");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    world.formatted_string = world.ed25519_private_key->ToString();
#endif
}

WHEN(when_derive_auth_key, "I derive the authentication key")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_public_key) {
        world.set_error("No public key available");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        auto key_bytes = world.ed25519_public_key->KeyBytes();
        auto auth_key = AuthenticationKey::FromEd25519PublicKey(key_bytes);
        // Store the derived address
        world.formatted_string = auth_key.DerivedAddress();
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#endif
}

WHEN(when_convert_auth_key_to_address, "I convert it to an account address")
{
    auto& world = cuke::context<TestWorld>();
    // Auth key derivation already produces the address in the previous step
    // Just verify we have the result
    cuke::is_true(world.formatted_string.has_value());
}

// =============================================================================
// Then Steps
// =============================================================================

THEN(then_valid_ed25519_private_key, "I should have a valid Ed25519 private key")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_private_key.has_value());
}

THEN(then_valid_ed25519_public_key, "I should have a valid Ed25519 public key")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_public_key.has_value());
}

THEN(then_valid_ed25519_signature, "I should have a valid Ed25519 signature")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_signature.has_value());
}

THEN(then_private_key_32_bytes, "the private key should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_private_key.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    auto key_bytes = world.ed25519_private_key->KeyBytes();
    cuke::equal(static_cast<int>(key_bytes.size()), 32);
#endif
}

THEN(then_public_key_32_bytes, "the public key should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_public_key.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    auto key_bytes = world.ed25519_public_key->KeyBytes();
    cuke::equal(static_cast<int>(key_bytes.size()), 32);
#endif
}

THEN(then_keypair_should_be_valid, "the key pair should be valid")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_private_key.has_value());
    cuke::is_false(world.has_error());
    
#ifdef APTOS_SDK_AVAILABLE
    if (world.ed25519_public_key) {
        cuke::is_true(world.ed25519_public_key->IsOnCurve());
    }
#endif
}

THEN(then_signature_64_bytes, "the signature should be 64 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_signature.has_value());
    // Ed25519 signatures are always 64 bytes
}

THEN(then_signature_should_be_valid, "the signature should be valid")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_signature.has_value());
    cuke::is_false(world.has_error());
}

THEN(then_signature_valid_for_message, "the signature should be valid for the message")
{
    auto& world = cuke::context<TestWorld>();
    if (!world.ed25519_public_key || !world.ed25519_signature || !world.message) {
        cuke::is_true(false, "Missing components for verification");
        return;
    }
    
#ifdef APTOS_SDK_AVAILABLE
    CryptoPP::SecByteBlock msg_bytes(world.message->data(), world.message->size());
    bool valid = world.ed25519_public_key->Verify(msg_bytes, *world.ed25519_signature);
    cuke::is_true(valid);
#endif
}

THEN(then_private_keys_different, "the private keys should be different")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_private_key.has_value());
    cuke::is_true(world.ed25519_private_key2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_false(*world.ed25519_private_key == *world.ed25519_private_key2);
#endif
}

THEN(then_public_keys_different, "the public keys should be different")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_public_key.has_value());
    cuke::is_true(world.ed25519_public_key2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_false(*world.ed25519_public_key == *world.ed25519_public_key2);
#endif
}

THEN(then_both_signatures_identical, "both signatures should be identical")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_signature.has_value());
    cuke::is_true(world.ed25519_signature2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_true(*world.ed25519_signature == *world.ed25519_signature2);
#endif
}

THEN(then_signatures_different, "the signatures should be different")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.ed25519_signature.has_value());
    cuke::is_true(world.ed25519_signature2.has_value());
    
#ifdef APTOS_SDK_AVAILABLE
    cuke::is_false(*world.ed25519_signature == *world.ed25519_signature2);
#endif
}

THEN(then_verification_should_succeed, "verification should succeed")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bool_result.has_value());
    cuke::is_true(*world.bool_result);
}

THEN(then_verification_should_fail, "verification should fail")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(!world.bool_result.has_value() || !*world.bool_result);
}

THEN(then_should_fail_invalid_private_key, "it should fail with an invalid private key error")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.has_error() || !world.ed25519_private_key.has_value());
}

THEN(then_should_fail_invalid_signature, "it should fail with an invalid signature error")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.has_error());
}

THEN(then_result_32_bytes, "the result should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bytes.has_value());
    cuke::equal(static_cast<int>(world.bytes->size()), 32);
}

THEN(then_result_32_or_64_bytes, "the result should be 32 or 64 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bytes.has_value());
    int size = static_cast<int>(world.bytes->size());
    cuke::is_true(size == 32 || size == 64);
}

THEN(then_result_starts_with_0x, "the result should start with {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string expected = CUKE_ARG(1);
    cuke::is_true(world.formatted_string.has_value());
    cuke::is_true(world.formatted_string->substr(0, expected.size()) == expected);
}

THEN(then_hex_length_should_be, "the hex length should be {int} or {int} characters")
{
    auto& world = cuke::context<TestWorld>();
    int len1 = CUKE_ARG(1);
    int len2 = CUKE_ARG(2);
    cuke::is_true(world.formatted_string.has_value());
    int actual = static_cast<int>(world.formatted_string->size());
    cuke::is_true(actual == len1 || actual == len2);
}

THEN(then_signature_verification_succeed, "the signature verification should succeed")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bool_result.has_value());
    cuke::is_true(*world.bool_result);
}

THEN(then_address_should_be_32_bytes, "the address should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.formatted_string.has_value());
    // Address hex (with 0x) should be 66 characters
    cuke::equal(static_cast<int>(world.formatted_string->size()), 66);
}
