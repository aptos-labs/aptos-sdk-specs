package com.aptos.specs.support

/**
 * Test context for sharing state between step definitions within a scenario.
 *
 * Each scenario gets a fresh instance of World via Cucumber's dependency injection
 * (PicoContainer), ensuring test isolation.
 */
class World {
    // ============================================================
    // Input Data
    // ============================================================

    /** Raw hex string input for parsing */
    var hexString: String? = null

    /** Raw byte array input */
    var bytes: ByteArray? = null

    /** Generic string input */
    var inputString: String? = null

    /** Mnemonic phrase */
    var mnemonic: String? = null

    /** Derivation path for HD wallets */
    var derivationPath: String? = null

    // ============================================================
    // Addresses
    // ============================================================

    /** Parsed AccountAddress */
    var address: Any? = null // Replace with actual AccountAddress type

    /** Second address for comparison */
    var address2: Any? = null

    // ============================================================
    // Cryptographic Keys
    // ============================================================

    /** Ed25519 private key */
    var privateKey: Any? = null // Replace with actual type

    /** Ed25519 public key */
    var publicKey: Any? = null // Replace with actual type

    /** Key pair (private + public) */
    var keyPair: Any? = null // Replace with actual type

    /** Second key pair for comparison */
    var keyPair2: Any? = null

    /** Signature result */
    var signature: Any? = null // Replace with actual type

    /** Authentication key */
    var authKey: Any? = null // Replace with actual type

    // ============================================================
    // Accounts
    // ============================================================

    /** Primary account under test */
    var account: Any? = null // Replace with actual Account type

    /** Secondary account for multi-signer scenarios */
    var account2: Any? = null

    /** Fee payer account */
    var feePayerAccount: Any? = null

    // ============================================================
    // Transactions
    // ============================================================

    /** Raw transaction (unsigned) */
    var rawTransaction: Any? = null // Replace with actual type

    /** Signed transaction */
    var signedTransaction: Any? = null // Replace with actual type

    /** Entry function payload */
    var entryFunction: Any? = null // Replace with actual type

    /** Transaction hash */
    var transactionHash: String? = null

    /** Signing message bytes */
    var signingMessage: ByteArray? = null

    // ============================================================
    // Type Tags
    // ============================================================

    /** Parsed TypeTag */
    var typeTag: Any? = null // Replace with actual type

    /** Module ID */
    var moduleId: Any? = null // Replace with actual type

    // ============================================================
    // Serialization
    // ============================================================

    /** BCS serialized bytes */
    var serializedBytes: ByteArray? = null

    /** Deserialized value */
    var deserializedValue: Any? = null

    // ============================================================
    // Hashing
    // ============================================================

    /** Hash result */
    var hashResult: ByteArray? = null

    /** Hash value object */
    var hashValue: Any? = null // Replace with actual HashValue type

    // ============================================================
    // API Client
    // ============================================================

    /** API client instance */
    var client: Any? = null // Replace with actual AptosClient type

    /** API response */
    var response: Any? = null

    /** Ledger info */
    var ledgerInfo: Any? = null

    // ============================================================
    // Error Handling
    // ============================================================

    /** Last error/exception encountered */
    var error: Throwable? = null

    /** Error message for assertions */
    val errorMessage: String?
        get() = error?.message

    /**
     * Record an error that occurred during a step.
     */
    fun recordError(e: Throwable) {
        error = e
    }

    /**
     * Clear any recorded error.
     */
    fun clearError() {
        error = null
    }

    /**
     * Check if an error has been recorded.
     */
    fun hasError(): Boolean = error != null

    // ============================================================
    // Generic Storage
    // ============================================================

    /** Generic storage for arbitrary values */
    private val storage = mutableMapOf<String, Any?>()

    /**
     * Store a value by key.
     */
    fun store(
        key: String,
        value: Any?,
    ) {
        storage[key] = value
    }

    /**
     * Retrieve a value by key.
     */
    @Suppress("UNCHECKED_CAST")
    fun <T> retrieve(key: String): T? = storage[key] as? T

    // ============================================================
    // Lifecycle
    // ============================================================

    /**
     * Reset all state. Called between scenarios if needed.
     */
    fun reset() {
        hexString = null
        bytes = null
        inputString = null
        mnemonic = null
        derivationPath = null
        address = null
        address2 = null
        privateKey = null
        publicKey = null
        keyPair = null
        keyPair2 = null
        signature = null
        authKey = null
        account = null
        account2 = null
        feePayerAccount = null
        rawTransaction = null
        signedTransaction = null
        entryFunction = null
        transactionHash = null
        signingMessage = null
        typeTag = null
        moduleId = null
        serializedBytes = null
        deserializedValue = null
        hashResult = null
        hashValue = null
        client = null
        response = null
        ledgerInfo = null
        error = null
        storage.clear()
    }
}
