/**
 * BLS12-381 Cryptography Step Definitions
 *
 * BLS12-381 is not currently supported by the Aptos .NET SDK.
 * These steps throw NotImplementedException to clearly indicate missing functionality.
 */
using Reqnroll;
using FluentAssertions;
using Aptos;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class BLSSteps
{
    private readonly TestWorld _world;

    public BLSSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // BLS Key Pair Generation - NOT IMPLEMENTED in .NET SDK
    // =========================================================================

    [Given("a BLS{word} key pair")]
    public void GivenABLSKeyPair(string variant)
    {
        throw new NotImplementedException($"BLS{variant} key pair generation is not supported by the Aptos .NET SDK");
    }

    [Given("a BLS{word} account")]
    public void GivenABLSAccount(string variant)
    {
        throw new NotImplementedException($"BLS{variant} accounts are not supported by the Aptos .NET SDK");
    }

    [Given("a BLS{word} public key")]
    public void GivenABLSPublicKey(string variant)
    {
        throw new NotImplementedException($"BLS{variant} public keys are not supported by the Aptos .NET SDK");
    }

    [Given("a BLS{word} signature")]
    public void GivenABLSSignature(string variant)
    {
        throw new NotImplementedException($"BLS{variant} signatures are not supported by the Aptos .NET SDK");
    }

    [Given("a BLS public key")]
    public void GivenABLSPublicKey()
    {
        throw new NotImplementedException("BLS public keys are not supported by the Aptos .NET SDK");
    }

    [Given("a BLS public key and its PoP")]
    public void GivenABLSPublicKeyAndItsPoP()
    {
        throw new NotImplementedException("BLS Proof of Possession is not supported by the Aptos .NET SDK");
    }

    [Given("a BLS signature for {string}")]
    public void GivenABLSSignatureFor(string message)
    {
        throw new NotImplementedException("BLS signatures are not supported by the Aptos .NET SDK");
    }

    [Given("a PoP from a different key")]
    public void GivenAPoPFromADifferentKey()
    {
        throw new NotImplementedException("BLS Proof of Possession is not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // BLS Operations - NOT IMPLEMENTED
    // =========================================================================

    [When("I verify the PoP")]
    public void WhenIVerifyThePoP()
    {
        throw new NotImplementedException("BLS PoP verification is not supported by the Aptos .NET SDK");
    }

    [When("I try to parse as BLS public key")]
    public void WhenITryToParseAsBLSPublicKey()
    {
        throw new NotImplementedException("BLS public key parsing is not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Codegen Steps - NOT IMPLEMENTED (external tooling, not SDK feature)
    // =========================================================================

    [Given("a Move struct definition")]
    public void GivenAMoveStructDefinition()
    {
        throw new NotImplementedException("Move ABI/codegen is not a .NET SDK feature");
    }

    [Given("a Move struct {string}")]
    public void GivenAMoveStruct(string structName)
    {
        throw new NotImplementedException("Move ABI/codegen is not a .NET SDK feature");
    }

    [Given("a Move module with doc comments")]
    public void GivenAMoveModuleWithDocComments()
    {
        throw new NotImplementedException("Move ABI/codegen is not a .NET SDK feature");
    }

    [Given("a CLI tool for code generation")]
    public void GivenACLIToolForCodeGeneration()
    {
        throw new NotImplementedException("Code generation CLI is not a .NET SDK feature");
    }

    [Given("a Rust procedural macro")]
    public void GivenARustProceduralMacro()
    {
        throw new NotImplementedException("Rust macros are not applicable to .NET SDK");
    }

    [When("I parse the ABI")]
    public void WhenIParseTheABI()
    {
        throw new NotImplementedException("ABI parsing is not a .NET SDK feature");
    }

    [When("I generate code")]
    public void WhenIGenerateCode()
    {
        throw new NotImplementedException("Code generation is not a .NET SDK feature");
    }

    [When("I generate TypeScript code")]
    public void WhenIGenerateTypeScriptCode()
    {
        throw new NotImplementedException("TypeScript code generation is not a .NET SDK feature");
    }

    [When("I generate Rust code")]
    public void WhenIGenerateRustCode()
    {
        throw new NotImplementedException("Rust code generation is not a .NET SDK feature");
    }

    [When("I generate Python code")]
    public void WhenIGeneratePythonCode()
    {
        throw new NotImplementedException("Python code generation is not a .NET SDK feature");
    }

    [When("I generate Go code")]
    public void WhenIGenerateGoCode()
    {
        throw new NotImplementedException("Go code generation is not a .NET SDK feature");
    }

    // =========================================================================
    // SDK-specific Steps - NOT APPLICABLE to .NET SDK
    // =========================================================================

    [Given("TypeScript SDK")]
    public void GivenTypeScriptSDK()
    {
        throw new NotImplementedException("TypeScript SDK scenarios do not apply to .NET SDK");
    }

    [Given("Rust SDK")]
    public void GivenRustSDK()
    {
        throw new NotImplementedException("Rust SDK scenarios do not apply to .NET SDK");
    }

    [Given("Python SDK")]
    public void GivenPythonSDK()
    {
        throw new NotImplementedException("Python SDK scenarios do not apply to .NET SDK");
    }

    [Given("Go SDK")]
    public void GivenGoSDK()
    {
        throw new NotImplementedException("Go SDK scenarios do not apply to .NET SDK");
    }

    [Given("Move types")]
    public void GivenMoveTypes()
    {
        throw new NotImplementedException("Move type codegen is not a .NET SDK feature");
    }

    [Given("Move types {word}")]
    public void GivenMoveTypesSpecific(string types)
    {
        throw new NotImplementedException("Move type codegen is not a .NET SDK feature");
    }

    // =========================================================================
    // Error Scenarios - These are valid test setup steps
    // =========================================================================

    [Given("a SEQUENCE_NUMBER_TOO_OLD error")]
    public void GivenASEQUENCE_NUMBER_TOO_OLD_Error()
    {
        _world.SetError(new Exception("SEQUENCE_NUMBER_TOO_OLD: Transaction sequence number is too old"));
        _world.TestVectors["errorType"] = "SEQUENCE_NUMBER_TOO_OLD";
    }

    [Given("a SHA{int} hash of a message")]
    public void GivenASHAHashOfAMessage(int bits)
    {
        _world.TestVectors["hashBits"] = bits;
        _world.Message = System.Text.Encoding.UTF8.GetBytes("test message");
        if (bits == 256)
        {
            using var sha256 = System.Security.Cryptography.SHA256.Create();
            _world.HashResult = sha256.ComputeHash(_world.Message);
        }
        else if (bits == 3)
        {
            // SHA3-256
            var sha3 = new Org.BouncyCastle.Crypto.Digests.Sha3Digest(256);
            sha3.BlockUpdate(_world.Message, 0, _world.Message.Length);
            _world.HashResult = new byte[32];
            sha3.DoFinal(_world.HashResult, 0);
        }
        else
        {
            throw new NotImplementedException($"SHA{bits} is not implemented");
        }
    }
}
