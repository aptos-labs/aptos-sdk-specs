package com.aptos.specs.support

import com.google.gson.Gson
import com.google.gson.JsonObject
import java.io.File

/**
 * Utility for loading test vectors from JSON files.
 *
 * Test vectors are located in ../../test-vectors/ relative to this test directory.
 */
object Vectors {
    private val gson = Gson()
    private val vectorsDir = File("../../test-vectors")

    /**
     * Load a JSON file and parse it as JsonObject.
     */
    fun loadJson(filename: String): JsonObject {
        val file = File(vectorsDir, filename)
        return gson.fromJson(file.readText(), JsonObject::class.java)
    }

    /**
     * Load address test vectors.
     */
    fun loadAddressVectors(): AddressVectors {
        val json = loadJson("addresses.json")
        return gson.fromJson(json, AddressVectors::class.java)
    }

    /**
     * Load BCS serialization test vectors.
     */
    fun loadBcsVectors(): BcsVectors {
        val json = loadJson("bcs.json")
        return gson.fromJson(json, BcsVectors::class.java)
    }

    /**
     * Load signature test vectors.
     */
    fun loadSignatureVectors(): SignatureVectors {
        val json = loadJson("signatures.json")
        return gson.fromJson(json, SignatureVectors::class.java)
    }

    /**
     * Load mnemonic test vectors.
     */
    fun loadMnemonicVectors(): MnemonicVectors {
        val json = loadJson("mnemonics.json")
        return gson.fromJson(json, MnemonicVectors::class.java)
    }

    /**
     * Load transaction test vectors.
     */
    fun loadTransactionVectors(): TransactionVectors {
        val json = loadJson("transactions.json")
        return gson.fromJson(json, TransactionVectors::class.java)
    }

    /**
     * Load type tag test vectors.
     */
    fun loadTypeTagVectors(): TypeTagVectors {
        val json = loadJson("type-tags.json")
        return gson.fromJson(json, TypeTagVectors::class.java)
    }

    /**
     * Load multi-sig test vectors.
     */
    fun loadMultiSigVectors(): MultiSigVectors {
        val json = loadJson("multi-sig.json")
        return gson.fromJson(json, MultiSigVectors::class.java)
    }

    // ============================================================
    // Vector Data Classes
    // ============================================================

    data class AddressVectors(
        val version: String,
        val description: String,
        val address_parsing: List<AddressParsingVector>? = null,
        val address_formatting: List<AddressFormattingVector>? = null,
        val special_addresses: List<SpecialAddressVector>? = null,
    )

    data class AddressParsingVector(
        val name: String,
        val description: String? = null,
        val input: String,
        val expected: AddressExpected? = null,
        val error: Boolean = false,
    )

    data class AddressFormattingVector(
        val name: String,
        val description: String? = null,
        val input: String,
        val expected: AddressExpected,
    )

    data class SpecialAddressVector(
        val name: String,
        val description: String? = null,
        val expected: AddressExpected,
    )

    data class AddressExpected(
        val full: String? = null,
        val short: String? = null,
        val bytes: String? = null,
    )

    data class BcsVectors(
        val version: String,
        val description: String,
        val primitives: List<BcsPrimitiveVector>? = null,
        val sequences: List<BcsSequenceVector>? = null,
        val structs: List<BcsStructVector>? = null,
    )

    data class BcsPrimitiveVector(
        val name: String,
        val description: String? = null,
        val type: String,
        val value: Any,
        val expected_bytes: String,
    )

    data class BcsSequenceVector(
        val name: String,
        val description: String? = null,
        val type: String,
        val value: Any,
        val expected_bytes: String,
    )

    data class BcsStructVector(
        val name: String,
        val description: String? = null,
        val struct_type: String,
        val fields: Map<String, Any>,
        val expected_bytes: String,
    )

    data class SignatureVectors(
        val version: String,
        val description: String,
        val ed25519: List<Ed25519Vector>? = null,
        val secp256k1: List<Secp256k1Vector>? = null,
    )

    data class Ed25519Vector(
        val name: String,
        val description: String? = null,
        val private_key: String? = null,
        val public_key: String? = null,
        val message: String? = null,
        val signature: String? = null,
        val auth_key: String? = null,
        val address: String? = null,
    )

    data class Secp256k1Vector(
        val name: String,
        val description: String? = null,
        val private_key: String? = null,
        val public_key: String? = null,
        val message: String? = null,
        val signature: String? = null,
        val auth_key: String? = null,
        val address: String? = null,
    )

    data class MnemonicVectors(
        val version: String,
        val description: String,
        val derivation: List<MnemonicDerivationVector>? = null,
    )

    data class MnemonicDerivationVector(
        val name: String,
        val description: String? = null,
        val mnemonic: String,
        val passphrase: String? = null,
        val path: String? = null,
        val expected: MnemonicExpected,
    )

    data class MnemonicExpected(
        val private_key: String? = null,
        val public_key: String? = null,
        val address: String? = null,
    )

    data class TransactionVectors(
        val version: String,
        val description: String,
        val raw_transactions: List<RawTransactionVector>? = null,
        val signed_transactions: List<SignedTransactionVector>? = null,
    )

    data class RawTransactionVector(
        val name: String,
        val description: String? = null,
        val sender: String,
        val sequence_number: Long,
        val payload: Map<String, Any>,
        val max_gas_amount: Long,
        val gas_unit_price: Long,
        val expiration_timestamp_secs: Long,
        val chain_id: Int,
        val expected: TransactionExpected,
    )

    data class SignedTransactionVector(
        val name: String,
        val description: String? = null,
        val raw_transaction: RawTransactionVector,
        val private_key: String,
        val expected: SignedTransactionExpected,
    )

    data class TransactionExpected(
        val bcs_bytes: String? = null,
        val signing_message: String? = null,
    )

    data class SignedTransactionExpected(
        val bcs_bytes: String? = null,
        val transaction_hash: String? = null,
    )

    data class TypeTagVectors(
        val version: String,
        val description: String,
        val parsing: List<TypeTagParsingVector>? = null,
        val formatting: List<TypeTagFormattingVector>? = null,
    )

    data class TypeTagParsingVector(
        val name: String,
        val description: String? = null,
        val input: String,
        val expected: TypeTagExpected? = null,
        val error: Boolean = false,
    )

    data class TypeTagFormattingVector(
        val name: String,
        val description: String? = null,
        val type_tag: Map<String, Any>,
        val expected: String,
    )

    data class TypeTagExpected(
        val kind: String? = null,
        val formatted: String? = null,
    )

    data class MultiSigVectors(
        val version: String,
        val description: String,
        val accounts: List<MultiSigAccountVector>? = null,
        val signatures: List<MultiSigSignatureVector>? = null,
    )

    data class MultiSigAccountVector(
        val name: String,
        val description: String? = null,
        val public_keys: List<String>,
        val threshold: Int,
        val expected: MultiSigExpected,
    )

    data class MultiSigExpected(
        val auth_key: String? = null,
        val address: String? = null,
    )

    data class MultiSigSignatureVector(
        val name: String,
        val description: String? = null,
        val public_keys: List<String>,
        val threshold: Int,
        val signers: List<Int>,
        val message: String,
        val expected: MultiSigSignatureExpected,
    )

    data class MultiSigSignatureExpected(
        val bitmap: String? = null,
        val signature_bytes: String? = null,
    )
}

// ============================================================
// Hex Utilities
// ============================================================

/**
 * Convert hex string to ByteArray.
 */
fun String.hexToBytes(): ByteArray {
    val hex = this.removePrefix("0x")
    require(hex.length % 2 == 0) { "Hex string must have even length" }
    return ByteArray(hex.length / 2) { i ->
        hex.substring(i * 2, i * 2 + 2).toInt(16).toByte()
    }
}

/**
 * Convert ByteArray to hex string.
 */
fun ByteArray.toHex(): String {
    return this.joinToString("") { "%02x".format(it) }
}

/**
 * Convert ByteArray to hex string with 0x prefix.
 */
fun ByteArray.toHexWithPrefix(): String {
    return "0x${this.toHex()}"
}
