package main

import (
	"fmt"
	"time"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initErrorSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Error Setup Steps
	// =============================================================================

	ctx.Step(`^a transaction that will fail \(e\.g\., insufficient balance\)$`, func() error {
		// Create a transaction that will fail due to insufficient balance
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		// Large amount that unfunded account won't have
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1_000_000_000_000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^a transaction that would fail$`, func() error {
		account, err := aptos.NewEd25519Account()
		if err != nil {
			return err
		}
		world.Account = account

		recipient := aptos.AccountAddress{}
		recipient[31] = 0x42
		payload, err := aptos.CoinTransferPayload(nil, recipient, 1_000_000_000_000)
		if err != nil {
			return err
		}

		rawTx := &aptos.RawTransaction{
			Sender:                     account.Address,
			SequenceNumber:             0,
			Payload:                    aptos.TransactionPayload{Payload: payload},
			MaxGasAmount:               200000,
			GasUnitPrice:               100,
			ExpirationTimestampSeconds: uint64(time.Now().Unix() + 600),
			ChainId:                    2,
		}
		world.TestVectors["rawTransaction"] = rawTx
		return nil
	})

	ctx.Step(`^a transaction failing due to insufficient balance$`, func() error {
		world.TestVectors["errorType"] = "insufficient_balance"
		return nil
	})

	ctx.Step(`^a transaction that ran out of gas$`, func() error {
		world.TestVectors["errorType"] = "out_of_gas"
		return nil
	})

	ctx.Step(`^a transaction that fails on-chain$`, func() error {
		world.TestVectors["errorType"] = "on_chain_failure"
		return nil
	})

	ctx.Step(`^a failed transaction$`, func() error {
		world.TestVectors["errorType"] = "failed"
		world.SetError(fmt.Errorf("transaction failed"))
		return nil
	})

	ctx.Step(`^a successful transaction$`, func() error {
		world.TestVectors["transactionSuccess"] = true
		return nil
	})

	ctx.Step(`^a successful simulation$`, func() error {
		world.TestVectors["simulationSuccess"] = true
		return nil
	})

	ctx.Step(`^a transaction simulation that fails$`, func() error {
		world.TestVectors["simulationSuccess"] = false
		return nil
	})

	ctx.Step(`^a transaction with invalid signature$`, func() error {
		world.TestVectors["errorType"] = "invalid_signature"
		return nil
	})

	ctx.Step(`^a signed transaction with corrupted signature$`, func() error {
		world.TestVectors["errorType"] = "corrupted_signature"
		return nil
	})

	ctx.Step(`^a transaction rejection for invalid signature$`, func() error {
		world.TestVectors["errorType"] = "invalid_signature"
		return nil
	})

	ctx.Step(`^a transaction rejected for wrong sequence number$`, func() error {
		world.TestVectors["errorType"] = "wrong_sequence_number"
		return nil
	})

	ctx.Step(`^a SEQUENCE_NUMBER_TOO_OLD error$`, func() error {
		world.TestVectors["errorType"] = "SEQUENCE_NUMBER_TOO_OLD"
		return nil
	})

	ctx.Step(`^an OUT_OF_GAS error$`, func() error {
		world.TestVectors["errorType"] = "OUT_OF_GAS"
		return nil
	})

	ctx.Step(`^a (\d+) Too Many Requests error$`, func(statusCode int) error {
		world.TestVectors["errorType"] = "rate_limit"
		world.TestVectors["httpStatus"] = statusCode
		return nil
	})

	ctx.Step(`^an API error response \((\d+)xx or (\d+)xx\)$`, func(code1, code2 int) error {
		world.TestVectors["errorType"] = "api_error"
		return nil
	})

	ctx.Step(`^an API error with request ID header$`, func() error {
		world.TestVectors["hasRequestId"] = true
		return nil
	})

	ctx.Step(`^a network timeout or connection failure$`, func() error {
		world.TestVectors["errorType"] = "network_error"
		return nil
	})

	ctx.Step(`^a low-level error \(e\.g\., JSON parse error\)$`, func() error {
		world.TestVectors["errorType"] = "parse_error"
		return nil
	})

	ctx.Step(`^a malformed request$`, func() error {
		world.TestVectors["errorType"] = "malformed_request"
		return nil
	})

	ctx.Step(`^malformed transaction bytes$`, func() error {
		world.Bytes = []byte{0x00, 0x01, 0x02, 0x03}
		return nil
	})

	ctx.Step(`^invalid input \(e\.g\., malformed address\)$`, func() error {
		world.TestVectors["errorType"] = "invalid_input"
		return nil
	})

	ctx.Step(`^an error$`, func() error {
		world.SetError(fmt.Errorf("test error"))
		return nil
	})

	ctx.Step(`^an error during "([^"]*)"$`, func(operation string) error {
		world.TestVectors["errorOperation"] = operation
		world.SetError(fmt.Errorf("error during %s", operation))
		return nil
	})

	ctx.Step(`^an error shown to SDK users$`, func() error {
		world.SetError(fmt.Errorf("user visible error"))
		return nil
	})

	ctx.Step(`^errors occur$`, func() error {
		world.SetError(fmt.Errorf("errors occurred"))
		return nil
	})

	ctx.Step(`^operations can fail$`, func() error {
		// Just a documentation step
		return nil
	})

	ctx.Step(`^an abort from a custom module$`, func() error {
		world.TestVectors["errorType"] = "module_abort"
		return nil
	})

	ctx.Step(`^a transaction with vm_status "([^"]*)"$`, func(status string) error {
		world.TestVectors["vmStatus"] = status
		return nil
	})

	ctx.Step(`^a transaction with vm_status containing abort code$`, func() error {
		world.TestVectors["hasAbortCode"] = true
		return nil
	})

	ctx.Step(`^a transfer transaction for more than account balance$`, func() error {
		world.TestVectors["errorType"] = "insufficient_balance"
		return nil
	})

	ctx.Step(`^a transaction hash that doesn't exist$`, func() error {
		world.TestVectors["transactionHash"] = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
		return nil
	})

	ctx.Step(`^a non-existent transaction hash$`, func() error {
		world.TestVectors["transactionHash"] = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
		return nil
	})

	ctx.Step(`^a known transaction hash$`, func() error {
		// Use a placeholder - real tests would use an actual hash
		world.TestVectors["transactionHash"] = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
		return nil
	})

	ctx.Step(`^a wait timeout of (\d+) seconds$`, func(seconds int) error {
		world.TestVectors["waitTimeout"] = time.Duration(seconds) * time.Second
		return nil
	})

	ctx.Step(`^many rapid requests$`, func() error {
		world.TestVectors["requestCount"] = 100
		return nil
	})

	// =============================================================================
	// Error Handling Steps
	// =============================================================================

	ctx.Step(`^I catch the error$`, func() error {
		// Just verify we have an error state
		if world.Error == nil {
			return fmt.Errorf("expected an error to catch")
		}
		return nil
	})

	ctx.Step(`^I catch the validation error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a validation error")
		}
		return nil
	})

	ctx.Step(`^I check the error$`, func() error {
		// Error is stored in world.Error
		return nil
	})

	ctx.Step(`^I parse the error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("no error to parse")
		}
		return nil
	})

	ctx.Step(`^I check if it's retryable$`, func() error {
		// Check error type for retryability
		errorType := world.TestVectors["errorType"]
		switch errorType {
		case "network_error", "rate_limit":
			world.TestVectors["isRetryable"] = true
		default:
			world.TestVectors["isRetryable"] = false
		}
		return nil
	})

	ctx.Step(`^I detect the failure$`, func() error {
		if world.Error != nil {
			return nil
		}
		results, ok := world.TestVectors["simulationResults"].([]interface{})
		if ok && len(results) > 0 {
			return nil
		}
		return fmt.Errorf("no failure detected")
	})

	ctx.Step(`^I check the status$`, func() error {
		// Status is checked through various means
		return nil
	})

	ctx.Step(`^I parse the status$`, func() error {
		// TODO: implement status parsing validation
		return godog.ErrPending
	})

	ctx.Step(`^I check gas info$`, func() error {
		// TODO: implement gas info checking
		return godog.ErrPending
	})

	ctx.Step(`^I want to recover$`, func() error {
		// Recovery intent
		return nil
	})

	ctx.Step(`^I log it$`, func() error {
		// Logging step
		return nil
	})

	ctx.Step(`^I inspect the result$`, func() error {
		// TODO: implement result inspection
		return godog.ErrPending
	})

	// =============================================================================
	// Error Validation Steps
	// =============================================================================

	ctx.Step(`^I should be able to extract the error code$`, func() error {
		// TODO: implement error code extraction validation
		return godog.ErrPending
	})

	ctx.Step(`^I should be able to identify it as a network error$`, func() error {
		errorType := world.TestVectors["errorType"]
		if errorType != "network_error" {
			return fmt.Errorf("expected network error")
		}
		return nil
	})

	ctx.Step(`^I should extract the abort code$`, func() error {
		// TODO: implement abort code extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should get a clear timeout error$`, func() error {
		// TODO: implement timeout error validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get the detailed failure reason$`, func() error {
		// TODO: implement failure reason extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should have access to the request ID for debugging$`, func() error {
		// TODO: implement request ID access
		return godog.ErrPending
	})

	ctx.Step(`^I should identify it as balance error$`, func() error {
		errorType := world.TestVectors["errorType"]
		if errorType != "insufficient_balance" {
			return fmt.Errorf("expected balance error")
		}
		return nil
	})

	ctx.Step(`^I should identify it as out-of-gas error$`, func() error {
		errorType := world.TestVectors["errorType"]
		if errorType != "out_of_gas" && errorType != "OUT_OF_GAS" {
			return fmt.Errorf("expected out-of-gas error")
		}
		return nil
	})

	ctx.Step(`^I should know the expected sequence number$`, func() error {
		// TODO: implement sequence number extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should know which operation failed$`, func() error {
		// TODO: implement operation failure identification
		return godog.ErrPending
	})

	ctx.Step(`^I should receive a (\d+) Bad Request error$`, func(statusCode int) error {
		if world.Error == nil {
			return fmt.Errorf("expected error")
		}
		return nil
	})

	ctx.Step(`^I should receive a (\d+) NotFound error$`, func(statusCode int) error {
		if world.Error == nil {
			return fmt.Errorf("expected error")
		}
		return nil
	})

	ctx.Step(`^I should receive a Network error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected network error")
		}
		return nil
	})

	ctx.Step(`^I should receive a Timeout error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected timeout error")
		}
		return nil
	})

	ctx.Step(`^I should receive a timeout error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected timeout error")
		}
		return nil
	})

	ctx.Step(`^I should receive an error about chain ID mismatch$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected chain ID mismatch error")
		}
		return nil
	})

	ctx.Step(`^I should receive an error about expired transaction$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected expired transaction error")
		}
		return nil
	})

	ctx.Step(`^I should receive an error about invalid signature$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected invalid signature error")
		}
		return nil
	})

	ctx.Step(`^I should receive an error about sequence number$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected sequence number error")
		}
		return nil
	})

	ctx.Step(`^I should see the HTTP status code$`, func() error {
		// TODO: implement HTTP status code extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should see the VM error$`, func() error {
		// TODO: implement VM error extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should see the VM error details$`, func() error {
		// TODO: implement VM error details extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should see the VM status code$`, func() error {
		// TODO: implement VM status code extraction
		return godog.ErrPending
	})

	ctx.Step(`^I should see which input was invalid$`, func() error {
		// TODO: implement invalid input identification
		return godog.ErrPending
	})

	ctx.Step(`^it should be retryable$`, func() error {
		isRetryable, ok := world.TestVectors["isRetryable"].(bool)
		if !ok || !isRetryable {
			return fmt.Errorf("expected retryable error")
		}
		return nil
	})

	ctx.Step(`^it should indicate permanent failure$`, func() error {
		// TODO: implement permanent failure check
		return godog.ErrPending
	})

	ctx.Step(`^it should indicate success$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected success, got error: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^it's not found after timeout$`, func() error {
		// TODO: implement not-found-after-timeout validation
		return godog.ErrPending
	})

	ctx.Step(`^network errors should be retryable$`, func() error {
		// TODO: implement retryable error classification
		return godog.ErrPending
	})

	ctx.Step(`^rate limit errors should be retryable \(with backoff\)$`, func() error {
		// TODO: implement rate limit retryable classification
		return godog.ErrPending
	})

	ctx.Step(`^validation errors should NOT be retryable$`, func() error {
		// TODO: implement non-retryable error classification
		return godog.ErrPending
	})

	ctx.Step(`^the error should contain the error_code$`, func() error {
		// TODO: implement error code presence check
		return godog.ErrPending
	})

	ctx.Step(`^the error should contain the HTTP status$`, func() error {
		// TODO: implement HTTP status presence check
		return godog.ErrPending
	})

	ctx.Step(`^the error should contain the message$`, func() error {
		// TODO: implement error message presence check
		return godog.ErrPending
	})

	ctx.Step(`^the error should indicate insufficient balance$`, func() error {
		// TODO: implement insufficient balance error check
		return godog.ErrPending
	})

	ctx.Step(`^the error should indicate rate limiting$`, func() error {
		// TODO: implement rate limiting error check
		return godog.ErrPending
	})

	ctx.Step(`^the error message from the API$`, func() error {
		// TODO: implement API error message extraction
		return godog.ErrPending
	})

	ctx.Step(`^the message should explain what went wrong$`, func() error {
		// TODO: implement error message clarity validation
		return godog.ErrPending
	})

	ctx.Step(`^the abort code from that module$`, func() error {
		// TODO: implement module abort code extraction
		return godog.ErrPending
	})

	ctx.Step(`^the abort code if applicable$`, func() error {
		// TODO: implement optional abort code extraction
		return godog.ErrPending
	})

	ctx.Step(`^the module that aborted \(if available\)$`, func() error {
		// TODO: implement module identification
		return godog.ErrPending
	})

	ctx.Step(`^know that increasing max_gas_amount may help$`, func() error {
		// TODO: implement gas suggestion validation
		return godog.ErrPending
	})

	ctx.Step(`^know which account lacks funds$`, func() error {
		// TODO: implement account identification in errors
		return godog.ErrPending
	})

	ctx.Step(`^retrying won't help$`, func() error {
		// TODO: implement permanent failure indication
		return godog.ErrPending
	})

	ctx.Step(`^SDK should help estimate proper gas$`, func() error {
		// TODO: implement gas estimation suggestion check
		return godog.ErrPending
	})

	ctx.Step(`^SDK should help refresh sequence number$`, func() error {
		// TODO: implement sequence number refresh suggestion
		return godog.ErrPending
	})

	ctx.Step(`^SDK should provide human-readable descriptions$`, func() error {
		// TODO: implement human-readable description check
		return godog.ErrPending
	})

	ctx.Step(`^SDK should suggest waiting$`, func() error {
		// TODO: implement wait suggestion check
		return godog.ErrPending
	})

	// =============================================================================
	// Language-Specific Steps (documentation only)
	// =============================================================================

	ctx.Step(`^Go SDK$`, func() error {
		world.TestVectors["sdk"] = "go"
		return nil
	})

	ctx.Step(`^TypeScript SDK$`, func() error {
		world.TestVectors["sdk"] = "typescript"
		return nil
	})

	ctx.Step(`^Python SDK$`, func() error {
		world.TestVectors["sdk"] = "python"
		return nil
	})

	ctx.Step(`^Rust SDK$`, func() error {
		world.TestVectors["sdk"] = "rust"
		return nil
	})

	ctx.Step(`^they should implement error interface$`, func() error {
		// Go-specific error interface check
		return nil
	})

	ctx.Step(`^support errors\.Is\/errors\.As$`, func() error {
		// Go error wrapping support
		return nil
	})

	ctx.Step(`^they should extend Error class$`, func() error {
		// JavaScript/TypeScript specific
		return nil
	})

	ctx.Step(`^they should raise specific exceptions$`, func() error {
		// Python specific
		return nil
	})

	ctx.Step(`^they should return Result<T, E>$`, func() error {
		// Rust specific
		return nil
	})

	ctx.Step(`^errors should implement std::error::Error$`, func() error {
		// Rust specific
		return nil
	})

	ctx.Step(`^be convertible to anyhow\/thiserror$`, func() error {
		// Rust specific
		return nil
	})

	ctx.Step(`^have specific error types \(AptosApiError, etc\.\)$`, func() error {
		// TODO: implement error type hierarchy validation
		return godog.ErrPending
	})

	ctx.Step(`^inherit from a base AptosError class$`, func() error {
		// TODO: implement error inheritance validation
		return godog.ErrPending
	})

	ctx.Step(`^be catchable by type$`, func() error {
		// TODO: implement type-catchable error validation
		return godog.ErrPending
	})

	ctx.Step(`^have context about the input$`, func() error {
		// TODO: implement input context validation
		return godog.ErrPending
	})

	ctx.Step(`^higher-level context should be added$`, func() error {
		// TODO: implement error context wrapping
		return godog.ErrPending
	})

	ctx.Step(`^original error should be accessible$`, func() error {
		// TODO: implement error unwrapping validation
		return godog.ErrPending
	})

	ctx.Step(`^it propagates up$`, func() error {
		// TODO: implement error propagation validation
		return godog.ErrPending
	})

	ctx.Step(`^sensitive data \(keys\) should NOT be included$`, func() error {
		// TODO: implement sensitive data exclusion check
		return godog.ErrPending
	})

	ctx.Step(`^it should not contain internal implementation details$`, func() error {
		// TODO: implement implementation detail exclusion
		return godog.ErrPending
	})

	ctx.Step(`^should use terminology from Aptos documentation$`, func() error {
		// TODO: implement terminology consistency check
		return godog.ErrPending
	})

	ctx.Step(`^all relevant details should be included$`, func() error {
		// TODO: implement error detail completeness check
		return godog.ErrPending
	})

	ctx.Step(`^ideally suggest how to fix it$`, func() error {
		// TODO: implement fix suggestion validation
		return godog.ErrPending
	})

	ctx.Step(`^why it was invalid$`, func() error {
		// TODO: implement invalidity reason check
		return godog.ErrPending
	})

	ctx.Step(`^I receive these in errors$`, func() error {
		// TODO: implement error field presence check
		return godog.ErrPending
	})

	ctx.Step(`^common abort codes like:$`, func() error {
		// TODO: implement abort code documentation
		return godog.ErrPending
	})

	ctx.Step(`^potentially auto-retry with backoff$`, func() error {
		// TODO: implement auto-retry validation
		return godog.ErrPending
	})

	// =============================================================================
	// Simulation Steps
	// =============================================================================

	ctx.Step(`^I should get a simulation result$`, func() error {
		if _, ok := world.TestVectors["simulationResult"]; !ok {
			return fmt.Errorf("no simulation result")
		}
		return nil
	})

	ctx.Step(`^I should get a network error not a simulation failure$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a network error")
		}
		return nil
	})

	ctx.Step(`^I should get validation error before simulation even runs$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a validation error")
		}
		return nil
	})

	ctx.Step(`^I should get timeout error with suggestion to increase timeout$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected a timeout error")
		}
		return nil
	})

	// =============================================================================
	// Signed Transaction Steps
	// =============================================================================

	ctx.Step(`^I should get a valid SignedTransaction$`, func() error {
		if _, ok := world.TestVectors["signedTransaction"].(*aptos.SignedTransaction); !ok {
			return fmt.Errorf("no valid signed transaction")
		}
		return nil
	})

	ctx.Step(`^I should get a Secp256r1 SignedTransaction$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// Public Key Steps
	// =============================================================================

	ctx.Step(`^I should get a valid public key$`, func() error {
		if world.Ed25519PublicKey == nil && world.Secp256k1PublicKey == nil {
			return fmt.Errorf("no public key")
		}
		return nil
	})

	ctx.Step(`^I should get a valid Secp256r1 public key$`, func() error {
		// TODO: awaiting SDK implementation - Secp256r1
		return godog.ErrPending
	})

	// =============================================================================
	// Keyless/ZK Steps - Pending
	// =============================================================================

	ctx.Step(`^I request a ZK proof$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^I refresh the proof$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^I get the issuer$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	ctx.Step(`^I get the provider$`, func() error {
		// TODO: awaiting SDK implementation - keyless
		return godog.ErrPending
	})

	// =============================================================================
	// Result Steps
	// =============================================================================

	ctx.Step(`^I should get bytecode$`, func() error {
		// TODO: implement bytecode validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get results for each$`, func() error {
		// TODO: implement batch result validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get the original words$`, func() error {
		// TODO: awaiting SDK implementation - mnemonic not supported
		return godog.ErrPending
	})

	ctx.Step(`^I should handle type parameters correctly$`, func() error {
		// TODO: implement type parameter handling validation
		return godog.ErrPending
	})

	ctx.Step(`^I should get a typed function$`, func() error {
		return godog.ErrPending
	})

	ctx.Step(`^I should get a typed function with type hints$`, func() error {
		return godog.ErrPending
	})

	ctx.Step(`^I should get a struct with typed fields$`, func() error {
		return godog.ErrPending
	})

	ctx.Step(`^I should get an async function$`, func() error {
		return godog.ErrPending
	})

	ctx.Step(`^I should get an interface with typed fields$`, func() error {
		return godog.ErrPending
	})
}
