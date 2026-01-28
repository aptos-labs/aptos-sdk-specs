# Aptos Swift SDK Behavioral Specification Tests
# Uses CucumberSwift with XCTest

.PHONY: all build test test-xctest test-cucumber test-required test-preferred test-optional \
        test-core-types test-cryptography test-accounts test-transactions \
        test-api-clients test-advanced clean setup link-features format lint help

# Default target
all: test

# Setup - resolve dependencies and link feature files
setup:
	swift package resolve
	$(MAKE) link-features

# Link feature files from shared directory
link-features:
	@echo "Linking feature files..."
	@mkdir -p Tests/AptosSpecsTests/Features
	@rm -rf Tests/AptosSpecsTests/Features/*
	@for dir in ../../features/*/; do \
		if [ -d "$$dir" ]; then \
			cp -r "$$dir" Tests/AptosSpecsTests/Features/; \
		fi \
	done
	@mkdir -p Tests/AptosSpecsTests/CucumberTests/Features
	@rm -rf Tests/AptosSpecsTests/CucumberTests/Features/*
	@for dir in ../../features/*/; do \
		if [ -d "$$dir" ]; then \
			cp -r "$$dir" Tests/AptosSpecsTests/CucumberTests/Features/; \
		fi \
	done
	@echo "Linking test vectors..."
	@mkdir -p Tests/AptosSpecsTests/TestVectors
	@rm -rf Tests/AptosSpecsTests/TestVectors/*
	@cp ../../test-vectors/*.json Tests/AptosSpecsTests/TestVectors/ 2>/dev/null || true
	@mkdir -p Tests/AptosSpecsTests/CucumberTests/TestVectors
	@rm -rf Tests/AptosSpecsTests/CucumberTests/TestVectors/*
	@cp ../../test-vectors/*.json Tests/AptosSpecsTests/CucumberTests/TestVectors/ 2>/dev/null || true
	@echo "Done."

# Build the package
build:
	swift build

# Run all tests (both XCTest and Cucumber)
test: link-features
	swift test

# Run only XCTest-based tests
test-xctest: link-features
	swift test --filter AptosSpecsTests

# Run only Cucumber BDD tests
test-cucumber: link-features
	swift test --filter CucumberTests

# Run tests by priority
test-required: link-features
	swift test --filter "required"

test-preferred: link-features
	swift test --filter "preferred"

test-optional: link-features
	swift test --filter "optional"

# Run tests by category
test-core-types: link-features
	swift test --filter "core-types"

test-cryptography: link-features
	swift test --filter "cryptography"

test-accounts: link-features
	swift test --filter "accounts"

test-transactions: link-features
	swift test --filter "transactions"

test-api-clients: link-features
	swift test --filter "api-clients"

test-advanced: link-features
	swift test --filter "advanced"

# Run tests excluding network-dependent ones
test-offline: link-features
	swift test --filter "not network"

# Clean build artifacts
clean:
	swift package clean
	rm -rf .build
	rm -rf Tests/AptosSpecsTests/Features
	rm -rf Tests/AptosSpecsTests/TestVectors
	rm -rf Tests/AptosSpecsTests/CucumberTests/Features
	rm -rf Tests/AptosSpecsTests/CucumberTests/TestVectors

# Format code (requires swift-format: brew install swift-format)
format:
	swift-format -i -r Sources/ Tests/ 2>/dev/null || echo "Install swift-format: brew install swift-format"

# Lint code (requires swiftlint: brew install swiftlint)
lint:
	swiftlint 2>/dev/null || echo "Install swiftlint: brew install swiftlint"

# Show help
help:
	@echo "Aptos Swift SDK Specification Tests"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup            - Resolve dependencies and link feature files"
	@echo "  build            - Build the package"
	@echo "  test             - Run all tests (XCTest + Cucumber)"
	@echo "  test-xctest      - Run only XCTest-based tests"
	@echo "  test-cucumber    - Run only Cucumber BDD tests"
	@echo "  test-required    - Run only @required (P0) tests"
	@echo "  test-preferred   - Run only @preferred (P1) tests"
	@echo "  test-optional    - Run only @optional (P2) tests"
	@echo "  test-core-types  - Run @core-types tests"
	@echo "  test-cryptography- Run @cryptography tests"
	@echo "  test-accounts    - Run @accounts tests"
	@echo "  test-transactions- Run @transactions tests"
	@echo "  test-api-clients - Run @api-clients tests"
	@echo "  test-advanced    - Run @advanced tests"
	@echo "  test-offline     - Run tests not requiring network"
	@echo "  clean            - Remove build artifacts"
	@echo "  help             - Show this help message"
