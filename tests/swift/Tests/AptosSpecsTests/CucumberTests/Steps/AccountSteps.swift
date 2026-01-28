import Aptos
import Core
import CucumberSwift
import XCTest

/// Step definitions for single-key.feature and account management
enum AccountSteps {
    
    static func registerSteps() {
        let world = TestWorld.shared
        
        // =============================================================================
        // Given Steps
        // =============================================================================
        
        Given("a random Ed25519 account") { _, _ in
            world.account = Account.generate()
        }
        
        Given("a random Secp256k1 account") { _, _ in
            world.account = Account.generate(scheme: .secp256k1Ecdsa)
        }
        
        Given("an Ed25519 account from private key {string}") { match, _ in
            do {
                let privateKey = try Ed25519PrivateKey(match[1])
                world.ed25519Account = try Account.Ed25519Account(privateKey: privateKey)
                world.account = world.ed25519Account
            } catch {
                world.setError(error)
            }
        }
        
        Given("a SingleKey Ed25519 account") { _, _ in
            world.account = Account.generate(scheme: .ed25519)
        }
        
        Given("a SingleKey Secp256k1 account") { _, _ in
            world.account = Account.generate(scheme: .secp256k1Ecdsa)
        }
        
        // =============================================================================
        // When Steps
        // =============================================================================
        
        When("I generate a random account") { _, _ in
            world.account = Account.generate()
        }
        
        When("I get the account address") { _, _ in
            guard let account = world.account else { return }
            world.address = account.accountAddress
        }
        
        When("I get the account public key") { _, _ in
            guard let account = world.account else { return }
            world.bytes = account.publicKey.toUInt8Array()
        }
        
        When("I sign with the account") { _, _ in
            guard let account = world.account, let message = world.message else { return }
            do {
                let signature = try account.sign(message: message)
                world.boolResult = try account.verifySignature(message: message, signature: signature)
            } catch {
                world.setError(error)
            }
        }
        
        // =============================================================================
        // Then Steps
        // =============================================================================
        
        Then("the account should have a valid address") { _, _ in
            guard let account = world.account else {
                XCTFail("No account created")
                return
            }
            XCTAssertEqual(account.accountAddress.toUInt8Array().count, 32)
        }
        
        Then("the account address should be {int} bytes") { match, _ in
            guard let account = world.account, let expected = Int(match[1]) else { return }
            XCTAssertEqual(account.accountAddress.toUInt8Array().count, expected)
        }
        
        Then("the account public key should be {int} bytes") { match, _ in
            guard let account = world.account, let expected = Int(match[1]) else { return }
            XCTAssertEqual(account.publicKey.toUInt8Array().count, expected)
        }
        
        Then("the account signing scheme should be {word}") { match, _ in
            guard let account = world.account else { return }
            switch match[1] {
            case "ed25519":
                XCTAssertEqual(account.signingScheme, .ed25519)
            case "singleKey":
                XCTAssertEqual(account.signingScheme, .singleKey)
            default:
                XCTFail("Unknown signing scheme: \(match[1])")
            }
        }
        
        Then("signing should succeed") { _, _ in
            XCTAssertTrue(world.boolResult ?? false)
        }
        
        Then("the signature should verify") { _, _ in
            XCTAssertTrue(world.boolResult ?? false)
        }
    }
}
