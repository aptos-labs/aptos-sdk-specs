import Aptos
import Core
import CucumberSwift
import XCTest

/// Step definitions for mnemonic-derivation.feature
enum MnemonicSteps {
    
    // Test mnemonic - DO NOT use in production
    static let testMnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a valid BIP-39 mnemonic") { _, _ in
            world.mnemonic = testMnemonic
        }
        
        Given("a mnemonic {string}") { match, _ in
            world.mnemonic = match[1]
        }
        
        Given("the standard Aptos Ed25519 derivation path") { _, _ in
            world.derivationPath = "m/44'/637'/0'/0'/0'"
        }
        
        Given("the derivation path {string}") { match, _ in
            world.derivationPath = match[1]
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I derive an Ed25519 private key from the mnemonic") { _, _ in
            guard let mnemonic = world.mnemonic, let path = world.derivationPath else { return }
            do {
                world.ed25519PrivateKey = try Ed25519PrivateKey.fromDerivationPath(path: path, mnemonic: mnemonic)
                world.ed25519PublicKey = try world.ed25519PrivateKey?.publicKey() as? Ed25519PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        When("I derive a Secp256k1 private key from the mnemonic") { _, _ in
            guard let mnemonic = world.mnemonic, let path = world.derivationPath else { return }
            do {
                world.secp256k1PrivateKey = try Secp256k1PrivateKey.fromDerivationPath(path: path, mnemonic: mnemonic)
                world.secp256k1PublicKey = try world.secp256k1PrivateKey?.publicKey() as? Secp256k1PublicKey
            } catch {
                world.setError(error)
            }
        }
        
        When("I derive an account from the mnemonic with path {string}") { match, _ in
            guard let mnemonic = world.mnemonic else { return }
            do {
                world.account = try Account.fromDerivationPath(match[1], mnemonic: mnemonic)
            } catch {
                world.setError(error)
            }
        }
        
        When("I derive a SingleKey account from the mnemonic") { _, _ in
            guard let mnemonic = world.mnemonic, let path = world.derivationPath else { return }
            do {
                world.account = try Account.fromDerivationPath(path, mnemonic: mnemonic, scheme: .secp256k1Ecdsa)
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the Ed25519 key derivation should succeed") { _, _ in
            XCTAssertNotNil(world.ed25519PrivateKey)
            XCTAssertNil(world.error)
        }
        
        Then("the Secp256k1 key derivation should succeed") { _, _ in
            XCTAssertNotNil(world.secp256k1PrivateKey)
            XCTAssertNil(world.error)
        }
        
        Then("the key derivation should fail") { _, _ in
            XCTAssertNotNil(world.error)
        }
        
        Then("deriving the same path again should produce the same key") { _, _ in
            guard let mnemonic = world.mnemonic, let path = world.derivationPath else { return }
            guard let firstKey = world.ed25519PrivateKey else { return }
            do {
                let secondKey = try Ed25519PrivateKey.fromDerivationPath(path: path, mnemonic: mnemonic)
                XCTAssertEqual(firstKey.toUInt8Array(), secondKey.toUInt8Array())
            } catch {
                XCTFail("Failed to derive key again: \(error)")
            }
        }
        
        Then("the account derivation should succeed") { _, _ in
            XCTAssertNotNil(world.account)
            XCTAssertNil(world.error)
        }
    }
}
