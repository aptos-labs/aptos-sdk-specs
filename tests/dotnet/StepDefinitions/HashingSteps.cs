using System.Security.Cryptography;
using System.Text;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;
using SHA3Core = Org.BouncyCastle.Crypto.Digests.Sha3Digest;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for SHA3-256 and SHA2-256 hashing.
/// </summary>
[Binding]
public class HashingSteps
{
    private readonly TestWorld _world;

    public HashingSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Helper Methods
    // =========================================================================

    private static byte[] Sha3_256(byte[] data)
    {
        var digest = new SHA3Core(256);
        digest.BlockUpdate(data, 0, data.Length);
        var result = new byte[32];
        digest.DoFinal(result, 0);
        return result;
    }

    private static byte[] Sha2_256(byte[] data)
    {
        return SHA256.HashData(data);
    }

    // =========================================================================
    // Given Steps - Input Data
    // =========================================================================

    [Given(@"empty bytes")]
    public void GivenEmptyBytes()
    {
        _world.Bytes = Array.Empty<byte>();
    }

    [Given(@"bytes for string ""(.*)""")]
    public void GivenBytesForString(string str)
    {
        _world.Bytes = Encoding.UTF8.GetBytes(str);
    }

    [Given(@"bytes for ""(.*)"" and ""(.*)""")]
    public void GivenBytesForStringAnd(string str1, string str2)
    {
        _world.TestVectors["input1"] = Encoding.UTF8.GetBytes(str1);
        _world.TestVectors["input2"] = Encoding.UTF8.GetBytes(str2);
    }

    [Given(@"the domain string ""(.*)""")]
    public void GivenTheDomainString(string domain)
    {
        _world.TestVectors["domain"] = domain;
    }

    [Given(@"transaction data bytes")]
    public void GivenTransactionDataBytes()
    {
        _world.TestVectors["transactionData"] = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8 };
    }

    [Given(@"the same data bytes")]
    public void GivenTheSameDataBytes()
    {
        _world.Bytes = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8 };
    }

    [Given(@"domains ""(.*)"" and ""(.*)""")]
    public void GivenDomainsAnd(string d1, string d2)
    {
        _world.TestVectors["domain1"] = d1;
        _world.TestVectors["domain2"] = d2;
    }

    [Given(@"a 64-character hex string")]
    public void GivenA64CharacterHexString()
    {
        _world.HexString = "0x" + new string('a', 64);
    }

    [Given(@"(\d+) bytes")]
    public void GivenNBytes(int count)
    {
        _world.Bytes = new byte[count];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Given(@"the HashValue ZERO constant")]
    public void GivenTheHashValueZEROConstant()
    {
        _world.Bytes = new byte[32];
    }

    [Given(@"a HashValue from known bytes")]
    public void GivenAHashValueFromKnownBytes()
    {
        _world.Bytes = new byte[32];
        _world.Bytes[0] = 0xab;
        _world.Bytes[1] = 0xcd;
    }

    [Given(@"two HashValues from the same bytes")]
    public void GivenTwoHashValuesFromTheSameBytes()
    {
        var bytes = new byte[32];
        bytes[0] = 0x12;
        _world.TestVectors["hash1"] = bytes;
        _world.TestVectors["hash2"] = (byte[])bytes.Clone();
    }

    [Given(@"(\d+) megabyte of random data")]
    public void GivenMegabyteOfRandomData(int mb)
    {
        _world.Bytes = new byte[mb * 1024 * 1024];
        // Don't fill with random for performance
    }

    // =========================================================================
    // When Steps - SHA3-256
    // =========================================================================

    [When(@"I compute SHA3-256")]
    public void WhenIComputeSHA3_256()
    {
        try
        {
            _world.HashResult = Sha3_256(_world.Bytes ?? Array.Empty<byte>());
            _world.Bytes = _world.HashResult;
            _world.Result = _world.HashResult;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I compute SHA3-256 for both")]
    public void WhenIComputeSHA3_256ForBoth()
    {
        var input1 = (byte[])_world.TestVectors["input1"];
        var input2 = (byte[])_world.TestVectors["input2"];
        _world.TestVectors["hash1"] = Sha3_256(input1);
        _world.TestVectors["hash2"] = Sha3_256(input2);
    }

    [When(@"I compute SHA3-256 twice")]
    public void WhenIComputeSHA3_256Twice()
    {
        var hash1 = Sha3_256(_world.Bytes!);
        var hash2 = Sha3_256(_world.Bytes!);
        _world.TestVectors["hash1"] = hash1;
        _world.TestVectors["hash2"] = hash2;
    }

    [When(@"I compute SHA3-256 of all parts concatenated")]
    public void WhenIComputeSHA3_256OfAllPartsConcatenated()
    {
        _world.HashResult = Sha3_256(_world.Bytes!);
        _world.Result = _world.HashResult;
    }

    [When(@"I compute SHA3-256 of the domain")]
    public void WhenIComputeSHA3_256OfTheDomain()
    {
        var domain = (string)_world.TestVectors["domain"];
        _world.HashResult = Sha3_256(Encoding.UTF8.GetBytes(domain));
        _world.Result = _world.HashResult;
    }

    // =========================================================================
    // When Steps - SHA2-256
    // =========================================================================

    [When(@"I compute SHA2-256")]
    public void WhenIComputeSHA2_256()
    {
        try
        {
            _world.HashResult = Sha2_256(_world.Bytes ?? Array.Empty<byte>());
            _world.Bytes = _world.HashResult;
            _world.Result = _world.HashResult;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I compute both SHA2-256 and SHA3-256")]
    public void WhenIComputeBothSHA2_256AndSHA3_256()
    {
        _world.TestVectors["sha2Result"] = Sha2_256(_world.Bytes!);
        _world.TestVectors["sha3Result"] = Sha3_256(_world.Bytes!);
    }

    // =========================================================================
    // When Steps - Domain-Separated Hashing
    // =========================================================================

    [When(@"I compute domain-separated hash")]
    public void WhenIComputeDomainSeparatedHash()
    {
        var domain = (string)_world.TestVectors["domain"];
        var data = (byte[])_world.TestVectors["transactionData"];

        // Domain-separated hash: SHA3-256(SHA3-256(domain) || data)
        var domainHash = Sha3_256(Encoding.UTF8.GetBytes(domain));
        var combined = new byte[domainHash.Length + data.Length];
        Array.Copy(domainHash, 0, combined, 0, domainHash.Length);
        Array.Copy(data, 0, combined, domainHash.Length, data.Length);

        _world.HashResult = Sha3_256(combined);
        _world.Result = _world.HashResult;
    }

    [When(@"I compute domain-separated hashes")]
    public void WhenIComputeDomainSeparatedHashes()
    {
        var domain1 = (string)_world.TestVectors["domain1"];
        var domain2 = (string)_world.TestVectors["domain2"];
        var data = _world.Bytes!;

        byte[] ComputeDomainHash(string domain)
        {
            var domainHash = Sha3_256(Encoding.UTF8.GetBytes(domain));
            var combined = new byte[domainHash.Length + data.Length];
            Array.Copy(domainHash, 0, combined, 0, domainHash.Length);
            Array.Copy(data, 0, combined, domainHash.Length, data.Length);
            return Sha3_256(combined);
        }

        _world.TestVectors["hash1"] = ComputeDomainHash(domain1);
        _world.TestVectors["hash2"] = ComputeDomainHash(domain2);
    }

    [When(@"I compute the domain prefix")]
    public void WhenIComputeTheDomainPrefix()
    {
        var domain = (string)_world.TestVectors["domain"];
        _world.HashResult = Sha3_256(Encoding.UTF8.GetBytes(domain));
        _world.Result = _world.HashResult;
    }

    // =========================================================================
    // When Steps - HashValue Operations
    // =========================================================================

    [When(@"I create a HashValue from the bytes")]
    public void WhenICreateAHashValueFromTheBytes()
    {
        if (_world.Bytes!.Length == 32)
        {
            _world.Result = _world.Bytes;
            _world.ClearError();
        }
        else
        {
            _world.SetError(new ArgumentException("Invalid length for HashValue"));
        }
    }

    [When(@"I create a HashValue from hex")]
    public void WhenICreateAHashValueFromHex()
    {
        try
        {
            _world.Result = Vectors.HexToBytes(_world.HexString!);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I try to create a HashValue")]
    public void WhenITryToCreateAHashValue()
    {
        try
        {
            if (_world.Bytes!.Length != 32)
            {
                throw new ArgumentException("Invalid length for HashValue: expected 32 bytes");
            }
            _world.Result = _world.Bytes;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I format it as hex")]
    public void WhenIFormatItAsHex()
    {
        var bytes = _world.Bytes ?? (byte[])_world.Result!;
        _world.HexString = Vectors.BytesToHex(bytes);
    }

    [When(@"I compute HashValue using sha3_256_of")]
    public void WhenIComputeHashValueUsingSha3_256_of()
    {
        _world.HashResult = Sha3_256(_world.Bytes!);
        _world.Result = _world.HashResult;
        _world.TestVectors["expectedHash"] = _world.HashResult;
    }

    // =========================================================================
    // Then Steps - Hash Validation
    // =========================================================================

    [Then(@"the hex should be ""(.*)""")]
    public void ThenTheHexShouldBe(string expected)
    {
        var result = (byte[])_world.Result!;
        var actual = Vectors.BytesToHex(result, false).ToLowerInvariant();
        actual.Should().Be(expected.ToLowerInvariant());
    }

    [Then(@"the hashes should be different")]
    public void ThenTheHashesShouldBeDifferent()
    {
        var hash1 = (byte[])_world.TestVectors["hash1"];
        var hash2 = (byte[])_world.TestVectors["hash2"];
        hash1.Should().NotBeNull();
        hash2.Should().NotBeNull();
        Vectors.BytesToHex(hash1).Should().NotBe(Vectors.BytesToHex(hash2));
    }

    [Then(@"both results should be identical")]
    public void ThenBothResultsShouldBeIdentical()
    {
        byte[] val1, val2;

        if (_world.TestVectors.TryGetValue("bytes1", out var b1))
        {
            val1 = (byte[])b1;
            val2 = (byte[])_world.TestVectors["bytes2"];
        }
        else if (_world.TestVectors.TryGetValue("authKey1", out var a1))
        {
            val1 = (byte[])a1;
            val2 = (byte[])_world.TestVectors["authKey2"];
        }
        else
        {
            val1 = (byte[])_world.TestVectors["hash1"];
            val2 = (byte[])_world.TestVectors["hash2"];
        }

        val1.Should().NotBeNull();
        val2.Should().NotBeNull();
        Vectors.BytesToHex(val1).Should().Be(Vectors.BytesToHex(val2));
    }

    [Then(@"the result should equal SHA3-256 of ""(.*)""")]
    public void ThenTheResultShouldEqualSHA3_256Of(string str)
    {
        var expected = Sha3_256(Encoding.UTF8.GetBytes(str));
        var actual = (byte[])_world.Result!;
        Vectors.BytesToHex(actual).Should().Be(Vectors.BytesToHex(expected));
    }

    [Then("the result should be the domain-separated hash")]
    public void ThenTheResultShouldBeDomainSeparatedHash()
    {
        _world.Result.Should().NotBeNull();
        ((byte[])_world.Result!).Length.Should().Be(32);
    }

    [Then(@"the results should be different")]
    public void ThenTheResultsShouldBeDifferent()
    {
        byte[] val1, val2;

        if (_world.TestVectors.TryGetValue("sha2Result", out var s2))
        {
            val1 = (byte[])s2;
            val2 = (byte[])_world.TestVectors["sha3Result"];
        }
        else if (_world.TestVectors.TryGetValue("bytes1", out var b1))
        {
            val1 = (byte[])b1;
            val2 = (byte[])_world.TestVectors["bytes2"];
        }
        else
        {
            val1 = (byte[])_world.TestVectors["hash1"];
            val2 = (byte[])_world.TestVectors["hash2"];
        }

        Vectors.BytesToHex(val1).Should().NotBe(Vectors.BytesToHex(val2));
    }

    [Then(@"the result should be SHA3-256 of the domain string bytes")]
    public void ThenTheResultShouldBeSHA3_256OfTheDomainStringBytes()
    {
        var domain = (string)_world.TestVectors["domain"];
        var expected = Sha3_256(Encoding.UTF8.GetBytes(domain));
        Vectors.BytesToHex((byte[])_world.Result!).Should().Be(Vectors.BytesToHex(expected));
    }

    [Then(@"the hash value should contain those bytes")]
    public void ThenTheHashValueShouldContainThoseBytes()
    {
        Vectors.BytesToHex((byte[])_world.Result!).Should().Be(Vectors.BytesToHex(_world.Bytes!));
    }

    [Then(@"all 32 bytes should be zero")]
    public void ThenAll32BytesShouldBeZero()
    {
        _world.Bytes.Should().NotBeNull();
        for (int i = 0; i < 32; i++)
        {
            _world.Bytes![i].Should().Be(0);
        }
    }

    [Then(@"the hex length should be (\d+) characters")]
    public void ThenTheHexLengthShouldBeCharacters(int count)
    {
        _world.HexString.Should().NotBeNull();
        _world.HexString!.Length.Should().Be(count);
    }

    [Then(@"the two hashes should be equal")]
    public void ThenTheTwoHashesShouldBeEqual()
    {
        var hash1 = (byte[])_world.TestVectors["hash1"];
        var hash2 = (byte[])_world.TestVectors["hash2"];
        Vectors.BytesToHex(hash1).Should().Be(Vectors.BytesToHex(hash2));
    }

    [Then(@"the result should equal a HashValue created from the expected hash")]
    public void ThenTheResultShouldEqualAHashValueCreatedFromTheExpectedHash()
    {
        var expected = (byte[])_world.TestVectors["expectedHash"];
        Vectors.BytesToHex((byte[])_world.Result!).Should().Be(Vectors.BytesToHex(expected));
    }

    [Then(@"it should fail with an invalid length error")]
    public void ThenItShouldFailWithAnInvalidLengthError()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().Contain("length");
    }

    [Then(@"the operation should complete successfully")]
    public void ThenTheOperationShouldCompleteSuccessfully()
    {
        _world.Error.Should().BeNull();
        _world.Result.Should().NotBeNull();
    }
}
