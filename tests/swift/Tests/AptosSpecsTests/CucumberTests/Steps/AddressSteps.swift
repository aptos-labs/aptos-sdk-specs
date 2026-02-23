import AptosSDK
import CucumberSwift
import XCTest

/// Step definitions for address.feature
enum AddressSteps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a hex string {string}") { match, _ in
            world.reset()
            world.hexString = match[1]
        }
        
        Given("an address string {string}") { match, _ in
            world.hexString = match[1]
        }
        
        Given("the address {string}") { match, _ in
            do {
                world.address = try AccountAddress.fromString(match[1])
            } catch {
                world.setError(error)
            }
        }
        
        Given("addresses {string} and {string}") { match, _ in
            do {
                world.address = try AccountAddress.fromString(match[1])
                world.address2 = try AccountAddress.fromString(match[2])
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I parse it as an address") { _, _ in
            guard let hexString = world.hexString else {
                world.setError(NSError(domain: "Test", code: 1, userInfo: [NSLocalizedDescriptionKey: "No hex string set"]))
                return
            }
            do {
                world.address = try AccountAddress.fromString(hexString)
                world.clearError()
            } catch {
                world.setError(error)
            }
        }
        
        When("I format it to full hex") { _, _ in
            guard let address = world.address else { return }
            world.stringResult = address.toStringLong()
        }
        
        When("I format it to short string") { _, _ in
            guard let address = world.address else { return }
            world.stringResult = address.toString()
        }
        
        When("I BCS serialize the address") { _, _ in
            guard let address = world.address else { return }
            do {
                world.serializedBytes = try address.bcsToBytes()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS deserialize the bytes") { _, _ in
            guard let bytes = world.serializedBytes else { return }
            do {
                let deserializer = BcsDeserializer(input: bytes)
                world.address = try AccountAddress.deserialize(deserializer: deserializer)
            } catch {
                world.setError(error)
            }
        }
        
        When("I compare them") { _, _ in
            guard let addr1 = world.address, let addr2 = world.address2 else { return }
            world.boolResult = addr1.equals(addr2)
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the address should be valid") { _, _ in
            XCTAssertNotNil(world.address, "Address should be valid")
            XCTAssertNil(world.error, "No error should occur")
        }
        
        Then("parsing should fail") { _, _ in
            XCTAssertNotNil(world.error, "Parsing should have failed")
        }
        
        Then("it should throw an error") { _, _ in
            XCTAssertNotNil(world.error, "An error should have been thrown")
        }
        
        Then("the result should be {string}") { match, _ in
            XCTAssertEqual(world.stringResult?.lowercased(), match[1].lowercased())
        }
        
        Then("they should be equal") { _, _ in
            XCTAssertTrue(world.boolResult ?? false, "Addresses should be equal")
        }
        
        Then("they should not be equal") { _, _ in
            XCTAssertFalse(world.boolResult ?? true, "Addresses should not be equal")
        }
        
        Then("the serialized bytes should have length {int}") { match, _ in
            guard let bytes = world.serializedBytes, let length = Int(match[1]) else { return }
            XCTAssertEqual(bytes.count, length)
        }
        
        Then("the result should match the original") { _, _ in
            guard let original = world.hexString else { return }
            guard let result = world.address else { return }
            do {
                let expected = try AccountAddress.fromString(original)
                XCTAssertEqual(result, expected)
            } catch {
                XCTFail("Failed to parse original: \(error)")
            }
        }
        
        Then("the address should have byte {int} equal to {int}") { match, _ in
            guard let address = world.address else { return }
            guard let byteIndex = Int(match[1]), let expectedValue = UInt8(match[2]) else { return }
            let bytes = address.toUInt8Array()
            XCTAssertEqual(bytes[byteIndex], expectedValue)
        }
        
        // =============================================================================
        // Address Constants
        // =============================================================================
        
        Given("the ZERO address constant") { _, _ in
            world.address = AccountAddress.ZERO
        }
        
        Given("the ONE address constant") { _, _ in
            world.address = AccountAddress.ONE
        }
        
        Given("the THREE address constant") { _, _ in
            world.address = AccountAddress.THREE
        }
        
        Given("the FOUR address constant") { _, _ in
            world.address = AccountAddress.FOUR
        }
        
        Then("it should be a special address") { _, _ in
            guard let address = world.address else { return }
            XCTAssertTrue(address.isSpecial())
        }
    }
}
