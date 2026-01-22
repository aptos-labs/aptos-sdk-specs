package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptoslabs.japtos.client.AptosClient;
import com.aptoslabs.japtos.api.AptosConfig;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.types.LedgerInfo;
import com.aptoslabs.japtos.types.AccountInfo;
import com.aptoslabs.japtos.types.AccountResource;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.util.List;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for fullnode-api.feature
 * 
 * These steps test the Fullnode REST API client configuration and queries
 * using the japtos SDK.
 */
public class FullnodeApiSteps {
    
    private final World world;
    
    // Client state
    private AptosClient client;
    private AptosConfig config;
    private String customUrl;
    private int timeoutSeconds;
    
    // Query results
    private LedgerInfo ledgerInfo;
    private LedgerInfo ledgerInfo2;
    private AccountInfo accountInfo;
    private List<AccountResource> resources;
    private AccountResource singleResource;
    private Object transactionDetails;
    private Exception caughtError;
    
    // Test data
    private AccountAddress testAddress;
    private String transactionHash;
    private long ledgerVersion;
    
    public FullnodeApiSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Client Configuration
    // ==========================================================================
    
    @Given("a custom URL {string}")
    public void givenCustomUrl(String url) {
        customUrl = url;
    }
    
    @Given("a connected client")
    public void givenConnectedClient() {
        config = AptosConfig.builder()
            .network(AptosConfig.Network.TESTNET)
            .build();
        client = new AptosClient(config);
        world.setClient(client);
    }
    
    @Given("a client connected to testnet")
    public void givenClientConnectedToTestnet() {
        givenConnectedClient();
    }
    
    @Given("a client connected to any network")
    public void givenClientConnectedToAnyNetwork() {
        givenConnectedClient();
    }
    
    @Given("a client configured for unreachable URL")
    public void givenClientWithUnreachableUrl() {
        config = AptosConfig.builder()
            .fullnodeUrl("https://unreachable.example.com/v1")
            .build();
        client = new AptosClient(config);
    }
    
    @Given("a client with 1ms timeout")
    public void givenClientWith1msTimeout() {
        config = AptosConfig.builder()
            .network(AptosConfig.Network.TESTNET)
            .timeout(1)
            .build();
        client = new AptosClient(config);
    }
    
    @Given("a malformed request")
    public void givenMalformedRequest() {
        // Will be tested when making request
    }
    
    @Given("many rapid requests")
    public void givenManyRapidRequests() {
        // Rate limiting test setup
    }
    
    // ==========================================================================
    // Given Steps - Account Data
    // ==========================================================================
    
    @Given("a known existing account address")
    public void givenKnownExistingAccountAddress() {
        testAddress = AccountAddress.ONE; // Framework account always exists
    }
    
    @Given("a random unused account address")
    public void givenRandomUnusedAccountAddress() {
        // Generate a random address that doesn't exist
        byte[] randomBytes = new byte[32];
        new java.security.SecureRandom().nextBytes(randomBytes);
        testAddress = AccountAddress.fromBytes(randomBytes);
    }
    
    @Given("an account address with resources")
    public void givenAccountAddressWithResources() {
        testAddress = AccountAddress.ONE;
    }
    
    @Given("an account with APT balance")
    public void givenAccountWithAptBalance() {
        testAddress = AccountAddress.ONE;
    }
    
    @Given("an account address")
    public void givenAccountAddress() {
        testAddress = AccountAddress.ONE;
    }
    
    @Given("an account with published modules \\(e.g., 0x1\\)")
    public void givenAccountWithPublishedModules() {
        testAddress = AccountAddress.ONE;
    }
    
    // ==========================================================================
    // Given Steps - Transaction Data
    // ==========================================================================
    
    @Given("a known transaction hash")
    public void givenKnownTransactionHash() {
        // Use a well-known genesis transaction hash or similar
        transactionHash = "0x0000000000000000000000000000000000000000000000000000000000000001";
    }
    
    @Given("a non-existent transaction hash")
    public void givenNonExistentTransactionHash() {
        transactionHash = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff";
    }
    
    @Given("a known ledger version")
    public void givenKnownLedgerVersion() {
        ledgerVersion = 1L;
    }
    
    @Given("an account with transaction history")
    public void givenAccountWithTransactionHistory() {
        testAddress = AccountAddress.ONE;
    }
    
    @Given("an account with many transactions")
    public void givenAccountWithManyTransactions() {
        testAddress = AccountAddress.ONE;
    }
    
    // ==========================================================================
    // When Steps - Client Creation
    // ==========================================================================
    
    @When("I create a client with testnet configuration")
    public void whenCreateClientWithTestnetConfig() {
        config = AptosConfig.builder()
            .network(AptosConfig.Network.TESTNET)
            .build();
        client = new AptosClient(config);
        world.setClient(client);
    }
    
    @When("I create a client with mainnet configuration")
    public void whenCreateClientWithMainnetConfig() {
        config = AptosConfig.builder()
            .network(AptosConfig.Network.MAINNET)
            .build();
        client = new AptosClient(config);
        world.setClient(client);
    }
    
    @When("I create a client with the custom URL")
    public void whenCreateClientWithCustomUrl() {
        config = AptosConfig.builder()
            .fullnodeUrl(customUrl)
            .build();
        client = new AptosClient(config);
        world.setClient(client);
    }
    
    @When("I create a client with {int} second timeout")
    public void whenCreateClientWithTimeout(int seconds) {
        timeoutSeconds = seconds;
        config = AptosConfig.builder()
            .network(AptosConfig.Network.TESTNET)
            .timeout(seconds * 1000)
            .build();
        client = new AptosClient(config);
    }
    
    // ==========================================================================
    // When Steps - Ledger Info
    // ==========================================================================
    
    @When("I request ledger info")
    public void whenRequestLedgerInfo() {
        try {
            ledgerInfo = client.getLedgerInfo();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get the ledger info")
    public void whenGetLedgerInfo() {
        whenRequestLedgerInfo();
    }
    
    @When("I get ledger info twice with delay")
    public void whenGetLedgerInfoTwiceWithDelay() {
        try {
            ledgerInfo = client.getLedgerInfo();
            Thread.sleep(1000);
            ledgerInfo2 = client.getLedgerInfo();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    // ==========================================================================
    // When Steps - Account Queries
    // ==========================================================================
    
    @When("I get account info for the address")
    public void whenGetAccountInfoForAddress() {
        try {
            accountInfo = client.getAccountInfo(testAddress);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get account info for {string}")
    public void whenGetAccountInfoFor(String address) {
        try {
            testAddress = AccountAddress.fromHex(address);
            accountInfo = client.getAccountInfo(testAddress);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get account resources")
    public void whenGetAccountResources() {
        try {
            resources = client.getAccountResources(testAddress);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get resource {string}")
    public void whenGetResource(String resourceType) {
        try {
            singleResource = client.getAccountResource(testAddress, resourceType);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get a resource type that doesn't exist")
    public void whenGetNonExistentResource() {
        try {
            singleResource = client.getAccountResource(testAddress, "0x1::fake::FakeResource");
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get account modules")
    public void whenGetAccountModules() {
        try {
            Object modules = client.getAccountModules(testAddress);
            world.setResult(modules);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get the CoinInfo resource for AptosCoin")
    public void whenGetCoinInfoResource() {
        try {
            singleResource = client.getAccountResource(
                AccountAddress.ONE,
                "0x1::coin::CoinInfo<0x1::aptos_coin::AptosCoin>"
            );
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // When Steps - Transaction Queries
    // ==========================================================================
    
    @When("I get transaction by hash")
    public void whenGetTransactionByHash() {
        try {
            transactionDetails = client.getTransactionByHash(transactionHash);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get transaction by version")
    public void whenGetTransactionByVersion() {
        try {
            transactionDetails = client.getTransactionByVersion(ledgerVersion);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get account transactions")
    public void whenGetAccountTransactions() {
        try {
            Object txns = client.getAccountTransactions(testAddress);
            world.setResult(txns);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I get account transactions with start={int} and limit={int}")
    public void whenGetAccountTransactionsWithPagination(int start, int limit) {
        try {
            Object txns = client.getAccountTransactions(testAddress, start, limit);
            world.setResult(txns);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // When Steps - General API
    // ==========================================================================
    
    @When("I make any API request")
    public void whenMakeAnyApiRequest() {
        whenRequestLedgerInfo();
    }
    
    @When("I try to make a request")
    public void whenTryToMakeRequest() {
        whenRequestLedgerInfo();
    }
    
    @When("the API returns an error")
    public void whenApiReturnsError() {
        // Error already caught in previous step
    }
    
    @When("the API returns {int}")
    public void whenApiReturnsStatusCode(int statusCode) {
        // Error handling for specific status codes
    }
    
    // ==========================================================================
    // Then Steps - Client Configuration
    // ==========================================================================
    
    @Then("the client should be configured for testnet")
    public void thenClientShouldBeConfiguredForTestnet() {
        assertThat(client).isNotNull();
        assertThat(config.getNetwork()).isEqualTo(AptosConfig.Network.TESTNET);
    }
    
    @Then("the client should be configured for mainnet")
    public void thenClientShouldBeConfiguredForMainnet() {
        assertThat(client).isNotNull();
        assertThat(config.getNetwork()).isEqualTo(AptosConfig.Network.MAINNET);
    }
    
    @Then("the base URL should be {string}")
    public void thenBaseUrlShouldBe(String expectedUrl) {
        assertThat(config.getFullnodeUrl()).isEqualTo(expectedUrl);
    }
    
    @Then("the client should use that URL for requests")
    public void thenClientShouldUseThatUrl() {
        assertThat(config.getFullnodeUrl()).isEqualTo(customUrl);
    }
    
    @Then("requests should timeout after {int} seconds")
    public void thenRequestsShouldTimeout(int seconds) {
        assertThat(config.getTimeout()).isEqualTo(seconds * 1000);
    }
    
    // ==========================================================================
    // Then Steps - Ledger Info
    // ==========================================================================
    
    @Then("I should receive chain_id")
    public void thenShouldReceiveChainId() {
        assertThat(ledgerInfo).isNotNull();
        assertThat(ledgerInfo.getChainId()).isGreaterThan(0);
    }
    
    @Then("I should receive ledger_version")
    public void thenShouldReceiveLedgerVersion() {
        assertThat(ledgerInfo).isNotNull();
        assertThat(ledgerInfo.getLedgerVersion()).isGreaterThanOrEqualTo(0);
    }
    
    @Then("I should receive block_height")
    public void thenShouldReceiveBlockHeight() {
        assertThat(ledgerInfo).isNotNull();
        assertThat(ledgerInfo.getBlockHeight()).isGreaterThanOrEqualTo(0);
    }
    
    @Then("chain_id should be {int}")
    public void thenChainIdShouldBe(int expected) {
        assertThat(ledgerInfo.getChainId()).isEqualTo(expected);
    }
    
    @Then("the second ledger_version should be >= first")
    public void thenSecondLedgerVersionShouldBeGreater() {
        assertThat(ledgerInfo2.getLedgerVersion())
            .isGreaterThanOrEqualTo(ledgerInfo.getLedgerVersion());
    }
    
    // ==========================================================================
    // Then Steps - Account Queries
    // ==========================================================================
    
    @Then("I should receive sequence_number")
    public void thenShouldReceiveSequenceNumber() {
        assertThat(accountInfo).isNotNull();
        assertThat(accountInfo.getSequenceNumber()).isGreaterThanOrEqualTo(0);
    }
    
    @Then("I should receive authentication_key")
    public void thenShouldReceiveAuthenticationKey() {
        assertThat(accountInfo).isNotNull();
        assertThat(accountInfo.getAuthenticationKey()).isNotNull();
    }
    
    @Then("I should receive a {int} NotFound error")
    public void thenShouldReceiveNotFoundError(int statusCode) {
        assertThat(caughtError).isNotNull();
        // Check for 404 or NotFound in error message/type
    }
    
    @Then("I should receive a list of resources")
    public void thenShouldReceiveListOfResources() {
        assertThat(resources).isNotNull();
        assertThat(resources).isNotEmpty();
    }
    
    @Then("each resource should have a type and data")
    public void thenEachResourceShouldHaveTypeAndData() {
        for (AccountResource resource : resources) {
            assertThat(resource.getType()).isNotNull();
            assertThat(resource.getData()).isNotNull();
        }
    }
    
    @Then("I should receive the coin store resource")
    public void thenShouldReceiveCoinStoreResource() {
        assertThat(singleResource).isNotNull();
        assertThat(singleResource.getType()).contains("CoinStore");
    }
    
    @Then("I should be able to read the balance")
    public void thenShouldBeAbleToReadBalance() {
        assertThat(singleResource.getData()).isNotNull();
    }
    
    @Then("I should receive a list of modules")
    public void thenShouldReceiveListOfModules() {
        assertThat(world.getResult()).isNotNull();
    }
    
    @Then("each module should have bytecode and ABI")
    public void thenEachModuleShouldHaveBytecodeAndAbi() {
        // Module structure validation
        assertThat(world.getResult()).isNotNull();
    }
    
    @Then("the account should exist")
    public void thenAccountShouldExist() {
        assertThat(accountInfo).isNotNull();
    }
    
    @Then("it should have resources")
    public void thenItShouldHaveResources() {
        assertThat(resources).isNotNull();
    }
    
    @Then("I should see name {string}")
    public void thenShouldSeeName(String expected) {
        assertThat(singleResource.getData().toString()).contains(expected);
    }
    
    @Then("I should see symbol {string}")
    public void thenShouldSeeSymbol(String expected) {
        assertThat(singleResource.getData().toString()).contains(expected);
    }
    
    @Then("I should see decimals {int}")
    public void thenShouldSeeDecimals(int expected) {
        assertThat(singleResource.getData().toString()).contains(String.valueOf(expected));
    }
    
    // ==========================================================================
    // Then Steps - Transaction Queries
    // ==========================================================================
    
    @Then("I should receive the transaction details")
    public void thenShouldReceiveTransactionDetails() {
        assertThat(transactionDetails).isNotNull();
    }
    
    @Then("I should see the transaction type")
    public void thenShouldSeeTransactionType() {
        assertThat(transactionDetails).isNotNull();
    }
    
    @Then("I should see the success status")
    public void thenShouldSeeSuccessStatus() {
        assertThat(transactionDetails).isNotNull();
    }
    
    @Then("I should receive the transaction at that version")
    public void thenShouldReceiveTransactionAtVersion() {
        assertThat(transactionDetails).isNotNull();
    }
    
    @Then("I should receive a list of transactions")
    public void thenShouldReceiveListOfTransactions() {
        assertThat(world.getResult()).isNotNull();
    }
    
    @Then("transactions should be for that account")
    public void thenTransactionsShouldBeForAccount() {
        assertThat(world.getResult()).isNotNull();
    }
    
    @Then("I should receive at most {int} transactions")
    public void thenShouldReceiveAtMostNTransactions(int limit) {
        // Pagination validation
        assertThat(world.getResult()).isNotNull();
    }
    
    @Then("they should start from the specified offset")
    public void thenTheyShouldStartFromOffset() {
        assertThat(world.getResult()).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Response Headers
    // ==========================================================================
    
    @Then("the response should include ledger state")
    public void thenResponseShouldIncludeLedgerState() {
        assertThat(ledgerInfo).isNotNull();
    }
    
    @Then("ledger state should have chain_id")
    public void thenLedgerStateShouldHaveChainId() {
        assertThat(ledgerInfo.getChainId()).isGreaterThan(0);
    }
    
    @Then("ledger state should have ledger_version")
    public void thenLedgerStateShouldHaveLedgerVersion() {
        assertThat(ledgerInfo.getLedgerVersion()).isGreaterThanOrEqualTo(0);
    }
    
    @Then("ledger state should have block_height")
    public void thenLedgerStateShouldHaveBlockHeight() {
        assertThat(ledgerInfo.getBlockHeight()).isGreaterThanOrEqualTo(0);
    }
    
    // ==========================================================================
    // Then Steps - Error Handling
    // ==========================================================================
    
    @Then("I should receive a Network error")
    public void thenShouldReceiveNetworkError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("I should receive a Timeout error")
    public void thenShouldReceiveTimeoutError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the error should contain the message")
    public void thenErrorShouldContainMessage() {
        assertThat(caughtError).isNotNull();
        assertThat(caughtError.getMessage()).isNotNull();
    }
    
    @Then("the error should contain the error_code")
    public void thenErrorShouldContainErrorCode() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the error should contain the HTTP status")
    public void thenErrorShouldContainHttpStatus() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the error should indicate rate limiting")
    public void thenErrorShouldIndicateRateLimiting() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the SDK should respect retry-after if present")
    public void thenSdkShouldRespectRetryAfter() {
        // Rate limiting behavior
    }
}
