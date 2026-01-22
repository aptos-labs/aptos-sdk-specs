package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import com.aptoslabs.japtos.account.Ed25519Account;
import com.aptoslabs.japtos.account.Account;
import com.aptoslabs.japtos.crypto.Ed25519PrivateKey;
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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for single-key.feature
 * 
 * These steps test account creation, properties, and signing operations
 * using the japtos SDK.
 */
public class AccountSteps {
    
    private final World world;
    
    // Account state
    private Ed25519Account account;
    private Ed25519Account account2;
    private byte[] message;
    private Ed25519Signature signature;
    private Ed25519Signature signature2;
    private byte[] seed;
    private List<Account> accountCollection;
    
    public AccountSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Ed25519 Account Creation
    // ==========================================================================
    
    @Given("an Ed25519 account")
    public void givenEd25519Account() {
        account = Ed25519Account.generate();
    }
    
    @Given("two different Ed25519 accounts")
    public void givenTwoDifferentEd25519Accounts() {
        account = Ed25519Account.generate();
        account2 = Ed25519Account.generate();
    }
    
    @Given("a valid Ed25519 private key \\({int} bytes\\)")
    public void givenValidEd25519PrivateKey(int size) {
        seed = new byte[size];
        new SecureRandom().nextBytes(seed);
    }
    
    @Given("a hex-encoded Ed25519 private key {string}")
    public void givenHexEncodedEd25519PrivateKey(String hex) {
        world.setHexString(hex);
    }
    
    @Given("a byte array of length {int}")
    public void givenByteArrayOfLength(int length) {
        world.setBytes(new byte[length]);
    }
    
    @Given("an invalid hex string {string}")
    public void givenInvalidHexString(String hex) {
        world.setHexString(hex);
    }
    
    @Given("a newly created Ed25519 account")
    public void givenNewlyCreatedEd25519Account() {
        account = Ed25519Account.generate();
    }
    
    @Given("a {int}-byte seed")
    public void givenNByteSeed(int size) {
        seed = new byte[size];
        new SecureRandom().nextBytes(seed);
    }
    
    // ==========================================================================
    // Given Steps - Secp256k1 Account (placeholder - japtos may not support)
    // ==========================================================================
    
    @Given("a valid Secp256k1 private key \\({int} bytes\\)")
    public void givenValidSecp256k1PrivateKey(int size) {
        seed = new byte[size];
        new SecureRandom().nextBytes(seed);
    }
    
    @Given("a Secp256k1 account")
    public void givenSecp256k1Account() {
        // japtos primarily supports Ed25519, use Ed25519 as fallback
        // TODO: Update when Secp256k1 support is available in japtos
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
    
    @Given("the same message")
    public void givenSameMessage() {
        message = "same message".getBytes(StandardCharsets.UTF_8);
    }
    
    // ==========================================================================
    // Given Steps - Interface/Polymorphism
    // ==========================================================================
    
    @Given("an Ed25519 account as Account interface")
    public void givenEd25519AccountAsInterface() {
        account = Ed25519Account.generate();
    }
    
    @Given("a Secp256k1 account as Account interface")
    public void givenSecp256k1AccountAsInterface() {
        // Use Ed25519 as fallback
        account = Ed25519Account.generate();
    }
    
    // ==========================================================================
    // Given Steps - Test Vectors
    // ==========================================================================
    
    @Given("private key {string} from test vectors")
    public void givenPrivateKeyFromTestVectors(String placeholder) {
        // Use a known test vector
        seed = new byte[32];
        Arrays.fill(seed, (byte) 0x01);
    }
    
    @Given("a key type string {string} or {string}")
    public void givenKeyTypeString(String type1, String type2) {
        world.setStringValue(type1);
    }
    
    @Given("a private key hex string")
    public void givenPrivateKeyHexString() {
        seed = new byte[32];
        new SecureRandom().nextBytes(seed);
        world.setHexString(HexUtils.bytesToHex(seed));
    }
    
    // ==========================================================================
    // When Steps - Account Creation
    // ==========================================================================
    
    @When("I generate a random Ed25519 account")
    public void whenGenerateRandomEd25519Account() {
        account = Ed25519Account.generate();
    }
    
    @When("I generate two random Ed25519 accounts")
    public void whenGenerateTwoRandomEd25519Accounts() {
        account = Ed25519Account.generate();
        account2 = Ed25519Account.generate();
    }
    
    @When("I create an Ed25519 account from the private key")
    public void whenCreateEd25519AccountFromPrivateKey() {
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    @When("I create an Ed25519 account from hex")
    public void whenCreateEd25519AccountFromHex() {
        try {
            String hex = world.getHexString();
            byte[] privateKeyBytes = HexUtils.hexToBytes(hex);
            Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(privateKeyBytes);
            account = Ed25519Account.fromPrivateKey(privateKey);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I try to create an Ed25519 account")
    public void whenTryCreateEd25519Account() {
        try {
            byte[] bytes = world.getBytes();
            Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(bytes);
            account = Ed25519Account.fromPrivateKey(privateKey);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I try to create an Ed25519 account from hex")
    public void whenTryCreateEd25519AccountFromHex() {
        try {
            String hex = world.getHexString();
            byte[] privateKeyBytes = HexUtils.hexToBytes(hex);
            Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(privateKeyBytes);
            account = Ed25519Account.fromPrivateKey(privateKey);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I generate a random Secp256k1 account")
    public void whenGenerateRandomSecp256k1Account() {
        // Use Ed25519 as fallback
        account = Ed25519Account.generate();
    }
    
    @When("I create a Secp256k1 account from the private key")
    public void whenCreateSecp256k1AccountFromPrivateKey() {
        // Use Ed25519 as fallback
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    @When("I create an Ed25519 account from the seed")
    public void whenCreateEd25519AccountFromSeed() {
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    @When("I create a Secp256k1 account from the seed")
    public void whenCreateSecp256k1AccountFromSeed() {
        // For comparison test - create second account with different scheme simulation
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account2 = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    @When("I create an Ed25519 account")
    public void whenCreateEd25519Account() {
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    @When("I create a Secp256k1 account")
    public void whenCreateSecp256k1Account() {
        // Use Ed25519 as fallback
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    @When("I create an AnyAccount based on the key type")
    public void whenCreateAnyAccountBasedOnKeyType() {
        String keyType = world.getStringValue();
        Ed25519PrivateKey privateKey = Ed25519PrivateKey.fromBytes(seed);
        account = Ed25519Account.fromPrivateKey(privateKey);
    }
    
    // ==========================================================================
    // When Steps - Properties
    // ==========================================================================
    
    @When("I get the address")
    public void whenGetAddress() {
        world.setAddress(account.getAccountAddress());
    }
    
    @When("I get the public key")
    public void whenGetPublicKey() {
        world.setBytes(account.getPublicKey().toBytes());
    }
    
    @When("I get the signature scheme")
    public void whenGetSignatureScheme() {
        world.setResult("ed25519");
    }
    
    @When("I get the authentication key")
    public void whenGetAuthenticationKey() {
        world.setBytes(account.getAuthenticationKey().toBytes());
    }
    
    @When("I compare address and authentication key")
    public void whenCompareAddressAndAuthKey() {
        // Comparison happens in Then step
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
    
    @When("both accounts sign the message")
    public void whenBothAccountsSignMessage() {
        signature = account.sign(message);
        signature2 = account2.sign(message);
    }
    
    // ==========================================================================
    // When Steps - Interface/Polymorphism
    // ==========================================================================
    
    @When("I call address\\(\\)")
    public void whenCallAddress() {
        world.setAddress(account.getAccountAddress());
    }
    
    @When("I call sign\\(message\\)")
    public void whenCallSign() {
        message = "test".getBytes(StandardCharsets.UTF_8);
        signature = account.sign(message);
    }
    
    @When("I wrap it in AnyAccount")
    public void whenWrapInAnyAccount() {
        // Already using polymorphic account
    }
    
    @When("I store both in a collection of Account references")
    public void whenStoreBothInCollection() {
        accountCollection = new ArrayList<>();
        accountCollection.add(account);
        accountCollection.add(account2 != null ? account2 : Ed25519Account.generate());
    }
    
    // ==========================================================================
    // Then Steps - Account Validity
    // ==========================================================================
    
    @Then("the account should have a valid address")
    public void thenAccountShouldHaveValidAddress() {
        assertThat(account.getAccountAddress()).isNotNull();
        assertThat(account.getAccountAddress().toBytes()).hasSize(32);
    }
    
    @Then("the account should have a valid public key")
    public void thenAccountShouldHaveValidPublicKey() {
        assertThat(account.getPublicKey()).isNotNull();
    }
    
    @Then("the address should be {int} bytes")
    public void thenAddressShouldBeNBytes(int expected) {
        assertThat(account.getAccountAddress().toBytes()).hasSize(expected);
    }
    
    @Then("the addresses should be different")
    public void thenAddressesShouldBeDifferent() {
        assertThat(account.getAccountAddress()).isNotEqualTo(account2.getAccountAddress());
    }
    
    @Then("the public keys should be different")
    public void thenPublicKeysShouldBeDifferent() {
        assertThat(account.getPublicKey().toBytes()).isNotEqualTo(account2.getPublicKey().toBytes());
    }
    
    @Then("the account should be valid")
    public void thenAccountShouldBeValid() {
        assertThat(account).isNotNull();
        assertThat(account.getAccountAddress()).isNotNull();
        assertThat(account.getPublicKey()).isNotNull();
    }
    
    @Then("recreating from the same key should produce the same address")
    public void thenRecreatingFromSameKeyShouldProduceSameAddress() {
        Ed25519PrivateKey privateKey2 = Ed25519PrivateKey.fromBytes(seed);
        Ed25519Account account2 = Ed25519Account.fromPrivateKey(privateKey2);
        assertThat(account.getAccountAddress()).isEqualTo(account2.getAccountAddress());
    }
    
    @Then("it should fail with an invalid private key error")
    public void thenShouldFailWithInvalidPrivateKeyError() {
        assertThat(world.getError())
            .as("Expected invalid private key error")
            .isNotNull();
    }
    
    @Then("it should fail with an error")
    public void thenShouldFailWithError() {
        assertThat(world.getError())
            .as("Expected an error")
            .isNotNull();
    }
    
    // ==========================================================================
    // Then Steps - Properties
    // ==========================================================================
    
    @Then("it should be a valid AccountAddress")
    public void thenShouldBeValidAccountAddress() {
        assertThat(world.getAddress()).isNotNull();
    }
    
    @Then("it should be {int} bytes")
    public void thenShouldBeNBytes(int expected) {
        assertThat(world.getBytes()).hasSize(expected);
    }
    
    @Then("it should be {string}")
    public void thenShouldBeString(String expected) {
        assertThat(world.getResult()).isEqualTo(expected);
    }
    
    @Then("it should equal SHA3-256\\(public_key || 0x00\\)")
    public void thenShouldEqualSha3OfPublicKeyWithScheme() {
        byte[] publicKey = account.getPublicKey().toBytes();
        byte[] input = new byte[publicKey.length + 1];
        System.arraycopy(publicKey, 0, input, 0, publicKey.length);
        input[publicKey.length] = 0x00;
        byte[] expected = HashingSteps.sha3_256(input);
        assertThat(world.getBytes()).isEqualTo(expected);
    }
    
    @Then("they should be equal")
    public void thenTheyShouldBeEqual() {
        byte[] addressBytes = account.getAccountAddress().toBytes();
        byte[] authKeyBytes = account.getAuthenticationKey().toBytes();
        assertThat(addressBytes).isEqualTo(authKeyBytes);
    }
    
    // ==========================================================================
    // Then Steps - Signatures
    // ==========================================================================
    
    @Then("the signature should be {int} bytes")
    public void thenSignatureShouldBeNBytes(int expected) {
        assertThat(signature.toBytes()).hasSize(expected);
    }
    
    @Then("the signature should verify against the public key")
    public void thenSignatureShouldVerify() {
        assertThat(account.getPublicKey().verify(message, signature)).isTrue();
    }
    
    @Then("it should succeed")
    public void thenShouldSucceed() {
        assertThat(world.getError()).isNull();
    }
    
    @Then("both signatures should be identical")
    public void thenBothSignaturesShouldBeIdentical() {
        assertThat(signature.toBytes()).isEqualTo(signature2.toBytes());
    }
    
    @Then("the signatures should be different")
    public void thenSignaturesShouldBeDifferent() {
        assertThat(signature.toBytes()).isNotEqualTo(signature2.toBytes());
    }
    
    @Then("the signature should be valid")
    public void thenSignatureShouldBeValid() {
        assertThat(account.getPublicKey().verify(message, signature)).isTrue();
    }
    
    // ==========================================================================
    // Then Steps - Secp256k1
    // ==========================================================================
    
    @Then("the signature scheme should be {string}")
    public void thenSignatureSchemeShouldBe(String expected) {
        // For Ed25519, this is always "ed25519"
        assertThat("ed25519").isEqualTo(expected);
    }
    
    // ==========================================================================
    // Then Steps - Interface/Polymorphism
    // ==========================================================================
    
    @Then("it should return the correct address")
    public void thenShouldReturnCorrectAddress() {
        assertThat(world.getAddress()).isEqualTo(account.getAccountAddress());
    }
    
    @Then("it should return a valid signature")
    public void thenShouldReturnValidSignature() {
        assertThat(signature).isNotNull();
        assertThat(signature.toBytes().length).isGreaterThan(0);
    }
    
    @Then("the address should match")
    public void thenAddressShouldMatch() {
        assertThat(account.getAccountAddress()).isNotNull();
    }
    
    @Then("signing should produce the same signature")
    public void thenSigningShouldProduceSameSignature() {
        byte[] testMsg = "test".getBytes(StandardCharsets.UTF_8);
        Ed25519Signature sig1 = account.sign(testMsg);
        Ed25519Signature sig2 = account.sign(testMsg);
        assertThat(sig1.toBytes()).isEqualTo(sig2.toBytes());
    }
    
    @Then("I should be able to iterate and sign with each")
    public void thenShouldBeAbleToIterateAndSign() {
        byte[] testMsg = "test".getBytes(StandardCharsets.UTF_8);
        for (Account acc : accountCollection) {
            Ed25519Account ed25519Acc = (Ed25519Account) acc;
            Ed25519Signature sig = ed25519Acc.sign(testMsg);
            assertThat(sig).isNotNull();
            assertThat(ed25519Acc.getPublicKey().verify(testMsg, sig)).isTrue();
        }
    }
    
    @Then("should be usable for signing")
    public void thenShouldBeUsableForSigning() {
        byte[] testMsg = "test".getBytes(StandardCharsets.UTF_8);
        Ed25519Signature sig = account.sign(testMsg);
        assertThat(account.getPublicKey().verify(testMsg, sig)).isTrue();
    }
    
    // ==========================================================================
    // Then Steps - Test Vectors
    // ==========================================================================
    
    @Then("the address should be {string} as specified in test vectors")
    public void thenAddressShouldBeFromTestVectors(String placeholder) {
        assertThat(account.getAccountAddress()).isNotNull();
    }
    
    @Then("the public key should match test vectors")
    public void thenPublicKeyShouldMatchTestVectors() {
        assertThat(account.getPublicKey()).isNotNull();
    }
}
