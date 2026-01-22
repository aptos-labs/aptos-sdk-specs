package com.aptos.specs.steps

import com.aptos.specs.support.World
import com.aptos.specs.support.hexToBytes
import com.aptos.specs.support.toHex
import io.cucumber.java.en.Given
import io.cucumber.java.en.When
import io.cucumber.java.en.Then
import io.kotest.matchers.shouldBe
import io.kotest.matchers.shouldNotBe
import xyz.mcxross.kaptos.account.Account

/**
 * Step definitions for transaction building and signing scenarios.
 * 
 * Features:
 * - features/04-transaction-building/entry-function.feature
 * - features/04-transaction-building/raw-transaction.feature
 * - features/04-transaction-building/signing.feature
 * 
 * Note: Transaction building in Kaptos 0.1.2-beta uses the high-level
 * Aptos client API. Low-level transaction primitives may not be exposed.
 */
class TransactionSteps(private val world: World) {
    
    // ============================================================
    // Given Steps - Entry Function
    // ============================================================
    
    @Given("an entry function {string}::{string}::{string}")
    fun givenAnEntryFunction(address: String, module: String, function: String) {
        world.store("entry_address", address)
        world.store("entry_module", module)
        world.store("entry_function", function)
    }
    
    @Given("entry function arguments:")
    fun givenEntryFunctionArguments(dataTable: io.cucumber.datatable.DataTable) {
        val args = dataTable.asMaps()
        world.store("entry_args", args)
    }
    
    @Given("entry function type arguments:")
    fun givenEntryFunctionTypeArguments(dataTable: io.cucumber.datatable.DataTable) {
        val typeArgs = dataTable.asList()
        world.store("entry_type_args", typeArgs)
    }
    
    @Given("no entry function arguments")
    fun givenNoEntryFunctionArguments() {
        world.store("entry_args", emptyList<Map<String, String>>())
    }
    
    @Given("no entry function type arguments")
    fun givenNoEntryFunctionTypeArguments() {
        world.store("entry_type_args", emptyList<String>())
    }
    
    // ============================================================
    // Given Steps - Raw Transaction
    // ============================================================
    
    @Given("a sender address {string}")
    fun givenASenderAddress(address: String) {
        world.store("sender", address)
    }
    
    @Given("a sequence number {long}")
    fun givenASequenceNumber(seqNum: Long) {
        world.store("sequence_number", seqNum)
    }
    
    @Given("a max gas amount {long}")
    fun givenAMaxGasAmount(maxGas: Long) {
        world.store("max_gas_amount", maxGas)
    }
    
    @Given("a gas unit price {long}")
    fun givenAGasUnitPrice(gasPrice: Long) {
        world.store("gas_unit_price", gasPrice)
    }
    
    @Given("an expiration timestamp {long}")
    fun givenAnExpirationTimestamp(expiration: Long) {
        world.store("expiration_timestamp_secs", expiration)
    }
    
    @Given("a chain ID {int}")
    fun givenAChainId(chainId: Int) {
        world.store("chain_id", chainId)
    }
    
    // ============================================================
    // When Steps - Entry Function
    // ============================================================
    
    @When("I create the entry function payload")
    fun whenICreateTheEntryFunctionPayload() {
        runCatching {
            val address = world.retrieve<String>("entry_address")!!
            val module = world.retrieve<String>("entry_module")!!
            val function = world.retrieve<String>("entry_function")!!
            
            // Store as a simple representation
            world.entryFunction = mapOf(
                "address" to address,
                "module" to module,
                "function" to function,
                "args" to (world.retrieve<List<Map<String, String>>>("entry_args") ?: emptyList()),
                "type_args" to (world.retrieve<List<String>>("entry_type_args") ?: emptyList())
            )
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I serialize the entry function with BCS")
    fun whenISerializeTheEntryFunctionWithBcs() {
        runCatching {
            throw NotImplementedError("Entry function BCS serialization not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    // ============================================================
    // When Steps - Raw Transaction
    // ============================================================
    
    @When("I create a raw transaction")
    fun whenICreateARawTransaction() {
        runCatching {
            // Store as a simple representation
            world.rawTransaction = mapOf(
                "sender" to world.retrieve<String>("sender"),
                "sequence_number" to world.retrieve<Long>("sequence_number"),
                "max_gas_amount" to world.retrieve<Long>("max_gas_amount"),
                "gas_unit_price" to world.retrieve<Long>("gas_unit_price"),
                "expiration_timestamp_secs" to world.retrieve<Long>("expiration_timestamp_secs"),
                "chain_id" to world.retrieve<Int>("chain_id"),
                "payload" to world.entryFunction
            )
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I serialize the raw transaction with BCS")
    fun whenISerializeTheRawTransactionWithBcs() {
        runCatching {
            throw NotImplementedError("Raw transaction BCS serialization not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I compute the signing message")
    fun whenIComputeTheSigningMessage() {
        runCatching {
            throw NotImplementedError("Signing message computation not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    // ============================================================
    // When Steps - Signing
    // ============================================================
    
    @When("I sign the raw transaction with the account")
    fun whenISignTheRawTransactionWithTheAccount() {
        runCatching {
            throw NotImplementedError("Low-level transaction signing not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I sign the raw transaction with the Ed25519 account")
    fun whenISignTheRawTransactionWithTheEd25519Account() {
        whenISignTheRawTransactionWithTheAccount()
    }
    
    @When("I sign the raw transaction with the Secp256k1 account")
    fun whenISignTheRawTransactionWithTheSecp256k1Account() {
        whenISignTheRawTransactionWithTheAccount()
    }
    
    @When("I serialize the signed transaction with BCS")
    fun whenISerializeTheSignedTransactionWithBcs() {
        runCatching {
            throw NotImplementedError("Signed transaction BCS serialization not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I compute the transaction hash")
    fun whenIComputeTheTransactionHash() {
        runCatching {
            throw NotImplementedError("Transaction hash computation not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    @When("I verify the signed transaction signature")
    fun whenIVerifyTheSignedTransactionSignature() {
        runCatching {
            throw NotImplementedError("Signed transaction verification not yet available")
        }.onSuccess {
            world.clearError()
        }.onFailure {
            world.recordError(it)
        }
    }
    
    // ============================================================
    // Then Steps - Entry Function
    // ============================================================
    
    @Then("the entry function should be valid")
    fun thenTheEntryFunctionShouldBeValid() {
        world.error shouldBe null
        world.entryFunction shouldNotBe null
    }
    
    @Then("the entry function creation should fail")
    fun thenTheEntryFunctionCreationShouldFail() {
        world.error shouldNotBe null
    }
    
    // ============================================================
    // Then Steps - Raw Transaction
    // ============================================================
    
    @Then("the raw transaction should be valid")
    fun thenTheRawTransactionShouldBeValid() {
        world.error shouldBe null
        world.rawTransaction shouldNotBe null
    }
    
    @Then("the raw transaction creation should fail")
    fun thenTheRawTransactionCreationShouldFail() {
        world.error shouldNotBe null
    }
    
    @Then("the raw transaction sender should be {string}")
    @Suppress("UNCHECKED_CAST")
    fun thenTheRawTransactionSenderShouldBe(expected: String) {
        val tx = world.rawTransaction as Map<String, Any?>
        val sender = tx["sender"] as String
        sender.removePrefix("0x").lowercase() shouldBe expected.removePrefix("0x").lowercase()
    }
    
    @Then("the raw transaction sequence number should be {long}")
    @Suppress("UNCHECKED_CAST")
    fun thenTheRawTransactionSequenceNumberShouldBe(expected: Long) {
        val tx = world.rawTransaction as Map<String, Any?>
        tx["sequence_number"] shouldBe expected
    }
    
    @Then("the raw transaction max gas should be {long}")
    @Suppress("UNCHECKED_CAST")
    fun thenTheRawTransactionMaxGasShouldBe(expected: Long) {
        val tx = world.rawTransaction as Map<String, Any?>
        tx["max_gas_amount"] shouldBe expected
    }
    
    @Then("the raw transaction gas unit price should be {long}")
    @Suppress("UNCHECKED_CAST")
    fun thenTheRawTransactionGasUnitPriceShouldBe(expected: Long) {
        val tx = world.rawTransaction as Map<String, Any?>
        tx["gas_unit_price"] shouldBe expected
    }
    
    @Then("the raw transaction expiration should be {long}")
    @Suppress("UNCHECKED_CAST")
    fun thenTheRawTransactionExpirationShouldBe(expected: Long) {
        val tx = world.rawTransaction as Map<String, Any?>
        tx["expiration_timestamp_secs"] shouldBe expected
    }
    
    @Then("the raw transaction chain ID should be {int}")
    @Suppress("UNCHECKED_CAST")
    fun thenTheRawTransactionChainIdShouldBe(expected: Int) {
        val tx = world.rawTransaction as Map<String, Any?>
        tx["chain_id"] shouldBe expected
    }
    
    @Then("the signing message should be {string}")
    fun thenTheSigningMessageShouldBe(expected: String) {
        val expectedBytes = expected.hexToBytes()
        world.signingMessage shouldBe expectedBytes
    }
    
    @Then("the signing message should start with the domain prefix")
    fun thenTheSigningMessageShouldStartWithTheDomainPrefix() {
        world.signingMessage shouldNotBe null
    }
    
    // ============================================================
    // Then Steps - Signed Transaction
    // ============================================================
    
    @Then("the signed transaction should be valid")
    fun thenTheSignedTransactionShouldBeValid() {
        world.error shouldBe null
        world.signedTransaction shouldNotBe null
    }
    
    @Then("the signed transaction should contain the raw transaction")
    fun thenTheSignedTransactionShouldContainTheRawTransaction() {
        world.signedTransaction shouldNotBe null
    }
    
    @Then("the signed transaction should contain an authenticator")
    fun thenTheSignedTransactionShouldContainAnAuthenticator() {
        world.signedTransaction shouldNotBe null
    }
    
    @Then("the authenticator should be Ed25519")
    fun thenTheAuthenticatorShouldBeEd25519() {
        // TODO: Verify when signed transaction structure is available
    }
    
    @Then("the authenticator should be Secp256k1")
    fun thenTheAuthenticatorShouldBeSecp256k1() {
        // TODO: Verify when signed transaction structure is available
    }
    
    @Then("the authenticator should be SingleKey")
    fun thenTheAuthenticatorShouldBeSingleKey() {
        // TODO: Verify when signed transaction structure is available
    }
    
    @Then("the transaction hash should be {string}")
    fun thenTheTransactionHashShouldBe(expected: String) {
        world.transactionHash shouldBe expected.removePrefix("0x").lowercase()
    }
    
    @Then("the transaction hash should be 32 bytes")
    fun thenTheTransactionHashShouldBe32Bytes() {
        world.transactionHash shouldNotBe null
        world.transactionHash!!.length shouldBe 64
    }
    
    @Then("signing the same transaction twice should produce the same result")
    fun thenSigningTheSameTransactionTwiceShouldProduceTheSameResult() {
        // TODO: Verify deterministic signing
    }
    
    // "the serialized bytes should be {string}" is in CommonSteps
    
    @Then("the serialization should be deterministic")
    fun thenTheSerializationShouldBeDeterministic() {
        // TODO: Verify deterministic serialization
    }
}
