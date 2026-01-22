package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.utils.HexUtils;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.util.Arrays;
import java.util.List;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for address.feature
 * 
 * These steps test AccountAddress parsing, formatting, comparison, and BCS serialization
 * using the japtos SDK.
 */
public class AddressSteps {
    
    private final World world;
    
    public AddressSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps
    // ==========================================================================
    
    @Given("a hex string {string}")
    public void givenHexString(String hexString) {
        world.setHexString(hexString);
    }
    
    @Given("an AccountAddress with value {int}")
    public void givenAccountAddressWithValue(int value) {
        try {
            // Create address from hex representation of the value
            String hex = String.format("0x%x", value);
            AccountAddress addr = AccountAddress.fromHex(hex);
            world.setAddress(addr);
            world.setBytes(addr.toBytes());
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @Given("an AccountAddress from hex {string}")
    public void givenAccountAddressFromHex(String hexString) {
        try {
            AccountAddress addr = AccountAddress.fromHex(hexString);
            world.setAddress(addr);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @Given("another AccountAddress from hex {string}")
    public void givenAnotherAccountAddressFromHex(String hexString) {
        try {
            AccountAddress addr = AccountAddress.fromHex(hexString);
            world.setAddress2(addr);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @Given("the ZERO address constant")
    public void givenZeroAddressConstant() {
        world.setAddress(AccountAddress.ZERO);
    }
    
    @Given("the ONE address constant")
    public void givenOneAddressConstant() {
        world.setAddress(AccountAddress.ONE);
    }
    
    @Given("the THREE address constant")
    public void givenThreeAddressConstant() {
        world.setAddress(AccountAddress.THREE);
    }
    
    @Given("the FOUR address constant")
    public void givenFourAddressConstant() {
        world.setAddress(AccountAddress.FOUR);
    }
    
    @Given("{int} bytes with value {int} in the last byte")
    public void givenBytesWithValueInLastByte(int numBytes, int value) {
        byte[] bytes = new byte[numBytes];
        bytes[numBytes - 1] = (byte) value;
        world.setBytes(bytes);
    }
    
    @Given("test vectors from addresses.json")
    public void givenAddressTestVectors() throws Exception {
        List<Vectors.AddressVector> vectors = Vectors.getAddressParsingVectors();
        world.getTestVectors().put("address_parsing", vectors);
    }
    
    // ==========================================================================
    // When Steps
    // ==========================================================================
    
    @When("I parse it as an AccountAddress")
    public void whenParseAsAccountAddress() {
        try {
            AccountAddress addr = AccountAddress.fromHex(world.getHexString());
            world.setAddress(addr);
            world.setBytes(addr.toBytes());
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I format it as full hex")
    public void whenFormatAsFullHex() {
        AccountAddress addr = (AccountAddress) world.getAddress();
        world.setResult(addr.toHexStringLong());
    }
    
    @When("I format it as short string")
    public void whenFormatAsShortString() {
        AccountAddress addr = (AccountAddress) world.getAddress();
        world.setResult(addr.toHexStringShort());
    }
    
    @When("I BCS serialize the address")
    public void whenBcsSerializeAddress() {
        AccountAddress addr = (AccountAddress) world.getAddress();
        byte[] bcsBytes = addr.toBytes(); // BCS serialization of address is just the 32 bytes
        world.setSerializedBytes(bcsBytes);
        world.setBytes(bcsBytes);
    }
    
    @When("I BCS deserialize as AccountAddress")
    public void whenBcsDeserializeAsAccountAddress() {
        try {
            byte[] bytes = world.getBytes();
            AccountAddress addr = AccountAddress.fromBytes(bytes);
            world.setAddress(addr);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I BCS deserialize the result as AccountAddress")
    public void whenBcsDeserializeResultAsAccountAddress() {
        try {
            byte[] bytes = world.getSerializedBytes();
            AccountAddress addr = AccountAddress.fromBytes(bytes);
            world.setResult(addr);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I run all parsing test vectors")
    public void whenRunAllParsingTestVectors() {
        @SuppressWarnings("unchecked")
        List<Vectors.AddressVector> vectors = 
            (List<Vectors.AddressVector>) world.getTestVectors().get("address_parsing");
        
        List<TestResult> results = new java.util.ArrayList<>();
        for (Vectors.AddressVector v : vectors) {
            try {
                AccountAddress addr = AccountAddress.fromHex(v.input);
                String fullHex = addr.toHexStringLong();
                String shortString = addr.toHexStringShort();
                
                boolean passed = fullHex.equalsIgnoreCase(v.expected.full_hex) &&
                                 shortString.equalsIgnoreCase(v.expected.short_string);
                
                results.add(new TestResult(v.name, passed, null));
            } catch (Exception e) {
                results.add(new TestResult(v.name, false, e.getMessage()));
            }
        }
        world.setResult(results);
    }
    
    // ==========================================================================
    // Then Steps
    // ==========================================================================
    
    @Then("the parsing should succeed")
    public void thenParsingShouldSucceed() {
        assertThat(world.getError())
            .as("Expected parsing to succeed, but got error: %s", 
                world.getError() != null ? world.getError().getMessage() : "")
            .isNull();
        assertThat(world.getAddress()).isNotNull();
    }
    
    @Then("the parsing should fail with an invalid address error")
    public void thenParsingShouldFailWithInvalidAddressError() {
        assertThat(world.getError())
            .as("Expected parsing to fail with invalid address error")
            .isNotNull();
    }
    
    @Then("the parsing should fail with an invalid hex error")
    public void thenParsingShouldFailWithInvalidHexError() {
        assertThat(world.getError())
            .as("Expected parsing to fail with invalid hex error")
            .isNotNull();
    }
    
    @Then("the parsing should fail with an invalid length error")
    public void thenParsingShouldFailWithInvalidLengthError() {
        assertThat(world.getError())
            .as("Expected parsing to fail with invalid length error")
            .isNotNull();
    }
    
    @Then("the address bytes should have length {int}")
    public void thenAddressBytesHaveLength(int expectedLength) {
        assertThat(world.getBytes()).hasSize(expectedLength);
    }
    
    @Then("byte {int} should equal {int}")
    public void thenByteAtIndexEquals(int index, int value) {
        assertThat(world.getBytes()[index] & 0xFF).isEqualTo(value);
    }
    
    @Then("bytes {int}-{int} should all be {int}")
    public void thenBytesInRangeShouldBe(int start, int end, int value) {
        for (int i = start; i <= end; i++) {
            assertThat(world.getBytes()[i] & 0xFF)
                .as("Byte at index %d", i)
                .isEqualTo(value);
        }
    }
    
    @Then("all {int} bytes should be {int}")
    public void thenAllBytesShouldBe(int count, int value) {
        assertThat(world.getBytes()).hasSize(count);
        for (int i = 0; i < count; i++) {
            assertThat(world.getBytes()[i] & 0xFF)
                .as("Byte at index %d", i)
                .isEqualTo(value);
        }
    }
    
    @Then("the short string should be {string}")
    public void thenShortStringShouldBe(String expected) {
        AccountAddress addr = (AccountAddress) world.getAddress();
        assertThat(addr.toHexStringShort()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the full hex should be {string}")
    public void thenFullHexShouldBe(String expected) {
        AccountAddress addr = (AccountAddress) world.getAddress();
        assertThat(addr.toHexStringLong()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the result should be {string}")
    public void thenResultShouldBe(String expected) {
        assertThat(world.getResult().toString()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the result should be {int} bytes")
    public void thenResultShouldBeBytes(int expectedLength) {
        assertThat(world.getSerializedBytes()).hasSize(expectedLength);
    }
    
    @Then("the two addresses should be equal")
    public void thenTwoAddressesShouldBeEqual() {
        AccountAddress addr1 = (AccountAddress) world.getAddress();
        AccountAddress addr2 = (AccountAddress) world.getAddress2();
        assertThat(addr1).isEqualTo(addr2);
    }
    
    @Then("the two addresses should not be equal")
    public void thenTwoAddressesShouldNotBeEqual() {
        AccountAddress addr1 = (AccountAddress) world.getAddress();
        AccountAddress addr2 = (AccountAddress) world.getAddress2();
        assertThat(addr1).isNotEqualTo(addr2);
    }
    
    @Then("the result should equal the original address")
    public void thenResultShouldEqualOriginalAddress() {
        AccountAddress original = (AccountAddress) world.getAddress();
        AccountAddress result = (AccountAddress) world.getResult();
        assertThat(result).isEqualTo(original);
    }
    
    @Then("all test vectors should pass")
    public void thenAllTestVectorsShouldPass() {
        @SuppressWarnings("unchecked")
        List<TestResult> results = (List<TestResult>) world.getResult();
        
        List<TestResult> failures = results.stream()
            .filter(r -> !r.passed)
            .toList();
        
        assertThat(failures)
            .as("Failed test vectors: %s", 
                failures.stream().map(f -> f.name + ": " + f.error).toList())
            .isEmpty();
    }
    
    // ==========================================================================
    // Helper Classes
    // ==========================================================================
    
    /**
     * Simple test result holder.
     */
    private static class TestResult {
        final String name;
        final boolean passed;
        final String error;
        
        TestResult(String name, boolean passed, String error) {
            this.name = name;
            this.passed = passed;
            this.error = error;
        }
    }
}
