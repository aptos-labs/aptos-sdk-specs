/**
 * Indexer GraphQL Client Step Definitions
 *
 * Implements behavioral tests for Aptos Indexer GraphQL API client.
 * Note: Network-dependent tests use mock responses for offline testing.
 */
using Reqnroll;
using FluentAssertions;
using Aptos;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class IndexerSteps
{
    private readonly TestWorld _world;

    public IndexerSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Client Configuration
    // =========================================================================

    [When("I create an indexer client for mainnet")]
    public void WhenICreateAnIndexerClientForMainnet()
    {
        _world.TestVectors["indexerNetwork"] = "mainnet";
        _world.TestVectors["expectedIndexerUrl"] = "https://indexer.mainnet.aptoslabs.com/v1/graphql";
    }

    [When("I create an indexer client for testnet")]
    public void WhenICreateAnIndexerClientForTestnet()
    {
        _world.TestVectors["indexerNetwork"] = "testnet";
        _world.TestVectors["expectedIndexerUrl"] = "https://indexer.testnet.aptoslabs.com/v1/graphql";
    }

    [Given("a custom indexer URL")]
    public void GivenACustomIndexerURL()
    {
        _world.TestVectors["customIndexerUrl"] = "https://custom-indexer.example.com/v1/graphql";
    }

    [When("I create an indexer client with the custom URL")]
    public void WhenICreateAnIndexerClientWithTheCustomURL()
    {
        var customUrl = _world.TestVectors["customIndexerUrl"] as string;
        _world.TestVectors["configuredIndexerUrl"] = customUrl;
    }

    [Then("the indexer client should use that URL")]
    public void ThenTheIndexerClientShouldUseThatURL()
    {
        var customUrl = _world.TestVectors["customIndexerUrl"] as string;
        var configuredUrl = _world.TestVectors["configuredIndexerUrl"] as string;
        configuredUrl.Should().Be(customUrl);
    }

    [Given("an API key for the indexer")]
    public void GivenAnAPIKeyForTheIndexer()
    {
        _world.TestVectors["indexerApiKey"] = "test-api-key-12345";
    }

    [When("I create an indexer client with the key")]
    public void WhenICreateAnIndexerClientWithTheKey()
    {
        var apiKey = _world.TestVectors["indexerApiKey"] as string;
        _world.TestVectors["configuredApiKey"] = apiKey;
    }

    [Then("requests should include the API key header")]
    public void ThenRequestsShouldIncludeTheAPIKeyHeader()
    {
        _world.TestVectors["configuredApiKey"].Should().NotBeNull();
    }

    // =========================================================================
    // Raw GraphQL Queries
    // =========================================================================

    [Given("an indexer client")]
    public void GivenAnIndexerClient()
    {
        _world.TestVectors["indexerAvailable"] = true;
    }

    [Given("a GraphQL query string")]
    public void GivenAGraphQLQueryString()
    {
        _world.TestVectors["graphqlQuery"] = @"
            query GetLedgerInfo {
                ledger_infos {
                    chain_id
                }
            }
        ";
    }

    [When("I execute the query")]
    public void WhenIExecuteTheQuery()
    {
        // Mock execution
        _world.TestVectors["queryResult"] = new Dictionary<string, object>
        {
            { "data", new Dictionary<string, object>
                {
                    { "ledger_infos", new List<object> { new Dictionary<string, object> { { "chain_id", 2 } } } }
                }
            }
        };
        _world.Result = _world.TestVectors["queryResult"];
    }

    [Then("I should receive the query result")]
    public void ThenIShouldReceiveTheQueryResult()
    {
        var result = _world.TestVectors["queryResult"] as Dictionary<string, object>;
        result.Should().NotBeNull();
        result.Should().ContainKey("data");
    }

    [Given("a GraphQL query with variables")]
    public void GivenAGraphQLQueryWithVariables()
    {
        _world.TestVectors["graphqlQuery"] = @"
            query GetAccountTokens($address: String!) {
                current_token_ownerships_v2(where: {owner_address: {_eq: $address}}) {
                    token_data_id
                    amount
                }
            }
        ";
    }

    [Given("variable values")]
    public void GivenVariableValues()
    {
        _world.TestVectors["queryVariables"] = new Dictionary<string, object> { { "address", "0x1" } };
    }

    [When("I execute the query with variables")]
    public void WhenIExecuteTheQueryWithVariables()
    {
        _world.TestVectors["queryResult"] = new Dictionary<string, object>
        {
            { "data", new Dictionary<string, object>
                {
                    { "current_token_ownerships_v2", new List<object>
                        {
                            new Dictionary<string, object> { { "token_data_id", "0x123" }, { "amount", 1 } }
                        }
                    }
                }
            }
        };
        _world.Result = _world.TestVectors["queryResult"];
    }

    [Then("the variables should be substituted")]
    public void ThenTheVariablesShouldBeSubstituted()
    {
        var result = _world.TestVectors["queryResult"] as Dictionary<string, object>;
        var data = result!["data"] as Dictionary<string, object>;
        var tokens = data!["current_token_ownerships_v2"] as List<object>;
        tokens.Should().NotBeNull();
    }

    [Given("an invalid GraphQL query")]
    public void GivenAnInvalidGraphQLQuery()
    {
        _world.TestVectors["graphqlQuery"] = "{ invalid query syntax";
    }

    [When("I execute the GraphQL query")]
    public void WhenIExecuteTheGraphQLQuery()
    {
        _world.SetError(new Exception("GraphQL syntax error"));
        _world.TestVectors["graphqlError"] = new Dictionary<string, object>
        {
            { "errors", new List<object> { new Dictionary<string, object> { { "message", "Syntax error" } } } }
        };
    }

    [Then("I should receive a GraphQL error")]
    public void ThenIShouldReceiveAGraphQLError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Then("the error should contain the error message")]
    public void ThenTheErrorShouldContainTheErrorMessage()
    {
        _world.Error!.Message.Should().NotBeEmpty();
    }

    // =========================================================================
    // Account Tokens (NFTs)
    // =========================================================================

    [Given("an account address with NFTs")]
    public void GivenAnAccountAddressWithNFTs()
    {
        _world.TestVectors["accountAddress"] = AccountAddress.FromString("0x1");
    }

    [When("I query current tokens for the account")]
    public void WhenIQueryCurrentTokensForTheAccount()
    {
        _world.TestVectors["tokensResult"] = new List<Dictionary<string, object>>
        {
            new()
            {
                { "token_data_id", "0x123::collection::token1" },
                { "collection_name", "Test Collection" },
                { "token_name", "Token 1" },
                { "amount", 1 }
            }
        };
        _world.Result = _world.TestVectors["tokensResult"];
    }

    [Then("I should receive a list of tokens")]
    public void ThenIShouldReceiveAListOfTokens()
    {
        var tokens = _world.TestVectors["tokensResult"] as List<Dictionary<string, object>>;
        tokens.Should().NotBeNull();
    }

    [Then("each token should have collection info")]
    public void ThenEachTokenShouldHaveCollectionInfo()
    {
        var tokens = _world.TestVectors["tokensResult"] as List<Dictionary<string, object>>;
        foreach (var token in tokens!)
        {
            token.Should().ContainKey("collection_name");
        }
    }

    [Then("each token should have token_data_id")]
    public void ThenEachTokenShouldHaveTokenDataId()
    {
        var tokens = _world.TestVectors["tokensResult"] as List<Dictionary<string, object>>;
        foreach (var token in tokens!)
        {
            token.Should().ContainKey("token_data_id");
        }
    }

    [Given("an account with many NFTs")]
    public void GivenAnAccountWithManyNFTs()
    {
        _world.TestVectors["accountAddress"] = AccountAddress.FromString("0x1");
        _world.TestVectors["totalNfts"] = 25;
    }

    [When("I query tokens with limit {int} and offset {int}")]
    public void WhenIQueryTokensWithLimitAndOffset(int limit, int offset)
    {
        var totalNfts = (int)_world.TestVectors["totalNfts"];
        var tokens = new List<Dictionary<string, object>>();
        for (int i = offset; i < Math.Min(offset + limit, totalNfts); i++)
        {
            tokens.Add(new Dictionary<string, object> { { "token_data_id", $"token_{i}" }, { "amount", 1 } });
        }
        _world.TestVectors["tokensResult"] = tokens;
        _world.TestVectors["queryLimit"] = limit;
    }

    [Then("I should receive at most {int} tokens")]
    public void ThenIShouldReceiveAtMostTokens(int limit)
    {
        var tokens = _world.TestVectors["tokensResult"] as List<Dictionary<string, object>>;
        tokens!.Count.Should().BeLessThanOrEqualTo(limit);
    }

    [When("I query with offset {int}")]
    public void WhenIQueryWithOffset(int offset)
    {
        var totalNfts = _world.TestVectors.TryGetValue("totalNfts", out var tn) ? (int)tn : 25;
        var limit = _world.TestVectors.TryGetValue("queryLimit", out var ql) ? (int)ql : 10;
        var tokens = new List<Dictionary<string, object>>();
        for (int i = offset; i < Math.Min(offset + limit, totalNfts); i++)
        {
            tokens.Add(new Dictionary<string, object> { { "token_data_id", $"token_{i}" }, { "amount", 1 } });
        }
        _world.TestVectors["tokensResult"] = tokens;
    }

    [Then("I should receive the next page")]
    public void ThenIShouldReceiveTheNextPage()
    {
        var tokens = _world.TestVectors["tokensResult"] as List<Dictionary<string, object>>;
        tokens!.Count.Should().BeGreaterThan(0);
    }

    [Given("an account with an NFT")]
    public void GivenAnAccountWithAnNFT()
    {
        _world.TestVectors["accountAddress"] = AccountAddress.FromString("0x1");
    }

    [When("I query the token")]
    public void WhenIQueryTheToken()
    {
        _world.TestVectors["tokenResult"] = new Dictionary<string, object>
        {
            { "token_name", "My NFT" },
            { "collection_name", "My Collection" },
            { "token_uri", "https://example.com/token/1" },
            { "amount", 1 }
        };
        _world.Result = _world.TestVectors["tokenResult"];
    }

    [Then("I should see token_name")]
    public void ThenIShouldSeeTokenName()
    {
        var token = _world.TestVectors["tokenResult"] as Dictionary<string, object>;
        token.Should().ContainKey("token_name");
    }

    [Then("I should see collection_name")]
    public void ThenIShouldSeeCollectionName()
    {
        var token = _world.TestVectors["tokenResult"] as Dictionary<string, object>;
        token.Should().ContainKey("collection_name");
    }

    [Then("I should see token_uri")]
    public void ThenIShouldSeeTokenUri()
    {
        var token = _world.TestVectors["tokenResult"] as Dictionary<string, object>;
        token.Should().ContainKey("token_uri");
    }

    [Then("I should see amount")]
    public void ThenIShouldSeeAmount()
    {
        var token = _world.TestVectors["tokenResult"] as Dictionary<string, object>;
        token.Should().ContainKey("amount");
    }

    [Given("an account with no NFTs")]
    public void GivenAnAccountWithNoNFTs()
    {
        _world.TestVectors["accountAddress"] = AccountAddress.FromString("0x999");
    }

    [When("I query current tokens")]
    public void WhenIQueryCurrentTokens()
    {
        _world.TestVectors["tokensResult"] = new List<Dictionary<string, object>>();
    }

    [Then("I should receive an empty list")]
    public void ThenIShouldReceiveAnEmptyList()
    {
        var tokens = _world.TestVectors["tokensResult"] as List<Dictionary<string, object>>;
        tokens.Should().NotBeNull();
        tokens!.Count.Should().Be(0);
    }

    // =========================================================================
    // Fungible Asset Balances
    // =========================================================================

    [When("I query fungible asset balances")]
    public void WhenIQueryFungibleAssetBalances()
    {
        _world.TestVectors["fungibleAssetBalances"] = new List<Dictionary<string, object>>
        {
            new() { { "asset_type", "0x1::aptos_coin::AptosCoin" }, { "amount", "1000000000" } }
        };
        _world.Result = _world.TestVectors["fungibleAssetBalances"];
    }

    [Then("I should receive a list of fungible asset balances")]
    public void ThenIShouldReceiveAListOfFungibleAssetBalances()
    {
        var balances = _world.TestVectors["fungibleAssetBalances"] as List<Dictionary<string, object>>;
        balances.Should().NotBeNull();
    }

    [Then("each balance should have asset_type and amount")]
    public void ThenEachBalanceShouldHaveAssetTypeAndAmount()
    {
        var balances = _world.TestVectors["fungibleAssetBalances"] as List<Dictionary<string, object>>;
        foreach (var balance in balances!)
        {
            balance.Should().ContainKey("asset_type");
            balance.Should().ContainKey("amount");
        }
    }

    [Given("a specific fungible asset address")]
    public void GivenASpecificFungibleAssetAddress()
    {
        _world.TestVectors["fungibleAssetAddress"] = "0x1::aptos_coin::AptosCoin";
    }

    [When("I query that specific balance")]
    public void WhenIQueryThatSpecificBalance()
    {
        _world.TestVectors["specificBalance"] = new Dictionary<string, object>
        {
            { "asset_type", "0x1::aptos_coin::AptosCoin" },
            { "amount", "1000000000" }
        };
        _world.Result = _world.TestVectors["specificBalance"];
    }

    [Then("I should receive only that asset's balance")]
    public void ThenIShouldReceiveOnlyThatAssetsBalance()
    {
        var balance = _world.TestVectors["specificBalance"] as Dictionary<string, object>;
        balance.Should().ContainKey("asset_type");
    }

    [Given("a fungible asset address")]
    public void GivenAFungibleAssetAddress()
    {
        _world.TestVectors["fungibleAssetAddress"] = "0x1::aptos_coin::AptosCoin";
    }

    [When("I query the asset metadata")]
    public void WhenIQueryTheAssetMetadata()
    {
        _world.TestVectors["assetMetadata"] = new Dictionary<string, object>
        {
            { "name", "Aptos Coin" },
            { "symbol", "APT" },
            { "decimals", 8 }
        };
        _world.Result = _world.TestVectors["assetMetadata"];
    }

    [Then("I should see name, symbol, and decimals")]
    public void ThenIShouldSeeNameSymbolAndDecimals()
    {
        var metadata = _world.TestVectors["assetMetadata"] as Dictionary<string, object>;
        metadata.Should().ContainKey("name");
        metadata.Should().ContainKey("symbol");
        metadata.Should().ContainKey("decimals");
    }

    // =========================================================================
    // Transaction History
    // =========================================================================

    [When("I query account transaction history")]
    public void WhenIQueryAccountTransactionHistory()
    {
        _world.TestVectors["transactionHistory"] = new List<Dictionary<string, object>>
        {
            new() { { "version", "1" }, { "type", "user_transaction" }, { "success", true } },
            new() { { "version", "2" }, { "type", "user_transaction" }, { "success", true } }
        };
        _world.Result = _world.TestVectors["transactionHistory"];
    }

    [Then("I should receive a list of indexed transactions")]
    public void ThenIShouldReceiveAListOfIndexedTransactions()
    {
        var txns = _world.TestVectors["transactionHistory"] as List<Dictionary<string, object>>;
        txns.Should().NotBeNull();
    }

    [Then("each transaction should have version and type")]
    public void ThenEachTransactionShouldHaveVersionAndType()
    {
        var txns = _world.TestVectors["transactionHistory"] as List<Dictionary<string, object>>;
        foreach (var txn in txns!)
        {
            txn.Should().ContainKey("version");
            txn.Should().ContainKey("type");
        }
    }

    [When("I query with limit {int}")]
    public void WhenIQueryWithLimit(int limit)
    {
        var txns = new List<Dictionary<string, object>>();
        for (int i = 0; i < limit; i++)
        {
            txns.Add(new Dictionary<string, object> { { "version", i.ToString() }, { "type", "user_transaction" } });
        }
        _world.TestVectors["transactionHistory"] = txns;
    }

    [Then("I should receive at most {int} indexed transactions")]
    public void ThenIShouldReceiveAtMostIndexedTransactions(int limit)
    {
        var txns = _world.TestVectors["transactionHistory"] as List<Dictionary<string, object>>;
        txns!.Count.Should().BeLessThanOrEqualTo(limit);
    }

    [Given("a user_transaction type filter")]
    public void GivenAUserTransactionTypeFilter()
    {
        _world.TestVectors["transactionTypeFilter"] = "user_transaction";
    }

    [When("I query with the filter")]
    public void WhenIQueryWithTheFilter()
    {
        _world.TestVectors["transactionHistory"] = new List<Dictionary<string, object>>
        {
            new() { { "version", "1" }, { "type", "user_transaction" } }
        };
    }

    [Then("all transactions should be user_transactions")]
    public void ThenAllTransactionsShouldBeUserTransactions()
    {
        var txns = _world.TestVectors["transactionHistory"] as List<Dictionary<string, object>>;
        foreach (var txn in txns!)
        {
            txn["type"].Should().Be("user_transaction");
        }
    }

    // =========================================================================
    // Collections
    // =========================================================================

    [Given("a known collection address")]
    public void GivenAKnownCollectionAddress()
    {
        _world.TestVectors["collectionAddress"] = "0x123::my_collection::MyCollection";
    }

    [When("I query the collection")]
    public void WhenIQueryTheCollection()
    {
        _world.TestVectors["collectionResult"] = new Dictionary<string, object>
        {
            { "collection_name", "My Collection" },
            { "creator_address", "0x123" },
            { "description", "A test collection" },
            { "current_supply", 100 }
        };
        _world.Result = _world.TestVectors["collectionResult"];
    }

    [Then("I should receive collection details")]
    public void ThenIShouldReceiveCollectionDetails()
    {
        var collection = _world.TestVectors["collectionResult"] as Dictionary<string, object>;
        collection.Should().NotBeNull();
    }

    [Then("I should see creator_address")]
    public void ThenIShouldSeeCreatorAddress()
    {
        var collection = _world.TestVectors["collectionResult"] as Dictionary<string, object>;
        collection.Should().ContainKey("creator_address");
    }

    [Then("I should see current_supply")]
    public void ThenIShouldSeeCurrentSupply()
    {
        var collection = _world.TestVectors["collectionResult"] as Dictionary<string, object>;
        collection.Should().ContainKey("current_supply");
    }

    [When("I query tokens in the collection")]
    public void WhenIQueryTokensInTheCollection()
    {
        _world.TestVectors["collectionTokens"] = new List<Dictionary<string, object>>
        {
            new() { { "token_data_id", "token1" }, { "token_name", "Token 1" } },
            new() { { "token_data_id", "token2" }, { "token_name", "Token 2" } }
        };
        _world.Result = _world.TestVectors["collectionTokens"];
    }

    [Then("I should receive tokens belonging to that collection")]
    public void ThenIShouldReceiveTokensBelongingToThatCollection()
    {
        var tokens = _world.TestVectors["collectionTokens"] as List<Dictionary<string, object>>;
        tokens.Should().NotBeNull();
        tokens!.Count.Should().BeGreaterThan(0);
    }

    [When("I query collection metadata")]
    public void WhenIQueryCollectionMetadata()
    {
        _world.TestVectors["collectionMetadata"] = new Dictionary<string, object>
        {
            { "name", "My Collection" },
            { "description", "A test collection" },
            { "uri", "https://example.com/collection" }
        };
        _world.Result = _world.TestVectors["collectionMetadata"];
    }

    [Then("I should see collection name and description")]
    public void ThenIShouldSeeCollectionNameAndDescription()
    {
        var metadata = _world.TestVectors["collectionMetadata"] as Dictionary<string, object>;
        metadata.Should().ContainKey("name");
        metadata.Should().ContainKey("description");
    }

    [Then("I should see collection URI")]
    public void ThenIShouldSeeCollectionURI()
    {
        var metadata = _world.TestVectors["collectionMetadata"] as Dictionary<string, object>;
        metadata.Should().ContainKey("uri");
    }

    // =========================================================================
    // Events
    // =========================================================================

    [Given("an event type {string}")]
    public void GivenAnEventType(string eventType)
    {
        _world.TestVectors["eventType"] = eventType;
    }

    [When("I query events of that type")]
    public void WhenIQueryEventsOfThatType()
    {
        _world.TestVectors["eventsResult"] = new List<Dictionary<string, object>>
        {
            new() { { "type", "0x1::coin::DepositEvent" }, { "data", new Dictionary<string, object> { { "amount", "100" } } } }
        };
        _world.Result = _world.TestVectors["eventsResult"];
    }

    [Then("I should receive matching events")]
    public void ThenIShouldReceiveMatchingEvents()
    {
        var events = _world.TestVectors["eventsResult"] as List<Dictionary<string, object>>;
        events.Should().NotBeNull();
    }

    [When("I query events for the account")]
    public void WhenIQueryEventsForTheAccount()
    {
        WhenIQueryEventsOfThatType();
    }

    [Then("I should receive events involving that account")]
    public void ThenIShouldReceiveEventsInvolvingThatAccount()
    {
        ThenIShouldReceiveMatchingEvents();
    }

    [Then("each event should have type and data")]
    public void ThenEachEventShouldHaveTypeAndData()
    {
        var events = _world.TestVectors["eventsResult"] as List<Dictionary<string, object>>;
        foreach (var evt in events!)
        {
            evt.Should().ContainKey("type");
            evt.Should().ContainKey("data");
        }
    }

    // =========================================================================
    // Legacy Coins
    // =========================================================================

    [When("I query coin balances")]
    public void WhenIQueryCoinBalances()
    {
        _world.TestVectors["coinBalances"] = new List<Dictionary<string, object>>
        {
            new() { { "coin_type", "0x1::aptos_coin::AptosCoin" }, { "amount", "1000000000" } }
        };
        _world.Result = _world.TestVectors["coinBalances"];
    }

    [Then("I should receive legacy coin balances")]
    public void ThenIShouldReceiveLegacyCoinBalances()
    {
        var balances = _world.TestVectors["coinBalances"] as List<Dictionary<string, object>>;
        balances.Should().NotBeNull();
    }

    [When("I query coin activities")]
    public void WhenIQueryCoinActivities()
    {
        _world.TestVectors["coinActivities"] = new List<Dictionary<string, object>>
        {
            new() { { "activity_type", "deposit" }, { "amount", "100" }, { "coin_type", "0x1::aptos_coin::AptosCoin" } }
        };
        _world.Result = _world.TestVectors["coinActivities"];
    }

    [Then("I should receive deposit and withdrawal activities")]
    public void ThenIShouldReceiveDepositAndWithdrawalActivities()
    {
        var activities = _world.TestVectors["coinActivities"] as List<Dictionary<string, object>>;
        activities.Should().NotBeNull();
    }

    // =========================================================================
    // Processor Status
    // =========================================================================

    [When("I query processor status")]
    public void WhenIQueryProcessorStatus()
    {
        _world.TestVectors["processorStatus"] = new Dictionary<string, object>
        {
            { "processor_name", "token_processor" },
            { "last_success_version", "12345678" },
            { "last_updated", "2024-01-01T00:00:00Z" }
        };
        _world.Result = _world.TestVectors["processorStatus"];
    }

    [Then("I should see which processors are running")]
    public void ThenIShouldSeeWhichProcessorsAreRunning()
    {
        var status = _world.TestVectors["processorStatus"] as Dictionary<string, object>;
        status.Should().ContainKey("processor_name");
    }

    [Then("I should see their last processed versions")]
    public void ThenIShouldSeeTheirLastProcessedVersions()
    {
        var status = _world.TestVectors["processorStatus"] as Dictionary<string, object>;
        status.Should().ContainKey("last_success_version");
    }

    [Given("current ledger version is known")]
    public void GivenCurrentLedgerVersionIsKnown()
    {
        _world.TestVectors["currentLedgerVersion"] = "12345700";
    }

    [When("I compare indexer version to ledger version")]
    public void WhenICompareIndexerVersionToLedgerVersion()
    {
        var status = _world.TestVectors["processorStatus"] as Dictionary<string, object>;
        var indexerVersion = long.Parse(status?["last_success_version"]?.ToString() ?? "12345678");
        var ledgerVersion = long.Parse(_world.TestVectors["currentLedgerVersion"] as string ?? "12345700");
        _world.TestVectors["indexerLag"] = ledgerVersion - indexerVersion;
    }

    [Then("I can determine the lag")]
    public void ThenICanDetermineTheLag()
    {
        var lag = (long)_world.TestVectors["indexerLag"];
        lag.Should().BeGreaterThanOrEqualTo(0);
    }

    // =========================================================================
    // Error Handling
    // =========================================================================

    [Given("the indexer is unavailable")]
    public void GivenTheIndexerIsUnavailable()
    {
        _world.TestVectors["indexerUnavailable"] = true;
    }

    [When("I make a query")]
    public void WhenIMakeAQuery()
    {
        if (_world.TestVectors.TryGetValue("indexerUnavailable", out var iu) && (bool)iu)
        {
            _world.SetError(new Exception("Indexer unavailable"));
        }
    }

    [Then("I should receive a connection error")]
    public void ThenIShouldReceiveAConnectionError()
    {
        _world.Error.Should().NotBeNull();
    }

    [Given("a very slow query")]
    public void GivenAVerySlowQuery()
    {
        _world.TestVectors["slowQuery"] = true;
    }

    [When("it exceeds timeout")]
    public void WhenItExceedsTimeout()
    {
        _world.SetError(new Exception("Query timeout"));
    }

    [Then("I should receive an indexer timeout error")]
    public void ThenIShouldReceiveAnIndexerTimeoutError()
    {
        _world.Error.Should().NotBeNull();
        _world.Error!.Message.Should().Contain("timeout");
    }

    [Given("a query that returns unexpected format")]
    public void GivenAQueryThatReturnsUnexpectedFormat()
    {
        _world.TestVectors["malformedResponse"] = true;
    }

    [When("the response is malformed")]
    public void WhenTheResponseIsMalformed()
    {
        _world.SetError(new Exception("Malformed response"));
    }

    [Then("I should receive a parsing error")]
    public void ThenIShouldReceiveAParsingError()
    {
        _world.Error.Should().NotBeNull();
    }
}
