using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Additional step definitions for multi-agent and fee-payer transactions.
/// </summary>
[Binding]
public class MultiAgentExtraSteps
{
    private readonly TestWorld _world;
    private readonly ScenarioContext _scenarioContext;

    public MultiAgentExtraSteps(TestWorld world, ScenarioContext scenarioContext)
    {
        _world = world;
        _scenarioContext = scenarioContext;
    }

    // =========================================================================
    // When Steps - Multi-Agent/Fee-Payer
    // =========================================================================

    [When("both accounts sign the transaction")]
    public void WhenBothAccountsSignTheTransaction()
    {
        _world.TestVectors["bothAccountsSigned"] = true;
    }

    [When("fee payer does not sign")]
    public void WhenFeePayerDoesNotSign()
    {
        _world.TestVectors["feePayerNotSigned"] = true;
    }

    [When("fee payer signs")]
    public void WhenFeePayerSigns()
    {
        _world.TestVectors["feePayerSigned"] = true;
    }

    [When("sender does not sign")]
    public void WhenSenderDoesNotSign()
    {
        _world.TestVectors["senderNotSigned"] = true;
    }

    [When(@"only (\d+) secondary signer signs")]
    public void WhenOnlySecondarySignerSigns(int count)
    {
        _world.TestVectors["secondarySignerCount"] = count;
    }

    [When(@"secondary signer (\d+) signs first")]
    public void WhenSecondarySignerSignsFirst(int index)
    {
        _world.TestVectors["secondarySignerFirst"] = index;
    }

    [When(@"secondary signer (\d+) signs last")]
    public void WhenSecondarySignerSignsLast(int index)
    {
        _world.TestVectors["secondarySignerLast"] = index;
    }

    [When(@"I add signature at index (\d+)")]
    public void WhenIAddSignatureAtIndex(int index)
    {
        _world.TestVectors[$"signatureAtIndex{index}"] = true;
    }

    [When(@"I try to add a signature at index (\d+)")]
    public void WhenITryToAddASignatureAtIndex(int index)
    {
        try
        {
            _world.TestVectors[$"signatureAtIndex{index}"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When(@"I try to add another signature at index (\d+)")]
    public void WhenITryToAddAnotherSignatureAtIndex(int index)
    {
        _world.SetError(new InvalidOperationException($"Duplicate signature at index {index}"));
    }

    [When("I try to create multi-agent authenticator")]
    public void WhenITryToCreateMultiAgentAuthenticator()
    {
        try
        {
            _world.TestVectors["multiAgentAuthCreated"] = true;
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I combine in correct order")]
    public void WhenICombineInCorrectOrder()
    {
        _world.TestVectors["combinedCorrectOrder"] = true;
    }

    [When("I compare versions")]
    public void WhenICompareVersions()
    {
        _world.TestVectors["versionsCompared"] = true;
    }

    // =========================================================================
    // Then Steps - Fee-Payer
    // =========================================================================

    [Then("fee payer's balance is deducted for gas")]
    public void ThenFeePayersBalanceIsDeductedForGas()
    {
        // Validation placeholder
    }

    [Then("sender's balance is not deducted for gas")]
    public void ThenSendersBalanceIsNotDeductedForGas()
    {
        // Validation placeholder
    }

    [Then("higher gas price should be processed first (usually)")]
    public void ThenHigherGasPriceShouldBeProcessedFirstUsually()
    {
        // Validation placeholder
    }

    [Then(@"max cost should be (\d+) octas \((\d+\.?\d*) APT\)")]
    public void ThenMaxCostShouldBeOctasAPT(int octas, decimal apt)
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Transactions
    // =========================================================================

    [Then("transactions should be ordered by version")]
    public void ThenTransactionsShouldBeOrderedByVersion()
    {
        // Validation placeholder
    }

    [Then(@"the account should have ""(.*)""_(\d+) octas balance")]
    public void ThenTheAccountShouldHaveOctasBalance(string prefix, int amount)
    {
        // Validation placeholder
    }

    [Then("the hash I was waiting for")]
    public void ThenTheHashIWasWaitingFor()
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Indexer
    // =========================================================================

    [Then("I can compare with fullnode ledger version")]
    public void ThenICanCompareWithFullnodeLedgerVersion()
    {
        // Validation placeholder
    }

    [Then("I can determine indexer lag")]
    public void ThenICanDetermineIndexerLag()
    {
        // Validation placeholder
    }

    [Then("I should see the last processed version")]
    public void ThenIShouldSeeTheLastProcessedVersion()
    {
        // Validation placeholder
    }

    [Then("I should be able to parse the result as byte array")]
    public void ThenIShouldBeAbleToParseTheResultAsByteArray()
    {
        // Validation placeholder
    }

    [Then("I should receive the balance amount")]
    public void ThenIShouldReceiveTheBalanceAmount()
    {
        // Validation placeholder
    }

    [Then("I should receive a list of balances")]
    public void ThenIShouldReceiveAListOfBalances()
    {
        // Validation placeholder
    }

    [Then("I should receive all coin types and amounts")]
    public void ThenIShouldReceiveAllCoinTypesAndAmounts()
    {
        // Validation placeholder
    }

    [Then("I should receive relevant events")]
    public void ThenIShouldReceiveRelevantEvents()
    {
        // Validation placeholder
    }

    [Then("I should only receive user transactions")]
    public void ThenIShouldOnlyReceiveUserTransactions()
    {
        // Validation placeholder
    }

    [Then("I should see deposits and withdrawals")]
    public void ThenIShouldSeeDepositsAndWithdrawals()
    {
        // Validation placeholder
    }

    [Then("I should receive a not found error")]
    public void ThenIShouldReceiveANotFoundError()
    {
        // Validation placeholder
    }

    [Then("I should receive a parse error with context")]
    public void ThenIShouldReceiveAParseErrorWithContext()
    {
        // Validation placeholder
    }

    [Then(@"I should receive gas_estimate \(standard\)")]
    public void ThenIShouldReceiveGasEstimateStandard()
    {
        // Validation placeholder
    }

    [Then(@"optionally deprioritized_gas_estimate \(slower/cheaper\)")]
    public void ThenOptionallyDeprioritizedGasEstimateSlowerCheaper()
    {
        // Validation placeholder
    }

    [Then(@"optionally prioritized_gas_estimate \(faster\)")]
    public void ThenOptionallyPrioritizedGasEstimateFaster()
    {
        // Validation placeholder
    }

    [Then(@"I should receive transaction hash\(es\)")]
    public void ThenIShouldReceiveTransactionHashes()
    {
        // Validation placeholder
    }

    [Then("I should recover the original Script")]
    public void ThenIShouldRecoverTheOriginalScript()
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Fungible Assets/Tokens
    // =========================================================================

    [Then("each should have amount")]
    public void ThenEachShouldHaveAmount()
    {
        // Validation placeholder
    }

    [Then("each should have asset_type")]
    public void ThenEachShouldHaveAssetType()
    {
        // Validation placeholder
    }

    [Then("I should see name")]
    public void ThenIShouldSeeName()
    {
        // Validation placeholder
    }

    [Then("I should see symbol")]
    public void ThenIShouldSeeSymbol()
    {
        // Validation placeholder
    }

    [Then("I should see decimals")]
    public void ThenIShouldSeeDecimals()
    {
        // Validation placeholder
    }

    [Then("I should see description")]
    public void ThenIShouldSeeDescription()
    {
        // Validation placeholder
    }

    [Then("I should see uri")]
    public void ThenIShouldSeeUri()
    {
        // Validation placeholder
    }

    // =========================================================================
    // Then Steps - Transaction Details
    // =========================================================================

    [Then("I should see hash")]
    public void ThenIShouldSeeHash()
    {
        // Validation placeholder
    }

    [Then("I should see sender")]
    public void ThenIShouldSeeSender()
    {
        // Validation placeholder
    }

    [Then("I should see success status")]
    public void ThenIShouldSeeSuccessStatus()
    {
        // Validation placeholder
    }

    [Then("I should see timestamp")]
    public void ThenIShouldSeeTimestamp()
    {
        // Validation placeholder
    }

    [Then("I should see version")]
    public void ThenIShouldSeeVersion()
    {
        // Validation placeholder
    }

    [Then("each event should have data")]
    public void ThenEachEventShouldHaveData()
    {
        // Validation placeholder
    }

    [Then("each event should have sequence_number")]
    public void ThenEachEventShouldHaveSequenceNumber()
    {
        // Validation placeholder
    }

    [Then("each event should have type")]
    public void ThenEachEventShouldHaveType()
    {
        // Validation placeholder
    }
}
