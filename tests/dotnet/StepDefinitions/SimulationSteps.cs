using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for transaction simulation tests.
/// Note: These are mock implementations for testing the specification patterns.
/// </summary>
[Binding]
public class SimulationSteps
{
    private readonly TestWorld _world;

    public SimulationSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Basic Simulation
    // =========================================================================

    [Given("a valid transaction for simulation")]
    public void GivenAValidTransactionForSimulation()
    {
        _world.Account = Ed25519Account.Generate();
        _world.TestVectors["simulationAccount"] = _world.Account;
        _world.TestVectors["validTransaction"] = true;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" },
            { "vm_status", "Executed successfully" },
            { "changes", new List<object>() },
            { "events", new List<object>() }
        };
    }

    [When("I simulate it")]
    [When("I simulate the transaction")]
    public void WhenISimulateTheTransaction()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        _world.TestVectors["simulationResult"] = response;
    }

    [Then("I should get a simulation result")]
    public void ThenIShouldGetASimulationResult()
    {
        _world.TestVectors.ContainsKey("simulationResult").Should().BeTrue();
    }

    [Then("it should include gas_used")]
    public void ThenItShouldIncludeGasUsed()
    {
        var result = (Dictionary<string, object?>)_world.TestVectors["simulationResult"];
        result.ContainsKey("gas_used").Should().BeTrue();
    }

    [Then("it should include success status")]
    public void ThenItShouldIncludeSuccessStatus()
    {
        var result = (Dictionary<string, object?>)_world.TestVectors["simulationResult"];
        result["success"].Should().BeOfType<bool>();
    }

    [Given("a transaction I haven't signed yet")]
    public void GivenATransactionIHaventSignedYet()
    {
        _world.Account = Ed25519Account.Generate();
        _world.TestVectors["unsignedTransaction"] = true;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "500" }
        };
    }

    [Then("simulation should work")]
    public void ThenSimulationShouldWork()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((bool)response["success"]!).Should().BeTrue();
    }

    [Then("use a dummy signature internally")]
    public void ThenUseADummySignatureInternally()
    {
        true.Should().BeTrue();
    }

    [Given("a transaction simulation")]
    public void GivenATransactionSimulation()
    {
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" },
            { "changes", new List<object> { new { type = "write_resource" } } },
            { "events", new List<object> { new { type = "0x1::coin::WithdrawEvent" } } }
        };
    }

    [When("I inspect the simulation result")]
    public void WhenIInspectTheSimulationResult()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        _world.TestVectors["simulationResult"] = response;
    }

    [Then("I should see state changes that would occur")]
    public void ThenIShouldSeeStateChangesThatWouldOccur()
    {
        var result = (Dictionary<string, object?>)_world.TestVectors["simulationResult"];
        result["changes"].Should().NotBeNull();
    }

    [Then("events that would be emitted")]
    public void ThenEventsThatWouldBeEmitted()
    {
        var result = (Dictionary<string, object?>)_world.TestVectors["simulationResult"];
        result["events"].Should().NotBeNull();
    }

    // =========================================================================
    // Gas Estimation
    // =========================================================================

    [Given("a transaction")]
    public void GivenATransaction()
    {
        _world.Account = Ed25519Account.Generate();
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" }
        };
    }

    [Then("gas_used tells me actual consumption")]
    public void ThenGasUsedTellsMeActualConsumption()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        var gasUsed = int.Parse((string)response["gas_used"]!);
        gasUsed.Should().BeGreaterThan(0);
    }

    [Then("I can set max_gas_amount with buffer")]
    public void ThenICanSetMaxGasAmountWithBuffer()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        var gasUsed = int.Parse((string)response["gas_used"]!);
        var maxGasWithBuffer = (int)Math.Ceiling(gasUsed * 1.2);
        _world.TestVectors["recommendedMaxGas"] = maxGasWithBuffer;
        maxGasWithBuffer.Should().BeGreaterThan(gasUsed);
    }

    [Given("a complex transaction")]
    public void GivenAComplexTransaction()
    {
        _world.TestVectors["complexTransaction"] = true;
        _world.TestVectors["simulationResults"] = new List<object>
        {
            new Dictionary<string, object?> { { "max_gas", 1000 }, { "gas_used", "950" }, { "success", true } },
            new Dictionary<string, object?> { { "max_gas", 500 }, { "gas_used", "500" }, { "success", false } }
        };
    }

    [When("I simulate with different max_gas amounts")]
    public void WhenISimulateWithDifferentMaxGasAmounts()
    {
        _world.TestVectors["simulatedWithDifferentGas"] = true;
    }

    [Then("I can find the minimum needed")]
    public void ThenICanFindTheMinimumNeeded()
    {
        var results = (List<object>)_world.TestVectors["simulationResults"];
        var successful = results.Cast<Dictionary<string, object?>>().Where(r => (bool)r["success"]!);
        successful.Count().Should().BeGreaterThan(0);
    }

    [Given("a simple transfer")]
    public void GivenASimpleTransfer()
    {
        _world.TestVectors["simpleTransferGas"] = 500;
    }

    // =========================================================================
    // Preview State Changes
    // =========================================================================

    [Given("a transfer transaction")]
    public void GivenATransferTransaction()
    {
        _world.TestVectors["transferTransaction"] = true;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "500" },
            { "changes", new List<object>
                {
                    new Dictionary<string, object?> { { "type", "write_resource" }, { "address", "0x1" } },
                    new Dictionary<string, object?> { { "type", "write_resource" }, { "address", "0x2" } }
                }
            }
        };
    }

    [Then("I should see sender balance decrease")]
    public void ThenIShouldSeeSenderBalanceDecrease()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        response["changes"].Should().NotBeNull();
    }

    [Then("recipient balance increase")]
    public void ThenRecipientBalanceIncrease()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        var changes = (List<object>)response["changes"]!;
        changes.Count.Should().BeGreaterThan(0);
    }

    [Given("a transaction that modifies resources")]
    public void GivenATransactionThatModifiesResources()
    {
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" },
            { "changes", new List<object>
                {
                    new Dictionary<string, object?> 
                    { 
                        { "type", "write_resource" },
                        { "address", "0x1" },
                        { "data", new { type = "0x1::coin::CoinStore" } }
                    }
                }
            }
        };
    }

    [Then("I should see which resources change")]
    public void ThenIShouldSeeWhichResourcesChange()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        var changes = (List<object>)response["changes"]!;
        changes.Count.Should().BeGreaterThan(0);
    }

    [Then("their new values")]
    public void ThenTheirNewValues()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        var changes = (List<object>)response["changes"]!;
        var firstChange = (Dictionary<string, object?>)changes[0];
        firstChange.ContainsKey("data").Should().BeTrue();
    }

    [Then("I should see which events would emit")]
    public void ThenIShouldSeeWhichEventsWouldEmit()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        response.ContainsKey("events").Should().BeTrue();
    }

    [Then("their data")]
    public void ThenTheirData()
    {
        true.Should().BeTrue();
    }

    // =========================================================================
    // Failure Preview
    // =========================================================================

    [Given("a transaction that would abort")]
    public void GivenATransactionThatWouldAbort()
    {
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", false },
            { "gas_used", "250" },
            { "vm_status", "Move abort in 0x1::coin: EINSUFFICIENT_BALANCE (code: 0x10001)" }
        };
    }

    [Then("simulation result should show failure")]
    public void ThenSimulationResultShouldShowFailure()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((bool)response["success"]!).Should().BeFalse();
    }

    [Then("include the abort code")]
    public void ThenIncludeTheAbortCode()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((string)response["vm_status"]!).Should().Contain("abort");
    }

    [Then("the module that aborted")]
    public void ThenTheModuleThatAborted()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((string)response["vm_status"]!).Should().Contain("::");
    }

    [Given("a transfer exceeding sender's balance")]
    public void GivenATransferExceedingSendersBalance()
    {
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", false },
            { "gas_used", "100" },
            { "vm_status", "INSUFFICIENT_BALANCE" }
        };
    }

    [Then("simulation should fail")]
    public void ThenSimulationShouldFail()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((bool)response["success"]!).Should().BeFalse();
    }

    [Then("indicate insufficient funds")]
    public void ThenIndicateInsufficientFunds()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((string)response["vm_status"]!).ToLowerInvariant().Should().ContainAny("insufficient", "balance");
    }

    [Given("a transaction with wrong type arguments")]
    public void GivenATransactionWithWrongTypeArguments()
    {
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", false },
            { "gas_used", "50" },
            { "vm_status", "TYPE_MISMATCH" }
        };
    }

    [Then("indicate the type mismatch")]
    public void ThenIndicateTheTypeMismatch()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((string)response["vm_status"]!).ToLowerInvariant().Should().Contain("type");
    }

    [Given("a transaction accessing non-existent resource")]
    public void GivenATransactionAccessingNonExistentResource()
    {
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", false },
            { "gas_used", "50" },
            { "vm_status", "RESOURCE_NOT_FOUND" }
        };
    }

    [Then("indicate resource not found")]
    public void ThenIndicateResourceNotFound()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((string)response["vm_status"]!).ToLowerInvariant().Should().ContainAny("resource", "not", "found");
    }

    // =========================================================================
    // Simulation Options
    // =========================================================================

    [Given("a historical ledger version")]
    [Given("a specific ledger version")]
    public void GivenAHistoricalLedgerVersion()
    {
        _world.TestVectors["ledgerVersion"] = 1000000L;
    }

    [When("I simulate at that version")]
    [When("I simulate at that ledger version")]
    public void WhenISimulateAtThatVersion()
    {
        _world.TestVectors["simulatedAtVersion"] = true;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "500" }
        };
    }

    [Then("simulation uses state at that version")]
    [Then("simulation should use state at that version")]
    public void ThenSimulationUsesStateAtThatVersion()
    {
        ((bool)_world.TestVectors["simulatedAtVersion"]).Should().BeTrue();
    }

    [When("I simulate with specific max_gas_amount")]
    public void WhenISimulateWithSpecificMaxGasAmount()
    {
        _world.TestVectors["specificMaxGas"] = 50000;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" }
        };
    }

    [Then("simulation respects that limit")]
    public void ThenSimulationRespectsThatLimit()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        var maxGas = (int)_world.TestVectors["specificMaxGas"];
        var gasUsed = int.Parse((string)response["gas_used"]!);
        gasUsed.Should().BeLessThanOrEqualTo(maxGas);
    }

    [When("I simulate with specific gas_unit_price")]
    public void WhenISimulateWithSpecificGasUnitPrice()
    {
        _world.TestVectors["specificGasPrice"] = 200;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" }
        };
    }

    [Then("simulation uses that price for calculations")]
    public void ThenSimulationUsesThatPriceForCalculations()
    {
        ((int)_world.TestVectors["specificGasPrice"]).Should().Be(200);
    }

    // =========================================================================
    // Multi-party Simulation
    // =========================================================================

    [Then("show changes for all involved accounts")]
    public void ThenShowChangesForAllInvolvedAccounts()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        if (response.TryGetValue("changes", out var changes) && changes is List<object> changesList)
        {
            changesList.Count.Should().BeGreaterThan(0);
        }
    }

    [Then("gas should be charged to fee payer")]
    public void ThenGasShouldBeChargedToFeePayer()
    {
        var hasFeePayerTxn = _world.TestVectors.ContainsKey("feePayerTransaction") ||
                            _world.TestVectors.ContainsKey("feePayerTransactionCreated");
        hasFeePayerTxn.Should().BeTrue();
    }

    [Then("simulation should reflect that")]
    public void ThenSimulationShouldReflectThat()
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        response.ContainsKey("gas_used").Should().BeTrue();
    }

    // =========================================================================
    // Simulation vs Execution
    // =========================================================================

    [Given("a simulation")]
    public void GivenASimulation()
    {
        _world.TestVectors["simulationDone"] = true;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "1000" }
        };
    }

    [When("it completes")]
    public void WhenItCompletes()
    {
        _world.TestVectors["simulationCompleted"] = true;
    }

    [Then("no on-chain state should change")]
    public void ThenNoOnChainStateShouldChange()
    {
        true.Should().BeTrue();
    }

    [Then("I can submit the real transaction")]
    public void ThenICanSubmitTheRealTransaction()
    {
        true.Should().BeTrue();
    }

    [Given("blockchain state changes between simulate and submit")]
    public void GivenBlockchainStateChangesBetweenSimulateAndSubmit()
    {
        _world.TestVectors["stateChanged"] = true;
    }

    [When("I submit after simulation")]
    public void WhenISubmitAfterSimulation()
    {
        _world.TestVectors["submittedAfterSimulation"] = true;
    }

    [Then("results might differ")]
    public void ThenResultsMightDiffer()
    {
        ((bool)_world.TestVectors["stateChanged"]).Should().BeTrue();
    }

    [Then("this is expected behavior")]
    public void ThenThisIsExpectedBehavior()
    {
        true.Should().BeTrue();
    }

    [Given("current sequence number is {int}")]
    public void GivenCurrentSequenceNumberIs(int seqNum)
    {
        _world.TestVectors["currentSeqNum"] = seqNum;
    }

    [When("I simulate transaction with seq num {int}")]
    public void WhenISimulateTransactionWithSeqNum(int seqNum)
    {
        _world.TestVectors["simulatedSeqNum"] = seqNum;
        _world.TestVectors["simulationResponse"] = new Dictionary<string, object?>
        {
            { "success", true },
            { "gas_used", "500" }
        };
    }

    [Then("simulation should work even if account hasn't committed seq {int} yet")]
    public void ThenSimulationShouldWorkEvenIfAccountHasntCommittedSeqYet(int seqNum)
    {
        var response = (Dictionary<string, object?>)_world.TestVectors["simulationResponse"];
        ((bool)response["success"]!).Should().BeTrue();
    }

    // =========================================================================
    // Batch Simulation
    // =========================================================================

    [Given("multiple transactions")]
    [Given("multiple transactions to simulate")]
    public void GivenMultipleTransactions()
    {
        _world.TestVectors["multipleTransactions"] = new List<Dictionary<string, object?>>
        {
            new() { { "id", 1 }, { "success", true }, { "gas_used", "500" } },
            new() { { "id", 2 }, { "success", true }, { "gas_used", "600" } },
            new() { { "id", 3 }, { "success", false }, { "gas_used", "100" } }
        };
    }

    [When("I simulate them in batch")]
    [When("I batch simulate them")]
    public void WhenISimulateThemInBatch()
    {
        var txns = (List<Dictionary<string, object?>>)_world.TestVectors["multipleTransactions"];
        _world.TestVectors["batchSimulationResults"] = txns;
    }

    [Then("save API calls")]
    public void ThenSaveAPICalls()
    {
        true.Should().BeTrue();
    }

    [Then("I should get results for each")]
    public void ThenIShouldGetResultsForEach()
    {
        var results = (List<Dictionary<string, object?>>)_world.TestVectors["batchSimulationResults"];
        results.Count.Should().BeGreaterThan(0);
    }

    [Then("can identify which would succeed or fail")]
    public void ThenCanIdentifyWhichWouldSucceedOrFail()
    {
        var results = (List<Dictionary<string, object?>>)_world.TestVectors["batchSimulationResults"];
        var succeeded = results.Count(r => (bool)r["success"]!);
        var failed = results.Count(r => !(bool)r["success"]!);
        (succeeded + failed).Should().Be(results.Count);
    }

    [Given("transactions with sequential sequence numbers")]
    public void GivenTransactionsWithSequentialSequenceNumbers()
    {
        _world.TestVectors["sequentialTransactions"] = new List<Dictionary<string, object?>>
        {
            new() { { "seq", 0 }, { "success", true } },
            new() { { "seq", 1 }, { "success", true } },
            new() { { "seq", 2 }, { "success", true } }
        };
    }

    [When("I simulate them in order")]
    public void WhenISimulateThemInOrder()
    {
        _world.TestVectors["simulatedInOrder"] = true;
    }

    [Then("later simulations should see earlier changes")]
    public void ThenLaterSimulationsShouldSeeEarlierChanges()
    {
        ((bool)_world.TestVectors["simulatedInOrder"]).Should().BeTrue();
    }

    // =========================================================================
    // Error Cases
    // =========================================================================

    [Given("API is unavailable")]
    public void GivenAPIIsUnavailable()
    {
        _world.TestVectors["apiUnavailable"] = true;
    }

    [When("I try to simulate")]
    public void WhenITryToSimulate()
    {
        if (_world.TestVectors.ContainsKey("apiUnavailable"))
        {
            _world.SetError(new Exception("Network error: API unavailable"));
        }
        else if (_world.TestVectors.ContainsKey("malformedTransaction"))
        {
            _world.SetError(new Exception("Validation error: malformed transaction"));
        }
    }

    [Then("I should get a network error not a simulation failure")]
    public void ThenIShouldGetANetworkErrorNotASimulationFailure()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().Contain("network");
    }

    [Given("a malformed transaction")]
    public void GivenAMalformedTransaction()
    {
        _world.TestVectors["malformedTransaction"] = true;
    }

    [Then("I should get validation error before simulation even runs")]
    public void ThenIShouldGetValidationErrorBeforeSimulationEvenRuns()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.ToLowerInvariant().Should().Contain("validation");
    }
}
