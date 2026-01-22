package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.security.SecureRandom;
import java.util.Arrays;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for authentication-key.feature
 * 
 * These steps test authentication key derivation from various public key types.
 * 
 * TODO: Replace placeholder implementations with actual japtos SDK calls.
 */
public class AuthKeySteps {
    
    private final World world;
    
    // Key and auth key state
    private byte[] publicKey;
    private byte[] publicKey2;
    private byte[] authKey;
    private byte[] authKey2;
    private byte[] authKeyInput;
    private int schemeId;
    
    public AuthKeySteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Ed25519
    // ==========================================================================
    
    @Given("an Ed25519 public key")
    public void givenEd25519PublicKey() {
        publicKey = new byte[32];
        new SecureRandom().nextBytes(publicKey);
        schemeId = 0x00;
    }
    
    @Given("an Ed25519 public key of {int} bytes")
    public void givenEd25519PublicKeyOfNBytes(int size) {
        publicKey = new byte[size];
        new SecureRandom().nextBytes(publicKey);
        schemeId = 0x00;
    }
    
    @Given("two different Ed25519 public keys")
    public void givenTwoDifferentEd25519PublicKeys() {
        publicKey = new byte[32];
        publicKey2 = new byte[32];
        new SecureRandom().nextBytes(publicKey);
        new SecureRandom().nextBytes(publicKey2);
        schemeId = 0x00;
    }
    
    @Given("Ed25519 public key from test vectors")
    public void givenEd25519PublicKeyFromTestVectors() {
        // Use a known test vector
        publicKey = new byte[32];
        // In real implementation, load from test vectors
        Arrays.fill(publicKey, (byte) 0x42);
        schemeId = 0x00;
    }
    
    // ==========================================================================
    // Given Steps - Secp256k1
    // ==========================================================================
    
    @Given("a Secp256k1 public key \\(uncompressed, {int} bytes\\)")
    public void givenSecp256k1PublicKeyUncompressed(int size) {
        publicKey = new byte[size];
        publicKey[0] = 0x04; // Uncompressed prefix
        new SecureRandom().nextBytes(Arrays.copyOfRange(publicKey, 1, size));
        System.arraycopy(new byte[size - 1], 0, publicKey, 1, size - 1);
        new SecureRandom().nextBytes(publicKey);
        publicKey[0] = 0x04;
        schemeId = 0x01;
    }
    
    @Given("a Secp256k1 key pair")
    public void givenSecp256k1KeyPair() {
        publicKey = new byte[65];
        publicKey[0] = 0x04; // Uncompressed prefix
        new SecureRandom().nextBytes(publicKey);
        publicKey[0] = 0x04;
        schemeId = 0x01;
    }
    
    @Given("a Secp256k1 public key")
    public void givenSecp256k1PublicKey() {
        publicKey = new byte[65];
        publicKey[0] = 0x04;
        new SecureRandom().nextBytes(publicKey);
        publicKey[0] = 0x04;
        schemeId = 0x01;
    }
    
    @Given("Secp256k1 public key from test vectors")
    public void givenSecp256k1PublicKeyFromTestVectors() {
        publicKey = new byte[65];
        publicKey[0] = 0x04;
        // In real implementation, load from test vectors
        schemeId = 0x01;
    }
    
    // ==========================================================================
    // Given Steps - Generic
    // ==========================================================================
    
    @Given("public key bytes")
    public void givenPublicKeyBytes() {
        publicKey = new byte[32];
        new SecureRandom().nextBytes(publicKey);
    }
    
    @Given("a scheme identifier")
    public void givenSchemeIdentifier() {
        schemeId = 0x00; // Default to Ed25519
    }
    
    @Given("a {word} public key")
    public void givenPublicKeyOfType(String keyType) {
        switch (keyType.toLowerCase()) {
            case "ed25519" -> {
                publicKey = new byte[32];
                schemeId = 0x00;
            }
            case "secp256k1" -> {
                publicKey = new byte[65];
                publicKey[0] = 0x04;
                schemeId = 0x01;
            }
            case "secp256r1" -> {
                publicKey = new byte[65];
                publicKey[0] = 0x04;
                schemeId = 0x02;
            }
            case "multied25519" -> {
                publicKey = new byte[64]; // Example: 2 keys
                schemeId = 0x01;
            }
            case "multikey" -> {
                publicKey = new byte[64];
                schemeId = 0x03;
            }
            default -> throw new IllegalArgumentException("Unknown key type: " + keyType);
        }
        new SecureRandom().nextBytes(publicKey);
        if (schemeId == 0x01 || schemeId == 0x02) {
            publicKey[0] = 0x04; // Restore uncompressed prefix
        }
    }
    
    // ==========================================================================
    // Given Steps - Authentication Key
    // ==========================================================================
    
    @Given("an authentication key")
    public void givenAuthenticationKey() {
        authKey = new byte[32];
        new SecureRandom().nextBytes(authKey);
    }
    
    @Given("{int} random bytes")
    public void givenRandomBytes(int count) {
        world.setBytes(new byte[count]);
        new SecureRandom().nextBytes(world.getBytes());
    }
    
    @Given("{int} zero bytes")
    public void givenZeroBytes(int count) {
        world.setBytes(new byte[count]);
    }
    
    @Given("an Ed25519 account that has never rotated keys")
    public void givenEd25519AccountNeverRotatedKeys() {
        // Generate a fresh account
        CryptoSteps.PlaceholderEd25519KeyPair keyPair = CryptoSteps.PlaceholderEd25519KeyPair.generate();
        publicKey = keyPair.getPublicKeyBytes();
        schemeId = 0x00;
        authKey = deriveAuthKey(publicKey, schemeId);
        world.setAddress(new AddressSteps.PlaceholderAddress(authKey));
    }
    
    // ==========================================================================
    // When Steps
    // ==========================================================================
    
    @When("I derive the authentication key")
    public void whenDeriveAuthenticationKey() {
        authKey = deriveAuthKey(publicKey, schemeId);
        world.setBytes(authKey);
    }
    
    @When("I derive the authentication key twice")
    public void whenDeriveAuthenticationKeyTwice() {
        authKey = deriveAuthKey(publicKey, schemeId);
        authKey2 = deriveAuthKey(publicKey, schemeId);
    }
    
    @When("I derive authentication keys from each")
    public void whenDeriveAuthKeysFromEach() {
        authKey = deriveAuthKey(publicKey, schemeId);
        authKey2 = deriveAuthKey(publicKey2, schemeId);
    }
    
    @When("I prepare the authentication key input")
    public void whenPrepareAuthKeyInput() {
        authKeyInput = new byte[publicKey.length + 1];
        System.arraycopy(publicKey, 0, authKeyInput, 0, publicKey.length);
        authKeyInput[publicKey.length] = (byte) schemeId;
    }
    
    @When("I get the public key for authentication key derivation")
    public void whenGetPublicKeyForAuthKeyDerivation() {
        // Store the public key bytes
        world.setBytes(publicKey);
    }
    
    @When("I derive the authentication key using from_public_key")
    public void whenDeriveAuthKeyUsingFromPublicKey() {
        authKey = deriveAuthKey(publicKey, schemeId);
    }
    
    @When("I convert it to an account address")
    public void whenConvertToAccountAddress() {
        if (authKey == null) {
            authKey = world.getBytes();
        }
        world.setAddress(new AddressSteps.PlaceholderAddress(authKey));
    }
    
    @When("I compare the address to the authentication key")
    public void whenCompareAddressToAuthKey() {
        // Address and auth key comparison will be done in Then step
    }
    
    @When("I create an authentication key from the bytes")
    public void whenCreateAuthKeyFromBytes() {
        try {
            byte[] bytes = world.getBytes();
            if (bytes.length != 32) {
                throw new IllegalArgumentException("Authentication key must be 32 bytes");
            }
            authKey = bytes.clone();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I get it as bytes")
    public void whenGetAsBytes() {
        world.setBytes(authKey);
    }
    
    @When("I format it as hex")
    public void whenFormatAsHex() {
        world.setHexString(Vectors.bytesToHex(authKey));
    }
    
    @When("I try to create an authentication key")
    public void whenTryCreateAuthKey() {
        try {
            byte[] bytes = world.getBytes();
            if (bytes.length != 32) {
                throw new IllegalArgumentException("Authentication key must be 32 bytes");
            }
            authKey = bytes.clone();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I create an authentication key")
    public void whenCreateAuthKey() {
        try {
            byte[] bytes = world.getBytes();
            authKey = bytes.clone();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    // ==========================================================================
    // Then Steps
    // ==========================================================================
    
    @Then("the result should be {int} bytes")
    public void thenResultShouldBeNBytes(int expected) {
        assertThat(world.getBytes()).hasSize(expected);
    }
    
    @Then("it should equal SHA3-256\\(public_key_bytes || 0x00\\)")
    public void thenShouldEqualSha3OfPublicKeyAnd00() {
        byte[] input = new byte[publicKey.length + 1];
        System.arraycopy(publicKey, 0, input, 0, publicKey.length);
        input[publicKey.length] = 0x00;
        byte[] expected = HashingSteps.PlaceholderHash.sha3_256(input);
        assertThat(world.getBytes()).isEqualTo(expected);
    }
    
    @Then("it should equal SHA3-256\\(public_key_bytes || 0x01\\)")
    public void thenShouldEqualSha3OfPublicKeyAnd01() {
        byte[] input = new byte[publicKey.length + 1];
        System.arraycopy(publicKey, 0, input, 0, publicKey.length);
        input[publicKey.length] = 0x01;
        byte[] expected = HashingSteps.PlaceholderHash.sha3_256(input);
        assertThat(world.getBytes()).isEqualTo(expected);
    }
    
    @Then("the input should be {int} bytes")
    public void thenInputShouldBeNBytes(int expected) {
        assertThat(authKeyInput).hasSize(expected);
    }
    
    @Then("the last byte should be {}")
    public void thenLastByteShouldBe(String valueStr) {
        int expected = Integer.decode(valueStr);
        assertThat(authKeyInput[authKeyInput.length - 1] & 0xFF).isEqualTo(expected);
    }
    
    @Then("both results should be identical")
    public void thenBothResultsShouldBeIdentical() {
        assertThat(authKey).isEqualTo(authKey2);
    }
    
    @Then("the authentication keys should be different")
    public void thenAuthKeysShouldBeDifferent() {
        assertThat(authKey).isNotEqualTo(authKey2);
    }
    
    @Then("it should be the uncompressed format \\({int} bytes\\)")
    public void thenShouldBeUncompressedFormat(int expectedSize) {
        assertThat(world.getBytes()).hasSize(expectedSize);
    }
    
    @Then("the first byte should be {}")
    public void thenFirstByteShouldBe(String valueStr) {
        int expected = Integer.decode(valueStr);
        assertThat(world.getBytes()[0] & 0xFF).isEqualTo(expected);
    }
    
    @Then("the result should equal SHA3-256\\(public_key_bytes || scheme_id\\)")
    public void thenResultShouldEqualSha3OfPublicKeyAndSchemeId() {
        byte[] input = new byte[publicKey.length + 1];
        System.arraycopy(publicKey, 0, input, 0, publicKey.length);
        input[publicKey.length] = (byte) schemeId;
        byte[] expected = HashingSteps.PlaceholderHash.sha3_256(input);
        assertThat(authKey).isEqualTo(expected);
    }
    
    @Then("the scheme identifier should be {}")
    public void thenSchemeIdentifierShouldBe(String valueStr) {
        int expected = Integer.decode(valueStr);
        assertThat(schemeId).isEqualTo(expected);
    }
    
    @Then("the address bytes should equal the authentication key bytes")
    public void thenAddressBytesShouldEqualAuthKeyBytes() {
        AddressSteps.PlaceholderAddress addr = (AddressSteps.PlaceholderAddress) world.getAddress();
        assertThat(addr.toBytes()).isEqualTo(authKey);
    }
    
    @Then("they should be equal")
    public void thenTheyShouldBeEqual() {
        AddressSteps.PlaceholderAddress addr = (AddressSteps.PlaceholderAddress) world.getAddress();
        assertThat(addr.toBytes()).isEqualTo(authKey);
    }
    
    @Then("the authentication key should contain those bytes")
    public void thenAuthKeyShouldContainThoseBytes() {
        assertThat(authKey).isEqualTo(world.getBytes());
    }
    
    @Then("converting to address should give those same bytes")
    public void thenConvertingToAddressShouldGiveSameBytes() {
        AddressSteps.PlaceholderAddress addr = new AddressSteps.PlaceholderAddress(authKey);
        assertThat(addr.toBytes()).isEqualTo(authKey);
    }
    
    @Then("I should get a {int}-byte array")
    public void thenShouldGetNByteArray(int expected) {
        assertThat(world.getBytes()).hasSize(expected);
    }
    
    @Then("the result should be {int} hex characters with 0x prefix")
    public void thenResultShouldBeNHexCharsWithPrefix(int hexChars) {
        String hex = world.getHexString();
        assertThat(hex).startsWith("0x");
        assertThat(hex).hasSize(hexChars + 2); // +2 for "0x"
    }
    
    @Then("it should match the expected value from test vectors")
    public void thenShouldMatchTestVectors() {
        // Placeholder - actual implementation would check against test vectors
        assertThat(authKey).isNotNull();
        assertThat(authKey).hasSize(32);
    }
    
    @Then("it should fail with an invalid length error")
    public void thenShouldFailWithInvalidLengthError() {
        assertThat(world.getError())
            .as("Expected invalid length error")
            .isNotNull();
    }
    
    @Then("it should succeed")
    public void thenShouldSucceed() {
        assertThat(world.getError()).isNull();
    }
    
    @Then("converting to address should give the zero address")
    public void thenConvertingToAddressShouldGiveZeroAddress() {
        AddressSteps.PlaceholderAddress addr = new AddressSteps.PlaceholderAddress(authKey);
        assertThat(addr).isEqualTo(AddressSteps.PlaceholderAddress.ZERO);
    }
    
    // ==========================================================================
    // Helper Methods
    // ==========================================================================
    
    private byte[] deriveAuthKey(byte[] publicKeyBytes, int scheme) {
        byte[] input = new byte[publicKeyBytes.length + 1];
        System.arraycopy(publicKeyBytes, 0, input, 0, publicKeyBytes.length);
        input[publicKeyBytes.length] = (byte) scheme;
        return HashingSteps.PlaceholderHash.sha3_256(input);
    }
}
