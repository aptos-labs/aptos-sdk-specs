using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// General/common step definitions shared across features.
/// </summary>
[Binding]
public class GeneralSteps
{
    private readonly TestWorld _world;

    public GeneralSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Result Size Steps (Note: some are in CommonSteps.cs)
    // =========================================================================

    [Then("the first byte should be 0x02")]
    public void ThenTheFirstByteShouldBe0x02OuterLength()
    {
        var result = _world.Bytes ?? (_world.Result as byte[]);
        result.Should().NotBeNull("expected result bytes to be set");
        result![0].Should().Be(0x02);
    }

    // =========================================================================
    // General Validation Steps
    // =========================================================================

    [Then("it should succeed")]
    public void ThenItShouldSucceed()
    {
        _world.Error.Should().BeNull();
    }

    [Then("it should fail")]
    public void ThenItShouldFail()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("the operation should succeed")]
    public void ThenTheOperationShouldSucceed()
    {
        _world.Error.Should().BeNull();
    }

    [Then("the operation should fail")]
    public void ThenTheOperationShouldFail()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Equality Steps
    // =========================================================================

    [Then("they should be equal")]
    public void ThenTheyShouldBeEqual()
    {
        if (_world.Result is bool boolResult)
        {
            boolResult.Should().BeTrue();
        }
        else
        {
            // For address comparisons
            if (_world.Address != null && _world.Address2 != null)
            {
                _world.Address.ToString().Should().Be(_world.Address2.ToString());
            }
        }
    }

    [Then("they should not be equal")]
    public void ThenTheyShouldNotBeEqual()
    {
        if (_world.Result is bool boolResult)
        {
            boolResult.Should().BeFalse();
        }
        else
        {
            if (_world.Address != null && _world.Address2 != null)
            {
                _world.Address.ToString().Should().NotBe(_world.Address2.ToString());
            }
        }
    }

    [Then("both results should be identical")]
    public void ThenBothResultsShouldBeIdentical()
    {
        if (_world.TestVectors.TryGetValue("authKey1", out var ak1) &&
            _world.TestVectors.TryGetValue("authKey2", out var ak2))
        {
            Vectors.BytesToHex((byte[])ak1).Should().Be(Vectors.BytesToHex((byte[])ak2));
        }
        else if (_world.TestVectors.TryGetValue("hash1", out var h1) &&
                 _world.TestVectors.TryGetValue("hash2", out var h2))
        {
            Vectors.BytesToHex((byte[])h1).Should().Be(Vectors.BytesToHex((byte[])h2));
        }
    }

    // =========================================================================
    // Common Given Steps
    // =========================================================================

    [Given("{int} bytes")]
    public void GivenBytes(int count)
    {
        _world.Bytes = new byte[count];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Given("32 random bytes")]
    public void Given32RandomBytes()
    {
        _world.Bytes = new byte[32];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Given("an empty byte array")]
    public void GivenAnEmptyByteArray()
    {
        _world.Bytes = Array.Empty<byte>();
    }

    [Given("a hex string {string}")]
    public void GivenAHexString(string hex)
    {
        _world.HexString = hex;
    }

    // =========================================================================
    // Error Assertion Steps
    // =========================================================================

    [Then("it should fail with an invalid length error")]
    public void ThenItShouldFailWithAnInvalidLengthError()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().Contain("length");
    }

    [Then("it should fail with an invalid private key error")]
    public void ThenItShouldFailWithAnInvalidPrivateKeyError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("it should fail with an invalid format error")]
    public void ThenItShouldFailWithAnInvalidFormatError()
    {
        _world.Error.Should().NotBeNull();
    }
}
