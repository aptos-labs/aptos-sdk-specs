# Makefile for Aptos Java SDK BDD Tests

.PHONY: all test test-required test-preferred test-optional test-core-types test-cryptography test-transactions test-offline dry-run clean compile help

# Default target
all: test

# Compile the project
compile:
	mvn compile test-compile -q

# Run all tests
test:
	mvn test

# Run only required (P0) tests
test-required:
	mvn test -Prequired

# Run only preferred (P1) tests
test-preferred:
	mvn test -Ppreferred

# Run only optional (P2) tests
test-optional:
	mvn test -Poptional

# Run core-types tests
test-core-types:
	mvn test -Pcore-types

# Run cryptography tests
test-cryptography:
	mvn test -Pcryptography

# Run transaction tests
test-transactions:
	mvn test -Ptransactions

# Run tests that don't require network
test-offline:
	mvn test -Poffline

# Dry run to check step definitions without executing
dry-run:
	mvn test -Dcucumber.execution.dry-run=true

# Run tests with specific tags (usage: make test-tags TAGS="@required and @core-types")
test-tags:
	mvn test -Dcucumber.filter.tags="$(TAGS)"

# Clean build artifacts
clean:
	mvn clean

# Generate test reports
report:
	@echo "Test reports available at: target/cucumber-reports/"
	@ls -la target/cucumber-reports/ 2>/dev/null || echo "No reports generated yet. Run 'make test' first."

# Install dependencies
install:
	mvn dependency:resolve

# Show help
help:
	@echo "Aptos Java SDK BDD Tests"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  test             Run all tests"
	@echo "  test-required    Run only @required (P0) tests"
	@echo "  test-preferred   Run only @preferred (P1) tests"
	@echo "  test-optional    Run only @optional (P2) tests"
	@echo "  test-core-types  Run @core-types tests"
	@echo "  test-cryptography Run @cryptography tests"
	@echo "  test-transactions Run @transactions tests"
	@echo "  test-offline     Run tests without network dependency"
	@echo "  test-tags        Run tests with custom tags (TAGS=\"@tag\")"
	@echo "  dry-run          Check step definitions without running tests"
	@echo "  compile          Compile the project"
	@echo "  clean            Clean build artifacts"
	@echo "  report           Show test report location"
	@echo "  install          Install Maven dependencies"
	@echo "  help             Show this help message"
