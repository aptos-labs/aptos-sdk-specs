/// Account step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/03-account-management/*.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_bip39_mnemonic, "a BIP-39 mnemonic {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string value = CUKE_ARG(1);
    world.string_value = value;
}

GIVEN(given_empty_passphrase, "an empty passphrase")
{
    auto& world = cuke::context<TestWorld>();
    world.named_values["passphrase"] = "";
}

GIVEN(given_derivation_path, "a derivation path {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string path = CUKE_ARG(1);
    world.named_values["derivation_path"] = path;
}

GIVEN(given_seed_bytes_hex, "seed bytes from hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.seed_bytes = vectors::hex_to_bytes(hex);
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_validate_mnemonic, "I validate the mnemonic")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
}

WHEN(when_derive_seed_from_mnemonic, "I derive the seed from the mnemonic")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
}

WHEN(when_compute_auth_key, "I compute the authentication key")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
}

// =============================================================================
// Then Steps
// =============================================================================

THEN(then_mnemonic_should_be_valid, "the mnemonic should be valid")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.bool_result.has_value());
    cuke::is_true(*world.bool_result);
}

THEN(then_seed_should_be_64_bytes, "the seed should be 64 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.seed_bytes.has_value());
    cuke::equal(static_cast<int>(world.seed_bytes->size()), 64);
}

THEN(then_auth_key_should_be_32_bytes, "the authentication key should be 32 bytes")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.auth_key_bytes.has_value());
    cuke::equal(static_cast<int>(world.auth_key_bytes->size()), 32);
}
