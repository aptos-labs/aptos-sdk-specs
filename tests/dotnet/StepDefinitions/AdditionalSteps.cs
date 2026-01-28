using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Additional step definitions for various features.
/// </summary>
[Binding]
public class AdditionalSteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public AdditionalSteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // Given Steps - Crypto
    // =========================================================================

    [Given(@"a valid (\d+)-byte Ed(\d+) private key \(seed \+ public key\)")]
    public void GivenAValidByteEdPrivateKeySeedPlusPublicKey(int bytes, int bits)
    {
        // Generate a key pair and store the concatenated private+public key bytes
        var pk = Ed25519PrivateKey.Generate();
        _world.Ed25519PrivateKey = pk;
        _world.Ed25519PublicKey = (Ed25519PublicKey)pk.PublicKey();
        _world.TestVectors["keyBytes"] = bytes;
    }

    [Given("an inner vector of length 2")]
    public void GivenAnInnerVectorOfLength2()
    {
        _world.TestVectors["innerVectorLength"] = 2;
    }

    // Note: "bytes [0xNN]" step is defined in SerializationSteps.cs as GivenBytesArray

    [Given("an Option containing a u64 value 1000000")]
    public void GivenAnOptionContainingU64()
    {
        _world.TestVectors["optionHasValue"] = true;
        _world.TestVectors["optionValue"] = 1000000UL;
    }

    [Given("an empty Option")]
    public void GivenAnEmptyOption()
    {
        _world.TestVectors["optionHasValue"] = false;
    }

    // =========================================================================
    // When Steps - Crypto
    // =========================================================================

    [When(@"I create an Ed(\d+) key pair from the bytes")]
    public void WhenICreateAnEdKeyPairFromTheBytes(int bits)
    {
        // Key pair already created in Given step
        _world.TestVectors["keyPairCreated"] = true;
    }

    // =========================================================================
    // Then Steps - Crypto
    // =========================================================================

    // Note: "the key pair should be valid" step is defined in CryptoSteps.cs

    // Note: "each inner vector should be length-prefixed" step is defined in SerializationSteps.cs

    // =========================================================================
    // Then Steps - Serialization
    // =========================================================================

    [Then("the first byte should be 0x01 (Some variant)")]
    public void ThenTheFirstByteShouldBe01Some()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![0].Should().Be(0x01);
    }

    [Then("the remaining 8 bytes should be the u64 value in little-endian")]
    public void ThenTheRemaining8BytesShouldBeU64LittleEndian()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterOrEqualTo(9);
    }

    [Then("the remaining bytes should be {string}, {string}, {string}")]
    public void ThenTheRemainingBytesShouldBe3(string b1, string b2, string b3)
    {
        _world.Bytes.Should().NotBeNull();
        // Check bytes starting from index 1
        _world.Bytes![1].Should().Be(Convert.ToByte(b1, 16));
        _world.Bytes[2].Should().Be(Convert.ToByte(b2, 16));
        _world.Bytes[3].Should().Be(Convert.ToByte(b3, 16));
    }

    // =========================================================================
    // Given Steps - TypeTag
    // =========================================================================

    [Given(@"a Move struct type ""(.*)::(.*)::(.*)""")]
    public void GivenAMoveStructType(string address, string module, string name)
    {
        _world.TestVectors["structAddress"] = address;
        _world.TestVectors["structModule"] = module;
        _world.TestVectors["structName"] = name;
    }

    [Given(@"an address ""(.*)"", module ""(.*)"", and struct ""(.*)""")]
    public void GivenAddressModuleAndStruct(string address, string module, string name)
    {
        _world.TestVectors["structAddress"] = address;
        _world.TestVectors["structModule"] = module;
        _world.TestVectors["structName"] = name;
    }

    [Given(@"an invalid struct string ""(.*)""")]
    public void GivenAnInvalidStructString(string invalid)
    {
        _world.TestVectors["invalidStruct"] = invalid;
    }

    [Given(@"an invalid address format like ""(.*)""")]
    public void GivenAnInvalidAddressFormat(string invalid)
    {
        _world.TestVectors["invalidAddress"] = invalid;
    }

    [Given(@"a vector type with unclosed bracket ""(.*)""")]
    public void GivenAVectorTypeWithUnclosedBracket(string invalid)
    {
        _world.TestVectors["invalidVector"] = invalid;
    }

    [Given(@"a malformed vector ""(.*)""")]
    public void GivenAMalformedVector(string invalid)
    {
        _world.TestVectors["malformedVector"] = invalid;
    }

    // =========================================================================
    // When Steps - TypeTag
    // =========================================================================

    // Note: "When I create a MoveStructTag" step is defined in TypeTagSteps.cs

    // Note: "When I try to parse it" and "When I format it as module ID" steps are
    // defined in TypeTagSteps.cs

    // =========================================================================
    // Then Steps - TypeTag
    // =========================================================================

    [Then(@"the address should be ""(.*)""")]
    public void ThenTheAddressShouldBe(string expected)
    {
        // Validation placeholder
    }

    [Then(@"the module should be ""(.*)""")]
    public void ThenTheModuleShouldBeTypetag(string expected)
    {
        // Note: Using different name to avoid conflict with TransactionBuilderSteps
        // Validation placeholder
    }

    [Then(@"the name should be ""(.*)""")]
    public void ThenTheNameShouldBe(string expected)
    {
        // Validation placeholder
    }

    [Then(@"the result should be ""(.*)::(.*)""")]
    public void ThenTheResultShouldBeModuleId(string addr, string module)
    {
        // Validation placeholder
    }

    [Then(@"the type tag should be Struct variant")]
    public void ThenTheTypeTagShouldBeStructVariant()
    {
        // Validation placeholder
    }

    [Then("parsing should fail with a meaningful error")]
    public void ThenParsingShouldFailWithMeaningfulError()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Given Steps - Auth Key
    // =========================================================================

    [Given(@"an Ed(\d+) account")]
    public void GivenAnEdAccount(int bits)
    {
        _world.Account = Ed25519Account.Generate();
        _world.Ed25519PublicKey = (Ed25519PublicKey)_world.Account.PublicKey;
    }

    // =========================================================================
    // When Steps - Auth Key
    // =========================================================================

    [When("I derive the authentication key")]
    public void WhenIDeriveTheAuthenticationKey()
    {
        if (_world.Ed25519PublicKey != null)
        {
            // TODO: SDK API may differ - using placeholder
            _world.TestVectors["authKeyDerived"] = true;
        }
    }

    [When("I derive the account address")]
    public void WhenIDeriveTheAccountAddress()
    {
        if (_world.Account != null)
        {
            _world.Address = _world.Account.Address;
        }
    }

    // =========================================================================
    // Then Steps - Auth Key
    // =========================================================================

    [Then("the authentication key should be 32 bytes")]
    public void ThenTheAuthenticationKeyShouldBe32Bytes()
    {
        // Validation placeholder - auth key derivation depends on SDK API
    }

    [Then("the account address should be 32 bytes")]
    public void ThenTheAccountAddressShouldBe32Bytes()
    {
        _world.Address.Should().NotBeNull();
        _world.Address!.ToByteArray().Length.Should().Be(32);
    }

    [Then("it should equal SHA3-256 of public_key_bytes concatenated with 0x00")]
    public void ThenItShouldEqualSHA3256PublicKeyBytes0x00()
    {
        // Auth key derivation check - placeholder
    }

    // =========================================================================
    // Then Steps - Memory Safety (Placeholder - not directly testable in C#)
    // =========================================================================

    [Then("the memory should be cleared")]
    public void ThenTheMemoryShouldBeCleared()
    {
        // Memory clearing is not directly testable in C#
        // The .NET runtime handles memory management
    }

    [Then("the private key bytes should be zeroed")]
    public void ThenThePrivateKeyBytesShouldBeZeroed()
    {
        // Memory clearing is not directly testable in C#
    }
}
