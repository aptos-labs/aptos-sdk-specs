import Aptos
import BCS
import Core
import CucumberSwift
import XCTest

/// Step definitions for type-tags.feature
enum TypeTagSteps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a type string {string}") { match, _ in
            world.typeTagString = match[1]
        }
        
        Given("a primitive type {word}") { match, _ in
            switch match[1] {
            case "bool": world.typeTag = .Bool
            case "u8": world.typeTag = .U8
            case "u16": world.typeTag = .U16
            case "u32": world.typeTag = .U32
            case "u64": world.typeTag = .U64
            case "u128": world.typeTag = .U128
            case "u256": world.typeTag = .U256
            case "address": world.typeTag = .Address
            case "signer": world.typeTag = .Signer
            default: world.typeTag = nil
            }
        }
        
        Given("a vector type of {word}") { match, _ in
            let inner: TypeTag
            switch match[1] {
            case "u8": inner = .U8
            case "u64": inner = .U64
            case "bool": inner = .Bool
            case "address": inner = .Address
            default: inner = .U8
            }
            world.typeTag = .Vector(inner)
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I parse it as a TypeTag") { _, _ in
            guard let typeString = world.typeTagString else {
                world.setError(NSError(domain: "Test", code: 1, userInfo: [NSLocalizedDescriptionKey: "No type string set"]))
                return
            }
            do {
                world.typeTag = try TypeTag.parseTypeTag(typeString)
                world.clearError()
            } catch {
                world.setError(error)
            }
        }
        
        When("I format the TypeTag") { _, _ in
            guard let typeTag = world.typeTag else { return }
            world.stringResult = typeTag.toString()
        }
        
        When("I BCS serialize the TypeTag") { _, _ in
            guard let typeTag = world.typeTag else { return }
            do {
                world.serializedBytes = try typeTag.bcsToBytes()
            } catch {
                world.setError(error)
            }
        }
        
        When("I BCS deserialize the TypeTag bytes") { _, _ in
            guard let bytes = world.serializedBytes else { return }
            do {
                let deserializer = BcsDeserializer(input: bytes)
                world.typeTag = try TypeTag.deserialize(deserializer: deserializer)
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the TypeTag should be valid") { _, _ in
            XCTAssertNotNil(world.typeTag)
            XCTAssertNil(world.error)
        }
        
        Then("parsing the TypeTag should fail") { _, _ in
            XCTAssertNotNil(world.error)
        }
        
        Then("the TypeTag should be a struct") { _, _ in
            guard let typeTag = world.typeTag else {
                XCTFail("No TypeTag set")
                return
            }
            XCTAssertTrue(typeTag.isStruct)
        }
        
        Then("the TypeTag should be a vector") { _, _ in
            guard let typeTag = world.typeTag else {
                XCTFail("No TypeTag set")
                return
            }
            if case .Vector = typeTag {
                // Success
            } else {
                XCTFail("TypeTag should be a vector")
            }
        }
        
        Then("the TypeTag should be a primitive") { _, _ in
            guard let typeTag = world.typeTag else {
                XCTFail("No TypeTag set")
                return
            }
            XCTAssertFalse(typeTag.isStruct)
            if case .Vector = typeTag {
                XCTFail("TypeTag should not be a vector")
            }
        }
        
        Then("the struct address should be {string}") { match, _ in
            guard let typeTag = world.typeTag else { return }
            if case .Struct(let structTag) = typeTag {
                XCTAssertEqual(structTag.address.toString().lowercased(), match[1].lowercased())
            } else {
                XCTFail("TypeTag is not a struct")
            }
        }
        
        Then("the struct module should be {string}") { match, _ in
            guard let typeTag = world.typeTag else { return }
            if case .Struct(let structTag) = typeTag {
                XCTAssertEqual(structTag.moduleName.identifier, match[1])
            } else {
                XCTFail("TypeTag is not a struct")
            }
        }
        
        Then("the struct name should be {string}") { match, _ in
            guard let typeTag = world.typeTag else { return }
            if case .Struct(let structTag) = typeTag {
                XCTAssertEqual(structTag.name.identifier, match[1])
            } else {
                XCTFail("TypeTag is not a struct")
            }
        }
        
        Then("the TypeTag string should be {string}") { match, _ in
            XCTAssertEqual(world.stringResult, match[1])
        }
        
        Then("the TypeTag BCS round-trip should match") { _, _ in
            guard let original = world.typeTag else { return }
            do {
                let bytes = try original.bcsToBytes()
                let deserializer = BcsDeserializer(input: bytes)
                let result = try TypeTag.deserialize(deserializer: deserializer)
                XCTAssertEqual(result, original)
            } catch {
                XCTFail("BCS round-trip failed: \(error)")
            }
        }
    }
}
