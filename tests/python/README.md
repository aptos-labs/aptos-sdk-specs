# Aptos Python SDK Behavioral Tests

This directory contains BDD (Behavior-Driven Development) tests for the
[Aptos Python SDK](https://github.com/aptos-labs/aptos-python-sdk) using
[Behave](https://behave.readthedocs.io/).

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)

## Setup

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment and install dependencies
make setup

# Activate the virtual environment
source venv/bin/activate
```

### Without Virtual Environment

```bash
# Install dependencies globally
make deps
# or
pip3 install -r requirements.txt
```

## Running Tests

### All Tests

```bash
make test
```

### By Priority Level

```bash
# Required tests only (P0 - every SDK must implement)
make test-required

# Preferred tests (P1 - expected in production SDKs)
make test-preferred

# Optional tests (P2 - for comprehensive SDKs)
make test-optional
```

### By Feature Category

```bash
make test-core-types      # Address, BCS serialization, type tags
make test-cryptography    # Ed25519, Secp256k1, hashing
make test-accounts        # Account management, mnemonic derivation
make test-transactions    # Transaction building and signing
make test-api-clients     # Fullnode API, faucet, indexer
make test-advanced        # Multi-sig, keyless, fee payer
```

### Verbose Output

```bash
make test-verbose
```

### Generate Snippets for Missing Steps

```bash
make snippets
```

## Project Structure

```
tests/python/
├── requirements.txt     # Python dependencies
├── Makefile            # Build and test commands
├── README.md           # This file
├── behave.ini          # Behave configuration
├── support/
│   ├── __init__.py
│   ├── world.py        # Test context (World class)
│   └── vectors.py      # Test vector loading utilities
└── steps/
    ├── __init__.py
    ├── address_steps.py
    ├── serialization_steps.py
    ├── cryptography_steps.py
    ├── hashing_steps.py
    ├── account_steps.py
    ├── mnemonic_steps.py
    ├── transaction_steps.py
    └── ...
```

## Writing Step Definitions

Step definitions map Gherkin steps to Python code. Example:

```python
from behave import given, when, then
from aptos_sdk.account_address import AccountAddress

@given('a hex string "{hex_string}"')
def step_given_hex_string(context, hex_string):
    context.hex_string = hex_string

@when('I parse the address')
def step_parse_address(context):
    try:
        context.address = AccountAddress.from_str(context.hex_string)
        context.error = None
    except Exception as e:
        context.error = e

@then('the parsing should succeed')
def step_parsing_should_succeed(context):
    assert context.error is None
    assert context.address is not None
```

## SDK Documentation

- [Aptos Python SDK GitHub](https://github.com/aptos-labs/aptos-python-sdk)
- [Aptos Python SDK Docs](https://aptos.dev/sdks/python-sdk/)
- [PyPI Package](https://pypi.org/project/aptos-sdk/)

## Notes

- The SDK recommends using the **async client** for new projects
- The synchronous client is deprecated
- Some tests may require a running Aptos node or testnet access
