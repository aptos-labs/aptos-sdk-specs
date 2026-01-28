using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for byte array assertions.
/// These handle the bracket array format like [0x00, 0x01, ...].
/// </summary>
[Binding]
public class ByteArraySteps
{
    private readonly TestWorld _world;

    public ByteArraySteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Helper Method
    // =========================================================================

    private static byte ParseHexByte(string hex)
    {
        var clean = hex.Trim();
        if (clean.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
            return Convert.ToByte(clean.Substring(2), 16);
        return Convert.ToByte(clean, 16);
    }

    private void AssertBytesMatch(params string[] expected)
    {
        _world.Bytes.Should().NotBeNull("bytes should not be null");
        _world.Bytes!.Length.Should().Be(expected.Length, $"expected {expected.Length} bytes");
        for (int i = 0; i < expected.Length; i++)
        {
            _world.Bytes[i].Should().Be(ParseHexByte(expected[i]), $"byte {i} should match");
        }
    }

    // =========================================================================
    // Then Steps - Byte assertions using a single general parser
    // =========================================================================

    /// <summary>
    /// Handles all byte array assertions by parsing the full array string.
    /// </summary>
    [Then("the bytes should be (.+)")]
    public void ThenTheBytesShouldBeDynamic(string bytesStr)
    {
        var matches = System.Text.RegularExpressions.Regex.Matches(bytesStr, @"0x[0-9a-fA-F]+");
        var expected = matches.Select(m => ParseHexByte(m.Value)).ToArray();
        _world.Bytes.Should().NotBeNull("bytes should not be null");
        _world.Bytes!.Length.Should().Be(expected.Length, $"expected {expected.Length} bytes but got {_world.Bytes.Length}");
        for (int i = 0; i < expected.Length; i++)
        {
            _world.Bytes[i].Should().Be(expected[i], $"byte {i} should match");
        }
    }

    // =========================================================================
    // Then Steps - Result assertions using a general parser
    // =========================================================================

    /// <summary>
    /// Handles byte array results starting with a bracket.
    /// </summary>
    [Then(@"the result should be \[(.+)\]")]
    public void ThenTheResultShouldBeBracketArray(string bytesStr)
    {
        var matches = System.Text.RegularExpressions.Regex.Matches(bytesStr, @"0x[0-9a-fA-F]+");
        var expected = matches.Select(m => ParseHexByte(m.Value)).ToArray();
        _world.Bytes.Should().NotBeNull("bytes should not be null");
        _world.Bytes!.Length.Should().Be(expected.Length, $"expected {expected.Length} bytes but got {_world.Bytes.Length}");
        for (int i = 0; i < expected.Length; i++)
        {
            _world.Bytes[i].Should().Be(expected[i], $"byte {i} should match");
        }
    }
}
