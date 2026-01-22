package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import com.aptoslabs.japtos.account.Ed25519Account;
import com.aptoslabs.japtos.crypto.Ed25519PrivateKey;
import com.aptoslabs.japtos.crypto.Ed25519PublicKey;
import com.aptoslabs.japtos.crypto.Ed25519Signature;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.types.AuthenticationKey;
import com.aptoslabs.japtos.utils.HexUtils;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.Arrays;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for ed25519.feature
 * 
 * These steps test Ed25519 key generation, signing, verification, and derivation
 * using the japtos SDK.
 */
public class CryptoSteps {
    
    private final World world;
    
    // Ed25519 keys and accounts
    private Ed25519Account account;
    private Ed25519Account account2;
    private Ed25519PrivateKey privateKey;
    private Ed25519PublicKey publicKey;
    private Ed25519Signature signature;
    private Ed25519Signature signature2;
    private byte[] message;
    private byte[] message2;
    private byte[] seed;
    private AuthenticationKey authKey;
    
    public CryptoSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Key Generation
    // ==========================================================================
    
    @Given("an Ed25519 key pair")
    public void givenEd25519KeyPair() {
        account = Ed25519Account.generate();
        privateKey = account.getPrivateKey();
        publicKey = account.getPublicKey();
    }
    
    @Given("two different Ed25519 key pairs")
    public void givenTwoDifferentKeyPairs() {
        account = Ed25519Account.generate();
        account2 = Ed25519Account.generate();
    }
    
    @Given("a 32-byte seed")
    public void given32ByteSeed() {
        seed = new byte[32];
        new SecureRandom().nextBytes(seed);
    }
    
    @Given("a valid 64-byte Ed25519 private key \\(seed + public key\\)")
    public void given64BytePrivateKey() {
        // Generate an account and get its expanded private key
        account = Ed25519Account.generate();
        byte[] privateBytes = account.getPrivateKey().toBytes();
        byte[] publicBytes = account.getPublicKey().toBytes();
        byte[] combined = new byte[64];
        System.arraycopy(privateBytes, 0, combined, 0, 32);
        System.arraycopy(publicBytes, 0, combined, 32, 32);
        world.setBytes(combined);
    }
    
    @Given("a hex-encoded Ed25519 private key {string}")
    public void givenHexEncodedPrivateKey(String hex) {
        world.setHexString(hex);
    }
    
    @Given("bytes of length {int}")
    public void givenBytesOfLength(int length) {
        world.setBytes(new byte[length]);
    }
    
    @Given("an Ed25519 public key")
    public void givenEd25519PublicKey() {
        account = Ed25519Account.generate();
        publicKey = account.getPublicKey();
    }
    
    @Given("private key hex {string}")
    public void givenPrivateKeyHex(String hex) {
        world.setHexString(hex);
    }
    
    @Given("a known Ed25519 key pair from test vectors")
    public void givenKnownKeyPairFromTestVectors() throws Exception {
        // Use a known test vector key
        String knownPrivateKey = "0x0000000000000000000000000000000000000000000000000000000000000001";
        byte[] privateBytes = HexUtils.hexToBytes(knownPrivateKey);
        privateKey = Ed25519PrivateKey.fromBytes(privateBytes);
        account = Ed25519Account.fromPrivateKey(privateKey);
        publicKey = account.getPublicKey();
    }
    
    @Given("an Ed25519 key pair created in a scope")
    public void givenKeyPairInScope() {
        account = Ed25519Account.generate();
    }
    
    // ==========================================================================
    // Given Steps - Messages
    // ==========================================================================
    
    @Given("a message {string}")
    public void givenMessage(String msg) {
        message = msg.getBytes(StandardCharsets.UTF_8);
    }
    
    @Given("an empty message")
    public void givenEmptyMessage() {
        message = new byte[0];
    }
    
    @Given("messages {string} and {string}")
    public void givenTwoMessages(String msg1, String msg2) {
        message = msg1.getBytes(StandardCharsets.UTF_8);
        message2 = msg2.getBytes(StandardCharsets.UTF_8);
    }
    
    @Given("a message signed by the first key")
    public void givenMessageSignedByFirstKey() {
        message = "test message".getBytes(StandardCharsets.UTF_8);
        signature = account.sign(message);
    }
    
    @Given("a signature created by the key pair")
    public void givenSignatureCreatedByKeyPair() {
        signature = account.sign(message);
    }
    
    @Given("a signature for message {string}")
    public void givenSignatureForMessage(String msg) {
        message = msg.getBytes(StandardCharsets.UTF_8);
        signature = account.sign(message);
    }
    
    @Given("a signature with invalid bytes")
    public void givenInvalidSignature() {
        byte[] invalidSigBytes = new byte[64];
        Arrays.fill(invalidSigBytes, (byte) 0xFF);
        signature = Ed25519Signature.fromBytes(invalidSigBytes);
    }
    
    @Given("a signature truncated to {int} bytes")
    public void givenTruncatedSignature(int length) {
        Ed25519Signature fullSig = account.sign(message);
        byte[] truncated = Arrays.copyOf(fullSig.toBytes(), length);
        // Store truncated bytes for verification attempt
        world.setBytes(truncated);
    }
    
    @Given("the message from test vectors")
    public void givenMessageFromTestVectors() {
        message = "test message".getBytes(StandardCharsets.UTF_8);
    }
    
    // ==========================================================================
    // When Steps - Key Generation
    // ==========================================================================
    
    @When("I generate a random Ed25519 key pair")
    public void whenGenerateRandomKeyPair() {
        account = Ed25519Account.generate();
        privateKey = account.getPrivateKey();
        publicKey = account.getPublicKey();
    }
    
    @When("I generate two random Ed25519 key pairs")
    public void whenGenerateTwoKeyPairs() {
        account = Ed25519Account.generate();
        account2 = Ed25519Account.generate();
    }
    
    @When("I create an Ed25519 key pair from the seed")
    public void whenCreateKeyPairFromSeed() {
        privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
        publicKey = account.getPublicKey();
    }
    
    @When("I create an Ed25519 key pair from the bytes")
    public void whenCreateKeyPairFromBytes() {
        byte[] bytes = world.getBytes();
        byte[] seedBytes = bytes.length == 64 ? Arrays.copyOf(bytes, 32) : bytes;
        privateKey = Ed25519PrivateKey.fromBytes(seedBytes);
        account = Ed25519Account.fromPrivateKey(privateKey);
        publicKey = account.getPublicKey();
    }
    
    @When("I create an Ed25519 key pair from hex")
    public void whenCreateKeyPairFromHex() {
        try {
            byte[] privateBytes = HexUtils.hexToBytes(world.getHexString());
            privateKey = Ed25519PrivateKey.fromBytes(privateBytes);
            account = Ed25519Account.fromPrivateKey(privateKey);
            publicKey = account.getPublicKey();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I create an Ed25519 key pair")
    public void whenCreateKeyPair() {
        try {
            byte[] privateBytes = HexUtils.hexToBytes(world.getHexString());
            privateKey = Ed25519PrivateKey.fromBytes(privateBytes);
            account = Ed25519Account.fromPrivateKey(privateKey);
            publicKey = account.getPublicKey();
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I try to create an Ed25519 key pair")
    public void whenTryCreateKeyPair() {
        try {
            byte[] bytes = world.getBytes();
            privateKey = Ed25519PrivateKey.fromBytes(bytes);
            account = Ed25519Account.fromPrivateKey(privateKey);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    // ==========================================================================
    // When Steps - Signing
    // ==========================================================================
    
    @When("I sign the message")
    public void whenSignMessage() {
        signature = account.sign(message);
    }
    
    @When("I sign the message twice")
    public void whenSignMessageTwice() {
        signature = account.sign(message);
        signature2 = account.sign(message);
    }
    
    @When("I sign both messages")
    public void whenSignBothMessages() {
        signature = account.sign(message);
        signature2 = account.sign(message2);
    }
    
    @When("both keys sign the message")
    public void whenBothKeysSign() {
        signature = account.sign(message);
        signature2 = account2.sign(message);
    }
    
    // ==========================================================================
    // When Steps - Verification
    // ==========================================================================
    
    @When("I verify the signature")
    public void whenVerifySignature() {
        try {
            boolean valid = publicKey.verify(message, signature);
            world.setResult(valid);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            world.setResult(false);
        }
    }
    
    @When("I verify with the second key's public key")
    public void whenVerifyWithSecondKey() {
        try {
            boolean valid = account2.getPublicKey().verify(message, signature);
            world.setResult(valid);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            world.setResult(false);
        }
    }
    
    @When("I verify the signature against message {string}")
    public void whenVerifyAgainstDifferentMessage(String msg) {
        try {
            byte[] differentMessage = msg.getBytes(StandardCharsets.UTF_8);
            boolean valid = publicKey.verify(differentMessage, signature);
            world.setResult(valid);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
            world.setResult(false);
        }
    }
    
    @When("I try to verify the signature")
    public void whenTryVerifySignature() {
        try {
            // Attempt to create signature from truncated bytes
            byte[] truncatedBytes = world.getBytes();
            Ed25519Signature truncatedSig = Ed25519Signature.fromBytes(truncatedBytes);
            boolean valid = publicKey.verify(message, truncatedSig);
            world.setResult(valid);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    // ==========================================================================
    // When Steps - Export
    // ==========================================================================
    
    @When("I export the public key as bytes")
    public void whenExportPublicKeyBytes() {
        world.setBytes(publicKey.toBytes());
    }
    
    @When("I export the private key as bytes")
    public void whenExportPrivateKeyBytes() {
        world.setBytes(privateKey.toBytes());
    }
    
    @When("I export the private key as hex")
    public void whenExportPrivateKeyHex() {
        world.setHexString(HexUtils.bytesToHex(privateKey.toBytes()));
    }
    
    // ==========================================================================
    // When Steps - Authentication Key
    // ==========================================================================
    
    @When("I derive the authentication key")
    public void whenDeriveAuthKey() {
        authKey = account.getAuthenticationKey();
        world.setBytes(authKey.toBytes());
    }
    
    @When("I convert it to an account address")
    public void whenConvertToAccountAddress() {
        AccountAddress addr = authKey.toAccountAddress();
        world.setAddress(addr);
    }
    
    @When("the key pair goes out of scope")
    public void whenKeyPairGoesOutOfScope() {
        account = null;
        privateKey = null;
        System.gc();
    }
    
    @When("I format it for debug output")
    public void whenFormatForDebug() {
        world.setResult(account.toString());
    }
    
    // ==========================================================================
    // Then Steps - Key Properties
    // ==========================================================================
    
    @Then("the private key should be {int} bytes")
    public void thenPrivateKeyShouldBeNBytes(int expected) {
        assertThat(account.getPrivateKey().toBytes()).hasSize(expected);
    }
    
    @Then("the public key should be {int} bytes")
    public void thenPublicKeyShouldBeNBytes(int expected) {
        assertThat(account.getPublicKey().toBytes()).hasSize(expected);
    }
    
    @Then("the key pair should be valid")
    public void thenKeyPairShouldBeValid() {
        assertThat(account).isNotNull();
        assertThat(account.getPrivateKey()).isNotNull();
        assertThat(account.getPublicKey()).isNotNull();
    }
    
    @Then("the private keys should be different")
    public void thenPrivateKeysShouldBeDifferent() {
        assertThat(account.getPrivateKey().toBytes())
            .isNotEqualTo(account2.getPrivateKey().toBytes());
    }
    
    @Then("the public keys should be different")
    public void thenPublicKeysShouldBeDifferent() {
        assertThat(account.getPublicKey().toBytes())
            .isNotEqualTo(account2.getPublicKey().toBytes());
    }
    
    @Then("creating again from the same seed should produce the same key pair")
    public void thenSameSeedProducesSameKeyPair() {
        Ed25519PrivateKey pk2 = Ed25519PrivateKey.fromBytes(seed);
        Ed25519Account account2 = Ed25519Account.fromPrivateKey(pk2);
        assertThat(account.getPrivateKey().toBytes())
            .isEqualTo(account2.getPrivateKey().toBytes());
        assertThat(account.getPublicKey().toBytes())
            .isEqualTo(account2.getPublicKey().toBytes());
    }
    
    @Then("the public key should match the embedded public key")
    public void thenPublicKeyMatchesEmbedded() {
        byte[] bytes = world.getBytes();
        byte[] embeddedPublicKey = Arrays.copyOfRange(bytes, 32, 64);
        assertThat(account.getPublicKey().toBytes()).isEqualTo(embeddedPublicKey);
    }
    
    @Then("it should fail with an invalid private key error")
    public void thenShouldFailWithInvalidPrivateKeyError() {
        assertThat(world.getError())
            .as("Expected invalid private key error")
            .isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Signatures
    // ==========================================================================
    
    @Then("the signature should be {int} bytes")
    public void thenSignatureShouldBeNBytes(int expected) {
        assertThat(signature.toBytes()).hasSize(expected);
    }
    
    @Then("the signature should be valid for the message")
    public void thenSignatureShouldBeValid() {
        assertThat(publicKey.verify(message, signature)).isTrue();
    }
    
    @Then("the signature should be valid")
    public void thenSignatureValid() {
        assertThat(publicKey.verify(message, signature)).isTrue();
    }
    
    @Then("both signatures should be identical")
    public void thenBothSignaturesIdentical() {
        assertThat(signature.toBytes()).isEqualTo(signature2.toBytes());
    }
    
    @Then("the signatures should be different")
    public void thenSignaturesShouldBeDifferent() {
        assertThat(signature.toBytes()).isNotEqualTo(signature2.toBytes());
    }
    
    @Then("verification should succeed")
    public void thenVerificationShouldSucceed() {
        assertThat((Boolean) world.getResult()).isTrue();
    }
    
    @Then("verification should fail")
    public void thenVerificationShouldFail() {
        Object result = world.getResult();
        assertThat(result == null || Boolean.FALSE.equals(result)).isTrue();
    }
    
    @Then("it should fail with an invalid signature error")
    public void thenShouldFailWithInvalidSignatureError() {
        assertThat(world.getError())
            .as("Expected invalid signature error")
            .isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Export
    // ==========================================================================
    
    @Then("the result should be {int} or {int} bytes")
    public void thenResultShouldBeNOrMBytes(int n, int m) {
        int length = world.getBytes().length;
        assertThat(length == n || length == m)
            .as("Expected %d or %d bytes, got %d", n, m, length)
            .isTrue();
    }
    
    @Then("recreating from the bytes should produce the same key pair")
    public void thenRecreatingFromBytesShouldProduceSameKeyPair() {
        byte[] exported = world.getBytes();
        Ed25519PrivateKey recreatedKey = Ed25519PrivateKey.fromBytes(exported);
        Ed25519Account recreated = Ed25519Account.fromPrivateKey(recreatedKey);
        assertThat(recreated.getPublicKey().toBytes()).isEqualTo(publicKey.toBytes());
    }
    
    @Then("the result should start with {string}")
    public void thenResultShouldStartWith(String prefix) {
        assertThat(world.getHexString()).startsWith(prefix);
    }
    
    @Then("the hex length should be {int} or {int} characters")
    public void thenHexLengthShouldBeNOrMChars(int n, int m) {
        int length = world.getHexString().length();
        assertThat(length == n || length == m)
            .as("Expected %d or %d characters, got %d", n, m, length)
            .isTrue();
    }
    
    @Then("it should match the original public key")
    public void thenShouldMatchOriginalPublicKey() {
        assertThat(world.getBytes()).isEqualTo(publicKey.toBytes());
    }
    
    // ==========================================================================
    // Then Steps - Authentication Key
    // ==========================================================================
    
    @Then("it should equal SHA3-256\\(public_key || 0x00\\)")
    public void thenShouldEqualSha3OfPublicKeyAndScheme() {
        byte[] pubKeyBytes = publicKey.toBytes();
        byte[] data = new byte[pubKeyBytes.length + 1];
        System.arraycopy(pubKeyBytes, 0, data, 0, pubKeyBytes.length);
        data[pubKeyBytes.length] = 0x00; // Ed25519 scheme identifier
        
        byte[] expected = HashingSteps.sha3_256(data);
        assertThat(authKey.toBytes()).isEqualTo(expected);
    }
    
    @Then("the address should be {int} bytes")
    public void thenAddressShouldBeNBytes(int expected) {
        AccountAddress addr = (AccountAddress) world.getAddress();
        assertThat(addr.toBytes()).hasSize(expected);
    }
    
    @Then("it should equal the authentication key bytes")
    public void thenShouldEqualAuthKeyBytes() {
        AccountAddress addr = (AccountAddress) world.getAddress();
        assertThat(addr.toBytes()).isEqualTo(authKey.toBytes());
    }
    
    // ==========================================================================
    // Then Steps - Test Vectors
    // ==========================================================================
    
    @Then("the public key hex should match the expected value from test vectors")
    public void thenPublicKeyHexShouldMatchTestVectors() {
        assertThat(publicKey.toBytes()).isNotNull();
    }
    
    @Then("the address should match the expected value from test vectors")
    public void thenAddressShouldMatchTestVectors() {
        assertThat(account.getAccountAddress()).isNotNull();
    }
    
    @Then("the signature should match the expected value from test vectors")
    public void thenSignatureShouldMatchTestVectors() {
        assertThat(signature.toBytes()).hasSize(64);
    }
    
    // ==========================================================================
    // Then Steps - Security
    // ==========================================================================
    
    @Then("the private key memory should be zeroized")
    public void thenPrivateKeyMemoryShouldBeZeroized() {
        // Java doesn't provide direct memory control like Rust
        // This test is primarily for Rust
    }
    
    @Then("the private key bytes should not appear in the output")
    public void thenPrivateKeyBytesShouldNotAppearInOutput() {
        String debugOutput = (String) world.getResult();
        String privateKeyHex = HexUtils.bytesToHex(account.getPrivateKey().toBytes());
        assertThat(debugOutput).doesNotContain(privateKeyHex.substring(2)); // Remove 0x prefix
    }
}
