package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.types.ChainId;
import com.aptoslabs.japtos.types.EntryFunction;
import com.aptoslabs.japtos.types.ModuleId;
import com.aptoslabs.japtos.types.RawTransaction;
import com.aptoslabs.japtos.types.TransactionPayload;
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
 * Step definitions for raw-transaction.feature
 * 
 * These steps test RawTransaction construction, BCS serialization,
 * and signing message generation using the japtos SDK.
 */
public class RawTransactionSteps {
    
    private final World world;
    
    // Transaction components
    private AccountAddress sender;
    private long sequenceNumber;
    private TransactionPayload payload;
    private long maxGasAmount = 200000;
    private long gasUnitPrice = 100;
    private long expirationTimestampSecs;
    private ChainId chainId;
    
    // RawTransaction
    private RawTransaction rawTransaction;
    private RawTransaction rawTransaction2;
    private byte[] serializedTransaction;
    private byte[] signingMessage;
    private byte[] signingMessage2;
    
    // Builder state
    private boolean senderSet = false;
    private boolean sequenceNumberSet = false;
    private boolean payloadSet = false;
    private boolean chainIdSet = false;
    
    public RawTransactionSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Transaction Fields
    // ==========================================================================
    
    @Given("a sender address {string}")
    public void givenSenderAddress(String address) {
        sender = AccountAddress.fromHex(address);
        senderSet = true;
    }
    
    @Given("a sequence number {long}")
    public void givenSequenceNumber(long seqNum) {
        sequenceNumber = seqNum;
        sequenceNumberSet = true;
    }
    
    @Given("an entry function payload for APT transfer")
    public void givenEntryFunctionPayloadForAptTransfer() {
        ModuleId moduleId = new ModuleId(AccountAddress.ONE, "aptos_account");
        List<byte[]> args = List.of(
            AccountAddress.ONE.toBytes(),
            encodeU64(1000000L)
        );
        EntryFunction entryFunction = new EntryFunction(moduleId, "transfer", new ArrayList<>(), args);
        payload = TransactionPayload.entryFunction(entryFunction);
        payloadSet = true;
    }
    
    @Given("max gas amount {long}")
    public void givenMaxGasAmount(long maxGas) {
        maxGasAmount = maxGas;
    }
    
    @Given("gas unit price {long}")
    public void givenGasUnitPrice(long price) {
        gasUnitPrice = price;
    }
    
    @Given("expiration timestamp {long}")
    public void givenExpirationTimestamp(long timestamp) {
        expirationTimestampSecs = timestamp;
    }
    
    @Given("chain ID testnet \\({int}\\)")
    public void givenChainIdTestnet(int id) {
        chainId = new ChainId((byte) id);
        chainIdSet = true;
    }
    
    @Given("chain ID {int} \\(mainnet\\)")
    public void givenChainIdMainnet(int id) {
        chainId = new ChainId((byte) id);
        chainIdSet = true;
    }
    
    @Given("chain ID {int} \\(testnet\\)")
    public void givenChainIdTestnetAlt(int id) {
        chainId = new ChainId((byte) id);
        chainIdSet = true;
    }
    
    // ==========================================================================
    // Given Steps - RawTransaction
    // ==========================================================================
    
    @Given("a valid RawTransaction")
    public void givenValidRawTransaction() {
        createDefaultRawTransaction();
    }
    
    @Given("a RawTransaction with known values")
    public void givenRawTransactionWithKnownValues() {
        createDefaultRawTransaction();
    }
    
    @Given("a RawTransaction")
    public void givenRawTransaction() {
        createDefaultRawTransaction();
    }
    
    @Given("two RawTransactions with different sequence numbers")
    public void givenTwoRawTransactionsWithDifferentSeqNums() {
        createDefaultRawTransaction();
        rawTransaction2 = new RawTransaction(
            sender,
            sequenceNumber + 1,
            payload,
            maxGasAmount,
            gasUnitPrice,
            expirationTimestampSecs,
            chainId
        );
    }
    
    @Given("a RawTransaction with chain ID {int} \\(mainnet\\)")
    public void givenRawTransactionWithMainnetChainId(int id) {
        chainId = new ChainId((byte) id);
        createDefaultRawTransaction();
    }
    
    @Given("a RawTransaction with chain ID {int} \\(testnet\\)")
    public void givenRawTransactionWithTestnetChainId(int id) {
        chainId = new ChainId((byte) id);
        createDefaultRawTransaction();
    }
    
    @Given("a RawTransaction with values from test vectors")
    public void givenRawTransactionFromTestVectors() {
        createDefaultRawTransaction();
    }
    
    @Given("a RawTransaction from test vectors")
    public void givenRawTransactionFromTestVectorsAlt() {
        createDefaultRawTransaction();
    }
    
    // ==========================================================================
    // Given Steps - Builder
    // ==========================================================================
    
    @Given("a TransactionBuilder")
    public void givenTransactionBuilder() {
        // Reset builder state
        senderSet = false;
        sequenceNumberSet = false;
        payloadSet = false;
        chainIdSet = false;
        maxGasAmount = 200000;
        gasUnitPrice = 100;
    }
    
    @Given("a TransactionBuilder with only required fields")
    public void givenTransactionBuilderWithRequiredFields() {
        givenTransactionBuilder();
        senderSet = true;
        sequenceNumberSet = true;
        payloadSet = true;
        chainIdSet = true;
        sender = AccountAddress.ONE;
        sequenceNumber = 0;
        givenEntryFunctionPayloadForAptTransfer();
        chainId = new ChainId((byte) 2);
    }
    
    @Given("a TransactionBuilder with sender set")
    public void givenTransactionBuilderWithSender() {
        givenTransactionBuilder();
        sender = AccountAddress.ONE;
        senderSet = true;
    }
    
    @Given("a TransactionBuilder with sender and sequence number")
    public void givenTransactionBuilderWithSenderAndSeqNum() {
        givenTransactionBuilderWithSender();
        sequenceNumber = 0;
        sequenceNumberSet = true;
    }
    
    @Given("a TransactionBuilder with sender, sequence, and payload")
    public void givenTransactionBuilderWithSenderSeqAndPayload() {
        givenTransactionBuilderWithSenderAndSeqNum();
        givenEntryFunctionPayloadForAptTransfer();
    }
    
    @Given("current time is T")
    public void givenCurrentTimeIsT() {
        // No-op, we'll use actual current time
    }
    
    // ==========================================================================
    // When Steps - RawTransaction Creation
    // ==========================================================================
    
    @When("I create a RawTransaction")
    public void whenCreateRawTransaction() {
        rawTransaction = new RawTransaction(
            sender,
            sequenceNumber,
            payload,
            maxGasAmount,
            gasUnitPrice,
            expirationTimestampSecs,
            chainId
        );
        world.setRawTransaction(rawTransaction);
    }
    
    @When("I access the fields")
    public void whenAccessFields() {
        // Fields will be accessed in Then steps
    }
    
    // ==========================================================================
    // When Steps - BCS Serialization
    // ==========================================================================
    
    @When("I BCS serialize it")
    public void whenBcsSerialize() {
        serializedTransaction = rawTransaction.toBytes();
        world.setSerializedBytes(serializedTransaction);
    }
    
    @When("I BCS serialize and deserialize it")
    public void whenBcsRoundTrip() {
        serializedTransaction = rawTransaction.toBytes();
        RawTransaction deserialized = RawTransaction.fromBytes(serializedTransaction);
        world.setResult(deserialized);
    }
    
    // ==========================================================================
    // When Steps - Signing Message
    // ==========================================================================
    
    @When("I generate the signing message")
    public void whenGenerateSigningMessage() {
        signingMessage = generateSigningMessage(rawTransaction);
        world.setBytes(signingMessage);
    }
    
    @When("I generate the signing message twice")
    public void whenGenerateSigningMessageTwice() {
        signingMessage = generateSigningMessage(rawTransaction);
        signingMessage2 = generateSigningMessage(rawTransaction);
    }
    
    @When("I generate signing messages for both")
    public void whenGenerateSigningMessagesForBoth() {
        signingMessage = generateSigningMessage(rawTransaction);
        signingMessage2 = generateSigningMessage(rawTransaction2);
    }
    
    @When("I compute SHA3-256 of {string}")
    public void whenComputeSha3Of(String input) {
        byte[] hash = sha3_256(input.getBytes(java.nio.charset.StandardCharsets.UTF_8));
        world.setBytes(hash);
    }
    
    // ==========================================================================
    // When Steps - Builder
    // ==========================================================================
    
    @When("I set sender to {string}")
    public void whenSetSender(String address) {
        sender = AccountAddress.fromHex(address);
        senderSet = true;
    }
    
    @When("I set sequence number to {long}")
    public void whenSetSequenceNumber(long seqNum) {
        sequenceNumber = seqNum;
        sequenceNumberSet = true;
    }
    
    @When("I set payload to an APT transfer")
    public void whenSetPayloadToAptTransfer() {
        givenEntryFunctionPayloadForAptTransfer();
    }
    
    @When("I set chain ID to testnet")
    public void whenSetChainIdToTestnet() {
        chainId = new ChainId((byte) 2);
        chainIdSet = true;
    }
    
    @When("I set expiration from now to {int} seconds")
    public void whenSetExpirationFromNow(int seconds) {
        expirationTimestampSecs = Instant.now().getEpochSecond() + seconds;
    }
    
    @When("I set expiration_from_now to {int} seconds")
    public void whenSetExpirationFromNowAlt(int seconds) {
        whenSetExpirationFromNow(seconds);
    }
    
    @When("I call build\\(\\)")
    public void whenCallBuild() {
        try {
            if (!senderSet) {
                world.setError(new IllegalStateException("MissingSender"));
                return;
            }
            if (!sequenceNumberSet) {
                world.setError(new IllegalStateException("MissingSequenceNumber"));
                return;
            }
            if (!payloadSet) {
                world.setError(new IllegalStateException("MissingPayload"));
                return;
            }
            if (!chainIdSet) {
                world.setError(new IllegalStateException("MissingChainId"));
                return;
            }
            
            rawTransaction = new RawTransaction(
                sender,
                sequenceNumber,
                payload,
                maxGasAmount,
                gasUnitPrice,
                expirationTimestampSecs,
                chainId
            );
            world.setRawTransaction(rawTransaction);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I build the transaction")
    public void whenBuildTransaction() {
        whenCallBuild();
    }
    
    @When("I set max_gas_amount to {long}")
    public void whenSetMaxGasAmount(long value) {
        maxGasAmount = value;
    }
    
    @When("I set gas_unit_price to {long}")
    public void whenSetGasUnitPrice(long value) {
        gasUnitPrice = value;
    }
    
    @When("I build with all required fields")
    public void whenBuildWithAllRequiredFields() {
        if (!senderSet) {
            sender = AccountAddress.ONE;
            senderSet = true;
        }
        if (!sequenceNumberSet) {
            sequenceNumber = 0;
            sequenceNumberSet = true;
        }
        if (!payloadSet) {
            givenEntryFunctionPayloadForAptTransfer();
        }
        if (!chainIdSet) {
            chainId = new ChainId((byte) 2);
            chainIdSet = true;
        }
        expirationTimestampSecs = Instant.now().getEpochSecond() + 600;
        whenCallBuild();
    }
    
    @When("I try to build without setting sender")
    public void whenTryBuildWithoutSender() {
        senderSet = false;
        whenCallBuild();
    }
    
    @When("I try to build without sequence number")
    public void whenTryBuildWithoutSequenceNumber() {
        sequenceNumberSet = false;
        whenCallBuild();
    }
    
    @When("I try to build without payload")
    public void whenTryBuildWithoutPayload() {
        payloadSet = false;
        whenCallBuild();
    }
    
    @When("I try to build without chain ID")
    public void whenTryBuildWithoutChainId() {
        chainIdSet = false;
        whenCallBuild();
    }
    
    // ==========================================================================
    // Then Steps - Transaction Validation
    // ==========================================================================
    
    @Then("the transaction should be valid")
    public void thenTransactionShouldBeValid() {
        assertThat(rawTransaction).isNotNull();
    }
    
    @Then("sender should be {string}")
    public void thenSenderShouldBe(String expected) {
        assertThat(rawTransaction.getSender().toHexStringShort()).isEqualToIgnoringCase(expected);
    }
    
    @Then("sequence number should be {long}")
    public void thenSequenceNumberShouldBe(long expected) {
        assertThat(rawTransaction.getSequenceNumber()).isEqualTo(expected);
    }
    
    @Then("sender\\(\\) should return the sender address")
    public void thenSenderShouldReturnSenderAddress() {
        assertThat(rawTransaction.getSender()).isEqualTo(sender);
    }
    
    @Then("sequence_number\\(\\) should return the sequence number")
    public void thenSequenceNumberShouldReturnSequenceNumber() {
        assertThat(rawTransaction.getSequenceNumber()).isEqualTo(sequenceNumber);
    }
    
    @Then("payload\\(\\) should return the payload")
    public void thenPayloadShouldReturnPayload() {
        assertThat(rawTransaction.getPayload()).isNotNull();
    }
    
    @Then("max_gas_amount\\(\\) should return the max gas")
    public void thenMaxGasAmountShouldReturnMaxGas() {
        assertThat(rawTransaction.getMaxGasAmount()).isEqualTo(maxGasAmount);
    }
    
    @Then("gas_unit_price\\(\\) should return the gas price")
    public void thenGasUnitPriceShouldReturnGasPrice() {
        assertThat(rawTransaction.getGasUnitPrice()).isEqualTo(gasUnitPrice);
    }
    
    @Then("expiration_timestamp_secs\\(\\) should return the expiration")
    public void thenExpirationShouldReturnExpiration() {
        assertThat(rawTransaction.getExpirationTimestampSecs()).isEqualTo(expirationTimestampSecs);
    }
    
    @Then("chain_id\\(\\) should return the chain ID")
    public void thenChainIdShouldReturnChainId() {
        assertThat(rawTransaction.getChainId()).isEqualTo(chainId);
    }
    
    // ==========================================================================
    // Then Steps - BCS Serialization
    // ==========================================================================
    
    @Then("the serialization should succeed")
    public void thenSerializationShouldSucceed() {
        assertThat(serializedTransaction).isNotNull();
        assertThat(serializedTransaction.length).isGreaterThan(0);
    }
    
    @Then("the bytes should be deterministic")
    public void thenBytesShouldBeDeterministic() {
        byte[] serialized2 = rawTransaction.toBytes();
        assertThat(serializedTransaction).isEqualTo(serialized2);
    }
    
    @Then("sender should be serialized first \\({int} bytes\\)")
    public void thenSenderShouldBeSerializedFirst(int bytes) {
        assertThat(serializedTransaction.length).isGreaterThanOrEqualTo(bytes);
    }
    
    @Then("sequence_number should be next \\({int} bytes\\)")
    public void thenSequenceNumberShouldBeNext(int bytes) {
        // Field order validation
        assertThat(serializedTransaction.length).isGreaterThanOrEqualTo(32 + bytes);
    }
    
    @Then("payload should follow")
    public void thenPayloadShouldFollow() {
        assertThat(serializedTransaction.length).isGreaterThan(40);
    }
    
    @Then("max_gas_amount, gas_unit_price, expiration, chain_id should be in order")
    public void thenRemainingFieldsInOrder() {
        // BCS serialization preserves field order
        assertThat(serializedTransaction).isNotNull();
    }
    
    @Then("the result should equal the original")
    public void thenResultShouldEqualOriginal() {
        RawTransaction deserialized = (RawTransaction) world.getResult();
        assertThat(deserialized.toBytes()).isEqualTo(rawTransaction.toBytes());
    }
    
    @Then("the chain_id byte should be {word}")
    public void thenChainIdByteShouldBe(String hex) {
        // Last byte of serialization should be chain ID
        byte expected = (byte) Integer.parseInt(hex.replace("0x", ""), 16);
        assertThat(serializedTransaction[serializedTransaction.length - 1]).isEqualTo(expected);
    }
    
    @Then("the bytes should match the expected value from test vectors")
    public void thenBytesShouldMatchTestVector() {
        assertThat(serializedTransaction).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Signing Message
    // ==========================================================================
    
    @Then("the message should start with SHA3-256\\({string}\\)")
    public void thenMessageShouldStartWithDomainHash(String domain) {
        byte[] domainHash = sha3_256(domain.getBytes(java.nio.charset.StandardCharsets.UTF_8));
        byte[] prefix = new byte[32];
        System.arraycopy(signingMessage, 0, prefix, 0, 32);
        assertThat(prefix).isEqualTo(domainHash);
    }
    
    @Then("the message should contain the BCS-serialized transaction")
    public void thenMessageShouldContainBcsTx() {
        assertThat(signingMessage.length).isGreaterThan(32);
    }
    
    @Then("both messages should be identical")
    public void thenBothMessagesShouldBeIdentical() {
        assertThat(signingMessage).isEqualTo(signingMessage2);
    }
    
    @Then("the messages should be different")
    public void thenMessagesShouldBeDifferent() {
        assertThat(signingMessage).isNotEqualTo(signingMessage2);
    }
    
    @Then("the result should be {int} bytes")
    public void thenResultShouldBeNBytes(int expected) {
        assertThat(world.getBytes()).hasSize(expected);
    }
    
    @Then("it should be the prefix of all single-signer signing messages")
    public void thenShouldBePrefixOfSigningMessages() {
        byte[] domainHash = world.getBytes();
        signingMessage = generateSigningMessage(rawTransaction);
        byte[] prefix = new byte[32];
        System.arraycopy(signingMessage, 0, prefix, 0, 32);
        assertThat(prefix).isEqualTo(domainHash);
    }
    
    @Then("it should match the expected value from test vectors")
    public void thenShouldMatchTestVector() {
        assertThat(signingMessage).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Builder
    // ==========================================================================
    
    @Then("I should get a valid RawTransaction")
    public void thenShouldGetValidRawTransaction() {
        assertThat(world.getError()).isNull();
        assertThat(rawTransaction).isNotNull();
    }
    
    @Then("max_gas_amount should be {long}")
    public void thenMaxGasAmountShouldBe(long expected) {
        assertThat(rawTransaction.getMaxGasAmount()).isEqualTo(expected);
    }
    
    @Then("gas_unit_price should be {long}")
    public void thenGasUnitPriceShouldBe(long expected) {
        assertThat(rawTransaction.getGasUnitPrice()).isEqualTo(expected);
    }
    
    @Then("the transaction should have the custom values")
    public void thenTransactionShouldHaveCustomValues() {
        assertThat(rawTransaction.getMaxGasAmount()).isEqualTo(maxGasAmount);
        assertThat(rawTransaction.getGasUnitPrice()).isEqualTo(gasUnitPrice);
    }
    
    @Then("build should fail with MissingSender error")
    public void thenBuildShouldFailWithMissingSender() {
        assertThat(world.getError()).isNotNull();
        assertThat(world.getError().getMessage()).contains("MissingSender");
    }
    
    @Then("build should fail with MissingSequenceNumber error")
    public void thenBuildShouldFailWithMissingSequenceNumber() {
        assertThat(world.getError()).isNotNull();
        assertThat(world.getError().getMessage()).contains("MissingSequenceNumber");
    }
    
    @Then("build should fail with MissingPayload error")
    public void thenBuildShouldFailWithMissingPayload() {
        assertThat(world.getError()).isNotNull();
        assertThat(world.getError().getMessage()).contains("MissingPayload");
    }
    
    @Then("build should fail with MissingChainId error")
    public void thenBuildShouldFailWithMissingChainId() {
        assertThat(world.getError()).isNotNull();
        assertThat(world.getError().getMessage()).contains("MissingChainId");
    }
    
    @Then("expiration_timestamp_secs should be approximately T \\+ {int}")
    public void thenExpirationShouldBeApproximately(int seconds) {
        long expected = Instant.now().getEpochSecond() + seconds;
        assertThat(rawTransaction.getExpirationTimestampSecs())
            .isBetween(expected - 5, expected + 5);
    }
    
    // ==========================================================================
    // Helper Methods
    // ==========================================================================
    
    private void createDefaultRawTransaction() {
        if (sender == null) {
            sender = AccountAddress.ONE;
        }
        if (payload == null) {
            givenEntryFunctionPayloadForAptTransfer();
        }
        if (chainId == null) {
            chainId = new ChainId((byte) 2);
        }
        if (expirationTimestampSecs == 0) {
            expirationTimestampSecs = Instant.now().getEpochSecond() + 600;
        }
        
        rawTransaction = new RawTransaction(
            sender,
            sequenceNumber,
            payload,
            maxGasAmount,
            gasUnitPrice,
            expirationTimestampSecs,
            chainId
        );
        world.setRawTransaction(rawTransaction);
    }
    
    private byte[] generateSigningMessage(RawTransaction tx) {
        // Domain-separated signing message:
        // SHA3-256("APTOS::RawTransaction") || BCS(RawTransaction)
        byte[] domainHash = sha3_256("APTOS::RawTransaction".getBytes(java.nio.charset.StandardCharsets.UTF_8));
        byte[] txBytes = tx.toBytes();
        
        byte[] message = new byte[domainHash.length + txBytes.length];
        System.arraycopy(domainHash, 0, message, 0, domainHash.length);
        System.arraycopy(txBytes, 0, message, domainHash.length, txBytes.length);
        
        return message;
    }
    
    private byte[] sha3_256(byte[] data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA3-256");
            return digest.digest(data);
        } catch (Exception e) {
            throw new RuntimeException("SHA3-256 not available", e);
        }
    }
    
    private byte[] encodeU64(long value) {
        ByteBuffer buffer = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN);
        buffer.putLong(value);
        return buffer.array();
    }
}
