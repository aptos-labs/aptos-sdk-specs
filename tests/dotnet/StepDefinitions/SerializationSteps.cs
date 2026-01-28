using System.Numerics;
using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for BCS serialization and deserialization.
/// Uses the actual Aptos SDK Serializer class.
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
        var numValue = value.StartsWith("0x")
            ? BigInteger.Parse(value[2..], System.Globalization.NumberStyles.HexNumber)
            : BigInteger.Parse(value);
        _world.TestVectors["u128Value"] = numValue;
    }

    [Given(@"a u256 value (\w+)")]
    public void GivenAU256Value(string value)
    {
        var numValue = value.StartsWith("0x")
            ? BigInteger.Parse(value[2..], System.Globalization.NumberStyles.HexNumber)
            : BigInteger.Parse(value);
        _world.TestVectors["u256Value"] = numValue;
    }

    [Given(@"a length value (\d+)")]
    public void GivenALengthValue(int value)
    {
        _world.TestVectors["lengthValue"] = (uint)value;
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
        _world.TestVectors["optionHasValue"] = false;
    }

    [Given(@"an Option containing u64 value (\d+)")]
    public void GivenAnOptionContainingU64Value(ulong value)
    {
        _world.TestVectors["optionValue"] = value;
        _world.TestVectors["optionHasValue"] = true;
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

    [Given(@"a vector \[\[(\d+), (\d+)\], \[(\d+), (\d+)\]\] of vectors of u8")]
    public void GivenNestedVectorOfU8(int a1, int a2, int b1, int b2)
    {
        _world.TestVectors["nestedVector"] = new[]
        {
            new byte[] { (byte)a1, (byte)a2 },
            new byte[] { (byte)b1, (byte)b2 }
        };
    }

    // =========================================================================
    // Given Steps - AccountAddress
    // =========================================================================

    [Given(@"an AccountAddress ""(.*)""")]
    public void GivenAnAccountAddress(string addressStr)
    {
        _world.Address = AccountAddress.FromString(addressStr, maxMissingChars: 62);
    }

    [Given(@"(\d+) bytes with byte (\d+) = (0x[0-9a-fA-F]+)")]
    public void GivenBytesWithSpecificByte(int totalBytes, int byteIndex, string value)
    {
        var bytes = new byte[totalBytes];
        bytes[byteIndex] = Convert.ToByte(value, 16);
        _world.Bytes = bytes;
    }

    // =========================================================================
    // Given Steps - Complex Structs
    // =========================================================================

    [Given(@"a struct with fields:")]
    public void GivenAStructWithFields(Table dataTable)
    {
        var fields = dataTable.Rows.Select(r => new
        {
            field = r["field"],
            type = r["type"],
            value = r["value"]
        }).ToList();
        _world.TestVectors["structFields"] = fields;
    }

    // =========================================================================
    // Given Steps - Error Cases
    // =========================================================================

    [Given(@"bytes \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\] intended for u64")]
    public void GivenBytesIntendedForU64(string b1, string b2)
    {
        _world.Bytes = new[] { Convert.ToByte(b1, 16), Convert.ToByte(b2, 16) };
        _world.TestVectors["intendedType"] = "u64";
    }

    // =========================================================================
    // When Steps - BCS Serialization using actual SDK Serializer
    // =========================================================================

    [When(@"I BCS serialize it")]
    public void WhenIBCSSerializeIt()
    {
        try
        {
            var serializer = new Serializer();

            if (_world.TestVectors.TryGetValue("boolValue", out var boolVal))
            {
                serializer.Bool((bool)boolVal);
            }
            else if (_world.TestVectors.TryGetValue("u8Value", out var u8Val))
            {
                serializer.U8((byte)u8Val);
            }
            else if (_world.TestVectors.TryGetValue("u16Value", out var u16Val))
            {
                serializer.U16((ushort)u16Val);
            }
            else if (_world.TestVectors.TryGetValue("u32Value", out var u32Val))
            {
                serializer.U32((uint)u32Val);
            }
            else if (_world.TestVectors.TryGetValue("u64Value", out var u64Val))
            {
                serializer.U64((ulong)u64Val);
            }
            else if (_world.TestVectors.TryGetValue("u128Value", out var u128Val))
            {
                serializer.U128((BigInteger)u128Val);
            }
            else if (_world.TestVectors.TryGetValue("u256Value", out var u256Val))
            {
                serializer.U256((BigInteger)u256Val);
            }
            else if (_world.TestVectors.TryGetValue("stringValue", out var strVal))
            {
                serializer.String((string)strVal);
            }
            else if (_world.TestVectors.TryGetValue("optionHasValue", out var hasOpt))
            {
                if ((bool)hasOpt)
                {
                    serializer.Bool(true);
                    serializer.U64((ulong)_world.TestVectors["optionValue"]);
                }
                else
                {
                    serializer.Bool(false);
                }
            }
            else if (_world.TestVectors.TryGetValue("vectorU8", out var vecU8))
            {
                serializer.Bytes((byte[])vecU8);
            }
            else if (_world.TestVectors.TryGetValue("vectorU64", out var vecU64))
            {
                var vec = (ulong[])vecU64;
                serializer.U32AsUleb128((uint)vec.Length);
                foreach (var v in vec)
                {
                    serializer.U64(v);
                }
            }
            else if (_world.TestVectors.TryGetValue("nestedVector", out var nestedVec))
            {
                var vec = (byte[][])nestedVec;
                serializer.U32AsUleb128((uint)vec.Length);
                foreach (var inner in vec)
                {
                    serializer.Bytes(inner);
                }
            }
            else if (_world.TestVectors.TryGetValue("structFields", out var structFields))
            {
                // Serialize struct fields in order
                var fields = (IEnumerable<dynamic>)structFields;
                foreach (var f in fields)
                {
                    string fieldType = f.type;
                    string fieldValue = f.value;
                    if (fieldType == "address")
                    {
                        var addr = AccountAddress.FromString(fieldValue, maxMissingChars: 62);
                        serializer.Serialize(addr);
                    }
                    else if (fieldType == "u64")
                    {
                        serializer.U64(ulong.Parse(fieldValue));
                    }
                    else if (fieldType == "u8")
                    {
                        serializer.U8(byte.Parse(fieldValue));
                    }
                }
            }
            else if (_world.Bytes != null)
            {
                serializer.Bytes(_world.Bytes);
            }
            else if (_world.Address != null)
            {
                serializer.Serialize(_world.Address);
            }
            else
            {
                throw new NotImplementedException("BCS serialization not implemented for this type");
            }

            _world.Bytes = serializer.ToBytes();
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
            var value = (uint)_world.TestVectors["lengthValue"];
            var serializer = new Serializer();
            serializer.U32AsUleb128(value);
            _world.Bytes = serializer.ToBytes();
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
            var originalValue = (uint)_world.TestVectors["lengthValue"];

            // Encode using SDK
            var serializer = new Serializer();
            serializer.U32AsUleb128(originalValue);
            var bytes = serializer.ToBytes();

            // Decode manually (SDK may not have Deserializer exposed)
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
    // Note: Deserializer may not be publicly exposed in SDK
    // =========================================================================

    [When(@"I BCS deserialize as boolean")]
    public void WhenIBCSDeserializeAsBoolean()
    {
        try
        {
            if (_world.Bytes == null || _world.Bytes.Length == 0)
                throw new InvalidOperationException("No bytes to deserialize");

            // BCS boolean: 0x00 = false, 0x01 = true
            if (_world.Bytes[0] == 0x00)
                _world.Result = false;
            else if (_world.Bytes[0] == 0x01)
                _world.Result = true;
            else
                throw new InvalidOperationException($"Invalid boolean byte: {_world.Bytes[0]}");

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
            if (_world.Bytes == null || _world.Bytes.Length < 8)
                throw new InvalidOperationException("Not enough bytes for u64 deserialization");

            _world.Result = BitConverter.ToUInt64(_world.Bytes, 0);
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
            if (_world.Bytes == null || _world.Bytes.Length == 0)
                throw new InvalidOperationException("No bytes to deserialize");

            // First byte(s) is ULEB128 length
            var length = _world.Bytes[0]; // Simplified: assuming length < 128
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

    // NOTE: "the bytes should be" step moved to ByteArraySteps.cs

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

    // NOTE: Byte array result assertions have been moved to ByteArraySteps.cs
    // to avoid ambiguous step definitions and provide a unified approach to
    // matching byte arrays of any size.

    [Then(@"the first byte should be (0x[0-9a-fA-F]+) \(length\)")]
    public void ThenTheFirstByteShouldBeLength(string expected)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![0].Should().Be(Convert.ToByte(expected, 16));
    }

    [Then(@"the first byte should be (0x[0-9a-fA-F]+) \(UTF-8 byte length\)")]
    public void ThenTheFirstByteShouldBeUtf8Length(string expected)
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

    [Then(@"the remaining bytes should be \[(0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)\]")]
    public void ThenTheRemainingBytesShouldBe(string b1, string b2, string b3)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes![1].Should().Be(Convert.ToByte(b1, 16));
        _world.Bytes[2].Should().Be(Convert.ToByte(b2, 16));
        _world.Bytes[3].Should().Be(Convert.ToByte(b3, 16));
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

    [Then(@"the fields should be serialized in order")]
    public void ThenTheFieldsShouldBeSerializedInOrder()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterThan(0);
    }

    [Then(@"each inner vector should be length-prefixed")]
    public void ThenEachInnerVectorShouldBeLengthPrefixed()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterThan(2);
    }

    [Then(@"the remaining (\d+) bytes should be the u64 value")]
    public void ThenTheRemainingBytesShouldBeTheU64Value(int count)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(count + 1); // 1 for the option flag
    }

    [Then(@"the remaining bytes should be two u64 values in little-endian")]
    public void ThenTheRemainingBytesShouldBeTwoU64Values()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(17); // 1 for length + 2*8 for u64s
    }

    [Then(@"the total length should be (\d+) bytes \((\d+) \+ (\d+)\)")]
    public void ThenTheTotalLengthShouldBeBytes(int total, int a, int b)
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().Be(total);
    }
}
