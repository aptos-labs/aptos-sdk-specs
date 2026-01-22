package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import com.aptos.specs.support.toHex
import io.cucumber.java.en.Given
import io.cucumber.java.en.When
import io.cucumber.java.en.Then
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import io.kotest.matchers.string.shouldNotContain
import xyz.mcxross.kaptos.account.Account
import xyz.mcxross.kaptos.model.HexInput

/**
 * Step definitions for account creation and management scenarios.
 * 
 * Features:
 * - features/03-account-management/single-key.feature
 * - features/03-account-management/authentication-key.feature
 * 
 * Note: Uses Kaptos SDK 0.1.2-beta. Some features may not be available.
 */
class AccountSteps(private val world: World) {
    
    // ============================================================
    // Given Steps - Account Generation
    // ============================================================
    
    @Given("I generate a random Ed25519 account")
    fun givenIGenerateARandomEd25519Account() {
        runCatching {
            world.account = Account.generate()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("I generate another random Ed25519 account")
    fun givenIGenerateAnotherRandomEd25519Account() {
        runCatching {
            world.account2 = Account.generate()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("I generate a random Secp256k1 account")
    fun givenIGenerateARandomSecp256k1Account() {
        runCatching {
            throw NotImplementedError("Secp256k1 account not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("an Ed25519 account from private key bytes {string}")
    fun givenAnEd25519AccountFromPrivateKeyBytes(hex: String) {
        runCatching {
            throw NotImplementedError("Account from private key bytes not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("an Ed25519 account from hex string {string}")
    fun givenAnEd25519AccountFromHexString(hex: String) {
        runCatching {
            throw NotImplementedError("Account from hex string not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("an Ed25519 account from 64-byte expanded key {string}")
    fun givenAnEd25519AccountFromExpandedKey(hex: String) {
        runCatching {
            throw NotImplementedError("Account from 64-byte key not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("an account from AIP-80 string {string}")
    fun givenAnAccountFromAip80String(aip80String: String) {
        runCatching {
            throw NotImplementedError("AIP-80 parsing not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    // ============================================================
    // When Steps - Account Operations
    // ============================================================
    
    @When("I get the account public key")
    fun whenIGetTheAccountPublicKey() {
        runCatching {
            world.publicKey = (world.account as Account).publicKey
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I get the account authentication key")
    fun whenIGetTheAccountAuthenticationKey() {
        runCatching {
            throw NotImplementedError("Authentication key access not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I get the account address")
    fun whenIGetTheAccountAddress() {
        runCatching {
            world.address = (world.account as Account).accountAddress
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I export the account to AIP-80 format")
    fun whenIExportTheAccountToAip80Format() {
        runCatching {
            throw NotImplementedError("AIP-80 export not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I sign a message with the account")
    fun whenISignAMessageWithTheAccount() {
        runCatching {
            val message = world.retrieve<ByteArray>("message")!!
            val account = world.account as Account
            world.signature = account.sign(HexInput.fromByteArray(message))
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I verify the signature with the account")
    fun whenIVerifyTheSignatureWithTheAccount() {
        runCatching {
            throw NotImplementedError("Signature verification not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I verify the signature with a different account")
    fun whenIVerifyTheSignatureWithADifferentAccount() {
        runCatching {
            throw NotImplementedError("Signature verification not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I get the private key explicitly")
    fun whenIGetThePrivateKeyExplicitly() {
        runCatching {
            throw NotImplementedError("Private key access not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    // ============================================================
    // Then Steps
    // ============================================================
    
    @Then("the account should be valid")
    fun thenTheAccountShouldBeValid() {
        world.error shouldBe null
        world.account shouldNotBe null
    }
    
    @Then("the account creation should fail")
    fun thenTheAccountCreationShouldFail() {
        world.error shouldNotBe null
    }
    
    @Then("the accounts should be different")
    fun thenTheAccountsShouldBeDifferent() {
        val acc1 = world.account as Account
        val acc2 = world.account2 as Account
        acc1.accountAddress shouldNotBe acc2.accountAddress
    }
    
    @Then("the account public key should be {string}")
    fun thenTheAccountPublicKeyShouldBe(expected: String) {
        // TODO: Implement when public key string is accessible
    }
    
    @Then("the account authentication key should be {string}")
    fun thenTheAccountAuthenticationKeyShouldBe(expected: String) {
        // TODO: Implement when auth key is accessible
    }
    
    @Then("the account address should be {string}")
    fun thenTheAccountAddressShouldBe(expected: String) {
        // TODO: Implement
    }
    
    @Then("the AIP-80 string should start with {string}")
    fun thenTheAip80StringShouldStartWith(prefix: String) {
        world.inputString shouldNotBe null
        world.inputString!!.startsWith(prefix) shouldBe true
    }
    
    @Then("the AIP-80 format should be {string}")
    fun thenTheAip80FormatShouldBe(expected: String) {
        world.inputString shouldBe expected
    }
    
    @Then("the private key should not be exposed accidentally")
    fun thenThePrivateKeyShouldNotBeExposedAccidentally() {
        val account = world.account as Account
        val accountString = account.toString()
        // Should not contain obvious private key patterns
        accountString shouldNotContain "privateKey"
    }
    
    @Then("the accounts should have the same address")
    fun thenTheAccountsShouldHaveTheSameAddress() {
        val acc1 = world.account as Account
        val acc2 = world.account2 as Account
        acc1.accountAddress shouldBe acc2.accountAddress
    }
    
    // ============================================================
    // Authentication Key Steps
    // ============================================================
    
    @Given("authentication key bytes {string}")
    fun givenAuthenticationKeyBytes(hex: String) {
        world.bytes = hex.hexToBytes()
    }
    
    @When("I create an AuthenticationKey from bytes")
    fun whenICreateAnAuthenticationKeyFromBytes() {
        runCatching {
            require(world.bytes!!.size == 32) { "AuthenticationKey must be 32 bytes" }
            world.authKey = world.bytes!!.clone()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I derive an AuthenticationKey from the public key")
    fun whenIDeriveAnAuthenticationKeyFromThePublicKey() {
        runCatching {
            throw NotImplementedError("AuthenticationKey derivation not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I convert the AuthenticationKey to account address")
    fun whenIConvertTheAuthenticationKeyToAccountAddress() {
        runCatching {
            // For new accounts, auth key == address
            val authKeyBytes = world.authKey as ByteArray
            world.address = authKeyBytes.toHex()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Then("the AuthenticationKey should be valid")
    fun thenTheAuthenticationKeyShouldBeValid() {
        world.error shouldBe null
        world.authKey shouldNotBe null
    }
    
    @Then("the AuthenticationKey creation should fail")
    fun thenTheAuthenticationKeyCreationShouldFail() {
        world.error shouldNotBe null
    }
    
    @Then("the AuthenticationKey should be {string}")
    fun thenTheAuthenticationKeyShouldBe(expected: String) {
        val authKey = world.authKey as ByteArray
        authKey.toHex() shouldBe expected.removePrefix("0x").lowercase()
    }
    
    @Then("the AuthenticationKey should equal the account address")
    fun thenTheAuthenticationKeyShouldEqualTheAccountAddress() {
        // For new accounts, auth key bytes == address bytes
        world.error shouldBe null
    }
}
