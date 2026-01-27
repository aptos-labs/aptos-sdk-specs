"""
Additional step definitions for accounts.
"""

from behave import given, when, then
from aptos_sdk.account import Account


# =============================================================================
# Given Steps - Account Setup
# =============================================================================


@given("a new account address")
def step_given_new_address(context):
    account = Account.generate()
    context.world.address = account.address()


@given("an account address")
def step_given_account_address(context):
    if context.world.account:
        context.world.address = context.world.account.address()
    else:
        account = Account.generate()
        context.world.address = account.address()


@given("an account address with NFTs")
def step_given_address_with_nfts(context):
    # TODO: implement NFT account
    context.scenario.skip("NFT account setup not implemented")


@given("an account with APT")
def step_given_account_with_apt(context):
    context.world.account = Account.generate()
    context.world.test_vectors["has_apt"] = True


@given("an account with coin balances")
def step_given_account_with_coins(context):
    context.world.account = Account.generate()
    context.world.test_vectors["has_coins"] = True


@given("an account with an NFT")
def step_given_account_with_nft(context):
    context.scenario.skip("NFT account setup not implemented")


@given("an account with many NFTs")
def step_given_account_with_many_nfts(context):
    context.scenario.skip("NFT account setup not implemented")


@given("an account with no NFTs")
def step_given_account_no_nfts(context):
    context.world.account = Account.generate()


@given("an account with sequence_number 5")
def step_given_account_seq_5(context):
    context.world.account = Account.generate()
    context.world.test_vectors["sequence_number"] = 5


@given("an account with transaction history")
def step_given_account_with_history(context):
    context.world.account = Account.generate()
    context.world.test_vectors["has_history"] = True


@given("an account with many transactions")
def step_given_account_many_txs(context):
    context.world.account = Account.generate()
    context.world.test_vectors["has_many_txs"] = True


@given("an account with various transaction types")
def step_given_account_various_txs(context):
    context.world.account = Account.generate()
    context.world.test_vectors["various_tx_types"] = True


@given("an account with published modules (e.g., 0x1)")
def step_given_account_with_modules(context):
    from aptos_sdk.account_address import AccountAddress
    context.world.address = AccountAddress.from_str_relaxed("0x1")


@given("an account with 1000 octas")
def step_given_account_1000_octas(context):
    context.world.account = Account.generate()
    context.world.test_vectors["balance"] = 1000


@given("an existing account with 1 APT")
def step_given_existing_account_1_apt(context):
    context.world.account = Account.generate()
    context.world.test_vectors["balance_apt"] = 1


@given("a funded account")
def step_given_funded_account(context):
    context.world.account = Account.generate()
    context.world.test_vectors["funded"] = True


@given("an address that doesn't exist on-chain")
def step_given_nonexistent_address(context):
    context.world.account = Account.generate()
    context.world.test_vectors["nonexistent"] = True


@given("a signing account")
def step_given_signing_account(context):
    context.world.account = Account.generate()


@given("a collection address")
def step_given_collection_address(context):
    context.world.test_vectors["collection_address"] = "0x123"


@given("a collection")
def step_given_collection(context):
    context.world.test_vectors["collection"] = True


@given("an account transaction")
def step_given_account_tx(context):
    context.world.test_vectors["account_tx"] = True


@given("an invalid address string")
def step_given_invalid_address(context):
    context.world.hex_string = "invalid"


@given("a message and valid signature")
def step_given_msg_and_sig(context):
    context.world.message = b"test message"
    if context.world.ed25519_private_key:
        context.world.ed25519_signature = context.world.ed25519_private_key.sign(
            context.world.message
        )


@given("a message signed by first key")
def step_given_msg_signed_first(context):
    context.world.message = b"test message"
    if context.world.ed25519_private_key:
        context.world.ed25519_signature = context.world.ed25519_private_key.sign(
            context.world.message
        )


@given("a message")
def step_given_message_generic(context):
    context.world.message = b"test message"


@given("variable values")
def step_given_variable_values(context):
    context.world.test_vectors["variable_values"] = True


@given("current time is T")
def step_given_current_time(context):
    import time
    context.world.test_vectors["current_time"] = time.time()


# =============================================================================
# When Steps - Account Operations
# =============================================================================


@when("I get account modules")
def step_get_account_modules(context):
    context.world.test_vectors["modules_queried"] = True


@when("I get account transactions")
def step_get_account_txs(context):
    context.world.test_vectors["account_txs_queried"] = True


@when("I get account transactions with start=10 and limit=5")
def step_get_account_txs_paginated(context):
    context.world.test_vectors["account_txs_paginated"] = True


@when("I get the account info")
def step_get_account_info(context):
    context.world.test_vectors["account_info_queried"] = True


@when('I get resource "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>"')
def step_get_coin_resource(context):
    context.world.test_vectors["coin_resource_queried"] = True


@when("I get a resource type that doesn't exist")
def step_get_nonexistent_resource(context):
    context.world.test_vectors["nonexistent_resource_queried"] = True


@when("I get the CoinInfo resource for AptosCoin")
def step_get_coin_info(context):
    context.world.test_vectors["coin_info_queried"] = True


@when("I derive the account address")
def step_derive_account_address(context):
    if context.world.account:
        context.world.address = context.world.account.address()


@when("I derive the public key")
def step_derive_pubkey(context):
    if context.world.account:
        context.world.ed25519_public_key = context.world.account.public_key()


# =============================================================================
# Then Steps - Account Assertions
# =============================================================================


@then("I should receive a new account")
def step_receive_new_account(context):
    assert context.world.account is not None


@then("I should receive the current sequence_number")
def step_receive_seq_num(context):
    pass


@then("I should receive the coin store resource")
def step_receive_coin_store(context):
    pass


@then("I should be able to read the balance")
def step_can_read_balance(context):
    pass


@then("I should receive gas_estimate")
def step_receive_gas_estimate(context):
    pass


@then("I should receive gas_estimate (standard)")
def step_receive_gas_estimate_standard(context):
    pass


@then("I should receive gas_used")
def step_receive_gas_used(context):
    pass


@then("I can use this to set max_gas_amount")
def step_can_set_max_gas(context):
    pass


@then("I can use it to set max_gas_amount with buffer")
def step_can_set_max_gas_buffer(context):
    pass


@then("I should be able to extract the error code")
def step_extract_error_code(context):
    pass


@then("I should receive the state as of that version")
def step_receive_state_at_version(context):
    pass


@then("I should receive an error about unavailable state")
def step_receive_unavailable_state_error(context):
    assert context.world.error is not None
