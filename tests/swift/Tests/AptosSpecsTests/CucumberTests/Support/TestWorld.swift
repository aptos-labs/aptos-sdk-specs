import Aptos
import BCS
import Core
import Transactions
import Foundation

/// Shared test context for Cucumber scenarios.
/// Holds state between steps within a scenario.
final class TestWorld {
    
    // MARK: - Singleton
    
    static let shared = TestWorld()
    
    private init() {}
    
    // MARK: - Core Types
    
    var hexString: String?
    var address: AccountAddress?
    var address2: AccountAddress?
    var bytes: [UInt8]?
    var serializedBytes: [UInt8]?
    var typeTagString: String?
    var typeTag: TypeTag?
    
    // MARK: - Cryptography
    
    var ed25519PrivateKey: Ed25519PrivateKey?
    var ed25519PublicKey: Ed25519PublicKey?
    var ed25519Signature: Ed25519Signature?
    var secp256k1PrivateKey: Secp256k1PrivateKey?
    var secp256k1PublicKey: Secp256k1PublicKey?
    var secp256k1Signature: Secp256k1Signature?
    var message: [UInt8]?
    var hashResult: [UInt8]?
    
    // MARK: - Accounts
    
    var ed25519Account: Account.Ed25519Account?
    var singleKeyAccount: Account.SingleKeyAccount?
    var account: (any AccountProtocol)?
    var authKey: AuthenticationKey?
    var mnemonic: String?
    var derivationPath: String?
    
    // MARK: - Transactions
    
    var rawTransaction: RawTransaction?
    var signedTransaction: SignedTransaction?
    var entryFunction: EntryFunction?
    
    // MARK: - API Client
    
    var client: Aptos?
    var network: AptosConfig.Network?
    
    // MARK: - Results
    
    var result: Any?
    var error: Error?
    var errorMessage: String?
    var boolResult: Bool?
    var stringResult: String?
    
    // MARK: - Test Vectors
    
    var testVectors: [String: Any]?
    
    // MARK: - Reset
    
    func reset() {
        hexString = nil
        address = nil
        address2 = nil
        bytes = nil
        serializedBytes = nil
        typeTagString = nil
        typeTag = nil
        ed25519PrivateKey = nil
        ed25519PublicKey = nil
        ed25519Signature = nil
        secp256k1PrivateKey = nil
        secp256k1PublicKey = nil
        secp256k1Signature = nil
        message = nil
        hashResult = nil
        ed25519Account = nil
        singleKeyAccount = nil
        account = nil
        authKey = nil
        mnemonic = nil
        derivationPath = nil
        rawTransaction = nil
        signedTransaction = nil
        entryFunction = nil
        client = nil
        network = nil
        result = nil
        error = nil
        errorMessage = nil
        boolResult = nil
        stringResult = nil
        testVectors = nil
    }
    
    func setError(_ error: Error) {
        self.error = error
        self.errorMessage = error.localizedDescription
    }
    
    func clearError() {
        error = nil
        errorMessage = nil
    }
}
