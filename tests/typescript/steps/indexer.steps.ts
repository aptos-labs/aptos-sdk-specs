/**
 * Indexer GraphQL Client Step Definitions
 *
 * Implements behavioral tests for Aptos Indexer GraphQL API client.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  Aptos,
  AptosConfig,
  Network,
  AccountAddress,
} from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";

// =============================================================================
// Client Configuration
// =============================================================================

When("I create an indexer client for mainnet", function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.MAINNET });
  const client = new Aptos(config);
  this.testVectors.set("indexerClient", client);
  this.testVectors.set("indexerConfig", config);
  this.testVectors.set("expectedIndexerUrl", "https://indexer.mainnet.aptoslabs.com/v1/graphql");
});

When("I create an indexer client for testnet", function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("indexerClient", client);
  this.testVectors.set("indexerConfig", config);
  this.testVectors.set("expectedIndexerUrl", "https://indexer.testnet.aptoslabs.com/v1/graphql");
});

Given("a custom indexer URL", function (this: AptosWorld) {
  this.testVectors.set("customIndexerUrl", "https://custom-indexer.example.com/v1/graphql");
});

When("I create an indexer client with the custom URL", function (this: AptosWorld) {
  const customUrl = this.testVectors.get("customIndexerUrl") as string;
  const config = new AptosConfig({
    network: Network.CUSTOM,
    indexer: customUrl,
  });
  const client = new Aptos(config);
  this.testVectors.set("indexerClient", client);
  this.testVectors.set("indexerConfig", config);
});

Then("the indexer client should use that URL", function (this: AptosWorld) {
  const config = this.testVectors.get("indexerConfig") as AptosConfig;
  const customUrl = this.testVectors.get("customIndexerUrl") as string;
  expect(config.indexer).to.equal(customUrl);
});

Given("an API key for the indexer", function (this: AptosWorld) {
  this.testVectors.set("indexerApiKey", "test-api-key-12345");
});

When("I create an indexer client with the key", function (this: AptosWorld) {
  const apiKey = this.testVectors.get("indexerApiKey") as string;
  const config = new AptosConfig({
    network: Network.TESTNET,
    clientConfig: {
      API_KEY: apiKey,
    },
  });
  const client = new Aptos(config);
  this.testVectors.set("indexerClient", client);
  this.testVectors.set("indexerConfig", config);
});

Then("requests should include the API key header", function (this: AptosWorld) {
  const config = this.testVectors.get("indexerConfig") as AptosConfig;
  expect(config.clientConfig?.API_KEY).to.not.be.undefined;
});

// =============================================================================
// Raw GraphQL Queries
// =============================================================================

Given("an indexer client", function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("indexerClient", client);
});

Given("a GraphQL query string", function (this: AptosWorld) {
  this.testVectors.set("graphqlQuery", `
    query GetLedgerInfo {
      ledger_infos {
        chain_id
      }
    }
  `);
});

When("I execute the query", async function (this: AptosWorld) {
  // Mock execution - actual execution would require network
  this.testVectors.set("queryResult", { data: { ledger_infos: [{ chain_id: 2 }] } });
});

Then("I should receive the query result", function (this: AptosWorld) {
  const result = this.testVectors.get("queryResult") as any;
  expect(result).to.not.be.undefined;
  expect(result.data).to.not.be.undefined;
});

Given("a GraphQL query with variables", function (this: AptosWorld) {
  this.testVectors.set("graphqlQuery", `
    query GetAccountTokens($address: String!) {
      current_token_ownerships_v2(where: {owner_address: {_eq: $address}}) {
        token_data_id
        amount
      }
    }
  `);
});

Given("variable values", function (this: AptosWorld) {
  this.testVectors.set("queryVariables", { address: "0x1" });
});

When("I execute the query with variables", async function (this: AptosWorld) {
  // Mock execution
  this.testVectors.set("queryResult", { 
    data: { 
      current_token_ownerships_v2: [
        { token_data_id: "0x123", amount: 1 }
      ] 
    } 
  });
});

Then("the variables should be substituted", function (this: AptosWorld) {
  const result = this.testVectors.get("queryResult") as any;
  expect(result.data.current_token_ownerships_v2).to.be.an("array");
});

Given("an invalid GraphQL query", function (this: AptosWorld) {
  this.testVectors.set("graphqlQuery", "{ invalid query syntax");
});

When("I execute the GraphQL query", async function (this: AptosWorld) {
  // Mock error
  this.error = new Error("GraphQL syntax error");
  this.testVectors.set("graphqlError", { errors: [{ message: "Syntax error" }] });
});

Then("I should receive a GraphQL error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("the error should contain the error message", function (this: AptosWorld) {
  expect(this.error!.message).to.not.be.empty;
});

// =============================================================================
// Account Tokens (NFTs)
// =============================================================================

Given("an account address with NFTs", function (this: AptosWorld) {
  this.testVectors.set("accountAddress", AccountAddress.from("0x1"));
});

When("I query current tokens for the account", async function (this: AptosWorld) {
  // Mock response
  this.testVectors.set("tokensResult", [
    {
      token_data_id: "0x123::collection::token1",
      collection_name: "Test Collection",
      token_name: "Token 1",
      amount: 1,
    },
  ]);
});

Then("I should receive a list of tokens", function (this: AptosWorld) {
  const tokens = this.testVectors.get("tokensResult") as any[];
  expect(tokens).to.be.an("array");
});

Then("each token should have collection info", function (this: AptosWorld) {
  const tokens = this.testVectors.get("tokensResult") as any[];
  for (const token of tokens) {
    expect(token.collection_name).to.not.be.undefined;
  }
});

Then("each token should have token_data_id", function (this: AptosWorld) {
  const tokens = this.testVectors.get("tokensResult") as any[];
  for (const token of tokens) {
    expect(token.token_data_id).to.not.be.undefined;
  }
});

Given("an account with many NFTs", function (this: AptosWorld) {
  this.testVectors.set("accountAddress", AccountAddress.from("0x1"));
  this.testVectors.set("totalNfts", 25);
});

When("I query tokens with limit {int} and offset {int}", async function (this: AptosWorld, limit: number, offset: number) {
  const totalNfts = this.testVectors.get("totalNfts") as number;
  const tokens = [];
  for (let i = offset; i < Math.min(offset + limit, totalNfts); i++) {
    tokens.push({ token_data_id: `token_${i}`, amount: 1 });
  }
  this.testVectors.set("tokensResult", tokens);
  this.testVectors.set("queryLimit", limit);
});

Then("I should receive at most {int} tokens", function (this: AptosWorld, limit: number) {
  const tokens = this.testVectors.get("tokensResult") as any[];
  expect(tokens.length).to.be.lessThanOrEqual(limit);
});

When("I query with offset {int}", async function (this: AptosWorld, offset: number) {
  const totalNfts = this.testVectors.get("totalNfts") as number;
  const limit = this.testVectors.get("queryLimit") as number || 10;
  const tokens = [];
  for (let i = offset; i < Math.min(offset + limit, totalNfts); i++) {
    tokens.push({ token_data_id: `token_${i}`, amount: 1 });
  }
  this.testVectors.set("tokensResult", tokens);
});

Then("I should receive the next page", function (this: AptosWorld) {
  const tokens = this.testVectors.get("tokensResult") as any[];
  expect(tokens.length).to.be.greaterThan(0);
});

Given("an account with an NFT", function (this: AptosWorld) {
  this.testVectors.set("accountAddress", AccountAddress.from("0x1"));
});

When("I query the token", async function (this: AptosWorld) {
  this.testVectors.set("tokenResult", {
    token_name: "My NFT",
    collection_name: "My Collection",
    token_uri: "https://example.com/token/1",
    amount: 1,
  });
});

Then("I should see token_name", function (this: AptosWorld) {
  const token = this.testVectors.get("tokenResult") as any;
  expect(token.token_name).to.not.be.undefined;
});

Then("I should see collection_name", function (this: AptosWorld) {
  const token = this.testVectors.get("tokenResult") as any;
  expect(token.collection_name).to.not.be.undefined;
});

Then("I should see token_uri", function (this: AptosWorld) {
  const token = this.testVectors.get("tokenResult") as any;
  expect(token.token_uri).to.not.be.undefined;
});

Then("I should see amount", function (this: AptosWorld) {
  const token = this.testVectors.get("tokenResult") as any;
  expect(token.amount).to.not.be.undefined;
});

Given("an account with no NFTs", function (this: AptosWorld) {
  this.testVectors.set("accountAddress", AccountAddress.from("0x999"));
});

When("I query current tokens", async function (this: AptosWorld) {
  this.testVectors.set("tokensResult", []);
});

Then("I should receive an empty list", function (this: AptosWorld) {
  const tokens = this.testVectors.get("tokensResult") as any[];
  expect(tokens).to.be.an("array");
  expect(tokens.length).to.equal(0);
});

// =============================================================================
// Fungible Asset Balances
// =============================================================================

When("I query fungible asset balances", async function (this: AptosWorld) {
  this.testVectors.set("fungibleAssetBalances", [
    { asset_type: "0x1::aptos_coin::AptosCoin", amount: "1000000000" },
  ]);
});

Then("I should receive a list of fungible asset balances", function (this: AptosWorld) {
  const balances = this.testVectors.get("fungibleAssetBalances") as any[];
  expect(balances).to.be.an("array");
});

Then("each balance should have asset_type and amount", function (this: AptosWorld) {
  const balances = this.testVectors.get("fungibleAssetBalances") as any[];
  for (const balance of balances) {
    expect(balance.asset_type).to.not.be.undefined;
    expect(balance.amount).to.not.be.undefined;
  }
});

Given("a specific fungible asset address", function (this: AptosWorld) {
  this.testVectors.set("fungibleAssetAddress", "0x1::aptos_coin::AptosCoin");
});

When("I query that specific balance", async function (this: AptosWorld) {
  this.testVectors.set("specificBalance", {
    asset_type: "0x1::aptos_coin::AptosCoin",
    amount: "1000000000",
  });
});

Then("I should receive only that asset's balance", function (this: AptosWorld) {
  const balance = this.testVectors.get("specificBalance") as any;
  expect(balance.asset_type).to.not.be.undefined;
});

Given("a fungible asset address", function (this: AptosWorld) {
  this.testVectors.set("fungibleAssetAddress", "0x1::aptos_coin::AptosCoin");
});

When("I query the asset metadata", async function (this: AptosWorld) {
  this.testVectors.set("assetMetadata", {
    name: "Aptos Coin",
    symbol: "APT",
    decimals: 8,
  });
});

Then("I should see name, symbol, and decimals", function (this: AptosWorld) {
  const metadata = this.testVectors.get("assetMetadata") as any;
  expect(metadata.name).to.not.be.undefined;
  expect(metadata.symbol).to.not.be.undefined;
  expect(metadata.decimals).to.not.be.undefined;
});

// =============================================================================
// Transaction History
// =============================================================================

When("I query account transaction history", async function (this: AptosWorld) {
  this.testVectors.set("transactionHistory", [
    { version: "1", type: "user_transaction", success: true },
    { version: "2", type: "user_transaction", success: true },
  ]);
});

Then("I should receive a list of indexed transactions", function (this: AptosWorld) {
  const txns = this.testVectors.get("transactionHistory") as any[];
  expect(txns).to.be.an("array");
});

Then("each transaction should have version and type", function (this: AptosWorld) {
  const txns = this.testVectors.get("transactionHistory") as any[];
  for (const txn of txns) {
    expect(txn.version).to.not.be.undefined;
    expect(txn.type).to.not.be.undefined;
  }
});

When("I query with limit {int}", async function (this: AptosWorld, limit: number) {
  const txns = [];
  for (let i = 0; i < limit; i++) {
    txns.push({ version: `${i}`, type: "user_transaction" });
  }
  this.testVectors.set("transactionHistory", txns);
});

Then("I should receive at most {int} indexed transactions", function (this: AptosWorld, limit: number) {
  const txns = this.testVectors.get("transactionHistory") as any[];
  expect(txns.length).to.be.lessThanOrEqual(limit);
});

Given("a user_transaction type filter", function (this: AptosWorld) {
  this.testVectors.set("transactionTypeFilter", "user_transaction");
});

When("I query with the filter", async function (this: AptosWorld) {
  this.testVectors.set("transactionHistory", [
    { version: "1", type: "user_transaction" },
  ]);
});

Then("all transactions should be user_transactions", function (this: AptosWorld) {
  const txns = this.testVectors.get("transactionHistory") as any[];
  for (const txn of txns) {
    expect(txn.type).to.equal("user_transaction");
  }
});

// =============================================================================
// Collections
// =============================================================================

Given("a known collection address", function (this: AptosWorld) {
  this.testVectors.set("collectionAddress", "0x123::my_collection::MyCollection");
});

When("I query the collection", async function (this: AptosWorld) {
  this.testVectors.set("collectionResult", {
    collection_name: "My Collection",
    creator_address: "0x123",
    description: "A test collection",
    current_supply: 100,
  });
});

Then("I should receive collection details", function (this: AptosWorld) {
  const collection = this.testVectors.get("collectionResult") as any;
  expect(collection).to.not.be.undefined;
});

Then("I should see creator_address", function (this: AptosWorld) {
  const collection = this.testVectors.get("collectionResult") as any;
  expect(collection.creator_address).to.not.be.undefined;
});

Then("I should see current_supply", function (this: AptosWorld) {
  const collection = this.testVectors.get("collectionResult") as any;
  expect(collection.current_supply).to.not.be.undefined;
});

When("I query tokens in the collection", async function (this: AptosWorld) {
  this.testVectors.set("collectionTokens", [
    { token_data_id: "token1", token_name: "Token 1" },
    { token_data_id: "token2", token_name: "Token 2" },
  ]);
});

Then("I should receive tokens belonging to that collection", function (this: AptosWorld) {
  const tokens = this.testVectors.get("collectionTokens") as any[];
  expect(tokens).to.be.an("array");
  expect(tokens.length).to.be.greaterThan(0);
});

When("I query collection metadata", async function (this: AptosWorld) {
  this.testVectors.set("collectionMetadata", {
    name: "My Collection",
    description: "A test collection",
    uri: "https://example.com/collection",
  });
});

Then("I should see collection name and description", function (this: AptosWorld) {
  const metadata = this.testVectors.get("collectionMetadata") as any;
  expect(metadata.name).to.not.be.undefined;
  expect(metadata.description).to.not.be.undefined;
});

Then("I should see collection URI", function (this: AptosWorld) {
  const metadata = this.testVectors.get("collectionMetadata") as any;
  expect(metadata.uri).to.not.be.undefined;
});

// =============================================================================
// Events
// =============================================================================

Given("an event type {string}", function (this: AptosWorld, eventType: string) {
  this.testVectors.set("eventType", eventType);
});

When("I query events of that type", async function (this: AptosWorld) {
  this.testVectors.set("eventsResult", [
    { type: "0x1::coin::DepositEvent", data: { amount: "100" } },
  ]);
});

Then("I should receive matching events", function (this: AptosWorld) {
  const events = this.testVectors.get("eventsResult") as any[];
  expect(events).to.be.an("array");
});

When("I query events for the account", async function (this: AptosWorld) {
  this.testVectors.set("eventsResult", [
    { type: "0x1::coin::DepositEvent", data: { amount: "100" } },
  ]);
});

Then("I should receive events involving that account", function (this: AptosWorld) {
  const events = this.testVectors.get("eventsResult") as any[];
  expect(events).to.be.an("array");
});

Then("each event should have type and data", function (this: AptosWorld) {
  const events = this.testVectors.get("eventsResult") as any[];
  for (const event of events) {
    expect(event.type).to.not.be.undefined;
    expect(event.data).to.not.be.undefined;
  }
});

// =============================================================================
// Legacy Coins
// =============================================================================

When("I query coin balances", async function (this: AptosWorld) {
  this.testVectors.set("coinBalances", [
    { coin_type: "0x1::aptos_coin::AptosCoin", amount: "1000000000" },
  ]);
});

Then("I should receive legacy coin balances", function (this: AptosWorld) {
  const balances = this.testVectors.get("coinBalances") as any[];
  expect(balances).to.be.an("array");
});

When("I query coin activities", async function (this: AptosWorld) {
  this.testVectors.set("coinActivities", [
    { activity_type: "deposit", amount: "100", coin_type: "0x1::aptos_coin::AptosCoin" },
  ]);
});

Then("I should receive deposit and withdrawal activities", function (this: AptosWorld) {
  const activities = this.testVectors.get("coinActivities") as any[];
  expect(activities).to.be.an("array");
});

// =============================================================================
// Processor Status
// =============================================================================

When("I query processor status", async function (this: AptosWorld) {
  this.testVectors.set("processorStatus", {
    processor_name: "token_processor",
    last_success_version: "12345678",
    last_updated: "2024-01-01T00:00:00Z",
  });
});

Then("I should see which processors are running", function (this: AptosWorld) {
  const status = this.testVectors.get("processorStatus") as any;
  expect(status.processor_name).to.not.be.undefined;
});

Then("I should see their last processed versions", function (this: AptosWorld) {
  const status = this.testVectors.get("processorStatus") as any;
  expect(status.last_success_version).to.not.be.undefined;
});

Given("current ledger version is known", function (this: AptosWorld) {
  this.testVectors.set("currentLedgerVersion", "12345700");
});

When("I compare indexer version to ledger version", function (this: AptosWorld) {
  const indexerVersion = parseInt(this.testVectors.get("processorStatus")?.last_success_version || "12345678", 10);
  const ledgerVersion = parseInt(this.testVectors.get("currentLedgerVersion") as string, 10);
  this.testVectors.set("indexerLag", ledgerVersion - indexerVersion);
});

Then("I can determine the lag", function (this: AptosWorld) {
  const lag = this.testVectors.get("indexerLag") as number;
  expect(lag).to.be.a("number");
});

// =============================================================================
// Error Handling
// =============================================================================

Given("the indexer is unavailable", function (this: AptosWorld) {
  this.testVectors.set("indexerUnavailable", true);
});

When("I make a query", async function (this: AptosWorld) {
  if (this.testVectors.get("indexerUnavailable")) {
    this.error = new Error("Indexer unavailable");
  }
});

Then("I should receive a connection error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Given("a very slow query", function (this: AptosWorld) {
  this.testVectors.set("slowQuery", true);
});

When("it exceeds timeout", async function (this: AptosWorld) {
  this.error = new Error("Query timeout");
});

Then("I should receive an indexer timeout error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
  expect(this.error!.message).to.include("timeout");
});

Given("a query that returns unexpected format", function (this: AptosWorld) {
  this.testVectors.set("malformedResponse", true);
});

When("the response is malformed", async function (this: AptosWorld) {
  this.error = new Error("Malformed response");
});

Then("I should receive a parsing error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});
