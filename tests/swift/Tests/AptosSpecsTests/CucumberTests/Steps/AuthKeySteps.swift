import Aptos
import Core
import CucumberSwift
import XCTest

/// Step definitions for authentication-key.feature
enum AuthKeySteps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("an Ed25519 public key") { _, _ in
            let privateKey = Ed25519PrivateKey.generate()
            do {
                world.ed25519PublicKey = try privateKey.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        Given("an Ed25519 public key from {string}") { match, _ in
            do {
                let privateKey = try Ed25519PrivateKey(match[1])
                world.ed25519PublicKey = try privateKey.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I derive the Ed25519 authentication key") { _, _ in
            guard let publicKey = world.ed25519PublicKey else { return }
            do {
                world.authKey = try publicKey.authKey()
            } catch {
                world.setError(error)
            }
        }
        
        When("I convert the authentication key to address") { _, _ in
            guard let authKey = world.authKey else { return }
            do {
                world.address = try authKey.derivedAddress()
            } catch {
                world.setError(error)
            }
        }
        
        When("I get the authentication key bytes") { _, _ in
            guard let authKey = world.authKey else { return }
            world.bytes = authKey.toUInt8Array()
        }
        
        When("I get the authentication key hex") { _, _ in
            guard let authKey = world.authKey else { return }
            world.stringResult = authKey.toString()
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the authentication key should have {int} bytes") { match, _ in
            guard let authKey = world.authKey, let expected = Int(match[1]) else { return }
            XCTAssertEqual(authKey.toUInt8Array().count, expected)
        }
        
        Then("the authentication key should equal the address bytes") { _, _ in
            guard let authKey = world.authKey, let address = world.address else { return }
            XCTAssertEqual(authKey.toUInt8Array(), address.toUInt8Array())
        }
        
        Then("the authentication key hex should start with {string}") { match, _ in
            guard let hex = world.stringResult else { return }
            XCTAssertTrue(hex.hasPrefix(match[1]))
        }
        
        Then("the authentication key hex should have length {int}") { match, _ in
            guard let hex = world.stringResult, let expected = Int(match[1]) else { return }
            XCTAssertEqual(hex.count, expected)
        }
        
        Then("deriving again should produce the same authentication key") { _, _ in
            guard let publicKey = world.ed25519PublicKey, let firstAuthKey = world.authKey else { return }
            do {
                let secondAuthKey = try publicKey.authKey()
                XCTAssertEqual(firstAuthKey.toUInt8Array(), secondAuthKey.toUInt8Array())
            } catch {
                XCTFail("Failed to derive auth key again: \(error)")
            }
        }
    }
}
