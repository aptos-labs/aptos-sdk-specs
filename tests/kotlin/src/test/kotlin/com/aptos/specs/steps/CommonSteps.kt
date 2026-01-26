package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import io.cucumber.java.en.Then
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe

/**
 * Common step definitions shared across multiple features.
 * These steps have generic patterns that could match across different contexts.
 */
class CommonSteps(private val world: World) {
    // ============================================================
    // Generic Parsing Steps
    // ============================================================

    @Then("the parsing should succeed")
    fun thenTheParsingShouldSucceed() {
        world.error shouldBe null
        // At least one result should be non-null
        val hasResult =
            world.address != null ||
                world.typeTag != null ||
                world.moduleId != null
        hasResult shouldBe true
    }

    @Then("the parsing should fail")
    fun thenTheParsingShouldFail() {
        world.error shouldNotBe null
    }

    // ============================================================
    // Generic Serialization Steps
    // ============================================================

    @Then("the serialized bytes should be {string}")
    fun thenTheSerializedBytesShouldBe(expected: String) {
        val expectedBytes = expected.hexToBytes()
        world.serializedBytes shouldBe expectedBytes
    }

    @Then("the serialization should succeed")
    fun thenTheSerializationShouldSucceed() {
        world.error shouldBe null
        world.serializedBytes shouldNotBe null
    }

    @Then("the serialization should fail")
    fun thenTheSerializationShouldFail() {
        world.error shouldNotBe null
    }

    @Then("the deserialization should succeed")
    fun thenTheDeserializationShouldSucceed() {
        world.error shouldBe null
        world.deserializedValue shouldNotBe null
    }

    @Then("the deserialization should fail")
    fun thenTheDeserializationShouldFail() {
        world.error shouldNotBe null
    }

    // ============================================================
    // Generic Result Steps
    // ============================================================

    @Then("the result should be {string}")
    fun thenTheResultShouldBe(expected: String) {
        world.hexString shouldBe expected
    }
}
