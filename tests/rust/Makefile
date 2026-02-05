# Behavioral specification tests for aptos-rust-sdk
.PHONY: test test-required test-preferred test-all test-core-types test-cryptography test-accounts clean

# Default: run all tests
test:
	cargo test --test specs

# Run only required (P0) tests
test-required:
	cargo test --test specs -- --tags @required

# Run only preferred (P1) tests
test-preferred:
	cargo test --test specs -- --tags @preferred

# Run all tests including optional
test-all:
	cargo test --test specs -- --tags "@required or @preferred or @optional"

# Run specific feature categories
test-core-types:
	cargo test --test specs -- --tags @core-types

test-cryptography:
	cargo test --test specs -- --tags @cryptography

test-accounts:
	cargo test --test specs -- --tags @accounts

test-transactions:
	cargo test --test specs -- --tags @transactions

test-api:
	cargo test --test specs -- --tags @api-clients

test-advanced:
	cargo test --test specs -- --tags @advanced

# Run with verbose output
test-verbose:
	cargo test --test specs -- -v

# Generate HTML report
test-report:
	cargo test --test specs -- --format junit > report.xml

# Clean build artifacts
clean:
	cargo clean

# Check that the code compiles
check:
	cargo check --test specs

# Format code
fmt:
	cargo fmt

# Run clippy
clippy:
	cargo clippy --test specs

