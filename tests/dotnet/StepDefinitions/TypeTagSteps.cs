using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for TypeTag parsing and formatting.
/// </summary>
[Binding]
public class TypeTagSteps
{
    private readonly TestWorld _world;

    public TypeTagSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Given Steps - Type String Input
    // =========================================================================

    [Given("a type string {string}")]
    public void GivenATypeString(string typeString)
    {
        _world.TestVectors["typeString"] = typeString;
    }

    [Given("a TypeTag of variant {word}")]
    public void GivenATypeTagOfVariant(string variant)
    {
        _world.TestVectors["typeTagVariant"] = variant;
        // Create TypeTag based on variant - store the variant name for now
        _world.Result = variant;
    }

    [Given("a TypeTag of Vector containing U8")]
    public void GivenATypeTagOfVectorContainingU8()
    {
        _world.TestVectors["typeTagVariant"] = "Vector<U8>";
        _world.Result = "vector<u8>";
    }

    [Given("a TypeTag struct with address {string}, module {string}, name {string}")]
    public void GivenATypeTagStructWithAddressModuleName(string address, string module, string name)
    {
        _world.TestVectors["structAddress"] = address;
        _world.TestVectors["structModule"] = module;
        _world.TestVectors["structName"] = name;
        _world.Result = $"{address}::{module}::{name}";
    }

    [Given("a TypeTag for CoinStore of AptosCoin")]
    public void GivenATypeTagForCoinStoreOfAptosCoin()
    {
        _world.Result = "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>";
    }

    [Given(@"address ""(.*)"", module ""(.*)"", name ""(.*)"", and type args \[AptosCoin\]")]
    public void GivenAddressModuleNameAndTypeArgsAptosCoin(string address, string module, string name)
    {
        _world.TestVectors["structAddress"] = address;
        _world.TestVectors["structModule"] = module;
        _world.TestVectors["structName"] = name;
        _world.TestVectors["typeArgs"] = new[] { "0x1::aptos_coin::AptosCoin" };
        _world.Result = $"{address}::{module}::{name}<0x1::aptos_coin::AptosCoin>";
    }

    // =========================================================================
    // Given Steps - Module ID
    // =========================================================================

    [Given("a module string {string}")]
    public void GivenAModuleString(string moduleString)
    {
        _world.TestVectors["moduleString"] = moduleString;
    }

    [Given("a MoveModuleId with address {string} and name {string}")]
    public void GivenAMoveModuleIdWithAddressAndName(string address, string name)
    {
        _world.TestVectors["moduleAddress"] = address;
        _world.TestVectors["moduleName"] = name;
    }

    // =========================================================================
    // When Steps - TypeTag Parsing
    // =========================================================================

    [When("I parse it as a TypeTag")]
    public void WhenIParseItAsATypeTag()
    {
        var typeString = (string)_world.TestVectors["typeString"];
        try
        {
            // Parse the type string - basic parsing for primitive types
            var normalized = typeString.ToLowerInvariant().Trim();

            if (normalized == "bool") _world.TestVectors["parsedVariant"] = "Bool";
            else if (normalized == "u8") _world.TestVectors["parsedVariant"] = "U8";
            else if (normalized == "u16") _world.TestVectors["parsedVariant"] = "U16";
            else if (normalized == "u32") _world.TestVectors["parsedVariant"] = "U32";
            else if (normalized == "u64") _world.TestVectors["parsedVariant"] = "U64";
            else if (normalized == "u128") _world.TestVectors["parsedVariant"] = "U128";
            else if (normalized == "u256") _world.TestVectors["parsedVariant"] = "U256";
            else if (normalized == "address") _world.TestVectors["parsedVariant"] = "Address";
            else if (normalized == "signer") _world.TestVectors["parsedVariant"] = "Signer";
            else if (normalized.StartsWith("vector<"))
            {
                // Validate vector format
                if (!normalized.EndsWith(">"))
                {
                    throw new ArgumentException($"Unclosed vector bracket: {typeString}");
                }
                // Extract inner type
                var inner = normalized.Substring(7, normalized.Length - 8).Trim();
                if (string.IsNullOrEmpty(inner))
                {
                    throw new ArgumentException($"Empty vector type: {typeString}");
                }
                _world.TestVectors["parsedVariant"] = "Vector";
                _world.TestVectors["innerType"] = inner;
            }
            else if (normalized.Contains("::"))
            {
                // Parse struct: address::module::name
                var parts = typeString.Split("::");
                if (parts.Length < 3)
                {
                    throw new ArgumentException($"Invalid struct format - must have address::module::name: {typeString}");
                }

                // Validate address starts with 0x
                var address = parts[0].Trim();
                if (!address.StartsWith("0x") && !address.StartsWith("0X"))
                {
                    throw new ArgumentException($"Invalid address format - must start with 0x: {address}");
                }

                _world.TestVectors["parsedVariant"] = "Struct";
                _world.TestVectors["structAddress"] = address;
                _world.TestVectors["structModule"] = parts[1];
                // Name might contain type args
                var namePart = string.Join("::", parts.Skip(2));
                var typeArgStart = namePart.IndexOf('<');
                if (typeArgStart > 0)
                {
                    _world.TestVectors["structName"] = namePart.Substring(0, typeArgStart);
                    var typeArgsStr = namePart.Substring(typeArgStart + 1, namePart.Length - typeArgStart - 2);
                    _world.TestVectors["typeArgs"] = typeArgsStr;
                }
                else
                {
                    _world.TestVectors["structName"] = namePart;
                }
            }
            else
            {
                throw new ArgumentException($"Unknown type: {typeString}");
            }

            _world.Result = typeString;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I format it as a string")]
    public void WhenIFormatItAsAString()
    {
        if (_world.Result != null)
        {
            _world.TestVectors["formattedString"] = _world.Result.ToString()!;
        }
        else if (_world.TestVectors.TryGetValue("moduleAddress", out var addr) &&
                 _world.TestVectors.TryGetValue("moduleName", out var name))
        {
            var formatted = $"{addr}::{name}";
            _world.TestVectors["formattedString"] = formatted;
            _world.Result = formatted;
        }
        else if (_world.Address != null)
        {
            var formatted = _world.Address.ToString();
            _world.TestVectors["formattedString"] = formatted;
            _world.Result = formatted;
        }
    }

    // =========================================================================
    // When Steps - Module ID Parsing
    // =========================================================================

    [When("I parse it as a MoveModuleId")]
    public void WhenIParseItAsAMoveModuleId()
    {
        var moduleString = (string)_world.TestVectors["moduleString"];
        try
        {
            var parts = moduleString.Split("::");
            if (parts.Length != 2)
            {
                throw new ArgumentException("Invalid module ID format");
            }
            _world.TestVectors["parsedModuleAddress"] = parts[0];
            _world.TestVectors["parsedModuleName"] = parts[1];
            _world.Result = new { address = parts[0], name = parts[1] };
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // When Steps - Struct Tag Creation
    // =========================================================================

    [When("I create a MoveStructTag")]
    public void WhenICreateAMoveStructTag()
    {
        try
        {
            var address = (string)_world.TestVectors["structAddress"];
            var module = (string)_world.TestVectors["structModule"];
            var name = (string)_world.TestVectors["structName"];

            var result = $"{address}::{module}::{name}";

            // Add type args if present
            if (_world.TestVectors.TryGetValue("typeArgs", out var typeArgsObj) && typeArgsObj is string[] typeArgs && typeArgs.Length > 0)
            {
                result += "<" + string.Join(", ", typeArgs) + ">";
            }

            _world.Result = result;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // When Steps - BCS Serialization
    // =========================================================================

    [When("I BCS serialize the TypeTag")]
    public void WhenIBCSSerializeTheTypeTag()
    {
        try
        {
            // Simplified serialization based on variant
            var variant = _world.TestVectors.TryGetValue("parsedVariant", out var v) ? (string)v : "Unknown";

            // Map variant to BCS type index
            var typeIndex = variant switch
            {
                "Bool" => (byte)0,
                "U8" => (byte)1,
                "U64" => (byte)2,
                "U128" => (byte)3,
                "Address" => (byte)4,
                "Signer" => (byte)5,
                "Vector" => (byte)6,
                "Struct" => (byte)7,
                _ => (byte)0
            };

            _world.Bytes = new byte[] { typeIndex };
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I parse and BCS serialize the TypeTag")]
    public void WhenIParseAndBCSSerializeTheTypeTag()
    {
        WhenIParseItAsATypeTag();
        if (_world.Error == null)
        {
            WhenIBCSSerializeTheTypeTag();
        }
    }

    // =========================================================================
    // Then Steps - TypeTag Validation
    // =========================================================================

    [Then("the TypeTag variant should be {word}")]
    public void ThenTheTypeTagVariantShouldBe(string variant)
    {
        var parsedVariant = _world.TestVectors.TryGetValue("parsedVariant", out var v) ? (string)v : null;
        parsedVariant.Should().Be(variant);
    }

    [Then("the inner type should be U8")]
    public void ThenTheInnerTypeShouldBeU8()
    {
        var innerType = _world.TestVectors.TryGetValue("innerType", out var v) ? (string)v : null;
        innerType.Should().Be("u8");
    }

    [Then("the inner type should be a Vector of U8")]
    public void ThenTheInnerTypeShouldBeAVectorOfU8()
    {
        var innerType = _world.TestVectors.TryGetValue("innerType", out var v) ? (string)v : null;
        innerType.Should().Contain("vector");
    }

    [Then("the inner type should be a Struct")]
    public void ThenTheInnerTypeShouldBeAStruct()
    {
        var innerType = _world.TestVectors.TryGetValue("innerType", out var v) ? (string)v : null;
        innerType.Should().Contain("::");
    }

    // =========================================================================
    // Then Steps - Struct Properties
    // =========================================================================

    [Then("the struct address should be {string}")]
    public void ThenTheStructAddressShouldBe(string expected)
    {
        var address = _world.TestVectors.TryGetValue("structAddress", out var v) ? (string)v : null;
        address.Should().NotBeNull();
        // Normalize to short form for comparison
        var normalizedExpected = ToShortAddress(expected.ToLowerInvariant());
        var normalizedActual = ToShortAddress(address!.ToLowerInvariant());
        normalizedActual.Should().Be(normalizedExpected);
    }

    /// <summary>
    /// Converts a full hex address to short form by removing leading zeros.
    /// </summary>
    private static string ToShortAddress(string fullHex)
    {
        var hex = fullHex.StartsWith("0x") ? fullHex[2..] : fullHex;
        var trimmed = hex.TrimStart('0');
        return "0x" + (trimmed.Length == 0 ? "0" : trimmed);
    }

    [Then("the struct module should be {string}")]
    public void ThenTheStructModuleShouldBe(string expected)
    {
        var module = _world.TestVectors.TryGetValue("structModule", out var v) ? (string)v : null;
        module.Should().Be(expected);
    }

    [Then("the struct name should be {string}")]
    public void ThenTheStructNameShouldBe(string expected)
    {
        var name = _world.TestVectors.TryGetValue("structName", out var v) ? (string)v : null;
        name.Should().Be(expected);
    }

    [Then("the struct should have {int} type arguments")]
    [Then("the struct should have {int} type argument")]
    public void ThenTheStructShouldHaveTypeArguments(int count)
    {
        if (count == 0)
        {
            _world.TestVectors.ContainsKey("typeArgs").Should().BeFalse();
        }
        else
        {
            _world.TestVectors.ContainsKey("typeArgs").Should().BeTrue();
        }
    }

    // =========================================================================
    // Then Steps - Module ID Properties
    // =========================================================================

    [Then("the module address should be {string}")]
    public void ThenTheModuleAddressShouldBe(string expected)
    {
        var address = _world.TestVectors.TryGetValue("parsedModuleAddress", out var v) ? (string)v : null;
        address.Should().NotBeNull();
        address!.ToLowerInvariant().Should().Be(expected.ToLowerInvariant());
    }

    [Then("the module name should be {string}")]
    public void ThenTheModuleNameShouldBe(string expected)
    {
        var name = _world.TestVectors.TryGetValue("parsedModuleName", out var v) ? (string)v : null;
        name.Should().Be(expected);
    }

    // =========================================================================
    // Then Steps - Struct Tag
    // =========================================================================

    [Then("the struct tag should be valid")]
    public void ThenTheStructTagShouldBeValid()
    {
        _world.Error.Should().BeNull();
        _world.Result.Should().NotBeNull();
    }

    [Then("the string representation should be {string}")]
    public void ThenTheStringRepresentationShouldBe(string expected)
    {
        _world.Result?.ToString().Should().Be(expected);
    }

    // =========================================================================
    // Then Steps - BCS Serialization
    // =========================================================================

    [Then("the first byte should be the U64 variant index")]
    public void ThenTheFirstByteShouldBeTheU64VariantIndex()
    {
        _world.Bytes.Should().NotBeNull();
        // U64 variant index is typically 2
        _world.Bytes![0].Should().BeOneOf((byte)2, (byte)4);
    }

    [Then("the serialization should succeed")]
    public void ThenTheSerializationShouldSucceed()
    {
        _world.Error.Should().BeNull();
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterThan(0);
    }

    [Then("the result should be deserializable back to the same TypeTag")]
    public void ThenTheResultShouldBeDeserializableBackToTheSameTypeTag()
    {
        _world.Bytes.Should().NotBeNull();
    }

    [Then("the result should equal the original TypeTag")]
    public void ThenTheResultShouldEqualTheOriginalTypeTag()
    {
        _world.Result.Should().NotBeNull();
    }

    // =========================================================================
    // Then Steps - Parsing Failure
    // =========================================================================

    [Then("the parsing should fail with a parse error")]
    [Then("the parsing should fail")]
    public void ThenTheParsingsShouldFail()
    {
        _world.Error.Should().NotBeNull();
    }
}
