import Aptos
import BCS
import Core
import CucumberSwift
import XCTest

/// Step definitions for serialization.feature
enum SerializationSteps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a boolean value {word}") { match, _ in
            world.boolResult = match[1] == "true"
        }
        
        Given("a u8 value {int}") { match, _ in
            if let value = UInt8(match[1]) {
                world.bytes = [value]
            }
        }
        
        Given("a u16 value {int}") { match, _ in
            if let value = UInt16(match[1]) {
                var bytes = [UInt8](repeating: 0, count: 2)
                bytes[0] = UInt8(value & 0xFF)
                bytes[1] = UInt8((value >> 8) & 0xFF)
                world.bytes = bytes
            }
        }
        
        Given("a u32 value {int}") { match, _ in
            if let value = UInt32(match[1]) {
                var bytes = [UInt8](repeating: 0, count: 4)
                for i in 0..<4 {
                    bytes[i] = UInt8((value >> (i * 8)) & 0xFF)
                }
                world.bytes = bytes
            }
        }
        
        Given("a u64 value {int}") { match, _ in
            if let value = UInt64(match[1]) {
                var bytes = [UInt8](repeating: 0, count: 8)
                for i in 0..<8 {
                    bytes[i] = UInt8((value >> (i * 8)) & 0xFF)
                }
                world.bytes = bytes
            }
        }
        
        Given("a string {string}") { match, _ in
            world.stringResult = match[1]
        }
        
        Given("an empty byte array") { _, _ in
            world.bytes = []
        }
        
        Given("bytes {string}") { match, _ in
            // Parse hex string into bytes
            let hex = match[1].replacingOccurrences(of: "0x", with: "")
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
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I BCS serialize the boolean") { _, _ in
            guard let value = world.boolResult else { return }
            let serializer = BcsSerializer()
            do {
                try serializer.serializeBool(value: value)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS serialize the u8") { _, _ in
            guard let bytes = world.bytes, let value = bytes.first else { return }
            let serializer = BcsSerializer()
            do {
                try serializer.serializeU8(value: value)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS serialize the u16") { _, _ in
            guard let bytes = world.bytes, bytes.count >= 2 else { return }
            let value = UInt16(bytes[0]) | (UInt16(bytes[1]) << 8)
            let serializer = BcsSerializer()
            do {
                try serializer.serializeU16(value: value)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS serialize the u32") { _, _ in
            guard let bytes = world.bytes, bytes.count >= 4 else { return }
            var value: UInt32 = 0
            for i in 0..<4 {
                value |= UInt32(bytes[i]) << (i * 8)
            }
            let serializer = BcsSerializer()
            do {
                try serializer.serializeU32(value: value)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS serialize the u64") { _, _ in
            guard let bytes = world.bytes, bytes.count >= 8 else { return }
            var value: UInt64 = 0
            for i in 0..<8 {
                value |= UInt64(bytes[i]) << (i * 8)
            }
            let serializer = BcsSerializer()
            do {
                try serializer.serializeU64(value: value)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS serialize the string") { _, _ in
            guard let value = world.stringResult else { return }
            let serializer = BcsSerializer()
            do {
                try serializer.serializeStr(value: value)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS serialize the bytes") { _, _ in
            guard let bytes = world.bytes else { return }
            let serializer = BcsSerializer()
            do {
                try serializer.serializeBytes(value: bytes)
                world.serializedBytes = serializer.toUInt8Array()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS deserialize a boolean from {string}") { match, _ in
            let hex = match[1].replacingOccurrences(of: "0x", with: "")
            guard let byte = UInt8(hex, radix: 16) else { return }
            let deserializer = BcsDeserializer(input: [byte])
            do {
                world.boolResult = try deserializer.deserializeBool()
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the serialized bytes should be {string}") { match, _ in
            guard let bytes = world.serializedBytes else {
                XCTFail("No serialized bytes")
                return
            }
            let expectedHex = match[1].replacingOccurrences(of: "0x", with: "").lowercased()
            let actualHex = bytes.map { String(format: "%02x", $0) }.joined()
            XCTAssertEqual(actualHex, expectedHex)
        }
        
        Then("the first byte should be {int}") { match, _ in
            guard let bytes = world.serializedBytes, let expected = UInt8(match[1]) else { return }
            XCTAssertEqual(bytes.first, expected)
        }
        
        Then("deserialization should succeed") { _, _ in
            XCTAssertNil(world.error)
        }
        
        Then("deserialization should fail") { _, _ in
            XCTAssertNotNil(world.error)
        }
        
        Then("the boolean result should be {word}") { match, _ in
            let expected = match[1] == "true"
            XCTAssertEqual(world.boolResult, expected)
        }
    }
}
