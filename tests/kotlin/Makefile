.PHONY: build test test-required test-preferred test-core-types test-cryptography test-transactions dry-run clean

# Default target
all: test

# Build the project
build:
	./gradlew build -x test

# Run all tests
test:
	./gradlew test

# Run only required (P0) tests
test-required:
	./gradlew testRequired

# Run only preferred (P1) tests
test-preferred:
	./gradlew testPreferred

# Run core-types tests
test-core-types:
	./gradlew testCoreTypes

# Run cryptography tests
test-cryptography:
	./gradlew testCryptography

# Run transaction tests
test-transactions:
	./gradlew testTransactions

# Run accounts tests
test-accounts:
	./gradlew test -Dcucumber.filter.tags="@accounts"

# Run API client tests
test-api:
	./gradlew test -Dcucumber.filter.tags="@api-clients"

# Dry run to check step definitions
dry-run:
	./gradlew dryRun

# Clean build artifacts
clean:
	./gradlew clean

# Show test report
report:
	open build/reports/cucumber/cucumber.html 2>/dev/null || xdg-open build/reports/cucumber/cucumber.html 2>/dev/null || echo "Report at build/reports/cucumber/cucumber.html"

# Install Gradle wrapper if needed
wrapper:
	gradle wrapper --gradle-version 8.5

# Help
help:
	@echo "Available targets:"
	@echo "  build            - Build the project without running tests"
	@echo "  test             - Run all tests"
	@echo "  test-required    - Run only @required (P0) tests"
	@echo "  test-preferred   - Run only @preferred (P1) tests"
	@echo "  test-core-types  - Run only @core-types tests"
	@echo "  test-cryptography - Run only @cryptography tests"
	@echo "  test-transactions - Run only @transactions tests"
	@echo "  test-accounts    - Run only @accounts tests"
	@echo "  test-api         - Run only @api-clients tests"
	@echo "  dry-run          - Check step definitions without running"
	@echo "  clean            - Remove build artifacts"
	@echo "  report           - Open HTML test report"
	@echo "  wrapper          - Install Gradle wrapper"
