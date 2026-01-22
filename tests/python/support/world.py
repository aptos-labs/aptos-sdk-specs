"""
World module - holds test context between steps.
Each scenario gets a fresh context.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class AptosWorld:
    """
    Test context class that holds state between Gherkin steps.
    Each scenario gets a fresh instance via before_scenario hook.
    """

    # Configuration
    network_url: str = "https://fullnode.testnet.aptoslabs.com/v1"
    client: Any = None

    # Addresses
    address: Any = None
    addresses: List[Any] = field(default_factory=list)

    # Cryptography - Ed25519
    ed25519_private_key: Any = None
    ed25519_private_key_2: Any = None
    ed25519_public_key: Any = None
    ed25519_public_key_2: Any = None
    ed25519_signature: Any = None
    ed25519_signature_2: Any = None

    # Cryptography - Secp256k1
    secp256k1_private_key: Any = None
    secp256k1_private_key_2: Any = None
    secp256k1_public_key: Any = None
    secp256k1_public_key_2: Any = None
    secp256k1_signature: Any = None
    secp256k1_signature_2: Any = None

    # Messages
    message: Optional[bytes] = None
    message_2: Optional[bytes] = None

    # Accounts
    account: Any = None
    account_2: Any = None
    accounts: List[Any] = field(default_factory=list)
    accounts_map: Dict[str, Any] = field(default_factory=dict)

    # Transactions
    raw_transaction: Any = None
    signed_transaction: Any = None
    transaction_hash: Optional[str] = None
    simulation_result: Any = None
    
    # Entry functions
    entry_function: Any = None
    transaction_payload: Any = None
    authenticator: Any = None
    
    # Account collections
    secp256k1_account: Any = None
    account_collection: List[Any] = field(default_factory=list)
    any_account: Any = None
    private_key: Any = None
    public_key: Any = None
    
    # Fee payer
    fee_payer: Any = None
    fee_payer_tx: Any = None
    multi_agent_tx: Any = None

    # Authentication
    auth_key: Any = None

    # Mnemonic
    mnemonic: Optional[str] = None
    derivation_path: Optional[str] = None
    passphrase: Optional[str] = None

    # Type tags
    type_tag: Any = None
    type_tags: List[Any] = field(default_factory=list)

    # General storage
    result: Any = None
    error: Optional[Exception] = None
    bytes_value: Optional[bytes] = None
    hex_string: Optional[str] = None

    # Test vectors
    test_vectors: Dict[str, Any] = field(default_factory=dict)

    # Hashing
    hash_result: Optional[bytes] = None
    hash_results: List[bytes] = field(default_factory=list)

    def reset(self) -> None:
        """Reset all state between scenarios."""
        self.client = None
        self.address = None
        self.addresses = []

        # Ed25519
        self.ed25519_private_key = None
        self.ed25519_private_key_2 = None
        self.ed25519_public_key = None
        self.ed25519_public_key_2 = None
        self.ed25519_signature = None
        self.ed25519_signature_2 = None

        # Secp256k1
        self.secp256k1_private_key = None
        self.secp256k1_private_key_2 = None
        self.secp256k1_public_key = None
        self.secp256k1_public_key_2 = None
        self.secp256k1_signature = None
        self.secp256k1_signature_2 = None

        # Messages
        self.message = None
        self.message_2 = None

        # Accounts
        self.account = None
        self.account_2 = None
        self.accounts = []
        self.accounts_map = {}

        # Transactions
        self.raw_transaction = None
        self.signed_transaction = None
        self.transaction_hash = None
        self.simulation_result = None
        
        # Entry functions
        self.entry_function = None
        self.transaction_payload = None
        self.authenticator = None
        
        # Account collections
        self.secp256k1_account = None
        self.account_collection = []
        self.any_account = None
        self.private_key = None
        self.public_key = None
        
        # Fee payer
        self.fee_payer = None
        self.fee_payer_tx = None
        self.multi_agent_tx = None

        # Authentication
        self.auth_key = None

        # Mnemonic
        self.mnemonic = None
        self.derivation_path = None
        self.passphrase = None

        # Type tags
        self.type_tag = None
        self.type_tags = []

        # General
        self.result = None
        self.error = None
        self.bytes_value = None
        self.hex_string = None
        self.test_vectors = {}

        # Hashing
        self.hash_result = None
        self.hash_results = []

    def set_error(self, error: Exception) -> None:
        """Store an error for later assertion."""
        self.error = error

    def clear_error(self) -> None:
        """Clear the error state."""
        self.error = None

    def get_or_create_account(self, name: str) -> Any:
        """Get or create a named account."""
        from aptos_sdk.account import Account

        if name not in self.accounts_map:
            self.accounts_map[name] = Account.generate()
        return self.accounts_map[name]


def before_scenario(context, scenario):
    """Behave hook - called before each scenario."""
    context.world = AptosWorld()


def after_scenario(context, scenario):
    """Behave hook - called after each scenario."""
    if hasattr(context, "world"):
        context.world.reset()
