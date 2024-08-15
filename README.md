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
