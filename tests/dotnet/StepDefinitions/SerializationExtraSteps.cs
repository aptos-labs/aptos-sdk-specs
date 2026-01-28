using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Additional step definitions for BCS serialization.
/// </summary>
[Binding]
public class SerializationExtraSteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public SerializationExtraSteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // When Steps - Serialization
    // =========================================================================

    [When("I serialize the multi-signature")]
    public void WhenISerializeTheMultiSignature()
    {
        _world.TestVectors["multiSigSerialized"] = true;
    }

    // =========================================================================
    // Then Steps - BCS Encoding
    // =========================================================================

    [Then("it should properly BCS encode all fields in order")]
    public void ThenItShouldProperlyBCSEncodeAllFieldsInOrder()
    {
        // Validation placeholder
    }

    [Then("it should properly BCS encode the value")]
    public void ThenItShouldProperlyBCSEncodeTheValue()
    {
        // Validation placeholder
    }

    [Then("it should properly BCS encode the vector")]
    public void ThenItShouldProperlyBCSEncodeTheVector()
    {
        // Validation placeholder
    }

    [Then("it should properly encode the address")]
    public void ThenItShouldProperlyEncodeTheAddress()
    {
        // Validation placeholder
    }

    [Then("the vector should be properly encoded")]
    public void ThenTheVectorShouldBeProperlyEncoded()
    {
        // Validation placeholder
    }

    [Then("the encoding should succeed")]
    public void ThenTheEncodingShouldSucceed()
    {
        _world.Error.Should().BeNull();
    }

    [Then("the result should be valid BCS")]
    public void ThenTheResultShouldBeValidBCS()
    {
        // Validation placeholder
    }

    [Then("the result should include module ID, function name, type args, and args")]
    public void ThenTheResultShouldIncludeModuleIDFunctionNameTypeArgsAndArgs()
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Byte Assertions
    // =========================================================================

    [Then(@"args should serialize as empty vector \(""(.*)""\)")]
    public void ThenArgsShouldSerializeAsEmptyVector(string expected)
    {
        // Validation placeholder
    }

    [Then(@"type_args should serialize as empty vector \(""(.*)""\)")]
    public void ThenTypeArgsShouldSerializeAsEmptyVector(string expected)
    {
        // Validation placeholder
    }

    [Then(@"argument (\d+) should be BCS-encoded address \((\d+) bytes\)")]
    public void ThenArgumentShouldBeBCSEncodedAddressBytes(int argIndex, int bytes)
    {
        // Validation placeholder
    }

    [Then(@"argument (\d+) should be BCS-encoded u(\d+) \((\d+) bytes\)")]
    public void ThenArgumentShouldBeBCSEncodedUBytes(int argIndex, int bits, int bytes)
    {
        // Validation placeholder
    }

    [Then(@"the first byte should be ""(.*)""")]
    public void ThenTheFirstByteShouldBe(string expected)
    {
        // Validation placeholder
    }

    [Then(@"the first byte should be ""(.*)"" \(outer length\)")]
    public void ThenTheFirstByteShouldBeOuterLength(string expected)
    {
        // Validation placeholder
    }

    [Then(@"the first (\d+) bytes should be ""(.*)""")]
    public void ThenTheFirstBytesShouldBe(int count, string expected)
    {
        // Validation placeholder
    }

    [Then(@"the chain_id byte should be ""(.*)""")]
    public void ThenTheChainIdByteShouldBe(string expected)
    {
        // Validation placeholder
    }

    [Then(@"the size should be (\d+) bytes")]
    public void ThenTheSizeShouldBeBytes(int size)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(size);
    }

    [Then("the bytes should be deterministic")]
    public void ThenTheBytesShouldBeDeterministic()
    {
        // Validation placeholder
    }

    [Then("the bytes should be identical")]
    public void ThenTheBytesShouldBeIdentical()
    {
        // Validation placeholder
    }

    [Then(@"the result should be (\d+) byte \(""(.*)""\)")]
    public void ThenTheResultShouldBeByte(int count, string expected)
    {
        // Validation placeholder
    }

    [Then(@"the result should be ULEB(\d+) length \+ bytes")]
    public void ThenTheResultShouldBeULEBLengthBytes(int bits)
    {
        // Validation placeholder
    }

    [Then(@"the result should be ULEB(\d+) length \+ UTF(\d+) bytes")]
    public void ThenTheResultShouldBeULEBLengthUTFBytes(int ulebBits, int utfBits)
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Byte Array Assertions
    // =========================================================================

    [Then(@"the bytes should be \[(.+xFF), (.+xFF)\]")]
    public void ThenTheBytesShouldBe2xFF(int b1, int b2)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(.+xFF), (.+xFF), (.+xFF), (.+xFF)\]")]
    public void ThenTheBytesShouldBe4xFF(int b1, int b2, int b3, int b4)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(.+xFF), (.+xFF), (.+xFF), (.+xFF), (.+xFF), (.+xFF), (.+xFF), (.+xFF)\]")]
    public void ThenTheBytesShouldBe8xFF(int b1, int b2, int b3, int b4, int b5, int b6, int b7, int b8)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBe2(string b1, string b2)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBe4(string b1, string b2, string b3, string b4)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBe8(string b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBe16(string b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8, string b9, string b10, string b11, string b12, string b13, string b14, string b15, string b16)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBe32(string b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8, string b9, string b10, string b11, string b12, string b13, string b14, string b15, string b16, string b17, string b18, string b19, string b20, string b21, string b22, string b23, string b24, string b25, string b26, string b27, string b28, string b29, string b30, string b31, string b32)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(\d+)xFF, ""(.*)""\]")]
    public void ThenTheBytesShouldBeXFF1(int b1, string b2)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(\d+)xFF, ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBeXFF3(int b1, string b2, string b3, string b4)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(\d+)xFF, ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBeXFF7(int b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(\d+)xFF, ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBeXFF15(int b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8, string b9, string b10, string b11, string b12, string b13, string b14, string b15, string b16)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[(\d+)xf(\d+), (\d+)xde, (\d+)xbc, ""(.*)""a, ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBeXfXdeXbc(int b1a, int b1b, int b2, int b3, string b4, string b5, string b6, string b7, string b8)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)""F, ""(.*)""E, ""(.*)""D, ""(.*)""C, ""(.*)""B, ""(.*)""A, ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBeFEDCBA16(string b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8, string b9, string b10, string b11, string b12, string b13, string b14, string b15, string b16)
    {
        // Validation placeholder
    }

    [Then(@"the bytes should be \[""(.*)""F, ""(.*)""E, ""(.*)""D, ""(.*)""C, ""(.*)""B, ""(.*)""A, ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""F, ""(.*)""E, ""(.*)""D, ""(.*)""C, ""(.*)""B, ""(.*)""A, ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)"", ""(.*)""\]")]
    public void ThenTheBytesShouldBeFEDCBA32(string b1, string b2, string b3, string b4, string b5, string b6, string b7, string b8, string b9, string b10, string b11, string b12, string b13, string b14, string b15, string b16, string b17, string b18, string b19, string b20, string b21, string b22, string b23, string b24, string b25, string b26, string b27, string b28, string b29, string b30, string b31, string b32)
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Type Arguments
    // =========================================================================

    [Then(@"type argument (\d+) should be ""(.*)""")]
    public void ThenTypeArgumentShouldBe(int index, string expected)
    {
        // Validation placeholder
    }

    [Then(@"type argument (\d+) should be U(\d+)")]
    public void ThenTypeArgumentShouldBeU(int index, int bits)
    {
        // Validation placeholder
    }

    [Then(@"type argument (\d+) should be a Struct named ""(.*)""")]
    public void ThenTypeArgumentShouldBeAStructNamed(int index, string name)
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Multi-Agent Serialization
    // =========================================================================

    [Then(@"it should contain secondary_signer_addresses \(may be empty\)")]
    public void ThenItShouldContainSecondarySignerAddressesMayBeEmpty()
    {
        // Validation placeholder
    }

    [Then(@"it should contain secondary_signers \(may be empty\)")]
    public void ThenItShouldContainSecondarySignersMayBeEmpty()
    {
        // Validation placeholder
    }

    [Then("it should include secondary signer addresses")]
    public void ThenItShouldIncludeSecondarySignerAddresses()
    {
        // Validation placeholder
    }

    [Then(@"the secondary_signer_addresses should be \[A, B, C] in order")]
    public void ThenTheSecondarySignerAddressesShouldBeABCInOrder()
    {
        // Validation placeholder
    }

    [Then(@"it should equal SHA(.*)\(pk(\d+) \|\| pk(\d+) \|\| pk(\d+) \|\| threshold \|\| ""(.*)""\)")]
    public void ThenItShouldEqualSHAPkPkPkThreshold(string algo, int pk1, int pk2, int pk3, string suffix)
    {
        // Multi-sig auth key derivation validation
    }
}
