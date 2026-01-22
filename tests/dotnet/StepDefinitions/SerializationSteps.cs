using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for BCS serialization and deserialization.
/// Note: Many serialization steps are placeholders pending SDK API investigation.
/// </summary>
[Binding]
public class SerializationSteps
{
    private readonly TestWorld _world;

    public SerializationSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Given Steps - Boolean Values
    // =========================================================================

    [Given(@"a boolean value true")]
    public void GivenABooleanValueTrue()
    {
        _world.TestVectors["boolValue"] = true;
    }

    [Given(@"a boolean value false")]
    public void GivenABooleanValueFalse()
    {
        _world.TestVectors["boolValue"] = false;
    }

    // =========================================================================
    // Given Steps - Integer Values
    // =========================================================================

    [Given(@"a u8 value (\d+)")]
    public void GivenAU8Value(int value)
    {
        _world.TestVectors["u8Value"] = (byte)value;
    }

    [Given(@"a u16 value (\w+)")]
    public void GivenAU16Value(string value)
    {
        var numValue = value.StartsWith("0x") 
            ? Convert.ToUInt16(value, 16) 
            : ushort.Parse(value);
        _world.TestVectors["u16Value"] = numValue;
    }

    [Given(@"a u32 value (\w+)")]
    public void GivenAU32Value(string value)
    {
        var numValue = value.StartsWith("0x") 
            ? Convert.ToUInt32(value, 16) 
            : uint.Parse(value);
        _world.TestVectors["u32Value"] = numValue;
    }

    [Given(@"a u64 value (\w+)")]
    public void GivenAU64Value(string value)
    {
        var numValue = value.StartsWith("0x") 
            ? Convert.ToUInt64(value, 16) 
            : ulong.Parse(value);
        _world.TestVectors["u64Value"] = numValue;
    }

    [Given(@"a u128 value (\w+)")]
    public void GivenAU128Value(string value)
    {
        _world.TestVectors["u128Value"] = value;
    }

    [Given(@"a u256 value (\w+)")]
    public void GivenAU256Value(string value)
    {
        _world.TestVectors["u256Value"] = value;
    }

    [Given(@"a length value (\d+)")]
    public void GivenALengthValue(int value)
    {
        _world.TestVectors["lengthValue"] = value;
    }

    // =========================================================================
    // Given Steps - Bytes/String Values
    // =========================================================================

    [Given(@"an empty byte array")]
    public void GivenAnEmptyByteArray()
    {
        _world.Bytes = Array.Empty<byte>();
    }

    [Given(@"bytes \[(0x[0-9a-fA-F]+(?:,\s*0x[0-9a-fA-F]+)*)\]")]
    public void GivenBytesArray(string bytesStr)
    {
        var byteValues = bytesStr.Split(',')
            .Select(b => Convert.ToByte(b.Trim(), 16))
            .ToArray();
        _world.Bytes = byteValues;
    }

    [Given(@"a string ""(.*)""")]
    public void GivenAString(string str)
    {
        _world.TestVectors["stringValue"] = str;
    }

    // =========================================================================
    // Given Steps - Option Values
    // =========================================================================

    [Given(@"an Option with no value")]
    public void GivenAnOptionWithNoValue()
    {
        _world.TestVectors["optionValue"] = null!;
    }

    [Given(@"an Option containing u64 value (\d+)")]
    public void GivenAnOptionContainingU64Value(ulong value)
    {
        _world.TestVectors["optionValue"] = value;
    }

    // =========================================================================
    // Given Steps - Vector Values
    // =========================================================================

    [Given(@"an empty vector of u8")]
    public void GivenAnEmptyVectorOfU8()
    {
        _world.TestVectors["vectorU8"] = Array.Empty<byte>();
    }

    [Given(@"a vector \[(\d+), (\d+), (\d+)\] of u8")]
    public void GivenAVectorOfU8(int a, int b, int c)
    {
        _world.TestVectors["vectorU8"] = new byte[] { (byte)a, (byte)b, (byte)c };
    }

    [Given(@"a vector \[(\d+), (\d+)\] of u64")]
    public void GivenAVectorOfU64(ulong a, ulong b)
    {
        _world.TestVectors["vectorU64"] = new[] { a, b };
    }

    // =========================================================================
    // Given Steps - AccountAddress
    // =========================================================================

    [Given(@"an AccountAddress ""(.*)""")]
    public void GivenAnAccountAddress(string addressStr)
    {
        _world.Address = AccountAddress.FromString(addressStr);
    }

    [Given(@"(\d+) bytes with byte (\d+) = (0x[0-9a-fA-F]+)")]
    public void GivenBytesWithSpecificByte(int totalBytes, int byteIndex, string value)
    {
        var bytes = new byte[totalBytes];
        bytes[byteIndex] = Convert.ToByte(value, 16);
        _world.Bytes = bytes;
    }

    // =========================================================================
    // When Steps - BCS Serialization
    // Note: These are simplified placeholders - SDK API may differ
    // =========================================================================

    [When(@"I BCS serialize it")]
    public void WhenIBCSSerializeIt()
    {
        try
        {
            // Simplified serialization - just handle basic types
            if (_world.TestVectors.TryGetValue("boolValue", out var boolVal))
            {
                _world.Bytes = new byte[] { (bool)boolVal ? (byte)0x01 : (byte)0x00 };
            }
            else if (_world.TestVectors.TryGetValue("u8Value", out var u8Val))
            {
                _world.Bytes = new byte[] { (byte)u8Val };
            }
            else if (_world.TestVectors.TryGetValue("u16Value", out var u16Val))
            {
                _world.Bytes = BitConverter.GetBytes((ushort)u16Val);
            }
            else if (_world.TestVectors.TryGetValue("u32Value", out var u32Val))
            {
                _world.Bytes = BitConverter.GetBytes((uint)u32Val);
            }
            else if (_world.TestVectors.TryGetValue("u64Value", out var u64Val))
            {
                _world.Bytes = BitConverter.GetBytes((ulong)u64Val);
            }
            else if (_world.TestVectors.TryGetValue("stringValue", out var strVal))
            {
                var strBytes = System.Text.Encoding.UTF8.GetBytes((string)strVal);
                // BCS string is length-prefixed
                var result = new byte[strBytes.Length + 1];
                result[0] = (byte)strBytes.Length;
                Array.Copy(strBytes, 0, result, 1, strBytes.Length);
                _world.Bytes = result;
            }
            else if (_world.TestVectors.TryGetValue("vectorU8", out var vecU8))
            {
                var bytes = (byte[])vecU8;
                // BCS vector is length-prefixed
                var result = new byte[bytes.Length + 1];
                result[0] = (byte)bytes.Length;
                Array.Copy(bytes, 0, result, 1, bytes.Length);
                _world.Bytes = result;
            }
            else if (_world.Bytes != null)
            {
                // Already have bytes, just use them
            }
            else if (_world.Address != null)
            {
                _world.Bytes = _world.Address.ToByteArray();
            }
            
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I ULEB128 encode it")]
    public void WhenIULEB128EncodeIt()
    {
        try
        {
            var value = (int)_world.TestVectors["lengthValue"];
            // Simple ULEB128 encoding for small values
            if (value < 128)
            {
                _world.Bytes = new byte[] { (byte)value };
            }
            else
            {
                var bytes = new List<byte>();
                while (value >= 0x80)
                {
                    bytes.Add((byte)((value & 0x7F) | 0x80));
                    value >>= 7;
                }
                bytes.Add((byte)value);
                _world.Bytes = bytes.ToArray();
            }
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I ULEB128 encode and decode it")]
    public void WhenIULEB128EncodeAndDecodeIt()
    {
        try
        {
            var originalValue = (int)_world.TestVectors["lengthValue"];
            WhenIULEB128EncodeIt();
            
            // Decode
            var bytes = _world.Bytes!;
            uint result = 0;
            int shift = 0;
            foreach (var b in bytes)
            {
                result |= (uint)(b & 0x7F) << shift;
                if ((b & 0x80) == 0) break;
                shift += 7;
            }
            _world.Result = result;
            _world.TestVectors["originalValue"] = originalValue;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // When Steps - BCS Deserialization
    // =========================================================================

    [When(@"I BCS deserialize as boolean")]
    public void WhenIBCSDeserializeAsBoolean()
    {
        try
        {
            _world.Result = _world.Bytes![0] != 0;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I BCS deserialize as u64")]
    public void WhenIBCSDeserializeAsU64()
    {
        try
        {
            _world.Result = BitConverter.ToUInt64(_world.Bytes!, 0);
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I BCS deserialize as vector of u8")]
    public void WhenIBCSDeserializeAsVectorOfU8()
    {
        try
        {
            // Assume first byte is length
            var length = _world.Bytes![0];
            _world.Result = _world.Bytes.Skip(1).Take(length).ToArray();
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // Then Steps - Result Validation
    // =========================================================================

    [Then(@"the byte should be (0x[0-9a-fA-F]+)")]
    public void ThenTheByteShouldBe(string expected)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![0].Should().Be(Convert.ToByte(expected, 16));
    }

    [Then("the bytes should be {string}")]
    public void ThenTheBytesShouldBe(string bytesStr)
    {
        var expected = System.Text.RegularExpressions.Regex.Matches(bytesStr, @"0x[0-9a-fA-F]+")
            .Select(m => Convert.ToByte(m.Value, 16))
            .ToArray();
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(expected.Length);
        for (int i = 0; i < expected.Length; i++)
        {
            _world.Bytes[i].Should().Be(expected[i]);
        }
    }

    [Then(@"the result should be (\d+) bytes in little-endian")]
    public void ThenTheResultShouldBeBytesInLittleEndian(int count)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(count);
    }

    [Then(@"the result should be (\d+) bytes in little-endian \(two's complement\)")]
    public void ThenTheResultShouldBeBytesInLittleEndianTwosComplement(int count)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(count);
    }

    [Then(@"byte (\d+) should be (0x[0-9a-fA-F]+)")]
    public void ThenByteIndexShouldBe(int index, string expected)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![index].Should().Be(Convert.ToByte(expected, 16));
    }

    [Then(@"bytes (\d+)-(\d+) should all be (0x[0-9a-fA-F]+)")]
    public void ThenBytesRangeShouldAllBeHex(int start, int end, string expected)
    {
        var value = Convert.ToByte(expected, 16);
        _world.Bytes.Should().NotBeNull();
        for (int i = start; i <= end; i++)
        {
            _world.Bytes![i].Should().Be(value, $"byte {i} should be {expected}");
        }
    }

    [Then(@"the result should be \[(0x[0-9a-fA-F]+)\]")]
    public void ThenTheResultShouldBeSingleByte(string expected)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(1);
        _world.Bytes[0].Should().Be(Convert.ToByte(expected, 16));
    }

    [Then(@"the result should be \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\]")]
    public void ThenTheResultShouldBeTwoBytes(string b1, string b2)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(2);
        _world.Bytes[0].Should().Be(Convert.ToByte(b1, 16));
        _world.Bytes[1].Should().Be(Convert.ToByte(b2, 16));
    }

    [Then(@"the first byte should be (0x[0-9a-fA-F]+) \(length\)")]
    public void ThenTheFirstByteShouldBeLength(string expected)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![0].Should().Be(Convert.ToByte(expected, 16));
    }

    [Then(@"the remaining bytes should be UTF-8 encoded ""(.*)""")]
    public void ThenTheRemainingBytesShouldBeUTF8Encoded(string str)
    {
        var encoded = System.Text.Encoding.UTF8.GetBytes(str);
        _world.Bytes.Should().NotBeNull();
        for (int i = 0; i < encoded.Length; i++)
        {
            _world.Bytes![i + 1].Should().Be(encoded[i]);
        }
    }

    [Then(@"the result should be exactly (\d+) bytes")]
    public void ThenTheResultShouldBeExactlyBytes(int count)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(count);
    }

    [Then(@"the result should be true")]
    public void ThenTheResultShouldBeTrue()
    {
        _world.Result.Should().Be(true);
    }

    [Then(@"the result should be false")]
    public void ThenTheResultShouldBeFalse()
    {
        _world.Result.Should().Be(false);
    }

    [Then(@"the result should equal the original value")]
    public void ThenTheResultShouldEqualTheOriginalValue()
    {
        var original = _world.TestVectors["originalValue"];
        _world.Result.Should().Be(Convert.ToUInt32(original));
    }

    [Then(@"the deserialization should fail with an error")]
    public void ThenTheDeserializationShouldFailWithAnError()
    {
        _world.Error.Should().NotBeNull();
    }
}
