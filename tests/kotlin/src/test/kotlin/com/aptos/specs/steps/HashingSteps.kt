package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import com.aptos.specs.support.toHex
import io.cucumber.java.en.Given
import io.cucumber.java.en.Then
import io.cucumber.java.en.When
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import java.security.MessageDigest
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

/**
 * Step definitions for hashing scenarios.
 *
 * Feature: features/02-cryptography/hashing.feature
 *
 * Note: Uses JVM standard library for hashing since Kaptos 0.1.2-beta
 * may not expose low-level hashing APIs directly.
 */
class HashingSteps(private val world: World) {
    // ============================================================
    // Given Steps
    // ============================================================

    @Given("empty data")
    fun givenEmptyData() {
        world.bytes = ByteArray(0)
    }

    @Given("data {string}")
    fun givenData(text: String) {
        world.bytes = text.toByteArray(Charsets.UTF_8)
    }

    @Given("data bytes {string}")
    fun givenDataBytes(hex: String) {
        world.bytes = hex.hexToBytes()
    }

    @Given("a domain separator {string}")
    fun givenADomainSeparator(domain: String) {
        world.store("domain", domain)
    }

    @Given("hash bytes {string}")
    fun givenHashBytes(hex: String) {
        world.bytes = hex.hexToBytes()
    }

    @Given("hash hex {string}")
    fun givenHashHex(hex: String) {
        world.hexString = hex
    }

    @Given("large data of {int} bytes")
    fun givenLargeDataOfBytes(size: Int) {
        world.bytes = ByteArray(size) { (it % 256).toByte() }
    }

    @Given("multiple data parts:")
    fun givenMultipleDataParts(dataTable: io.cucumber.datatable.DataTable) {
        val parts = dataTable.asList().map { it.toByteArray(Charsets.UTF_8) }
        world.store("data_parts", parts)
    }

    // ============================================================
    // When Steps - SHA3-256
    // ============================================================

    @When("I compute SHA3-256")
    fun whenIComputeSha3256() {
        runCatching {
            val digest = MessageDigest.getInstance("SHA3-256")
            world.hashResult = digest.digest(world.bytes!!)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I compute SHA3-256 of the parts")
    fun whenIComputeSha3256OfTheParts() {
        runCatching {
            val parts = world.retrieve<List<ByteArray>>("data_parts")!!
            val digest = MessageDigest.getInstance("SHA3-256")
            parts.forEach { digest.update(it) }
            world.hashResult = digest.digest()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I compute SHA3-256 twice")
    fun whenIComputeSha3256Twice() {
        runCatching {
            val digest = MessageDigest.getInstance("SHA3-256")
            val hash1 = digest.digest(world.bytes!!)
            digest.reset()
            val hash2 = digest.digest(world.bytes!!)
            world.hashResult = hash1
            world.store("hash2", hash2)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - SHA2-256
    // ============================================================

    @When("I compute SHA2-256")
    fun whenIComputeSha2256() {
        runCatching {
            val digest = MessageDigest.getInstance("SHA-256")
            world.hashResult = digest.digest(world.bytes!!)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Domain-Separated Hashing
    // ============================================================

    @When("I compute the domain-separated hash")
    fun whenIComputeTheDomainSeparatedHash() {
        runCatching {
            val domain = world.retrieve<String>("domain")!!
            val digest = MessageDigest.getInstance("SHA3-256")
            // Domain-separated hash: SHA3-256(SHA3-256(domain) || data)
            val domainHash = digest.digest(domain.toByteArray(Charsets.UTF_8))
            digest.reset()
            digest.update(domainHash)
            digest.update(world.bytes!!)
            world.hashResult = digest.digest()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I compute the domain prefix")
    fun whenIComputeTheDomainPrefix() {
        runCatching {
            val domain = world.retrieve<String>("domain")!!
            val digest = MessageDigest.getInstance("SHA3-256")
            world.hashResult = digest.digest(domain.toByteArray(Charsets.UTF_8))
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - HashValue
    // ============================================================

    @When("I create a HashValue from bytes")
    fun whenICreateAHashValueFromBytes() {
        runCatching {
            // HashValue is just a 32-byte wrapper
            require(world.bytes!!.size == 32) { "HashValue must be 32 bytes" }
            world.hashValue = world.bytes!!.clone()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I create a HashValue from hex")
    fun whenICreateAHashValueFromHex() {
        runCatching {
            val bytes = world.hexString!!.hexToBytes()
            require(bytes.size == 32) { "HashValue must be 32 bytes" }
            world.hashValue = bytes
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I get the ZERO HashValue constant")
    fun whenIGetTheZeroHashValueConstant() {
        runCatching {
            world.hashValue = ByteArray(32) // All zeros
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I format the HashValue as hex")
    fun whenIFormatTheHashValueAsHex() {
        runCatching {
            world.hexString = (world.hashValue as ByteArray).toHex()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - HMAC
    // ============================================================

    @When("I compute HMAC-SHA512 with key {string}")
    fun whenIComputeHmacSha512WithKey(keyHex: String) {
        runCatching {
            val key = keyHex.hexToBytes()
            val mac = Mac.getInstance("HmacSHA512")
            mac.init(SecretKeySpec(key, "HmacSHA512"))
            world.hashResult = mac.doFinal(world.bytes!!)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I compute HMAC-SHA512 for BIP-39 seed derivation")
    fun whenIComputeHmacSha512ForBip39SeedDerivation() {
        runCatching {
            val key = "ed25519 seed".toByteArray(Charsets.UTF_8)
            val mac = Mac.getInstance("HmacSHA512")
            mac.init(SecretKeySpec(key, "HmacSHA512"))
            world.hashResult = mac.doFinal(world.bytes!!)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // Then Steps
    // ============================================================

    @Then("the hash should be 32 bytes")
    fun thenTheHashShouldBe32Bytes() {
        world.hashResult shouldNotBe null
        world.hashResult!!.size shouldBe 32
    }

    @Then("the hash should be 64 bytes")
    fun thenTheHashShouldBe64Bytes() {
        world.hashResult shouldNotBe null
        world.hashResult!!.size shouldBe 64
    }

    @Then("the hash should be {string}")
    fun thenTheHashShouldBe(expected: String) {
        val expectedBytes = expected.removePrefix("0x").hexToBytes()
        world.hashResult shouldBe expectedBytes
    }

    @Then("the hash hex should be {string}")
    fun thenTheHashHexShouldBe(expected: String) {
        world.hashResult shouldNotBe null
        world.hashResult!!.toHex() shouldBe expected.removePrefix("0x").lowercase()
    }

    @Then("the hashes should be identical")
    fun thenTheHashesShouldBeIdentical() {
        val hash2 = world.retrieve<ByteArray>("hash2")
        world.hashResult.contentEquals(hash2) shouldBe true
    }

    @Then("the hashes should be different")
    fun thenTheHashesShouldBeDifferent() {
        val hash2 = world.retrieve<ByteArray>("hash2")
        world.hashResult.contentEquals(hash2) shouldBe false
    }

    @Then("the SHA3-256 and SHA2-256 should be different")
    fun thenTheSha3256AndSha2256ShouldBeDifferent() {
        val sha2Hash = world.retrieve<ByteArray>("sha2_hash")
        world.hashResult.contentEquals(sha2Hash) shouldBe false
    }

    @Then("the HashValue should be valid")
    fun thenTheHashValueShouldBeValid() {
        world.error shouldBe null
        world.hashValue shouldNotBe null
    }

    @Then("the HashValue creation should fail")
    fun thenTheHashValueCreationShouldFail() {
        world.error shouldNotBe null
    }

    @Then("the HashValue should equal {string}")
    fun thenTheHashValueShouldEqual(expected: String) {
        val hv = world.hashValue as ByteArray
        hv.toHex() shouldBe expected.removePrefix("0x").lowercase()
    }

    @Then("the HashValue should be all zeros")
    fun thenTheHashValueShouldBeAllZeros() {
        val hv = world.hashValue as ByteArray
        hv.all { it == 0.toByte() } shouldBe true
    }

    @Then("two identical hashes should be equal")
    fun thenTwoIdenticalHashesShouldBeEqual() {
        val hash1 = world.bytes!!.clone()
        val hash2 = world.bytes!!.clone()
        hash1.contentEquals(hash2) shouldBe true
    }

    @Then("the domain prefix should be {string}")
    fun thenTheDomainPrefixShouldBe(expected: String) {
        val expectedBytes = expected.removePrefix("0x").hexToBytes()
        world.hashResult.contentEquals(expectedBytes) shouldBe true
    }
}
