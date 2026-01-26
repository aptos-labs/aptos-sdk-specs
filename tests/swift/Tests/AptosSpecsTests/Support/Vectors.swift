import Foundation

/// Test vector loading utilities.
struct Vectors {

  struct AddressVector: Codable {
    let name: String
    let description: String?
    let input: String
    let expected: AddressExpected

    struct AddressExpected: Codable {
      let full_hex: String
      let short_string: String
    }
  }

  struct AddressVectorFile: Codable {
    let version: String
    let description: String
    let address_parsing: [AddressVector]?
  }

  static func getAddressParsingVectors() throws -> [AddressVector] {
    guard
      let url = Bundle.module.url(
        forResource: "addresses", withExtension: "json", subdirectory: "TestVectors")
    else {
      throw VectorError.fileNotFound("addresses")
    }
    let data = try Data(contentsOf: url)
    let file = try JSONDecoder().decode(AddressVectorFile.self, from: data)
    return file.address_parsing ?? []
  }

  enum VectorError: Error {
    case fileNotFound(String)
  }
}
