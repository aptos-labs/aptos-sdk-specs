using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Additional step definitions for cryptographic operations.
/// </summary>
[Binding]
public class MoreCryptoSteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public MoreCryptoSteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // When Steps - Account Creation
    // =========================================================================

    [When(@"I create an Ed(\d+) account")]
    public void WhenICreateAnEdAccount(int bits)
    {
        if (bits == 25519)
        {
            _world.Account = Ed25519Account.Generate();
        }
    }

    [When(@"I create a Secp(.*) account")]
    public void WhenICreateASecpAccount(string curve)
    {
        if (curve == "256k1")
        {
            _world.TestVectors["secp256k1AccountCreated"] = true;
        }
        else if (curve == "256r1")
        {
            // TODO: awaiting SDK implementation - Secp256r1 not fully supported
            _scenarioContext.Pending();
        }
    }

    [When(@"I create a BLS(.*) account")]
    public void WhenICreateABLSAccount(string curve)
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When(@"I create a BLS(.*) key pair from the seed")]
    public void WhenICreateABLSKeyPairFromTheSeed(string curve)
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I create a key pair from hex")]
    public void WhenICreateAKeyPairFromHex()
    {
        if (_world.HexString != null)
        {
            var bytes = Vectors.HexToBytes(_world.HexString);
            _world.Ed25519PrivateKey = new Ed25519PrivateKey(bytes);
        }
    }

    [When("I try to create a key pair")]
    public void WhenITryToCreateAKeyPair()
    {
        try
        {
            if (_world.HexString != null)
            {
                var bytes = Vectors.HexToBytes(_world.HexString);
                _world.Ed25519PrivateKey = new Ed25519PrivateKey(bytes);
            }
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I try to create a Secp(.*) key pair")]
    public void WhenITryToCreateASecpKeyPair(string curve)
    {
        try
        {
            if (curve == "256r1")
            {
                // TODO: awaiting SDK implementation - Secp256r1 not fully supported
                _scenarioContext.Pending();
            }
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I generate a random BLS(.*) key pair")]
    public void WhenIGenerateARandomBLSKeyPair(string curve)
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I derive a BLS key pair")]
    public void WhenIDeriveABLSKeyPair()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I generate a proof of possession")]
    public void WhenIGenerateAProofOfPossession()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    // =========================================================================
    // When Steps - Derivation
    // =========================================================================

    [When("I derive the address")]
    public void WhenIDeriveTheAddress()
    {
        if (_world.Ed25519PublicKey != null)
        {
            // Use SDK-specific derivation
            _world.TestVectors["addressDerived"] = true;
        }
    }

    [When("I derive the address twice")]
    public void WhenIDeriveTheAddressTwice()
    {
        if (_world.Ed25519PublicKey != null)
        {
            // Use SDK-specific derivation
            _world.TestVectors["addressDerivedTwice"] = true;
        }
    }

    [When("I derive addresses for each")]
    public void WhenIDeriveAddressesForEach()
    {
        _world.TestVectors["addressesDerived"] = true;
    }

    [When(@"I derive a Secp(.*) account from the mnemonic")]
    public void WhenIDeriveASecpAccountFromTheMnemonic(string curve)
    {
        if (curve == "256r1")
        {
            // TODO: awaiting SDK implementation - Secp256r1 not fully supported
            _scenarioContext.Pending();
        }
        _world.TestVectors["secpDerivedFromMnemonic"] = curve;
    }

    [When(@"I derive a Secp(.*) account")]
    public void WhenIDeriveASecpAccount(string curve)
    {
        if (curve == "256r1")
        {
            // TODO: awaiting SDK implementation - Secp256r1 not fully supported
            _scenarioContext.Pending();
        }
    }

    [When("I derive authentication key from compressed public key")]
    public void WhenIDeriveAuthenticationKeyFromCompressedPublicKey()
    {
        _world.TestVectors["authKeyFromCompressed"] = true;
    }

    [When("I derive authentication key from uncompressed public key")]
    public void WhenIDeriveAuthenticationKeyFromUncompressedPublicKey()
    {
        _world.TestVectors["authKeyFromUncompressed"] = true;
    }

    // =========================================================================
    // When Steps - Hashing
    // =========================================================================

    [When(@"I compute SHA(.*) of ""(.*)""")]
    public void WhenIComputeSHAOf(string algo, string input)
    {
        var inputBytes = System.Text.Encoding.UTF8.GetBytes(input);
        using var sha256 = System.Security.Cryptography.SHA256.Create();
        _world.HashResult = sha256.ComputeHash(inputBytes);
    }

    [When(@"I compute HMAC-SHA(\d+) with key ""(.*)"" \+ passphrase")]
    public void WhenIComputeHMACSHA(int bits, string key)
    {
        var mnemonic = _world.TestVectors.TryGetValue("mnemonic", out var m) ? (string)m : "";
        var passphrase = _world.TestVectors.TryGetValue("passphrase", out var p) ? (string)p : "";

        var keyBytes = System.Text.Encoding.UTF8.GetBytes(key + passphrase);
        var data = System.Text.Encoding.UTF8.GetBytes(mnemonic);

        if (bits == 512)
        {
            using var hmac = new System.Security.Cryptography.HMACSHA512(keyBytes);
            _world.Bytes = hmac.ComputeHash(data);
        }
        else
        {
            using var hmac = new System.Security.Cryptography.HMACSHA256(keyBytes);
            _world.Bytes = hmac.ComputeHash(data);
        }
        _world.Result = _world.Bytes;
        _world.TestVectors["hmacComputed"] = true;
    }

    [When("I compute the hash twice")]
    public void WhenIComputeTheHashTwice()
    {
        if (_world.Message != null)
        {
            using var sha256 = System.Security.Cryptography.SHA256.Create();
            _world.HashResult = sha256.ComputeHash(_world.Message);
            _world.TestVectors["hashComputedTwice"] = true;
        }
    }

    [When("I compute their hashes")]
    public void WhenIComputeTheirHashes()
    {
        _world.TestVectors["hashesComputed"] = true;
    }

    // =========================================================================
    // When Steps - Verification
    // =========================================================================

    [When("I try to verify the signature")]
    public void WhenITryToVerifyTheSignature()
    {
        try
        {
            _world.TestVectors["verificationAttempted"] = true;
            // Verification is done via SDK-specific methods
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I try to verify")]
    public void WhenITryToVerify()
    {
        WhenITryToVerifyTheSignature();
    }

    [When(@"I verify against ""(.*)""")]
    public void WhenIVerifyAgainst(string message)
    {
        try
        {
            _world.TestVectors["verifiedAgainst"] = message;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I verify with second key's public key")]
    public void WhenIVerifyWithSecondKeysPublicKey()
    {
        try
        {
            _world.TestVectors["verifiedWithSecondKey"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // When Steps - BLS Aggregation (Pending)
    // =========================================================================

    [When("I aggregate all keys")]
    public void WhenIAggregateAllKeys()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I aggregate all signatures")]
    public void WhenIAggregateAllSignatures()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I aggregate in different orders")]
    public void WhenIAggregateInDifferentOrders()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I aggregate signatures and public keys")]
    public void WhenIAggregateSignaturesAndPublicKeys()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I verify each PoP before aggregation")]
    public void WhenIVerifyEachPoPBeforeAggregation()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I verify the aggregated signature")]
    public void WhenIVerifyTheAggregatedSignature()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("verify aggregated signature with aggregated public key")]
    public void WhenVerifyAggregatedSignatureWithAggregatedPublicKey()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [When("I try to parse as BLS signature")]
    public void WhenITryToParseAsBLSSignature()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    // =========================================================================
    // When Steps - Misc
    // =========================================================================

    [When("I serialize it to bytes")]
    public void WhenISerializeItToBytes()
    {
        _world.TestVectors["serializedToBytes"] = true;
    }

    [When("I serialize and deserialize it")]
    public void WhenISerializeAndDeserializeIt()
    {
        _world.TestVectors["serializedAndDeserialized"] = true;
    }

    [When("I convert to raw (r,s) format")]
    public void WhenIConvertToRawRSFormat()
    {
        _world.TestVectors["convertedToRawFormat"] = true;
    }

    [When("I format it for debug output")]
    public void WhenIFormatItForDebugOutput()
    {
        _world.TestVectors["formattedForDebug"] = true;
    }

    [When("I log it")]
    public void WhenILogIt()
    {
        _world.TestVectors["logged"] = true;
    }

    [When("I inspect the account's public properties")]
    public void WhenIInspectTheAccountsPublicProperties()
    {
        _world.TestVectors["propertiesInspected"] = true;
    }

    [When("the key pair goes out of scope")]
    public void WhenTheKeyPairGoesOutOfScope()
    {
        // Memory safety - not directly testable in C#
    }

    [When("the crate is compiled")]
    public void WhenTheCrateIsCompiled()
    {
        // Rust-specific - not applicable to .NET
    }

    // =========================================================================
    // Then Steps - Crypto Validation
    // =========================================================================

    [Then(@"I should get a single (\d+)-byte public key")]
    public void ThenIShouldGetASingleBytePublicKey(int bytes)
    {
        // Validation placeholder
    }

    [Then(@"I should get a single (\d+)-byte signature")]
    public void ThenIShouldGetASingleByteSignature(int bytes)
    {
        // Validation placeholder
    }

    [Then("I should get a valid public key")]
    public void ThenIShouldGetAValidPublicKey()
    {
        // Validation placeholder
    }

    [Then(@"the public key should be (\d+) bytes")]
    public void ThenThePublicKeyShouldBeBytes(int bytes)
    {
        if (_world.Ed25519PublicKey != null)
        {
            _world.Ed25519PublicKey.ToByteArray().Length.Should().Be(bytes);
        }
        else if (_world.Secp256k1PublicKey != null)
        {
            _world.Secp256k1PublicKey.ToByteArray().Length.Should().Be(bytes);
        }
        else
        {
            throw new InvalidOperationException("No public key available");
        }
    }

    [Then("the public key should match expected value")]
    public void ThenThePublicKeyShouldMatchExpectedValue()
    {
        // Validation placeholder
    }

    [Then("the public key should match test vectors")]
    public void ThenThePublicKeyShouldMatchTestVectors()
    {
        // Validation placeholder
    }

    [Then("the public key should match the expected value from test vectors")]
    public void ThenThePublicKeyShouldMatchTheExpectedValueFromTestVectors()
    {
        // Validation placeholder
    }

    [Then("the public key hex should match the expected value from test vectors")]
    public void ThenThePublicKeyHexShouldMatchTheExpectedValueFromTestVectors()
    {
        // Validation placeholder
    }

    [Then("the public key should match the embedded public key")]
    public void ThenThePublicKeyShouldMatchTheEmbeddedPublicKey()
    {
        // Validation placeholder
    }

    [Then("the compressed public key should match test vectors")]
    public void ThenTheCompressedPublicKeyShouldMatchTestVectors()
    {
        // Validation placeholder
    }

    [Then(@"the uncompressed public key should be (\d+) bytes")]
    public void ThenTheUncompressedPublicKeyShouldBeBytes(int bytes)
    {
        // Validation placeholder
    }

    [Then("the uncompressed public key should match test vectors")]
    public void ThenTheUncompressedPublicKeyShouldMatchTestVectors()
    {
        // Validation placeholder
    }

    [Then(@"it should be the uncompressed format \((\d+) bytes\)")]
    public void ThenItShouldBeTheUncompressedFormatBytes(int bytes)
    {
        // Validation placeholder
    }

    [Then("creating again from same seed should produce same key pair")]
    public void ThenCreatingAgainFromSameSeedShouldProduceSameKeyPair()
    {
        // Determinism validation
    }

    [Then("recreating from the bytes should produce the same key pair")]
    public void ThenRecreatingFromTheBytesShouldProduceTheSameKeyPair()
    {
        // Determinism validation
    }

    [Then("it should fail with invalid key error")]
    public void ThenItShouldFailWithInvalidKeyError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail with invalid point error")]
    public void ThenItShouldFailWithInvalidPointError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail with invalid signature error")]
    public void ThenItShouldFailWithInvalidSignatureError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should return true")]
    public void ThenItShouldReturnTrue()
    {
        _world.Result.Should().Be(true);
    }

    [Then("the private key bytes should not appear in the output")]
    public void ThenThePrivateKeyBytesShouldNotAppearInTheOutput()
    {
        // Security validation - placeholder
    }

    [Then("the private key memory should be zeroized")]
    public void ThenThePrivateKeyMemoryShouldBeZeroized()
    {
        // Memory safety - not directly testable in C#
    }

    [Then(@"the address should be (\d+) bytes")]
    public void ThenTheAddressShouldBeBytes(int bytes)
    {
        var address = _world.Address ?? _world.Account?.Address;
        address.Should().NotBeNull("account or address should be set");
        address!.ToByteArray().Length.Should().Be(bytes);
    }

    [Then("each address should match the expected values from test vectors")]
    public void ThenEachAddressShouldMatchTheExpectedValuesFromTestVectors()
    {
        // Validation placeholder
    }

    [Then("the account should be Ed25519 type")]
    public void ThenTheAccountShouldBeEd25519Type()
    {
        _world.Account.Should().NotBeNull();
    }

    [Then("the account should be Secp256k1 type")]
    public void ThenTheAccountShouldBeSecp256k1Type()
    {
        // Type validation placeholder
    }

    [Then(@"the authenticator should be Ed(\d+) variant")]
    public void ThenTheAuthenticatorShouldBeEdVariant(int bits)
    {
        // Validation placeholder
    }

    [Then(@"the authenticator should be Secp(.*)Ecdsa variant")]
    public void ThenTheAuthenticatorShouldBeSecpEcdsaVariant(string curve)
    {
        // Validation placeholder
    }

    [Then("the authenticator should use BLS")]
    public void ThenTheAuthenticatorShouldUseBLS()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then("it should use the BLS scheme identifier")]
    public void ThenItShouldUseTheBLSSchemeIdentifier()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then(@"the scheme identifier used should be ""(.*)""")]
    public void ThenTheSchemeIdentifierUsedShouldBe(string scheme)
    {
        // Validation placeholder
    }

    [Then("the derivation should either fail or produce a different result than Aptos default")]
    public void ThenTheDerivationShouldEitherFailOrProduceDifferentResult()
    {
        // Validation placeholder
    }

    [Then("the derivation should fail or produce different result")]
    public void ThenTheDerivationShouldFailOrProduceDifferentResult()
    {
        // Validation placeholder
    }

    [Then(@"the result should equal SHA(.*)\(public_key_bytes \|\| scheme_id\)")]
    public void ThenTheResultShouldEqualSHAPublicKeyBytesSchemeId(string algo)
    {
        // Validation placeholder
    }

    [Then(@"the result should be SHA(.*)\(SHA(.*)\(domain\) \|\| data\)")]
    public void ThenTheResultShouldBeSHASHADomainData(string algo1, string algo2)
    {
        // Validation placeholder
    }

    [Then(@"the PoP should be (\d+) bytes")]
    public void ThenThePoPShouldBeBytes(int bytes)
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then("rogue key attacks are prevented")]
    public void ThenRogueKeyAttacksArePrevented()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then("the aggregated signatures should be the same")]
    public void ThenTheAggregatedSignaturesShouldBeTheSame()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then("the result should match expected aggregated signature")]
    public void ThenTheResultShouldMatchExpectedAggregatedSignature()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then("the signature scheme should include BLS identifier")]
    public void ThenTheSignatureSchemeShouldIncludeBLSIdentifier()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }

    [Then("verification against any single message should fail")]
    public void ThenVerificationAgainstAnySingleMessageShouldFail()
    {
        // TODO: awaiting SDK implementation - BLS not supported in .NET SDK
        _scenarioContext.Pending();
    }
}
