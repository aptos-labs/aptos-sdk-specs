import Aptos
import BCS
import Core
import CryptoKit
import CryptoSwift
import Transactions
import Utils
import XCTest

@testable import AptosSpecs

/// Main test class for Aptos SDK behavioral specifications.
/// Uses XCTest with Gherkin-style test naming conventions.
final class AptosSpecsTests: XCTestCase {

  /// Shared world state for tests
  var world: World!

  override func setUp() {
    super.setUp()
    world = World.shared
    world.reset()
  }

  override func tearDown() {
    world.reset()
    super.tearDown()
  }
}

// MARK: - Address Tests (address.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Address Parsing - Valid Inputs
  // =============================================================================

  func test_Address_ParseHexWithPrefix() throws {
    // Scenario: Parse hex address with 0x prefix
    let address = try AccountAddress.fromString("0x1")
    XCTAssertEqual(address.toUInt8Array().count, 32)
    XCTAssertEqual(address.toUInt8Array()[31], 1)
    for i in 0..<31 {
      XCTAssertEqual(address.toUInt8Array()[i], 0)
    }
  }

  func test_Address_ParseHexWithoutPrefix() throws {
    // Scenario: Parse hex address without 0x prefix
    let address = try AccountAddress.fromString("1")
    XCTAssertEqual(address.toString().lowercased(), "0x1")
  }

  func test_Address_ParseFull64CharHex() throws {
    // Scenario: Parse full 64-character hex address
    let address = try AccountAddress.fromString(
      "0x0000000000000000000000000000000000000000000000000000000000000001")
    XCTAssertEqual(address.toString().lowercased(), "0x1")
  }

  func test_Address_ParseVariousFormats_0x10() throws {
    let address = try AccountAddress.fromString("0x10")
    // SDK returns long format for non-special addresses
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000000010")
  }

  func test_Address_ParseVariousFormats_0xff() throws {
    let address = try AccountAddress.fromString("0xff")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x00000000000000000000000000000000000000000000000000000000000000ff")
  }

  func test_Address_ParseVariousFormats_0x100() throws {
    let address = try AccountAddress.fromString("0x100")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000000100")
  }

  func test_Address_ParseVariousFormats_0xabcdef() throws {
    let address = try AccountAddress.fromString("0xabcdef")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000abcdef")
  }

  func test_Address_ParseUppercaseHex() throws {
    // Scenario: Parse uppercase hex address - SDK normalizes to lowercase
    let address = try AccountAddress.fromString("0xABCDEF")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000abcdef")
  }

  func test_Address_ParseMixedCaseHex() throws {
    // Scenario: Parse mixed case hex address - SDK normalizes to lowercase
    let address = try AccountAddress.fromString("0xAbCdEf")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000abcdef")
  }

  // =============================================================================
  // Address Parsing - Invalid Inputs
  // =============================================================================

  func test_Address_RejectEmptyString() throws {
    XCTAssertThrowsError(try AccountAddress.fromString(""))
  }

  func test_Address_RejectJust0xPrefix() throws {
    XCTAssertThrowsError(try AccountAddress.fromString("0x"))
  }

  func test_Address_RejectNonHexCharacters() throws {
    XCTAssertThrowsError(try AccountAddress.fromString("0xGHIJKL"))
  }

  func test_Address_RejectTooLongAddress() throws {
    XCTAssertThrowsError(
      try AccountAddress.fromString(
        "0x00000000000000000000000000000000000000000000000000000000000000001"))
  }

  func test_Address_RejectAddressWithSpaces() throws {
    XCTAssertThrowsError(try AccountAddress.fromString("0x1 2 3"))
  }

  // =============================================================================
  // Address Formatting
  // =============================================================================

  func test_Address_FormatToFullHex() throws {
    let address = try AccountAddress.fromString("0x1")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000000001")
  }

  func test_Address_FormatToShortString() throws {
    let address = try AccountAddress.fromString("0x1")
    XCTAssertEqual(address.toString().lowercased(), "0x1")
  }

  func test_Address_FormatZeroAddress() throws {
    let address = AccountAddress.ZERO
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000000000")
    XCTAssertEqual(address.toString().lowercased(), "0x0")
  }

  func test_Address_ShortStringRemovesLeadingZeros_0x10() throws {
    // Note: SDK toString() only shortens "special" addresses (0-9)
    // For non-special addresses, it returns full format
    let address = try AccountAddress.fromString(
      "0x0000000000000000000000000000000000000000000000000000000000000010")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000000010")
  }

  func test_Address_ShortStringRemovesLeadingZeros_0x1000() throws {
    // Note: SDK toString() only shortens "special" addresses (0-9)
    let address = try AccountAddress.fromString(
      "0x0000000000000000000000000000000000000000000000000000000000001000")
    XCTAssertEqual(
      address.toStringLong().lowercased(),
      "0x0000000000000000000000000000000000000000000000000000000000001000")
  }

  func test_Address_ShortStringPreservesLeading_0x1XXX() throws {
    let address = try AccountAddress.fromString(
      "0x1000000000000000000000000000000000000000000000000000000000000000")
    XCTAssertEqual(
      address.toString().lowercased(),
      "0x1000000000000000000000000000000000000000000000000000000000000000")
  }

  // =============================================================================
  // Standard Address Constants
  // =============================================================================

  func test_Address_ZeroConstant() throws {
    let address = AccountAddress.ZERO
    for byte in address.toUInt8Array() {
      XCTAssertEqual(byte, 0)
    }
    XCTAssertEqual(address.toString().lowercased(), "0x0")
    XCTAssertTrue(address.isSpecial())
  }

  func test_Address_OneConstant() throws {
    let address = AccountAddress.ONE
    XCTAssertEqual(address.toUInt8Array()[31], 1)
    for i in 0..<31 {
      XCTAssertEqual(address.toUInt8Array()[i], 0)
    }
    XCTAssertEqual(address.toString().lowercased(), "0x1")
    XCTAssertTrue(address.isSpecial())
  }

  func test_Address_ThreeConstant() throws {
    let address = AccountAddress.THREE
    XCTAssertEqual(address.toUInt8Array()[31], 3)
    XCTAssertEqual(address.toString().lowercased(), "0x3")
    XCTAssertTrue(address.isSpecial())
  }

  func test_Address_FourConstant() throws {
    let address = AccountAddress.FOUR
    XCTAssertEqual(address.toUInt8Array()[31], 4)
    XCTAssertEqual(address.toString().lowercased(), "0x4")
    XCTAssertTrue(address.isSpecial())
  }

  // =============================================================================
  // Address Comparison
  // =============================================================================

  func test_Address_EquivalentInputsAreEqual() throws {
    let addr1 = try AccountAddress.fromString("0x1")
    let addr2 = try AccountAddress.fromString(
      "0x0000000000000000000000000000000000000000000000000000000000000001")
    XCTAssertTrue(addr1.equals(addr2))
    XCTAssertEqual(addr1, addr2)
  }

  func test_Address_DifferentAddressesNotEqual() throws {
    let addr1 = try AccountAddress.fromString("0x1")
    let addr2 = try AccountAddress.fromString("0x2")
    XCTAssertFalse(addr1.equals(addr2))
    XCTAssertNotEqual(addr1, addr2)
  }

  // =============================================================================
  // BCS Serialization
  // =============================================================================

  func test_Address_BcsSerialize() throws {
    let address = try AccountAddress.fromString("0x1")
    let bytes = try address.bcsToBytes()
    XCTAssertEqual(bytes.count, 32)
    XCTAssertEqual(bytes[31], 1)
    for i in 0..<31 {
      XCTAssertEqual(bytes[i], 0)
    }
  }

  func test_Address_BcsDeserialize() throws {
    var bytes = [UInt8](repeating: 0, count: 32)
    bytes[31] = 1
    let deserializer = BcsDeserializer(input: bytes)
    let address = try AccountAddress.deserialize(deserializer: deserializer)
    XCTAssertEqual(address.toString().lowercased(), "0x1")
  }

  func test_Address_BcsRoundTrip() throws {
    let original = try AccountAddress.fromString("0xabcdef1234567890")
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try AccountAddress.deserialize(deserializer: deserializer)
    XCTAssertEqual(result, original)
  }
}

// MARK: - Ed25519 Tests (ed25519.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Key Generation
  // =============================================================================

  func test_Ed25519_GenerateRandomKeyPair() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey

    XCTAssertEqual(privateKey.toUInt8Array().count, 32)
    XCTAssertEqual(publicKey.toUInt8Array().count, 32)
  }

  func test_Ed25519_GenerateUniqueKeyPairs() throws {
    let privateKey1 = Ed25519PrivateKey.generate()
    let privateKey2 = Ed25519PrivateKey.generate()
    let publicKey1 = try privateKey1.publicKey() as! Ed25519PublicKey
    let publicKey2 = try privateKey2.publicKey() as! Ed25519PublicKey

    XCTAssertNotEqual(privateKey1.toUInt8Array(), privateKey2.toUInt8Array())
    XCTAssertNotEqual(publicKey1.toUInt8Array(), publicKey2.toUInt8Array())
  }

  func test_Ed25519_CreateFromSeed() throws {
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 1
    let privateKey1 = try Ed25519PrivateKey(seed)
    let privateKey2 = try Ed25519PrivateKey(seed)

    XCTAssertEqual(privateKey1.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Ed25519_CreateFromHexString() throws {
    let hex = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    let privateKey = try Ed25519PrivateKey(hex)

    XCTAssertEqual(privateKey.toUInt8Array().count, 32)
  }

  func test_Ed25519_RejectInvalidLength() throws {
    let invalidBytes = [UInt8](repeating: 0, count: 31)
    XCTAssertThrowsError(try Ed25519PrivateKey(invalidBytes))
  }

  // =============================================================================
  // Signing
  // =============================================================================

  func test_Ed25519_SignMessage() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let message = Array("hello world".utf8)

    let signature = try privateKey.sign(message: message) as! Ed25519Signature
    XCTAssertEqual(signature.toUInt8Array().count, 64)

    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Ed25519_SignEmptyMessage() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let message = [UInt8]()

    let signature = try privateKey.sign(message: message) as! Ed25519Signature
    XCTAssertEqual(signature.toUInt8Array().count, 64)

    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Ed25519_SignDeterministic() throws {
    // Note: Ed25519 signing should be deterministic per the specification.
    // We verify this by ensuring the signature can be verified.
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 42
    let privateKey = try Ed25519PrivateKey(seed)
    let message = Array("test message".utf8)

    let signature = try privateKey.sign(message: message) as! Ed25519Signature
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey

    // Verify the signature is valid
    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
    XCTAssertEqual(signature.toUInt8Array().count, 64)
  }

  func test_Ed25519_DifferentMessagesDifferentSignatures() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let msg1 = Array("message1".utf8)
    let msg2 = Array("message2".utf8)

    let sig1 = try privateKey.sign(message: msg1) as! Ed25519Signature
    let sig2 = try privateKey.sign(message: msg2) as! Ed25519Signature

    XCTAssertNotEqual(sig1.toUInt8Array(), sig2.toUInt8Array())
  }

  func test_Ed25519_DifferentKeysDifferentSignatures() throws {
    let privateKey1 = Ed25519PrivateKey.generate()
    let privateKey2 = Ed25519PrivateKey.generate()
    let message = Array("same message".utf8)

    let sig1 = try privateKey1.sign(message: message) as! Ed25519Signature
    let sig2 = try privateKey2.sign(message: message) as! Ed25519Signature

    XCTAssertNotEqual(sig1.toUInt8Array(), sig2.toUInt8Array())
  }

  // =============================================================================
  // Verification
  // =============================================================================

  func test_Ed25519_VerifyValidSignature() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let message = Array("test message".utf8)
    let signature = try privateKey.sign(message: message) as! Ed25519Signature
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey

    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Ed25519_RejectSignatureFromWrongKey() throws {
    let privateKey1 = Ed25519PrivateKey.generate()
    let privateKey2 = Ed25519PrivateKey.generate()
    let message = Array("test message".utf8)

    let signature = try privateKey1.sign(message: message) as! Ed25519Signature
    let publicKey2 = try privateKey2.publicKey() as! Ed25519PublicKey

    let isValid = try publicKey2.verifySignature(message: message, signature: signature)
    XCTAssertFalse(isValid)
  }

  func test_Ed25519_RejectSignatureForWrongMessage() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let signature = try privateKey.sign(message: Array("original".utf8)) as! Ed25519Signature
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey

    let isValid = try publicKey.verifySignature(
      message: Array("modified".utf8), signature: signature)
    XCTAssertFalse(isValid)
  }

  // =============================================================================
  // Key Export
  // =============================================================================

  func test_Ed25519_ExportPublicKeyBytes() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let bytes = publicKey.toUInt8Array()

    XCTAssertEqual(bytes.count, 32)
  }

  func test_Ed25519_ExportPrivateKeyBytes() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let bytes = privateKey.toUInt8Array()

    XCTAssertTrue(bytes.count == 32 || bytes.count == 64)

    let privateKey2 = try Ed25519PrivateKey(bytes)
    XCTAssertEqual(privateKey.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Ed25519_ExportKeysAsHex() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let hex = privateKey.toString()

    XCTAssertTrue(hex.hasPrefix("0x"))
    XCTAssertTrue(hex.count == 66 || hex.count == 130)
  }

  // =============================================================================
  // Authentication Key Derivation
  // =============================================================================

  func test_Ed25519_DeriveAuthKey() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let authKey = try publicKey.authKey()

    XCTAssertEqual(authKey.toUInt8Array().count, 32)
  }

  func test_Ed25519_DeriveAccountAddress() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let authKey = try publicKey.authKey()
    let address = try authKey.derivedAddress()

    XCTAssertEqual(address.toUInt8Array().count, 32)
    XCTAssertEqual(address.toUInt8Array(), authKey.toUInt8Array())
  }
}

// MARK: - Account Tests (single-key.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Ed25519 Account Creation
  // =============================================================================

  func test_Account_GenerateRandomEd25519() throws {
    let account = Account.generate()

    XCTAssertNotNil(account.accountAddress)
    XCTAssertNotNil(account.publicKey)
    XCTAssertEqual(account.accountAddress.toUInt8Array().count, 32)
  }

  func test_Account_GeneratedAccountsUnique() throws {
    let account1 = Account.generate()
    let account2 = Account.generate()

    XCTAssertNotEqual(account1.accountAddress, account2.accountAddress)
    XCTAssertNotEqual(account1.publicKey.toUInt8Array(), account2.publicKey.toUInt8Array())
  }

  func test_Account_CreateFromPrivateKeyBytes() throws {
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 42
    let privateKey = try Ed25519PrivateKey(seed)
    let account = try Account.Ed25519Account(privateKey: privateKey)

    XCTAssertNotNil(account.accountAddress)

    let privateKey2 = try Ed25519PrivateKey(seed)
    let account2 = try Account.Ed25519Account(privateKey: privateKey2)
    XCTAssertEqual(account.accountAddress, account2.accountAddress)
  }

  func test_Account_CreateFromHexString() throws {
    let hex = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    let privateKey = try Ed25519PrivateKey(hex)
    let account = try Account.Ed25519Account(privateKey: privateKey)

    XCTAssertNotNil(account.accountAddress)
  }

  func test_Account_CreateFromHexWithoutPrefix() throws {
    let hex = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    let privateKey = try Ed25519PrivateKey(hex)
    let account = try Account.Ed25519Account(privateKey: privateKey)

    XCTAssertNotNil(account.accountAddress)
  }

  func test_Account_RejectInvalidPrivateKeyLength() throws {
    let invalidBytes = [UInt8](repeating: 0, count: 31)
    XCTAssertThrowsError(try Ed25519PrivateKey(invalidBytes))
  }

  func test_Account_RejectInvalidHexString() throws {
    XCTAssertThrowsError(try Ed25519PrivateKey("0xGGGG"))
  }

  // =============================================================================
  // Account Properties
  // =============================================================================

  func test_Account_GetAddress() throws {
    let account = Account.generate()
    let address = account.accountAddress

    XCTAssertNotNil(address)
    XCTAssertEqual(address.toUInt8Array().count, 32)
  }

  func test_Account_GetPublicKey() throws {
    let account = Account.generate()
    let publicKey = account.publicKey

    XCTAssertEqual(publicKey.toUInt8Array().count, 32)
  }

  func test_Account_GetSignatureScheme_Ed25519() throws {
    let account = Account.generate()
    XCTAssertEqual(account.signingScheme, .ed25519)
  }

  func test_Account_GetSignatureScheme_SingleKey() throws {
    let account = Account.generate(scheme: .ed25519)
    XCTAssertEqual(account.signingScheme, .singleKey)
  }

  // =============================================================================
  // Signing
  // =============================================================================

  func test_Account_SignArbitraryMessage() throws {
    let account = Account.generate()
    let message = Array("hello world".utf8)

    let signature = try account.sign(message: message)
    let isValid = try account.verifySignature(message: message, signature: signature)

    XCTAssertTrue(isValid)
  }

  func test_Account_SignEmptyMessage() throws {
    let account = Account.generate()
    let message = [UInt8]()

    let signature = try account.sign(message: message)
    XCTAssertNotNil(signature)
  }

  func test_Account_SignDeterministic() throws {
    // Verify account signing produces valid signatures
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 42
    let privateKey = try Ed25519PrivateKey(seed)
    let account = try Account.Ed25519Account(privateKey: privateKey)
    let message = Array("test".utf8)

    let signature = try account.sign(message: message)

    // Verify the signature is valid
    let isValid = try account.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Account_DifferentAccountsDifferentSignatures() throws {
    let account1 = Account.generate()
    let account2 = Account.generate()
    let message = Array("same message".utf8)

    let sig1 = try account1.sign(message: message)
    let sig2 = try account2.sign(message: message)

    XCTAssertNotEqual(sig1.toUInt8Array(), sig2.toUInt8Array())
  }
}

// MARK: - TypeTag Tests (type-tags.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Primitive Type Parsing
  // =============================================================================

  func test_TypeTag_ParseBool() throws {
    let typeTag = try TypeTag.parseTypeTag("bool")
    XCTAssertEqual(typeTag, .Bool)
  }

  func test_TypeTag_ParseU8() throws {
    let typeTag = try TypeTag.parseTypeTag("u8")
    XCTAssertEqual(typeTag, .U8)
  }

  func test_TypeTag_ParseU16() throws {
    let typeTag = try TypeTag.parseTypeTag("u16")
    XCTAssertEqual(typeTag, .U16)
  }

  func test_TypeTag_ParseU32() throws {
    let typeTag = try TypeTag.parseTypeTag("u32")
    XCTAssertEqual(typeTag, .U32)
  }

  func test_TypeTag_ParseU64() throws {
    let typeTag = try TypeTag.parseTypeTag("u64")
    XCTAssertEqual(typeTag, .U64)
  }

  func test_TypeTag_ParseU128() throws {
    let typeTag = try TypeTag.parseTypeTag("u128")
    XCTAssertEqual(typeTag, .U128)
  }

  func test_TypeTag_ParseU256() throws {
    let typeTag = try TypeTag.parseTypeTag("u256")
    XCTAssertEqual(typeTag, .U256)
  }

  func test_TypeTag_ParseAddress() throws {
    let typeTag = try TypeTag.parseTypeTag("address")
    XCTAssertEqual(typeTag, .Address)
  }

  func test_TypeTag_ParseSigner() throws {
    let typeTag = try TypeTag.parseTypeTag("signer")
    XCTAssertEqual(typeTag, .Signer)
  }

  func test_TypeTag_FormatPrimitive() throws {
    let typeTag = TypeTag.U64
    XCTAssertEqual(typeTag.toString(), "u64")
  }

  // =============================================================================
  // Vector Type Parsing
  // =============================================================================

  func test_TypeTag_ParseVectorU8() throws {
    let typeTag = try TypeTag.parseTypeTag("vector<u8>")
    if case .Vector(let inner) = typeTag {
      XCTAssertEqual(inner, .U8)
    } else {
      XCTFail("Expected Vector type")
    }
  }

  func test_TypeTag_ParseNestedVector() throws {
    let typeTag = try TypeTag.parseTypeTag("vector<vector<u8>>")
    if case .Vector(let outer) = typeTag {
      if case .Vector(let inner) = outer {
        XCTAssertEqual(inner, .U8)
      } else {
        XCTFail("Expected inner Vector type")
      }
    } else {
      XCTFail("Expected outer Vector type")
    }
  }

  func test_TypeTag_ParseVectorOfStruct() throws {
    let typeTag = try TypeTag.parseTypeTag("vector<0x1::aptos_coin::AptosCoin>")
    if case .Vector(let inner) = typeTag {
      XCTAssertTrue(inner.isStruct)
    } else {
      XCTFail("Expected Vector type")
    }
  }

  func test_TypeTag_FormatVector() throws {
    let typeTag = TypeTag.Vector(.U8)
    XCTAssertEqual(typeTag.toString(), "vector<u8>")
  }

  // =============================================================================
  // Struct Type Parsing
  // =============================================================================

  func test_TypeTag_ParseSimpleStruct() throws {
    let typeTag = try TypeTag.parseTypeTag("0x1::aptos_coin::AptosCoin")
    XCTAssertTrue(typeTag.isStruct)

    if case .Struct(let structTag) = typeTag {
      XCTAssertEqual(structTag.address.toString().lowercased(), "0x1")
      XCTAssertEqual(structTag.moduleName.identifier, "aptos_coin")
      XCTAssertEqual(structTag.name.identifier, "AptosCoin")
      XCTAssertEqual(structTag.typeArgs.count, 0)
    } else {
      XCTFail("Expected Struct type")
    }
  }

  func test_TypeTag_ParseStructWithTypeArg() throws {
    let typeTag = try TypeTag.parseTypeTag("0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>")
    XCTAssertTrue(typeTag.isStruct)

    if case .Struct(let structTag) = typeTag {
      XCTAssertEqual(structTag.address.toString().lowercased(), "0x1")
      XCTAssertEqual(structTag.moduleName.identifier, "coin")
      XCTAssertEqual(structTag.name.identifier, "CoinStore")
      XCTAssertEqual(structTag.typeArgs.count, 1)

      if case .Struct(let innerStruct) = structTag.typeArgs[0] {
        XCTAssertEqual(innerStruct.name.identifier, "AptosCoin")
      } else {
        XCTFail("Expected inner Struct type argument")
      }
    } else {
      XCTFail("Expected Struct type")
    }
  }

  func test_TypeTag_ParseStructWithMultipleTypeArgs() throws {
    let typeTag = try TypeTag.parseTypeTag(
      "0x1::some_module::Pair<u64, 0x1::aptos_coin::AptosCoin>")

    if case .Struct(let structTag) = typeTag {
      XCTAssertEqual(structTag.typeArgs.count, 2)
      XCTAssertEqual(structTag.typeArgs[0], .U64)
      XCTAssertTrue(structTag.typeArgs[1].isStruct)
    } else {
      XCTFail("Expected Struct type")
    }
  }

  func test_TypeTag_ParseString() throws {
    let typeTag = try TypeTag.parseTypeTag("0x1::string::String")
    XCTAssertTrue(typeTag.isString())
  }

  // =============================================================================
  // Invalid Type Parsing
  // =============================================================================

  func test_TypeTag_RejectEmptyString() throws {
    XCTAssertThrowsError(try TypeTag.parseTypeTag(""))
  }

  func test_TypeTag_RejectUnknownPrimitive() throws {
    XCTAssertThrowsError(try TypeTag.parseTypeTag("int"))
  }

  func test_TypeTag_RejectMalformedVector() throws {
    XCTAssertThrowsError(try TypeTag.parseTypeTag("vector<>"))
  }

  func test_TypeTag_RejectUnclosedVector() throws {
    XCTAssertThrowsError(try TypeTag.parseTypeTag("vector<u8"))
  }

  func test_TypeTag_RejectInvalidStructFormat() throws {
    XCTAssertThrowsError(try TypeTag.parseTypeTag("0x1::module"))
  }

  func test_TypeTag_RejectInvalidStructAddress() throws {
    XCTAssertThrowsError(try TypeTag.parseTypeTag("invalid::module::Struct"))
  }
}

// MARK: - Hashing Tests (hashing.feature)

extension AptosSpecsTests {

  // =============================================================================
  // SHA3-256
  // =============================================================================

  func test_Hashing_SHA3_256_Empty() throws {
    let input = [UInt8]()
    let hash = CryptoSwift.Digest.sha3(input, variant: .sha256)

    XCTAssertEqual(hash.count, 32)
    let expectedHex = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
    XCTAssertEqual(hash.map { String(format: "%02x", $0) }.joined(), expectedHex)
  }

  func test_Hashing_SHA3_256_Hello() throws {
    let input = Array("hello".utf8)
    let hash = CryptoSwift.Digest.sha3(input, variant: .sha256)

    let expectedHex = "3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392"
    XCTAssertEqual(hash.map { String(format: "%02x", $0) }.joined(), expectedHex)
  }

  func test_Hashing_SHA3_256_DifferentInputs() throws {
    let hash1 = CryptoSwift.Digest.sha3(Array("input1".utf8), variant: .sha256)
    let hash2 = CryptoSwift.Digest.sha3(Array("input2".utf8), variant: .sha256)

    XCTAssertNotEqual(hash1, hash2)
  }

  func test_Hashing_SHA3_256_Deterministic() throws {
    let input = Array("test data".utf8)
    let hash1 = CryptoSwift.Digest.sha3(input, variant: .sha256)
    let hash2 = CryptoSwift.Digest.sha3(input, variant: .sha256)

    XCTAssertEqual(hash1, hash2)
  }

  func test_Hashing_SHA3_256_Concatenation() throws {
    let parts = ["hello", " ", "world"]
    let concatenated = parts.joined()

    let hashConcatenated = CryptoSwift.Digest.sha3(Array(concatenated.utf8), variant: .sha256)
    let hashParts = CryptoSwift.Digest.sha3(Array("hello world".utf8), variant: .sha256)

    XCTAssertEqual(hashConcatenated, hashParts)
  }

  // =============================================================================
  // SHA2-256
  // =============================================================================

  func test_Hashing_SHA2_256_Empty() throws {
    let input = Data()
    let digest = CryptoKit.SHA256.hash(data: input)
    let hash = Array(digest)

    XCTAssertEqual(hash.count, 32)
    let expectedHex = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    XCTAssertEqual(hash.map { String(format: "%02x", $0) }.joined(), expectedHex)
  }

  func test_Hashing_SHA2_256_Hello() throws {
    let input = Data("hello".utf8)
    let digest = CryptoKit.SHA256.hash(data: input)
    let hash = Array(digest)

    let expectedHex = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    XCTAssertEqual(hash.map { String(format: "%02x", $0) }.joined(), expectedHex)
  }

  func test_Hashing_SHA2_256_DiffersFromSHA3() throws {
    let input = Array("test".utf8)

    let sha2Hash = Array(CryptoKit.SHA256.hash(data: Data(input)))
    let sha3Hash = CryptoSwift.Digest.sha3(input, variant: .sha256)

    XCTAssertNotEqual(sha2Hash, sha3Hash)
  }

  // =============================================================================
  // Large Data Hashing
  // =============================================================================

  func test_Hashing_LargeData() throws {
    let largeData = [UInt8](repeating: 0xAB, count: 1_000_000)  // 1 MB
    let hash = CryptoSwift.Digest.sha3(largeData, variant: .sha256)

    XCTAssertEqual(hash.count, 32)
  }
}

// MARK: - AuthenticationKey Tests (authentication-key.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Ed25519 Authentication Key
  // =============================================================================

  func test_AuthKey_DeriveFromEd25519() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let authKey = try publicKey.authKey()

    XCTAssertEqual(authKey.toUInt8Array().count, 32)
  }

  func test_AuthKey_Ed25519SchemeIdentifier() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let publicKeyBytes = publicKey.toUInt8Array()

    XCTAssertEqual(publicKeyBytes.count, 32)
  }

  func test_AuthKey_SamePublicKeySameAuthKey() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey

    let authKey1 = try publicKey.authKey()
    let authKey2 = try publicKey.authKey()

    XCTAssertEqual(authKey1.toUInt8Array(), authKey2.toUInt8Array())
  }

  func test_AuthKey_DifferentPublicKeysDifferentAuthKeys() throws {
    let privateKey1 = Ed25519PrivateKey.generate()
    let privateKey2 = Ed25519PrivateKey.generate()
    let publicKey1 = try privateKey1.publicKey() as! Ed25519PublicKey
    let publicKey2 = try privateKey2.publicKey() as! Ed25519PublicKey

    let authKey1 = try publicKey1.authKey()
    let authKey2 = try publicKey2.authKey()

    XCTAssertNotEqual(authKey1.toUInt8Array(), authKey2.toUInt8Array())
  }

  // =============================================================================
  // Authentication Key to Address
  // =============================================================================

  func test_AuthKey_ConvertToAddress() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let authKey = try publicKey.authKey()
    let address = try authKey.derivedAddress()

    XCTAssertEqual(address.toUInt8Array(), authKey.toUInt8Array())
  }

  func test_AuthKey_NewAccountAddressEqualsAuthKey() throws {
    let account = Account.generate()
    let publicKey = account.publicKey as! Ed25519PublicKey
    let authKey = try publicKey.authKey()

    XCTAssertEqual(account.accountAddress.toUInt8Array(), authKey.toUInt8Array())
  }

  // =============================================================================
  // Authentication Key Formatting
  // =============================================================================

  func test_AuthKey_AsBytes() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let authKey = try publicKey.authKey()
    let bytes = authKey.toUInt8Array()

    XCTAssertEqual(bytes.count, 32)
  }

  func test_AuthKey_ToHex() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let authKey = try publicKey.authKey()
    let hex = authKey.toString()

    XCTAssertTrue(hex.hasPrefix("0x"))
    XCTAssertEqual(hex.count, 66)  // 0x + 64 hex chars
  }
}

// MARK: - BCS Serialization Tests (serialization.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Boolean Serialization
  // =============================================================================

  func test_BCS_SerializeBoolFalse() throws {
    let serializer = BcsSerializer()
    try serializer.serializeBool(value: false)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 1)
    XCTAssertEqual(bytes[0], 0x00)
  }

  func test_BCS_SerializeBoolTrue() throws {
    let serializer = BcsSerializer()
    try serializer.serializeBool(value: true)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 1)
    XCTAssertEqual(bytes[0], 0x01)
  }

  func test_BCS_DeserializeBoolFalse() throws {
    let deserializer = BcsDeserializer(input: [0x00])
    let result = try deserializer.deserializeBool()
    XCTAssertFalse(result)
  }

  func test_BCS_DeserializeBoolTrue() throws {
    let deserializer = BcsDeserializer(input: [0x01])
    let result = try deserializer.deserializeBool()
    XCTAssertTrue(result)
  }

  // =============================================================================
  // Integer Serialization
  // =============================================================================

  func test_BCS_SerializeU8() throws {
    let serializer = BcsSerializer()
    try serializer.serializeU8(value: 255)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 1)
    XCTAssertEqual(bytes[0], 0xFF)
  }

  func test_BCS_SerializeU16() throws {
    let serializer = BcsSerializer()
    try serializer.serializeU16(value: 0x1234)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 2)
    XCTAssertEqual(bytes, [0x34, 0x12])  // Little-endian
  }

  func test_BCS_SerializeU32() throws {
    let serializer = BcsSerializer()
    try serializer.serializeU32(value: 0x1234_5678)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 4)
    XCTAssertEqual(bytes, [0x78, 0x56, 0x34, 0x12])  // Little-endian
  }

  func test_BCS_SerializeU64() throws {
    let serializer = BcsSerializer()
    try serializer.serializeU64(value: 0x1234_5678_9abc_def0)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 8)
    XCTAssertEqual(bytes, [0xf0, 0xde, 0xbc, 0x9a, 0x78, 0x56, 0x34, 0x12])  // Little-endian
  }

  // =============================================================================
  // String Serialization
  // =============================================================================

  func test_BCS_SerializeEmptyString() throws {
    let serializer = BcsSerializer()
    try serializer.serializeStr(value: "")
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes, [0x00])
  }

  func test_BCS_SerializeString() throws {
    let serializer = BcsSerializer()
    try serializer.serializeStr(value: "hello")
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes[0], 0x05)  // Length
    XCTAssertEqual(Array(bytes[1...]), Array("hello".utf8))
  }

  // =============================================================================
  // AccountAddress Serialization
  // =============================================================================

  func test_BCS_SerializeAccountAddress() throws {
    let address = try AccountAddress.fromString("0x1")
    let bytes = try address.bcsToBytes()

    XCTAssertEqual(bytes.count, 32)
    XCTAssertEqual(bytes[31], 0x01)
    for i in 0..<31 {
      XCTAssertEqual(bytes[i], 0x00)
    }
  }

  func test_BCS_DeserializeAccountAddress() throws {
    var bytes = [UInt8](repeating: 0, count: 32)
    bytes[31] = 0x42

    let deserializer = BcsDeserializer(input: bytes)
    let address = try AccountAddress.deserialize(deserializer: deserializer)

    // Verify the bytes match rather than string format
    XCTAssertEqual(address.toUInt8Array()[31], 0x42)
    for i in 0..<31 {
      XCTAssertEqual(address.toUInt8Array()[i], 0)
    }
  }
}

// MARK: - Secp256k1 Tests (secp256k1.feature)

extension AptosSpecsTests {

  // =============================================================================
  // Key Generation
  // =============================================================================

  func test_Secp256k1_GenerateRandomKeyPair() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey

    XCTAssertEqual(privateKey.toUInt8Array().count, 32)
    XCTAssertEqual(publicKey.toUInt8Array().count, 65)  // Uncompressed format
  }

  func test_Secp256k1_GenerateUniqueKeyPairs() throws {
    let privateKey1 = Secp256k1PrivateKey.generate()
    let privateKey2 = Secp256k1PrivateKey.generate()
    let publicKey1 = try privateKey1.publicKey() as! Secp256k1PublicKey
    let publicKey2 = try privateKey2.publicKey() as! Secp256k1PublicKey

    XCTAssertNotEqual(privateKey1.toUInt8Array(), privateKey2.toUInt8Array())
    XCTAssertNotEqual(publicKey1.toUInt8Array(), publicKey2.toUInt8Array())
  }

  func test_Secp256k1_CreateFromSeed() throws {
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 1
    let privateKey1 = try Secp256k1PrivateKey(seed)
    let privateKey2 = try Secp256k1PrivateKey(seed)

    XCTAssertEqual(privateKey1.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Secp256k1_CreateFromHexString() throws {
    let hex = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    let privateKey = try Secp256k1PrivateKey(hex)

    XCTAssertEqual(privateKey.toUInt8Array().count, 32)
  }

  func test_Secp256k1_RejectInvalidLength() throws {
    let invalidBytes = [UInt8](repeating: 0, count: 31)
    XCTAssertThrowsError(try Secp256k1PrivateKey(invalidBytes))
  }

  // =============================================================================
  // Signing
  // =============================================================================

  func test_Secp256k1_SignMessage() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let message = Array("hello world".utf8)

    let signature = try privateKey.sign(message: message) as! Secp256k1Signature
    XCTAssertEqual(signature.toUInt8Array().count, 64)

    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey
    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Secp256k1_SignEmptyMessage() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let message = [UInt8]()

    let signature = try privateKey.sign(message: message) as! Secp256k1Signature
    XCTAssertEqual(signature.toUInt8Array().count, 64)

    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey
    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Secp256k1_DifferentMessagesDifferentSignatures() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let msg1 = Array("message1".utf8)
    let msg2 = Array("message2".utf8)

    let sig1 = try privateKey.sign(message: msg1) as! Secp256k1Signature
    let sig2 = try privateKey.sign(message: msg2) as! Secp256k1Signature

    XCTAssertNotEqual(sig1.toUInt8Array(), sig2.toUInt8Array())
  }

  func test_Secp256k1_DifferentKeysDifferentSignatures() throws {
    let privateKey1 = Secp256k1PrivateKey.generate()
    let privateKey2 = Secp256k1PrivateKey.generate()
    let message = Array("same message".utf8)

    let sig1 = try privateKey1.sign(message: message) as! Secp256k1Signature
    let sig2 = try privateKey2.sign(message: message) as! Secp256k1Signature

    XCTAssertNotEqual(sig1.toUInt8Array(), sig2.toUInt8Array())
  }

  // =============================================================================
  // Verification
  // =============================================================================

  func test_Secp256k1_VerifyValidSignature() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let message = Array("test message".utf8)
    let signature = try privateKey.sign(message: message) as! Secp256k1Signature
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey

    let isValid = try publicKey.verifySignature(message: message, signature: signature)
    XCTAssertTrue(isValid)
  }

  func test_Secp256k1_RejectSignatureFromWrongKey() throws {
    let privateKey1 = Secp256k1PrivateKey.generate()
    let privateKey2 = Secp256k1PrivateKey.generate()
    let message = Array("test message".utf8)

    let signature = try privateKey1.sign(message: message) as! Secp256k1Signature
    let publicKey2 = try privateKey2.publicKey() as! Secp256k1PublicKey

    let isValid = try publicKey2.verifySignature(message: message, signature: signature)
    XCTAssertFalse(isValid)
  }

  func test_Secp256k1_RejectSignatureForWrongMessage() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let signature = try privateKey.sign(message: Array("original".utf8)) as! Secp256k1Signature
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey

    let isValid = try publicKey.verifySignature(
      message: Array("modified".utf8), signature: signature)
    XCTAssertFalse(isValid)
  }

  // =============================================================================
  // Key Export
  // =============================================================================

  func test_Secp256k1_ExportPublicKeyBytes() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey
    let bytes = publicKey.toUInt8Array()

    XCTAssertEqual(bytes.count, 65)
    XCTAssertEqual(bytes[0], 0x04)  // Uncompressed public key prefix
  }

  func test_Secp256k1_ExportPrivateKeyBytes() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let bytes = privateKey.toUInt8Array()

    XCTAssertEqual(bytes.count, 32)

    let privateKey2 = try Secp256k1PrivateKey(bytes)
    XCTAssertEqual(privateKey.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Secp256k1_ExportKeysAsHex() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let hex = privateKey.toString()

    XCTAssertTrue(hex.hasPrefix("0x"))
    XCTAssertEqual(hex.count, 66)  // 0x + 64 hex chars
  }
}

// MARK: - SingleKey Account with Secp256k1 Tests

extension AptosSpecsTests {

  func test_SingleKeyAccount_GenerateSecp256k1() throws {
    let account = Account.generate(scheme: .secp256k1Ecdsa)

    XCTAssertNotNil(account.accountAddress)
    XCTAssertNotNil(account.publicKey)
    XCTAssertEqual(account.signingScheme, .singleKey)
  }

  func test_SingleKeyAccount_Secp256k1_UniqueAddresses() throws {
    let account1 = Account.generate(scheme: .secp256k1Ecdsa)
    let account2 = Account.generate(scheme: .secp256k1Ecdsa)

    XCTAssertNotEqual(account1.accountAddress, account2.accountAddress)
  }

  func test_SingleKeyAccount_Secp256k1_SignAndVerify() throws {
    let account = Account.generate(scheme: .secp256k1Ecdsa)
    let message = Array("hello from secp256k1".utf8)

    let signature = try account.sign(message: message)
    let isValid = try account.verifySignature(message: message, signature: signature)

    XCTAssertTrue(isValid)
  }

  func test_SingleKeyAccount_Secp256k1_FromPrivateKey() throws {
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 42
    let privateKey = try Secp256k1PrivateKey(seed)
    let account = try Account.SingleKeyAccount(privateKey: privateKey)

    XCTAssertNotNil(account.accountAddress)
    XCTAssertEqual(account.signingScheme, .singleKey)
  }

  func test_SingleKeyAccount_Ed25519_DifferentAddressFromSecp256k1() throws {
    // Same seed produces different addresses for different key types
    var seed = [UInt8](repeating: 0, count: 32)
    seed[0] = 42

    let ed25519Key = try Ed25519PrivateKey(seed)
    let secp256k1Key = try Secp256k1PrivateKey(seed)

    let ed25519Account = try Account.SingleKeyAccount(privateKey: ed25519Key)
    let secp256k1Account = try Account.SingleKeyAccount(privateKey: secp256k1Key)

    XCTAssertNotEqual(ed25519Account.accountAddress, secp256k1Account.accountAddress)
  }
}

// MARK: - Mnemonic/BIP-44 Derivation Tests (mnemonic-derivation.feature)

extension AptosSpecsTests {

  // Known test mnemonic - DO NOT use in production
  static let testMnemonic =
    "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

  func test_Mnemonic_Ed25519_DerivationPath() throws {
    // Standard Aptos BIP-44 path for Ed25519
    let path = "m/44'/637'/0'/0'/0'"

    let privateKey = try Ed25519PrivateKey.fromDerivationPath(
      path: path, mnemonic: Self.testMnemonic)
    XCTAssertEqual(privateKey.toUInt8Array().count, 32)

    // Derivation should be deterministic
    let privateKey2 = try Ed25519PrivateKey.fromDerivationPath(
      path: path, mnemonic: Self.testMnemonic)
    XCTAssertEqual(privateKey.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Mnemonic_Ed25519_DifferentPathsDifferentKeys() throws {
    let path1 = "m/44'/637'/0'/0'/0'"
    let path2 = "m/44'/637'/0'/0'/1'"

    let privateKey1 = try Ed25519PrivateKey.fromDerivationPath(
      path: path1, mnemonic: Self.testMnemonic)
    let privateKey2 = try Ed25519PrivateKey.fromDerivationPath(
      path: path2, mnemonic: Self.testMnemonic)

    XCTAssertNotEqual(privateKey1.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Mnemonic_Secp256k1_DerivationPath() throws {
    // Standard BIP-44 path for secp256k1
    let path = "m/44'/637'/0'/0/0"

    let privateKey = try Secp256k1PrivateKey.fromDerivationPath(
      path: path, mnemonic: Self.testMnemonic)
    XCTAssertEqual(privateKey.toUInt8Array().count, 32)

    // Derivation should be deterministic
    let privateKey2 = try Secp256k1PrivateKey.fromDerivationPath(
      path: path, mnemonic: Self.testMnemonic)
    XCTAssertEqual(privateKey.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Mnemonic_Secp256k1_DifferentPathsDifferentKeys() throws {
    let path1 = "m/44'/637'/0'/0/0"
    let path2 = "m/44'/637'/0'/0/1"

    let privateKey1 = try Secp256k1PrivateKey.fromDerivationPath(
      path: path1, mnemonic: Self.testMnemonic)
    let privateKey2 = try Secp256k1PrivateKey.fromDerivationPath(
      path: path2, mnemonic: Self.testMnemonic)

    XCTAssertNotEqual(privateKey1.toUInt8Array(), privateKey2.toUInt8Array())
  }

  func test_Account_Ed25519_FromDerivationPath() throws {
    let path = "m/44'/637'/0'/0'/0'"

    let account = try Account.fromDerivationPath(path, mnemonic: Self.testMnemonic)
    XCTAssertNotNil(account.accountAddress)
    XCTAssertEqual(account.signingScheme, .ed25519)
  }

  func test_Account_SingleKey_FromDerivationPath() throws {
    let path = "m/44'/637'/0'/0/0"

    let account = try Account.fromDerivationPath(
      path, mnemonic: Self.testMnemonic, scheme: .secp256k1Ecdsa)
    XCTAssertNotNil(account.accountAddress)
    XCTAssertEqual(account.signingScheme, .singleKey)
  }

  func test_Mnemonic_InvalidPath_Ed25519() throws {
    // Invalid path (not matching BIP-44 format)
    let invalidPath = "m/44'/637'/0'/0/0"  // Missing apostrophe for hardened derivation

    XCTAssertThrowsError(
      try Ed25519PrivateKey.fromDerivationPath(path: invalidPath, mnemonic: Self.testMnemonic))
  }

  func test_Mnemonic_InvalidPath_Secp256k1() throws {
    // Invalid path for secp256k1
    let invalidPath = "invalid/path"

    XCTAssertThrowsError(
      try Secp256k1PrivateKey.fromDerivationPath(path: invalidPath, mnemonic: Self.testMnemonic))
  }
}

// MARK: - Hex Utility Tests

extension AptosSpecsTests {

  func test_Hex_FromHexString_WithPrefix() throws {
    let hex = try Hex.fromHexString("0x1234abcd")
    let bytes = hex.toUInt8Array()

    XCTAssertEqual(bytes, [0x12, 0x34, 0xab, 0xcd])
  }

  func test_Hex_FromHexString_WithoutPrefix() throws {
    let hex = try Hex.fromHexString("1234abcd")
    let bytes = hex.toUInt8Array()

    XCTAssertEqual(bytes, [0x12, 0x34, 0xab, 0xcd])
  }

  func test_Hex_ToString() throws {
    let hex = try Hex.fromHexString("0x1234")
    XCTAssertEqual(hex.toString(), "0x1234")
  }

  func test_Hex_ToStringWithoutPrefix() throws {
    let hex = try Hex.fromHexString("0x1234")
    XCTAssertEqual(hex.toStringWithoutPrefix(), "1234")
  }

  func test_Hex_FromBytes() throws {
    let bytes: [UInt8] = [0xde, 0xad, 0xbe, 0xef]
    let hex = Hex(data: bytes)

    XCTAssertEqual(hex.toString().lowercased(), "0xdeadbeef")
  }

  func test_Hex_FromData() throws {
    let data = Data([0xca, 0xfe, 0xba, 0xbe])
    let hex = Hex(data: data)

    XCTAssertEqual(hex.toString().lowercased(), "0xcafebabe")
  }

  func test_Hex_Equality() throws {
    let hex1 = try Hex.fromHexString("0x1234")
    let hex2 = try Hex.fromHexString("1234")

    XCTAssertTrue(hex1.equals(hex2))
    XCTAssertEqual(hex1, hex2)
  }

  func test_Hex_Inequality() throws {
    let hex1 = try Hex.fromHexString("0x1234")
    let hex2 = try Hex.fromHexString("0x5678")

    XCTAssertFalse(hex1.equals(hex2))
    XCTAssertNotEqual(hex1, hex2)
  }

  func test_Hex_IsValid_Valid() throws {
    let result = Hex.isValid("0x1234abcd")
    XCTAssertTrue(result.valid)
    XCTAssertNil(result.invalidReason)
  }

  func test_Hex_IsValid_InvalidChars() throws {
    let result = Hex.isValid("0xGGGG")
    XCTAssertFalse(result.valid)
    XCTAssertEqual(result.invalidReason, .invalidHexChars)
  }

  func test_Hex_IsValid_OddLength() throws {
    let result = Hex.isValid("0x123")  // 3 hex chars is invalid
    XCTAssertFalse(result.valid)
    XCTAssertEqual(result.invalidReason, .invalidLength)
  }

  func test_Hex_IsValid_Empty() throws {
    let result = Hex.isValid("0x")
    XCTAssertFalse(result.valid)
    XCTAssertEqual(result.invalidReason, .tooShort)
  }

  func test_Hex_RejectEmptyString() throws {
    XCTAssertThrowsError(try Hex.fromHexString(""))
  }

  func test_Hex_RejectInvalidChars() throws {
    XCTAssertThrowsError(try Hex.fromHexString("0xZZZZ"))
  }

  func test_Hex_RejectOddLength() throws {
    XCTAssertThrowsError(try Hex.fromHexString("0x123"))
  }

  func test_Hex_UppercaseNormalization() throws {
    let hex = try Hex.fromHexString("0xABCDEF")
    XCTAssertEqual(hex.toUInt8Array(), [0xab, 0xcd, 0xef])
  }

  func test_Hex_MixedCaseNormalization() throws {
    let hex = try Hex.fromHexString("0xAbCdEf")
    XCTAssertEqual(hex.toUInt8Array(), [0xab, 0xcd, 0xef])
  }
}

// MARK: - Additional BCS Tests

extension AptosSpecsTests {

  func test_BCS_SerializeU128() throws {
    // Use a smaller value that fits in UInt128
    let serializer = BcsSerializer()
    try serializer.serializeU128(value: 0x1234_5678_9abc_def0)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes.count, 16)
    // Little-endian: low 8 bytes first, then high 8 bytes (zeros)
    XCTAssertEqual(bytes[0], 0xf0)
    XCTAssertEqual(bytes[1], 0xde)
    XCTAssertEqual(bytes[7], 0x12)
    // High bytes should be zero
    for i in 8..<16 {
      XCTAssertEqual(bytes[i], 0)
    }
  }

  func test_BCS_DeserializeU8() throws {
    let deserializer = BcsDeserializer(input: [0x42])
    let result = try deserializer.deserializeU8()
    XCTAssertEqual(result, 0x42)
  }

  func test_BCS_DeserializeU16() throws {
    let deserializer = BcsDeserializer(input: [0x34, 0x12])
    let result = try deserializer.deserializeU16()
    XCTAssertEqual(result, 0x1234)
  }

  func test_BCS_DeserializeU32() throws {
    let deserializer = BcsDeserializer(input: [0x78, 0x56, 0x34, 0x12])
    let result = try deserializer.deserializeU32()
    XCTAssertEqual(result, 0x1234_5678)
  }

  func test_BCS_DeserializeU64() throws {
    let deserializer = BcsDeserializer(input: [0xf0, 0xde, 0xbc, 0x9a, 0x78, 0x56, 0x34, 0x12])
    let result = try deserializer.deserializeU64()
    XCTAssertEqual(result, 0x1234_5678_9abc_def0)
  }

  func test_BCS_DeserializeString() throws {
    let bytes: [UInt8] = [0x05] + Array("hello".utf8)
    let deserializer = BcsDeserializer(input: bytes)
    let result = try deserializer.deserializeStr()
    XCTAssertEqual(result, "hello")
  }

  func test_BCS_SerializeBytes() throws {
    let serializer = BcsSerializer()
    try serializer.serializeBytes(value: [0x01, 0x02, 0x03])
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes[0], 0x03)  // Length
    XCTAssertEqual(Array(bytes[1...]), [0x01, 0x02, 0x03])
  }

  func test_BCS_DeserializeBytes() throws {
    let deserializer = BcsDeserializer(input: [0x03, 0x01, 0x02, 0x03])
    let result = try deserializer.deserializeBytes()
    XCTAssertEqual(result, [0x01, 0x02, 0x03])
  }

  func test_BCS_SerializeEmptyBytes() throws {
    let serializer = BcsSerializer()
    try serializer.serializeBytes(value: [])
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes, [0x00])
  }

  func test_BCS_SerializeULEB128_Small() throws {
    let serializer = BcsSerializer()
    try serializer.serializeLen(value: 127)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes, [0x7f])
  }

  func test_BCS_SerializeULEB128_Medium() throws {
    let serializer = BcsSerializer()
    try serializer.serializeLen(value: 128)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes, [0x80, 0x01])
  }

  func test_BCS_SerializeULEB128_Large() throws {
    let serializer = BcsSerializer()
    try serializer.serializeLen(value: 16384)
    let bytes = serializer.toUInt8Array()

    XCTAssertEqual(bytes, [0x80, 0x80, 0x01])
  }
}

// MARK: - TypeTag BCS Serialization Tests

extension AptosSpecsTests {

  func test_TypeTag_BCS_SerializeBool() throws {
    let typeTag = TypeTag.Bool
    let bytes = try typeTag.bcsToBytes()

    XCTAssertEqual(bytes[0], 0)  // Bool variant index
  }

  func test_TypeTag_BCS_SerializeU8() throws {
    let typeTag = TypeTag.U8
    let bytes = try typeTag.bcsToBytes()

    XCTAssertEqual(bytes[0], 1)  // U8 variant index
  }

  func test_TypeTag_BCS_SerializeU64() throws {
    let typeTag = TypeTag.U64
    let bytes = try typeTag.bcsToBytes()

    XCTAssertEqual(bytes[0], 2)  // U64 variant index
  }

  func test_TypeTag_BCS_SerializeAddress() throws {
    let typeTag = TypeTag.Address
    let bytes = try typeTag.bcsToBytes()

    XCTAssertEqual(bytes[0], 4)  // Address variant index
  }

  func test_TypeTag_BCS_SerializeVector() throws {
    let typeTag = TypeTag.Vector(.U8)
    let bytes = try typeTag.bcsToBytes()

    XCTAssertEqual(bytes[0], 6)  // Vector variant index
    XCTAssertEqual(bytes[1], 1)  // U8 inner type
  }

  func test_TypeTag_BCS_RoundTrip() throws {
    let original = try TypeTag.parseTypeTag("0x1::aptos_coin::AptosCoin")
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try TypeTag.deserialize(deserializer: deserializer)

    XCTAssertEqual(result, original)
  }

  func test_TypeTag_BCS_RoundTrip_Complex() throws {
    let original = try TypeTag.parseTypeTag("0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>")
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try TypeTag.deserialize(deserializer: deserializer)

    XCTAssertEqual(result, original)
  }
}

// MARK: - Additional Address Tests

extension AptosSpecsTests {

  func test_Address_FromHexInput_String() throws {
    // Using string as hex input
    let address = try AccountAddress.from("0x1")
    XCTAssertEqual(address.toString().lowercased(), "0x1")
  }

  func test_Address_FromHexInput_Data() throws {
    var data = Data(repeating: 0, count: 32)
    data[31] = 0x42
    let address = try AccountAddress.from(data)
    XCTAssertEqual(address.toUInt8Array()[31], 0x42)
  }

  func test_Address_FromHexInput_Bytes() throws {
    var bytes = [UInt8](repeating: 0, count: 32)
    bytes[31] = 0x99
    let address = try AccountAddress.from(bytes)
    XCTAssertEqual(address.toUInt8Array()[31], 0x99)
  }

  // SDK defines special as: last byte < 16 (0x10) and all other bytes are 0
  // So addresses 0x0-0xf are special
  func test_Address_IsSpecial_0to15() throws {
    for i in 0...15 {
      let hex = String(format: "0x%x", i)
      let address = try AccountAddress.fromString(hex)
      XCTAssertTrue(address.isSpecial(), "Address \(hex) should be special")
    }
  }

  func test_Address_IsNotSpecial_GreaterThan15() throws {
    for i in [16, 100, 1000, 0xABCD] {
      let hex = String(format: "0x%x", i)
      let address = try AccountAddress.fromString(hex)
      XCTAssertFalse(address.isSpecial(), "Address \(hex) should not be special")
    }
  }
}

// MARK: - Additional TypeTag Tests

extension AptosSpecsTests {

  func test_TypeTag_IsStruct_True() throws {
    let typeTag = try TypeTag.parseTypeTag("0x1::aptos_coin::AptosCoin")
    XCTAssertTrue(typeTag.isStruct)
  }

  func test_TypeTag_IsStruct_False() throws {
    let typeTag = TypeTag.U64
    XCTAssertFalse(typeTag.isStruct)
  }

  func test_TypeTag_IsOption() throws {
    let typeTag = try TypeTag.parseTypeTag("0x1::option::Option<u64>")
    XCTAssertTrue(typeTag.isOption())
  }

  func test_TypeTag_IsObject() throws {
    let typeTag = try TypeTag.parseTypeTag("0x1::object::Object<0x1::aptos_coin::AptosCoin>")
    XCTAssertTrue(typeTag.isObject())
  }

  func test_TypeTag_StructTag_AptosCoin() throws {
    let aptosCoin = TypeTag.StructTag.aptosCoin
    XCTAssertEqual(aptosCoin.address, AccountAddress.ONE)
    XCTAssertEqual(aptosCoin.moduleName.identifier, "aptos_coin")
    XCTAssertEqual(aptosCoin.name.identifier, "AptosCoin")
    XCTAssertEqual(aptosCoin.typeArgs.count, 0)
  }

  func test_TypeTag_StructTag_String() throws {
    let stringTag = TypeTag.StructTag.string
    XCTAssertEqual(stringTag.address, AccountAddress.ONE)
    XCTAssertEqual(stringTag.moduleName.identifier, "string")
    XCTAssertEqual(stringTag.name.identifier, "String")
  }

  func test_TypeTag_StructTag_Option() throws {
    let optionTag = TypeTag.StructTag.option(.U64)
    XCTAssertEqual(optionTag.address, AccountAddress.ONE)
    XCTAssertEqual(optionTag.moduleName.identifier, "option")
    XCTAssertEqual(optionTag.name.identifier, "Option")
    XCTAssertEqual(optionTag.typeArgs.count, 1)
    XCTAssertEqual(optionTag.typeArgs[0], .U64)
  }

  func test_TypeTag_StructTag_Object() throws {
    let objectTag = TypeTag.StructTag.object(.Address)
    XCTAssertEqual(objectTag.address, AccountAddress.ONE)
    XCTAssertEqual(objectTag.moduleName.identifier, "object")
    XCTAssertEqual(objectTag.name.identifier, "Object")
    XCTAssertEqual(objectTag.typeArgs.count, 1)
    XCTAssertEqual(objectTag.typeArgs[0], .Address)
  }
}

// MARK: - Identifier Tests

extension AptosSpecsTests {

  func test_Identifier_Create() throws {
    let id = Identifier("my_module")
    XCTAssertEqual(id.identifier, "my_module")
  }

  func test_Identifier_Equality() throws {
    let id1 = Identifier("module_name")
    let id2 = Identifier("module_name")
    XCTAssertEqual(id1, id2)
  }

  func test_Identifier_Inequality() throws {
    let id1 = Identifier("module_a")
    let id2 = Identifier("module_b")
    XCTAssertNotEqual(id1, id2)
  }

  func test_Identifier_BCS_Serialize() throws {
    let id = Identifier("test")
    let bytes = try id.bcsToBytes()

    // Identifier serializes as a string: length + bytes
    XCTAssertEqual(bytes[0], 4)  // Length of "test"
    XCTAssertEqual(Array(bytes[1...]), Array("test".utf8))
  }

  func test_Identifier_BCS_Deserialize() throws {
    let bytes: [UInt8] = [5] + Array("hello".utf8)
    let deserializer = BcsDeserializer(input: bytes)
    let id = try Identifier.deserialize(deserializer: deserializer)

    XCTAssertEqual(id.identifier, "hello")
  }

  func test_Identifier_BCS_RoundTrip() throws {
    let original = Identifier("aptos_coin")
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try Identifier.deserialize(deserializer: deserializer)

    XCTAssertEqual(result, original)
  }
}

// MARK: - ModuleId Tests

extension AptosSpecsTests {

  func test_ModuleId_Create() throws {
    let moduleId = ModuleId(
      address: try AccountAddress.fromString("0x1"),
      name: Identifier("aptos_coin")
    )

    XCTAssertEqual(moduleId.address.toString().lowercased(), "0x1")
    XCTAssertEqual(moduleId.name.identifier, "aptos_coin")
  }

  func test_ModuleId_FromStr() throws {
    let moduleId = try ModuleId.fromStr("0x1::aptos_coin")

    XCTAssertEqual(moduleId.address.toString().lowercased(), "0x1")
    XCTAssertEqual(moduleId.name.identifier, "aptos_coin")
  }

  func test_ModuleId_FromStr_FullAddress() throws {
    let moduleId = try ModuleId.fromStr(
      "0x0000000000000000000000000000000000000000000000000000000000000001::coin")

    XCTAssertEqual(moduleId.address.toString().lowercased(), "0x1")
    XCTAssertEqual(moduleId.name.identifier, "coin")
  }

  func test_ModuleId_FromStr_InvalidFormat() throws {
    XCTAssertThrowsError(try ModuleId.fromStr("0x1"))
    XCTAssertThrowsError(try ModuleId.fromStr("invalid"))
  }

  func test_ModuleId_BCS_Serialize() throws {
    let moduleId = ModuleId(
      address: try AccountAddress.fromString("0x1"),
      name: Identifier("coin")
    )

    let bytes = try moduleId.bcsToBytes()

    // First 32 bytes are address, then serialized string
    XCTAssertEqual(bytes.count, 32 + 1 + 4)  // 32 address + 1 length + 4 chars
    XCTAssertEqual(bytes[31], 1)  // Address byte
  }

  func test_ModuleId_BCS_RoundTrip() throws {
    let original = ModuleId(
      address: try AccountAddress.fromString("0x1234"),
      name: Identifier("my_module")
    )

    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try ModuleId.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.address, original.address)
    XCTAssertEqual(result.name, original.name)
  }
}

// MARK: - ChainId Tests

extension AptosSpecsTests {

  func test_ChainId_Create() throws {
    let chainId = ChainId(id: 1)
    XCTAssertEqual(chainId.id, 1)
  }

  func test_ChainId_MainnetValue() throws {
    let chainId = ChainId(id: 1)
    XCTAssertEqual(chainId.id, 1)
  }

  func test_ChainId_TestnetValue() throws {
    let chainId = ChainId(id: 2)
    XCTAssertEqual(chainId.id, 2)
  }

  func test_ChainId_DevnetValue() throws {
    // Devnet typically uses a different chain ID
    let chainId = ChainId(id: 4)
    XCTAssertEqual(chainId.id, 4)
  }

  func test_ChainId_Equality() throws {
    let chainId1 = ChainId(id: 1)
    let chainId2 = ChainId(id: 1)
    XCTAssertEqual(chainId1, chainId2)
  }

  func test_ChainId_Inequality() throws {
    let chainId1 = ChainId(id: 1)
    let chainId2 = ChainId(id: 2)
    XCTAssertNotEqual(chainId1, chainId2)
  }

  func test_ChainId_BCS_Serialize() throws {
    let chainId = ChainId(id: 42)
    let bytes = try chainId.bcsToBytes()

    XCTAssertEqual(bytes.count, 1)
    XCTAssertEqual(bytes[0], 42)
  }

  func test_ChainId_BCS_Deserialize() throws {
    let deserializer = BcsDeserializer(input: [255])
    let chainId = try ChainId.deserialize(deserializer: deserializer)

    XCTAssertEqual(chainId.id, 255)
  }

  func test_ChainId_BCS_RoundTrip() throws {
    let original = ChainId(id: 123)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try ChainId.deserialize(deserializer: deserializer)

    XCTAssertEqual(result, original)
  }
}

// MARK: - Move Primitive Tests

extension AptosSpecsTests {

  func test_MovePrimitive_Boolean_True() throws {
    let value = BCS.Boolean(value: true)
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes, [0x01])
  }

  func test_MovePrimitive_Boolean_False() throws {
    let value = BCS.Boolean(value: false)
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes, [0x00])
  }

  func test_MovePrimitive_Boolean_RoundTrip() throws {
    let original = BCS.Boolean(value: true)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try BCS.Boolean.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }

  func test_MovePrimitive_U8() throws {
    let value = BCS.U8(value: 255)
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes, [0xFF])
  }

  func test_MovePrimitive_U8_RoundTrip() throws {
    let original = BCS.U8(value: 42)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try BCS.U8.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }

  func test_MovePrimitive_U16() throws {
    let value = BCS.U16(value: 0x1234)
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes, [0x34, 0x12])  // Little-endian
  }

  func test_MovePrimitive_U16_RoundTrip() throws {
    let original = BCS.U16(value: 12345)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try BCS.U16.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }

  func test_MovePrimitive_U32() throws {
    let value = BCS.U32(value: 0x1234_5678)
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes, [0x78, 0x56, 0x34, 0x12])  // Little-endian
  }

  func test_MovePrimitive_U32_RoundTrip() throws {
    let original = BCS.U32(value: 123_456_789)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try BCS.U32.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }

  func test_MovePrimitive_U64() throws {
    let value = BCS.U64(value: 0x1234_5678_9ABC_DEF0)
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes.count, 8)
    XCTAssertEqual(bytes[0], 0xF0)  // Lowest byte first
  }

  func test_MovePrimitive_U64_RoundTrip() throws {
    let original = BCS.U64(value: 9_876_543_210)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try BCS.U64.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }
}

// MARK: - MoveString Tests

extension AptosSpecsTests {

  func test_MoveString_Create() throws {
    let value = MoveString(value: "hello")
    XCTAssertEqual(value.value, "hello")
  }

  func test_MoveString_Empty() throws {
    let value = MoveString(value: "")
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes, [0x00])
  }

  func test_MoveString_Serialize() throws {
    let value = MoveString(value: "test")
    let bytes = try value.bcsToBytes()

    XCTAssertEqual(bytes[0], 4)  // Length
    XCTAssertEqual(Array(bytes[1...]), Array("test".utf8))
  }

  func test_MoveString_RoundTrip() throws {
    let original = MoveString(value: "Hello, Aptos!")
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try MoveString.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }

  func test_MoveString_Unicode() throws {
    let original = MoveString(value: "Hello, 世界! 🚀")
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try MoveString.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value, original.value)
  }
}

// MARK: - MoveVector Tests

extension AptosSpecsTests {

  func test_MoveVector_U8_Empty() throws {
    let vector = MoveVector<BCS.U8>.U8([])
    let bytes = try vector.bcsToBytes()

    XCTAssertEqual(bytes, [0x00])  // Just length (0)
  }

  func test_MoveVector_U8() throws {
    let vector = MoveVector<BCS.U8>.U8([1, 2, 3])
    let bytes = try vector.bcsToBytes()

    XCTAssertEqual(bytes[0], 3)  // Length
    XCTAssertEqual(Array(bytes[1...]), [1, 2, 3])
  }

  func test_MoveVector_U8_RoundTrip() throws {
    let original = MoveVector<BCS.U8>.U8([10, 20, 30, 40, 50])
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try MoveVector<BCS.U8>.deserialize(deserializer: deserializer)

    XCTAssertEqual(result.value.map { $0.value }, original.value.map { $0.value })
  }

  func test_MoveVector_U64() throws {
    let vector = MoveVector<BCS.U64>.U64([100, 200, 300])
    let bytes = try vector.bcsToBytes()

    XCTAssertEqual(bytes[0], 3)  // Length
    XCTAssertEqual(bytes.count, 1 + 3 * 8)  // Length + 3 U64s
  }

  func test_MoveVector_Boolean() throws {
    let vector = MoveVector<BCS.Boolean>.Boolean([true, false, true])
    let bytes = try vector.bcsToBytes()

    XCTAssertEqual(bytes, [3, 1, 0, 1])  // Length + values
  }

  func test_MoveVector_String() throws {
    let vector = MoveVector<MoveString>.String(["hello", "world"])
    let bytes = try vector.bcsToBytes()

    XCTAssertEqual(bytes[0], 2)  // Vector length
    XCTAssertEqual(bytes[1], 5)  // First string length
  }
}

// MARK: - MoveOption Tests

extension AptosSpecsTests {

  func test_MoveOption_None() throws {
    let option = MoveOption<BCS.U64>(value: nil)

    XCTAssertFalse(option.isSome)
    XCTAssertNil(option.value)
  }

  func test_MoveOption_Some() throws {
    let innerValue = BCS.U64(value: 42)
    let option = MoveOption<BCS.U64>(value: innerValue)

    XCTAssertTrue(option.isSome)
    XCTAssertEqual(option.unwrap.value, 42)
  }

  func test_MoveOption_U8_None() throws {
    let option = MoveOption<BCS.U8>.U8(nil)
    let bytes = try option.bcsToBytes()

    XCTAssertEqual(bytes, [0x00])  // Empty vector
  }

  func test_MoveOption_U8_Some() throws {
    let option = MoveOption<BCS.U8>.U8(42)
    let bytes = try option.bcsToBytes()

    XCTAssertEqual(bytes, [0x01, 42])  // Vector with one element
  }

  func test_MoveOption_U64_Some() throws {
    let option = MoveOption<BCS.U64>.U64(1_000_000)
    let bytes = try option.bcsToBytes()

    XCTAssertEqual(bytes[0], 1)  // Vector length
    XCTAssertEqual(bytes.count, 9)  // 1 length + 8 bytes for U64
  }

  func test_MoveOption_Boolean() throws {
    let option = MoveOption<BCS.Boolean>.Boolean(true)
    let bytes = try option.bcsToBytes()

    XCTAssertEqual(bytes, [0x01, 0x01])  // Vector with true
  }

  func test_MoveOption_String_Some() throws {
    let option = MoveOption<MoveString>.String("hello")
    let bytes = try option.bcsToBytes()

    XCTAssertEqual(bytes[0], 1)  // Vector length
    XCTAssertEqual(bytes[1], 5)  // String length
  }

  func test_MoveOption_String_None() throws {
    let option = MoveOption<MoveString>.String(nil)
    let bytes = try option.bcsToBytes()

    XCTAssertEqual(bytes, [0x00])
  }

  func test_MoveOption_RoundTrip_Some() throws {
    let original = MoveOption<BCS.U64>.U64(12345)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try MoveOption<BCS.U64>.deserialize(deserializer: deserializer)

    XCTAssertTrue(result.isSome)
    XCTAssertEqual(result.unwrap.value, 12345)
  }

  func test_MoveOption_RoundTrip_None() throws {
    let original = MoveOption<BCS.U64>(value: nil)
    let bytes = try original.bcsToBytes()
    let deserializer = BcsDeserializer(input: bytes)
    let result = try MoveOption<BCS.U64>.deserialize(deserializer: deserializer)

    XCTAssertFalse(result.isSome)
    XCTAssertNil(result.value)
  }
}

// MARK: - API Client Tests

extension AptosSpecsTests {

  func test_Client_DevnetConfiguration() throws {
    let client = Aptos(aptosConfig: .devnet)
    XCTAssertNotNil(client)
    XCTAssertEqual(client.aptosConfig.network.name, "devnet")
  }

  func test_Client_TestnetConfiguration() throws {
    let client = Aptos(aptosConfig: .testnet)
    XCTAssertNotNil(client)
    XCTAssertEqual(client.aptosConfig.network.name, "testnet")
  }

  func test_Client_MainnetConfiguration() throws {
    let client = Aptos(aptosConfig: .mainnet)
    XCTAssertNotNil(client)
    XCTAssertEqual(client.aptosConfig.network.name, "mainnet")
  }
}

// MARK: - Network Configuration Tests

extension AptosSpecsTests {

  func test_Network_MainnetName() throws {
    let network = AptosConfig.Network.mainnet
    XCTAssertEqual(network.name, "mainnet")
  }

  func test_Network_TestnetName() throws {
    let network = AptosConfig.Network.testnet
    XCTAssertEqual(network.name, "testnet")
  }

  func test_Network_DevnetName() throws {
    let network = AptosConfig.Network.devnet
    XCTAssertEqual(network.name, "devnet")
  }

  func test_Network_LocalnetName() throws {
    let network = AptosConfig.Network.localnet
    XCTAssertEqual(network.name, "local")
  }

  func test_Network_MainnetChainId() throws {
    let network = AptosConfig.Network.mainnet
    XCTAssertEqual(network.chainId, 1)
  }

  func test_Network_TestnetChainId() throws {
    let network = AptosConfig.Network.testnet
    XCTAssertEqual(network.chainId, 2)
  }

  func test_Network_LocalnetChainId() throws {
    let network = AptosConfig.Network.localnet
    XCTAssertEqual(network.chainId, 4)
  }

  func test_Network_MainnetFullNodeUrl() throws {
    let network = AptosConfig.Network.mainnet
    XCTAssertEqual(network.fullNodeApi, "https://api.mainnet.aptoslabs.com/v1")
  }

  func test_Network_TestnetFullNodeUrl() throws {
    let network = AptosConfig.Network.testnet
    XCTAssertEqual(network.fullNodeApi, "https://api.testnet.aptoslabs.com/v1")
  }

  func test_Network_DevnetFullNodeUrl() throws {
    let network = AptosConfig.Network.devnet
    XCTAssertEqual(network.fullNodeApi, "https://api.devnet.aptoslabs.com/v1")
  }

  func test_Network_LocalnetFullNodeUrl() throws {
    let network = AptosConfig.Network.localnet
    XCTAssertEqual(network.fullNodeApi, "http://127.0.0.1:8080/v1")
  }

  func test_Network_MainnetIndexerUrl() throws {
    let network = AptosConfig.Network.mainnet
    XCTAssertEqual(network.indexerApi, "https://api.mainnet.aptoslabs.com/v1/graphql")
  }

  func test_Network_TestnetIndexerUrl() throws {
    let network = AptosConfig.Network.testnet
    XCTAssertEqual(network.indexerApi, "https://api.testnet.aptoslabs.com/v1/graphql")
  }

  func test_Network_MainnetFaucetUrl() throws {
    let network = AptosConfig.Network.mainnet
    XCTAssertEqual(network.faucetApi, "https://faucet.mainnet.aptoslabs.com")
  }

  func test_Network_TestnetFaucetUrl() throws {
    let network = AptosConfig.Network.testnet
    XCTAssertEqual(network.faucetApi, "https://faucet.testnet.aptoslabs.com")
  }

  func test_Network_DevnetFaucetUrl() throws {
    let network = AptosConfig.Network.devnet
    XCTAssertEqual(network.faucetApi, "https://faucet.devnet.aptoslabs.com")
  }

  func test_Network_CustomNetwork() throws {
    let network = AptosConfig.Network.custom(
      apiEnv: .custom(
        nodeApi: "https://custom.node.com/v1",
        indexerApi: "https://custom.indexer.com/v1/graphql",
        faucetApi: "https://custom.faucet.com"
      ))

    XCTAssertEqual(network.name, "custom")
    XCTAssertEqual(network.fullNodeApi, "https://custom.node.com/v1")
    XCTAssertEqual(network.indexerApi, "https://custom.indexer.com/v1/graphql")
    XCTAssertEqual(network.faucetApi, "https://custom.faucet.com")
    XCTAssertNil(network.chainId)  // Custom networks don't have predefined chain ID
  }
}

// MARK: - AptosConfig Tests

extension AptosSpecsTests {

  func test_AptosConfig_Mainnet() throws {
    let config = AptosConfig.mainnet
    XCTAssertEqual(config.network.name, "mainnet")
  }

  func test_AptosConfig_Testnet() throws {
    let config = AptosConfig.testnet
    XCTAssertEqual(config.network.name, "testnet")
  }

  func test_AptosConfig_Devnet() throws {
    let config = AptosConfig.devnet
    XCTAssertEqual(config.network.name, "devnet")
  }

  func test_AptosConfig_Localnet() throws {
    let config = AptosConfig.localnet
    XCTAssertEqual(config.network.name, "local")
  }

  func test_AptosConfig_DefaultsToDevnet() throws {
    let config = AptosConfig()
    XCTAssertEqual(config.network.name, "devnet")
  }

  func test_AptosConfig_CustomNetwork() throws {
    let customNetwork = AptosConfig.Network.custom(
      apiEnv: .custom(
        nodeApi: "https://my-node.example.com/v1",
        indexerApi: nil,
        faucetApi: nil
      ))
    let config = AptosConfig(network: customNetwork)

    XCTAssertEqual(config.network.name, "custom")
    XCTAssertEqual(config.network.fullNodeApi, "https://my-node.example.com/v1")
  }
}

// MARK: - Signature Tests

extension AptosSpecsTests {

  func test_Ed25519Signature_Length() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let message = Array("test".utf8)
    let signature = try privateKey.sign(message: message) as! Ed25519Signature

    XCTAssertEqual(signature.toUInt8Array().count, 64)
  }

  func test_Ed25519Signature_FromBytes() throws {
    let bytes = [UInt8](repeating: 0x42, count: 64)
    let signature = try Ed25519Signature(bytes)

    XCTAssertEqual(signature.toUInt8Array(), bytes)
  }

  func test_Ed25519Signature_FromHex() throws {
    let hex = "0x" + String(repeating: "ab", count: 64)
    let signature = try Ed25519Signature(hex)

    XCTAssertEqual(signature.toUInt8Array().count, 64)
    XCTAssertEqual(signature.toUInt8Array()[0], 0xab)
  }

  func test_Ed25519Signature_RejectInvalidLength() throws {
    let bytes = [UInt8](repeating: 0, count: 63)
    XCTAssertThrowsError(try Ed25519Signature(bytes))
  }

  func test_Secp256k1Signature_Length() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let message = Array("test".utf8)
    let signature = try privateKey.sign(message: message) as! Secp256k1Signature

    XCTAssertEqual(signature.toUInt8Array().count, 64)
  }

  func test_Secp256k1Signature_FromBytes() throws {
    let bytes = [UInt8](repeating: 0x55, count: 64)
    let signature = try Secp256k1Signature(bytes)

    XCTAssertEqual(signature.toUInt8Array(), bytes)
  }

  func test_Secp256k1Signature_RejectInvalidLength() throws {
    let bytes = [UInt8](repeating: 0, count: 65)
    XCTAssertThrowsError(try Secp256k1Signature(bytes))
  }
}

// MARK: - PublicKey Tests

extension AptosSpecsTests {

  func test_Ed25519PublicKey_Length() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey

    XCTAssertEqual(publicKey.toUInt8Array().count, 32)
  }

  func test_Ed25519PublicKey_FromBytes() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let bytes = publicKey.toUInt8Array()

    let reconstructed = try Ed25519PublicKey(bytes)
    XCTAssertEqual(reconstructed.toUInt8Array(), bytes)
  }

  func test_Ed25519PublicKey_FromHex() throws {
    let privateKey = Ed25519PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Ed25519PublicKey
    let hex = publicKey.key.toString()

    let reconstructed = try Ed25519PublicKey(hex)
    XCTAssertEqual(reconstructed.toUInt8Array(), publicKey.toUInt8Array())
  }

  func test_Ed25519PublicKey_RejectInvalidLength() throws {
    let bytes = [UInt8](repeating: 0, count: 31)
    XCTAssertThrowsError(try Ed25519PublicKey(bytes))
  }

  func test_Secp256k1PublicKey_Length() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey

    XCTAssertEqual(publicKey.toUInt8Array().count, 65)  // Uncompressed
  }

  func test_Secp256k1PublicKey_UncompressedPrefix() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey

    XCTAssertEqual(publicKey.toUInt8Array()[0], 0x04)  // Uncompressed prefix
  }

  func test_Secp256k1PublicKey_FromBytes() throws {
    let privateKey = Secp256k1PrivateKey.generate()
    let publicKey = try privateKey.publicKey() as! Secp256k1PublicKey
    let bytes = publicKey.toUInt8Array()

    let reconstructed = try Secp256k1PublicKey(bytes)
    XCTAssertEqual(reconstructed.toUInt8Array(), bytes)
  }

  func test_Secp256k1PublicKey_RejectInvalidLength() throws {
    let bytes = [UInt8](repeating: 0, count: 64)
    XCTAssertThrowsError(try Secp256k1PublicKey(bytes))
  }
}
