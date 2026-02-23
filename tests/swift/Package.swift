// swift-tools-version:6.0
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "AptosSpecs",
    platforms: [
        .iOS(.v17),
        .macOS(.v14),
        .tvOS(.v17)
    ],
    products: [
        .library(
            name: "AptosSpecs",
            targets: ["AptosSpecs"]
        )
    ],
    dependencies: [
        // Official Aptos Swift SDK (aptos-labs)
        .package(url: "https://github.com/aptos-labs/aptos-swift-sdk.git", branch: "main")

        // CucumberSwift for BDD testing
        // DISABLED: CucumberSwift has a bug - uses addTeardownBlock without @available annotation
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

        // Test target with XCTest-based tests covering core functionality
        // These tests manually implement Gherkin scenarios as XCTest methods
        .testTarget(
            name: "AptosSpecsTests",
            dependencies: [
                "AptosSpecs",
                .product(name: "AptosSDK", package: "aptos-swift-sdk")
            ],
            path: "Tests/AptosSpecsTests",
            exclude: ["CucumberTests"],
            resources: [
                .copy("Features"),
                .copy("TestVectors")
            ]
        )

        // CucumberSwift BDD test target (disabled until upstream bug is fixed)
        // Step definitions are prepared in Tests/AptosSpecsTests/CucumberTests/Steps/
        // , .testTarget(
        //     name: "CucumberTests",
        //     dependencies: [
        //         "AptosSpecs",
        //         .product(name: "AptosSDK", package: "aptos-swift-sdk"),
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
