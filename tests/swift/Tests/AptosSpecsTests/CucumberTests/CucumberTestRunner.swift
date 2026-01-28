import CucumberSwift
import XCTest

/// Main Cucumber test runner for Aptos SDK behavioral specifications.
/// This class discovers and runs all Gherkin feature files.
@objc class CucumberTestRunner: NSObject {
    
    @objc static func setup() {
        // Configure Cucumber
        Cucumber.shared.parseIntoFeaturesAndScenarios()
        
        // Register step definitions
        AddressSteps.registerSteps()
        SerializationSteps.registerSteps()
        TypeTagSteps.registerSteps()
        Ed25519Steps.registerSteps()
        HashingSteps.registerSteps()
        AccountSteps.registerSteps()
        AuthKeySteps.registerSteps()
        MnemonicSteps.registerSteps()
        Secp256k1Steps.registerSteps()
    }
}

// MARK: - XCTest Integration

final class CucumberTests: XCTestCase {
    
    override class func setUp() {
        super.setUp()
        CucumberTestRunner.setup()
    }
    
    /// Run all Cucumber scenarios as XCTest test cases
    func testAllFeatures() {
        let cucumber = Cucumber.shared
        
        // Run all scenarios
        for feature in cucumber.features {
            for scenario in feature.scenarios {
                print("Running: \(feature.title) - \(scenario.title)")
                
                // Execute scenario
                scenario.steps.forEach { step in
                    step.execute()
                }
            }
        }
    }
}
