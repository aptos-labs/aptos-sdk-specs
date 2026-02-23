import AptosSDK
import CucumberSwift
import XCTest

/// Step definitions for ed25519.feature
enum Ed25519Steps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a random Ed25519 key pair") { _, _ in
            world.ed25519PrivateKey = Ed25519PrivateKey.generate()
            do {
                world.ed25519PublicKey = try world.ed25519PrivateKey?.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        Given("an Ed25519 private key from seed {string}") { match, _ in
            let hex = match[1].replacingOccurrences(of: "0x", with: "")
            var seed = [UInt8]()
            var index = hex.startIndex
            while index < hex.endIndex {
                let nextIndex = hex.index(index, offsetBy: 2, limitedBy: hex.endIndex) ?? hex.endIndex
                if let byte = UInt8(hex[index..<nextIndex], radix: 16) {
                    seed.append(byte)
                }
                index = nextIndex
            }
            // Pad or truncate to 32 bytes
            while seed.count < 32 { seed.append(0) }
            if seed.count > 32 { seed = Array(seed.prefix(32)) }
            
            do {
                world.ed25519PrivateKey = try Ed25519PrivateKey(seed)
                world.ed25519PublicKey = try world.ed25519PrivateKey?.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        Given("an Ed25519 private key from hex {string}") { match, _ in
            do {
                world.ed25519PrivateKey = try Ed25519PrivateKey(match[1])
                world.ed25519PublicKey = try world.ed25519PrivateKey?.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        Given("a message {string}") { match, _ in
            world.message = Array(match[1].utf8)
        }
        
        Given("an empty message") { _, _ in
            world.message = []
        }
        
        Given("a {int}-byte message") { match, _ in
            if let size = Int(match[1]) {
                world.message = [UInt8](repeating: 0xAB, count: size)
            }
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I generate an Ed25519 key pair") { _, _ in
            world.ed25519PrivateKey = Ed25519PrivateKey.generate()
            do {
                world.ed25519PublicKey = try world.ed25519PrivateKey?.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        When("I sign the message") { _, _ in
            guard let privateKey = world.ed25519PrivateKey, let message = world.message else { return }
            do {
                world.ed25519Signature = try privateKey.sign(message: message) as? Ed25519Signature
            } catch {
                world.setError(error)
            }
        }
        
        When("I verify the signature") { _, _ in
            guard let publicKey = world.ed25519PublicKey,
                  let signature = world.ed25519Signature,
                  let message = world.message else { return }
            do {
                world.boolResult = try publicKey.verifySignature(message: message, signature: signature)
            } catch {
                world.setError(error)
            }
        }
        
        When("I derive the public key") { _, _ in
            guard let privateKey = world.ed25519PrivateKey else { return }
            do {
                world.ed25519PublicKey = try privateKey.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        When("I derive the authentication key") { _, _ in
            guard let publicKey = world.ed25519PublicKey else { return }
            do {
                world.authKey = try publicKey.authKey()
            } catch {
                world.setError(error)
            }
        }
        
        When("I export the private key bytes") { _, _ in
            guard let privateKey = world.ed25519PrivateKey else { return }
            world.bytes = privateKey.toUInt8Array()
        }
        
        When("I export the public key bytes") { _, _ in
            guard let publicKey = world.ed25519PublicKey else { return }
            world.bytes = publicKey.toUInt8Array()
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the Ed25519 private key should have {int} bytes") { match, _ in
            guard let privateKey = world.ed25519PrivateKey, let expected = Int(match[1]) else { return }
            XCTAssertEqual(privateKey.toUInt8Array().count, expected)
        }
        
        Then("the Ed25519 public key should have {int} bytes") { match, _ in
            guard let publicKey = world.ed25519PublicKey, let expected = Int(match[1]) else { return }
            XCTAssertEqual(publicKey.toUInt8Array().count, expected)
        }
        
        Then("the Ed25519 signature should have {int} bytes") { match, _ in
            guard let signature = world.ed25519Signature, let expected = Int(match[1]) else { return }
            XCTAssertEqual(signature.toUInt8Array().count, expected)
        }
        
        Then("the signature should be valid") { _, _ in
            XCTAssertTrue(world.boolResult ?? false, "Signature should be valid")
        }
        
        Then("the signature should be invalid") { _, _ in
            XCTAssertFalse(world.boolResult ?? true, "Signature should be invalid")
        }
        
        Then("the authentication key should have {int} bytes") { match, _ in
            guard let authKey = world.authKey, let expected = Int(match[1]) else { return }
            XCTAssertEqual(authKey.toUInt8Array().count, expected)
        }
        
        Then("the key pair creation should fail") { _, _ in
            XCTAssertNotNil(world.error, "Key pair creation should have failed")
        }
        
        Then("the exported bytes should have length {int}") { match, _ in
            guard let bytes = world.bytes, let expected = Int(match[1]) else { return }
            XCTAssertEqual(bytes.count, expected)
        }
    }
}
