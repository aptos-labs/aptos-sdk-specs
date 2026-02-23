import AptosSDK
import CryptoKit
import CucumberSwift
import XCTest

/// Step definitions for hashing.feature
enum HashingSteps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("input bytes {string}") { match, _ in
            let hex = match[1].replacingOccurrences(of: "0x", with: "")
            if hex.isEmpty {
                world.bytes = []
            } else {
                var bytes = [UInt8]()
                var index = hex.startIndex
                while index < hex.endIndex {
                    let nextIndex = hex.index(index, offsetBy: 2, limitedBy: hex.endIndex) ?? hex.endIndex
                    if let byte = UInt8(hex[index..<nextIndex], radix: 16) {
                        bytes.append(byte)
                    }
                    index = nextIndex
                }
                world.bytes = bytes
            }
        }
        
        Given("input string {string}") { match, _ in
            world.bytes = Array(match[1].utf8)
        }
        
        Given("empty input") { _, _ in
            world.bytes = []
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I compute SHA3-256 hash") { _, _ in
            guard let bytes = world.bytes else { return }
            world.hashResult = CryptoSwift.Digest.sha3(bytes, variant: .sha256)
        }
        
        When("I compute SHA2-256 hash") { _, _ in
            guard let bytes = world.bytes else { return }
            let digest = CryptoKit.SHA256.hash(data: Data(bytes))
            world.hashResult = Array(digest)
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the hash should be {string}") { match, _ in
            guard let hash = world.hashResult else {
                XCTFail("No hash result")
                return
            }
            let expectedHex = match[1].replacingOccurrences(of: "0x", with: "").lowercased()
            let actualHex = hash.map { String(format: "%02x", $0) }.joined()
            XCTAssertEqual(actualHex, expectedHex)
        }
        
        Then("the hash should have {int} bytes") { match, _ in
            guard let hash = world.hashResult, let expected = Int(match[1]) else { return }
            XCTAssertEqual(hash.count, expected)
        }
        
        Then("hashing again should produce the same result") { _, _ in
            guard let bytes = world.bytes, let firstHash = world.hashResult else { return }
            let secondHash = CryptoSwift.Digest.sha3(bytes, variant: .sha256)
            XCTAssertEqual(firstHash, secondHash)
        }
    }
}
