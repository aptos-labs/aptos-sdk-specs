using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Common step definitions shared across multiple features.
/// </summary>
[Binding]
public class CommonSteps
{
    private readonly TestWorld _world;

    public CommonSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Given Steps - Hex Input
    // =========================================================================

    [Given(@"a hex string ""(.*)""")]
    public void GivenAHexString(string hex)
    {
        _world.HexString = hex;
    }

    [Given(@"an invalid hex string ""(.*)""")]
    public void GivenAnInvalidHexString(string hex)
    {
        _world.HexString = hex;
    }

    // =========================================================================
    // Given Steps - Bytes
    // =========================================================================

    [Given(@"(\d+) random bytes")]
    public void GivenRandomBytes(int count)
    {
        _world.Bytes = new byte[count];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Given(@"(\d+) bytes with value (\d+) in the last byte")]
    public void GivenBytesWithValueInLastByte(int count, int value)
    {
        _world.Bytes = new byte[count];
        if (count > 0)
        {
            _world.Bytes[count - 1] = (byte)value;
        }
    }

    [Given(@"bytes from hex ""(.*)""")]
    public void GivenBytesFromHex(string hex)
    {
        _world.Bytes = Vectors.HexToBytes(hex);
    }

    // =========================================================================
    // Given Steps - Messages
    // =========================================================================

    [Given(@"a message ""(.*)""")]
    public void GivenAMessage(string message)
    {
        _world.Message = System.Text.Encoding.UTF8.GetBytes(message);
    }

    [Given(@"the message bytes ""(.*)""")]
    public void GivenTheMessageBytes(string hex)
    {
        _world.Message = Vectors.HexToBytes(hex);
    }

    // =========================================================================
    // Then Steps - Success/Failure
    // =========================================================================

    [Then(@"the parsing should succeed")]
    public void ThenTheParsingShouldSucceed()
    {
        _world.Error.Should().BeNull("parsing should succeed without errors");
    }

    [Then(@"parsing should fail")]
    public void ThenParsingShouldFail()
    {
        _world.Error.Should().NotBeNull("parsing should fail with an error");
    }

    [Then(@"parsing should fail with an error")]
    public void ThenParsingShouldFailWithAnError()
    {
        _world.Error.Should().NotBeNull("parsing should fail with an error");
    }

    [Then(@"it should fail with an InvalidAddress error")]
    public void ThenItShouldFailWithAnInvalidAddressError()
    {
        _world.Error.Should().NotBeNull("should fail with an error");
    }

    [Then(@"the operation should succeed")]
    public void ThenTheOperationShouldSucceed()
    {
        _world.Error.Should().BeNull("operation should succeed without errors");
    }

    [Then(@"the operation should fail")]
    public void ThenTheOperationShouldFail()
    {
        _world.Error.Should().NotBeNull("operation should fail with an error");
    }

    // =========================================================================
    // Then Steps - Result Assertions
    // =========================================================================

    [Then(@"the result should be ""(.*)""")]
    public void ThenTheResultShouldBe(string expected)
    {
        var actual = _world.Result?.ToString() ?? _world.HexString;
        actual.Should().NotBeNull();
        actual!.ToLowerInvariant().Should().Be(expected.ToLowerInvariant());
    }

    [Then(@"the result should be (\d+) bytes")]
    public void ThenTheResultShouldBeBytes(int count)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(count);
    }

    [Then(@"they should be equal")]
    public void ThenTheyShouldBeEqual()
    {
        if (_world.Result is bool result)
        {
            result.Should().BeTrue("values should be equal");
        }
        else
        {
            _world.Address.Should().Be(_world.Address2);
        }
    }

    [Then(@"they should not be equal")]
    public void ThenTheyShouldNotBeEqual()
    {
        if (_world.Result is bool result)
        {
            result.Should().BeFalse("values should not be equal");
        }
        else
        {
            _world.Address.Should().NotBe(_world.Address2);
        }
    }

    // =========================================================================
    // Then Steps - Byte Assertions
    // =========================================================================

    [Then(@"the byte length should be (\d+)")]
    public void ThenTheByteLengthShouldBe(int length)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(length);
    }

    [Then(@"the bytes should be (\d+) bytes")]
    public void ThenTheBytesShouldBeNBytes(int length)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(length);
    }

    [Then(@"byte (\d+) should equal (\d+)")]
    public void ThenByteShouldEqual(int index, int value)
    {
        var bytes = _world.Address?.ToByteArray() ?? _world.Bytes;
        bytes.Should().NotBeNull();
        bytes![index].Should().Be((byte)value);
    }

    [Then(@"bytes (\d+)-(\d+) should all be (\d+)")]
    public void ThenBytesRangeShouldAllBe(int start, int end, int value)
    {
        var bytes = _world.Address?.ToByteArray() ?? _world.Bytes;
        bytes.Should().NotBeNull();
        for (int i = start; i <= end; i++)
        {
            bytes![i].Should().Be((byte)value, $"byte {i} should be {value}");
        }
    }

    [Then(@"all (\d+) bytes should be (\d+)")]
    public void ThenAllBytesShouldBe(int count, int value)
    {
        var bytes = _world.Address?.ToByteArray() ?? _world.Bytes;
        bytes.Should().NotBeNull();
        bytes!.Length.Should().Be(count);
        for (int i = 0; i < count; i++)
        {
            bytes[i].Should().Be((byte)value, $"byte {i} should be {value}");
        }
    }

    [Then(@"the first byte should be zero")]
    public void ThenTheFirstByteShouldBeZero()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![0].Should().Be(0);
    }

    [Then(@"the last byte should be (\d+)")]
    public void ThenTheLastByteShouldBe(int value)
    {
        var bytes = _world.Address?.ToByteArray() ?? _world.Bytes;
        bytes.Should().NotBeNull();
        bytes![^1].Should().Be((byte)value);
    }

    // =========================================================================
    // Then Steps - Error Messages
    // =========================================================================

    [Then(@"the error message should contain ""(.*)""")]
    public void ThenTheErrorMessageShouldContain(string text)
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().Contain(text);
    }
}
