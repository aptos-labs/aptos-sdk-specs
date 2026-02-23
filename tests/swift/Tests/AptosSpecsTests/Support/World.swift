import AptosSDK
import Foundation

/// Shared test context for XCTest scenarios.
/// Holds state between test methods.
final class World {

  // MARK: - Singleton

  static let shared = World()

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
  var message: [UInt8]?
  var hashResult: [UInt8]?

  // MARK: - Accounts

  var ed25519Account: Ed25519Account?
  var singleKeyAccount: SingleKeyAccount?
  var account: (any AptosAccount)?
  var authKey: AuthenticationKey?
  var mnemonic: String?
  var derivationPath: String?

  // MARK: - API Client

  var client: AptosClient?

  // MARK: - Results

  var result: Any?
  var error: Error?
  var errorMessage: String?
  var boolResult: Bool?
  var stringResult: String?

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
    message = nil
    hashResult = nil
    ed25519Account = nil
    singleKeyAccount = nil
    account = nil
    authKey = nil
    mnemonic = nil
    derivationPath = nil
    client = nil
    result = nil
    error = nil
    errorMessage = nil
    boolResult = nil
    stringResult = nil
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
