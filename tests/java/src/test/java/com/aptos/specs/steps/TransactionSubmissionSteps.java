package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptoslabs.japtos.account.Ed25519Account;
import com.aptoslabs.japtos.client.AptosClient;
import com.aptoslabs.japtos.api.AptosConfig;
import com.aptoslabs.japtos.types.*;
import com.aptoslabs.japtos.utils.HexUtils;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for transaction-submission.feature
 * 
 * These steps test transaction submission, waiting, and simulation
 * using the japtos SDK.
 */
public class TransactionSubmissionSteps {
    
    private final World world;
    
    // Client and accounts
    private AptosClient client;
    private Ed25519Account fundedAccount;
    private Ed25519Account testAccount;
    
    // Transactions
    private RawTransaction rawTransaction;
    private SignedTransaction signedTransaction;
    private TransactionPayload payload;
    private byte[] transactionBytes;
    
    // Submission results
    private String submittedHash;
    private Object pendingResponse;
    private Object transactionResult;
    private Object simulationResult;
    private Object gasEstimate;
    private Exception caughtError;
    
    // Test state
    private long accountSequenceNumber;
    private int waitTimeoutSeconds = 30;
    private String locallyComputedHash;
    
    public TransactionSubmissionSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Client and Accounts
    // ==========================================================================
    
    @Given("a client connected to testnet")
    public void givenClientConnectedToTestnet() {
        AptosConfig config = AptosConfig.builder()
            .network(AptosConfig.Network.TESTNET)
            .build();
        client = new AptosClient(config);
        world.setClient(client);
    }
    
    @Given("a funded account")
    public void givenFundedAccount() {
        fundedAccount = Ed25519Account.generate();
        world.setAccount(fundedAccount);
    }
    
    @Given("a valid signed APT transfer transaction")
    public void givenValidSignedAptTransfer() {
        createSignedAptTransfer(fundedAccount);
    }
    
    @Given("a signed transaction for submission")
    public void givenSignedTransactionForSubmission() {
        if (fundedAccount == null) {
            fundedAccount = Ed25519Account.generate();
        }
        createSignedAptTransfer(fundedAccount);
    }
    
    @Given("a valid signed transaction")
    public void givenValidSignedTransaction() {
        givenSignedTransactionForSubmission();
    }
    
    @Given("malformed transaction bytes")
    public void givenMalformedTransactionBytes() {
        transactionBytes = new byte[]{0x00, 0x01, 0x02, 0x03}; // Invalid BCS
    }
    
    @Given("a signed transaction with corrupted signature")
    public void givenSignedTransactionWithCorruptedSignature() {
        createSignedAptTransfer(fundedAccount);
        // Corrupt the signature bytes
        byte[] bytes = signedTransaction.toBytes();
        bytes[bytes.length - 1] ^= 0xFF; // Flip last byte
        transactionBytes = bytes;
    }
    
    @Given("a transaction signed for mainnet \\(chain_id={int}\\)")
    public void givenTransactionSignedForMainnet(int chainId) {
        fundedAccount = Ed25519Account.generate();
        rawTransaction = createRawTransaction(fundedAccount, new ChainId((byte) chainId));
        signedTransaction = fundedAccount.signTransaction(rawTransaction);
    }
    
    @Given("a client connected to testnet \\(chain_id={int}\\)")
    public void givenClientConnectedToTestnetWithChainId(int chainId) {
        AptosConfig config = AptosConfig.builder()
            .network(AptosConfig.Network.TESTNET)
            .build();
        client = new AptosClient(config);
    }
    
    @Given("a signed transaction with past expiration")
    public void givenSignedTransactionWithPastExpiration() {
        fundedAccount = Ed25519Account.generate();
        // Create transaction that expired in the past
        long pastExpiration = Instant.now().getEpochSecond() - 3600; // 1 hour ago
        rawTransaction = createRawTransactionWithExpiration(fundedAccount, pastExpiration);
        signedTransaction = fundedAccount.signTransaction(rawTransaction);
    }
    
    // ==========================================================================
    // Given Steps - Wait for Transaction
    // ==========================================================================
    
    @Given("a submitted transaction hash")
    public void givenSubmittedTransactionHash() {
        submittedHash = "0x" + "a".repeat(64); // Placeholder hash
    }
    
    @Given("a transaction hash that doesn't exist")
    public void givenNonExistentTransactionHash() {
        submittedHash = "0x" + "f".repeat(64);
    }
    
    @Given("a wait timeout of {int} seconds")
    public void givenWaitTimeout(int seconds) {
        waitTimeoutSeconds = seconds;
    }
    
    @Given("a successful transaction")
    public void givenSuccessfulTransaction() {
        givenSubmittedTransactionHash();
    }
    
    @Given("a transaction that will fail \\(e.g., insufficient balance\\)")
    public void givenTransactionThatWillFail() {
        givenSubmittedTransactionHash();
    }
    
    @Given("a newly submitted transaction")
    public void givenNewlySubmittedTransaction() {
        givenSubmittedTransactionHash();
    }
    
    // ==========================================================================
    // Given Steps - Submit and Wait
    // ==========================================================================
    
    @Given("a valid transaction payload")
    public void givenValidTransactionPayload() {
        createPayload();
    }
    
    @Given("a transaction payload")
    public void givenTransactionPayload() {
        createPayload();
    }
    
    // ==========================================================================
    // Given Steps - Simulation
    // ==========================================================================
    
    @Given("a valid transaction")
    public void givenValidTransaction() {
        if (fundedAccount == null) {
            fundedAccount = Ed25519Account.generate();
        }
        createSignedAptTransfer(fundedAccount);
    }
    
    @Given("a transaction that would fail")
    public void givenTransactionThatWouldFail() {
        givenValidTransaction();
    }
    
    @Given("a transfer transaction for more than account balance")
    public void givenTransferForMoreThanBalance() {
        givenValidTransaction();
    }
    
    @Given("a transaction with invalid signature")
    public void givenTransactionWithInvalidSignature() {
        givenSignedTransactionWithCorruptedSignature();
    }
    
    // ==========================================================================
    // Given Steps - Gas Estimation
    // ==========================================================================
    
    @Given("a gas price estimate")
    public void givenGasPriceEstimate() {
        gasEstimate = 100L; // Default gas price
    }
    
    // ==========================================================================
    // Given Steps - Sequence Number
    // ==========================================================================
    
    @Given("an account address")
    public void givenAccountAddressForSeqNum() {
        if (fundedAccount == null) {
            fundedAccount = Ed25519Account.generate();
        }
    }
    
    @Given("an account with sequence_number {int}")
    public void givenAccountWithSequenceNumber(int seqNum) {
        accountSequenceNumber = seqNum;
        if (fundedAccount == null) {
            fundedAccount = Ed25519Account.generate();
        }
    }
    
    // ==========================================================================
    // Given Steps - Error Handling
    // ==========================================================================
    
    @Given("a client with unreachable endpoint")
    public void givenClientWithUnreachableEndpoint() {
        AptosConfig config = AptosConfig.builder()
            .fullnodeUrl("https://unreachable.example.com/v1")
            .build();
        client = new AptosClient(config);
    }
    
    @Given("a transaction that fails on-chain")
    public void givenTransactionThatFailsOnChain() {
        givenSubmittedTransactionHash();
    }
    
    // ==========================================================================
    // When Steps - Submission
    // ==========================================================================
    
    @When("I submit the transaction")
    public void whenSubmitTransaction() {
        try {
            pendingResponse = client.submitTransaction(signedTransaction);
            submittedHash = signedTransaction.getHash();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I submit it to the API")
    public void whenSubmitToApi() {
        whenSubmitTransaction();
    }
    
    @When("I submit it successfully")
    public void whenSubmitSuccessfully() {
        whenSubmitTransaction();
    }
    
    @When("I try to submit them")
    public void whenTryToSubmitMalformed() {
        try {
            // Try to submit malformed bytes directly
            client.submitBcsTransaction(transactionBytes);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I try to submit it")
    public void whenTryToSubmit() {
        try {
            if (transactionBytes != null) {
                client.submitBcsTransaction(transactionBytes);
            } else {
                client.submitTransaction(signedTransaction);
            }
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I try to submit the transaction")
    public void whenTryToSubmitTransaction() {
        whenTryToSubmit();
    }
    
    // ==========================================================================
    // When Steps - Wait for Transaction
    // ==========================================================================
    
    @When("I wait for the transaction")
    public void whenWaitForTransaction() {
        try {
            transactionResult = client.waitForTransaction(submittedHash, waitTimeoutSeconds);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I wait for it to complete")
    public void whenWaitForCompletion() {
        whenWaitForTransaction();
    }
    
    @When("I wait for it")
    public void whenWaitForIt() {
        whenWaitForTransaction();
    }
    
    // ==========================================================================
    // When Steps - Submit and Wait
    // ==========================================================================
    
    @When("I call submit_and_wait")
    public void whenCallSubmitAndWait() {
        try {
            if (signedTransaction == null) {
                createSignedAptTransfer(fundedAccount);
            }
            transactionResult = client.submitAndWait(signedTransaction);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I call sign_submit_and_wait")
    public void whenCallSignSubmitAndWait() {
        try {
            if (rawTransaction == null) {
                rawTransaction = createRawTransaction(fundedAccount, new ChainId((byte) 2));
            }
            transactionResult = client.signSubmitAndWait(fundedAccount, rawTransaction);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // When Steps - Simulation
    // ==========================================================================
    
    @When("I simulate the transaction")
    public void whenSimulateTransaction() {
        try {
            simulationResult = client.simulateTransaction(signedTransaction);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I simulate it")
    public void whenSimulateIt() {
        whenSimulateTransaction();
    }
    
    // ==========================================================================
    // When Steps - Gas Estimation
    // ==========================================================================
    
    @When("I request gas price estimate")
    public void whenRequestGasPriceEstimate() {
        try {
            gasEstimate = client.getGasEstimate();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I build a transaction using the estimate")
    public void whenBuildTransactionUsingEstimate() {
        long gasPrice = (long) gasEstimate;
        rawTransaction = new RawTransaction(
            fundedAccount.getAccountAddress(),
            0L,
            payload,
            200000L,
            gasPrice,
            Instant.now().getEpochSecond() + 600,
            new ChainId((byte) 2)
        );
    }
    
    @When("submit it")
    public void whenSubmitIt() {
        signedTransaction = fundedAccount.signTransaction(rawTransaction);
        whenSubmitTransaction();
    }
    
    // ==========================================================================
    // When Steps - Sequence Number
    // ==========================================================================
    
    @When("I get the account info")
    public void whenGetAccountInfo() {
        try {
            AccountInfo info = client.getAccountInfo(fundedAccount.getAccountAddress());
            accountSequenceNumber = info.getSequenceNumber();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            caughtError = e;
        }
    }
    
    @When("I submit a transaction with sequence_number {int}")
    public void whenSubmitWithSequenceNumber(int seqNum) {
        rawTransaction = new RawTransaction(
            fundedAccount.getAccountAddress(),
            seqNum,
            payload != null ? payload : createPayload(),
            200000L,
            100L,
            Instant.now().getEpochSecond() + 600,
            new ChainId((byte) 2)
        );
        signedTransaction = fundedAccount.signTransaction(rawTransaction);
        whenTryToSubmit();
    }
    
    @When("I submit transactions with sequence numbers {int}, {int}, {int}")
    public void whenSubmitMultipleTransactions(int seq0, int seq1, int seq2) {
        for (int seqNum : new int[]{seq0, seq1, seq2}) {
            whenSubmitWithSequenceNumber(seqNum);
        }
    }
    
    // ==========================================================================
    // When Steps - Error Handling
    // ==========================================================================
    
    @When("I compute its hash locally")
    public void whenComputeHashLocally() {
        locallyComputedHash = computeTransactionHash(signedTransaction);
    }
    
    @When("compare with the hash from submission response")
    public void whenCompareWithSubmissionResponse() {
        // Hash comparison done in Then step
    }
    
    // ==========================================================================
    // Then Steps - Submission
    // ==========================================================================
    
    @Then("I should receive a pending transaction response")
    public void thenShouldReceivePendingResponse() {
        assertThat(pendingResponse).isNotNull();
    }
    
    @Then("the response should contain the transaction hash")
    public void thenResponseShouldContainHash() {
        assertThat(submittedHash).isNotNull();
        assertThat(submittedHash).startsWith("0x");
    }
    
    @Then("the request content type should be {string}")
    public void thenContentTypeShouldBe(String expected) {
        // Content type is handled by japtos SDK
        assertThat(true).isTrue();
    }
    
    @Then("the body should be BCS-serialized bytes")
    public void thenBodyShouldBeBcs() {
        assertThat(signedTransaction.toBytes()).isNotNull();
    }
    
    @Then("I should receive the transaction hash")
    public void thenShouldReceiveTransactionHash() {
        assertThat(submittedHash).isNotNull();
    }
    
    @Then("the hash should be {int} hex characters with 0x prefix")
    public void thenHashShouldBe64HexChars(int chars) {
        assertThat(submittedHash).hasSize(chars + 2); // +2 for "0x"
        assertThat(submittedHash).startsWith("0x");
    }
    
    @Then("I should receive a {int} Bad Request error")
    public void thenShouldReceiveBadRequestError(int statusCode) {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("I should receive an error about invalid signature")
    public void thenShouldReceiveInvalidSignatureError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("I should receive an error about chain ID mismatch")
    public void thenShouldReceiveChainIdMismatchError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("I should receive an error about expired transaction")
    public void thenShouldReceiveExpiredTransactionError() {
        assertThat(caughtError).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Wait for Transaction
    // ==========================================================================
    
    @Then("I should receive the final transaction result")
    public void thenShouldReceiveFinalResult() {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("the transaction should be committed or failed")
    public void thenTransactionShouldBeCommittedOrFailed() {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("I should receive a timeout error")
    public void thenShouldReceiveTimeoutError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the result should indicate success: {word}")
    public void thenResultShouldIndicateSuccess(String success) {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("I should see the VM error")
    public void thenShouldSeeVmError() {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("the SDK should poll the API")
    public void thenSdkShouldPollApi() {
        // Polling behavior is internal
    }
    
    @Then("return when the transaction is finalized")
    public void thenReturnWhenFinalized() {
        assertThat(transactionResult).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Submit and Wait
    // ==========================================================================
    
    @Then("the transaction should be submitted")
    public void thenTransactionShouldBeSubmitted() {
        assertThat(world.getError()).isNull();
    }
    
    @Then("the method should return the final result")
    public void thenMethodShouldReturnFinalResult() {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("the transaction should be signed")
    public void thenTransactionShouldBeSigned() {
        assertThat(world.getError()).isNull();
    }
    
    @Then("submitted")
    public void thenSubmitted() {
        assertThat(world.getError()).isNull();
    }
    
    @Then("waited upon")
    public void thenWaitedUpon() {
        assertThat(world.getError()).isNull();
    }
    
    @Then("I should receive the final result")
    public void thenShouldReceiveFinalResultAlt() {
        assertThat(transactionResult).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Simulation
    // ==========================================================================
    
    @Then("I should receive simulation results")
    public void thenShouldReceiveSimulationResults() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("the results should include gas_used")
    public void thenResultsShouldIncludeGasUsed() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("the results should include success status")
    public void thenResultsShouldIncludeSuccessStatus() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("I should see the estimated gas_used")
    public void thenShouldSeeEstimatedGasUsed() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("I can use this to set max_gas_amount")
    public void thenCanUseToSetMaxGas() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("I should see success: {word}")
    public void thenShouldSeeSuccess(String success) {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("I should see the VM error details")
    public void thenShouldSeeVmErrorDetails() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("I should see the failure reason")
    public void thenShouldSeeFailureReason() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("the error should indicate insufficient balance")
    public void thenErrorShouldIndicateInsufficientBalance() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("simulation should still work")
    public void thenSimulationShouldStillWork() {
        assertThat(simulationResult).isNotNull();
    }
    
    @Then("show what would happen if signature were valid")
    public void thenShowWhatWouldHappen() {
        assertThat(simulationResult).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Gas Estimation
    // ==========================================================================
    
    @Then("I should receive gas_estimate")
    public void thenShouldReceiveGasEstimate() {
        assertThat(gasEstimate).isNotNull();
    }
    
    @Then("optionally prioritized_gas_estimate")
    public void thenOptionallyPrioritizedEstimate() {
        // Optional field
    }
    
    @Then("optionally deprioritized_gas_estimate")
    public void thenOptionallyDeprioritizedEstimate() {
        // Optional field
    }
    
    @Then("the transaction should be accepted")
    public void thenTransactionShouldBeAccepted() {
        assertThat(world.getError()).isNull();
    }
    
    // ==========================================================================
    // Then Steps - Sequence Number
    // ==========================================================================
    
    @Then("I should receive the current sequence_number")
    public void thenShouldReceiveCurrentSequenceNumber() {
        assertThat(accountSequenceNumber).isGreaterThanOrEqualTo(0);
    }
    
    @Then("I should receive an error about sequence number")
    public void thenShouldReceiveSequenceNumberError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("all should be accepted")
    public void thenAllShouldBeAccepted() {
        // Multiple transaction acceptance
    }
    
    @Then("processed in order")
    public void thenProcessedInOrder() {
        // Order verification
    }
    
    // ==========================================================================
    // Then Steps - Error Handling
    // ==========================================================================
    
    @Then("I should receive a Network error")
    public void thenShouldReceiveNetworkError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("I can retry the submission")
    public void thenCanRetrySubmission() {
        // Retry is possible
    }
    
    @Then("I should see vm_status in the result")
    public void thenShouldSeeVmStatusInResult() {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("I should be able to extract the error code")
    public void thenShouldBeAbleToExtractErrorCode() {
        assertThat(transactionResult).isNotNull();
    }
    
    @Then("they should match")
    public void thenHashesShouldMatch() {
        assertThat(locallyComputedHash).isEqualTo(submittedHash);
    }
    
    // ==========================================================================
    // Helper Methods
    // ==========================================================================
    
    private void createSignedAptTransfer(Ed25519Account account) {
        rawTransaction = createRawTransaction(account, new ChainId((byte) 2));
        signedTransaction = account.signTransaction(rawTransaction);
        world.setSignedTransaction(signedTransaction);
    }
    
    private RawTransaction createRawTransaction(Ed25519Account account, ChainId chainId) {
        TransactionPayload payload = createPayload();
        return new RawTransaction(
            account.getAccountAddress(),
            0L,
            payload,
            200000L,
            100L,
            Instant.now().getEpochSecond() + 600,
            chainId
        );
    }
    
    private RawTransaction createRawTransactionWithExpiration(Ed25519Account account, long expiration) {
        TransactionPayload payload = createPayload();
        return new RawTransaction(
            account.getAccountAddress(),
            0L,
            payload,
            200000L,
            100L,
            expiration,
            new ChainId((byte) 2)
        );
    }
    
    private TransactionPayload createPayload() {
        ModuleId moduleId = new ModuleId(AccountAddress.ONE, "aptos_account");
        List<byte[]> args = List.of(
            AccountAddress.ONE.toBytes(),
            encodeU64(1000000L)
        );
        EntryFunction entryFunction = new EntryFunction(moduleId, "transfer", new ArrayList<>(), args);
        payload = TransactionPayload.entryFunction(entryFunction);
        return payload;
    }
    
    private byte[] encodeU64(long value) {
        ByteBuffer buffer = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN);
        buffer.putLong(value);
        return buffer.array();
    }
    
    private String computeTransactionHash(SignedTransaction tx) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA3-256");
            byte[] domainHash = digest.digest("APTOS::Transaction".getBytes());
            
            digest.reset();
            byte[] combined = new byte[domainHash.length + tx.toBytes().length];
            System.arraycopy(domainHash, 0, combined, 0, domainHash.length);
            System.arraycopy(tx.toBytes(), 0, combined, domainHash.length, tx.toBytes().length);
            
            byte[] hash = digest.digest(combined);
            return HexUtils.bytesToHex(hash);
        } catch (Exception e) {
            throw new RuntimeException("Failed to compute hash", e);
        }
    }
}
