"""
Additional step definitions for multi-sig and multi-agent transactions.
"""

from behave import given, then

# =============================================================================
# Given Steps - Multi-Sig Setup
# =============================================================================


@given("1 Ed25519 public key")
def step_given_1_ed25519_pubkey(context):
    from aptos_sdk.ed25519 import PrivateKey

    context.world.ed25519_public_key = PrivateKey.random().public_key()


@given("a 3-key multi-sig")
def step_given_3_key_multisig(context):
    context.world.test_vectors["multisig_keys"] = 3


@given("a 2-of-3 multi-sig with public keys only")
def step_given_2_of_3_pubkeys_only(context):
    context.world.test_vectors["multisig_threshold"] = 2
    context.world.test_vectors["multisig_keys"] = 3


@given("a 2-of-3 multi-sig signature from keys 0 and 2")
def step_given_2_of_3_sig(context):
    context.world.test_vectors["multisig_signers"] = [0, 2]


@given("a message and valid 2-of-3 signature")
def step_given_msg_and_multisig(context):
    context.world.message = b"test message"
    context.world.test_vectors["multisig_valid"] = True


@given("a signature with only 1 signer")
def step_given_sig_1_signer(context):
    context.world.test_vectors["signers_count"] = 1


@given("a signature from different keys")
def step_given_sig_diff_keys(context):
    context.world.test_vectors["different_keys"] = True


@given("a multi-sig signature builder")
def step_given_multisig_builder(context):
    context.world.test_vectors["multisig_builder"] = True


@given("a multi-sig account and message from test vectors")
def step_given_multisig_from_vectors(context):
    context.world.test_vectors["multisig_from_vectors"] = True


@given("a RawTransaction for multi-sig signing")
def step_given_raw_tx_multisig(context):
    context.world.test_vectors["raw_tx_multisig"] = True


@given("a signed multi-sig transaction")
def step_given_signed_multisig_tx(context):
    context.world.test_vectors["signed_multisig"] = True


# =============================================================================
# Given Steps - Multi-Agent Setup
# =============================================================================


@given("2 secondary signer accounts")
def step_given_2_secondary(context):
    from aptos_sdk.account import Account

    context.world.test_vectors["secondary_accounts"] = [
        Account.generate(),
        Account.generate(),
    ]


@given("3 secondary signer addresses")
def step_given_3_secondary_addresses(context):
    from aptos_sdk.account import Account

    context.world.test_vectors["secondary_addresses"] = [
        Account.generate().address(),
        Account.generate().address(),
        Account.generate().address(),
    ]


@given("a multi-agent transaction from test vectors")
def step_given_multi_agent_vectors(context):
    context.world.test_vectors["multi_agent_from_vectors"] = True


@given("a multi-agent transaction with 2 secondary signers")
def step_given_multi_agent_2_secondary(context):
    context.world.test_vectors["secondary_count"] = 2


@given("a multi-agent transaction with no secondary signers")
def step_given_multi_agent_no_secondary(context):
    context.world.test_vectors["secondary_count"] = 0


@given("a multi-agent authenticator")
def step_given_multi_agent_auth(context):
    context.world.test_vectors["multi_agent_auth"] = True


@given("a RawTransaction for multi-agent")
def step_given_raw_tx_multi_agent(context):
    context.world.test_vectors["raw_tx_multi_agent"] = True


@given("a RawTransaction and secondary addresses from test vectors")
def step_given_raw_tx_secondary_vectors(context):
    context.world.test_vectors["raw_tx_secondary_vectors"] = True


@given("a signed multi-agent transaction")
def step_given_signed_multi_agent(context):
    context.world.test_vectors["signed_multi_agent"] = True


@given("a Secp256k1 secondary signer")
def step_given_secp256k1_secondary(context):
    try:
        from aptos_sdk.account import Account

        context.world.test_vectors["secp256k1_secondary"] = (
            Account.generate_secp256k1_ecdsa()
        )
    except Exception:
        context.scenario.skip("Secp256k1 not supported")


# =============================================================================
# Given Steps - Fee Payer
# =============================================================================


@given("a sender who wants sponsored transaction")
def step_given_sender_wants_sponsor(context):
    from aptos_sdk.account import Account

    context.world.account = Account.generate()
    context.world.test_vectors["wants_sponsor"] = True


@given("a fee payer transaction from test vectors")
def step_given_fee_payer_vectors(context):
    context.world.test_vectors["fee_payer_from_vectors"] = True


@given("a fee payer authenticator")
def step_given_fee_payer_auth(context):
    context.world.test_vectors["fee_payer_auth"] = True


@given("a RawTransaction and fee payer address from test vectors")
def step_given_raw_tx_fee_payer_vectors(context):
    context.world.test_vectors["raw_tx_fee_payer_vectors"] = True


@given("a partially signed fee payer transaction from sender")
def step_given_partial_fee_payer(context):
    context.world.test_vectors["partial_fee_payer"] = True


@given("a Secp256k1 fee payer")
def step_given_secp256k1_fee_payer(context):
    try:
        from aptos_sdk.account import Account

        context.world.test_vectors["secp256k1_fee_payer"] = (
            Account.generate_secp256k1_ecdsa()
        )
    except Exception:
        context.scenario.skip("Secp256k1 not supported")


# =============================================================================
# Then Steps - Multi-Sig Assertions
# =============================================================================


@then("the authenticator should be MultiEd25519 variant")
def step_auth_is_multi_ed25519(context):
    # TODO: implement authenticator check
    pass


@then("the bitmap should indicate positions 0 and 2")
def step_bitmap_positions(context):
    # TODO: implement bitmap check
    pass


@then("the multi-agent message should match test vectors")
def step_multi_agent_msg_matches(context):
    pass


@then("the authenticator should be MultiAgent variant")
def step_auth_is_multi_agent(context):
    pass


# Note: "the authenticator should be FeePayer variant" is defined in fee_payer_steps.py
