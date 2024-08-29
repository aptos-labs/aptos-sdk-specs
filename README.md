# Aptos SDK Specs

This project is a collection of specifications for SDKs for Aptos. The main purposes of this project are:

* Define a common set of features for SDKs
* Provide a common set of tests for SDKs
* Increase consistency across SDKs
* Increase speed of feature development for SDKs

## Overview

We are using [Cucumber](https://cucumber.io/docs/guides/overview/) for Behavioral testing across multiple languages.  
It uses Gherkin as the language for specification.

The project is broken down into the following sections:

* [Required Features](./features/required/README.md) - These features are required to have a minimally working SDK for
  most use cases.
* [Preferred Features](./features/preferred/README.md) - These features are required to have a fully featured SDK
  including all main features.
* [Optional Features](./features/optional/README.md) - These features are optional, and mostly provide quality of life
  improvements.

## Features Support

Note: This is currently in progress, and does not have all features specified.

Do you have an SDK that you maintain?  Please feel free to open a PR, and add your specification support here!

| Status         | Emoji | Details                                     |
|----------------|-------|---------------------------------------------|
| Supported      | ✅ | Currently supported and passing specifications |
| Supported, not specified | ▶️ | Currently supported, no specification yet |
| Limited support | 🔺 | Supported, but not fully featured |
| Not Supported | ❌ | Currently not supported |
| Unknown | ❓ | Unknown if SDK supports this feature |

| Feature | [TypeScript](https://aptos.dev/en/build/sdks/ts-sdk) | [Go](https://aptos.dev/en/build/sdks/go-sdk) | [Python](https://aptos.dev/en/build/sdks/python-sdk) | [Rust](https://aptos.dev/en/build/sdks/rust-sdk) | [C#](https://aptos.dev/en/build/sdks/unity-sdk) | [C++](https://aptos.dev/en/build/sdks/cpp-sdk) | [Kaptos(Kotlin)](https://aptos.dev/en/build/sdks/kotlin-sdk) | [Alcove(Swift)](https://aptos.dev/en/build/sdks/community-sdks/swift-sdk) |
|--|--|--|--|--|--|--|--|--|
| BCS Encoding | [✅](https://github.com/aptos-labs/aptos-ts-sdk/blob/main/tests/features/bcs_serialization.feature) | [✅](https://github.com/aptos-labs/aptos-go-sdk/blob/main/features/bcs_serialization.feature) | [✅](https://github.com/aptos-labs/aptos-python-sdk/blob/main/features/bcs_serialization.feature) | ▶️ | ▶️ | ▶️ | ▶️ | ❓|
| BCS Decoding | [✅](https://github.com/aptos-labs/aptos-ts-sdk/blob/main/tests/features/bcs_deserialization.feature) | [✅](https://github.com/aptos-labs/aptos-go-sdk/blob/main/features/bcs_deserialization.feature) | [✅](https://github.com/aptos-labs/aptos-python-sdk/blob/main/features/bcs_deserialization.feature) | ▶️ | ▶️ | ▶️ | ▶️ | ❓|
