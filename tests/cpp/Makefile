# Makefile for Aptos C++ SDK Behavioral Specification Tests
# Uses CMake + Conan for building

.PHONY: all build test test-required test-preferred test-core-types test-cryptography \
        test-accounts test-transactions clean install-deps help

# Default target
all: build

# =============================================================================
# Setup
# =============================================================================

# Install dependencies via Conan
install-deps:
	@echo "Installing dependencies with Conan..."
	conan install . --output-folder=build --build=missing

# =============================================================================
# Build
# =============================================================================

# Configure and build
build: build/aptos_spec_tests

build/aptos_spec_tests: CMakeLists.txt
	@mkdir -p build
	@if [ -f build/conan_toolchain.cmake ]; then \
		cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release; \
	else \
		echo "Warning: Conan toolchain not found, using FetchContent fallback..."; \
		cmake -S . -B build -DCMAKE_BUILD_TYPE=Release; \
	fi
	cmake --build build --parallel

# =============================================================================
# Test Targets
# =============================================================================

# Run all tests
test: build
	@echo "Running all specification tests..."
	./build/aptos_spec_tests ../../features

# Run only @required (P0) tests
test-required: build
	@echo "Running @required tests..."
	./build/aptos_spec_tests ../../features --tags "@required"

# Run only @preferred (P1) tests  
test-preferred: build
	@echo "Running @preferred tests..."
	./build/aptos_spec_tests ../../features --tags "@preferred"

# Run only @optional (P2) tests
test-optional: build
	@echo "Running @optional tests..."
	./build/aptos_spec_tests ../../features --tags "@optional"

# Category-specific tests
test-core-types: build
	@echo "Running @core-types tests..."
	./build/aptos_spec_tests ../../features --tags "@core-types"

test-cryptography: build
	@echo "Running @cryptography tests..."
	./build/aptos_spec_tests ../../features --tags "@cryptography"

test-accounts: build
	@echo "Running @accounts tests..."
	./build/aptos_spec_tests ../../features --tags "@accounts"

test-transactions: build
	@echo "Running @transactions tests..."
	./build/aptos_spec_tests ../../features --tags "@transactions"

test-api-clients: build
	@echo "Running @api-clients tests..."
	./build/aptos_spec_tests ../../features --tags "@api-clients"

test-advanced: build
	@echo "Running @advanced tests..."
	./build/aptos_spec_tests ../../features --tags "@advanced"

# Run tests excluding network-dependent ones
test-offline: build
	@echo "Running tests without network..."
	./build/aptos_spec_tests ../../features --tags "not @network"

# =============================================================================
# Utilities
# =============================================================================

# Clean build artifacts
clean:
	rm -rf build

# Full rebuild
rebuild: clean build

# =============================================================================
# Help
# =============================================================================

help:
	@echo "Aptos C++ SDK Specification Tests"
	@echo ""
	@echo "Setup:"
	@echo "  make install-deps    Install Conan dependencies"
	@echo "  make build           Configure and build tests"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests"
	@echo "  make test-required   Run @required (P0) tests only"
	@echo "  make test-preferred  Run @preferred (P1) tests only"
	@echo "  make test-optional   Run @optional (P2) tests only"
	@echo "  make test-offline    Run tests without network dependency"
	@echo ""
	@echo "Category tests:"
	@echo "  make test-core-types"
	@echo "  make test-cryptography"
	@echo "  make test-accounts"
	@echo "  make test-transactions"
	@echo "  make test-api-clients"
	@echo "  make test-advanced"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean           Remove build artifacts"
	@echo "  make rebuild         Clean and rebuild"
