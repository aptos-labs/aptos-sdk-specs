.PHONY: all build test test-required test-preferred test-optional clean restore
.PHONY: test-core-types test-cryptography test-accounts test-transactions test-api-clients test-advanced

# Default target
all: test

# Restore NuGet packages
restore:
	dotnet restore

# Build the project
build: restore
	dotnet build --no-restore

# Run all tests
test: build
	dotnet test --no-build --logger "console;verbosity=normal"

# Run tests by priority level
test-required: build
	dotnet test --no-build --filter "Category=required" --logger "console;verbosity=normal"

test-preferred: build
	dotnet test --no-build --filter "Category=preferred" --logger "console;verbosity=normal"

test-optional: build
	dotnet test --no-build --filter "Category=optional" --logger "console;verbosity=normal"

# Run tests by category
test-core-types: build
	dotnet test --no-build --filter "Category=core-types" --logger "console;verbosity=normal"

test-cryptography: build
	dotnet test --no-build --filter "Category=cryptography" --logger "console;verbosity=normal"

test-accounts: build
	dotnet test --no-build --filter "Category=account-management" --logger "console;verbosity=normal"

test-transactions: build
	dotnet test --no-build --filter "Category=transaction-building" --logger "console;verbosity=normal"

test-api-clients: build
	dotnet test --no-build --filter "Category=api-clients" --logger "console;verbosity=normal"

test-advanced: build
	dotnet test --no-build --filter "Category=advanced" --logger "console;verbosity=normal"

# Clean build artifacts
clean:
	dotnet clean
	rm -rf bin obj TestResults

# Format code (requires dotnet-format tool)
format:
	dotnet format

# Check for outdated packages
outdated:
	dotnet list package --outdated
