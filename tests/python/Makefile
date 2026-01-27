.PHONY: setup deps test test-required test-preferred test-optional clean

# Python command (use python3 on most systems)
PYTHON := python3
PIP := pip3
FEATURES := ../../features

# Setup - create virtual environment and install dependencies
setup:
	$(PYTHON) -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

# Install dependencies (without venv)
deps:
	$(PIP) install -r requirements.txt

# Run all tests (behave.ini defines feature paths, steps found in ./steps/)
test:
	$(PYTHON) -m behave --no-capture

# Run only required tests
test-required:
	$(PYTHON) -m behave --tags=@required --no-capture

# Run only preferred tests
test-preferred:
	$(PYTHON) -m behave --tags=@preferred --no-capture

# Run only optional tests
test-optional:
	$(PYTHON) -m behave --tags=@optional --no-capture

# Run tests by feature category
test-core-types:
	$(PYTHON) -m behave $(FEATURES)/01-core-types --no-capture

test-cryptography:
	$(PYTHON) -m behave $(FEATURES)/02-cryptography --no-capture

test-accounts:
	$(PYTHON) -m behave $(FEATURES)/03-account-management --no-capture

test-transactions:
	$(PYTHON) -m behave $(FEATURES)/04-transaction-building --no-capture

test-api-clients:
	$(PYTHON) -m behave $(FEATURES)/05-api-clients --no-capture

test-advanced:
	$(PYTHON) -m behave $(FEATURES)/06-advanced --no-capture

# Run with verbose output
test-verbose:
	$(PYTHON) -m behave --no-capture -v

# Generate step definition snippets for unimplemented steps
snippets:
	$(PYTHON) -m behave --dry-run --snippets

# Clean up
clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf steps/__pycache__
	rm -rf support/__pycache__
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +

# Format code
format:
	$(PYTHON) -m black steps/ support/

# Lint code
lint:
	$(PYTHON) -m flake8 steps/ support/
