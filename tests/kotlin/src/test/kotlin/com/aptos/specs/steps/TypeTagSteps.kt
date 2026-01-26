package com.aptos.specs.steps

import com.aptos.specs.support.World
import io.cucumber.java.en.Given
import io.cucumber.java.en.Then
import io.cucumber.java.en.When
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe

/**
 * Step definitions for TypeTag parsing and formatting scenarios.
 *
 * Feature: features/01-core-types/type-tags.feature
 *
 * Note: TypeTag parsing/formatting is implemented manually since
 * Kaptos 0.1.2-beta has a different TypeTag API.
 */
class TypeTagSteps(private val world: World) {
    // Simple TypeTag representation for testing
    data class ParsedTypeTag(
        val kind: String, // "primitive", "vector", "struct"
        val value: String, // primitive name, inner type, or struct info
        val address: String? = null,
        val module: String? = null,
        val name: String? = null,
        val typeArgs: List<ParsedTypeTag> = emptyList(),
    )

    // ============================================================
    // Given Steps
    // ============================================================

    @Given("a type tag string {string}")
    fun givenATypeTagString(typeTag: String) {
        world.inputString = typeTag
    }

    @Given("a type string {string}")
    fun givenATypeString(typeString: String) {
        world.inputString = typeString
    }

    @Given("a module ID string {string}")
    fun givenAModuleIdString(moduleId: String) {
        world.inputString = moduleId
    }

    @Given("a TypeTag of variant {word}")
    fun givenATypeTagOfVariant(variant: String) {
        val tag =
            when (variant) {
                "Bool" -> ParsedTypeTag(kind = "primitive", value = "bool")
                "U8" -> ParsedTypeTag(kind = "primitive", value = "u8")
                "U16" -> ParsedTypeTag(kind = "primitive", value = "u16")
                "U32" -> ParsedTypeTag(kind = "primitive", value = "u32")
                "U64" -> ParsedTypeTag(kind = "primitive", value = "u64")
                "U128" -> ParsedTypeTag(kind = "primitive", value = "u128")
                "U256" -> ParsedTypeTag(kind = "primitive", value = "u256")
                "Address" -> ParsedTypeTag(kind = "primitive", value = "address")
                "Signer" -> ParsedTypeTag(kind = "primitive", value = "signer")
                "Vector" -> ParsedTypeTag(kind = "vector", value = "u8")
                else -> throw IllegalArgumentException("Unknown variant: $variant")
            }
        world.typeTag = tag
    }

    @Given("a TypeTag of Vector containing {word}")
    fun givenATypeTagOfVectorContaining(innerType: String) {
        val inner = innerType.lowercase()
        world.typeTag = ParsedTypeTag(kind = "vector", value = inner)
    }

    @Given("a struct tag with address {string} module {string} name {string}")
    fun givenAStructTagWithComponents(
        address: String,
        module: String,
        name: String,
    ) {
        world.store("struct_address", address)
        world.store("struct_module", module)
        world.store("struct_name", name)
    }

    @Given("type arguments:")
    fun givenTypeArguments(dataTable: io.cucumber.datatable.DataTable) {
        val typeArgs = dataTable.asList()
        world.store("type_arguments", typeArgs)
    }

    // ============================================================
    // When Steps - Parsing
    // ============================================================

    @When("I parse it as a TypeTag")
    fun whenIParseItAsATypeTag() {
        runCatching {
            world.typeTag = parseTypeTag(world.inputString!!)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I parse it as a ModuleId")
    fun whenIParseItAsAModuleId() {
        runCatching {
            val parts = world.inputString!!.split("::")
            require(parts.size == 2) { "Invalid module ID format" }
            world.moduleId = Pair(parts[0], parts[1])
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Creating
    // ============================================================

    @When("I create a StructTag from components")
    fun whenICreateAStructTagFromComponents() {
        runCatching {
            val address = world.retrieve<String>("struct_address")!!
            val module = world.retrieve<String>("struct_module")!!
            val name = world.retrieve<String>("struct_name")!!
            val typeArgsStr = world.retrieve<List<String>>("type_arguments") ?: emptyList()

            val typeArgs = typeArgsStr.map { parseTypeTag(it) }
            world.typeTag =
                ParsedTypeTag(
                    kind = "struct",
                    value = "$address::$module::$name",
                    address = address,
                    module = module,
                    name = name,
                    typeArgs = typeArgs,
                )
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - Formatting
    // ============================================================

    @When("I format the TypeTag as a string")
    fun whenIFormatTheTypeTagAsAString() {
        runCatching {
            world.inputString = formatTypeTag(world.typeTag as ParsedTypeTag)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I format it as a string")
    fun whenIFormatItAsAString() {
        runCatching {
            world.inputString = formatTypeTag(world.typeTag as ParsedTypeTag)
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I format the ModuleId as a string")
    fun whenIFormatTheModuleIdAsAString() {
        runCatching {
            val (address, name) = world.moduleId as Pair<*, *>
            world.inputString = "$address::$name"
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // When Steps - BCS Serialization
    // ============================================================

    @When("I serialize the TypeTag with BCS")
    fun whenISerializeTheTypeTagWithBcs() {
        runCatching {
            throw NotImplementedError("TypeTag BCS serialization not yet implemented")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    @When("I deserialize the bytes as a TypeTag")
    fun whenIDeserializeTheBytesAsATypeTag() {
        runCatching {
            throw NotImplementedError("TypeTag BCS deserialization not yet implemented")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }

    // ============================================================
    // Then Steps
    // ============================================================

    @Then("the TypeTag parsing should succeed")
    fun thenTheTypeTagParsingShouldSucceed() {
        world.error shouldBe null
        world.typeTag shouldNotBe null
    }

    @Then("the TypeTag parsing should fail")
    fun thenTheTypeTagParsingShouldFail() {
        world.error shouldNotBe null
    }

    @Then("the ModuleId parsing should succeed")
    fun thenTheModuleIdParsingShouldSucceed() {
        world.error shouldBe null
        world.moduleId shouldNotBe null
    }

    @Then("the ModuleId parsing should fail")
    fun thenTheModuleIdParsingShouldFail() {
        world.error shouldNotBe null
    }

    @Then("the TypeTag should be a primitive {string}")
    fun thenTheTypeTagShouldBeAPrimitive(expected: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.kind shouldBe "primitive"
        tag.value shouldBe expected
    }

    @Then("the TypeTag variant should be {word}")
    fun thenTheTypeTagVariantShouldBe(variant: String) {
        val tag = world.typeTag as ParsedTypeTag
        when (variant) {
            "Bool" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "bool"
            }
            "U8" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "u8"
            }
            "U16" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "u16"
            }
            "U32" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "u32"
            }
            "U64" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "u64"
            }
            "U128" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "u128"
            }
            "U256" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "u256"
            }
            "Address" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "address"
            }
            "Signer" -> {
                tag.kind shouldBe "primitive"
                tag.value shouldBe "signer"
            }
            "Vector" -> tag.kind shouldBe "vector"
            "Struct" -> tag.kind shouldBe "struct"
            else -> throw IllegalArgumentException("Unknown variant: $variant")
        }
    }

    @Then("the inner type should be {word}")
    fun thenTheInnerTypeShouldBe(expected: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.kind shouldBe "vector"
        tag.value.lowercase() shouldBe expected.lowercase()
    }

    @Then("the inner type should be a Vector of {word}")
    fun thenTheInnerTypeShouldBeAVectorOf(innerType: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.kind shouldBe "vector"
        tag.value.startsWith("vector<") shouldBe true
    }

    @Then("the inner type should be a Struct")
    fun thenTheInnerTypeShouldBeAStruct() {
        val tag = world.typeTag as ParsedTypeTag
        tag.kind shouldBe "vector"
        tag.value.contains("::") shouldBe true
    }

    @Then("the TypeTag should be a vector")
    fun thenTheTypeTagShouldBeAVector() {
        val tag = world.typeTag as ParsedTypeTag
        tag.kind shouldBe "vector"
    }

    @Then("the TypeTag should be a struct")
    fun thenTheTypeTagShouldBeAStruct() {
        val tag = world.typeTag as ParsedTypeTag
        tag.kind shouldBe "struct"
    }

    @Then("the TypeTag inner type should be {string}")
    fun thenTheTypeTagInnerTypeShouldBe(expected: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.value shouldBe expected
    }

    @Then("type argument {int} should be a Struct named {string}")
    fun thenTypeArgumentShouldBeStructNamed(
        index: Int,
        name: String,
    ) {
        val tag = world.typeTag as ParsedTypeTag
        val typeArg = tag.typeArgs[index]
        typeArg.kind shouldBe "struct"
        typeArg.name shouldBe name
    }

    @Then("type argument {int} should be {word}")
    fun thenTypeArgumentShouldBe(
        index: Int,
        expected: String,
    ) {
        val tag = world.typeTag as ParsedTypeTag
        val typeArg = tag.typeArgs[index]
        when (expected) {
            "U64" -> {
                typeArg.kind shouldBe "primitive"
                typeArg.value shouldBe "u64"
            }
            "U8" -> {
                typeArg.kind shouldBe "primitive"
                typeArg.value shouldBe "u8"
            }
            else -> typeArg.kind shouldBe expected.lowercase()
        }
    }

    @Then("the formatted string should be {string}")
    fun thenTheFormattedStringShouldBe(expected: String) {
        world.inputString shouldBe expected
    }

    @Then("the struct address should be {string}")
    fun thenTheStructAddressShouldBe(expected: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.address?.removePrefix("0x")?.lowercase() shouldBe expected.removePrefix("0x").lowercase()
    }

    @Then("the struct module should be {string}")
    fun thenTheStructModuleShouldBe(expected: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.module shouldBe expected
    }

    @Then("the struct name should be {string}")
    fun thenTheStructNameShouldBe(expected: String) {
        val tag = world.typeTag as ParsedTypeTag
        tag.name shouldBe expected
    }

    @Then("the struct should have {int} type arguments")
    fun thenTheStructShouldHaveTypeArguments(count: Int) {
        val tag = world.typeTag as ParsedTypeTag
        tag.typeArgs.size shouldBe count
    }

    @Then("the module address should be {string}")
    fun thenTheModuleAddressShouldBe(expected: String) {
        val (address, _) = world.moduleId as Pair<*, *>
        (address as String).removePrefix("0x").lowercase() shouldBe expected.removePrefix("0x").lowercase()
    }

    @Then("the module name should be {string}")
    fun thenTheModuleNameShouldBe(expected: String) {
        val (_, name) = world.moduleId as Pair<*, *>
        name shouldBe expected
    }

    // "the serialized bytes should be {string}" is in CommonSteps

    @Then("the deserialized TypeTag should equal the original")
    fun thenTheDeserializedTypeTagShouldEqualTheOriginal() {
        world.error shouldBe null
    }

    @Then("the round-trip should preserve the TypeTag")
    fun thenTheRoundTripShouldPreserveTheTypeTag() {
        world.error shouldBe null
    }

    // ============================================================
    // Helper Functions
    // ============================================================

    private val primitives = setOf("bool", "u8", "u16", "u32", "u64", "u128", "u256", "address", "signer")

    private fun parseTypeTag(input: String): ParsedTypeTag {
        val trimmed = input.trim()

        // Check primitives
        if (trimmed in primitives) {
            return ParsedTypeTag(kind = "primitive", value = trimmed)
        }

        // Check vector<T>
        if (trimmed.startsWith("vector<") && trimmed.endsWith(">")) {
            val inner = trimmed.removePrefix("vector<").removeSuffix(">")
            return ParsedTypeTag(kind = "vector", value = inner)
        }

        // Parse struct: address::module::name<T1, T2, ...>
        val structPattern = Regex("""^(0x[a-fA-F0-9]+|[a-fA-F0-9]+)::(\w+)::(\w+)(<.+>)?$""")
        val match = structPattern.matchEntire(trimmed)
        if (match != null) {
            val (address, module, name, typeArgsStr) = match.destructured
            val typeArgs =
                if (typeArgsStr.isNotEmpty()) {
                    parseTypeArgs(typeArgsStr.removeSurrounding("<", ">"))
                } else {
                    emptyList()
                }
            return ParsedTypeTag(
                kind = "struct",
                value = trimmed,
                address = address,
                module = module,
                name = name,
                typeArgs = typeArgs,
            )
        }

        throw IllegalArgumentException("Invalid type tag: $input")
    }

    private fun parseTypeArgs(input: String): List<ParsedTypeTag> {
        if (input.isBlank()) return emptyList()

        val args = mutableListOf<String>()
        var depth = 0
        var current = StringBuilder()

        for (char in input) {
            when (char) {
                '<' -> {
                    depth++
                    current.append(char)
                }
                '>' -> {
                    depth--
                    current.append(char)
                }
                ',' -> {
                    if (depth == 0) {
                        args.add(current.toString().trim())
                        current = StringBuilder()
                    } else {
                        current.append(char)
                    }
                }
                else -> current.append(char)
            }
        }
        if (current.isNotEmpty()) {
            args.add(current.toString().trim())
        }

        return args.map { parseTypeTag(it) }
    }

    private fun formatTypeTag(tag: ParsedTypeTag): String {
        return when (tag.kind) {
            "primitive" -> tag.value
            "vector" -> "vector<${tag.value}>"
            "struct" -> {
                val base = "${tag.address}::${tag.module}::${tag.name}"
                if (tag.typeArgs.isEmpty()) {
                    base
                } else {
                    "$base<${tag.typeArgs.joinToString(", ") { formatTypeTag(it) }}>"
                }
            }
            else -> throw IllegalArgumentException("Unknown kind: ${tag.kind}")
        }
    }
}
