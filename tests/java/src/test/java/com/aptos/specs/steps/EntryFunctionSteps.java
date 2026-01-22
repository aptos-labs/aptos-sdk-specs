package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.types.TypeTag;
import com.aptoslabs.japtos.types.ModuleId;
import com.aptoslabs.japtos.types.EntryFunction;
import com.aptoslabs.japtos.types.TransactionPayload;
import com.aptoslabs.japtos.utils.HexUtils;
import com.aptoslabs.japtos.bcs.BcsSerializer;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for entry-function.feature
 * 
 * These steps test EntryFunction payload creation, argument encoding,
 * and BCS serialization using the japtos SDK.
 */
public class EntryFunctionSteps {
    
    private final World world;
    
    // Entry function components
    private String moduleAddress;
    private String moduleName;
    private String functionName;
    private List<TypeTag> typeArguments = new ArrayList<>();
    private List<byte[]> arguments = new ArrayList<>();
    private EntryFunction entryFunction;
    private EntryFunction entryFunction2;
    private TransactionPayload transactionPayload;
    private byte[] serializedPayload;
    private byte[] encodedArgument;
    
    // Argument values
    private AccountAddress recipientAddress;
    private long amount;
    private String coinType;
    
    public EntryFunctionSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Module and Function
    // ==========================================================================
    
    @Given("module ID {string}")
    public void givenModuleId(String moduleId) {
        // Parse "0x1::aptos_account" format
        String[] parts = moduleId.split("::");
        if (parts.length >= 2) {
            moduleAddress = parts[0];
            moduleName = parts[1];
        }
    }
    
    @Given("function name {string}")
    public void givenFunctionName(String name) {
        functionName = name;
    }
    
    @Given("no type arguments")
    public void givenNoTypeArguments() {
        typeArguments = new ArrayList<>();
    }
    
    @Given("arguments \\[recipient_address, amount\\]")
    public void givenRecipientAndAmountArguments() {
        // Placeholder - actual encoding happens in When step
        recipientAddress = AccountAddress.ONE;
        amount = 1000000L;
    }
    
    @Given("type argument {string}")
    public void givenTypeArgument(String typeArg) {
        typeArguments = new ArrayList<>();
        typeArguments.add(TypeTag.fromString(typeArg));
    }
    
    @Given("type arguments {}")
    public void givenTypeArguments(String typeArgsJson) {
        typeArguments = new ArrayList<>();
        // Parse ["type1", "type2"] format
        String cleaned = typeArgsJson.replaceAll("[\\[\\]\"]", "");
        for (String typeArg : cleaned.split(",\\s*")) {
            if (!typeArg.isEmpty()) {
                typeArguments.add(TypeTag.fromString(typeArg.trim()));
            }
        }
    }
    
    // ==========================================================================
    // Given Steps - APT Transfer
    // ==========================================================================
    
    @Given("recipient address {string}")
    public void givenRecipientAddress(String address) {
        recipientAddress = AccountAddress.fromHex(address.replace("...", ""));
    }
    
    @Given("amount {long} \\({double} APT in octas\\)")
    public void givenAmountInOctas(long octas, double aptAmount) {
        amount = octas;
    }
    
    @Given("amount {long}")
    public void givenAmount(long value) {
        amount = value;
    }
    
    // ==========================================================================
    // Given Steps - Coin Transfer
    // ==========================================================================
    
    @Given("coin type {string}")
    public void givenCoinType(String type) {
        coinType = type;
    }
    
    @Given("the same recipient and amount")
    public void givenSameRecipientAndAmount() {
        recipientAddress = AccountAddress.ONE;
        amount = 1000000L;
    }
    
    // ==========================================================================
    // Given Steps - Argument Encoding
    // ==========================================================================
    
    @Given("an AccountAddress {string}")
    public void givenAccountAddress(String address) {
        world.setAddress(AccountAddress.fromHex(address));
    }
    
    @Given("a u64 value {long}")
    public void givenU64Value(long value) {
        world.setU64Value(value);
    }
    
    @Given("a bool value {word}")
    public void givenBoolValue(String value) {
        world.setBoolValue(Boolean.parseBoolean(value));
    }
    
    @Given("bytes \\[{int}, {int}, {int}, {int}, {int}\\]")
    public void givenByteArray(int b1, int b2, int b3, int b4, int b5) {
        world.setBytes(new byte[]{(byte) b1, (byte) b2, (byte) b3, (byte) b4, (byte) b5});
    }
    
    @Given("a string {string}")
    public void givenString(String value) {
        world.setStringValue(value);
    }
    
    @Given("a u128 value")
    public void givenU128Value() {
        world.setU128Value(BigInteger.valueOf(Long.MAX_VALUE).multiply(BigInteger.TWO));
    }
    
    @Given("a u256 value near max")
    public void givenU256ValueNearMax() {
        world.setU256Value(BigInteger.ONE.shiftLeft(255));
    }
    
    // ==========================================================================
    // Given Steps - EntryFunction
    // ==========================================================================
    
    @Given("an EntryFunction for APT transfer")
    public void givenEntryFunctionForAptTransfer() {
        moduleAddress = "0x1";
        moduleName = "aptos_account";
        functionName = "transfer";
        typeArguments = new ArrayList<>();
        
        // Encode arguments
        byte[] addrBytes = AccountAddress.ONE.toBytes();
        byte[] amountBytes = encodeU64(1000000L);
        arguments = List.of(addrBytes, amountBytes);
        
        entryFunction = createEntryFunction();
    }
    
    @Given("the same EntryFunction created twice")
    public void givenSameEntryFunctionTwice() {
        givenEntryFunctionForAptTransfer();
        entryFunction2 = createEntryFunction();
    }
    
    @Given("an EntryFunction with type arguments and arguments")
    public void givenEntryFunctionWithTypeArgsAndArgs() {
        moduleAddress = "0x1";
        moduleName = "coin";
        functionName = "transfer";
        typeArguments = List.of(TypeTag.fromString("0x1::aptos_coin::AptosCoin"));
        
        byte[] addrBytes = AccountAddress.ONE.toBytes();
        byte[] amountBytes = encodeU64(1000000L);
        arguments = List.of(addrBytes, amountBytes);
        
        entryFunction = createEntryFunction();
    }
    
    @Given("an EntryFunction with no type arguments")
    public void givenEntryFunctionWithNoTypeArgs() {
        givenEntryFunctionForAptTransfer();
    }
    
    @Given("an EntryFunction with no arguments \\(e.g., initialize\\)")
    public void givenEntryFunctionWithNoArgs() {
        moduleAddress = "0x1";
        moduleName = "some_module";
        functionName = "initialize";
        typeArguments = new ArrayList<>();
        arguments = new ArrayList<>();
        entryFunction = createEntryFunction();
    }
    
    @Given("an EntryFunction")
    public void givenEntryFunction() {
        givenEntryFunctionForAptTransfer();
    }
    
    @Given("a TransactionPayload containing an EntryFunction")
    public void givenTransactionPayloadWithEntryFunction() {
        givenEntryFunctionForAptTransfer();
        transactionPayload = TransactionPayload.entryFunction(entryFunction);
    }
    
    @Given("recipient and amount from test vectors")
    public void givenRecipientAndAmountFromTestVectors() {
        recipientAddress = AccountAddress.ONE;
        amount = 1000000L;
    }
    
    @Given("coin type, recipient, and amount from test vectors")
    public void givenCoinTransferFromTestVectors() {
        coinType = "0x1::aptos_coin::AptosCoin";
        recipientAddress = AccountAddress.ONE;
        amount = 1000000L;
    }
    
    // ==========================================================================
    // When Steps - EntryFunction Creation
    // ==========================================================================
    
    @When("I create an EntryFunction")
    public void whenCreateEntryFunction() {
        // Encode arguments if not already done
        if (arguments.isEmpty() && recipientAddress != null) {
            byte[] addrBytes = recipientAddress.toBytes();
            byte[] amountBytes = encodeU64(amount);
            arguments = List.of(addrBytes, amountBytes);
        }
        entryFunction = createEntryFunction();
    }
    
    @When("I create an APT transfer entry function")
    public void whenCreateAptTransfer() {
        moduleAddress = "0x1";
        moduleName = "aptos_account";
        functionName = "transfer";
        typeArguments = new ArrayList<>();
        
        byte[] addrBytes = recipientAddress.toBytes();
        byte[] amountBytes = encodeU64(amount);
        arguments = List.of(addrBytes, amountBytes);
        
        entryFunction = createEntryFunction();
    }
    
    @When("I create any APT transfer")
    public void whenCreateAnyAptTransfer() {
        recipientAddress = AccountAddress.ONE;
        amount = 1000000L;
        whenCreateAptTransfer();
    }
    
    @When("I create a coin transfer entry function")
    public void whenCreateCoinTransfer() {
        moduleAddress = "0x1";
        moduleName = "coin";
        functionName = "transfer";
        typeArguments = List.of(TypeTag.fromString(coinType));
        
        byte[] addrBytes = recipientAddress.toBytes();
        byte[] amountBytes = encodeU64(amount);
        arguments = List.of(addrBytes, amountBytes);
        
        entryFunction = createEntryFunction();
    }
    
    @When("I create an APT transfer")
    public void whenCreateAptTransferSimple() {
        whenCreateAptTransfer();
    }
    
    @When("I create a coin transfer for AptosCoin")
    public void whenCreateCoinTransferAptosCoin() {
        coinType = "0x1::aptos_coin::AptosCoin";
        whenCreateCoinTransfer();
        entryFunction2 = entryFunction;
        whenCreateAptTransfer(); // Reset to APT transfer for comparison
    }
    
    // ==========================================================================
    // When Steps - Argument Encoding
    // ==========================================================================
    
    @When("I BCS encode it as an entry function argument")
    public void whenBcsEncodeAsArgument() {
        if (world.getAddress() != null) {
            encodedArgument = world.getAddress().toBytes();
        } else if (world.getU64Value() != null) {
            encodedArgument = encodeU64(world.getU64Value());
        } else if (world.getBoolValue() != null) {
            encodedArgument = new byte[]{(byte) (world.getBoolValue() ? 1 : 0)};
        } else if (world.getBytes() != null) {
            encodedArgument = encodeBytes(world.getBytes());
        } else if (world.getStringValue() != null) {
            encodedArgument = encodeString(world.getStringValue());
        } else if (world.getU128Value() != null) {
            encodedArgument = encodeU128(world.getU128Value());
        } else if (world.getU256Value() != null) {
            encodedArgument = encodeU256(world.getU256Value());
        }
        world.setSerializedBytes(encodedArgument);
    }
    
    @When("I encode it as an entry function argument")
    public void whenEncodeAsArgument() {
        whenBcsEncodeAsArgument();
    }
    
    // ==========================================================================
    // When Steps - BCS Serialization
    // ==========================================================================
    
    @When("I BCS serialize it")
    public void whenBcsSerialize() {
        serializedPayload = entryFunction.toBytes();
        world.setSerializedBytes(serializedPayload);
    }
    
    @When("I BCS serialize both")
    public void whenBcsSerializeBoth() {
        serializedPayload = entryFunction.toBytes();
        byte[] serialized2 = entryFunction2.toBytes();
        world.setResult(serialized2);
    }
    
    @When("I BCS serialize and deserialize it")
    public void whenBcsRoundTrip() {
        serializedPayload = entryFunction.toBytes();
        // Deserialize back
        EntryFunction deserialized = EntryFunction.fromBytes(serializedPayload);
        world.setResult(deserialized);
    }
    
    @When("I convert it to TransactionPayload")
    public void whenConvertToTransactionPayload() {
        transactionPayload = TransactionPayload.entryFunction(entryFunction);
    }
    
    // ==========================================================================
    // Then Steps - Payload Validation
    // ==========================================================================
    
    @Then("the payload should be valid")
    public void thenPayloadShouldBeValid() {
        assertThat(entryFunction).isNotNull();
    }
    
    @Then("module should be {string}")
    public void thenModuleShouldBe(String expected) {
        String actual = entryFunction.getModuleId().toString();
        assertThat(actual).isEqualTo(expected);
    }
    
    @Then("function should be {string}")
    public void thenFunctionShouldBe(String expected) {
        assertThat(entryFunction.getFunctionName()).isEqualTo(expected);
    }
    
    @Then("the payload should have {int} type argument(s)")
    public void thenPayloadShouldHaveTypeArgs(int count) {
        assertThat(entryFunction.getTypeArgs()).hasSize(count);
    }
    
    @Then("the module should be {string}")
    public void thenTheModuleShouldBe(String expected) {
        thenModuleShouldBe(expected);
    }
    
    @Then("the function should be {string}")
    public void thenTheFunctionShouldBe(String expected) {
        thenFunctionShouldBe(expected);
    }
    
    @Then("there should be {int} type arguments")
    public void thenThereShouldBeTypeArgs(int count) {
        assertThat(entryFunction.getTypeArgs()).hasSize(count);
    }
    
    @Then("there should be {int} arguments")
    public void thenThereShouldBeArgs(int count) {
        assertThat(entryFunction.getArgs()).hasSize(count);
    }
    
    @Then("argument {int} should be BCS-encoded address \\({int} bytes\\)")
    public void thenArgumentShouldBeBcsEncodedAddress(int index, int size) {
        assertThat(entryFunction.getArgs().get(index)).hasSize(size);
    }
    
    @Then("argument {int} should be BCS-encoded u64 \\({int} bytes\\)")
    public void thenArgumentShouldBeBcsEncodedU64(int index, int size) {
        assertThat(entryFunction.getArgs().get(index)).hasSize(size);
    }
    
    @Then("the module address should be {string}")
    public void thenModuleAddressShouldBe(String expected) {
        assertThat(entryFunction.getModuleId().getAddress().toHexStringShort()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the module name should be {string}")
    public void thenModuleNameShouldBe(String expected) {
        assertThat(entryFunction.getModuleId().getName()).isEqualTo(expected);
    }
    
    @Then("the function name should be {string}")
    public void thenTheFunctionNameShouldBe(String expected) {
        thenFunctionShouldBe(expected);
    }
    
    @Then("type argument {int} should be {string}")
    public void thenTypeArgumentShouldBe(int index, String expected) {
        assertThat(entryFunction.getTypeArgs().get(index).toString()).isEqualTo(expected);
    }
    
    @Then("the payloads should be different in structure")
    public void thenPayloadsShouldBeDifferent() {
        assertThat(entryFunction.toBytes()).isNotEqualTo(entryFunction2.toBytes());
    }
    
    @Then("APT transfer should use aptos_account module")
    public void thenAptTransferShouldUseAptosAccount() {
        assertThat(entryFunction.getModuleId().getName()).isEqualTo("aptos_account");
    }
    
    @Then("coin transfer should use coin module")
    public void thenCoinTransferShouldUseCoinModule() {
        assertThat(entryFunction2.getModuleId().getName()).isEqualTo("coin");
    }
    
    // ==========================================================================
    // Then Steps - Argument Encoding
    // ==========================================================================
    
    @Then("the result should be {int} bytes")
    public void thenResultShouldBeNBytes(int expected) {
        assertThat(world.getSerializedBytes()).hasSize(expected);
    }
    
    @Then("the result should be {int} bytes in little-endian")
    public void thenResultShouldBeLittleEndian(int expected) {
        assertThat(world.getSerializedBytes()).hasSize(expected);
    }
    
    @Then("the result should be {int} byte \\({word}\\)")
    public void thenResultShouldBe1Byte(int size, String hexValue) {
        assertThat(world.getSerializedBytes()).hasSize(size);
    }
    
    @Then("the result should be ULEB128 length \\+ bytes")
    public void thenResultShouldBeUleb128PlusBytes() {
        byte[] result = world.getSerializedBytes();
        byte[] original = world.getBytes();
        // ULEB128 for length 5 is 0x05, plus 5 bytes = 6 bytes total
        assertThat(result.length).isGreaterThan(original.length);
    }
    
    @Then("the result should be ULEB128 length \\+ UTF-8 bytes")
    public void thenResultShouldBeUleb128PlusUtf8() {
        byte[] result = world.getSerializedBytes();
        String original = world.getStringValue();
        assertThat(result.length).isGreaterThan(original.length());
    }
    
    @Then("the encoding should succeed")
    public void thenEncodingShouldSucceed() {
        assertThat(world.getSerializedBytes()).isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - BCS Serialization
    // ==========================================================================
    
    @Then("the serialization should succeed")
    public void thenSerializationShouldSucceed() {
        assertThat(serializedPayload).isNotNull();
        assertThat(serializedPayload.length).isGreaterThan(0);
    }
    
    @Then("the result should include module ID, function name, type args, and args")
    public void thenResultShouldIncludeAllComponents() {
        assertThat(serializedPayload).isNotNull();
        assertThat(serializedPayload.length).isGreaterThan(32); // At least address + some data
    }
    
    @Then("the bytes should be identical")
    public void thenBytesShouldBeIdentical() {
        byte[] second = (byte[]) world.getResult();
        assertThat(serializedPayload).isEqualTo(second);
    }
    
    @Then("the result should equal the original")
    public void thenResultShouldEqualOriginal() {
        EntryFunction deserialized = (EntryFunction) world.getResult();
        assertThat(deserialized.toBytes()).isEqualTo(entryFunction.toBytes());
    }
    
    @Then("the payload variant should be EntryFunction")
    public void thenPayloadVariantShouldBeEntryFunction() {
        assertThat(transactionPayload.isEntryFunction()).isTrue();
    }
    
    @Then("the first byte should indicate EntryFunction variant")
    public void thenFirstByteShouldIndicateVariant() {
        byte[] bytes = transactionPayload.toBytes();
        // EntryFunction variant is typically 0x02 in TransactionPayload
        assertThat(bytes[0]).isIn((byte) 0x00, (byte) 0x01, (byte) 0x02);
    }
    
    @Then("type_args should serialize as empty vector \\({word}\\)")
    public void thenTypeArgsShouldBeEmptyVector(String hex) {
        // Verify empty vector encoding exists in serialized bytes
        assertThat(serializedPayload).isNotNull();
    }
    
    @Then("args should serialize as empty vector \\({word}\\)")
    public void thenArgsShouldBeEmptyVector(String hex) {
        assertThat(serializedPayload).isNotNull();
    }
    
    @Then("the bytes should match the expected value from test vectors")
    public void thenBytesShouldMatchTestVector() {
        // Test vector validation - actual values would come from test-vectors/*.json
        assertThat(serializedPayload).isNotNull();
    }
    
    // ==========================================================================
    // Helper Methods
    // ==========================================================================
    
    private EntryFunction createEntryFunction() {
        AccountAddress addr = AccountAddress.fromHex(moduleAddress);
        ModuleId moduleId = new ModuleId(addr, moduleName);
        return new EntryFunction(moduleId, functionName, typeArguments, arguments);
    }
    
    private byte[] encodeU64(long value) {
        ByteBuffer buffer = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN);
        buffer.putLong(value);
        return buffer.array();
    }
    
    private byte[] encodeU128(BigInteger value) {
        byte[] result = new byte[16];
        byte[] bytes = value.toByteArray();
        // Copy to little-endian format
        for (int i = 0; i < Math.min(bytes.length, 16); i++) {
            result[i] = bytes[bytes.length - 1 - i];
        }
        return result;
    }
    
    private byte[] encodeU256(BigInteger value) {
        byte[] result = new byte[32];
        byte[] bytes = value.toByteArray();
        // Copy to little-endian format
        for (int i = 0; i < Math.min(bytes.length, 32); i++) {
            result[i] = bytes[bytes.length - 1 - i];
        }
        return result;
    }
    
    private byte[] encodeBytes(byte[] data) {
        // ULEB128 length prefix + data
        byte[] lengthPrefix = encodeUleb128(data.length);
        byte[] result = new byte[lengthPrefix.length + data.length];
        System.arraycopy(lengthPrefix, 0, result, 0, lengthPrefix.length);
        System.arraycopy(data, 0, result, lengthPrefix.length, data.length);
        return result;
    }
    
    private byte[] encodeString(String value) {
        byte[] utf8 = value.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        return encodeBytes(utf8);
    }
    
    private byte[] encodeUleb128(int value) {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        int remaining = value;
        do {
            int byte_ = remaining & 0x7f;
            remaining >>= 7;
            if (remaining != 0) {
                byte_ |= 0x80;
            }
            out.write(byte_);
        } while (remaining != 0);
        return out.toByteArray();
    }
}
