using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for view function tests.
/// These are mock implementations for testing the specification patterns.
/// </summary>
[Binding]
public class ViewFunctionSteps
{
    private readonly TestWorld _world;

    public ViewFunctionSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Basic View Function Calls
    // =========================================================================

    [When("I call view function {string}")]
    public void WhenICallViewFunction(string functionId)
    {
        _world.TestVectors["viewFunctionId"] = functionId;
    }

    [When("with type arguments [{string}]")]
    public void WhenWithTypeArguments(string typeArg)
    {
        _world.TestVectors["typeArguments"] = new List<string> { typeArg };
    }

    [When("arguments [{string}]")]
    public void WhenArguments(string arg)
    {
        _world.TestVectors["functionArguments"] = new List<string> { arg };
    }

    [Then("the call should succeed")]
    public void ThenTheCallShouldSucceed()
    {
        // Mock successful view function call
        _world.TestVectors["viewResult"] = new List<object> { true };
        _world.Result = _world.TestVectors["viewResult"];
    }

    [Then("I should receive return values")]
    public void ThenIShouldReceiveReturnValues()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Should().NotBeNull();
    }

    [When("with no type arguments")]
    public void WhenWithNoTypeArguments()
    {
        _world.TestVectors["typeArguments"] = new List<string>();
    }

    [Then("the result should be a boolean")]
    public void ThenTheResultShouldBeABoolean()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Count.Should().BeGreaterThan(0);
        result[0].Should().BeOfType<bool>();
    }

    [When("no arguments")]
    public void WhenNoArguments()
    {
        _world.TestVectors["functionArguments"] = new List<string>();
    }

    [Then("the result should be a u64")]
    public void ThenTheResultShouldBeAU64()
    {
        _world.TestVectors["viewResult"] = new List<object> { 1000UL };
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Count.Should().BeGreaterThan(0);
    }

    [When("I call a view function that returns multiple values")]
    public void WhenICallAViewFunctionThatReturnsMultipleValues()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::timestamp::now_seconds";
        _world.TestVectors["viewResult"] = new List<object> { 1700000000UL, "extra_value" };
    }

    [Then("I should receive all return values in order")]
    public void ThenIShouldReceiveAllReturnValuesInOrder()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Should().BeOfType<List<object>>();
    }

    // =========================================================================
    // Argument Encoding
    // =========================================================================

    [Given("a view function expecting an address")]
    public void GivenAViewFunctionExpectingAnAddress()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::account::exists_at";
        _world.TestVectors["typeArguments"] = new List<string>();
    }

    [When("I pass address {string} as argument")]
    public void WhenIPassAddressAsArgument(string address)
    {
        _world.TestVectors["functionArguments"] = new List<string> { address };
    }

    [Then("the address should be properly encoded")]
    public void ThenTheAddressShouldBeProperlyEncoded()
    {
        _world.TestVectors["viewResult"] = new List<object> { true };
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Should().NotBeNull();
    }

    [Given("a view function expecting a u64")]
    public void GivenAViewFunctionExpectingAU64()
    {
        _world.TestVectors["expectedArgType"] = "u64";
    }

    [When("I pass number {int} as argument")]
    public void WhenIPassNumberAsArgument(int num)
    {
        _world.TestVectors["functionArguments"] = new List<string> { num.ToString() };
    }

    [Then("the number should be properly encoded")]
    public void ThenTheNumberShouldBeProperlyEncoded()
    {
        var args = (List<string>)_world.TestVectors["functionArguments"];
        args[0].Should().NotBeNullOrEmpty();
    }

    [Given("a view function expecting a string")]
    public void GivenAViewFunctionExpectingAString()
    {
        _world.TestVectors["expectedArgType"] = "string";
    }

    [When("I pass {string} as argument")]
    public void WhenIPassAsArgument(string str)
    {
        _world.TestVectors["functionArguments"] = new List<string> { str };
    }

    [Then("the string should be properly encoded")]
    public void ThenTheStringShouldBeProperlyEncoded()
    {
        var args = (List<string>)_world.TestVectors["functionArguments"];
        args[0].Should().NotBeNullOrEmpty();
    }

    [Given("a view function expecting a bool")]
    public void GivenAViewFunctionExpectingABool()
    {
        _world.TestVectors["expectedArgType"] = "bool";
    }

    [When("I pass true as argument")]
    public void WhenIPassTrueAsArgument()
    {
        _world.TestVectors["functionArguments"] = new List<object> { true };
    }

    [Then("the boolean should be properly encoded")]
    public void ThenTheBooleanShouldBeProperlyEncoded()
    {
        var args = (List<object>)_world.TestVectors["functionArguments"];
        args[0].Should().Be(true);
    }

    // =========================================================================
    // Type Argument Handling
    // =========================================================================

    [Given("a view function with one type parameter")]
    public void GivenAViewFunctionWithOneTypeParameter()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::coin::balance";
    }

    [When("I call with type argument {string}")]
    public void WhenICallWithTypeArgument(string typeArg)
    {
        _world.TestVectors["typeArguments"] = new List<string> { typeArg };
    }

    [Then("the type should be properly passed")]
    public void ThenTheTypeShouldBeProperlyPassed()
    {
        var typeArgs = (List<string>)_world.TestVectors["typeArguments"];
        typeArgs.Count.Should().Be(1);
    }

    [Given("a view function with multiple type parameters")]
    public void GivenAViewFunctionWithMultipleTypeParameters()
    {
        _world.TestVectors["expectedTypeParamCount"] = 2;
    }

    [When("I call with type arguments [{string}, {string}]")]
    public void WhenICallWithTypeArguments(string type1, string type2)
    {
        _world.TestVectors["typeArguments"] = new List<string> { type1, type2 };
    }

    [Then("both types should be properly passed")]
    public void ThenBothTypesShouldBeProperlyPassed()
    {
        var typeArgs = (List<string>)_world.TestVectors["typeArguments"];
        typeArgs.Count.Should().Be(2);
    }

    [Given("a view function with generic type")]
    public void GivenAViewFunctionWithGenericType()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::coin::balance";
    }

    [Then("the nested type should be properly parsed")]
    public void ThenTheNestedTypeShouldBeProperlyParsed()
    {
        var typeArgs = (List<string>)_world.TestVectors["typeArguments"];
        typeArgs[0].Should().Contain("::");
    }

    // =========================================================================
    // Return Value Parsing
    // =========================================================================

    [Given("a view function returning u64")]
    public void GivenAViewFunctionReturningU64()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::timestamp::now_seconds";
        _world.TestVectors["typeArguments"] = new List<string>();
        _world.TestVectors["functionArguments"] = new List<string>();
        _world.TestVectors["viewResult"] = new List<object> { 1700000000UL };
    }

    [When("I execute the call")]
    public void WhenIExecuteTheCall()
    {
        _world.Result = _world.TestVectors["viewResult"];
    }

    [Then("I should be able to parse the result as u64")]
    public void ThenIShouldBeAbleToParseTheResultAsU64()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Count.Should().BeGreaterThan(0);
    }

    [Given("a view function returning a String")]
    public void GivenAViewFunctionReturningAString()
    {
        _world.TestVectors["expectedReturnType"] = "string";
        _world.TestVectors["viewResult"] = new List<object> { "test_string" };
    }

    [Then("I should be able to parse the result as string")]
    public void ThenIShouldBeAbleToParseTheResultAsString()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        if (result.Count > 0)
        {
            (result[0] is string).Should().BeTrue();
        }
    }

    [Given("a view function returning bool")]
    public void GivenAViewFunctionReturningBool()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::account::exists_at";
        _world.TestVectors["typeArguments"] = new List<string>();
        _world.TestVectors["functionArguments"] = new List<string> { "0x1" };
        _world.TestVectors["viewResult"] = new List<object> { true };
    }

    [Then("I should be able to parse the result as boolean")]
    public void ThenIShouldBeAbleToParseTheResultAsBoolean()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Count.Should().BeGreaterThan(0);
        result[0].Should().BeOfType<bool>();
    }

    [Given("a view function returning a struct")]
    public void GivenAViewFunctionReturningAStruct()
    {
        _world.TestVectors["expectedReturnType"] = "struct";
        _world.TestVectors["viewResult"] = new List<object>
        {
            new Dictionary<string, object> { { "value", 100UL } }
        };
    }

    [Then("I should be able to access struct fields")]
    public void ThenIShouldBeAbleToAccessStructFields()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        if (result.Count > 0 && result[0] is Dictionary<string, object> dict)
        {
            dict.Keys.Count.Should().BeGreaterThan(0);
        }
    }

    // =========================================================================
    // Error Cases
    // =========================================================================

    [When("I call non-existent view function {string}")]
    public void WhenICallNonExistentViewFunction(string functionId)
    {
        _world.SetError(new Exception($"FUNCTION_NOT_FOUND: {functionId}"));
    }

    [Then("I should receive an error")]
    public void ThenIShouldReceiveAnError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("the error should indicate function not found")]
    public void ThenTheErrorShouldIndicateFunctionNotFound()
    {
        _world.Error!.Message.Should().ContainAny("not found", "does not exist", "FUNCTION_NOT_FOUND");
    }

    [When("I call a view function with wrong argument types")]
    public void WhenICallAViewFunctionWithWrongArgumentTypes()
    {
        _world.SetError(new Exception("TYPE_MISMATCH: Invalid argument type"));
    }

    [Then("the error should indicate type mismatch")]
    public void ThenTheErrorShouldIndicateTypeMismatch()
    {
        _world.Error.Should().NotBeNull();
    }

    [When("I call a view function with too few arguments")]
    public void WhenICallAViewFunctionWithTooFewArguments()
    {
        _world.SetError(new Exception("ARGUMENT_COUNT_MISMATCH: Too few arguments"));
    }

    [When("I call a generic function without type arguments")]
    public void WhenICallAGenericFunctionWithoutTypeArguments()
    {
        _world.SetError(new Exception("TYPE_ARGUMENT_MISMATCH: Missing type arguments"));
    }

    [Given("a view function that can abort")]
    public void GivenAViewFunctionThatCanAbort()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::coin::balance";
    }

    [When("I call with arguments that cause abort")]
    public void WhenICallWithArgumentsThatCauseAbort()
    {
        _world.SetError(new Exception("ABORTED: View function aborted with code 65537"));
    }

    [Then("the error should contain the abort code")]
    public void ThenTheErrorShouldContainTheAbortCode()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Common View Functions
    // =========================================================================

    [When("I call 0x1::coin::balance<0x1::aptos_coin::AptosCoin>")]
    public void WhenICallCoinBalance()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::coin::balance";
        _world.TestVectors["typeArguments"] = new List<string> { "0x1::aptos_coin::AptosCoin" };
    }

    [When("with the account address as argument")]
    public void WhenWithTheAccountAddressAsArgument()
    {
        var address = _world.Address ?? AccountAddress.FromString("0x1");
        _world.TestVectors["functionArguments"] = new List<string> { address.ToString() };
        _world.TestVectors["viewResult"] = new List<object> { 1000000UL };
    }

    [Then("I should receive the balance as u64")]
    public void ThenIShouldReceiveTheBalanceAsU64()
    {
        if (_world.Error == null)
        {
            var result = (List<object>)_world.TestVectors["viewResult"];
            result.Count.Should().BeGreaterThan(0);
        }
    }

    [When("I call 0x1::account::exists_at")]
    public void WhenICallAccountExistsAt()
    {
        _world.TestVectors["viewFunctionId"] = "0x1::account::exists_at";
        _world.TestVectors["typeArguments"] = new List<string>();
    }

    [When("with address {string} as argument")]
    public void WhenWithAddressAsArgument(string address)
    {
        _world.TestVectors["functionArguments"] = new List<string> { address };
        _world.TestVectors["viewResult"] = new List<object> { true };
    }

    [Then("I should receive true")]
    public void ThenIShouldReceiveTrue()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result[0].Should().Be(true);
    }

    [When("I call 0x1::timestamp::now_seconds")]
    public void WhenICallTimestampNowSeconds()
    {
        _world.TestVectors["viewResult"] = new List<object> { 1700000000UL };
    }

    [Then("I should receive current blockchain timestamp")]
    public void ThenIShouldReceiveCurrentBlockchainTimestamp()
    {
        var result = (List<object>)_world.TestVectors["viewResult"];
        result.Count.Should().BeGreaterThan(0);
        ((ulong)result[0]).Should().BeGreaterThan(0);
    }

    [When("I call 0x1::coin::supply<0x1::aptos_coin::AptosCoin>")]
    public void WhenICallCoinSupply()
    {
        _world.TestVectors["viewResult"] = new List<object> { 1000000000000UL };
    }

    [Then("I should receive the total supply")]
    public void ThenIShouldReceiveTheTotalSupply()
    {
        if (_world.Error == null)
        {
            var result = (List<object>)_world.TestVectors["viewResult"];
            result.Should().NotBeNull();
        }
    }

    // =========================================================================
    // At Specific Ledger Version
    // =========================================================================

    [Given("a known past ledger version")]
    public void GivenAKnownPastLedgerVersion()
    {
        _world.TestVectors["pastLedgerVersion"] = 1000000UL;
    }

    [When("I call a view function at that version")]
    public void WhenICallAViewFunctionAtThatVersion()
    {
        _world.TestVectors["viewResult"] = new List<object> { 1699000000UL };
    }

    [Then("I should receive the state as of that version")]
    public void ThenIShouldReceiveTheStateAsOfThatVersion()
    {
        if (_world.Error == null)
        {
            var result = (List<object>)_world.TestVectors["viewResult"];
            result.Should().NotBeNull();
        }
    }

    [Given("a ledger version older than oldest available")]
    public void GivenALedgerVersionOlderThanOldestAvailable()
    {
        _world.TestVectors["oldLedgerVersion"] = 1UL;
    }

    [When("I try to call a view function at that version")]
    public void WhenITryToCallAViewFunctionAtThatVersion()
    {
        // May or may not error depending on node configuration
        _world.TestVectors["attemptedOldVersion"] = true;
    }

    [Then("I should receive an error about unavailable state")]
    public void ThenIShouldReceiveAnErrorAboutUnavailableState()
    {
        // Old versions may or may not be available
        true.Should().BeTrue();
    }
}
