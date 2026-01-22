/// Transaction step definitions for Aptos C++ SDK behavioral tests.
///
/// Implements steps from features/04-transaction-building/*.feature

#include <cucumber.hpp>

#include "../support/world.hpp"
#include "../support/vectors.hpp"

using namespace aptos::specs;

// =============================================================================
// Given Steps
// =============================================================================

GIVEN(given_sender_address, "a sender address {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string addr = CUKE_ARG(1);
    
#ifdef APTOS_SDK_AVAILABLE
    try {
        world.tx_sender = AccountAddress::FromHex(addr);
    } catch (const std::exception& e) {
        world.set_error(e.what());
    }
#else
    auto result = AccountAddress::from_hex(addr);
    if (result) {
        world.tx_sender = *result;
    } else {
        world.set_error("Invalid sender address");
    }
#endif
}

GIVEN(given_sequence_number, "a sequence number {int}")
{
    auto& world = cuke::context<TestWorld>();
    int val = CUKE_ARG(1);
    world.tx_sequence_number = static_cast<uint64_t>(val);
}

GIVEN(given_max_gas_amount, "a max gas amount {int}")
{
    auto& world = cuke::context<TestWorld>();
    int val = CUKE_ARG(1);
    world.tx_max_gas = static_cast<uint64_t>(val);
}

GIVEN(given_chain_id, "a chain ID {int}")
{
    auto& world = cuke::context<TestWorld>();
    int val = CUKE_ARG(1);
    world.tx_chain_id = static_cast<uint8_t>(val);
}

GIVEN(given_raw_transaction_bcs_hex, "a raw transaction from BCS hex {string}")
{
    auto& world = cuke::context<TestWorld>();
    std::string hex = CUKE_ARG(1);
    world.raw_transaction_bytes = vectors::hex_to_bytes(hex);
}

// =============================================================================
// When Steps
// =============================================================================

WHEN(when_build_raw_transaction, "I build the raw transaction")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK once transaction payload is set up
    world.set_error("Not implemented");
}

WHEN(when_sign_transaction, "I sign the transaction")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
}

WHEN(when_compute_transaction_hash, "I compute the transaction hash")
{
    auto& world = cuke::context<TestWorld>();
    // TODO: Implement with actual SDK
    world.set_error("Not implemented");
}

// =============================================================================
// Then Steps
// =============================================================================

THEN(then_raw_transaction_valid, "the raw transaction should be valid")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.raw_transaction.has_value());
}

THEN(then_signed_transaction_valid, "the signed transaction should be valid")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.signed_transaction.has_value());
}

THEN(then_transaction_hash_should_be, "the transaction hash should be {string}")
{
    auto& world = cuke::context<TestWorld>();
    cuke::is_true(world.transaction_hash.has_value());
    
    std::string expected = CUKE_ARG(1);
    std::string actual = vectors::bytes_to_hex(
        std::vector<uint8_t>(world.transaction_hash->begin(), 
                             world.transaction_hash->end())
    );
    cuke::equal(actual, expected);
}
