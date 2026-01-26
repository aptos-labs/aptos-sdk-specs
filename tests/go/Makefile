.PHONY: test test-required test-preferred test-optional deps setup format lint

# Setup - run this first to initialize dependencies
setup:
	go mod tidy

# Install dependencies
deps:
	go mod download

# Run all tests
test:
	go test -v ./...

# Run only required tests
test-required:
	GODOG_TAGS=@required go test -v ./...

# Run only preferred tests
test-preferred:
	GODOG_TAGS=@preferred go test -v ./...

# Run only optional tests
test-optional:
	GODOG_TAGS=@optional go test -v ./...

# Run tests by feature category
test-core-types:
	GODOG_TAGS=@core-types go test -v ./...

test-cryptography:
	GODOG_TAGS=@cryptography go test -v ./...

test-accounts:
	GODOG_TAGS=@accounts go test -v ./...

test-transactions:
	GODOG_TAGS=@transactions go test -v ./...

test-api-clients:
	GODOG_TAGS=@api-clients go test -v ./...

test-advanced:
	GODOG_TAGS=@advanced go test -v ./...

# Generate step definition snippets for unimplemented steps
snippets:
	go test -v ./...

# Run with verbose output
test-verbose:
	go test -v ./...

# Run network tests (requires testnet connection)
test-network:
	GODOG_TAGS="@api-clients or @fullnode-api or @transaction-submission" go test -v ./...

# Run local-only tests (no network required)
test-local:
	GODOG_TAGS="@core-types or @cryptography or @transactions" go test -v ./...

# Run performance benchmarks
test-performance:
	GODOG_TAGS=@performance go test -v ./...

# Format code
format:
	go fmt ./...

# Lint code
lint:
	golangci-lint run ./...
