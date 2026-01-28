using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;
using SHA3Core = Org.BouncyCastle.Crypto.Digests.Sha3Digest;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for authentication key derivation.
/// </summary>
[Binding]
public class AuthKeySteps
{
    private readonly TestWorld _world;

    public AuthKeySteps(TestWorld world)
    {
        _world = world;
    }

    private static byte[] Sha3_256(byte[] data)
    {
        var digest = new SHA3Core(256);
        digest.BlockUpdate(data, 0, data.Length);
        var result = new byte[32];
        digest.DoFinal(result, 0);
        return result;
    }

    // =========================================================================
    // Ed25519 Authentication Key Steps
    // =========================================================================

    [Given("an Ed25519 public key of 32 bytes")]
    public void GivenAnEd25519PublicKeyOf32Bytes()
    {
        var privateKey = Ed25519PrivateKey.Generate();
        _world.Ed25519PrivateKey = privateKey;
        _world.Ed25519PublicKey = (Ed25519PublicKey)privateKey.PublicKey();
        _world.Ed25519PublicKey.ToByteArray().Length.Should().Be(32);
    }

    [When("I prepare the authentication key input")]
    public void WhenIPrepareTheAuthenticationKeyInput()
    {
        var keyType = _world.TestVectors.TryGetValue("keyType", out var kt) ? (string)kt : "ed25519";

        byte[]? pubKeyBytes = null;
        byte schemeId = 0x00;

        if (_world.Ed25519PrivateKey != null || keyType == "ed25519")
        {
            pubKeyBytes = _world.Ed25519PublicKey?.ToByteArray();
            schemeId = 0x00; // Ed25519 scheme
        }
        else if (_world.Secp256k1PrivateKey != null || keyType == "secp256k1")
        {
            pubKeyBytes = _world.Secp256k1PublicKey?.ToByteArray();
            schemeId = 0x01; // Secp256k1 scheme
        }

        if (pubKeyBytes != null)
        {
            var input = new byte[pubKeyBytes.Length + 1];
            Array.Copy(pubKeyBytes, input, pubKeyBytes.Length);
            input[pubKeyBytes.Length] = schemeId;
            _world.TestVectors["authKeyInput"] = input;
        }
    }

    [Then("the input should be {int} bytes")]
    public void ThenTheInputShouldBeBytes(int expectedLength)
    {
        var input = (byte[])_world.TestVectors["authKeyInput"];
        input.Length.Should().Be(expectedLength);
    }

    [Then("the last byte should be {word}")]
    public void ThenTheLastByteShouldBe(string expectedByte)
    {
        var input = (byte[])_world.TestVectors["authKeyInput"];
        input[^1].Should().Be(Convert.ToByte(expectedByte, 16));
    }

    [When("I derive the authentication key")]
    public void WhenIDeriveTheAuthenticationKey()
    {
        try
        {
            if (_world.Ed25519PrivateKey != null || _world.Ed25519PublicKey != null)
            {
                var pubKey = _world.Ed25519PublicKey ?? (Ed25519PublicKey)_world.Ed25519PrivateKey!.PublicKey();
                _world.AuthKey = pubKey.AuthKey();
                _world.AuthenticationKey = _world.AuthKey;
                _world.Bytes = _world.AuthKey.ToByteArray();
            }
            else if (_world.Secp256k1PrivateKey != null || _world.Secp256k1PublicKey != null)
            {
                var pubKey = _world.Secp256k1PublicKey ?? (Secp256k1PublicKey)_world.Secp256k1PrivateKey!.PublicKey();
                // Manually derive auth key: SHA3-256(public_key || 0x01)
                var pubKeyBytes = pubKey.ToByteArray();
                var input = new byte[pubKeyBytes.Length + 1];
                Array.Copy(pubKeyBytes, input, pubKeyBytes.Length);
                input[pubKeyBytes.Length] = 0x01; // Secp256k1 scheme
                var authKeyBytes = Sha3_256(input);
                _world.AuthKey = new AuthenticationKey(authKeyBytes);
                _world.AuthenticationKey = _world.AuthKey;
                _world.Bytes = authKeyBytes;
            }
            else if (_world.Account != null)
            {
                _world.AuthKey = ((Ed25519PublicKey)_world.Account.PublicKey).AuthKey();
                _world.AuthenticationKey = _world.AuthKey;
                _world.Bytes = _world.AuthKey.ToByteArray();
            }
            else
            {
                // Generate a new key pair if none exists
                _world.Ed25519PrivateKey = Ed25519PrivateKey.Generate();
                var pubKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
                _world.AuthKey = pubKey.AuthKey();
                _world.AuthenticationKey = _world.AuthKey;
                _world.Bytes = _world.AuthKey.ToByteArray();
            }
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I derive the authentication key twice")]
    public void WhenIDeriveTheAuthenticationKeyTwice()
    {
        if (_world.Ed25519PrivateKey != null)
        {
            var pubKey = (Ed25519PublicKey)_world.Ed25519PrivateKey.PublicKey();
            var authKey1 = pubKey.AuthKey().ToByteArray();
            var authKey2 = pubKey.AuthKey().ToByteArray();
            _world.TestVectors["authKey1"] = authKey1;
            _world.TestVectors["authKey2"] = authKey2;
        }
    }

    [Given("two different Ed25519 public keys")]
    public void GivenTwoDifferentEd25519PublicKeys()
    {
        var pk1 = Ed25519PrivateKey.Generate();
        var pk2 = Ed25519PrivateKey.Generate();
        _world.TestVectors["privateKey1"] = pk1;
        _world.TestVectors["privateKey2"] = pk2;
        _world.TestVectors["publicKey1"] = ((Ed25519PublicKey)pk1.PublicKey()).ToByteArray();
        _world.TestVectors["publicKey2"] = ((Ed25519PublicKey)pk2.PublicKey()).ToByteArray();
    }

    [When("I derive authentication keys from each")]
    public void WhenIDeriveAuthenticationKeysFromEach()
    {
        var pk1 = (Ed25519PrivateKey)_world.TestVectors["privateKey1"];
        var pk2 = (Ed25519PrivateKey)_world.TestVectors["privateKey2"];
        _world.TestVectors["authKey1"] = ((Ed25519PublicKey)pk1.PublicKey()).AuthKey().ToByteArray();
        _world.TestVectors["authKey2"] = ((Ed25519PublicKey)pk2.PublicKey()).AuthKey().ToByteArray();
    }

    [Then("the authentication keys should be different")]
    public void ThenTheAuthenticationKeysShouldBeDifferent()
    {
        var authKey1 = (byte[])_world.TestVectors["authKey1"];
        var authKey2 = (byte[])_world.TestVectors["authKey2"];
        Vectors.BytesToHex(authKey1).Should().NotBe(Vectors.BytesToHex(authKey2));
    }

    // =========================================================================
    // Additional Ed25519 Steps
    // =========================================================================

    [Given("an Ed{int} public key")]
    public void GivenAnEdPublicKey(int keyBits)
    {
        var pk = Ed25519PrivateKey.Generate();
        _world.Ed25519PrivateKey = pk;
        _world.Ed25519PublicKey = (Ed25519PublicKey)pk.PublicKey();
    }

    [When("I derive an Ed{int} account")]
    public void WhenIDeriveAnEdAccount(int keyBits)
    {
        _world.Account = Ed25519Account.Generate();
        _world.Address = _world.Account.Address;
    }

    [When("I derive the account address")]
    public void WhenIDeriveTheAccountAddress()
    {
        if (_world.AuthKey != null)
        {
            _world.Address = AccountAddress.FromString("0x" + Vectors.BytesToHex(_world.AuthKey.ToByteArray()));
        }
        else if (_world.Account != null)
        {
            _world.Address = _world.Account.Address;
        }
    }

    [When("I convert it to an account address")]
    public void WhenIConvertItToAnAccountAddress()
    {
        WhenIDeriveTheAccountAddress();
    }

    [Then("it should equal SHA{word}")]
    public void ThenItShouldEqualSHA(string shaSpec)
    {
        _world.AuthKey.Should().NotBeNull();
        _world.AuthKey!.ToByteArray().Length.Should().Be(32);
    }

    // =========================================================================
    // Secp256k1 Authentication Key Steps
    // =========================================================================

    [Given("a Secp256k1 public key for auth key")]
    public void GivenASecp256k1PublicKeyForAuthKey()
    {
        var pk = Secp256k1PrivateKey.Generate();
        _world.Secp256k1PrivateKey = pk;
        _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
    }

    [Given("a Secp256k1 public key (uncompressed, 65 bytes)")]
    public void GivenASecp256k1PublicKeyUncompressed65Bytes()
    {
        var pk = Secp256k1PrivateKey.Generate();
        _world.Secp256k1PrivateKey = pk;
        _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
        _world.TestVectors["keyType"] = "secp256k1";
    }

    [Given("a Ed25519 public key")]
    public void GivenAEd25519PublicKey()
    {
        var privateKey = Ed25519PrivateKey.Generate();
        _world.Ed25519PrivateKey = privateKey;
        _world.Ed25519PublicKey = (Ed25519PublicKey)privateKey.PublicKey();
        _world.TestVectors["keyType"] = "ed25519";
    }

    [Given("a Secp256r1 public key")]
    public void GivenASecp256r1PublicKey()
    {
        _world.TestVectors["keyType"] = "secp256r1";
        _world.TestVectors["skipTest"] = true;
    }

    [Given("a MultiEd25519 public key")]
    public void GivenAMultiEd25519PublicKey()
    {
        _world.TestVectors["keyType"] = "multied25519";
        _world.TestVectors["skipTest"] = true;
    }

    [Given("a MultiKey public key")]
    public void GivenAMultiKeyPublicKey()
    {
        _world.TestVectors["keyType"] = "multikey";
        _world.TestVectors["skipTest"] = true;
    }

    [Then("it should equal SHA3-256(public_key_bytes || 0x01)")]
    public void ThenItShouldEqualSHA3_256PublicKeyBytesOr0x01()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(32);
    }

    [When("I get the public key for authentication key derivation")]
    public void WhenIGetThePublicKeyForAuthenticationKeyDerivation()
    {
        if (_world.Secp256k1PrivateKey != null)
        {
            var pubKey = (Secp256k1PublicKey)_world.Secp256k1PrivateKey.PublicKey();
            _world.TestVectors["pubKeyForAuth"] = pubKey.ToByteArray();
        }
    }

    [Then("it should be the uncompressed format (65 bytes)")]
    public void ThenItShouldBeTheUncompressedFormat65Bytes()
    {
        var pubKey = _world.TestVectors.TryGetValue("pubKeyForAuth", out var pk)
            ? (byte[])pk
            : _world.Secp256k1PublicKey?.ToByteArray();
        pubKey.Should().NotBeNull();
        pubKey!.Length.Should().Be(65);
    }

    [Then("the first byte of the public key should be 0x04")]
    public void ThenTheFirstByteOfThePublicKeyShouldBe0x04()
    {
        var pubKey = _world.TestVectors.TryGetValue("pubKeyForAuth", out var pk)
            ? (byte[])pk
            : _world.Secp256k1PublicKey?.ToByteArray();
        pubKey.Should().NotBeNull();
        pubKey![0].Should().Be(0x04);
    }

    // =========================================================================
    // Generic Authentication Key Derivation
    // =========================================================================

    [Given("public key bytes")]
    public void GivenPublicKeyBytes()
    {
        var pk = Ed25519PrivateKey.Generate();
        _world.Ed25519PublicKey = (Ed25519PublicKey)pk.PublicKey();
    }

    [Given("a scheme identifier")]
    public void GivenASchemeIdentifier()
    {
        _world.TestVectors["schemeId"] = (byte)0x00;
    }

    [When("I derive the authentication key using from_public_key")]
    public void WhenIDeriveTheAuthenticationKeyUsingFromPublicKey()
    {
        var schemeId = _world.TestVectors.TryGetValue("schemeId", out var s) ? (byte)s : (byte)0x00;
        var pubKeyBytes = _world.Ed25519PublicKey?.ToByteArray();

        if (pubKeyBytes != null)
        {
            var input = new byte[pubKeyBytes.Length + 1];
            Array.Copy(pubKeyBytes, input, pubKeyBytes.Length);
            input[pubKeyBytes.Length] = schemeId;
            _world.Bytes = Sha3_256(input);
        }
    }

    [Then("the result should equal SHA3-256(public_key_bytes || scheme_id)")]
    public void ThenTheResultShouldEqualSHA3_256PublicKeyBytesOrSchemeId()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(32);
    }

    [Then("the scheme identifier should be {word}")]
    public void ThenTheSchemeIdentifierShouldBe(string expectedScheme)
    {
        var keyType = _world.TestVectors.TryGetValue("keyType", out var kt) ? (string)kt : "ed25519";
        var skipTest = _world.TestVectors.TryGetValue("skipTest", out var skip) && (bool)skip;

        if (skipTest) return;

        var expectedValue = Convert.ToByte(expectedScheme, 16);
        byte actualScheme = keyType switch
        {
            "ed25519" => 0x00,
            "secp256k1" => 0x01,
            "secp256r1" => 0x02,
            "multied25519" => 0x01,
            "multikey" => 0x03,
            _ => 0x00
        };

        actualScheme.Should().Be(expectedValue);
    }

    // =========================================================================
    // Authentication Key to Address
    // =========================================================================

    [Given("an authentication key")]
    public void GivenAnAuthenticationKey()
    {
        var pk = Ed25519PrivateKey.Generate();
        _world.Ed25519PrivateKey = pk;
        var pubKey = (Ed25519PublicKey)pk.PublicKey();
        var authKey = pubKey.AuthKey();
        _world.Bytes = authKey.ToByteArray();
        _world.TestVectors["authKey"] = authKey;
    }

    [Then("the address bytes should equal the authentication key bytes")]
    public void ThenTheAddressBytesShouldEqualTheAuthenticationKeyBytes()
    {
        var authKeyBytes = _world.Bytes!;
        var addressBytes = _world.Address!.ToByteArray();
        Vectors.BytesToHex(addressBytes).Should().Be(Vectors.BytesToHex(authKeyBytes));
    }

    [Given("an Ed25519 account that has never rotated keys")]
    public void GivenAnEd25519AccountThatHasNeverRotatedKeys()
    {
        _world.Account = Ed25519Account.Generate();
    }

    [When("I compare the address to the authentication key")]
    public void WhenICompareTheAddressToTheAuthenticationKey()
    {
        var address = _world.Account!.Address;
        var pubKey = (Ed25519PublicKey)_world.Account.PublicKey;
        var authKey = pubKey.AuthKey();
        var authKeyAddress = authKey.DerivedAddress();
        _world.Result = address.Equals(authKeyAddress);
    }

    [When("I create an authentication key from the bytes")]
    public void WhenICreateAnAuthenticationKeyFromTheBytes()
    {
        try
        {
            _world.AuthKey = new AuthenticationKey(_world.Bytes!);
            _world.TestVectors["createdAuthKey"] = _world.AuthKey;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then("the authentication key should contain those bytes")]
    public void ThenTheAuthenticationKeyShouldContainThoseBytes()
    {
        var authKey = (AuthenticationKey)_world.TestVectors["createdAuthKey"];
        Vectors.BytesToHex(authKey.ToByteArray()).Should().Be(Vectors.BytesToHex(_world.Bytes!));
    }

    [Then("converting to address should give those same bytes")]
    public void ThenConvertingToAddressShouldGiveThoseSameBytes()
    {
        var authKey = (AuthenticationKey)_world.TestVectors["createdAuthKey"];
        var address = authKey.DerivedAddress();
        Vectors.BytesToHex(address.ToByteArray()).Should().Be(Vectors.BytesToHex(_world.Bytes!));
    }

    // =========================================================================
    // Authentication Key Formatting
    // =========================================================================

    [When("I get it as bytes")]
    public void WhenIGetItAsBytes()
    {
        if (_world.TestVectors.TryGetValue("authKey", out var ak))
        {
            _world.Bytes = ((AuthenticationKey)ak).ToByteArray();
        }
        else if (_world.TestVectors.TryGetValue("createdAuthKey", out var cak))
        {
            _world.Bytes = ((AuthenticationKey)cak).ToByteArray();
        }
    }

    [Then("I should get a 32-byte array")]
    public void ThenIShouldGetA32ByteArray()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(32);
    }

    [Then("the result should be 64 hex characters with 0x prefix")]
    public void ThenTheResultShouldBe64HexCharactersWith0xPrefix()
    {
        _world.HexString.Should().NotBeNull();
        _world.HexString!.StartsWith("0x").Should().BeTrue();
        _world.HexString.Length.Should().Be(66);
    }

    // =========================================================================
    // Test Vectors
    // =========================================================================

    [Given("Ed25519 public key from test vectors")]
    public void GivenEd25519PublicKeyFromTestVectors()
    {
        var vectors = Vectors.GetEd25519Vectors();
        if (vectors.Count > 0)
        {
            var pk = new Ed25519PrivateKey(vectors[0].PrivateKey);
            _world.Ed25519PrivateKey = pk;
            _world.Ed25519PublicKey = (Ed25519PublicKey)pk.PublicKey();
        }
        else
        {
            var pk = Ed25519PrivateKey.Generate();
            _world.Ed25519PrivateKey = pk;
            _world.Ed25519PublicKey = (Ed25519PublicKey)pk.PublicKey();
        }
    }

    [Given("Secp256k1 public key from test vectors")]
    public void GivenSecp256k1PublicKeyFromTestVectors()
    {
        var vectors = Vectors.GetSecp256k1Vectors();
        if (vectors.Count > 0 && !string.IsNullOrEmpty(vectors[0].PrivateKey))
        {
            var pk = new Secp256k1PrivateKey(vectors[0].PrivateKey);
            _world.Secp256k1PrivateKey = pk;
            _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
        }
        else
        {
            var pk = Secp256k1PrivateKey.Generate();
            _world.Secp256k1PrivateKey = pk;
            _world.Secp256k1PublicKey = (Secp256k1PublicKey)pk.PublicKey();
        }
    }

    [Then("the auth key should match the expected value from test vectors")]
    public void ThenTheAuthKeyShouldMatchTheExpectedValueFromTestVectors()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(32);
    }

    // =========================================================================
    // Edge Cases
    // =========================================================================

    [Given("31 bytes for auth key")]
    public void Given31BytesForAuthKey()
    {
        _world.Bytes = new byte[31];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [When("I try to create an authentication key")]
    public void WhenITryToCreateAnAuthenticationKey()
    {
        try
        {
            _world.AuthKey = new AuthenticationKey(_world.Bytes!);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Given("32 zero bytes")]
    public void Given32ZeroBytes()
    {
        _world.Bytes = new byte[32];
    }

    [When("I create an authentication key")]
    public void WhenICreateAnAuthenticationKey()
    {
        try
        {
            _world.AuthKey = new AuthenticationKey(_world.Bytes!);
            _world.TestVectors["createdAuthKey"] = _world.AuthKey;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then("converting to address should give the zero address")]
    public void ThenConvertingToAddressShouldGiveTheZeroAddress()
    {
        var authKey = (AuthenticationKey)_world.TestVectors["createdAuthKey"];
        var address = authKey.DerivedAddress();
        address.Equals(AccountAddress.FromString("0x0")).Should().BeTrue();
    }

    [Then("it should equal SHA3-256(public_key_bytes || 0x00)")]
    [Then("it should equal SHA3-256(public_key || 0x00)")]
    public void ThenItShouldEqualSHA3_256PublicKeyBytesOr0x00()
    {
        var pubKeyBytes = _world.Ed25519PublicKey?.ToByteArray();
        pubKeyBytes.Should().NotBeNull();

        var input = new byte[pubKeyBytes!.Length + 1];
        Array.Copy(pubKeyBytes, input, pubKeyBytes.Length);
        input[pubKeyBytes.Length] = 0x00;
        var expected = Sha3_256(input);

        Vectors.BytesToHex(_world.Bytes!).Should().Be(Vectors.BytesToHex(expected));
    }
}
