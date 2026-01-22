// swift-tools-version:5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "AptosSpecs",
    platforms: [
        .iOS(.v13),
        .macOS(.v10_15),
        .tvOS(.v13)
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
        .package(url: "https://github.com/GigaBitcoin/secp256k1.swift.git", exact: "0.17.0"),
    ],
    targets: [
        // Empty library target (test-only package)
        .target(
            name: "AptosSpecs",
            dependencies: [],
            path: "Sources/AptosSpecs"
        ),
        
        // Test target with step definitions
        .testTarget(
            name: "AptosSpecsTests",
            dependencies: [
                "AptosSpecs",
                .product(name: "Aptos", package: "aptos-swift-sdk"),
            ],
            path: "Tests/AptosSpecsTests",
            resources: [
                // Include feature files from the shared features directory
                .copy("Features"),
                // Include test vectors
                .copy("TestVectors")
            ]
        )
    ]
)
