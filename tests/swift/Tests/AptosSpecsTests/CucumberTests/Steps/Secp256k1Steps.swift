import AptosSDK
import CucumberSwift
import XCTest

/// Step definitions for secp256k1.feature
enum Secp256k1Steps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a random Secp256k1 key pair") { _, _ in
            world.secp256k1PrivateKey = Secp256k1PrivateKey.generate()
            do {
                world.secp256k1PublicKey = try world.secp256k1PrivateKey?.publicKey() as? Secp256k1PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        Given("a Secp256k1 private key from seed {string}") { match, _ in
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
                world.secp256k1PrivateKey = try Secp256k1PrivateKey(seed)
                world.secp256k1PublicKey = try world.secp256k1PrivateKey?.publicKey() as? Secp256k1PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        Given("a Secp256k1 private key from hex {string}") { match, _ in
            do {
                world.secp256k1PrivateKey = try Secp256k1PrivateKey(match[1])
                world.secp256k1PublicKey = try world.secp256k1PrivateKey?.publicKey() as? Secp256k1PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I generate a Secp256k1 key pair") { _, _ in
            world.secp256k1PrivateKey = Secp256k1PrivateKey.generate()
            do {
                world.secp256k1PublicKey = try world.secp256k1PrivateKey?.publicKey() as? Secp256k1PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        When("I sign the message with Secp256k1") { _, _ in
            guard let privateKey = world.secp256k1PrivateKey, let message = world.message else { return }
            do {
                world.secp256k1Signature = try privateKey.sign(message: message) as? Secp256k1Signature
            } catch {
                world.setError(error)
            }
        }
        
        When("I verify the Secp256k1 signature") { _, _ in
            guard let publicKey = world.secp256k1PublicKey,
                  let signature = world.secp256k1Signature,
                  let message = world.message else { return }
            do {
                world.boolResult = try publicKey.verifySignature(message: message, signature: signature)
            } catch {
                world.setError(error)
            }
        }
        
        When("I derive the Secp256k1 public key") { _, _ in
            guard let privateKey = world.secp256k1PrivateKey else { return }
            do {
                world.secp256k1PublicKey = try privateKey.publicKey() as? Secp256k1PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        When("I export the Secp256k1 private key bytes") { _, _ in
            guard let privateKey = world.secp256k1PrivateKey else { return }
            world.bytes = privateKey.toUInt8Array()
        }
        
        When("I export the Secp256k1 public key bytes") { _, _ in
            guard let publicKey = world.secp256k1PublicKey else { return }
            world.bytes = publicKey.toUInt8Array()
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the Secp256k1 private key should have {int} bytes") { match, _ in
            guard let privateKey = world.secp256k1PrivateKey, let expected = Int(match[1]) else { return }
            XCTAssertEqual(privateKey.toUInt8Array().count, expected)
        }
        
        Then("the Secp256k1 public key should have {int} bytes") { match, _ in
            guard let publicKey = world.secp256k1PublicKey, let expected = Int(match[1]) else { return }
            XCTAssertEqual(publicKey.toUInt8Array().count, expected)
        }
        
        Then("the Secp256k1 signature should have {int} bytes") { match, _ in
            guard let signature = world.secp256k1Signature, let expected = Int(match[1]) else { return }
            XCTAssertEqual(signature.toUInt8Array().count, expected)
        }
        
        Then("the Secp256k1 signature should be valid") { _, _ in
            XCTAssertTrue(world.boolResult ?? false)
        }
        
        Then("the Secp256k1 signature should be invalid") { _, _ in
            XCTAssertFalse(world.boolResult ?? true)
        }
        
        Then("the Secp256k1 public key should start with 0x04") { _, _ in
            guard let publicKey = world.secp256k1PublicKey else { return }
            let bytes = publicKey.toUInt8Array()
            XCTAssertEqual(bytes.first, 0x04, "Uncompressed public key should start with 0x04")
        }
        
        Then("the Secp256k1 key pair creation should fail") { _, _ in
            XCTAssertNotNil(world.error)
        }
    }
}
