/// Cryptography step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/02-cryptography/*.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_generate_ed25519_keypair, "I generate a new Ed25519 key pair")
{
    auto& world = cuke::context<TestWorld>();
    world.ed25519_private_key = Ed25519PrivateKey::generate();
}

GIVEN(given_ed25519_private_key_hex, "an Ed25519 private key from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    
    auto bytes = vectors::hex_to_bytes(hex);
    auto key = Ed25519PrivateKey::from_bytes(bytes);
    if (key) {
        world.ed25519_private_key = *key;
    } else {
        world.set_error("Failed to parse Ed25519 private key");
    }
}

GIVEN(given_message_string, "a message {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string msg = CUKE_ARG(1);
    world.message = std::vector<uint8_t>(msg.begin(), msg.end());
}

GIVEN(given_message_hex, "a message from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.message = vectors::hex_to_bytes(hex);
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_derive_public_key, "I derive the public key")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
}

WHEN(when_sign_message_ed25519, "I sign the message with Ed25519")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
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

THEN(then_signature_verification_succeed, "the signature verification should succeed")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bool_result.has_value());
    cuke::is_true(*world.bool_result);
}
