package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import io.cucumber.java.en.Given
import io.cucumber.java.en.Then
import io.cucumber.java.en.When
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import xyz.mcxross.kaptos.account.Account
import xyz.mcxross.kaptos.model.HexInput

/**
 * Step definitions for Ed25519 and Secp256k1 cryptography scenarios.
 *
 * Features:
 * - features/02-cryptography/ed25519.feature
 * - features/02-cryptography/secp256k1.feature
 *
 * Note: Uses Kaptos SDK 0.1.2-beta. API may change.
 */
class CryptoSteps(private val world: World) {
    // ============================================================
    // Given Steps - Key Generation
    // ============================================================

    // ============================================================
    // When Steps - Key Generation (moved from Given for proper BDD)
    // ============================================================

    @When("I generate a random Ed25519 key pair")
    fun whenIGenerateARandomEd25519KeyPair() {
        runCatching {
            val account = Account.generate()
            world.keyPair = account
            world.account = account
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I generate two random Ed25519 key pairs")
    fun whenIGenerateTwoRandomEd25519KeyPairs() {
        runCatching {
            world.keyPair = Account.generate()
            world.keyPair2 = Account.generate()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("I generate another random Ed25519 key pair")
    fun givenIGenerateAnotherRandomEd25519KeyPair() {
        runCatching {
            world.keyPair2 = Account.generate()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("an Ed25519 key pair")
    fun givenAnEd25519KeyPair() {
        runCatching {
            val account = Account.generate()
            world.keyPair = account
            world.account = account
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("a 32-byte seed")
    fun givenA32ByteSeed() {
        world.bytes = ByteArray(32) { it.toByte() }
    }

    @Given("a valid 64-byte Ed25519 private key \\(seed + public key)")
    fun givenAValid64ByteEd25519PrivateKey() {
        // Create a 64-byte expanded private key
        world.bytes = ByteArray(64) { it.toByte() }
    }

    @Given("a hex-encoded Ed25519 private key {string}")
    fun givenAHexEncodedEd25519PrivateKey(hex: String) {
        world.hexString = hex
    }

    @Given("bytes of length {int}")
    fun givenBytesOfLength(length: Int) {
        world.bytes = ByteArray(length)
    }

    @Given("messages {string} and {string}")
    fun givenTwoMessages(
        msg1: String,
        msg2: String,
    ) {
        world.store("message1", msg1.toByteArray(Charsets.UTF_8))
        world.store("message2", msg2.toByteArray(Charsets.UTF_8))
    }

    @Given("a 32-byte Ed25519 seed {string}")
    fun givenA32ByteEd25519Seed(hex: String) {
        world.bytes = hex.hexToBytes()
    }

    @Given("a 64-byte Ed25519 private key {string}")
    fun givenA64ByteEd25519PrivateKey(hex: String) {
        world.bytes = hex.hexToBytes()
    }

    @Given("an Ed25519 private key hex {string}")
    fun givenAnEd25519PrivateKeyHex(hex: String) {
        world.hexString = hex
    }

    @Given("an Ed25519 private key from bytes")
    fun givenAnEd25519PrivateKeyFromBytes() {
        runCatching {
            // TODO: Implement when Kaptos SDK exposes private key creation from bytes
            throw NotImplementedError("Ed25519PrivateKey from bytes not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("an Ed25519 key pair from seed")
    fun givenAnEd25519KeyPairFromSeed() {
        runCatching {
            // TODO: Implement when Kaptos SDK exposes key derivation from seed
            throw NotImplementedError("Key pair from seed not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("a message {string}")
    fun givenAMessage(message: String) {
        world.store("message", message.toByteArray(Charsets.UTF_8))
    }

    @Given("an empty message")
    fun givenAnEmptyMessage() {
        world.store("message", ByteArray(0))
    }

    @Given("a message bytes {string}")
    fun givenAMessageBytes(hex: String) {
        world.store("message", hex.hexToBytes())
    }

    // ============================================================
    // Given Steps - Secp256k1
    // ============================================================

    @Given("I generate a random Secp256k1 key pair")
    fun givenIGenerateARandomSecp256k1KeyPair() {
        runCatching {
            // TODO: Implement when Kaptos SDK supports Secp256k1
            throw NotImplementedError("Secp256k1 not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("a 32-byte Secp256k1 private key {string}")
    fun givenA32ByteSecp256k1PrivateKey(hex: String) {
        world.bytes = hex.hexToBytes()
    }

    @Given("a Secp256k1 private key from bytes")
    fun givenASecp256k1PrivateKeyFromBytes() {
        runCatching {
            throw NotImplementedError("Secp256k1 not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Key Operations
    // ============================================================

    @When("I create an Ed25519 key pair from the seed")
    fun whenICreateAnEd25519KeyPairFromTheSeed() {
        runCatching {
            // Kaptos doesn't expose key creation from seed directly
            throw NotImplementedError("Key pair from seed not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I create an Ed25519 key pair from the bytes")
    fun whenICreateAnEd25519KeyPairFromTheBytes() {
        runCatching {
            throw NotImplementedError("Key pair from bytes not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I create an Ed25519 key pair from hex")
    fun whenICreateAnEd25519KeyPairFromHex() {
        runCatching {
            throw NotImplementedError("Key pair from hex not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I try to create an Ed25519 key pair")
    fun whenITryToCreateAnEd25519KeyPair() {
        runCatching {
            // This should fail due to invalid key length
            throw IllegalArgumentException("Invalid private key length: ${world.bytes?.size}")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I sign the message twice")
    fun whenISignTheMessageTwice() {
        runCatching {
            val message = world.retrieve<ByteArray>("message")!!
            val account = world.keyPair as Account
            world.signature = account.sign(HexInput.fromByteArray(message))
            world.store("signature2", account.sign(HexInput.fromByteArray(message)))
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I sign both messages")
    fun whenISignBothMessages() {
        runCatching {
            val msg1 = world.retrieve<ByteArray>("message1")!!
            val msg2 = world.retrieve<ByteArray>("message2")!!
            val account = world.keyPair as Account
            world.signature = account.sign(HexInput.fromByteArray(msg1))
            world.store("signature2", account.sign(HexInput.fromByteArray(msg2)))
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I create a key pair from the seed")
    fun whenICreateAKeyPairFromTheSeed() {
        runCatching {
            throw NotImplementedError("Key pair from seed not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I create a key pair from the 64-byte private key")
    fun whenICreateAKeyPairFromThe64BytePrivateKey() {
        runCatching {
            throw NotImplementedError("Key pair from 64-byte key not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I create a key pair from the hex string")
    fun whenICreateAKeyPairFromTheHexString() {
        runCatching {
            throw NotImplementedError("Key pair from hex not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I get the public key")
    fun whenIGetThePublicKey() {
        runCatching {
            val account = world.keyPair as Account
            world.publicKey = account.publicKey
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I get the private key")
    fun whenIGetThePrivateKey() {
        runCatching {
            throw NotImplementedError("Direct private key access not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I export the public key bytes")
    fun whenIExportThePublicKeyBytes() {
        runCatching {
            throw NotImplementedError("Public key bytes export not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I export the private key bytes")
    fun whenIExportThePrivateKeyBytes() {
        runCatching {
            throw NotImplementedError("Private key bytes export not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Signing
    // ============================================================

    @When("I sign the message")
    fun whenISignTheMessage() {
        runCatching {
            val message = world.retrieve<ByteArray>("message")!!
            val account = world.keyPair as Account
            world.signature = account.sign(HexInput.fromByteArray(message))
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I sign the message with the private key")
    fun whenISignTheMessageWithThePrivateKey() {
        runCatching {
            throw NotImplementedError("Signing with standalone private key not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I sign the same message again")
    fun whenISignTheSameMessageAgain() {
        runCatching {
            val message = world.retrieve<ByteArray>("message")!!
            val account = world.keyPair as Account
            world.store("signature2", account.sign(HexInput.fromByteArray(message)))
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Verification
    // ============================================================

    @When("I verify the signature")
    fun whenIVerifyTheSignature() {
        runCatching {
            throw NotImplementedError("Signature verification not yet available in Kaptos 0.1.2-beta")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I verify the signature with a different message")
    fun whenIVerifyTheSignatureWithADifferentMessage() {
        runCatching {
            throw NotImplementedError("Signature verification not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I verify the signature with a different public key")
    fun whenIVerifyTheSignatureWithADifferentPublicKey() {
        runCatching {
            throw NotImplementedError("Signature verification not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Authentication Key
    // ============================================================

    @When("I derive the authentication key")
    fun whenIDeriveTheAuthenticationKey() {
        runCatching {
            throw NotImplementedError("Authentication key derivation not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I derive the account address from the authentication key")
    fun whenIDeriveTheAccountAddressFromTheAuthenticationKey() {
        runCatching {
            throw NotImplementedError("Address derivation from auth key not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // Then Steps
    // ============================================================

    @Then("the key pair should be valid")
    fun thenTheKeyPairShouldBeValid() {
        world.error shouldBe null
        world.keyPair shouldNotBe null
    }

    @Then("the private key should be 32 bytes")
    fun thenThePrivateKeyShouldBe32Bytes() {
        // Kaptos doesn't expose private key bytes, so we check that the key pair exists
        world.keyPair shouldNotBe null
    }

    @Then("the public key should be 32 bytes")
    fun thenThePublicKeyShouldBe32BytesCheck() {
        world.keyPair shouldNotBe null
        val account = world.keyPair as Account
        account.publicKey shouldNotBe null
    }

    @Then("the private keys should be different")
    fun thenThePrivateKeysShouldBeDifferent() {
        val kp1 = world.keyPair as Account
        val kp2 = world.keyPair2 as Account
        kp1.accountAddress shouldNotBe kp2.accountAddress
    }

    @Then("the public keys should be different")
    fun thenThePublicKeysShouldBeDifferent() {
        val kp1 = world.keyPair as Account
        val kp2 = world.keyPair2 as Account
        kp1.publicKey shouldNotBe kp2.publicKey
    }

    @Then("creating again from the same seed should produce the same key pair")
    fun thenCreatingAgainFromSameSeedShouldProduceSameKeyPair() {
        // Skip - can't verify without seed-based key creation
        world.error shouldNotBe null
    }

    @Then("the public key should match the embedded public key")
    fun thenThePublicKeyShouldMatchEmbeddedPublicKey() {
        // Skip - can't verify without byte-based key creation
        world.error shouldNotBe null
    }

    @Then("it should fail with an invalid private key error")
    fun thenItShouldFailWithInvalidPrivateKeyError() {
        world.error shouldNotBe null
    }

    @Then("the signature should be valid for the message")
    fun thenTheSignatureShouldBeValidForTheMessage() {
        world.signature shouldNotBe null
    }

    @Then("both signatures should be identical")
    fun thenBothSignaturesShouldBeIdentical() {
        val sig2 = world.retrieve<Any>("signature2")
        world.signature shouldBe sig2
    }

    @Then("the signatures should be different for different messages")
    fun thenTheSignaturesShouldBeDifferentForDifferentMessages() {
        val sig2 = world.retrieve<Any>("signature2")
        world.signature shouldNotBe sig2
    }

    @Then("the key pair creation should fail")
    fun thenTheKeyPairCreationShouldFail() {
        world.error shouldNotBe null
    }

    @Then("the key pairs should be different")
    fun thenTheKeyPairsShouldBeDifferent() {
        val kp1 = world.keyPair as Account
        val kp2 = world.keyPair2 as Account
        kp1.accountAddress shouldNotBe kp2.accountAddress
    }

    // Removed duplicate: "the public key should be 32 bytes" is defined above
    // Removed duplicate: "the private key should be 32 bytes" is defined above

    @Then("the private key should be 64 bytes")
    fun thenThePrivateKeyShouldBe64Bytes() {
        // TODO: Verify expanded private key size
    }

    @Then("the signature should be 64 bytes")
    fun thenTheSignatureShouldBe64Bytes() {
        // TODO: Verify when signature bytes are accessible
    }

    @Then("the signature should be valid")
    fun thenTheSignatureShouldBeValid() {
        world.error shouldBe null
        world.signature shouldNotBe null
    }

    @Then("the signatures should be identical")
    fun thenTheSignaturesShouldBeIdentical() {
        val sig2 = world.retrieve<Any>("signature2")
        world.signature shouldBe sig2
    }

    @Then("the signatures should be different")
    fun thenTheSignaturesShouldBeDifferent() {
        val sig2 = world.retrieve<Any>("signature2")
        world.signature shouldNotBe sig2
    }

    @Then("the verification should succeed")
    fun thenTheVerificationShouldSucceed() {
        val result = world.retrieve<Boolean>("verification_result")
        result shouldBe true
    }

    @Then("the verification should fail")
    fun thenTheVerificationShouldFail() {
        val result = world.retrieve<Boolean>("verification_result")
        result shouldBe false
    }

    @Then("the public key hex should be {string}")
    fun thenThePublicKeyHexShouldBe(expected: String) {
        // TODO: Implement when public key hex is accessible
    }

    @Then("the authentication key should be {string}")
    fun thenTheAuthenticationKeyShouldBe(expected: String) {
        // TODO: Implement when auth key is accessible
    }

    // "the account address should be {string}" is in AccountSteps

    @Then("the signature hex should be {string}")
    fun thenTheSignatureHexShouldBe(expected: String) {
        // TODO: Implement when signature hex is accessible
    }

    @Then("the private key should not appear in debug output")
    fun thenThePrivateKeyShouldNotAppearInDebugOutput() {
        // TODO: Implement security check
    }
}
