using Reqnroll;

namespace Aptos.Specs.Support;

/// <summary>
/// Reqnroll hooks for scenario lifecycle management.
/// </summary>
[Binding]
public class Hooks
{
    private readonly TestWorld _world;

    public Hooks(TestWorld world)
    {
        _world = world;
    }

    /// <summary>
    /// Reset world state before each scenario
    /// </summary>
    [BeforeScenario]
    public void BeforeScenario()
    {
        _world.Reset();
    }

    /// <summary>
    /// Cleanup after each scenario
    /// </summary>
    [AfterScenario]
    public void AfterScenario()
    {
        // Clear client reference - AptosClient doesn't implement IDisposable
        _world.Client = null;
    }
}
