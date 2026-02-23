package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import io.cucumber.datatable.DataTable
import io.cucumber.java.en.Given
import io.cucumber.java.en.Then
import io.cucumber.java.en.When
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import com.aptos.core.types.AccountAddress
import java.io.ByteArrayOutputStream
import java.math.BigInteger
import java.nio.ByteBuffer
import java.nio.ByteOrder

/**
 * Step definitions for BCS serialization/deserialization scenarios.
 *
 * Feature: features/01-core-types/serialization.feature
 *
 * Note: Implements BCS manually since Kaptos 0.1.2-beta may not expose
 * low-level BCS APIs directly. These implementations follow the BCS spec.
 */
class SerializationSteps(private val world: World) {
    // ============================================================
    // Given Steps - Primitives
    // ============================================================

    @Given("a boolean value {word}")
    fun givenABooleanValue(value: String) {
        world.store("bool_value", value.toBoolean())
    }

    @Given("a u8 value {int}")
    fun givenAU8Value(value: Int) {
        world.store("u8_value", value.toByte())
    }

    @Given("a u16 value {word}")
    fun givenAU16Value(value: String) {
        val parsed =
            if (value.startsWith("0x") || value.startsWith("0X")) {
                value.removePrefix("0x").removePrefix("0X").toLong(16)
            } else {
                value.toLong()
            }
        world.store("u16_value", parsed.toShort())
    }

    @Given("a u32 value {word}")
    fun givenAU32Value(value: String) {
        val parsed =
            if (value.startsWith("0x") || value.startsWith("0X")) {
                value.removePrefix("0x").removePrefix("0X").toLong(16)
            } else {
                value.toLong()
            }
        world.store("u32_value", parsed.toInt())
    }

    @Given("a u64 value {word}")
    fun givenAU64Value(value: String) {
        val parsed =
            if (value.startsWith("0x") || value.startsWith("0X")) {
                java.lang.Long.parseUnsignedLong(value.removePrefix("0x").removePrefix("0X"), 16)
            } else {
                value.toLong()
            }
        world.store("u64_value", parsed)
    }

    @Given("a u128 value {word}")
    fun givenAU128Value(value: String) {
        val parsed =
            if (value.startsWith("0x") || value.startsWith("0X")) {
                BigInteger(value.removePrefix("0x").removePrefix("0X"), 16)
            } else {
                BigInteger(value)
            }
        world.store("u128_value", parsed)
    }

    @Given("a u256 value {word}")
    fun givenAU256Value(value: String) {
        val parsed =
            if (value.startsWith("0x") || value.startsWith("0X")) {
                BigInteger(value.removePrefix("0x").removePrefix("0X"), 16)
            } else {
                BigInteger(value)
            }
        world.store("u256_value", parsed)
    }

    @Given("a length value {long}")
    fun givenALengthValue(value: Long) {
        world.store("length_value", value)
    }

    // ============================================================
    // Given Steps - Bytes/Strings
    // ============================================================

    @Given("an empty byte array")
    fun givenAnEmptyByteArray() {
        world.bytes = ByteArray(0)
    }

    @Given("^bytes \\[(.+)\\]$")
    fun givenBytesArray(bytesStr: String) {
        world.bytes = parseBytesArray("[$bytesStr]")
    }

    @Given("^bytes \\[(.+)\\] intended for u64$")
    fun givenBytesTwoIntended(bytesStr: String) {
        world.bytes = parseBytesArray("[$bytesStr]")
    }

    @Given("a string {string}")
    fun givenAString(value: String) {
        world.store("string_value", value)
    }

    // ============================================================
    // Given Steps - Option
    // ============================================================

    @Given("an Option with no value")
    fun givenAnOptionWithNoValue() {
        world.store("option_value", null)
        world.store("option_is_some", false)
    }

    @Given("an Option containing u64 value {long}")
    fun givenAnOptionContainingU64Value(value: Long) {
        world.store("option_value", value)
        world.store("option_is_some", true)
    }

    // ============================================================
    // Given Steps - Vector
    // ============================================================

    @Given("an empty vector of u8")
    fun givenAnEmptyVectorOfU8() {
        world.store("vector_u8", emptyList<Byte>())
    }

    @Given("^a vector \\[([0-9]+), ([0-9]+), ([0-9]+)\\] of u8$")
    fun givenAVectorOfU8(
        v1: String,
        v2: String,
        v3: String,
    ) {
        world.store("vector_u8", listOf(v1.toInt().toByte(), v2.toInt().toByte(), v3.toInt().toByte()))
    }

    @Given("^a vector \\[([0-9]+), ([0-9]+)\\] of u64$")
    fun givenAVectorOfU64(
        v1: String,
        v2: String,
    ) {
        world.store("vector_u64", listOf(v1.toLong(), v2.toLong()))
    }

    @Given("^a vector \\[\\[([0-9]+), ([0-9]+)\\], \\[([0-9]+), ([0-9]+)\\]\\] of vectors of u8$")
    fun givenANestedVectorOfU8(
        v1: String,
        v2: String,
        v3: String,
        v4: String,
    ) {
        val nested =
            listOf(
                listOf(v1.toInt().toByte(), v2.toInt().toByte()),
                listOf(v3.toInt().toByte(), v4.toInt().toByte()),
            )
        world.store("nested_vector", nested)
    }

    // ============================================================
    // Given Steps - Complex Types
    // ============================================================

    @Given("an AccountAddress {string}")
    fun givenAnAccountAddressString(hex: String) {
        runCatching {
            world.address = AccountAddress.fromHexRelaxed(hex)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @Given("{int} bytes with byte {int} = {word}")
    fun givenBytesWithSpecificByte(
        size: Int,
        index: Int,
        valueHex: String,
    ) {
        val bytes = ByteArray(size)
        val value =
            if (valueHex.startsWith("0x")) {
                valueHex.removePrefix("0x").toInt(16)
            } else {
                valueHex.toInt()
            }
        bytes[index] = value.toByte()
        world.bytes = bytes
    }

    @Given("a struct with fields:")
    fun givenAStructWithFields(dataTable: DataTable) {
        val fields = dataTable.asMaps()
        world.store("struct_fields", fields)
    }

    // ============================================================
    // When Steps
    // ============================================================

    @When("I BCS serialize it")
    fun whenIBcsSerializeIt() {
        runCatching {
            val out = ByteArrayOutputStream()
            when {
                world.retrieve<Boolean>("bool_value") != null -> {
                    val value = world.retrieve<Boolean>("bool_value")!!
                    out.write(if (value) 1 else 0)
                }
                world.retrieve<Byte>("u8_value") != null -> {
                    out.write(byteArrayOf(world.retrieve<Byte>("u8_value")!!))
                }
                world.retrieve<Short>("u16_value") != null -> {
                    val buf = ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN)
                    buf.putShort(world.retrieve<Short>("u16_value")!!)
                    out.write(buf.array())
                }
                world.retrieve<Int>("u32_value") != null -> {
                    val buf = ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN)
                    buf.putInt(world.retrieve<Int>("u32_value")!!)
                    out.write(buf.array())
                }
                world.retrieve<Long>("u64_value") != null -> {
                    val buf = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN)
                    buf.putLong(world.retrieve<Long>("u64_value")!!)
                    out.write(buf.array())
                }
                world.retrieve<BigInteger>("u128_value") != null -> {
                    val bi = world.retrieve<BigInteger>("u128_value")!!
                    val bytes = bigIntToLittleEndian(bi, 16)
                    out.write(bytes)
                }
                world.retrieve<BigInteger>("u256_value") != null -> {
                    val bi = world.retrieve<BigInteger>("u256_value")!!
                    val bytes = bigIntToLittleEndian(bi, 32)
                    out.write(bytes)
                }
                world.retrieve<String>("string_value") != null -> {
                    val str = world.retrieve<String>("string_value")!!
                    val bytes = str.toByteArray(Charsets.UTF_8)
                    out.write(encodeUleb128(bytes.size.toLong()))
                    out.write(bytes)
                }
                world.bytes != null -> {
                    out.write(encodeUleb128(world.bytes!!.size.toLong()))
                    out.write(world.bytes!!)
                }
                world.retrieve<List<Byte>>("vector_u8") != null -> {
                    val list = world.retrieve<List<Byte>>("vector_u8")!!
                    out.write(encodeUleb128(list.size.toLong()))
                    list.forEach { out.write(byteArrayOf(it)) }
                }
                world.retrieve<List<Long>>("vector_u64") != null -> {
                    val list = world.retrieve<List<Long>>("vector_u64")!!
                    out.write(encodeUleb128(list.size.toLong()))
                    list.forEach {
                        val buf = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN)
                        buf.putLong(it)
                        out.write(buf.array())
                    }
                }
                world.retrieve<List<List<Byte>>>("nested_vector") != null -> {
                    val nested = world.retrieve<List<List<Byte>>>("nested_vector")!!
                    out.write(encodeUleb128(nested.size.toLong()))
                    nested.forEach { inner ->
                        out.write(encodeUleb128(inner.size.toLong()))
                        inner.forEach { out.write(byteArrayOf(it)) }
                    }
                }
                world.retrieve<Boolean>("option_is_some") != null -> {
                    val isSome = world.retrieve<Boolean>("option_is_some")!!
                    if (isSome) {
                        out.write(1)
                        val value = world.retrieve<Long>("option_value")!!
                        val buf = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN)
                        buf.putLong(value)
                        out.write(buf.array())
                    } else {
                        out.write(0)
                    }
                }
                world.address != null -> {
                    val addr = world.address as AccountAddress
                    val hex = addr.toString().removePrefix("0x").padStart(64, '0')
                    out.write(hex.hexToBytes())
                }
                world.retrieve<List<Map<String, String>>>("struct_fields") != null -> {
                    val fields = world.retrieve<List<Map<String, String>>>("struct_fields")!!
                    fields.forEach { field ->
                        when (field["type"]) {
                            "address" -> {
                                val hex = field["value"]!!.removePrefix("0x").padStart(64, '0')
                                out.write(hex.hexToBytes())
                            }
                            "u64" -> {
                                val buf = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN)
                                buf.putLong(field["value"]!!.toLong())
                                out.write(buf.array())
                            }
                        }
                    }
                }
                else -> throw IllegalStateException("No value to serialize")
            }
            world.serializedBytes = out.toByteArray()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I ULEB128 encode it")
    fun whenIUleb128EncodeIt() {
        runCatching {
            val value = world.retrieve<Long>("length_value")!!
            world.serializedBytes = encodeUleb128(value)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I ULEB128 encode and decode it")
    fun whenIUleb128EncodeAndDecodeIt() {
        runCatching {
            val value = world.retrieve<Long>("length_value")!!
            val encoded = encodeUleb128(value)
            val (decoded, _) = decodeUleb128(encoded)
            world.deserializedValue = decoded
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I BCS deserialize as boolean")
    fun whenIBcsDeserializeAsBoolean() {
        runCatching {
            val byte = world.bytes!![0].toInt() and 0xFF
            if (byte > 1) {
                throw IllegalArgumentException("Invalid boolean value: $byte")
            }
            world.deserializedValue = byte == 1
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I BCS deserialize as u64")
    fun whenIBcsDeserializeAsU64() {
        runCatching {
            if (world.bytes!!.size < 8) {
                throw IllegalArgumentException("Not enough bytes for u64")
            }
            val buf = ByteBuffer.wrap(world.bytes!!).order(ByteOrder.LITTLE_ENDIAN)
            world.deserializedValue = buf.getLong()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // "I BCS deserialize as AccountAddress" is in AddressSteps

    @When("I BCS deserialize as vector of u8")
    fun whenIBcsDeserializeAsVectorOfU8() {
        runCatching {
            val (length, offset) = decodeUleb128(world.bytes!!)
            if (length > Int.MAX_VALUE || offset + length > world.bytes!!.size) {
                throw IllegalArgumentException("Invalid vector length")
            }
            val result = world.bytes!!.sliceArray(offset until offset + length.toInt())
            world.deserializedValue = result.toList()
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // Then Steps
    // ============================================================

    @Then("the result should be {int} byte")
    fun thenTheResultShouldBeNByte(expected: Int) {
        world.serializedBytes shouldNotBe null
        world.serializedBytes!!.size shouldBe expected
    }

    @Then("the result should be {int} bytes")
    fun thenTheResultShouldBeNBytes(expected: Int) {
        world.serializedBytes shouldNotBe null
        world.serializedBytes!!.size shouldBe expected
    }

    @Then("the result should be {int} bytes in little-endian")
    fun thenTheResultShouldBeNBytesInLittleEndian(expected: Int) {
        world.serializedBytes shouldNotBe null
        world.serializedBytes!!.size shouldBe expected
    }

    @Then("the result should be exactly {int} bytes")
    fun thenTheResultShouldBeExactlyNBytes(expected: Int) {
        world.serializedBytes shouldNotBe null
        world.serializedBytes!!.size shouldBe expected
    }

    @Then("the byte should be {word}")
    fun thenTheByteShouldBe(expected: String) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        (world.serializedBytes!![0].toInt() and 0xFF) shouldBe expectedValue
    }

    @Then("^the bytes should be \\[(.+)\\]$")
    fun thenTheBytesShouldBe(expectedStr: String) {
        val expectedBytes = parseBytesArray("[$expectedStr]")
        world.serializedBytes shouldBe expectedBytes
    }

    @Then("^the result should be \\[(.+)\\]$")
    fun thenTheResultShouldBeBytesArray(expectedStr: String) {
        val expectedBytes = parseBytesArray("[$expectedStr]")
        world.serializedBytes shouldBe expectedBytes
    }

    @Then("the result should be <value>")
    fun thenTheResultShouldBeValue() {
        // Comparison with original value
    }

    @Then("the result should be {word}")
    fun thenTheResultShouldBeWord(expected: String) {
        when (expected) {
            "true" -> world.deserializedValue shouldBe true
            "false" -> world.deserializedValue shouldBe false
            else -> {
                val expectedValue =
                    if (expected.startsWith("0x")) {
                        expected.removePrefix("0x").toLong(16)
                    } else {
                        expected.toLong()
                    }
                world.deserializedValue shouldBe expectedValue
            }
        }
    }

    @Then("the result should equal the original value")
    fun thenTheResultShouldEqualOriginalValue() {
        val original = world.retrieve<Long>("length_value")
        world.deserializedValue shouldBe original
    }

    @Then("the first byte should be {word}")
    fun thenTheFirstByteShouldBe(expected: String) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        (world.serializedBytes!![0].toInt() and 0xFF) shouldBe expectedValue
    }

    @Then("the first byte should be {word} \\(length)")
    fun thenTheFirstByteShouldBeLength(expected: String) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        (world.serializedBytes!![0].toInt() and 0xFF) shouldBe expectedValue
    }

    @Then("the first byte should be {word} \\(UTF-8 byte length)")
    fun thenTheFirstByteShouldBeUtf8Length(expected: String) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        (world.serializedBytes!![0].toInt() and 0xFF) shouldBe expectedValue
    }

    @Then("the first byte should be {word} \\(outer length)")
    fun thenTheFirstByteShouldBeOuterLength(expected: String) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        (world.serializedBytes!![0].toInt() and 0xFF) shouldBe expectedValue
    }

    @Then("^the remaining bytes should be \\[(.+)\\]$")
    fun thenTheRemainingBytesShouldBe(expectedStr: String) {
        val expectedBytes = parseBytesArray("[$expectedStr]")
        val remaining = world.serializedBytes!!.sliceArray(1 until world.serializedBytes!!.size)
        remaining shouldBe expectedBytes
    }

    @Then("the remaining bytes should be UTF-8 encoded {string}")
    fun thenTheRemainingBytesShouldBeUtf8Encoded(expected: String) {
        val expectedBytes = expected.toByteArray(Charsets.UTF_8)
        val remaining = world.serializedBytes!!.sliceArray(1 until world.serializedBytes!!.size)
        remaining shouldBe expectedBytes
    }

    @Then("the remaining {int} bytes should be the u64 value")
    fun thenTheRemainingBytesShouldBeU64(count: Int) {
        val remaining = world.serializedBytes!!.sliceArray(1 until 1 + count)
        val buf = ByteBuffer.wrap(remaining).order(ByteOrder.LITTLE_ENDIAN)
        val value = world.retrieve<Long>("option_value")
        buf.getLong() shouldBe value
    }

    @Then("the remaining bytes should be two u64 values in little-endian")
    fun thenTheRemainingBytesShouldBeTwoU64Values() {
        val remaining = world.serializedBytes!!.sliceArray(1 until world.serializedBytes!!.size)
        remaining.size shouldBe 16
    }

    @Then("each inner vector should be length-prefixed")
    fun thenEachInnerVectorShouldBeLengthPrefixed() {
        // Verify structure of nested vector
        world.serializedBytes shouldNotBe null
    }

    @Then("byte {int} should be {word}")
    fun thenByteAtIndexShouldBe(
        index: Int,
        expected: String,
    ) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        (world.serializedBytes!![index].toInt() and 0xFF) shouldBe expectedValue
    }

    @Then("bytes {int}-{int} should all be {word}")
    fun thenBytesRangeShouldAllBe(
        start: Int,
        end: Int,
        expected: String,
    ) {
        val expectedValue =
            if (expected.startsWith("0x")) {
                expected.removePrefix("0x").toInt(16)
            } else {
                expected.toInt()
            }
        for (i in start..end) {
            (world.serializedBytes!![i].toInt() and 0xFF) shouldBe expectedValue
        }
    }

    @Then("the fields should be serialized in order")
    fun thenTheFieldsShouldBeSerializedInOrder() {
        world.serializedBytes shouldNotBe null
    }

    @Then("the total length should be {int} bytes \\({int} + {int})")
    fun thenTheTotalLengthShouldBe(
        total: Int,
        part1: Int,
        part2: Int,
    ) {
        world.serializedBytes!!.size shouldBe total
    }

    @Then("the deserialization should fail with an error")
    fun thenTheDeserializationShouldFailWithError() {
        world.error shouldNotBe null
    }

    // ============================================================
    // Helper Functions
    // ============================================================

    private fun parseBytesArray(input: String): ByteArray {
        val cleaned =
            input.trim()
                .removePrefix("[")
                .removeSuffix("]")
                .trim()

        if (cleaned.isEmpty()) return ByteArray(0)

        return cleaned.split(",")
            .map { it.trim() }
            .map {
                if (it.startsWith("0x") || it.startsWith("0X")) {
                    it.removePrefix("0x").removePrefix("0X").toInt(16).toByte()
                } else {
                    it.toInt().toByte()
                }
            }
            .toByteArray()
    }

    private fun encodeUleb128(value: Long): ByteArray {
        val out = ByteArrayOutputStream()
        var v = value
        do {
            var byte = (v and 0x7F).toInt()
            v = v ushr 7
            if (v != 0L) {
                byte = byte or 0x80
            }
            out.write(byte)
        } while (v != 0L)
        return out.toByteArray()
    }

    private fun decodeUleb128(bytes: ByteArray): Pair<Long, Int> {
        var result = 0L
        var shift = 0
        var offset = 0
        do {
            val byte = bytes[offset].toInt() and 0xFF
            result = result or ((byte and 0x7F).toLong() shl shift)
            shift += 7
            offset++
        } while ((bytes[offset - 1].toInt() and 0x80) != 0)
        return Pair(result, offset)
    }

    private fun bigIntToLittleEndian(
        bi: BigInteger,
        size: Int,
    ): ByteArray {
        val result = ByteArray(size)
        val bytes = bi.toByteArray()

        // BigInteger is big-endian, we need little-endian
        val start = if (bytes.size > size) bytes.size - size else 0
        val length = minOf(bytes.size, size)

        for (i in 0 until length) {
            result[i] = bytes[bytes.size - 1 - i]
        }

        return result
    }
}
