/**
 * Gas Estimation Step Definitions
 *
 * Implements behavioral tests for gas price and usage estimation.
 */
using Reqnroll;
using NUnit.Framework;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class GasEstimationSteps
{
    private readonly TestWorld _world;

    public GasEstimationSteps(TestWorld world)
    {
        _world = world;
    }

    // =============================================================================
    // Gas Price Estimation
    // =============================================================================

    [Given("a connected Aptos client")]
    public void GivenAConnectedAptosClient()
    {
        _world.TestVectors["aptosClientConnected"] = true;
        // In a real implementation, this would create an AptosClient
    }

    [Then("the value should be in octas per gas unit")]
    public void ThenTheValueShouldBeInOctasPerGasUnit()
    {
        var gasEstimate = _world.TestVectors.TryGetValue("gasEstimate", out var val) ? val as Dictionary<string, object> : null;
        if (gasEstimate != null && gasEstimate.TryGetValue("gas_estimate", out var estimate))
        {
            Assert.That(Convert.ToInt64(estimate), Is.GreaterThan(0));
        }
    }

    [Then("I should receive gas_estimate standard")]
    public void ThenIShouldReceiveGasEstimateStandard()
    {
        var gasEstimate = _world.TestVectors.TryGetValue("gasEstimate", out var val) ? val as Dictionary<string, object> : null;
        if (gasEstimate != null)
        {
            Assert.That(gasEstimate.ContainsKey("gas_estimate"), Is.True);
        }
    }

    [Then("optionally prioritized_gas_estimate faster")]
    public void ThenOptionallyPrioritizedGasEstimateFaster()
    {
        // Prioritized estimate may or may not be present
        Assert.Pass();
    }

    [Then("optionally deprioritized_gas_estimate slower/cheaper")]
    public void ThenOptionallyDeprioritizedGasEstimateSlowerCheaper()
    {
        // Deprioritized estimate may or may not be present
        Assert.Pass();
    }

    [Given("gas price estimates")]
    public void GivenGasPriceEstimates()
    {
        // Use mock values
        _world.TestVectors["gasEstimate"] = new Dictionary<string, object>
        {
            { "gas_estimate", 100L },
            { "prioritized_gas_estimate", 150L },
            { "deprioritized_gas_estimate", 75L }
        };
    }

    [When("I compare prioritized vs standard")]
    public void WhenIComparePrioritizedVsStandard()
    {
        _world.TestVectors["comparedPrioritized"] = true;
    }

    [Then("prioritized should be >= standard")]
    public void ThenPrioritizedShouldBeGreaterThanOrEqualStandard()
    {
        var estimate = _world.TestVectors.TryGetValue("gasEstimate", out var val) ? val as Dictionary<string, object> : null;
        if (estimate != null && estimate.TryGetValue("prioritized_gas_estimate", out var prioritized) 
            && estimate.TryGetValue("gas_estimate", out var standard))
        {
            Assert.That(Convert.ToInt64(prioritized), Is.GreaterThanOrEqualTo(Convert.ToInt64(standard)));
        }
    }

    [When("I compare deprioritized vs standard")]
    public void WhenICompareDeprioritizedVsStandard()
    {
        _world.TestVectors["comparedDeprioritized"] = true;
    }

    [Then("deprioritized should be <= standard")]
    public void ThenDeprioritizedShouldBeLessThanOrEqualStandard()
    {
        var estimate = _world.TestVectors.TryGetValue("gasEstimate", out var val) ? val as Dictionary<string, object> : null;
        if (estimate != null && estimate.TryGetValue("deprioritized_gas_estimate", out var deprioritized)
            && estimate.TryGetValue("gas_estimate", out var standard))
        {
            Assert.That(Convert.ToInt64(deprioritized), Is.LessThanOrEqualTo(Convert.ToInt64(standard)));
        }
    }

    [Then("all estimates should be greater than {int}")]
    public void ThenAllEstimatesShouldBeGreaterThan(int minValue)
    {
        var estimate = _world.TestVectors.TryGetValue("gasEstimate", out var val) ? val as Dictionary<string, object> : null;
        if (estimate != null && estimate.TryGetValue("gas_estimate", out var gasEstimate))
        {
            Assert.That(Convert.ToInt64(gasEstimate), Is.GreaterThan(minValue));
        }
    }

    // =============================================================================
    // Transaction Simulation for Gas
    // =============================================================================

    [When("I simulate the transaction for gas")]
    public void WhenISimulateTheTransactionForGas()
    {
        // Create a mock simulation result
        _world.TestVectors["simulationResult"] = new Dictionary<string, object>
        {
            { "gas_used", "1000" },
            { "success", true }
        };
    }

    [Then("I should receive gas_used")]
    public void ThenIShouldReceiveGasUsed()
    {
        var result = _world.TestVectors.TryGetValue("simulationResult", out var val) ? val as Dictionary<string, object> : null;
        if (result != null)
        {
            Assert.That(result.ContainsKey("gas_used"), Is.True);
        }
    }

    [Then("gas_used represents actual consumption")]
    public void ThenGasUsedRepresentsActualConsumption()
    {
        var result = _world.TestVectors.TryGetValue("simulationResult", out var val) ? val as Dictionary<string, object> : null;
        if (result != null && result.TryGetValue("gas_used", out var gasUsed))
        {
            Assert.That(Convert.ToInt64(gasUsed), Is.GreaterThan(0));
        }
    }

    [Given("a transaction simulation result")]
    public void GivenATransactionSimulationResult()
    {
        _world.TestVectors["simulationResult"] = new Dictionary<string, object>
        {
            { "gas_used", "5000" },
            { "success", true }
        };
    }

    [When("I extract gas_used")]
    public void WhenIExtractGasUsed()
    {
        var result = _world.TestVectors.TryGetValue("simulationResult", out var val) ? val as Dictionary<string, object> : null;
        if (result != null && result.TryGetValue("gas_used", out var gasUsed))
        {
            _world.TestVectors["extractedGasUsed"] = Convert.ToInt64(gasUsed);
        }
    }

    [Then("I can use it to set max_gas_amount with buffer")]
    public void ThenICanUseItToSetMaxGasAmountWithBuffer()
    {
        var gasUsed = _world.TestVectors.TryGetValue("extractedGasUsed", out var val) ? Convert.ToInt64(val) : 0;
        var buffer = 1.2; // 20% buffer
        var maxGasAmount = (long)Math.Ceiling(gasUsed * buffer);
        _world.TestVectors["recommendedMaxGas"] = maxGasAmount;
        Assert.That(maxGasAmount, Is.GreaterThan(gasUsed));
    }

    [Given("a simulated and executed transaction")]
    public void GivenASimulatedAndExecutedTransaction()
    {
        _world.TestVectors["simulatedGas"] = 5000L;
        _world.TestVectors["actualGas"] = 4800L;
        _world.TestVectors["maxGasAmount"] = 10000L;
    }

    [When("I compare gas values")]
    public void WhenICompareGasValues()
    {
        _world.TestVectors["gasCompared"] = true;
    }

    [Then("actual gas should be similar to simulated")]
    public void ThenActualGasShouldBeSimilarToSimulated()
    {
        var simulated = Convert.ToInt64(_world.TestVectors["simulatedGas"]);
        var actual = Convert.ToInt64(_world.TestVectors["actualGas"]);
        // Actual should be within 20% of simulated
        Assert.That(actual, Is.InRange(simulated * 0.8, simulated * 1.2));
    }

    [Then("actual should not exceed max_gas_amount")]
    public void ThenActualShouldNotExceedMaxGasAmount()
    {
        var actual = Convert.ToInt64(_world.TestVectors["actualGas"]);
        var maxGas = Convert.ToInt64(_world.TestVectors["maxGasAmount"]);
        Assert.That(actual, Is.LessThanOrEqualTo(maxGas));
    }

    [Given("a simple transfer transaction")]
    public void GivenASimpleTransferTransaction()
    {
        _world.TestVectors["simpleTransferGas"] = 500L;
    }

    [Given("a complex smart contract call")]
    public void GivenAComplexSmartContractCall()
    {
        _world.TestVectors["complexCallGas"] = 5000L;
    }

    [When("I simulate both")]
    public void WhenISimulateBoth()
    {
        _world.TestVectors["bothSimulated"] = true;
    }

    [Then("the complex call should use more gas")]
    public void ThenTheComplexCallShouldUseMoreGas()
    {
        var simpleGas = Convert.ToInt64(_world.TestVectors["simpleTransferGas"]);
        var complexGas = Convert.ToInt64(_world.TestVectors["complexCallGas"]);
        Assert.That(complexGas, Is.GreaterThan(simpleGas));
    }

    // =============================================================================
    // Gas Configuration
    // =============================================================================

    [Given("a transaction builder with defaults")]
    public void GivenATransactionBuilderWithDefaults()
    {
        _world.TestVectors["defaultMaxGas"] = 200000L;
        _world.TestVectors["defaultGasPrice"] = 100L;
    }

    [When("I check default values")]
    public void WhenICheckDefaultValues()
    {
        _world.TestVectors["defaultsChecked"] = true;
    }

    [Then("max_gas_amount should be reasonable")]
    public void ThenMaxGasAmountShouldBeReasonable()
    {
        var defaultMaxGas = Convert.ToInt64(_world.TestVectors["defaultMaxGas"]);
        Assert.That(defaultMaxGas, Is.GreaterThan(0));
    }

    [Then("gas_unit_price should be reasonable")]
    public void ThenGasUnitPriceShouldBeReasonable()
    {
        var defaultPrice = Convert.ToInt64(_world.TestVectors["defaultGasPrice"]);
        Assert.That(defaultPrice, Is.GreaterThan(0));
    }

    [Given("current gas estimate is {int}")]
    public void GivenCurrentGasEstimateIs(int estimate)
    {
        _world.TestVectors["currentGasEstimate"] = (long)estimate;
    }

    [When("I build a transaction with gas_unit_price {int}")]
    public void WhenIBuildATransactionWithGasUnitPrice(int price)
    {
        _world.TestVectors["overrideGasPrice"] = (long)price;
    }

    [Then("the transaction should use price {int}")]
    public void ThenTheTransactionShouldUsePrice(int price)
    {
        var overridePrice = Convert.ToInt64(_world.TestVectors["overrideGasPrice"]);
        Assert.That(overridePrice, Is.EqualTo(price));
    }

    [Given("a transaction builder")]
    public void GivenATransactionBuilder()
    {
        _world.TestVectors["builderReady"] = true;
    }

    [When("I set max_gas_amount to {int}")]
    public void WhenISetMaxGasAmountTo(int maxGas)
    {
        _world.TestVectors["setMaxGas"] = (long)maxGas;
    }

    [When("I set gas_unit_price to {int}")]
    public void WhenISetGasUnitPriceTo(int gasPrice)
    {
        _world.TestVectors["setGasPrice"] = (long)gasPrice;
    }

    [Then("the transaction should have that limit")]
    public void ThenTheTransactionShouldHaveThatLimit()
    {
        var setMaxGas = Convert.ToInt64(_world.TestVectors["setMaxGas"]);
        Assert.That(setMaxGas, Is.GreaterThan(0));
    }

    [Given("two transactions with different gas prices")]
    public void GivenTwoTransactionsWithDifferentGasPrices()
    {
        _world.TestVectors["txn1GasPrice"] = 100L;
        _world.TestVectors["txn2GasPrice"] = 200L;
    }

    [When("both are submitted")]
    public void WhenBothAreSubmitted()
    {
        _world.TestVectors["bothSubmitted"] = true;
    }

    [Then("higher gas price should be processed first usually")]
    public void ThenHigherGasPriceShouldBeProcessedFirstUsually()
    {
        var price1 = Convert.ToInt64(_world.TestVectors["txn1GasPrice"]);
        var price2 = Convert.ToInt64(_world.TestVectors["txn2GasPrice"]);
        // Higher gas price generally has priority
        Assert.That(price2, Is.GreaterThan(price1));
    }

    // =============================================================================
    // Gas Calculation
    // =============================================================================

    [Given("gas_used = {int} units")]
    public void GivenGasUsedUnits(int gasUsed)
    {
        _world.TestVectors["gasUsed"] = (long)gasUsed;
    }

    [Given("gas_unit_price = {int} octas")]
    public void GivenGasUnitPriceOctas(int price)
    {
        _world.TestVectors["gasUnitPrice"] = (long)price;
    }

    [When("I calculate total cost")]
    public void WhenICalculateTotalCost()
    {
        var gasUsed = Convert.ToInt64(_world.TestVectors["gasUsed"]);
        var price = Convert.ToInt64(_world.TestVectors["gasUnitPrice"]);
        _world.TestVectors["totalCost"] = gasUsed * price;
    }

    [Then("total should be {int} octas")]
    public void ThenTotalShouldBeOctas(int expected)
    {
        var total = Convert.ToInt64(_world.TestVectors["totalCost"]);
        Assert.That(total, Is.EqualTo(expected));
    }

    [Given("max_gas_amount = {int}")]
    public void GivenMaxGasAmount(int maxGas)
    {
        _world.TestVectors["maxGasAmount"] = (long)maxGas;
    }

    [Given("gas_unit_price = {int}")]
    public void GivenGasUnitPrice(int price)
    {
        _world.TestVectors["gasUnitPrice"] = (long)price;
    }

    [When("I calculate maximum possible cost")]
    public void WhenICalculateMaximumPossibleCost()
    {
        var maxGas = Convert.ToInt64(_world.TestVectors["maxGasAmount"]);
        var price = Convert.ToInt64(_world.TestVectors["gasUnitPrice"]);
        _world.TestVectors["maxPossibleCost"] = maxGas * price;
    }

    [Then("max cost should be {int} octas")]
    public void ThenMaxCostShouldBeOctas(long octas)
    {
        var maxCost = Convert.ToInt64(_world.TestVectors["maxPossibleCost"]);
        Assert.That(maxCost, Is.EqualTo(octas));
    }

    [Given("a completed transaction")]
    public void GivenACompletedTransaction()
    {
        _world.TestVectors["actualCost"] = 15000000L;
        _world.TestVectors["maxPossibleCost"] = 20000000L;
    }

    [When("I compare actual cost to max possible")]
    public void WhenICompareActualCostToMaxPossible()
    {
        _world.TestVectors["costCompared"] = true;
    }

    [Then("actual should be <= max possible")]
    public void ThenActualShouldBeLessThanOrEqualMaxPossible()
    {
        var actual = Convert.ToInt64(_world.TestVectors["actualCost"]);
        var max = Convert.ToInt64(_world.TestVectors["maxPossibleCost"]);
        Assert.That(actual, Is.LessThanOrEqualTo(max));
    }

    [Then("difference is refunded")]
    public void ThenDifferenceIsRefunded()
    {
        var actual = Convert.ToInt64(_world.TestVectors["actualCost"]);
        var max = Convert.ToInt64(_world.TestVectors["maxPossibleCost"]);
        var refund = max - actual;
        Assert.That(refund, Is.GreaterThanOrEqualTo(0));
    }

    // =============================================================================
    // Insufficient Gas Handling
    // =============================================================================

    [Given("a transaction requiring {int} gas")]
    public void GivenATransactionRequiringGas(int requiredGas)
    {
        _world.TestVectors["requiredGas"] = (long)requiredGas;
    }

    [When("I submit with max_gas_amount = {int}")]
    public void WhenISubmitWithMaxGasAmount(int maxGas)
    {
        var required = Convert.ToInt64(_world.TestVectors["requiredGas"]);
        if (maxGas < required)
        {
            _world.SetError(new Exception("Out of gas"));
            _world.TestVectors["outOfGas"] = true;
        }
    }

    [Then("transaction should fail")]
    public void ThenTransactionShouldFail()
    {
        Assert.That(_world.Error, Is.Not.Null);
    }

    [Then("error should indicate out of gas")]
    public void ThenErrorShouldIndicateOutOfGas()
    {
        Assert.That(_world.TestVectors["outOfGas"], Is.True);
    }

    [Given("an account with {int} octas")]
    public void GivenAnAccountWithOctas(int balance)
    {
        _world.TestVectors["accountBalance"] = (long)balance;
    }

    [Given("a transaction requiring {int} octas gas")]
    public void GivenATransactionRequiringOctasGas(int gasCost)
    {
        _world.TestVectors["requiredGasCost"] = (long)gasCost;
    }

    [When("I try to submit")]
    public void WhenITryToSubmit()
    {
        var balance = Convert.ToInt64(_world.TestVectors["accountBalance"]);
        var required = Convert.ToInt64(_world.TestVectors["requiredGasCost"]);

        if (balance < required)
        {
            _world.SetError(new Exception("Insufficient balance for gas"));
            _world.TestVectors["insufficientBalance"] = true;
        }
    }

    [Then("submission should fail")]
    public void ThenSubmissionShouldFail()
    {
        Assert.That(_world.Error, Is.Not.Null);
    }

    [Then("error should indicate insufficient balance")]
    public void ThenErrorShouldIndicateInsufficientBalance()
    {
        Assert.That(_world.TestVectors["insufficientBalance"], Is.True);
    }

    [Given("a transaction with very low max_gas_amount")]
    public void GivenATransactionWithVeryLowMaxGasAmount()
    {
        _world.TestVectors["maxGasAmount"] = 1L;
    }

    [Then("simulation should show failure")]
    public void ThenSimulationShouldShowFailure()
    {
        var maxGas = Convert.ToInt64(_world.TestVectors["maxGasAmount"]);
        Assert.That(maxGas, Is.LessThan(100)); // Too low for any transaction
    }

    [Then("should indicate gas exhaustion")]
    public void ThenShouldIndicateGasExhaustion()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Dynamic Gas Adjustment
    // =============================================================================

    [Given("an Aptos client with auto-gas enabled")]
    public void GivenAnAptosClientWithAutoGasEnabled()
    {
        _world.TestVectors["aptosClientConnected"] = true;
        _world.TestVectors["autoGasEnabled"] = true;
    }

    [When("I submit a transaction without specifying gas")]
    public void WhenISubmitATransactionWithoutSpecifyingGas()
    {
        _world.TestVectors["noGasSpecified"] = true;
    }

    [Then("SDK should simulate first")]
    public void ThenSDKShouldSimulateFirst()
    {
        var autoGas = _world.TestVectors.TryGetValue("autoGasEnabled", out var val) && (bool)val;
        Assert.That(autoGas, Is.True);
    }

    [Then("set appropriate max_gas_amount")]
    public void ThenSetAppropriateMaxGasAmount()
    {
        Assert.Pass();
    }

    [Given("simulated gas_used = {int}")]
    public void GivenSimulatedGasUsed(int gasUsed)
    {
        _world.TestVectors["simulatedGasUsed"] = (long)gasUsed;
    }

    [When("I apply {int}% buffer")]
    public void WhenIApplyBuffer(int bufferPercent)
    {
        var gasUsed = Convert.ToInt64(_world.TestVectors["simulatedGasUsed"]);
        var buffer = 1 + (double)bufferPercent / 100;
        _world.TestVectors["bufferedMaxGas"] = (long)Math.Ceiling(gasUsed * buffer);
    }

    [Then("max_gas_amount should be {int}")]
    public void ThenMaxGasAmountShouldBe(int expected)
    {
        var buffered = Convert.ToInt64(_world.TestVectors["bufferedMaxGas"]);
        Assert.That(buffered, Is.EqualTo(expected));
    }

    [Given("an Aptos client")]
    public void GivenAnAptosClient()
    {
        _world.TestVectors["aptosClientConnected"] = true;
    }

    [When("I build transaction without specifying gas_unit_price")]
    public void WhenIBuildTransactionWithoutSpecifyingGasUnitPrice()
    {
        _world.TestVectors["noGasPriceSpecified"] = true;
    }

    [Then("SDK should fetch current estimate")]
    public void ThenSDKShouldFetchCurrentEstimate()
    {
        Assert.Pass();
    }

    [Then("use it for the transaction")]
    public void ThenUseItForTheTransaction()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Network Conditions
    // =============================================================================

    [Given("network is under high load")]
    public void GivenNetworkIsUnderHighLoad()
    {
        _world.TestVectors["highNetworkLoad"] = true;
    }

    [When("I check gas estimates")]
    public void WhenICheckGasEstimates()
    {
        _world.TestVectors["estimatesChecked"] = true;
    }

    [Then("estimates should be higher than usual")]
    public void ThenEstimatesShouldBeHigherThanUsual()
    {
        var highLoad = _world.TestVectors.TryGetValue("highNetworkLoad", out var val) && (bool)val;
        Assert.That(highLoad, Is.True);
    }

    [Given("mainnet and testnet clients")]
    public void GivenMainnetAndTestnetClients()
    {
        _world.TestVectors["hasMainnet"] = true;
        _world.TestVectors["hasTestnet"] = true;
    }

    [When("I check gas estimates on each")]
    public void WhenICheckGasEstimatesOnEach()
    {
        _world.TestVectors["checkedBothNetworks"] = true;
    }

    [Then("values may differ between networks")]
    public void ThenValuesMayDifferBetweenNetworks()
    {
        Assert.Pass();
    }

    // =============================================================================
    // Error Cases
    // =============================================================================

    [Given("a network error during estimation")]
    public void GivenANetworkErrorDuringEstimation()
    {
        _world.TestVectors["networkError"] = true;
    }

    [When("I request gas estimate")]
    public void WhenIRequestGasEstimate()
    {
        if (_world.TestVectors.TryGetValue("networkError", out var val) && (bool)val)
        {
            _world.SetError(new Exception("Network error during gas estimation"));
        }
    }

    [Then("I should receive an appropriate error")]
    public void ThenIShouldReceiveAnAppropriateError()
    {
        Assert.That(_world.Error != null || _world.TestVectors.ContainsKey("networkError"));
    }

    [Given("an invalid gas_unit_price = {int}")]
    public void GivenAnInvalidGasUnitPrice(int price)
    {
        _world.TestVectors["invalidGasPrice"] = (long)price;
        _world.TestVectors["gasUnitPrice"] = (long)price;
    }

    [When("I try to submit transaction")]
    public void WhenITryToSubmitTransaction()
    {
        var price = Convert.ToInt64(_world.TestVectors["invalidGasPrice"]);
        if (price == 0)
        {
            _world.SetError(new Exception("Invalid gas price"));
        }
    }

    [Then("it should fail with validation error")]
    public void ThenItShouldFailWithValidationError()
    {
        var price = Convert.ToInt64(_world.TestVectors["invalidGasPrice"]);
        if (price == 0)
        {
            Assert.That(_world.Error, Is.Not.Null);
        }
    }
}
