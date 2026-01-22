using Aptos;

namespace Aptos.Specs.Support;

/// <summary>
/// Holds test context/state between Gherkin steps within a scenario.
/// Each scenario gets a fresh TestWorld instance via dependency injection.
/// </summary>
public class TestWorld
{
    // =========================================================================
    // Configuration
    // =========================================================================
    
    public NetworkConfig Network { get; set; } = Networks.Testnet;
    public AptosClient? Client { get; set; }
    
    // =========================================================================
    // Addresses
    // =========================================================================
    
    public AccountAddress? Address { get; set; }
    public AccountAddress? Address2 { get; set; }
    public List<AccountAddress> Addresses { get; set; } = new();
    
    // =========================================================================
    // Cryptography - Ed25519
    // =========================================================================
    
    public Ed25519PrivateKey? Ed25519PrivateKey { get; set; }
    public Ed25519PrivateKey? Ed25519PrivateKey2 { get; set; }
    public Ed25519PublicKey? Ed25519PublicKey { get; set; }
    public Ed25519PublicKey? Ed25519PublicKey2 { get; set; }
    public Ed25519Signature? Ed25519Signature { get; set; }
    public Ed25519Signature? Ed25519Signature2 { get; set; }
    
    // =========================================================================
    // Cryptography - Secp256k1 (if SDK supports)
    // =========================================================================
    
    public Secp256k1PrivateKey? Secp256k1PrivateKey { get; set; }
    public Secp256k1PrivateKey? Secp256k1PrivateKey2 { get; set; }
    public Secp256k1PublicKey? Secp256k1PublicKey { get; set; }
    public Secp256k1PublicKey? Secp256k1PublicKey2 { get; set; }
    public Secp256k1Signature? Secp256k1Signature { get; set; }
    public Secp256k1Signature? Secp256k1Signature2 { get; set; }
    
    // =========================================================================
    // Messages and Data
    // =========================================================================
    
    public byte[]? Message { get; set; }
    public byte[]? Message2 { get; set; }
    public byte[]? Bytes { get; set; }
    public byte[]? HashResult { get; set; }
    public string? HexString { get; set; }
    
    // =========================================================================
    // Accounts
    // =========================================================================
    
    public Ed25519Account? Account { get; set; }
    public Ed25519Account? Account2 { get; set; }
    public List<Ed25519Account> Accounts { get; set; } = new();
    public Dictionary<string, Ed25519Account> NamedAccounts { get; set; } = new();
    
    // =========================================================================
    // Authentication
    // =========================================================================
    
    public AuthenticationKey? AuthenticationKey { get; set; }
    public AuthenticationKey? AuthKey { get; set; }
    public string? Mnemonic { get; set; }
    public string? DerivationPath { get; set; }
    
    // =========================================================================
    // Transactions
    // =========================================================================
    
    public RawTransaction? RawTransaction { get; set; }
    public SignedTransaction? SignedTransaction { get; set; }
    public string? TransactionHash { get; set; }
    
    // =========================================================================
    // General Purpose
    // =========================================================================
    
    public object? Result { get; set; }
    public Exception? Error { get; private set; }
    public Dictionary<string, object> TestVectors { get; set; } = new();
    
    // =========================================================================
    // Methods
    // =========================================================================
    
    /// <summary>
    /// Initialize the Aptos client for the current network
    /// </summary>
    public AptosClient InitClient()
    {
        if (Client == null)
        {
            var config = new AptosConfig(Network);
            Client = new AptosClient(config);
        }
        return Client;
    }
    
    /// <summary>
    /// Get or create a named account
    /// </summary>
    public Ed25519Account GetOrCreateAccount(string name)
    {
        if (!NamedAccounts.TryGetValue(name, out var account))
        {
            account = Ed25519Account.Generate();
            NamedAccounts[name] = account;
        }
        return account;
    }
    
    /// <summary>
    /// Store an error for later assertion
    /// </summary>
    public void SetError(Exception error)
    {
        Error = error;
    }
    
    /// <summary>
    /// Clear error state
    /// </summary>
    public void ClearError()
    {
        Error = null;
    }
    
    /// <summary>
    /// Check if there is an error
    /// </summary>
    public bool HasError => Error != null;
    
    /// <summary>
    /// Reset all state (called between scenarios)
    /// </summary>
    public void Reset()
    {
        // Configuration
        Network = Networks.Testnet;
        Client = null;
        
        // Addresses
        Address = null;
        Address2 = null;
        Addresses.Clear();
        
        // Ed25519
        Ed25519PrivateKey = null;
        Ed25519PrivateKey2 = null;
        Ed25519PublicKey = null;
        Ed25519PublicKey2 = null;
        Ed25519Signature = null;
        Ed25519Signature2 = null;
        
        // Secp256k1
        Secp256k1PrivateKey = null;
        Secp256k1PrivateKey2 = null;
        Secp256k1PublicKey = null;
        Secp256k1PublicKey2 = null;
        Secp256k1Signature = null;
        Secp256k1Signature2 = null;
        
        // Messages
        Message = null;
        Message2 = null;
        Bytes = null;
        HashResult = null;
        HexString = null;
        
        // Accounts
        Account = null;
        Account2 = null;
        Accounts.Clear();
        NamedAccounts.Clear();
        
        // Authentication
        AuthenticationKey = null;
        AuthKey = null;
        Mnemonic = null;
        DerivationPath = null;
        
        // Transactions
        RawTransaction = null;
        SignedTransaction = null;
        TransactionHash = null;
        
        // General
        Result = null;
        Error = null;
        TestVectors.Clear();
    }
}
