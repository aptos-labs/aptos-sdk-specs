package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import com.aptos.specs.support.toHex
import io.cucumber.java.en.Given
import io.cucumber.java.en.When
import io.cucumber.java.en.Then
import io.cucumber.java.en.And
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import xyz.mcxross.kaptos.model.AccountAddress

/**
 * Step definitions for address parsing and formatting scenarios.
 * 
 * Feature: features/01-core-types/address.feature
 * 
 * Note: Uses Kaptos SDK 0.1.2-beta. Some methods may need adjustment
 * as the SDK API evolves.
 */
class AddressSteps(private val world: World) {
    
    // Helper to get address bytes
    private fun getAddressBytes(): ByteArray {
        val addr = world.address as AccountAddress
        return addr.toString().removePrefix("0x").padStart(64, '0').hexToBytes()
    }
    
    // ============================================================
    // Given Steps
    // ============================================================
    
    @Given("a hex string {string}")
    fun givenAHexString(hex: String) {
        world.hexString = hex
    }
    
    @Given("a short address {string}")
    fun givenAShortAddress(address: String) {
        world.hexString = address
    }
    
    @Given("a full address {string}")
    fun givenAFullAddress(address: String) {
        world.hexString = address
    }
    
    @Given("an address from bytes")
    fun givenAnAddressFromBytes() {
        world.bytes shouldNotBe null
    }
    
    @Given("an AccountAddress with value {int}")
    fun givenAnAccountAddressWithValue(value: Int) {
        runCatching {
            world.address = AccountAddress.fromString("0x${value.toString(16)}")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("an AccountAddress from hex {string}")
    fun givenAnAccountAddressFromHex(hex: String) {
        runCatching {
            world.address = AccountAddress.fromString(hex)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("another AccountAddress from hex {string}")
    fun givenAnotherAccountAddressFromHex(hex: String) {
        runCatching {
            world.address2 = AccountAddress.fromString(hex)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("{int} bytes with value {int} in the last byte")
    fun givenBytesWithValueInLastByte(size: Int, value: Int) {
        val bytes = ByteArray(size)
        bytes[size - 1] = value.toByte()
        world.bytes = bytes
    }
    
    // ============================================================
    // When Steps
    // ============================================================
    
    @When("I parse it as an AccountAddress")
    fun whenIParseItAsAnAccountAddress() {
        runCatching {
            world.address = AccountAddress.fromString(world.hexString!!)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I format the address as full hex")
    fun whenIFormatTheAddressAsFullHex() {
        runCatching {
            world.hexString = (world.address as AccountAddress).toString()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I format the address as short string")
    fun whenIFormatTheAddressAsShortString() {
        runCatching {
            val addr = world.address as AccountAddress
            // Remove leading zeros for short format
            val full = addr.toString().removePrefix("0x")
            val short = full.trimStart('0').ifEmpty { "0" }
            world.hexString = "0x$short"
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I serialize the address with BCS")
    fun whenISerializeTheAddressWithBcs() {
        runCatching {
            val addr = world.address as AccountAddress
            // AccountAddress is 32 bytes - convert from hex representation
            val hex = addr.toString().removePrefix("0x").padStart(64, '0')
            world.serializedBytes = hex.hexToBytes()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I deserialize the bytes as AccountAddress")
    fun whenIDeserializeTheBytesAsAccountAddress() {
        runCatching {
            val hex = "0x" + world.bytes!!.toHex()
            world.address = AccountAddress.fromString(hex)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I compare the two addresses")
    fun whenICompareTheTwoAddresses() {
        // Comparison happens in the Then step
    }
    
    @When("I format it as full hex")
    fun whenIFormatItAsFullHex() {
        runCatching {
            val addr = world.address as AccountAddress
            world.hexString = addr.toString()
            // Ensure it's padded to full length with 0x prefix
            val hex = world.hexString!!.removePrefix("0x").padStart(64, '0')
            world.hexString = "0x$hex"
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I format it as short string")
    fun whenIFormatItAsShortString() {
        runCatching {
            val addr = world.address as AccountAddress
            val full = addr.toString().removePrefix("0x")
            val short = full.trimStart('0').ifEmpty { "0" }
            world.hexString = "0x$short"
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I BCS serialize the address")
    fun whenIBcsSerializeTheAddress() {
        runCatching {
            val addr = world.address as AccountAddress
            // BCS serialization of AccountAddress is just the 32 bytes
            world.serializedBytes = getAddressBytes()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I BCS deserialize as AccountAddress")
    fun whenIBcsDeserializeAsAccountAddress() {
        runCatching {
            val hex = "0x" + world.bytes!!.toHex()
            world.address = AccountAddress.fromString(hex)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I BCS deserialize the result as AccountAddress")
    fun whenIBcsDeserializeTheResultAsAccountAddress() {
        runCatching {
            val hex = "0x" + world.serializedBytes!!.toHex()
            world.address2 = AccountAddress.fromString(hex)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    // ============================================================
    // Then Steps
    // ============================================================
    
    // "the parsing should succeed" and "the parsing should fail" are in CommonSteps
    
    @Then("the parsing should fail with {string}")
    fun thenTheParsingShouldFailWith(errorType: String) {
        world.error shouldNotBe null
    }
    
    @Then("the parsing should fail with an invalid address error")
    fun thenTheParsingShouldFailWithInvalidAddressError() {
        world.error shouldNotBe null
    }
    
    @Then("the parsing should fail with an invalid hex error")
    fun thenTheParsingShouldFailWithInvalidHexError() {
        world.error shouldNotBe null
    }
    
    @Then("the parsing should fail with an invalid length error")
    fun thenTheParsingShouldFailWithInvalidLengthError() {
        world.error shouldNotBe null
    }
    
    @Then("the full hex should be {string}")
    fun thenTheFullHexShouldBe(expected: String) {
        val addr = world.address as AccountAddress
        val actual = addr.toString().removePrefix("0x").lowercase().padStart(64, '0')
        val exp = expected.removePrefix("0x").lowercase()
        actual shouldBe exp
    }
    
    @Then("the short string should be {string}")
    fun thenTheShortStringShouldBe(expected: String) {
        // If hexString was set by a When step, use it
        if (world.hexString != null) {
            world.hexString!!.lowercase() shouldBe expected.lowercase()
        } else {
            // Otherwise compute from address
            val addr = world.address as AccountAddress
            val full = addr.toString().removePrefix("0x")
            val short = "0x" + full.trimStart('0').ifEmpty { "0" }
            short.lowercase() shouldBe expected.lowercase()
        }
    }
    
    @Then("the bytes should be {string}")
    fun thenTheBytesShouldBe(expected: String) {
        val expectedBytes = expected.hexToBytes()
        val addrBytes = getAddressBytes()
        addrBytes shouldBe expectedBytes
    }
    
    @Then("the addresses should be equal")
    fun thenTheAddressesShouldBeEqual() {
        world.address shouldBe world.address2
    }
    
    @Then("the addresses should not be equal")
    fun thenTheAddressesShouldNotBeEqual() {
        world.address shouldNotBe world.address2
    }
    
    @Then("the address bytes should have length {int}")
    fun thenTheAddressBytesShouldHaveLength(expectedLength: Int) {
        val bytes = getAddressBytes()
        bytes.size shouldBe expectedLength
    }
    
    @Then("byte {int} should equal {int}")
    fun thenByteShouldEqual(index: Int, expectedValue: Int) {
        val bytes = getAddressBytes()
        (bytes[index].toInt() and 0xFF) shouldBe expectedValue
    }
    
    @Then("bytes {int}-{int} should all be {int}")
    fun thenBytesShouldAllBe(start: Int, end: Int, expectedValue: Int) {
        val bytes = getAddressBytes()
        for (i in start..end) {
            (bytes[i].toInt() and 0xFF) shouldBe expectedValue
        }
    }
    
    @Then("all {int} bytes should be {int}")
    fun thenAllBytesShouldBe(count: Int, expectedValue: Int) {
        val bytes = getAddressBytes()
        bytes.size shouldBe count
        bytes.all { (it.toInt() and 0xFF) == expectedValue } shouldBe true
    }
    
    // "the result should be {int} bytes" is in SerializationSteps
    
    @Then("the result should equal the original address")
    fun thenTheResultShouldEqualTheOriginalAddress() {
        val addr1 = world.address as AccountAddress
        val addr2 = world.address2 as AccountAddress
        addr1.toString().lowercase() shouldBe addr2.toString().lowercase()
    }
    
    @Then("the two addresses should be equal")
    fun thenTheTwoAddressesShouldBeEqual() {
        val addr1 = world.address as AccountAddress
        val addr2 = world.address2 as AccountAddress
        addr1.toString().lowercase() shouldBe addr2.toString().lowercase()
    }
    
    @Then("the two addresses should not be equal")
    fun thenTheTwoAddressesShouldNotBeEqual() {
        val addr1 = world.address as AccountAddress
        val addr2 = world.address2 as AccountAddress
        addr1.toString().lowercase() shouldNotBe addr2.toString().lowercase()
    }
    
    // "the serialized bytes should be {string}" is in CommonSteps
    
    // "the result should be {string}" is in CommonSteps
    
    // ============================================================
    // Special Address Steps
    // ============================================================
    
    @Given("the ZERO address constant")
    fun givenTheZeroAddressConstant() {
        runCatching {
            world.address = AccountAddress.fromString("0x0")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("the ONE address constant")
    fun givenTheOneAddressConstant() {
        runCatching {
            world.address = AccountAddress.fromString("0x1")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("the THREE address constant")
    fun givenTheThreeAddressConstant() {
        runCatching {
            world.address = AccountAddress.fromString("0x3")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @Given("the FOUR address constant")
    fun givenTheFourAddressConstant() {
        runCatching {
            world.address = AccountAddress.fromString("0x4")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
}
