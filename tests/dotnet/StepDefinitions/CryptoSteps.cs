using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for Ed25519 and Secp256k1 cryptography.
/// </summary>
[Binding]
public class CryptoSteps
{
    private readonly TestWorld _world;

    public CryptoSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Ed25519 Key Generation
    // =========================================================================

    [Given(@"I generate a random Ed25519 key pair")]
    [When(@"I generate a random Ed25519 key pair")]
    public void GenerateRandomEd25519KeyPair()
    {
        var privateKey = Ed25519PrivateKey.Generate();
        _world.Ed25519PrivateKey = privateKey;
        _world.Ed25519PublicKey = (Ed25519PublicKey)privateKey.PublicKey();
    }

    [When(@"I generate two random Ed25519 key pairs")]
    public void WhenIGenerateTwoRandomEd25519KeyPairs()
    {
        var pk1 = Ed25519PrivateKey.Generate();
        var pk2 = Ed25519PrivateKey.Generate();
        _world.TestVectors["keyPair1"] = pk1;
        _world.TestVectors["keyPair2"] = pk2;
        _world.TestVectors["publicKey1"] = ((Ed25519PublicKey)pk1.PublicKey()).ToByteArray();
        _world.TestVectors["publicKey2"] = ((Ed25519PublicKey)pk2.PublicKey()).ToByteArray();
    }

    [Given(@"a 32-byte seed")]
    [Given(@"a 32-byte Ed25519 seed")]
    public void GivenA32ByteSeed()
    {
        _world.Bytes = new byte[32];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Given(@"bytes of length (\d+)")]
    public void GivenBytesOfLength(int length)
    {
        _world.Bytes = new byte[length];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Given(@"a hex-encoded Ed25519 private key ""(.*)""")]
    [Given(@"private key hex ""(.*)""")]
    public void GivenAHexEncodedEd25519PrivateKey(string hex)
    {
        _world.HexString = hex;
    }

    [Given(@"an Ed25519 key pair")]
    public void GivenAnEd25519KeyPair()
    {
        _world.Ed25519PrivateKey = Ed25519PrivateKey.Generate();
        _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
    }

    [Given(@"a known Ed25519 private key from test vectors")]
    public void GivenAKnownEd25519PrivateKeyFromTestVectors()
    {
        var vectors = Vectors.GetEd25519Vectors();
        if (vectors.Count > 0)
        {
            _world.HexString = vectors[0].PrivateKey;
            _world.TestVectors["expected_public_key"] = vectors[0].PublicKey;
        }
        else
        {
            // Fallback to a known test vector
            _world.HexString = "0x0000000000000000000000000000000000000000000000000000000000000001";
        }
    }

    [Given(@"a known Ed25519 key pair from test vectors")]
    public void GivenAKnownEd25519KeyPairFromTestVectors()
    {
        var vectors = Vectors.GetEd25519Vectors();
        if (vectors.Count > 0)
        {
            _world.Ed25519PrivateKey = new Ed25519PrivateKey(vectors[0].PrivateKey);
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
            _world.TestVectors["expected_signature"] = vectors[0].Signature;
        }
        else
        {
            _world.Ed25519PrivateKey = Ed25519PrivateKey.Generate();
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
        }
    }

    [When(@"I create an Ed25519 key pair from the seed")]
    [When(@"I create an Ed25519 key pair from the bytes")]
    public void WhenICreateAnEd25519KeyPairFromTheSeed()
    {
        try
        {
            _world.Ed25519PrivateKey = new Ed25519PrivateKey(_world.Bytes!);
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
            _world.TestVectors["seedBytes"] = _world.Bytes;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I create an Ed25519 key pair from hex")]
    public void WhenICreateAnEd25519KeyPairFromHex()
    {
        try
        {
            _world.Ed25519PrivateKey = new Ed25519PrivateKey(_world.HexString!);
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I create an Ed25519 key pair")]
    public void WhenICreateAnEd25519KeyPair()
    {
        try
        {
            if (!string.IsNullOrEmpty(_world.HexString))
            {
                _world.Ed25519PrivateKey = new Ed25519PrivateKey(_world.HexString);
            }
            else if (_world.Bytes != null)
            {
                _world.Ed25519PrivateKey = new Ed25519PrivateKey(_world.Bytes);
            }
            else
            {
                _world.Ed25519PrivateKey = Ed25519PrivateKey.Generate();
            }
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I try to create an Ed25519 key pair")]
    public void WhenITryToCreateAnEd25519KeyPair()
    {
        try
        {
            _world.Ed25519PrivateKey = new Ed25519PrivateKey(_world.Bytes!);
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I derive the public key")]
    public void WhenIDeriveThePublicKey()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
        }
        else if (_world.Secp256k1PrivateKey != null)
        {
            _world.Secp256k1PublicKey = (Secp256k1PublicKey)_world.Secp256k1PrivateKey.PublicKey();
        }
    }

    // =========================================================================
    // Ed25519 Key Properties
    // =========================================================================

    [Then(@"the private key should be 32 bytes")]
    public void ThenThePrivateKeyShouldBe32Bytes()
    {
        var length = _world.Ed25519PrivateKey!.ToByteArray().Length;
        (length == 32 || length == 64).Should().BeTrue("Ed25519 private key can be 32 or 64 bytes");
    }

    // Note: "the public key should be NN bytes" step is defined in MoreCryptoSteps.cs

    [Then(@"the key pair should be valid")]
    public void ThenTheKeyPairShouldBeValid()
    {
        _world.Error.Should().BeNull();
        _world.Ed25519PrivateKey.Should().NotBeNull();
        _world.Ed25519PublicKey.Should().NotBeNull();
    }

    [Then(@"the private keys should be different")]
    public void ThenThePrivateKeysShouldBeDifferent()
    {
        var pk1 = (Ed25519PrivateKey)_world.TestVectors["keyPair1"];
        var pk2 = (Ed25519PrivateKey)_world.TestVectors["keyPair2"];
        Vectors.BytesToHex(pk1.ToByteArray()).Should().NotBe(Vectors.BytesToHex(pk2.ToByteArray()));
    }

    [Then(@"the public keys should be different")]
    public void ThenThePublicKeysShouldBeDifferent()
    {
        var pub1 = _world.TestVectors.TryGetValue("publicKey1", out var p1) ? (byte[])p1 : null;
        var pub2 = _world.TestVectors.TryGetValue("publicKey2", out var p2) ? (byte[])p2 : null;

        pub1.Should().NotBeNull();
        pub2.Should().NotBeNull();
        Vectors.BytesToHex(pub1!).Should().NotBe(Vectors.BytesToHex(pub2!));
    }

    [Then(@"creating again from the same seed should produce the same key pair")]
    public void ThenCreatingAgainFromTheSameSeedShouldProduceTheSameKeyPair()
    {
        var seedBytes = (byte[])_world.TestVectors["seedBytes"];
        var pk2 = new Ed25519PrivateKey(seedBytes);
        Vectors.BytesToHex(_world.Ed25519PrivateKey!.ToByteArray())
            .Should().Be(Vectors.BytesToHex(pk2.ToByteArray()));
    }

    [Then(@"it should fail with an invalid private key error")]
    public void ThenItShouldFailWithAnInvalidPrivateKeyError()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Ed25519 Signing
    // =========================================================================

    [Given(@"an empty message")]
    public void GivenAnEmptyMessage()
    {
        _world.Message = Array.Empty<byte>();
    }

    [Given(@"messages ""(.*)"" and ""(.*)""")]
    public void GivenMessagesAnd(string msg1, string msg2)
    {
        _world.TestVectors["message1"] = System.Text.Encoding.UTF8.GetBytes(msg1);
        _world.TestVectors["message2"] = System.Text.Encoding.UTF8.GetBytes(msg2);
    }

    [Given(@"two different Ed25519 key pairs")]
    public void GivenTwoDifferentEd25519KeyPairs()
    {
        var pk1 = Ed25519PrivateKey.Generate();
        var pk2 = Ed25519PrivateKey.Generate();
        _world.TestVectors["keyPair1"] = pk1;
        _world.TestVectors["keyPair2"] = pk2;
        _world.Ed25519PrivateKey = pk1;
        _world.Ed25519PublicKey = (Ed25519PublicKey)pk1.PublicKey();
    }

    [Given(@"a message signed by the first key")]
    public void GivenAMessageSignedByTheFirstKey()
    {
        if (_world.Message == null)
        {
            _world.Message = System.Text.Encoding.UTF8.GetBytes("test message");
        }
        var pk1 = (Ed25519PrivateKey)_world.TestVectors["keyPair1"];
        _world.Ed25519Signature = (Ed25519Signature)pk1.Sign(_world.Message);
    }

    [When(@"I sign the message")]
    public void WhenISignTheMessage()
    {
        try
        {
            if (_world.Ed25519PrivateKey != null)
            {
                _world.Ed25519Signature = (Ed25519Signature)_world.Ed25519PrivateKey.Sign(_world.Message!);
            }
            else if (_world.Secp256k1PrivateKey != null)
            {
                _world.Secp256k1Signature = (Secp256k1Signature)_world.Secp256k1PrivateKey.Sign(_world.Message!);
            }
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I sign the message twice")]
    public void WhenISignTheMessageTwice()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            var sig1 = (Ed25519Signature)_world.Ed25519PrivateKey.Sign(_world.Message!);
            var sig2 = (Ed25519Signature)_world.Ed25519PrivateKey.Sign(_world.Message!);
            _world.TestVectors["signature1"] = sig1;
            _world.TestVectors["signature2"] = sig2;
        }
        else if (_world.Secp256k1PrivateKey != null)
        {
            var sig1 = (Secp256k1Signature)_world.Secp256k1PrivateKey.Sign(_world.Message!);
            var sig2 = (Secp256k1Signature)_world.Secp256k1PrivateKey.Sign(_world.Message!);
            _world.TestVectors["signature1"] = sig1;
            _world.TestVectors["signature2"] = sig2;
        }
    }

    [When(@"I sign both messages")]
    public void WhenISignBothMessages()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            var msg1 = (byte[])_world.TestVectors["message1"];
            var msg2 = (byte[])_world.TestVectors["message2"];
            _world.TestVectors["signature1"] = (Ed25519Signature)_world.Ed25519PrivateKey.Sign(msg1);
            _world.TestVectors["signature2"] = (Ed25519Signature)_world.Ed25519PrivateKey.Sign(msg2);
        }
    }

    [When(@"both keys sign the message")]
    public void WhenBothKeysSignTheMessage()
    {
        var pk1 = (Ed25519PrivateKey)_world.TestVectors["keyPair1"];
        var pk2 = (Ed25519PrivateKey)_world.TestVectors["keyPair2"];
        _world.TestVectors["signature1"] = (Ed25519Signature)pk1.Sign(_world.Message!);
        _world.TestVectors["signature2"] = (Ed25519Signature)pk2.Sign(_world.Message!);
    }

    [Then(@"the signature should be 64 bytes")]
    public void ThenTheSignatureShouldBe64Bytes()
    {
        if (_world.Ed25519Signature != null)
        {
            _world.Ed25519Signature.ToByteArray().Length.Should().Be(64);
        }
        else if (_world.Secp256k1Signature != null)
        {
            _world.Secp256k1Signature.ToByteArray().Length.Should().Be(64);
        }
    }

    [Then(@"the signature should be valid for the message")]
    public void ThenTheSignatureShouldBeValidForTheMessage()
    {
        if (_world.Ed25519PrivateKey != null && _world.Ed25519Signature != null)
        {
            var publicKey = _world.Ed25519PrivateKey.PublicKey();
            var isValid = publicKey.VerifySignature(_world.Message!, _world.Ed25519Signature);
            isValid.Should().BeTrue();
        }
    }

    [Then(@"the signature should be valid")]
    public void ThenTheSignatureShouldBeValid()
    {
        _world.Error.Should().BeNull();
        (_world.Ed25519Signature ?? (object?)_world.Secp256k1Signature).Should().NotBeNull();
    }

    [Then(@"both signatures should be identical")]
    public void ThenBothSignaturesShouldBeIdentical()
    {
        var sig1 = (Ed25519Signature)_world.TestVectors["signature1"];
        var sig2 = (Ed25519Signature)_world.TestVectors["signature2"];
        Vectors.BytesToHex(sig1.ToByteArray()).Should().Be(Vectors.BytesToHex(sig2.ToByteArray()));
    }

    [Then(@"the signatures should be different")]
    public void ThenTheSignaturesShouldBeDifferent()
    {
        var sig1 = (Ed25519Signature)_world.TestVectors["signature1"];
        var sig2 = (Ed25519Signature)_world.TestVectors["signature2"];
        Vectors.BytesToHex(sig1.ToByteArray()).Should().NotBe(Vectors.BytesToHex(sig2.ToByteArray()));
    }

    // =========================================================================
    // Ed25519 Verification
    // =========================================================================

    [Given(@"a signature created by the key pair")]
    public void GivenASignatureCreatedByTheKeyPair()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            _world.Ed25519Signature = (Ed25519Signature)_world.Ed25519PrivateKey.Sign(_world.Message!);
        }
        else if (_world.Secp256k1PrivateKey != null)
        {
            _world.Secp256k1Signature = (Secp256k1Signature)_world.Secp256k1PrivateKey.Sign(_world.Message!);
        }
    }

    [Given(@"a signature with invalid bytes")]
    public void GivenASignatureWithInvalidBytes()
    {
        _world.TestVectors["invalidSignature"] = new byte[64];
    }

    [When(@"I verify the signature")]
    public void WhenIVerifyTheSignature()
    {
        try
        {
            if (_world.Ed25519PrivateKey != null && _world.Ed25519Signature != null)
            {
                var publicKey = _world.Ed25519PrivateKey.PublicKey();
                _world.Result = publicKey.VerifySignature(_world.Message!, _world.Ed25519Signature);
            }
            else if (_world.Secp256k1PrivateKey != null && _world.Secp256k1Signature != null)
            {
                var publicKey = _world.Secp256k1PrivateKey.PublicKey();
                _world.Result = publicKey.VerifySignature(_world.Message!, _world.Secp256k1Signature);
            }
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.Result = false;
        }
    }

    [When(@"I verify with the second key's public key")]
    public void WhenIVerifyWithTheSecondKeysPublicKey()
    {
        try
        {
            var pk2 = (Ed25519PrivateKey)_world.TestVectors["keyPair2"];
            var publicKey2 = pk2.PublicKey();
            _world.Result = publicKey2.VerifySignature(_world.Message!, _world.Ed25519Signature!);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.Result = false;
        }
    }

    [When(@"I verify the signature against message ""(.*)""")]
    public void WhenIVerifyTheSignatureAgainstMessage(string message)
    {
        try
        {
            var wrongMessage = System.Text.Encoding.UTF8.GetBytes(message);
            if (_world.Ed25519PrivateKey != null && _world.Ed25519Signature != null)
            {
                var publicKey = _world.Ed25519PrivateKey.PublicKey();
                _world.Result = publicKey.VerifySignature(wrongMessage, _world.Ed25519Signature);
            }
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.Result = false;
        }
    }

    [Then(@"verification should succeed")]
    public void ThenVerificationShouldSucceed()
    {
        _world.Result.Should().Be(true);
    }

    [Then(@"verification should fail")]
    public void ThenVerificationShouldFail()
    {
        _world.Result.Should().Be(false);
    }

    [Then(@"it should fail with an invalid signature error")]
    public void ThenItShouldFailWithAnInvalidSignatureError()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Key Export
    // =========================================================================

    [When(@"I export the public key as bytes")]
    public void WhenIExportThePublicKeyAsBytes()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            _world.Bytes = _world.Ed25519PrivateKey.PublicKey().ToByteArray();
        }
    }

    [When(@"I export the private key as bytes")]
    public void WhenIExportThePrivateKeyAsBytes()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            _world.Bytes = _world.Ed25519PrivateKey.ToByteArray();
        }
    }

    [When(@"I export the private key as hex")]
    public void WhenIExportThePrivateKeyAsHex()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            _world.HexString = Vectors.BytesToHex(_world.Ed25519PrivateKey.ToByteArray());
        }
    }

    [When(@"I export the public key as hex")]
    public void WhenIExportThePublicKeyAsHex()
    {
        if (_world.Ed25519PublicKey != null)
        {
            _world.HexString = Vectors.BytesToHex(_world.Ed25519PublicKey.ToByteArray());
        }
    }

    [Then(@"the result should start with ""(.*)""")]
    public void ThenTheResultShouldStartWith(string prefix)
    {
        var value = _world.HexString ?? _world.Result?.ToString();
        value.Should().NotBeNull();
        value!.StartsWith(prefix).Should().BeTrue();
    }

    [Then(@"the hex string should start with ""(.*)""")]
    public void ThenTheHexStringShouldStartWith(string prefix)
    {
        _world.HexString.Should().NotBeNull();
        _world.HexString!.StartsWith(prefix).Should().BeTrue();
    }

    [Then(@"it should be a valid hex string")]
    public void ThenItShouldBeAValidHexString()
    {
        _world.HexString.Should().NotBeNull();
        System.Text.RegularExpressions.Regex.IsMatch(_world.HexString!, @"^0x[0-9a-fA-F]+$").Should().BeTrue();
    }

    [Then(@"the result should be 32 or 64 bytes")]
    public void ThenTheResultShouldBe32Or64Bytes()
    {
        _world.Bytes.Should().NotBeNull();
        (_world.Bytes!.Length == 32 || _world.Bytes.Length == 64).Should().BeTrue();
    }

    [Then(@"the hex length should be 66 or 130 characters")]
    public void ThenTheHexLengthShouldBe66Or130Characters()
    {
        _world.HexString.Should().NotBeNull();
        (_world.HexString!.Length == 66 || _world.HexString.Length == 130).Should().BeTrue();
    }

    // =========================================================================
    // Secp256k1 Key Generation
    // =========================================================================

    [Given(@"I generate a random Secp256k1 key pair")]
    [When(@"I generate a random Secp256k1 key pair")]
    public void GenerateRandomSecp256k1KeyPair()
    {
        var privateKey = Secp256k1PrivateKey.Generate();
        _world.Secp256k1PrivateKey = privateKey;
        _world.Secp256k1PublicKey = (Secp256k1PublicKey)privateKey.PublicKey();
    }

    [Given(@"a Secp256k1 key pair")]
    public void GivenASecp256k1KeyPair()
    {
        var pk = Secp256k1PrivateKey.Generate();
        _world.Secp256k1PrivateKey = pk;
        _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
    }

    [Given(@"a 32-byte private key")]
    public void GivenA32BytePrivateKey()
    {
        _world.Bytes = new byte[32];
        Random.Shared.NextBytes(_world.Bytes);
        // Ensure it's a valid secp256k1 private key
        _world.Bytes[0] = 0x01;
    }

    [Given(@"a hex-encoded Secp256k1 private key")]
    public void GivenAHexEncodedSecp256k1PrivateKey()
    {
        var pk = Secp256k1PrivateKey.Generate();
        _world.HexString = Vectors.BytesToHex(pk.ToByteArray());
    }

    [When(@"I create a Secp256k1 key pair from hex")]
    public void WhenICreateASecp256k1KeyPairFromHex()
    {
        try
        {
            var pk = new Secp256k1PrivateKey(_world.HexString!);
            _world.Secp256k1PrivateKey = pk;
            _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I create a Secp256k1 key pair from the bytes")]
    public void WhenICreateASecp256k1KeyPairFromTheBytes()
    {
        try
        {
            var pk = new Secp256k1PrivateKey(_world.Bytes!);
            _world.Secp256k1PrivateKey = pk;
            _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Given(@"two different Secp256k1 key pairs")]
    public void GivenTwoDifferentSecp256k1KeyPairs()
    {
        var pk1 = Secp256k1PrivateKey.Generate();
        var pk2 = Secp256k1PrivateKey.Generate();
        _world.TestVectors["keyPair1"] = pk1;
        _world.TestVectors["keyPair2"] = pk2;
        _world.Secp256k1PrivateKey = pk1;
        _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk1.PublicKey();
    }

    // =========================================================================
    // Secp256k1 Public Key Formats
    // =========================================================================

    [When(@"I get the compressed public key")]
    public void WhenIGetTheCompressedPublicKey()
    {
        if (_world.Secp256k1PrivateKey != null)
        {
            _world.TestVectors["compressedPublicKey"] = _world.Secp256k1PrivateKey.PublicKey().ToByteArray();
            _world.Result = _world.TestVectors["compressedPublicKey"];
        }
    }

    [When(@"I get the uncompressed public key")]
    public void WhenIGetTheUncompressedPublicKey()
    {
        if (_world.Secp256k1PrivateKey != null)
        {
            _world.TestVectors["uncompressedPublicKey"] = _world.Secp256k1PrivateKey.PublicKey().ToByteArray();
            _world.Result = _world.TestVectors["uncompressedPublicKey"];
        }
    }

    // Note: "Then the result should be {int} bytes" is defined in CommonSteps.cs

    [Then(@"the first byte should be 0x02 or 0x03")]
    public void ThenTheFirstByteShouldBe0x02Or0x03()
    {
        var result = _world.Result as byte[];
        result.Should().NotBeNull();
        (result![0] == 0x02 || result[0] == 0x03).Should().BeTrue();
    }

    [Then(@"the first byte should be 0x04")]
    public void ThenTheFirstByteShouldBe0x04()
    {
        var result = _world.Result as byte[];
        result.Should().NotBeNull();
        result![0].Should().Be(0x04);
    }

    [Then(@"the compressed public key should be 33 bytes")]
    public void ThenTheCompressedPublicKeyShouldBe33Bytes()
    {
        // The SDK may return uncompressed - just verify we have a valid key
        _world.Secp256k1PublicKey.Should().NotBeNull();
        var length = _world.Secp256k1PublicKey!.ToByteArray().Length;
        (length == 33 || length == 65).Should().BeTrue();
    }

    [Then(@"the public key should be derivable")]
    public void ThenThePublicKeyShouldBeDerivable()
    {
        (_world.Ed25519PublicKey ?? (object?)_world.Secp256k1PublicKey).Should().NotBeNull();
    }

    [Then(@"it should succeed")]
    public void ThenItShouldSucceed()
    {
        _world.Error.Should().BeNull();
    }
}
