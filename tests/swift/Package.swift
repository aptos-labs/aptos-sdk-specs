// swift-tools-version:5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "AptosSpecs",
    platforms: [
        .iOS(.v15),
        .macOS(.v12),
        .tvOS(.v15)
    ],
    products: [
        .library(
            name: "AptosSpecs",
            targets: ["AptosSpecs"]
        )
    ],
    dependencies: [
        // Aptos Swift SDK
        .package(url: "https://github.com/ALCOVE-LAB/aptos-swift-sdk.git", branch: "main"),
        
        // Pin secp256k1 to a version compatible with the SDK
        .package(url: "https://github.com/GigaBitcoin/secp256k1.swift.git", exact: "0.17.0")
        
        // CucumberSwift for BDD testing
        // DISABLED: CucumberSwift has a bug - uses addTeardownBlock without @available annotation
        // See: CucumberTest.swift line 84 needs @available(macOS 10.15, iOS 13.0, tvOS 13.0, *)
        // When fixed upstream, uncomment this and the CucumberTests target below
        // , .package(url: "https://github.com/cucumberswift/CucumberSwift.git", from: "4.2.0")
    ],
    targets: [
        // Empty library target (test-only package)
        .target(
            name: "AptosSpecs",
            dependencies: [],
            path: "Sources/AptosSpecs"
        ),
        
        // Test target with XCTest-based tests (286 tests covering core functionality)
        // These tests manually implement Gherkin scenarios as XCTest methods
        .testTarget(
            name: "AptosSpecsTests",
            dependencies: [
                "AptosSpecs",
                .product(name: "Aptos", package: "aptos-swift-sdk")
            ],
            path: "Tests/AptosSpecsTests",
            exclude: ["CucumberTests"],
            resources: [
                // Include feature files from the shared features directory
                .copy("Features"),
                // Include test vectors
                .copy("TestVectors")
            ]
        )
        
        // CucumberSwift BDD test target (disabled until upstream bug is fixed)
        // Step definitions are prepared in Tests/AptosSpecsTests/CucumberTests/Steps/
        // , .testTarget(
        //     name: "CucumberTests",
        //     dependencies: [
        //         "AptosSpecs",
        //         .product(name: "Aptos", package: "aptos-swift-sdk"),
        //         .product(name: "CucumberSwift", package: "CucumberSwift")
        //     ],
        //     path: "Tests/AptosSpecsTests/CucumberTests",
        //     resources: [
        //         .copy("Features"),
        //         .copy("TestVectors")
        //     ]
        // )
    ]
)
