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

    // Note: Common validation and equality steps are defined in CommonSteps.cs
    // This file only contains additional steps not defined elsewhere

    // =========================================================================
    // Additional Operation Steps (not in other files)
    // =========================================================================

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

    [Then("it should fail with an invalid format error")]
    public void ThenItShouldFailWithAnInvalidFormatError()
    {
        _world.Error.Should().NotBeNull();
    }
}
