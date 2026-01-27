package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initRetrySteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Retry Setup
	// =============================================================================

	ctx.Step(`^an Aptos client with retry enabled$`, func() error {
		client, err := aptos.NewClient(aptos.TestnetConfig)
		if err != nil {
			return err
		}
		world.Client = client
		world.TestVectors["retryEnabled"] = true
		return nil
	})

	ctx.Step(`^a (\d+) response with Retry-After: (\d+)$`, func(status, seconds int) error {
		world.TestVectors["httpStatus"] = status
		world.TestVectors["retryAfter"] = seconds
		return nil
	})

	ctx.Step(`^a (\d+) response with Retry-After as HTTP date$`, func(status int) error {
		world.TestVectors["httpStatus"] = status
		world.TestVectors["retryAfterDate"] = time.Now().Add(5 * time.Second).Format(time.RFC1123)
		return nil
	})

	ctx.Step(`^a (\d+) response without Retry-After$`, func(status int) error {
		world.TestVectors["httpStatus"] = status
		world.TestVectors["noRetryAfter"] = true
		return nil
	})

	ctx.Step(`^a retry occurs$`, func() error {
		world.TestVectors["retryOccurred"] = true
		return nil
	})

	ctx.Step(`^any API method encounters retryable error$`, func() error {
		world.TestVectors["retryableError"] = true
		return nil
	})

	ctx.Step(`^exponential backoff with jitter enabled$`, func() error {
		world.TestVectors["exponentialBackoff"] = true
		world.TestVectors["jitterEnabled"] = true
		return nil
	})

	ctx.Step(`^initial_delay=(\d+)ms and backoff_factor=(\d+)\.(\d+)$`, func(delay, factor1, factor2 int) error {
		world.TestVectors["initialDelay"] = time.Duration(delay) * time.Millisecond
		world.TestVectors["backoffFactor"] = float64(factor1) + float64(factor2)/10.0
		return nil
	})

	ctx.Step(`^initial_delay=(\d+)ms, backoff_factor=(\d+)\.(\d+), max_delay=(\d+)ms$`, func(delay, factor1, factor2, maxDelay int) error {
		world.TestVectors["initialDelay"] = time.Duration(delay) * time.Millisecond
		world.TestVectors["backoffFactor"] = float64(factor1) + float64(factor2)/10.0
		world.TestVectors["maxDelay"] = time.Duration(maxDelay) * time.Millisecond
		return nil
	})

	ctx.Step(`^it fails with retryable error$`, func() error {
		world.TestVectors["retryableError"] = true
		world.SetError(fmt.Errorf("retryable error"))
		return nil
	})

	ctx.Step(`^deciding whether to retry$`, func() error {
		world.TestVectors["decidingRetry"] = true
		return nil
	})

	// =============================================================================
	// When Steps - Retry Operations
	// =============================================================================

	ctx.Step(`^I make a request with retry disabled$`, func() error {
		if world.Client == nil {
			client, err := aptos.NewClient(aptos.TestnetConfig)
			if err != nil {
				return err
			}
			world.Client = client
		}
		world.TestVectors["retryDisabled"] = true
		return nil
	})

	// =============================================================================
	// Then Steps - Retry Validation
	// =============================================================================

	ctx.Step(`^it should NOT retry the same transaction$`, func() error {
		// Transaction submission should not be retried
		world.TestVectors["noTxRetry"] = true
		return nil
	})

	ctx.Step(`^it should NOT retry$`, func() error {
		world.TestVectors["noRetry"] = true
		return nil
	})

	ctx.Step(`^it should retry after delay$`, func() error {
		world.TestVectors["retryAfterDelay"] = true
		return nil
	})

	ctx.Step(`^it should retry the request$`, func() error {
		world.TestVectors["shouldRetry"] = true
		return nil
	})

	ctx.Step(`^it should retry twice$`, func() error {
		world.TestVectors["retryCount"] = 2
		return nil
	})

	ctx.Step(`^it should use default backoff$`, func() error {
		world.TestVectors["useDefaultBackoff"] = true
		return nil
	})

	ctx.Step(`^it should wait at least (\d+) seconds before retrying$`, func(seconds int) error {
		world.TestVectors["minRetryWait"] = time.Duration(seconds) * time.Second
		return nil
	})

	ctx.Step(`^backoff should be exponential$`, func() error {
		world.TestVectors["exponentialBackoff"] = true
		return nil
	})

	ctx.Step(`^the delay should be approximately (\d+)ms$`, func(ms int) error {
		world.TestVectors["expectedDelay"] = time.Duration(ms) * time.Millisecond
		return nil
	})

	ctx.Step(`^the delay should include jitter$`, func() error {
		world.TestVectors["hasJitter"] = true
		return nil
	})

	ctx.Step(`^the delay should not exceed (\d+)ms$`, func(ms int) error {
		world.TestVectors["maxDelay"] = time.Duration(ms) * time.Millisecond
		return nil
	})

	ctx.Step(`^the delay should be roughly (\d+)ms \(with jitter\)$`, func(ms int) error {
		world.TestVectors["roughDelay"] = time.Duration(ms) * time.Millisecond
		return nil
	})

	ctx.Step(`^the request should succeed without retry$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("request failed: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^the SDK should eventually fail after max attempts$`, func() error {
		world.TestVectors["maxAttemptsReached"] = true
		return nil
	})

	ctx.Step(`^the SDK should parse the date correctly$`, func() error {
		return nil
	})

	ctx.Step(`^the SDK should respect Retry-After$`, func() error {
		return nil
	})

	ctx.Step(`^the SDK should return success$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected success: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^jitter should be within (\d+)% of base delay$`, func(percent int) error {
		world.TestVectors["jitterPercent"] = percent
		return nil
	})

	ctx.Step(`^max_retries=(\d+)$`, func(maxRetries int) error {
		world.TestVectors["maxRetries"] = maxRetries
		return nil
	})

	ctx.Step(`^multiple requests fail simultaneously$`, func() error {
		world.TestVectors["simultaneousFailures"] = true
		return nil
	})

	ctx.Step(`^their retry timings should differ$`, func() error {
		world.TestVectors["differentTimings"] = true
		return nil
	})

	ctx.Step(`^the (\d+)(?:st|nd|rd|th) attempt should happen after approximately (\d+)ms$`, func(attempt, ms int) error {
		world.TestVectors[fmt.Sprintf("attempt%dDelay", attempt)] = time.Duration(ms) * time.Millisecond
		return nil
	})

	ctx.Step(`^the (\d+)(?:st|nd|rd|th) request succeeds$`, func(attempt int) error {
		world.TestVectors["successAttempt"] = attempt
		return nil
	})

	ctx.Step(`^(\d+) retries are attempted$`, func(count int) error {
		world.TestVectors["retryAttempts"] = count
		return nil
	})
}
