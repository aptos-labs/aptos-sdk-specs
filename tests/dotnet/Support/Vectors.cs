using System.Text.Json;
using System.Text.Json.Serialization;

namespace Aptos.Specs.Support;

/// <summary>
/// Utilities for loading test vectors from JSON files.
/// Test vectors are located in ../../test-vectors/
/// </summary>
public static class Vectors
{
    private static readonly string VectorsPath = Path.Combine(
        AppDomain.CurrentDomain.BaseDirectory,
        "..", "..", "..", "..", "..", "test-vectors"
    );

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true
    };

    // =========================================================================
    // Address Vectors
    // =========================================================================

    public static List<AddressVector> GetAddressParsingVectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "addresses.json"));
        var data = JsonSerializer.Deserialize<AddressVectorFile>(json, JsonOptions);
        return data?.AddressParsing ?? new List<AddressVector>();
    }

    public static AddressConstants GetAddressConstants()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "addresses.json"));
        var data = JsonSerializer.Deserialize<AddressVectorFile>(json, JsonOptions);
        return data?.Constants ?? new AddressConstants();
    }

    public static List<InvalidAddressInput> GetInvalidAddressInputs()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "addresses.json"));
        var data = JsonSerializer.Deserialize<AddressVectorFile>(json, JsonOptions);
        return data?.InvalidInputs ?? new List<InvalidAddressInput>();
    }

    // =========================================================================
    // Signature Vectors
    // =========================================================================

    public static List<SignatureVector> GetEd25519Vectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "signatures.json"));
        var data = JsonSerializer.Deserialize<SignatureVectorFile>(json, JsonOptions);
        return data?.Ed25519 ?? new List<SignatureVector>();
    }

    public static List<SignatureVector> GetSecp256k1Vectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "signatures.json"));
        var data = JsonSerializer.Deserialize<SignatureVectorFile>(json, JsonOptions);
        return data?.Secp256k1 ?? new List<SignatureVector>();
    }

    // =========================================================================
    // BCS Vectors
    // =========================================================================

    public static List<BcsVector> GetBcsVectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "bcs.json"));
        var data = JsonSerializer.Deserialize<BcsVectorFile>(json, JsonOptions);
        return data?.Vectors ?? new List<BcsVector>();
    }

    // =========================================================================
    // Mnemonic Vectors
    // =========================================================================

    public static List<MnemonicVector> GetMnemonicVectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "mnemonics.json"));
        var data = JsonSerializer.Deserialize<MnemonicVectorFile>(json, JsonOptions);
        return data?.Vectors ?? new List<MnemonicVector>();
    }

    // =========================================================================
    // Type Tag Vectors
    // =========================================================================

    public static List<TypeTagVector> GetTypeTagVectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "type-tags.json"));
        var data = JsonSerializer.Deserialize<TypeTagVectorFile>(json, JsonOptions);
        return data?.Vectors ?? new List<TypeTagVector>();
    }

    // =========================================================================
    // Transaction Vectors
    // =========================================================================

    public static List<TransactionVector> GetTransactionVectors()
    {
        var json = File.ReadAllText(Path.Combine(VectorsPath, "transactions.json"));
        var data = JsonSerializer.Deserialize<TransactionVectorFile>(json, JsonOptions);
        return data?.Vectors ?? new List<TransactionVector>();
    }

    // =========================================================================
    // Hex Utilities
    // =========================================================================

    public static byte[] HexToBytes(string hex)
    {
        if (hex.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
            hex = hex[2..];

        return Convert.FromHexString(hex);
    }

    public static string BytesToHex(byte[] bytes, bool prefix = true)
    {
        var hex = Convert.ToHexString(bytes).ToLowerInvariant();
        return prefix ? "0x" + hex : hex;
    }
}

// =============================================================================
// Vector Data Classes
// =============================================================================

public class AddressVectorFile
{
    public string? Version { get; set; }
    public string? Description { get; set; }
    public List<AddressVector>? AddressParsing { get; set; }
    public AddressConstants? Constants { get; set; }
    public List<InvalidAddressInput>? InvalidInputs { get; set; }
}

public class AddressVector
{
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public string Input { get; set; } = "";
    public AddressExpected Expected { get; set; } = new();
}

public class AddressExpected
{
    public string FullHex { get; set; } = "";
    public string ShortString { get; set; } = "";
    public string Bytes { get; set; } = "";
}

public class AddressConstants
{
    public string Zero { get; set; } = "";
    public string One { get; set; } = "";
    public string Two { get; set; } = "";
    public string Three { get; set; } = "";
    public string Four { get; set; } = "";
}

public class InvalidAddressInput
{
    public string Name { get; set; } = "";
    public string Input { get; set; } = "";
    public string ErrorType { get; set; } = "";
}

public class SignatureVectorFile
{
    public string? Version { get; set; }
    public List<SignatureVector>? Ed25519 { get; set; }
    public List<SignatureVector>? Secp256k1 { get; set; }
}

public class SignatureVector
{
    public string Name { get; set; } = "";
    public string PrivateKey { get; set; } = "";
    public string PublicKey { get; set; } = "";
    public string Message { get; set; } = "";
    public string Signature { get; set; } = "";
}

public class BcsVectorFile
{
    public string? Version { get; set; }
    public List<BcsVector>? Vectors { get; set; }
}

public class BcsVector
{
    public string Name { get; set; } = "";
    public string Type { get; set; } = "";
    public object? Value { get; set; }
    public string Expected { get; set; } = "";
}

public class MnemonicVectorFile
{
    public string? Version { get; set; }
    public List<MnemonicVector>? Vectors { get; set; }
}

public class MnemonicVector
{
    public string Name { get; set; } = "";
    public string Mnemonic { get; set; } = "";
    public string DerivationPath { get; set; } = "";
    public string PrivateKey { get; set; } = "";
    public string PublicKey { get; set; } = "";
    public string Address { get; set; } = "";
}

public class TypeTagVectorFile
{
    public string? Version { get; set; }
    public List<TypeTagVector>? Vectors { get; set; }
}

public class TypeTagVector
{
    public string Name { get; set; } = "";
    public string Input { get; set; } = "";
    public string Expected { get; set; } = "";
    public bool ShouldFail { get; set; }
}

public class TransactionVectorFile
{
    public string? Version { get; set; }
    public List<TransactionVector>? Vectors { get; set; }
}

public class TransactionVector
{
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    // Add more fields as needed based on actual test-vectors/transactions.json structure
}
