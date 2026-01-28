using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for API queries and view functions.
/// </summary>
[Binding]
public class ApiQuerySteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public ApiQuerySteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // When Steps - View Functions
    // =========================================================================

    [When("I call a function with wrong argument types")]
    public void WhenICallAFunctionWithWrongArgumentTypes()
    {
        _world.TestVectors["wrongArgTypes"] = true;
    }

    [When("I call it with a number")]
    public void WhenICallItWithANumber()
    {
        _world.TestVectors["calledWithNumber"] = true;
    }

    [When("I call it with a specific type")]
    public void WhenICallItWithASpecificType()
    {
        _world.TestVectors["calledWithType"] = true;
    }

    [When("I call it with an address string")]
    public void WhenICallItWithAnAddressString()
    {
        _world.TestVectors["calledWithAddress"] = true;
    }

    [When("I call it with byte array")]
    public void WhenICallItWithByteArray()
    {
        _world.TestVectors["calledWithBytes"] = true;
    }

    [When("I call it with the struct")]
    public void WhenICallItWithTheStruct()
    {
        _world.TestVectors["calledWithStruct"] = true;
    }

    [When("I parse the response")]
    public void WhenIParseTheResponse()
    {
        _world.TestVectors["responseParsed"] = true;
    }

    // =========================================================================
    // When Steps - Indexer Queries
    // =========================================================================

    [When("I query APT fungible asset balance")]
    public void WhenIQueryAPTFungibleAssetBalance()
    {
        _world.TestVectors["aptFABalanceQueried"] = true;
    }

    [When("I query account transactions")]
    public void WhenIQueryAccountTransactions()
    {
        _world.TestVectors["accountTxsQueried"] = true;
    }

    [When("I query coin balances from indexer")]
    public void WhenIQueryCoinBalancesFromIndexer()
    {
        _world.TestVectors["coinBalancesQueried"] = true;
    }

    [When("I query events involving that account")]
    public void WhenIQueryEventsInvolvingThatAccount()
    {
        _world.TestVectors["eventsQueried"] = true;
    }

    [When("I query it from indexer")]
    public void WhenIQueryItFromIndexer()
    {
        _world.TestVectors["indexerQueried"] = true;
    }

    [When("I query its metadata")]
    public void WhenIQueryItsMetadata()
    {
        _world.TestVectors["metadataQueried"] = true;
    }

    [When("I query only user transactions")]
    public void WhenIQueryOnlyUserTransactions()
    {
        _world.TestVectors["userTxsQueried"] = true;
    }

    [When("I request metadata")]
    public void WhenIRequestMetadata()
    {
        _world.TestVectors["metadataRequested"] = true;
    }

    [When("I try to query")]
    public void WhenITryToQuery()
    {
        try
        {
            _world.TestVectors["queryAttempted"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    // =========================================================================
    // When Steps - Account Checks
    // =========================================================================

    [When(@"I check can_sign\(\)")]
    public void WhenICheckCanSign()
    {
        _world.TestVectors["canSignChecked"] = true;
    }

    [When("I check gas info")]
    public void WhenICheckGasInfo()
    {
        _world.TestVectors["gasInfoChecked"] = true;
    }

    [When(@"I check is_expired\(\)")]
    public void WhenICheckIsExpired()
    {
        _world.TestVectors["isExpiredChecked"] = true;
    }

    [When(@"I check is_valid\(\)")]
    public void WhenICheckIsValid()
    {
        _world.TestVectors["isValidChecked"] = true;
    }

    [When(@"I call address\(\)")]
    public void WhenICallAddress()
    {
        if (_world.Account != null)
        {
            _world.Address = _world.Account.Address;
        }
    }

    // =========================================================================
    // When Steps - Faucet
    // =========================================================================

    [When("I call aptos.fund_account(address, amount)")]
    public void WhenICallAptosFundAccountAddressAmount()
    {
        _world.TestVectors["fundAccountCalled"] = true;
    }

    [When(@"I call create_funded_account with ""(.*)""_(\d+) octas")]
    public void WhenICallCreateFundedAccountWithOctas(string prefix, int amount)
    {
        _world.TestVectors["createFundedCalled"] = true;
        _world.TestVectors["fundAmount"] = amount;
    }

    [When(@"I request funding for ""(.*)""_(\d+) octas \((\d+) APT\)")]
    public void WhenIRequestFundingForOctasAPT(string prefix, int octas, int apt)
    {
        _world.TestVectors["fundingRequested"] = true;
        _world.TestVectors["fundAmount"] = octas;
    }

    // =========================================================================
    // When Steps - Simulation
    // =========================================================================

    [When("I try to submit a transaction")]
    public void WhenITryToSubmitATransaction()
    {
        try
        {
            _world.TestVectors["submissionAttempted"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("simulation takes too long")]
    public void WhenSimulationTakesTooLong()
    {
        _world.TestVectors["simulationTimeout"] = true;
    }

    [When("it's not found after timeout")]
    public void WhenItsNotFoundAfterTimeout()
    {
        _world.TestVectors["notFoundTimeout"] = true;
    }

    [When(@"I wait (\d+) seconds")]
    public void WhenIWaitSeconds(int seconds)
    {
        // Don't actually wait in tests
        _world.TestVectors["waitedSeconds"] = seconds;
    }
}
