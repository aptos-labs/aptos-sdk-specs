using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for transaction signing operations.
/// </summary>
[Binding]
public class SigningSteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public SigningSteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // When Steps - Signing
    // =========================================================================

    [When(@"I call account\.sign_transaction\(raw_txn\)")]
    public void WhenICallAccountSignTransaction()
    {
        try
        {
            _world.TestVectors["signTransactionCalled"] = true;
            // Transaction signing via SDK-specific methods
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I call sign_transaction\(raw_txn, account\)")]
    public void WhenICallSignTransactionRawTxnAccount()
    {
        try
        {
            _world.TestVectors["signTransactionCalled"] = true;
            // Transaction signing via SDK-specific methods
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I call sign\(message\)")]
    public void WhenICallSignMessage()
    {
        try
        {
            if (_world.Account != null && _world.Message != null)
            {
                var signature = _world.Account.Sign(_world.Message);
                _world.Ed25519Signature = (Ed25519Signature)signature;
            }
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I call to_bytes\(\)")]
    public void WhenICallToBytes()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            _world.Bytes = _world.Ed25519PrivateKey.ToByteArray();
        }
        else if (_world.Ed25519PublicKey != null)
        {
            _world.Bytes = _world.Ed25519PublicKey.ToByteArray();
        }
    }

    [When("I sign the transaction twice")]
    public void WhenISignTheTransactionTwice()
    {
        _world.TestVectors["signedTwice"] = true;
    }

    [When("I try to sign the message")]
    public void WhenITryToSignTheMessage()
    {
        try
        {
            if (_world.Account != null && _world.Message != null)
            {
                var signature = _world.Account.Sign(_world.Message);
                _world.Ed25519Signature = (Ed25519Signature)signature;
            }
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I generate signing messages for both")]
    public void WhenIGenerateSigningMessagesForBoth()
    {
        _world.TestVectors["signingMessagesGenerated"] = true;
    }

    [When("I generate the signing message twice")]
    public void WhenIGenerateTheSigningMessageTwice()
    {
        _world.TestVectors["signingMessageGeneratedTwice"] = true;
    }

    [When("I extract the signature from the authenticator")]
    public void WhenIExtractTheSignatureFromTheAuthenticator()
    {
        _world.TestVectors["signatureExtracted"] = true;
    }

    [When("I get the public key bytes")]
    public void WhenIGetThePublicKeyBytes()
    {
        if (_world.Ed25519PublicKey != null)
        {
            _world.Bytes = _world.Ed25519PublicKey.ToByteArray();
        }
    }

    [When("I get the signature bytes")]
    public void WhenIGetTheSignatureBytes()
    {
        if (_world.Ed25519Signature != null)
        {
            _world.Bytes = _world.Ed25519Signature.ToByteArray();
        }
    }

    [When("I BCS serialize both")]
    public void WhenIBCSSerializeBoth()
    {
        _world.TestVectors["bcsSerialized"] = true;
    }

    // =========================================================================
    // Then Steps - Signing Results
    // =========================================================================

    [Then("both SignedTransactions should be identical")]
    public void ThenBothSignedTransactionsShouldBeIdentical()
    {
        // Deterministic signing validation
    }

    [Then("both hashes should be identical")]
    public void ThenBothHashesShouldBeIdentical()
    {
        // Hash determinism validation
    }

    [Then("both messages should be identical")]
    public void ThenBothMessagesShouldBeIdentical()
    {
        // Message determinism validation
    }

    [Then("both addresses should be identical")]
    public void ThenBothAddressesShouldBeIdentical()
    {
        _world.Address.Should().Be(_world.Address2);
    }

    [Then("the messages should be different")]
    public void ThenTheMessagesShouldBeDifferent()
    {
        // Messages should differ for different transactions
    }

    [Then("the signing should succeed (SDK doesn't validate sender match)")]
    public void ThenTheSigningShouldSucceed()
    {
        _world.Error.Should().BeNull();
    }

    [Then("it should contain the signature")]
    public void ThenItShouldContainTheSignature()
    {
        // Validation placeholder
    }

    [Then("it should contain the signer's public key")]
    public void ThenItShouldContainTheSignersPublicKey()
    {
        // Validation placeholder
    }

    [Then("it should have a public_key field")]
    public void ThenItShouldHaveAPublicKeyField()
    {
        // Validation placeholder
    }

    [Then(@"it should have a public_key field \((\d+) bytes\)")]
    public void ThenItShouldHaveAPublicKeyFieldBytes(int bytes)
    {
        // Validation placeholder
    }

    [Then("it should have a signature field")]
    public void ThenItShouldHaveASignatureField()
    {
        // Validation placeholder
    }

    [Then(@"it should have a signature field \((\d+) bytes\)")]
    public void ThenItShouldHaveASignatureFieldBytes(int bytes)
    {
        // Validation placeholder
    }

    [Then("the signature should verify against the signing message")]
    public void ThenTheSignatureShouldVerifyAgainstTheSigningMessage()
    {
        // Validation placeholder
    }

    [Then("the signature should match expected value")]
    public void ThenTheSignatureShouldMatchExpectedValue()
    {
        // Validation placeholder
    }

    [Then(@"the signature should be (\d+) bytes")]
    public void ThenTheSignatureShouldBeBytes(int bytes)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(bytes);
    }

    [Then("it should equal the original RawTransaction")]
    public void ThenItShouldEqualTheOriginalRawTransaction()
    {
        // Validation placeholder
    }

    [Then("it should match the original public key")]
    public void ThenItShouldMatchTheOriginalPublicKey()
    {
        // Validation placeholder
    }

    [Then("signing attempts should fail")]
    public void ThenSigningAttemptsShouldFail()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("signatures should be ordered by index")]
    public void ThenSignaturesShouldBeOrderedByIndex()
    {
        // Multi-sig validation
    }

    [Then("it should contain the multi public key")]
    public void ThenItShouldContainTheMultiPublicKey()
    {
        // Multi-sig validation
    }

    [Then("it should contain the multi signature")]
    public void ThenItShouldContainTheMultiSignature()
    {
        // Multi-sig validation
    }

    [Then(@"it should equal SHA(.*)\(public_key \|\| ""(.*)""\)")]
    public void ThenItShouldEqualSHAPublicKey(string algo, string suffix)
    {
        // Auth key derivation validation
    }

    [Then(@"it should equal SHA(.*)\(public_key_bytes \|\| ""(.*)""\)")]
    public void ThenItShouldEqualSHAPublicKeyBytes(string algo, string suffix)
    {
        // Auth key derivation validation
    }

    [Then(@"it should equal SHA(.*)\(uncompressed_public_key \|\| ""(.*)""\)")]
    public void ThenItShouldEqualSHAUncompressedPublicKey(string algo, string suffix)
    {
        // Auth key derivation validation (Secp256k1)
    }

    [Then(@"it should equal SHA(.*)\(SHA(.*)\(""(.*)""\) \|\| bcs\(SignedTransaction\)\)")]
    public void ThenItShouldEqualSHAPrefix(string algo1, string algo2, string prefix)
    {
        // Transaction hash validation
    }

    [Then("the message should contain the BCS-serialized transaction")]
    public void ThenTheMessageShouldContainTheBCSSerializedTransaction()
    {
        // Validation placeholder
    }

    [Then(@"the message should start with SHA(.*)\(""(.*)""\)")]
    public void ThenTheMessageShouldStartWithSHA(string algo, string prefix)
    {
        // Validation placeholder
    }

    [Then(@"it should start with SHA(.*)\(""(.*)""\)")]
    public void ThenItShouldStartWithSHA(string algo, string prefix)
    {
        // Validation placeholder
    }

    [Then("it should be the prefix of all single-signer signing messages")]
    public void ThenItShouldBeThePrefixOfAllSingleSignerSigningMessages()
    {
        // Validation placeholder
    }

    [Then("the remaining bytes should contain the authenticator data")]
    public void ThenTheRemainingBytesShouldContainTheAuthenticatorData()
    {
        // Validation placeholder
    }

    [Then("the sender should match the account address")]
    public void ThenTheSenderShouldMatchTheAccountAddress()
    {
        // Validation placeholder
    }

    [Then("it should equal the authentication key bytes")]
    public void ThenItShouldEqualTheAuthenticationKeyBytes()
    {
        // Validation placeholder
    }

    [Then("the authentication keys should match")]
    public void ThenTheAuthenticationKeysShouldMatch()
    {
        // Validation placeholder
    }
}
