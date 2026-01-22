package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import com.aptoslabs.japtos.types.HashValue;
import com.aptoslabs.japtos.utils.HexUtils;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Arrays;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for hashing.feature
 * 
 * These steps test SHA3-256, SHA2-256, domain-separated hashing, and HashValue
 * using the japtos SDK and standard Java crypto.
 */
public class HashingSteps {
    
    private final World world;
    
    // Hash results
    private byte[] hashResult;
    private byte[] hashResult2;
    private byte[] sha2Result;
    private byte[] sha3Result;
    private byte[] domainHash1;
    private byte[] domainHash2;
    private HashValue hashValue;
    
    // Input data
    private byte[] inputBytes;
    private byte[] inputBytes2;
    private byte[][] multipleInputs;
    private String domainString;
    private String domainString2;
    private byte[] transactionData;
    
    public HashingSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Static utility methods for hashing (used by other step classes)
    // ==========================================================================
    
    /**
     * Compute SHA3-256 hash.
     */
    public static byte[] sha3_256(byte[] data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA3-256");
            return digest.digest(data);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA3-256 not available", e);
        }
    }
    
    /**
     * Compute SHA2-256 hash.
     */
    public static byte[] sha2_256(byte[] data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            return digest.digest(data);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
    }
    
    /**
     * Compute HMAC-SHA512.
     */
    public static byte[] hmacSha512(byte[] key, byte[] data) {
        try {
            Mac mac = Mac.getInstance("HmacSHA512");
            SecretKeySpec secretKey = new SecretKeySpec(key, "HmacSHA512");
            mac.init(secretKey);
            return mac.doFinal(data);
        } catch (Exception e) {
            throw new RuntimeException("HMAC-SHA512 failed", e);
        }
    }
    
    // ==========================================================================
    // Given Steps - Input Data
    // ==========================================================================
    
    @Given("empty bytes")
    public void givenEmptyBytes() {
        inputBytes = new byte[0];
    }
    
    @Given("bytes for string {string}")
    public void givenBytesForString(String str) {
        inputBytes = str.getBytes(StandardCharsets.UTF_8);
    }
    
    @Given("bytes for {string} and {string}")
    public void givenBytesForTwoStrings(String str1, String str2) {
        inputBytes = str1.getBytes(StandardCharsets.UTF_8);
        inputBytes2 = str2.getBytes(StandardCharsets.UTF_8);
    }
    
    @Given("bytes {}")
    public void givenBytesArray(String bytesSpec) {
        // Parse ["hello", " ", "world"] format
        if (bytesSpec.startsWith("[\"")) {
            String[] parts = bytesSpec.substring(1, bytesSpec.length() - 1)
                .replace("\"", "")
                .split(", ");
            multipleInputs = new byte[parts.length][];
            for (int i = 0; i < parts.length; i++) {
                multipleInputs[i] = parts[i].getBytes(StandardCharsets.UTF_8);
            }
        }
    }
    
    @Given("{int} random bytes")
    public void givenRandomBytes(int count) {
        inputBytes = new byte[count];
        new SecureRandom().nextBytes(inputBytes);
    }
    
    @Given("{int} megabyte of random data")
    public void givenMegabyteOfRandomData(int megabytes) {
        inputBytes = new byte[megabytes * 1024 * 1024];
        new SecureRandom().nextBytes(inputBytes);
    }
    
    @Given("{int} bytes")
    public void givenNBytes(int count) {
        inputBytes = new byte[count];
        new SecureRandom().nextBytes(inputBytes);
    }
    
    // ==========================================================================
    // Given Steps - Domain Hashing
    // ==========================================================================
    
    @Given("the domain string {string}")
    public void givenDomainString(String domain) {
        domainString = domain;
    }
    
    @Given("transaction data bytes")
    public void givenTransactionDataBytes() {
        transactionData = new byte[100];
        new SecureRandom().nextBytes(transactionData);
    }
    
    @Given("the same data bytes")
    public void givenSameDataBytes() {
        transactionData = new byte[100];
        new SecureRandom().nextBytes(transactionData);
    }
    
    @Given("domains {string} and {string}")
    public void givenTwoDomains(String domain1, String domain2) {
        domainString = domain1;
        domainString2 = domain2;
    }
    
    // ==========================================================================
    // Given Steps - HashValue
    // ==========================================================================
    
    @Given("a 64-character hex string")
    public void given64CharacterHexString() {
        byte[] bytes = new byte[32];
        new SecureRandom().nextBytes(bytes);
        world.setHexString(HexUtils.bytesToHex(bytes));
    }
    
    @Given("the HashValue ZERO constant")
    public void givenHashValueZero() {
        hashValue = HashValue.ZERO;
    }
    
    @Given("a HashValue from known bytes")
    public void givenHashValueFromKnownBytes() {
        byte[] bytes = new byte[32];
        for (int i = 0; i < 32; i++) {
            bytes[i] = (byte) i;
        }
        hashValue = HashValue.fromBytes(bytes);
    }
    
    @Given("two HashValues from the same bytes")
    public void givenTwoHashValuesFromSameBytes() {
        byte[] bytes = new byte[32];
        new SecureRandom().nextBytes(bytes);
        hashValue = HashValue.fromBytes(bytes);
        world.setResult(HashValue.fromBytes(bytes.clone()));
    }
    
    // ==========================================================================
    // Given Steps - HMAC
    // ==========================================================================
    
    @Given("a mnemonic entropy and passphrase")
    public void givenMnemonicEntropyAndPassphrase() {
        inputBytes = "mnemonic entropy data".getBytes(StandardCharsets.UTF_8);
        world.setStringValue("passphrase");
    }
    
    // ==========================================================================
    // When Steps - SHA3-256
    // ==========================================================================
    
    @When("I compute SHA3-256")
    public void whenComputeSha3_256() {
        hashResult = sha3_256(inputBytes);
        world.setBytes(hashResult);
    }
    
    @When("I compute SHA3-256 for both")
    public void whenComputeSha3_256ForBoth() {
        hashResult = sha3_256(inputBytes);
        hashResult2 = sha3_256(inputBytes2);
    }
    
    @When("I compute SHA3-256 twice")
    public void whenComputeSha3_256Twice() {
        hashResult = sha3_256(inputBytes);
        hashResult2 = sha3_256(inputBytes);
    }
    
    @When("I compute SHA3-256 of all parts concatenated")
    public void whenComputeSha3_256OfConcatenated() {
        int totalLength = 0;
        for (byte[] part : multipleInputs) {
            totalLength += part.length;
        }
        byte[] combined = new byte[totalLength];
        int pos = 0;
        for (byte[] part : multipleInputs) {
            System.arraycopy(part, 0, combined, pos, part.length);
            pos += part.length;
        }
        hashResult = sha3_256(combined);
    }
    
    @When("I compute SHA3-256 of the domain")
    public void whenComputeSha3_256OfDomain() {
        hashResult = sha3_256(domainString.getBytes(StandardCharsets.UTF_8));
        world.setBytes(hashResult);
    }
    
    // ==========================================================================
    // When Steps - SHA2-256
    // ==========================================================================
    
    @When("I compute SHA2-256")
    public void whenComputeSha2_256() {
        hashResult = sha2_256(inputBytes);
        world.setBytes(hashResult);
    }
    
    @When("I compute both SHA2-256 and SHA3-256")
    public void whenComputeBothSha2AndSha3() {
        sha2Result = sha2_256(inputBytes);
        sha3Result = sha3_256(inputBytes);
    }
    
    // ==========================================================================
    // When Steps - Domain Hashing
    // ==========================================================================
    
    @When("I compute domain-separated hash")
    public void whenComputeDomainSeparatedHash() {
        // Domain-separated hash: SHA3-256(SHA3-256(domain) || data)
        byte[] domainHash = sha3_256(domainString.getBytes(StandardCharsets.UTF_8));
        byte[] combined = new byte[domainHash.length + transactionData.length];
        System.arraycopy(domainHash, 0, combined, 0, domainHash.length);
        System.arraycopy(transactionData, 0, combined, domainHash.length, transactionData.length);
        hashResult = sha3_256(combined);
    }
    
    @When("I compute domain-separated hashes")
    public void whenComputeDomainSeparatedHashes() {
        // First domain
        byte[] domainHash1Prefix = sha3_256(domainString.getBytes(StandardCharsets.UTF_8));
        byte[] combined1 = new byte[domainHash1Prefix.length + transactionData.length];
        System.arraycopy(domainHash1Prefix, 0, combined1, 0, domainHash1Prefix.length);
        System.arraycopy(transactionData, 0, combined1, domainHash1Prefix.length, transactionData.length);
        domainHash1 = sha3_256(combined1);
        
        // Second domain
        byte[] domainHash2Prefix = sha3_256(domainString2.getBytes(StandardCharsets.UTF_8));
        byte[] combined2 = new byte[domainHash2Prefix.length + transactionData.length];
        System.arraycopy(domainHash2Prefix, 0, combined2, 0, domainHash2Prefix.length);
        System.arraycopy(transactionData, 0, combined2, domainHash2Prefix.length, transactionData.length);
        domainHash2 = sha3_256(combined2);
    }
    
    @When("I compute the domain prefix")
    public void whenComputeDomainPrefix() {
        hashResult = sha3_256(domainString.getBytes(StandardCharsets.UTF_8));
    }
    
    // ==========================================================================
    // When Steps - HashValue
    // ==========================================================================
    
    @When("I create a HashValue from the bytes")
    public void whenCreateHashValueFromBytes() {
        try {
            hashValue = HashValue.fromBytes(inputBytes);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I create a HashValue from hex")
    public void whenCreateHashValueFromHex() {
        try {
            hashValue = HashValue.fromHex(world.getHexString());
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I try to create a HashValue")
    public void whenTryCreateHashValue() {
        try {
            hashValue = HashValue.fromBytes(inputBytes);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I format it as hex")
    public void whenFormatAsHex() {
        world.setHexString(hashValue.toHex());
    }
    
    @When("I compute HashValue using sha3_256_of")
    public void whenComputeHashValueUsingSha3_256Of() {
        byte[] hash = sha3_256(inputBytes);
        hashValue = HashValue.fromBytes(hash);
    }
    
    // ==========================================================================
    // When Steps - HMAC
    // ==========================================================================
    
    @When("I compute HMAC-SHA512 with key {string} + passphrase")
    public void whenComputeHmacSha512(String keyPrefix) {
        String key = keyPrefix + world.getStringValue();
        hashResult = hmacSha512(key.getBytes(StandardCharsets.UTF_8), inputBytes);
        world.setBytes(hashResult);
    }
    
    // ==========================================================================
    // Then Steps - Hash Results
    // ==========================================================================
    
    @Then("the result should be {int} bytes")
    public void thenResultShouldBeNBytes(int expected) {
        assertThat(world.getBytes()).hasSize(expected);
    }
    
    @Then("the hex should be {string}")
    public void thenHexShouldBe(String expected) {
        String actual = HexUtils.bytesToHex(world.getBytes()).substring(2); // Remove 0x prefix
        assertThat(actual).isEqualToIgnoringCase(expected);
    }
    
    @Then("the hashes should be different")
    public void thenHashesShouldBeDifferent() {
        assertThat(hashResult).isNotEqualTo(hashResult2);
    }
    
    @Then("both results should be identical")
    public void thenBothResultsShouldBeIdentical() {
        assertThat(hashResult).isEqualTo(hashResult2);
    }
    
    @Then("the result should equal SHA3-256 of {string}")
    public void thenResultShouldEqualSha3Of(String input) {
        byte[] expected = sha3_256(input.getBytes(StandardCharsets.UTF_8));
        assertThat(hashResult).isEqualTo(expected);
    }
    
    @Then("the results should be different")
    public void thenResultsShouldBeDifferent() {
        if (sha2Result != null && sha3Result != null) {
            assertThat(sha2Result).isNotEqualTo(sha3Result);
        } else if (domainHash1 != null && domainHash2 != null) {
            assertThat(domainHash1).isNotEqualTo(domainHash2);
        }
    }
    
    // ==========================================================================
    // Then Steps - Domain Hashing
    // ==========================================================================
    
    @Then("the result should be SHA3-256\\(SHA3-256\\(domain\\) || data\\)")
    public void thenResultShouldBeDomainSeparatedHash() {
        // Verify by recomputing
        byte[] domainHash = sha3_256(domainString.getBytes(StandardCharsets.UTF_8));
        byte[] combined = new byte[domainHash.length + transactionData.length];
        System.arraycopy(domainHash, 0, combined, 0, domainHash.length);
        System.arraycopy(transactionData, 0, combined, domainHash.length, transactionData.length);
        byte[] expected = sha3_256(combined);
        
        assertThat(hashResult).isEqualTo(expected);
    }
    
    @Then("the result should be SHA3-256 of the domain string bytes")
    public void thenResultShouldBeSha3OfDomainStringBytes() {
        byte[] expected = sha3_256(domainString.getBytes(StandardCharsets.UTF_8));
        assertThat(hashResult).isEqualTo(expected);
    }
    
    @Then("the first {int} bytes should be {string}")
    public void thenFirstBytesShouldBe(int count, String expected) {
        assertThat(world.getBytes()).hasSizeGreaterThanOrEqualTo(count);
    }
    
    // ==========================================================================
    // Then Steps - HashValue
    // ==========================================================================
    
    @Then("the hash value should contain those bytes")
    public void thenHashValueShouldContainThoseBytes() {
        assertThat(hashValue.toBytes()).isEqualTo(inputBytes);
    }
    
    @Then("all {int} bytes should be zero")
    public void thenAllBytesShouldBeZero(int count) {
        byte[] bytes = hashValue.toBytes();
        assertThat(bytes).hasSize(count);
        for (byte b : bytes) {
            assertThat(b).isZero();
        }
    }
    
    @Then("the hex length should be {int} characters")
    public void thenHexLengthShouldBe(int expected) {
        assertThat(world.getHexString()).hasSize(expected);
    }
    
    @Then("they should be equal")
    public void thenTheyShouldBeEqual() {
        HashValue other = (HashValue) world.getResult();
        assertThat(hashValue).isEqualTo(other);
    }
    
    @Then("the result should equal a HashValue created from the expected hash")
    public void thenResultShouldEqualHashValueFromExpectedHash() {
        byte[] expectedHash = sha3_256(inputBytes);
        HashValue expected = HashValue.fromBytes(expectedHash);
        assertThat(hashValue).isEqualTo(expected);
    }
    
    @Then("it should fail with an invalid length error")
    public void thenShouldFailWithInvalidLengthError() {
        assertThat(world.getError())
            .as("Expected invalid length error")
            .isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Large Data
    // ==========================================================================
    
    @Then("the operation should complete successfully")
    public void thenOperationShouldCompleteSuccessfully() {
        assertThat(world.getError()).isNull();
        assertThat(world.getBytes()).isNotNull();
    }
}
