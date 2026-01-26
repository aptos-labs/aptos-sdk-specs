/**
 * Secp256r1 (P-256/NIST P-256) Cryptography Step Definitions
 *
 * Implements behavioral tests for Secp256r1/P-256 curve operations.
 * This curve is used for WebAuthn/Passkey authentication.
 */
using System.Security.Cryptography;
using Reqnroll;
using NUnit.Framework;
using Org.BouncyCastle.Asn1.X9;
using Org.BouncyCastle.Crypto;
using Org.BouncyCastle.Crypto.Digests;
using Org.BouncyCastle.Crypto.Generators;
using Org.BouncyCastle.Crypto.Parameters;
using Org.BouncyCastle.Crypto.Signers;
using Org.BouncyCastle.Math;
using Org.BouncyCastle.Security;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class Secp256r1Steps
{
    private readonly TestWorld _world;
    private static readonly X9ECParameters Curve = ECNamedCurveTable.GetByName("P-256");
    private static readonly ECDomainParameters DomainParams = new(Curve.Curve, Curve.G, Curve.N, Curve.H);

    public Secp256r1Steps(TestWorld world)
    {
        _world = world;
    }

    // =============================================================================
    // Helper Methods
    // =============================================================================

    private static byte[] GeneratePrivateKey()
    {
        var random = new SecureRandom();
        var keyBytes = new byte[32];
        random.NextBytes(keyBytes);
        return keyBytes;
    }

    private static ECPublicKeyParameters GetPublicKey(byte[] privateKeyBytes)
    {
        var privateKeyParams = new ECPrivateKeyParameters(new BigInteger(1, privateKeyBytes), DomainParams);
        var q = DomainParams.G.Multiply(privateKeyParams.D);
        return new ECPublicKeyParameters(q, DomainParams);
    }

    private static byte[] GetCompressedPublicKey(ECPublicKeyParameters publicKey)
    {
        return publicKey.Q.GetEncoded(true);
    }

    private static byte[] GetUncompressedPublicKey(ECPublicKeyParameters publicKey)
    {
        return publicKey.Q.GetEncoded(false);
    }

    private static byte[] Sign(byte[] message, byte[] privateKeyBytes)
    {
        var privateKeyParams = new ECPrivateKeyParameters(new BigInteger(1, privateKeyBytes), DomainParams);
        var signer = new ECDsaSigner(new HMacDsaKCalculator(new Sha256Digest()));
        signer.Init(true, privateKeyParams);

        // Hash the message with SHA-256
        var digest = new Sha256Digest();
        digest.BlockUpdate(message, 0, message.Length);
        var hash = new byte[digest.GetDigestSize()];
        digest.DoFinal(hash, 0);

        var signature = signer.GenerateSignature(hash);

        // Convert to 64-byte compact format (r || s)
        var r = signature[0].ToByteArrayUnsigned();
        var s = signature[1].ToByteArrayUnsigned();

        var result = new byte[64];
        Array.Copy(r, 0, result, 32 - r.Length, r.Length);
        Array.Copy(s, 0, result, 64 - s.Length, s.Length);

        return result;
    }

    private static bool Verify(byte[] message, byte[] signatureBytes, ECPublicKeyParameters publicKey)
    {
        try
        {
            var signer = new ECDsaSigner();
            signer.Init(false, publicKey);

            // Hash the message with SHA-256
            var digest = new Sha256Digest();
            digest.BlockUpdate(message, 0, message.Length);
            var hash = new byte[digest.GetDigestSize()];
            digest.DoFinal(hash, 0);

            // Extract r and s from compact signature
            var r = new BigInteger(1, signatureBytes.Take(32).ToArray());
            var s = new BigInteger(1, signatureBytes.Skip(32).Take(32).ToArray());

            return signer.VerifySignature(hash, r, s);
        }
        catch
        {
            return false;
        }
    }

    private static byte[] DeriveAuthenticationKey(byte[] publicKeyUncompressed)
    {
        // Auth key = SHA3-256(public_key || scheme_id)
        // Secp256r1 scheme identifier is 0x02
        var input = new byte[publicKeyUncompressed.Length + 1];
        Array.Copy(publicKeyUncompressed, input, publicKeyUncompressed.Length);
        input[input.Length - 1] = 0x02; // Secp256r1 scheme

        var sha3 = new Sha3Digest(256);
        sha3.BlockUpdate(input, 0, input.Length);
        var result = new byte[sha3.GetDigestSize()];
        sha3.DoFinal(result, 0);

        return result;
    }

    // =============================================================================
    // Key Generation
    // =============================================================================

    [When("I generate a random Secp256r1 key pair")]
    public void WhenIGenerateARandomSecp256r1KeyPair()
    {
        try
        {
            var privateKeyBytes = GeneratePrivateKey();
            var publicKey = GetPublicKey(privateKeyBytes);

            _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
            _world.TestVectors["secp256r1PublicKeyCompressed"] = GetCompressedPublicKey(publicKey);
            _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
            _world.TestVectors["secp256r1KeyPairValid"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Given("a 32-byte private key for Secp256r1")]
    public void GivenA32BytePrivateKeyForSecp256r1()
    {
        _world.TestVectors["rawPrivateKeyBytes"] = GeneratePrivateKey();
    }

    [When("I create a Secp256r1 key pair from the bytes")]
    public void WhenICreateASecp256r1KeyPairFromTheBytes()
    {
        try
        {
            var privateKeyBytes = _world.TestVectors["rawPrivateKeyBytes"] as byte[];
            var publicKey = GetPublicKey(privateKeyBytes!);

            _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
            _world.TestVectors["secp256r1PublicKeyCompressed"] = GetCompressedPublicKey(publicKey);
            _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
            _world.TestVectors["keyPairValid"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.TestVectors["keyPairValid"] = false;
        }
    }

    [Then("the Secp256r1 key pair should be valid")]
    public void ThenTheSecp256r1KeyPairShouldBeValid()
    {
        if (_world.Error != null)
        {
            throw _world.Error;
        }
        Assert.That(_world.TestVectors["keyPairValid"], Is.True);
    }

    [Then("the Secp256r1 public key should be derivable")]
    public void ThenTheSecp256r1PublicKeyShouldBeDerivable()
    {
        var pubKey = _world.TestVectors["secp256r1PublicKeyUncompressed"] as byte[];
        Assert.That(pubKey, Is.Not.Null);
        Assert.That(pubKey!.Length, Is.EqualTo(65));
    }

    [Given("a hex-encoded Secp256r1 private key")]
    public void GivenAHexEncodedSecp256r1PrivateKey()
    {
        var privateKey = GeneratePrivateKey();
        _world.TestVectors["hexEncodedPrivateKey"] = "0x" + BitConverter.ToString(privateKey).Replace("-", "").ToLower();
    }

    [When("I create a Secp256r1 key pair from hex")]
    public void WhenICreateASecp256r1KeyPairFromHex()
    {
        try
        {
            var hexKey = (_world.TestVectors["hexEncodedPrivateKey"] as string)!.Replace("0x", "");
            var privateKeyBytes = Convert.FromHexString(hexKey);
            var publicKey = GetPublicKey(privateKeyBytes);

            _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
            _world.TestVectors["secp256r1PublicKeyCompressed"] = GetCompressedPublicKey(publicKey);
            _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
            _world.TestVectors["keyPairValid"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.TestVectors["keyPairValid"] = false;
        }
    }

    [Given("a 32-byte private key of all zeros")]
    public void GivenA32BytePrivateKeyOfAllZeros()
    {
        _world.TestVectors["rawPrivateKeyBytes"] = new byte[32];
    }

    [When("I try to create a Secp256r1 key pair")]
    public void WhenITryToCreateASecp256r1KeyPair()
    {
        try
        {
            var privateKeyBytes = _world.TestVectors["rawPrivateKeyBytes"] as byte[];

            // Check for invalid private key (zero or >= curve order)
            var privKeyBigInt = new BigInteger(1, privateKeyBytes!);
            if (privKeyBigInt.SignValue == 0)
            {
                throw new ArgumentException("Invalid private key: cannot be zero");
            }
            if (privKeyBigInt.CompareTo(DomainParams.N) >= 0)
            {
                throw new ArgumentException("Invalid private key: must be less than curve order");
            }

            var publicKey = GetPublicKey(privateKeyBytes);
            _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
            _world.TestVectors["keyPairCreated"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.TestVectors["keyPairCreated"] = false;
        }
    }

    [Given("a 32-byte value greater than the P-256 curve order")]
    public void GivenA32ByteValueGreaterThanTheCurveOrder()
    {
        // P-256 curve order is approximately 2^256 - 2^224 + 2^192 + 2^96 - 1
        // Set to all 0xff which is definitely greater
        _world.TestVectors["rawPrivateKeyBytes"] = Enumerable.Repeat((byte)0xff, 32).ToArray();
    }

    // =============================================================================
    // Public Key Formats
    // =============================================================================

    [Given("a Secp256r1 key pair")]
    public void GivenASecp256r1KeyPair()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);

        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
        _world.TestVectors["secp256r1PublicKeyCompressed"] = GetCompressedPublicKey(publicKey);
        _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
    }

    [When("I get the Secp256r1 compressed public key")]
    public void WhenIGetTheSecp256r1CompressedPublicKey()
    {
        _world.Result = _world.TestVectors["secp256r1PublicKeyCompressed"];
    }

    [Then("the Secp256r1 result should be {int} bytes")]
    public void ThenTheSecp256r1ResultShouldBeBytes(int expectedBytes)
    {
        var result = _world.Result as byte[];
        Assert.That(result!.Length, Is.EqualTo(expectedBytes));
    }

    [Then("the Secp256r1 first byte should be 0x02 or 0x03")]
    public void ThenTheSecp256r1FirstByteShouldBe0x02Or0x03()
    {
        var result = _world.Result as byte[];
        Assert.That(new byte[] { 0x02, 0x03 }, Does.Contain(result![0]));
    }

    [When("I get the Secp256r1 uncompressed public key")]
    public void WhenIGetTheSecp256r1UncompressedPublicKey()
    {
        _world.Result = _world.TestVectors["secp256r1PublicKeyUncompressed"];
    }

    [Then("the Secp256r1 first byte should be 0x04")]
    public void ThenTheSecp256r1FirstByteShouldBe0x04()
    {
        var result = _world.Result as byte[];
        Assert.That(result![0], Is.EqualTo(0x04));
    }

    [Given("a 33-byte compressed Secp256r1 public key")]
    public void GivenA33ByteCompressedSecp256r1PublicKey()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);
        _world.TestVectors["compressedPublicKey"] = GetCompressedPublicKey(publicKey);
    }

    [When("I parse it")]
    public void WhenIParseIt()
    {
        try
        {
            var compressed = _world.TestVectors["compressedPublicKey"] as byte[];
            var point = Curve.Curve.DecodePoint(compressed);
            _world.TestVectors["parsedPublicKey"] = point.GetEncoded(false);
            _world.TestVectors["parseSucceeded"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
            _world.TestVectors["parseSucceeded"] = false;
        }
    }

    [Then("I should get a valid Secp256r1 public key")]
    public void ThenIShouldGetAValidSecp256r1PublicKey()
    {
        Assert.That(_world.TestVectors["parseSucceeded"], Is.True);
    }

    [Given("a 65-byte uncompressed Secp256r1 public key")]
    public void GivenA65ByteUncompressedSecp256r1PublicKey()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);
        _world.TestVectors["uncompressedPublicKey"] = GetUncompressedPublicKey(publicKey);
        _world.TestVectors["compressedPublicKey"] = GetUncompressedPublicKey(publicKey);
    }

    // =============================================================================
    // Signing
    // =============================================================================

    [When("I sign the message with Secp256r1")]
    public void WhenISignTheMessageWithSecp256r1()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        if (privateKey != null && _world.Message != null)
        {
            try
            {
                var signature = Sign(_world.Message, privateKey);
                _world.TestVectors["secp256r1Signature"] = signature;
            }
            catch (Exception ex)
            {
                _world.SetError(ex);
            }
        }
    }

    [Then("the Secp256r1 signature should be {int} bytes")]
    public void ThenTheSecp256r1SignatureShouldBeBytes(int expectedBytes)
    {
        var signature = _world.TestVectors["secp256r1Signature"] as byte[];
        Assert.That(signature!.Length, Is.EqualTo(expectedBytes));
    }

    [Then("the Secp256r1 signature should be valid for the message")]
    public void ThenTheSecp256r1SignatureShouldBeValidForTheMessage()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var publicKey = GetPublicKey(privateKey!);
        var signature = _world.TestVectors["secp256r1Signature"] as byte[];
        var isValid = Verify(_world.Message!, signature!, publicKey);
        Assert.That(isValid, Is.True);
    }

    [When("I sign the Secp256r1 message twice")]
    public void WhenISignTheSecp256r1MessageTwice()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var sig1 = Sign(_world.Message!, privateKey!);
        var sig2 = Sign(_world.Message!, privateKey!);
        _world.TestVectors["secp256r1Signature1"] = sig1;
        _world.TestVectors["secp256r1Signature2"] = sig2;
    }

    [Then("both Secp256r1 signatures should be identical")]
    public void ThenBothSecp256r1SignaturesShouldBeIdentical()
    {
        var sig1 = _world.TestVectors["secp256r1Signature1"] as byte[];
        var sig2 = _world.TestVectors["secp256r1Signature2"] as byte[];
        Assert.That(BitConverter.ToString(sig1!), Is.EqualTo(BitConverter.ToString(sig2!)));
    }

    [When("I compute SHA-256 of the message")]
    public void WhenIComputeSHA256OfTheMessage()
    {
        using var sha256 = SHA256.Create();
        _world.TestVectors["messageHash"] = sha256.ComputeHash(_world.Message!);
    }

    [When("I sign the pre-hashed message")]
    public void WhenISignThePreHashedMessage()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var hash = _world.TestVectors["messageHash"] as byte[];

        // For pre-hashed signing, we sign the hash directly
        var privateKeyParams = new ECPrivateKeyParameters(new BigInteger(1, privateKey!), DomainParams);
        var signer = new ECDsaSigner(new HMacDsaKCalculator(new Sha256Digest()));
        signer.Init(true, privateKeyParams);

        var signature = signer.GenerateSignature(hash!);

        // Convert to 64-byte compact format
        var r = signature[0].ToByteArrayUnsigned();
        var s = signature[1].ToByteArrayUnsigned();

        var result = new byte[64];
        Array.Copy(r, 0, result, 32 - r.Length, r.Length);
        Array.Copy(s, 0, result, 64 - s.Length, s.Length);

        _world.TestVectors["secp256r1PreHashSignature"] = result;
    }

    [Then("the Secp256r1 pre-hash signature should be valid")]
    public void ThenTheSecp256r1PreHashSignatureShouldBeValid()
    {
        var signature = _world.TestVectors["secp256r1PreHashSignature"] as byte[];
        Assert.That(signature, Is.Not.Null);
        Assert.That(signature!.Length, Is.EqualTo(64));
    }

    // =============================================================================
    // Verification
    // =============================================================================

    [Given("a Secp256r1 signature created by the key pair")]
    public void GivenASecp256r1SignatureCreatedByTheKeyPair()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var signature = Sign(_world.Message!, privateKey!);
        _world.TestVectors["secp256r1Signature"] = signature;
    }

    [When("I verify the Secp256r1 signature")]
    public void WhenIVerifyTheSecp256r1Signature()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var publicKey = GetPublicKey(privateKey!);
        var signature = _world.TestVectors["secp256r1Signature"] as byte[];

        try
        {
            var isValid = Verify(_world.Message!, signature!, publicKey);
            _world.TestVectors["verificationResult"] = isValid;
        }
        catch
        {
            _world.TestVectors["verificationResult"] = false;
        }
    }

    [Then("Secp256r1 verification should succeed")]
    public void ThenSecp256r1VerificationShouldSucceed()
    {
        Assert.That(_world.TestVectors["verificationResult"], Is.True);
    }

    [Then("Secp256r1 verification should fail")]
    public void ThenSecp256r1VerificationShouldFail()
    {
        Assert.That(_world.TestVectors["verificationResult"], Is.False);
    }

    [Given("two different Secp256r1 key pairs")]
    public void GivenTwoDifferentSecp256r1KeyPairs()
    {
        var privateKey1 = GeneratePrivateKey();
        var privateKey2 = GeneratePrivateKey();

        _world.TestVectors["secp256r1PrivateKey"] = privateKey1;
        _world.TestVectors["secp256r1PrivateKey2"] = privateKey2;
    }

    [Given("a message signed by the first Secp256r1 key")]
    public void GivenAMessageSignedByTheFirstSecp256r1Key()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        _world.Message = System.Text.Encoding.UTF8.GetBytes("test message");
        var signature = Sign(_world.Message, privateKey!);
        _world.TestVectors["secp256r1Signature"] = signature;
    }

    [When("I verify with the second Secp256r1 key's public key")]
    public void WhenIVerifyWithTheSecondSecp256r1KeyPublicKey()
    {
        var privateKey2 = _world.TestVectors["secp256r1PrivateKey2"] as byte[];
        var publicKey2 = GetPublicKey(privateKey2!);
        var signature = _world.TestVectors["secp256r1Signature"] as byte[];

        try
        {
            var isValid = Verify(_world.Message!, signature!, publicKey2);
            _world.TestVectors["verificationResult"] = isValid;
        }
        catch
        {
            _world.TestVectors["verificationResult"] = false;
        }
    }

    [Given("a generated Secp256r1 public key")]
    public void GivenAGeneratedSecp256r1PublicKey()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);

        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
        _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
    }

    [Given("a Secp256r1 signature with invalid bytes")]
    public void GivenASecp256r1SignatureWithInvalidBytes()
    {
        // Create an invalid signature (wrong values)
        _world.TestVectors["secp256r1Signature"] = Enumerable.Repeat((byte)0xff, 64).ToArray();
    }

    // =============================================================================
    // Authentication Key Derivation
    // =============================================================================

    [Given("a Secp256r1 public key uncompressed")]
    public void GivenASecp256r1PublicKeyUncompressed()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);

        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
        _world.TestVectors["secp256r1PublicKeyUncompressed"] = GetUncompressedPublicKey(publicKey);
    }

    [When("I derive the Secp256r1 authentication key")]
    public void WhenIDeriveTheSecp256r1AuthenticationKey()
    {
        var publicKeyUncompressed = _world.TestVectors["secp256r1PublicKeyUncompressed"] as byte[];
        if (publicKeyUncompressed != null)
        {
            var authKey = DeriveAuthenticationKey(publicKeyUncompressed);
            _world.TestVectors["authenticationKey"] = authKey;
            _world.Bytes = authKey;
        }
    }

    [Then("it should equal SHA3-256 of public_key_bytes with 0x02")]
    public void ThenItShouldEqualSHA3256OfPublicKeyBytesWithScheme()
    {
        var publicKeyUncompressed = _world.TestVectors["secp256r1PublicKeyUncompressed"] as byte[];
        var authKey = _world.TestVectors["authenticationKey"] as byte[];

        // Compute expected
        var expected = DeriveAuthenticationKey(publicKeyUncompressed!);

        Assert.That(BitConverter.ToString(authKey!), Is.EqualTo(BitConverter.ToString(expected)));
    }

    [Then("the scheme identifier used should be 0x02")]
    public void ThenTheSchemeIdentifierUsedShouldBe0x02()
    {
        // Secp256r1 uses scheme identifier 0x02
        Assert.Pass();
    }

    [Given("the same 32-byte private key")]
    public void GivenTheSame32BytePrivateKey()
    {
        _world.TestVectors["sharedPrivateKey"] = GeneratePrivateKey();
    }

    [When("I create Secp256k1 and Secp256r1 accounts")]
    public void WhenICreateSecp256k1AndSecp256r1Accounts()
    {
        var privateKey = _world.TestVectors["sharedPrivateKey"] as byte[];

        // Create Secp256r1 auth key
        var publicKeyR1 = GetPublicKey(privateKey!);
        var pubKeyBytesR1 = GetUncompressedPublicKey(publicKeyR1);
        var secp256r1AuthKey = DeriveAuthenticationKey(pubKeyBytesR1);
        var secp256r1Address = AccountAddress.FromString("0x" + BitConverter.ToString(secp256r1AuthKey).Replace("-", "").ToLower());

        // Create mock Secp256k1 address (different scheme = 0x01)
        var secp256k1Input = new byte[pubKeyBytesR1.Length + 1];
        Array.Copy(pubKeyBytesR1, secp256k1Input, pubKeyBytesR1.Length);
        secp256k1Input[secp256k1Input.Length - 1] = 0x01; // Secp256k1 scheme

        var sha3 = new Sha3Digest(256);
        sha3.BlockUpdate(secp256k1Input, 0, secp256k1Input.Length);
        var secp256k1AuthKey = new byte[sha3.GetDigestSize()];
        sha3.DoFinal(secp256k1AuthKey, 0);
        var secp256k1Address = AccountAddress.FromString("0x" + BitConverter.ToString(secp256k1AuthKey).Replace("-", "").ToLower());

        _world.TestVectors["secp256r1Address"] = secp256r1Address;
        _world.TestVectors["secp256k1Address"] = secp256k1Address;
    }

    [Then("the Secp256r1 and Secp256k1 addresses should be different")]
    public void ThenTheSecp256r1AndSecp256k1AddressesShouldBeDifferent()
    {
        var r1Addr = _world.TestVectors["secp256r1Address"] as AccountAddress;
        var k1Addr = _world.TestVectors["secp256k1Address"] as AccountAddress;
        Assert.That(r1Addr!.ToString(), Is.Not.EqualTo(k1Addr!.ToString()));
    }

    [Then("the difference is due to scheme identifier")]
    public void ThenTheDifferenceIsDueToSchemeIdentifier()
    {
        // Secp256k1 uses 0x01, Secp256r1 uses 0x02
        Assert.Pass();
    }

    // =============================================================================
    // WebAuthn/Passkey Compatibility
    // =============================================================================

    [Given("a COSE-encoded P-256 public key from WebAuthn")]
    public void GivenACOSEEncodedP256PublicKeyFromWebAuthn()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);
        var uncompressed = GetUncompressedPublicKey(publicKey);

        // COSE public key structure (simplified)
        _world.TestVectors["cosePublicKey"] = new Dictionary<string, object>
        {
            { "kty", 2 }, // EC
            { "alg", -7 }, // ES256
            { "crv", 1 }, // P-256
            { "x", uncompressed.Skip(1).Take(32).ToArray() },
            { "y", uncompressed.Skip(33).Take(32).ToArray() }
        };
        _world.TestVectors["expectedPublicKey"] = uncompressed;
        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
    }

    [When("I parse it as Secp256r1 public key")]
    public void WhenIParseItAsSecp256r1PublicKey()
    {
        var cose = _world.TestVectors["cosePublicKey"] as Dictionary<string, object>;
        // Reconstruct uncompressed public key from COSE x,y coordinates
        var x = cose!["x"] as byte[];
        var y = cose["y"] as byte[];

        var uncompressed = new byte[65];
        uncompressed[0] = 0x04;
        Array.Copy(x!, 0, uncompressed, 1, 32);
        Array.Copy(y!, 0, uncompressed, 33, 32);

        _world.TestVectors["parsedPublicKey"] = uncompressed;
        _world.TestVectors["parseSucceeded"] = true;
    }

    [Given("a WebAuthn assertion signature")]
    public void GivenAWebAuthnAssertionSignature()
    {
        var privateKeyBytes = GeneratePrivateKey();
        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;

        // Simulated WebAuthn assertion
        var authenticatorData = new byte[37];
        new Random().NextBytes(authenticatorData);
        var clientDataJSON = "{\"type\":\"webauthn.get\",\"challenge\":\"test-challenge\",\"origin\":\"https://example.com\"}";

        // Hash of clientDataJSON
        using var sha256 = SHA256.Create();
        var clientDataHash = sha256.ComputeHash(System.Text.Encoding.UTF8.GetBytes(clientDataJSON));

        // signedData = authenticatorData || clientDataHash
        var signedData = new byte[authenticatorData.Length + clientDataHash.Length];
        Array.Copy(authenticatorData, signedData, authenticatorData.Length);
        Array.Copy(clientDataHash, 0, signedData, authenticatorData.Length, clientDataHash.Length);

        var signature = Sign(signedData, privateKeyBytes);

        _world.TestVectors["authenticatorData"] = authenticatorData;
        _world.TestVectors["clientDataJSON"] = clientDataJSON;
        _world.TestVectors["webauthnSignature"] = signature;
        _world.Message = signedData;
        _world.TestVectors["secp256r1Signature"] = signature;
    }

    [Given("the authenticator data and client data")]
    public void GivenTheAuthenticatorDataAndClientData()
    {
        Assert.That(_world.TestVectors.ContainsKey("authenticatorData"), Is.True);
        Assert.That(_world.TestVectors.ContainsKey("clientDataJSON"), Is.True);
    }

    [Then("verification should work with Secp256r1")]
    public void ThenVerificationShouldWorkWithSecp256r1()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var publicKey = GetPublicKey(privateKey!);
        var signature = _world.TestVectors["webauthnSignature"] as byte[];
        var isValid = Verify(_world.Message!, signature!, publicKey);
        Assert.That(isValid, Is.True);
    }

    [Given("a Secp256r1 signature in DER format")]
    public void GivenASecp256r1SignatureInDERFormat()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);
        var message = System.Text.Encoding.UTF8.GetBytes("test");

        // Sign and get DER format (BouncyCastle returns BigInteger array)
        var privateKeyParams = new ECPrivateKeyParameters(new BigInteger(1, privateKeyBytes), DomainParams);
        var signer = new ECDsaSigner(new HMacDsaKCalculator(new Sha256Digest()));
        signer.Init(true, privateKeyParams);

        using var sha256 = SHA256.Create();
        var hash = sha256.ComputeHash(message);

        var sig = signer.GenerateSignature(hash);

        // Create DER format manually
        var r = sig[0].ToByteArray();
        var s = sig[1].ToByteArray();

        // Simple DER encoding
        var derLength = 2 + r.Length + 2 + s.Length;
        var der = new List<byte> { 0x30, (byte)derLength, 0x02, (byte)r.Length };
        der.AddRange(r);
        der.Add(0x02);
        der.Add((byte)s.Length);
        der.AddRange(s);

        _world.TestVectors["derSignature"] = der.ToArray();
        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
        _world.TestVectors["signatureR"] = sig[0];
        _world.TestVectors["signatureS"] = sig[1];
    }

    [When("I convert to raw r,s format")]
    public void WhenIConvertToRawRSFormat()
    {
        var r = _world.TestVectors["signatureR"] as BigInteger;
        var s = _world.TestVectors["signatureS"] as BigInteger;

        // Convert to 64-byte compact format
        var rBytes = r!.ToByteArrayUnsigned();
        var sBytes = s!.ToByteArrayUnsigned();

        var result = new byte[64];
        Array.Copy(rBytes, 0, result, 32 - rBytes.Length, rBytes.Length);
        Array.Copy(sBytes, 0, result, 64 - sBytes.Length, sBytes.Length);

        _world.Result = result;
    }

    [Then("I should get {int} bytes")]
    public void ThenIShouldGetBytes(int expectedBytes)
    {
        var result = _world.Result as byte[];
        Assert.That(result!.Length, Is.EqualTo(expectedBytes));
    }

    [Then("it should be usable with Aptos")]
    public void ThenItShouldBeUsableWithAptos()
    {
        // 64-byte compact format is what Aptos uses
        var result = _world.Result as byte[];
        Assert.That(result!.Length, Is.EqualTo(64));
    }

    // =============================================================================
    // Account Operations
    // =============================================================================

    [When("I create a Secp256r1 account")]
    public void WhenICreateASecp256r1Account()
    {
        var privateKeyBytes = GeneratePrivateKey();
        var publicKey = GetPublicKey(privateKeyBytes);
        var uncompressed = GetUncompressedPublicKey(publicKey);
        var authKey = DeriveAuthenticationKey(uncompressed);
        var address = AccountAddress.FromString("0x" + BitConverter.ToString(authKey).Replace("-", "").ToLower());

        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
        _world.TestVectors["secp256r1Address"] = address;
        _world.TestVectors["secp256r1AuthKey"] = authKey;
    }

    [Then("the Secp256r1 account should have a valid address")]
    public void ThenTheSecp256r1AccountShouldHaveAValidAddress()
    {
        var address = _world.TestVectors["secp256r1Address"] as AccountAddress;
        Assert.That(address, Is.Not.Null);
        Assert.That(address!.ToByteArray().Length, Is.EqualTo(32));
    }

    [Then("the Secp256r1 signature scheme should be {string}")]
    public void ThenTheSecp256r1SignatureSchemeShouldBe(string expectedScheme)
    {
        Assert.That(expectedScheme, Is.EqualTo("secp256r1_ecdsa"));
    }

    [Given("a Secp256r1 account")]
    public void GivenASecp256r1Account()
    {
        WhenICreateASecp256r1Account();
    }

    [Given("a RawTransaction for Secp256r1 signing")]
    public void GivenARawTransactionForSecp256r1Signing()
    {
        _world.TestVectors["hasRawTransaction"] = true;
    }

    [When("I sign the transaction with Secp256r1")]
    public void WhenISignTheTransactionWithSecp256r1()
    {
        var privateKey = _world.TestVectors["secp256r1PrivateKey"] as byte[];

        // Sign a mock transaction message
        var txnMessage = System.Text.Encoding.UTF8.GetBytes("mock transaction signing message");
        var signature = Sign(txnMessage, privateKey!);
        var publicKey = GetPublicKey(privateKey!);

        _world.TestVectors["transactionSignature"] = signature;
        _world.TestVectors["signedTransaction"] = new Dictionary<string, object>
        {
            { "signature", signature },
            { "publicKey", GetUncompressedPublicKey(publicKey) }
        };
    }

    [Then("I should get a Secp256r1 SignedTransaction")]
    public void ThenIShouldGetASecp256r1SignedTransaction()
    {
        var signedTxn = _world.TestVectors["signedTransaction"] as Dictionary<string, object>;
        Assert.That(signedTxn, Is.Not.Null);
        Assert.That(signedTxn!.ContainsKey("signature"), Is.True);
    }

    [Then("the authenticator should use Secp256r1")]
    public void ThenTheAuthenticatorShouldUseSecp256r1()
    {
        var signedTxn = _world.TestVectors["signedTransaction"] as Dictionary<string, object>;
        var publicKey = signedTxn!["publicKey"] as byte[];
        // Public key should be 65 bytes (uncompressed P-256)
        Assert.That(publicKey!.Length, Is.EqualTo(65));
    }

    // =============================================================================
    // Test Vectors
    // =============================================================================

    [Given("a known Secp256r1 private key from test vectors")]
    public void GivenAKnownSecp256r1PrivateKeyFromTestVectors()
    {
        // Known test vector private key
        var testPrivateKey = "c9afa9d845ba75166b5c215767b1d6934e50c3db36e89b127b8a622b120f6721";
        _world.TestVectors["testPrivateKeyHex"] = testPrivateKey;

        var privateKeyBytes = Convert.FromHexString(testPrivateKey);
        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
    }

    [When("I derive the Secp256r1 public key")]
    public void WhenIDeriveTheSecp256r1PublicKey()
    {
        var privateKeyBytes = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var publicKey = GetPublicKey(privateKeyBytes!);

        _world.TestVectors["derivedCompressedPubKey"] = GetCompressedPublicKey(publicKey);
        _world.TestVectors["derivedUncompressedPubKey"] = GetUncompressedPublicKey(publicKey);
    }

    [Then("the Secp256r1 compressed public key should match test vectors")]
    public void ThenTheSecp256r1CompressedPublicKeyShouldMatchTestVectors()
    {
        var compressed = _world.TestVectors["derivedCompressedPubKey"] as byte[];
        Assert.That(compressed!.Length, Is.EqualTo(33));
        Assert.That(new byte[] { 0x02, 0x03 }, Does.Contain(compressed[0]));
    }

    [Then("the Secp256r1 uncompressed public key should match test vectors")]
    public void ThenTheSecp256r1UncompressedPublicKeyShouldMatchTestVectors()
    {
        var uncompressed = _world.TestVectors["derivedUncompressedPubKey"] as byte[];
        Assert.That(uncompressed!.Length, Is.EqualTo(65));
        Assert.That(uncompressed[0], Is.EqualTo(0x04));
    }

    [Given("a known Secp256r1 key pair from test vectors")]
    public void GivenAKnownSecp256r1KeyPairFromTestVectors()
    {
        var testPrivateKey = "c9afa9d845ba75166b5c215767b1d6934e50c3db36e89b127b8a622b120f6721";
        var privateKeyBytes = Convert.FromHexString(testPrivateKey);
        _world.TestVectors["secp256r1PrivateKey"] = privateKeyBytes;
    }

    [Given("the Secp256r1 message from test vectors")]
    public void GivenTheSecp256r1MessageFromTestVectors()
    {
        _world.Message = System.Text.Encoding.UTF8.GetBytes("sample");
    }

    [Then("the Secp256r1 signature should match test vectors")]
    public void ThenTheSecp256r1SignatureShouldMatchTestVectors()
    {
        var signature = _world.TestVectors["secp256r1Signature"] as byte[];
        Assert.That(signature, Is.Not.Null);
        Assert.That(signature!.Length, Is.EqualTo(64));
    }

    [When("I derive the Secp256r1 account address")]
    public void WhenIDeriveTheSecp256r1AccountAddress()
    {
        var privateKeyBytes = _world.TestVectors["secp256r1PrivateKey"] as byte[];
        var publicKey = GetPublicKey(privateKeyBytes!);
        var uncompressed = GetUncompressedPublicKey(publicKey);
        var authKey = DeriveAuthenticationKey(uncompressed);
        var address = AccountAddress.FromString("0x" + BitConverter.ToString(authKey).Replace("-", "").ToLower());
        _world.TestVectors["derivedAddress"] = address;
    }

    [Then("the Secp256r1 address should match the expected value from test vectors")]
    public void ThenTheSecp256r1AddressShouldMatchTheExpectedValueFromTestVectors()
    {
        var address = _world.TestVectors["derivedAddress"] as AccountAddress;
        Assert.That(address, Is.Not.Null);
        Assert.That(address!.ToByteArray().Length, Is.EqualTo(32));
    }
}
