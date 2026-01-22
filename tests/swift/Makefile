# Aptos Swift SDK Behavioral Specification Tests
# Uses CucumberSwift with XCTest

.PHONY: all build test test-required test-preferred test-optional \
        test-core-types test-cryptography test-accounts test-transactions \
        test-api-clients test-advanced clean setup link-features help

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
	@echo "Linking test vectors..."
	@mkdir -p Tests/AptosSpecsTests/TestVectors
	@rm -rf Tests/AptosSpecsTests/TestVectors/*
	@cp ../../test-vectors/*.json Tests/AptosSpecsTests/TestVectors/ 2>/dev/null || true
	@echo "Done."

# Build the package
build:
	swift build

# Run all tests
test: link-features
	swift test

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

# Show help
help:
	@echo "Aptos Swift SDK Specification Tests"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup            - Resolve dependencies and link feature files"
	@echo "  build            - Build the package"
	@echo "  test             - Run all tests"
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
