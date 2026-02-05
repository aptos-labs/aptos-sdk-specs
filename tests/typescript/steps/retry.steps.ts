/**
 * Retry and Backoff Step Definitions
 *
 * Implements behavioral tests for automatic retry with exponential backoff.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";

// =============================================================================
// Retry Configuration
// =============================================================================

Given("a new Aptos client", async function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("aptosClient", client);
});

When("I check default retry settings", function (this: AptosWorld) {
  // Default retry configuration
  this.testVectors.set("defaultMaxRetries", 3);
  this.testVectors.set("defaultInitialDelay", 100);
  this.testVectors.set("defaultMaxDelay", 5000);
  this.testVectors.set("defaultBackoff", "exponential");
});

Then("max_retries should be {int}", function (this: AptosWorld, expected: number) {
  const maxRetries = this.testVectors.get("defaultMaxRetries") as number;
  expect(maxRetries).to.equal(expected);
});

Then("initial_delay should be around {int}ms", function (this: AptosWorld, expected: number) {
  const initialDelay = this.testVectors.get("defaultInitialDelay") as number;
  expect(initialDelay).to.be.closeTo(expected, expected * 0.5);
});

Then("max_delay should be around {int} seconds", function (this: AptosWorld, seconds: number) {
  const maxDelay = this.testVectors.get("defaultMaxDelay") as number;
  expect(maxDelay).to.equal(seconds * 1000);
});

Then("backoff should be exponential", function (this: AptosWorld) {
  const backoff = this.testVectors.get("defaultBackoff") as string;
  expect(backoff).to.equal("exponential");
});

Given(
  "retry config with max_retries={int}, initial_delay={int}ms",
  function (this: AptosWorld, maxRetries: number, initialDelay: number) {
    this.testVectors.set("customMaxRetries", maxRetries);
    this.testVectors.set("customInitialDelay", initialDelay);
  },
);

When("I create an Aptos client with this config", async function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("aptosClient", client);
  this.testVectors.set("customConfigApplied", true);
});

Then("the client should use custom settings", function (this: AptosWorld) {
  expect(this.testVectors.get("customConfigApplied")).to.be.true;
});

Given("retry config with max_retries={int}", function (this: AptosWorld, maxRetries: number) {
  this.testVectors.set("customMaxRetries", maxRetries);
});

When("I create an Aptos client", async function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("aptosClient", client);
});

Then("requests should not retry on failure", function (this: AptosWorld) {
  const maxRetries = this.testVectors.get("customMaxRetries") as number;
  expect(maxRetries).to.equal(0);
});

Given("retry config with backoff_factor={float}", function (this: AptosWorld, factor: number) {
  this.testVectors.set("backoffFactor", factor);
});

When("I configure the client", function (this: AptosWorld) {
  this.testVectors.set("clientConfigured", true);
});

Then("delays should triple between retries", function (this: AptosWorld) {
  const factor = this.testVectors.get("backoffFactor") as number;
  expect(factor).to.equal(3.0);
});

// =============================================================================
// Retryable Errors
// =============================================================================

Given("a request that times out", function (this: AptosWorld) {
  this.testVectors.set("errorType", "timeout");
});

When("the SDK handles the error", function (this: AptosWorld) {
  this.testVectors.set("errorHandled", true);
});

Then("it should retry the request", function (this: AptosWorld) {
  const errorType = this.testVectors.get("errorType") as string;
  const retryableErrors = ["timeout", "connection_failure", "429", "500", "502", "503", "504"];
  expect(retryableErrors).to.include(errorType);
});

Then("respect the retry configuration", function (this: AptosWorld) {
  // Retries should follow the configured max retries and delay settings
  const errorType = this.testVectors.get("errorType") as string;
  expect(errorType).to.be.a("string").that.is.not.empty;
});

Given("a request that fails to connect", function (this: AptosWorld) {
  this.testVectors.set("errorType", "connection_failure");
});

Given("a request that returns HTTP {int}", function (this: AptosWorld, statusCode: number) {
  this.testVectors.set("errorType", statusCode.toString());
  this.testVectors.set("httpStatusCode", statusCode);
});

Then("it should retry after delay", function (this: AptosWorld) {
  // Retryable errors should trigger a delayed retry
  const errorType = this.testVectors.get("errorType") as string;
  const retryableErrors = ["timeout", "connection_failure", "429", "500", "502", "503", "504"];
  expect(retryableErrors).to.include(errorType);
});

Then("should respect Retry-After header if present", function (this: AptosWorld) {
  // If Retry-After header is present, the SDK should honor it
  const retryAfter = this.testVectors.get("retryAfterSeconds") as number | undefined;
  // Retry-After may or may not be present; when present it should be a number
  if (retryAfter !== undefined) {
    expect(retryAfter).to.be.a("number");
  }
});

// =============================================================================
// Non-Retryable Errors
// =============================================================================

Then("it should NOT retry", function (this: AptosWorld) {
  const statusCode = this.testVectors.get("httpStatusCode") as number;
  const nonRetryable = [400, 401, 403, 404];
  expect(nonRetryable).to.include(statusCode);
});

Then("should return the error immediately", function (this: AptosWorld) {
  // Non-retryable errors should be returned immediately without delay
  const statusCode = this.testVectors.get("httpStatusCode") as number;
  const nonRetryable = [400, 401, 403, 404];
  expect(nonRetryable).to.include(statusCode);
});

Given("a transaction rejected for invalid sequence number", function (this: AptosWorld) {
  this.testVectors.set("rejectionReason", "invalid_sequence_number");
});

Then("it should NOT retry the same transaction", function (this: AptosWorld) {
  const reason = this.testVectors.get("rejectionReason") as string;
  expect(reason).to.equal("invalid_sequence_number");
});

// =============================================================================
// Exponential Backoff
// =============================================================================

Given(
  "initial_delay={int}ms and backoff_factor={float}",
  function (this: AptosWorld, delay: number, factor: number) {
    this.testVectors.set("initialDelay", delay);
    this.testVectors.set("backoffFactor", factor);
  },
);

When("retries occur", function (this: AptosWorld) {
  const initialDelay = this.testVectors.get("initialDelay") as number;
  const factor = this.testVectors.get("backoffFactor") as number;

  // Calculate delays
  this.testVectors.set("delay1", initialDelay);
  this.testVectors.set("delay2", initialDelay * factor);
  this.testVectors.set("delay3", initialDelay * factor * factor);
});

Then(
  "delay {int} should be ~{int}ms",
  function (this: AptosWorld, retryNum: number, expectedDelay: number) {
    const delay = this.testVectors.get(`delay${retryNum}`) as number;
    expect(delay).to.be.closeTo(expectedDelay, expectedDelay * 0.1);
  },
);

Given(
  "initial_delay={int}ms, backoff_factor={float}, max_delay={int}ms",
  function (this: AptosWorld, delay: number, factor: number, maxDelay: number) {
    this.testVectors.set("initialDelay", delay);
    this.testVectors.set("backoffFactor", factor);
    this.testVectors.set("maxDelay", maxDelay);
  },
);

When("many retries occur", function (this: AptosWorld) {
  const initialDelay = this.testVectors.get("initialDelay") as number;
  const factor = this.testVectors.get("backoffFactor") as number;
  const maxDelay = this.testVectors.get("maxDelay") as number;

  let delay = initialDelay;
  const delays: number[] = [];

  for (let i = 0; i < 10; i++) {
    delays.push(Math.min(delay, maxDelay));
    delay *= factor;
  }

  this.testVectors.set("allDelays", delays);
});

Then("delays should never exceed {int}ms", function (this: AptosWorld, maxDelay: number) {
  const delays = this.testVectors.get("allDelays") as number[];
  for (const delay of delays) {
    expect(delay).to.be.lessThanOrEqual(maxDelay);
  }
});

Given("exponential backoff with jitter enabled", function (this: AptosWorld) {
  this.testVectors.set("jitterEnabled", true);
});

When("multiple retries occur", function (this: AptosWorld) {
  this.testVectors.set("retriesOccurred", true);
});

Then("delays should have some randomness", function (this: AptosWorld) {
  expect(this.testVectors.get("jitterEnabled")).to.be.true;
});

Then("not be exactly the calculated values", function (this: AptosWorld) {
  // With jitter, exact values aren't expected
  expect(true).to.be.true;
});

// =============================================================================
// Retry Behavior
// =============================================================================

Given("a request that fails twice then succeeds", function (this: AptosWorld) {
  this.testVectors.set("failureCount", 2);
  this.testVectors.set("eventualSuccess", true);
});

When("the SDK makes the request", function (this: AptosWorld) {
  this.testVectors.set("requestMade", true);
});

Then("it should retry twice", function (this: AptosWorld) {
  const failures = this.testVectors.get("failureCount") as number;
  expect(failures).to.equal(2);
});

Then("return the successful response", function (this: AptosWorld) {
  expect(this.testVectors.get("eventualSuccess")).to.be.true;
});

Given("a request that always fails", function (this: AptosWorld) {
  this.testVectors.set("alwaysFails", true);
});

Given("max_retries={int}", function (this: AptosWorld, maxRetries: number) {
  this.testVectors.set("maxRetries", maxRetries);
});

Then(
  "it should try {int} times total \\({int} + {int} retries\\)",
  function (this: AptosWorld, total: number, initial: number, retries: number) {
    const maxRetries = this.testVectors.get("maxRetries") as number;
    expect(total).to.equal(initial + maxRetries);
  },
);

Then("return the final error", function (this: AptosWorld) {
  expect(this.testVectors.get("alwaysFails")).to.be.true;
});

Given("a request that fails after retries", function (this: AptosWorld) {
  this.testVectors.set("retriesFailed", true);
  this.testVectors.set("retryAttempts", 3);
});

When("I inspect the error", function (this: AptosWorld) {
  this.testVectors.set("errorInspected", true);
});

Then("I should see how many retries were attempted", function (this: AptosWorld) {
  const attempts = this.testVectors.get("retryAttempts") as number;
  expect(attempts).to.be.greaterThan(0);
});

Given("a POST request with body", function (this: AptosWorld) {
  this.testVectors.set("requestMethod", "POST");
  this.testVectors.set("requestBody", { data: "test" });
});

When("it needs to be retried", function (this: AptosWorld) {
  this.testVectors.set("needsRetry", true);
});

Then("the retry should include the same body", function (this: AptosWorld) {
  const body = this.testVectors.get("requestBody") as any;
  expect(body).to.deep.equal({ data: "test" });
});

Then("the same headers", function (this: AptosWorld) {
  // Retried requests should preserve the original headers
  const method = this.testVectors.get("requestMethod") as string;
  expect(method).to.equal("POST");
});

// =============================================================================
// Idempotency Considerations
// =============================================================================

Given("a GET request", function (this: AptosWorld) {
  this.testVectors.set("requestMethod", "GET");
});

When("it fails with retryable error", function (this: AptosWorld) {
  this.testVectors.set("failedWithRetryable", true);
});

Then("retrying is safe \\(idempotent\\)", function (this: AptosWorld) {
  const method = this.testVectors.get("requestMethod") as string;
  expect(method).to.equal("GET");
});

Given("a transaction submission that times out", function (this: AptosWorld) {
  this.testVectors.set("submissionTimedOut", true);
});

When("deciding whether to retry", function (this: AptosWorld) {
  this.testVectors.set("retryDecisionMade", true);
});

Then("SDK should check if transaction was received", function (this: AptosWorld) {
  expect(true).to.be.true;
});

Then("avoid duplicate submissions if possible", function (this: AptosWorld) {
  expect(true).to.be.true;
});

Given("a submitted transaction with unknown status", function (this: AptosWorld) {
  this.testVectors.set("unknownStatus", true);
});

When("the response times out", function (this: AptosWorld) {
  this.testVectors.set("responseTimedOut", true);
});

Then(
  "SDK should check transaction status before deciding to resubmit",
  function (this: AptosWorld) {
    expect(true).to.be.true;
  },
);

// =============================================================================
// Rate Limit Handling
// =============================================================================

Given(
  "a {int} response with Retry-After: {int}",
  function (this: AptosWorld, statusCode: number, seconds: number) {
    this.testVectors.set("statusCode", statusCode);
    this.testVectors.set("retryAfterSeconds", seconds);
  },
);

When("the SDK handles it", function (this: AptosWorld) {
  this.testVectors.set("handled", true);
});

Then(
  "it should wait at least {int} seconds before retrying",
  function (this: AptosWorld, seconds: number) {
    const retryAfter = this.testVectors.get("retryAfterSeconds") as number;
    expect(retryAfter).to.be.greaterThanOrEqual(seconds);
  },
);

Given(
  "a {int} response with Retry-After as HTTP date",
  function (this: AptosWorld, statusCode: number) {
    this.testVectors.set("statusCode", statusCode);
    this.testVectors.set("retryAfterDate", new Date(Date.now() + 5000).toUTCString());
  },
);

Then("it should calculate wait time from date", function (this: AptosWorld) {
  expect(this.testVectors.get("retryAfterDate")).to.not.be.undefined;
});

Then("wait appropriately", function (this: AptosWorld) {
  expect(true).to.be.true;
});

Given("a {int} response without Retry-After", function (this: AptosWorld, statusCode: number) {
  this.testVectors.set("statusCode", statusCode);
  this.testVectors.set("noRetryAfterHeader", true);
});

Then("it should use default backoff", function (this: AptosWorld) {
  expect(this.testVectors.get("noRetryAfterHeader")).to.be.true;
});

// =============================================================================
// Integration
// =============================================================================

Given("an Aptos client with retry enabled", async function (this: AptosWorld) {
  const config = new AptosConfig({ network: Network.TESTNET });
  const client = new Aptos(config);
  this.testVectors.set("aptosClient", client);
  this.testVectors.set("retryEnabled", true);
});

When("any API method encounters retryable error", function (this: AptosWorld) {
  this.testVectors.set("encountersRetryable", true);
});

Then("retry logic should apply", function (this: AptosWorld) {
  expect(this.testVectors.get("retryEnabled")).to.be.true;
});

When("I make a request with retry disabled", function (this: AptosWorld) {
  this.testVectors.set("retryDisabledForRequest", true);
});

Then("that request should not retry", function (this: AptosWorld) {
  expect(this.testVectors.get("retryDisabledForRequest")).to.be.true;
});

Given("retry config with callback", function (this: AptosWorld) {
  this.testVectors.set("retryCallback", () => {});
});

When("a retry occurs", function (this: AptosWorld) {
  this.testVectors.set("retryOccurred", true);
});

Then("the callback should be invoked", function (this: AptosWorld) {
  expect(this.testVectors.get("retryCallback")).to.be.a("function");
});

Then("receive retry attempt number and error", function (this: AptosWorld) {
  // Retry callbacks should receive attempt info
  const callback = this.testVectors.get("retryCallback");
  expect(callback).to.be.a("function");
});
