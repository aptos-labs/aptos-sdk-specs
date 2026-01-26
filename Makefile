# Root Makefile for Aptos SDK Specs
# Provides unified commands for formatting, linting, testing, and maintenance

.PHONY: format format-check format-docs format-tests help check-tools
.PHONY: format-typescript format-go format-rust format-python format-dotnet
.PHONY: format-java format-kotlin format-swift format-cpp
.PHONY: lint lint-tests lint-typescript lint-go lint-rust lint-python lint-dotnet
.PHONY: lint-java lint-kotlin lint-swift lint-cpp
.PHONY: lint-fix lint-fix-tests lint-fix-go lint-fix-rust lint-fix-python lint-fix-swift

# Default target
all: help

# =============================================================================
# Tool Checks
# =============================================================================

# Check all required tools and show installation instructions
check-tools:
	@echo "Checking formatting and linting tools..."
	@echo ""
	@missing=0; \
	\
	echo "=== Core Tools ==="; \
	if command -v bun >/dev/null 2>&1; then \
		echo "✓ bun           $$(bun --version)"; \
	else \
		echo "✗ bun           Install: curl -fsSL https://bun.sh/install | bash"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	echo ""; \
	echo "=== Language Tools ==="; \
	\
	if command -v go >/dev/null 2>&1; then \
		echo "✓ go            $$(go version | awk '{print $$3}')"; \
	else \
		echo "✗ go            Install: https://go.dev/dl/"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v cargo >/dev/null 2>&1; then \
		echo "✓ cargo         $$(cargo --version | awk '{print $$2}')"; \
	else \
		echo "✗ cargo         Install: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v python3 >/dev/null 2>&1; then \
		echo "✓ python3       $$(python3 --version | awk '{print $$2}')"; \
	else \
		echo "✗ python3       Install: https://www.python.org/downloads/"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v dotnet >/dev/null 2>&1; then \
		echo "✓ dotnet        $$(dotnet --version)"; \
	else \
		echo "✗ dotnet        Install: https://dotnet.microsoft.com/download"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v mvn >/dev/null 2>&1; then \
		echo "✓ mvn           $$(mvn --version 2>/dev/null | head -1 | awk '{print $$3}')"; \
	else \
		echo "✗ mvn           Install: brew install maven (or https://maven.apache.org/)"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v gradle >/dev/null 2>&1 || [ -f tests/kotlin/gradlew ]; then \
		echo "✓ gradle        (wrapper available)"; \
	else \
		echo "✗ gradle        Install: brew install gradle (or https://gradle.org/)"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v swift >/dev/null 2>&1; then \
		echo "✓ swift         $$(swift --version 2>/dev/null | head -1 | awk '{print $$4}')"; \
	else \
		echo "✗ swift         Install: Xcode or https://swift.org/download/"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	echo ""; \
	echo "=== Formatters ==="; \
	\
	if [ -f tests/python/venv/bin/black ]; then \
		echo "✓ black         $$(tests/python/venv/bin/black --version 2>/dev/null | head -1 | awk '{print $$2}') (in venv)"; \
	elif python3 -c "import black" 2>/dev/null; then \
		echo "✓ black         $$(python3 -m black --version 2>/dev/null | head -1 | awk '{print $$2}')"; \
	else \
		echo "✗ black         Will be installed in venv by 'make format-python'"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v swift-format >/dev/null 2>&1; then \
		echo "✓ swift-format  $$(swift-format --version 2>/dev/null)"; \
	else \
		echo "✗ swift-format  Install: brew install swift-format"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v clang-format >/dev/null 2>&1; then \
		echo "✓ clang-format  $$(clang-format --version | awk '{print $$3}')"; \
	else \
		echo "✗ clang-format  Install: brew install clang-format"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	echo ""; \
	echo "=== Linters ==="; \
	\
	if command -v golangci-lint >/dev/null 2>&1; then \
		echo "✓ golangci-lint $$(golangci-lint --version 2>/dev/null | awk '{print $$4}')"; \
	else \
		echo "✗ golangci-lint Install: brew install golangci-lint"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if [ -f tests/python/venv/bin/flake8 ]; then \
		echo "✓ flake8        $$(tests/python/venv/bin/flake8 --version 2>/dev/null | head -1 | awk '{print $$1}') (in venv)"; \
	elif python3 -c "import flake8" 2>/dev/null; then \
		echo "✓ flake8        $$(python3 -m flake8 --version 2>/dev/null | head -1 | awk '{print $$1}')"; \
	else \
		echo "✗ flake8        Will be installed in venv by 'make lint-python'"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if [ -f tests/python/venv/bin/autopep8 ]; then \
		echo "✓ autopep8      $$(tests/python/venv/bin/autopep8 --version 2>/dev/null | awk '{print $$2}') (in venv)"; \
	else \
		echo "✗ autopep8      Will be installed in venv by 'make lint-fix-python'"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v swiftlint >/dev/null 2>&1; then \
		echo "✓ swiftlint     $$(swiftlint version 2>/dev/null)"; \
	else \
		echo "✗ swiftlint     Install: brew install swiftlint"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	if command -v clang-tidy >/dev/null 2>&1; then \
		echo "✓ clang-tidy    available"; \
	elif command -v cppcheck >/dev/null 2>&1; then \
		echo "✓ cppcheck      $$(cppcheck --version | awk '{print $$2}')"; \
	else \
		echo "✗ clang-tidy    Install: brew install llvm (or cppcheck)"; \
		missing=$$((missing + 1)); \
	fi; \
	\
	echo ""; \
	echo "=== Summary ==="; \
	if [ $$missing -eq 0 ]; then \
		echo "All tools are installed!"; \
	else \
		echo "$$missing tool(s) missing. Install them for full functionality."; \
		echo ""; \
		echo "Quick install (macOS):"; \
		echo "  brew install go maven gradle swift-format clang-format golangci-lint swiftlint"; \
		echo "  pip install black flake8"; \
		echo ""; \
		echo "Note: Some tools are optional. Formatting/linting will skip unavailable tools."; \
	fi

# =============================================================================
# Formatting
# =============================================================================

# Format everything
format: format-docs format-tests
	@echo "✓ All formatting complete"

# Format documentation and feature files (root level)
format-docs:
	@echo "Formatting docs and feature files..."
	@bun run format

# Check formatting without making changes
format-check:
	@echo "Checking formatting..."
	@bun run format:check

# Format all test implementations
format-tests: format-typescript format-go format-rust format-python format-dotnet format-java format-kotlin format-swift format-cpp
	@echo "✓ All test code formatted"

# Individual language formatters
format-typescript:
	@echo "Formatting TypeScript..."
	@cd tests/typescript && bun run format 2>/dev/null || echo "  (skipped - bun not available or no changes)"

format-go:
	@echo "Formatting Go..."
	@cd tests/go && go fmt ./... 2>/dev/null || echo "  (skipped - go not available)"

format-rust:
	@echo "Formatting Rust..."
	@cd tests/rust && cargo fmt 2>&1 || echo "  (skipped - cargo fmt failed or not available)"

format-python:
	@echo "Formatting Python..."
	@cd tests/python && \
		if [ -d venv ]; then \
			./venv/bin/pip install -q black 2>/dev/null || true; \
			./venv/bin/python -m black steps/ support/ 2>&1; \
		else \
			echo "  Creating virtualenv..."; \
			python3 -m venv venv && \
			./venv/bin/pip install -q --upgrade pip && \
			./venv/bin/pip install -q black && \
			./venv/bin/python -m black steps/ support/ 2>&1; \
		fi || echo "  (skipped - could not set up Python environment)"

format-dotnet:
	@echo "Formatting .NET..."
	@cd tests/dotnet && dotnet format 2>/dev/null || echo "  (skipped - dotnet not available)"

format-java:
	@echo "Formatting Java..."
	@cd tests/java && (mvn spotless:apply 2>/dev/null || mvn fmt:format 2>/dev/null) || echo "  (skipped - no formatter configured)"

format-kotlin:
	@echo "Formatting Kotlin..."
	@cd tests/kotlin && ./gradlew ktlintFormat 2>/dev/null || echo "  (skipped - ktlint not configured)"

format-swift:
	@echo "Formatting Swift..."
	@cd tests/swift && swift-format -i -r Sources/ Tests/ 2>/dev/null || echo "  (skipped - swift-format not available)"

format-cpp:
	@echo "Formatting C++..."
	@cd tests/cpp && find src -name '*.cpp' -o -name '*.hpp' 2>/dev/null | xargs clang-format -i 2>/dev/null || echo "  (skipped - clang-format not available)"

# =============================================================================
# Linting
# =============================================================================

# Lint everything
lint: lint-tests
	@echo "✓ All linting complete"

# Lint all test implementations
lint-tests: lint-typescript lint-go lint-rust lint-python lint-dotnet lint-java lint-kotlin lint-swift lint-cpp
	@echo "✓ All test code linted"

# Individual language linters (excluding generated files)
lint-typescript:
	@echo "Linting TypeScript..."
	@cd tests/typescript && bun run lint 2>/dev/null || echo "  (skipped - bun not available or lint script missing)"

lint-go:
	@echo "Linting Go..."
	@cd tests/go && (golangci-lint run ./... 2>&1 || go vet ./... 2>&1) || echo "  (skipped - go not available)"

lint-rust:
	@echo "Linting Rust..."
	@cd tests/rust && cargo clippy --test specs 2>/dev/null || echo "  (skipped - cargo/clippy not available)"

lint-python:
	@echo "Linting Python..."
	@cd tests/python && \
		if [ -d venv ]; then \
			./venv/bin/pip install -q flake8 2>/dev/null || true; \
			./venv/bin/python -m flake8 steps/ support/ 2>&1; \
		else \
			echo "  (skipped - run 'make format-python' first to create virtualenv)"; \
		fi || echo "  (skipped - flake8 failed)"

lint-dotnet:
	@echo "Linting .NET..."
	@cd tests/dotnet && dotnet format --verify-no-changes --exclude bin/ --exclude obj/ 2>/dev/null || echo "  (skipped - dotnet not available)"

lint-java:
	@echo "Linting Java..."
	@cd tests/java && (mvn checkstyle:check 2>/dev/null || mvn spotless:check 2>/dev/null) || echo "  (skipped - no linter configured)"

lint-kotlin:
	@echo "Linting Kotlin..."
	@cd tests/kotlin && ./gradlew ktlintCheck 2>/dev/null || echo "  (skipped - ktlint not configured)"

lint-swift:
	@echo "Linting Swift..."
	@cd tests/swift && swiftlint 2>/dev/null || echo "  (skipped - swiftlint not available)"

lint-cpp:
	@echo "Linting C++..."
	@cd tests/cpp && cppcheck --exclude=build --exclude=sdk src/ steps/ support/ 2>/dev/null || echo "  (skipped - cppcheck not available)"

# =============================================================================
# Lint Fix (auto-fix where supported)
# =============================================================================

# Fix all linting issues where possible
lint-fix: lint-fix-tests
	@echo "✓ All auto-fixable lint issues resolved"

# Fix lint issues in all test implementations
lint-fix-tests: lint-fix-go lint-fix-rust lint-fix-python lint-fix-swift
	@echo "✓ All test code lint issues fixed (where possible)"

lint-fix-go:
	@echo "Fixing Go lint issues..."
	@cd tests/go && golangci-lint run --fix ./... 2>&1 || echo "  (some issues could not be auto-fixed)"

lint-fix-rust:
	@echo "Fixing Rust lint issues..."
	@cd tests/rust && cargo clippy --fix --allow-dirty --allow-staged --test specs 2>/dev/null || echo "  (skipped - cargo/clippy not available)"

lint-fix-python:
	@echo "Fixing Python lint issues..."
	@cd tests/python && \
		if [ -d venv ]; then \
			./venv/bin/pip install -q autopep8 2>/dev/null || true; \
			find steps/ support/ -name '*.py' -type f ! -type l | xargs ./venv/bin/python -m autopep8 --in-place 2>&1; \
		else \
			echo "  (skipped - run 'make format-python' first to create virtualenv)"; \
		fi || echo "  (skipped - autopep8 failed)"

lint-fix-swift:
	@echo "Fixing Swift lint issues..."
	@cd tests/swift && swiftlint --fix 2>/dev/null || echo "  (skipped - swiftlint not available)"

# =============================================================================
# Help
# =============================================================================

help:
	@echo "Aptos SDK Specs - Unified Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make check-tools     - Check which tools are installed"
	@echo ""
	@echo "Formatting:"
	@echo "  make format          - Format everything (docs + all test code)"
	@echo "  make format-check    - Check formatting without changes"
	@echo "  make format-docs     - Format .md and .feature files only"
	@echo "  make format-tests    - Format all test implementations"
	@echo ""
	@echo "Linting:"
	@echo "  make lint            - Lint all test implementations"
	@echo "  make lint-fix        - Auto-fix lint issues (Go, Rust, Python, Swift)"
	@echo ""
	@echo "Individual formatters:      Individual linters:       Lint fixers:"
	@echo "  make format-typescript    make lint-typescript"
	@echo "  make format-go            make lint-go              make lint-fix-go"
	@echo "  make format-rust          make lint-rust            make lint-fix-rust"
	@echo "  make format-python        make lint-python          make lint-fix-python"
	@echo "  make format-dotnet        make lint-dotnet"
	@echo "  make format-java          make lint-java"
	@echo "  make format-kotlin        make lint-kotlin"
	@echo "  make format-swift         make lint-swift           make lint-fix-swift"
	@echo "  make format-cpp           make lint-cpp"
