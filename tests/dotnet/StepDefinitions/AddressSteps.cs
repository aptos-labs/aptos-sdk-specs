using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for address parsing, formatting, and manipulation.
/// Tests the AccountAddress type from the Aptos .NET SDK.
/// </summary>
[Binding]
public class AddressSteps
{
    private readonly TestWorld _world;

    public AddressSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Given Steps - Address Input
    // =========================================================================

    [Given(@"a valid hex address string ""(.*)""")]
    public void GivenAValidHexAddressString(string hex)
    {
        _world.HexString = hex;
    }

    [Given(@"the address string ""(.*)""")]
    public void GivenTheAddressString(string address)
    {
        _world.HexString = address;
    }

    [Given(@"a short address ""(.*)""")]
    public void GivenAShortAddress(string address)
    {
        _world.HexString = address;
    }

    [Given(@"a full 64-character hex address")]
    public void GivenAFull64CharacterHexAddress()
    {
        _world.HexString = "0x0000000000000000000000000000000000000000000000000000000000000001";
    }

    [Given(@"test vectors from addresses\.json")]
    public void GivenTestVectorsFromAddressesJson()
    {
        var vectors = Vectors.GetAddressParsingVectors();
        _world.TestVectors["address_parsing"] = vectors;
    }

    // =========================================================================
    // Given Steps - Address Constants
    // =========================================================================

    // Well-known address constants (SDK may not expose these as statics)
    private static readonly string AddressZero = "0x0000000000000000000000000000000000000000000000000000000000000000";
    private static readonly string AddressOne = "0x0000000000000000000000000000000000000000000000000000000000000001";
    private static readonly string AddressThree = "0x0000000000000000000000000000000000000000000000000000000000000003";
    private static readonly string AddressFour = "0x0000000000000000000000000000000000000000000000000000000000000004";

    [Given(@"the ZERO address constant")]
    public void GivenTheZEROAddressConstant()
    {
        _world.Address = AccountAddress.FromString(AddressZero);
    }

    [Given(@"the zero address constant")]
    public void GivenTheZeroAddressConstant()
    {
        _world.Address = AccountAddress.FromString(AddressZero);
    }

    [Given(@"the ONE address constant")]
    public void GivenTheONEAddressConstant()
    {
        _world.Address = AccountAddress.FromString(AddressOne);
    }

    [Given(@"the framework address constant")]
    public void GivenTheFrameworkAddressConstant()
    {
        _world.Address = AccountAddress.FromString(AddressOne);
    }

    [Given(@"the THREE address constant")]
    public void GivenTheTHREEAddressConstant()
    {
        _world.Address = AccountAddress.FromString(AddressThree);
    }

    [Given(@"the FOUR address constant")]
    public void GivenTheFOURAddressConstant()
    {
        _world.Address = AccountAddress.FromString(AddressFour);
    }

    // =========================================================================
    // Given Steps - Address Creation
    // =========================================================================

    [Given(@"an AccountAddress with value (\d+)")]
    public void GivenAnAccountAddressWithValue(int value)
    {
        // Create address with specific byte value in last position
        var bytes = new byte[32];
        bytes[31] = (byte)value;
        _world.Address = new AccountAddress(bytes);
    }

    [Given(@"an AccountAddress from hex ""(.*)""")]
    public void GivenAnAccountAddressFromHex(string hex)
    {
        try
        {
            _world.Address = AccountAddress.FromString(hex);
            // Also add to addresses list for comparison scenarios
            _world.Addresses.Clear();
            _world.Addresses.Add(_world.Address);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Given(@"another AccountAddress from hex ""(.*)""")]
    public void GivenAnotherAccountAddressFromHex(string hex)
    {
        try
        {
            _world.Address2 = AccountAddress.FromString(hex);
            // Add second address to list for comparison scenarios
            if (_world.Addresses.Count == 0 && _world.Address != null)
            {
                _world.Addresses.Add(_world.Address);
            }
            _world.Addresses.Add(_world.Address2);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Given(@"two addresses ""(.*)"" and ""(.*)""")]
    public void GivenTwoAddresses(string addr1, string addr2)
    {
        _world.Addresses.Clear();
        _world.Addresses.Add(AccountAddress.FromString(addr1));
        _world.Addresses.Add(AccountAddress.FromString(addr2));
    }

    // =========================================================================
    // When Steps - Parsing
    // =========================================================================

    [When(@"I parse the address")]
    public void WhenIParseTheAddress()
    {
        try
        {
            // Use maxMissingChars=62 to allow short addresses (minimum "0x" + 2 chars)
            _world.Address = AccountAddress.FromString(_world.HexString!, maxMissingChars: 62);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I parse the address string")]
    public void WhenIParseTheAddressString()
    {
        WhenIParseTheAddress();
    }

    [When(@"I parse it as an AccountAddress")]
    public void WhenIParseItAsAnAccountAddress()
    {
        WhenIParseTheAddress();
    }

    [When(@"I try to parse it as an address")]
    public void WhenITryToParseItAsAnAddress()
    {
        WhenIParseTheAddress();
    }

    [When(@"I create an AccountAddress from the bytes")]
    public void WhenICreateAnAccountAddressFromTheBytes()
    {
        try
        {
            _world.Address = new AccountAddress(_world.Bytes!);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // When Steps - Formatting
    // =========================================================================

    [When(@"I format the address as a string")]
    public void WhenIFormatTheAddressAsAString()
    {
        _world.HexString = _world.Address!.ToString();
    }

    [When(@"I format it as full hex")]
    public void WhenIFormatItAsFullHex()
    {
        _world.Result = _world.Address!.ToStringLong();
    }

    [When(@"I format it as a full hex string")]
    public void WhenIFormatItAsAFullHexString()
    {
        _world.HexString = _world.Address!.ToStringLong();
    }

    [When(@"I format it as short string")]
    public void WhenIFormatItAsShortString()
    {
        _world.Result = ToShortString(_world.Address!.ToString().ToLowerInvariant());
    }

    [When(@"I format it as a short string")]
    public void WhenIFormatItAsAShortString()
    {
        _world.HexString = ToShortString(_world.Address!.ToString().ToLowerInvariant());
    }

    // =========================================================================
    // When Steps - Bytes/Serialization
    // =========================================================================

    [When(@"I get the raw bytes")]
    public void WhenIGetTheRawBytes()
    {
        _world.Bytes = _world.Address!.ToByteArray();
    }

    [When(@"I BCS serialize the address")]
    public void WhenIBCSSerializeTheAddress()
    {
        if (_world.Address == null)
        {
            _world.SetError(new InvalidOperationException("No address to serialize"));
            return;
        }
        // BCS serialization of an address is just the 32 bytes
        _world.Bytes = _world.Address.ToByteArray();
        // Store original address for round-trip comparison
        _world.Address2 = _world.Address;
    }

    [When(@"I BCS deserialize as AccountAddress")]
    public void WhenIBCSDeserializeAsAccountAddress()
    {
        try
        {
            _world.Address = new AccountAddress(_world.Bytes!);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I BCS deserialize the result as AccountAddress")]
    public void WhenIBCSDeserializeTheResultAsAccountAddress()
    {
        WhenIBCSDeserializeAsAccountAddress();
    }

    // =========================================================================
    // When Steps - Comparison
    // =========================================================================

    [When(@"I compare them for equality")]
    public void WhenICompareThemForEquality()
    {
        _world.Result = _world.Addresses[0].Equals(_world.Addresses[1]);
    }

    // =========================================================================
    // When Steps - Test Vectors
    // =========================================================================

    [When(@"I run all parsing test vectors")]
    public void WhenIRunAllParsingTestVectors()
    {
        var vectors = (List<AddressVector>)_world.TestVectors["address_parsing"];
        var results = new List<VectorResult>();

        foreach (var vector in vectors)
        {
            try
            {
                var address = AccountAddress.FromString(vector.Input);
                var fullHex = address.ToStringLong();
                var shortString = address.ToString();

                var passed = string.Equals(fullHex, vector.Expected.FullHex, StringComparison.OrdinalIgnoreCase) &&
                             string.Equals(shortString, vector.Expected.ShortString, StringComparison.OrdinalIgnoreCase);

                results.Add(new VectorResult { Name = vector.Name, Passed = passed });
            }
            catch (Exception ex)
            {
                results.Add(new VectorResult { Name = vector.Name, Passed = false, Error = ex.Message });
            }
        }

        _world.Result = results;
    }

    // =========================================================================
    // Then Steps - Address Validity
    // =========================================================================

    [Then(@"I should get a valid AccountAddress")]
    public void ThenIShouldGetAValidAccountAddress()
    {
        _world.Error.Should().BeNull();
        _world.Address.Should().NotBeNull();
    }

    [Then(@"the address should be valid")]
    public void ThenTheAddressShouldBeValid()
    {
        _world.Error.Should().BeNull();
        _world.Address.Should().NotBeNull();
    }

    [Then(@"the parsing should fail with an invalid address error")]
    public void ThenTheParsingShouldFailWithAnInvalidAddressError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then(@"the parsing should fail with an invalid hex error")]
    public void ThenTheParsingShouldFailWithAnInvalidHexError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then(@"the parsing should fail with an invalid length error")]
    public void ThenTheParsingShouldFailWithAnInvalidLengthError()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Then Steps - Address Bytes
    // =========================================================================

    [Then(@"the address bytes should have length (\d+)")]
    public void ThenTheAddressBytesShouldHaveLength(int length)
    {
        _world.Address.Should().NotBeNull();
        _world.Address!.ToByteArray().Length.Should().Be(length);
    }

    // =========================================================================
    // Then Steps - String Formatting
    // =========================================================================

    [Then(@"the full hex should be ""(.*)""")]
    public void ThenTheFullHexShouldBe(string expected)
    {
        _world.Address.Should().NotBeNull();
        _world.Address!.ToStringLong().ToLowerInvariant().Should().Be(expected.ToLowerInvariant());
    }

    [Then(@"the full hex representation should be ""(.*)""")]
    public void ThenTheFullHexRepresentationShouldBe(string expected)
    {
        ThenTheFullHexShouldBe(expected);
    }

    [Then(@"the short string should be ""(.*)""")]
    public void ThenTheShortStringShouldBe(string expected)
    {
        _world.Address.Should().NotBeNull();
        // Convert to short form: remove leading zeros after 0x prefix
        var fullHex = _world.Address!.ToString().ToLowerInvariant();
        var shortHex = ToShortString(fullHex);
        shortHex.Should().Be(expected.ToLowerInvariant());
    }

    /// <summary>
    /// Converts a full hex address to short form by removing leading zeros.
    /// </summary>
    private static string ToShortString(string fullHex)
    {
        // Remove 0x prefix, trim leading zeros, add 0x back
        var hex = fullHex.StartsWith("0x") ? fullHex[2..] : fullHex;
        var trimmed = hex.TrimStart('0');
        return "0x" + (trimmed.Length == 0 ? "0" : trimmed);
    }

    [Then(@"the address should equal ""(.*)""")]
    public void ThenTheAddressShouldEqual(string expected)
    {
        _world.Address.Should().NotBeNull();
        _world.Address!.ToString().ToLowerInvariant().Should().Be(expected.ToLowerInvariant());
    }

    // =========================================================================
    // Then Steps - Address Equality
    // =========================================================================

    [Then(@"it should equal address ""(.*)""")]
    public void ThenItShouldEqualAddress(string expected)
    {
        var expectedAddress = AccountAddress.FromString(expected);
        _world.Address.Should().NotBeNull();
        _world.Address!.Equals(expectedAddress).Should().BeTrue();
    }

    [Then(@"the two addresses should be equal")]
    public void ThenTheTwoAddressesShouldBeEqual()
    {
        _world.Addresses.Should().HaveCount(2);
        _world.Addresses[0].Equals(_world.Addresses[1]).Should().BeTrue();
    }

    [Then(@"the two addresses should not be equal")]
    public void ThenTheTwoAddressesShouldNotBeEqual()
    {
        _world.Addresses.Should().HaveCount(2);
        _world.Addresses[0].Equals(_world.Addresses[1]).Should().BeFalse();
    }

    [Then(@"the result should equal the original address")]
    public void ThenTheResultShouldEqualTheOriginalAddress()
    {
        _world.Address.Should().NotBeNull();
        _world.Address2.Should().NotBeNull();
        _world.Address!.Equals(_world.Address2).Should().BeTrue();
    }

    // =========================================================================
    // Then Steps - Test Vectors
    // =========================================================================

    [Then(@"all test vectors should pass")]
    public void ThenAllTestVectorsShouldPass()
    {
        var results = (List<VectorResult>)_world.Result!;
        var failures = results.Where(r => !r.Passed).ToList();

        if (failures.Count > 0)
        {
            var failureMessages = string.Join("\n", failures.Select(f => $"  - {f.Name}: {f.Error ?? "mismatch"}"));
            throw new Exception($"{failures.Count} test vectors failed:\n{failureMessages}");
        }
    }

    // =========================================================================
    // Helper Classes
    // =========================================================================

    private class VectorResult
    {
        public string Name { get; set; } = "";
        public bool Passed { get; set; }
        public string? Error { get; set; }
    }
}
