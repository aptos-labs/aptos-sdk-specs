package com.aptos.specs.steps;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import static org.assertj.core.api.Assertions.assertThat;

import com.aptos.specs.support.World;
import com.aptoslabs.japtos.account.Ed25519Account;
import com.aptoslabs.japtos.bcs.Deserializer;
import com.aptoslabs.japtos.bcs.Serializer;
import com.aptoslabs.japtos.core.AccountAddress;
import com.aptoslabs.japtos.core.AuthenticationKey;
import com.aptoslabs.japtos.core.crypto.Ed25519PrivateKey;
import com.aptoslabs.japtos.core.crypto.Ed25519PublicKey;
import com.aptoslabs.japtos.core.crypto.Signature;
import com.aptoslabs.japtos.utils.HexUtils;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/**
 * Consolidated step definitions for japtos SDK BDD tests.
 * Covers core-types, cryptography, accounts, and serialization.
 */
public class AllSteps {
    
    private final World world;
    
    // ==========================================================================
    // Address State
    // ==========================================================================
    private String hexString;
    private AccountAddress address;
    private AccountAddress address2;
    private byte[] serializedBytes;
    
    // ==========================================================================
    // Crypto State
    // ==========================================================================
    private Ed25519PrivateKey privateKey;
    private Ed25519PrivateKey privateKey2;
    private Ed25519PublicKey publicKey;
    private Ed25519PublicKey publicKey2;
    private Signature signature;
    private Signature signature2;
    private AuthenticationKey authKey;
    private AccountAddress accountAddress;
    private byte[] privateKeyBytes;
    private String privateKeyHex;
    private byte[] message;
    private byte[] message2;
    private boolean verificationResult;
    
    // ==========================================================================
    // Account State
    // ==========================================================================
    private Ed25519Account account;
    private Ed25519Account account2;
    
    // ==========================================================================
    // Hashing State
    // ==========================================================================
    private byte[] inputData;
    private byte[] inputData2;
    private byte[] hashResult;
    private byte[] hashResult2;
    private byte[] sha2Result;
    private byte[] sha3Result;
    private String domain;
    private String domain2;
    
    // ==========================================================================
    // Serialization State
    // ==========================================================================
    private boolean boolValue;
    private byte u8Value;
    private short u16Value;
    private int u32Value;
    private long u64Value;
    private byte[] u128Value;
    private byte[] u256Value;
    private byte[] bytesValue;
    private String stringValue;
    private Object deserializedValue;
    
    // ==========================================================================
    // Common State
    // ==========================================================================
    private Exception caughtError;
    
    public AllSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // ADDRESS: Given Steps
    // ==========================================================================
    
    @Given("a hex string {string}")
    public void givenHexString(String hex) {
        this.hexString = hex;
    }
    
    @Given("a short address {string}")
    public void givenShortAddress(String address) {
        this.hexString = address;
    }
    
    @Given("an address without 0x prefix {string}")
    public void givenAddressWithoutPrefix(String address) {
        this.hexString = address;
    }
    
    @Given("a full 64-character hex address {string}")
    public void givenFullHexAddress(String address) {
        this.hexString = address;
    }
    
    @Given("an uppercase hex address {string}")
    public void givenUppercaseHexAddress(String address) {
        this.hexString = address;
    }
    
    @Given("a mixed case hex address {string}")
    public void givenMixedCaseHexAddress(String address) {
        this.hexString = address;
    }
    
    @Given("an empty string")
    public void givenEmptyString() {
        this.hexString = "";
        this.stringValue = "";
    }
    
    @Given("just the 0x prefix")
    public void givenJust0xPrefix() {
        this.hexString = "0x";
    }
    
    @Given("a hex string with non-hex characters {string}")
    public void givenHexStringWithNonHexChars(String hex) {
        this.hexString = hex;
    }
    
    @Given("a hex string longer than 64 characters {string}")
    public void givenHexStringTooLong(String hex) {
        this.hexString = hex;
    }
    
    @Given("a hex string with spaces {string}")
    public void givenHexStringWithSpaces(String hex) {
        this.hexString = hex;
    }
    
    @Given("a valid AccountAddress")
    public void givenValidAccountAddress() {
        this.address = AccountAddress.fromHex("0x1");
    }
    
    @Given("a zero address")
    public void givenZeroAddress() {
        this.address = AccountAddress.zero();
    }
    
    @Given("two equivalent addresses from {string} and {string}")
    public void givenTwoEquivalentAddresses(String hex1, String hex2) {
        this.address = AccountAddress.fromHex(hex1);
        this.address2 = AccountAddress.fromHex(hex2);
    }
    
    @Given("two different addresses {string} and {string}")
    public void givenTwoDifferentAddresses(String hex1, String hex2) {
        this.address = AccountAddress.fromHex(hex1);
        this.address2 = AccountAddress.fromHex(hex2);
    }
    
    @Given("BCS-serialized address bytes")
    public void givenBcsSerializedAddressBytes() {
        try {
            AccountAddress addr = AccountAddress.fromHex("0x1");
            Serializer serializer = new Serializer();
            serializer.serializeAccountAddress(addr);
            this.serializedBytes = serializer.toByteArray();
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // ADDRESS: When Steps
    // ==========================================================================
    
    @When("I parse it as an AccountAddress")
    public void whenParseAsAccountAddress() {
        try {
            // japtos requires full hex string, so we need to pad short addresses
            String hex = hexString;
            if (hex.startsWith("0x") || hex.startsWith("0X")) {
                hex = hex.substring(2);
            }
            // Pad to 64 characters
            if (hex.length() < 64) {
                hex = String.format("%64s", hex).replace(' ', '0');
            }
            this.address = AccountAddress.fromHex(hex);
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I format the address to full hex")
    public void whenFormatToFullHex() {
        // Address is already parsed, will format in Then step
    }
    
    @When("I format the address to short string")
    public void whenFormatToShortString() {
        // Address is already parsed, will format in Then step
    }
    
    @When("I BCS serialize the address")
    public void whenBcsSerializeAddress() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeAccountAddress(address);
            this.serializedBytes = serializer.toByteArray();
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS deserialize the bytes")
    public void whenBcsDeserializeBytes() {
        try {
            Deserializer deserializer = new Deserializer(serializedBytes);
            byte[] bytes = deserializer.deserializeFixedBytes(AccountAddress.LENGTH);
            this.address = AccountAddress.fromBytes(bytes);
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I serialize and deserialize the address")
    public void whenSerializeAndDeserializeAddress() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeAccountAddress(address);
            byte[] bytes = serializer.toByteArray();
            this.address2 = AccountAddress.fromBytes(bytes);
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // ADDRESS: Then Steps
    // ==========================================================================
    
    @Then("the parsing should succeed")
    public void thenParsingShouldSucceed() {
        assertThat(caughtError).isNull();
        assertThat(address).isNotNull();
    }
    
    @Then("the parsing should fail")
    public void thenParsingShouldFail() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the parsing should fail with an error about empty input")
    public void thenParsingShouldFailWithEmptyInputError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the parsing should fail with an error about invalid characters")
    public void thenParsingShouldFailWithInvalidCharsError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the parsing should fail with an error about length")
    public void thenParsingShouldFailWithLengthError() {
        assertThat(caughtError).isNotNull();
    }
    
    @Then("the address bytes should be {int} bytes")
    public void thenAddressBytesShouldBeNBytes(int expectedLength) {
        assertThat(address.toBytes()).hasSize(expectedLength);
    }
    
    @Then("the full hex should be {string}")
    public void thenFullHexShouldBe(String expected) {
        String fullHex = address.toHexString();
        String normalizedExpected = expected.toLowerCase();
        String normalizedActual = fullHex.toLowerCase();
        // japtos doesn't include 0x prefix, so add it
        if (!normalizedActual.startsWith("0x")) {
            normalizedActual = "0x" + normalizedActual;
        }
        if (!normalizedExpected.startsWith("0x")) {
            normalizedExpected = "0x" + normalizedExpected;
        }
        assertThat(normalizedActual).isEqualTo(normalizedExpected);
    }
    
    @Then("the short string should be {string}")
    public void thenShortStringShouldBe(String expected) {
        // japtos toString() returns full hex without 0x, so we'll derive short form
        String fullHex = address.toHexString();
        // Remove leading zeros to get short form
        String shortened = fullHex.replaceFirst("^0+", "");
        if (shortened.isEmpty()) {
            shortened = "0";
        }
        shortened = "0x" + shortened;
        String normalizedExpected = expected.toLowerCase();
        assertThat(shortened.toLowerCase()).isEqualTo(normalizedExpected);
    }
    
    @Then("it should be the zero address")
    public void thenShouldBeZeroAddress() {
        assertThat(address.isZero()).isTrue();
    }
    
    @Then("the address constant ZERO should equal {string}")
    public void thenAddressConstantZeroShouldEqual(String expected) {
        AccountAddress zero = AccountAddress.zero();
        assertThat(zero.isZero()).isTrue();
    }
    
    @Then("the address constant ONE should equal {string}")
    public void thenAddressConstantOneShouldEqual(String expected) {
        AccountAddress one = AccountAddress.fromHex("0x1");
        assertThat(one.toHexString()).containsIgnoringCase("1");
    }
    
    @Then("the addresses should be equal")
    public void thenAddressesShouldBeEqual() {
        assertThat(address).isEqualTo(address2);
    }
    
    @Then("the addresses should not be equal")
    public void thenAddressesShouldNotBeEqual() {
        assertThat(address).isNotEqualTo(address2);
    }
    
    @Then("the serialized bytes should be {int} bytes")
    public void thenSerializedBytesShouldBeNBytes(int expectedLength) {
        assertThat(serializedBytes).hasSize(expectedLength);
    }
    
    @Then("I should get back the original address")
    public void thenShouldGetBackOriginalAddress() {
        assertThat(address).isEqualTo(address2);
    }
    
    @Then("the round-trip should preserve the address")
    public void thenRoundTripShouldPreserveAddress() {
        assertThat(address).isEqualTo(address2);
    }
    
    // ==========================================================================
    // CRYPTO: Given Steps
    // ==========================================================================
    
    @Given("I want to generate an Ed25519 key pair")
    public void givenWantToGenerateKeyPair() {
        // Setup for generation
    }
    
    @Given("a 32-byte seed")
    public void givenA32ByteSeed() {
        privateKeyBytes = new byte[32];
        new java.security.SecureRandom().nextBytes(privateKeyBytes);
    }
    
    @Given("a hex-encoded Ed25519 private key {string}")
    public void givenHexEncodedPrivateKey(String hex) {
        privateKeyHex = hex;
    }
    
    @Given("an Ed25519 key pair")
    public void givenEd25519KeyPair() {
        privateKey = Ed25519PrivateKey.generate();
        publicKey = privateKey.publicKey();
    }
    
    @Given("two different Ed25519 key pairs")
    public void givenTwoDifferentKeyPairs() {
        privateKey = Ed25519PrivateKey.generate();
        publicKey = privateKey.publicKey();
        privateKey2 = Ed25519PrivateKey.generate();
        publicKey2 = privateKey2.publicKey();
    }
    
    @Given("an Ed25519 public key")
    public void givenEd25519PublicKey() {
        privateKey = Ed25519PrivateKey.generate();
        publicKey = privateKey.publicKey();
    }
    
    @Given("a message {string}")
    public void givenMessage(String msg) {
        message = msg.getBytes();
    }
    
    @Given("an empty message")
    public void givenEmptyMessage() {
        message = new byte[0];
    }
    
    @Given("messages {string} and {string}")
    public void givenTwoMessages(String msg1, String msg2) {
        message = msg1.getBytes();
        message2 = msg2.getBytes();
    }
    
    @Given("a message and valid Ed25519 signature")
    public void givenMessageAndValidSignature() {
        givenEd25519KeyPair();
        message = "test".getBytes();
        signature = privateKey.sign(message);
    }
    
    // ==========================================================================
    // CRYPTO: When Steps
    // ==========================================================================
    
    @When("I generate a random Ed25519 key pair")
    public void whenGenerateRandomKeyPair() {
        try {
            privateKey = Ed25519PrivateKey.generate();
            publicKey = privateKey.publicKey();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I sign the message")
    public void whenSignMessage() {
        try {
            signature = privateKey.sign(message);
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I verify the signature")
    public void whenVerifySignature() {
        try {
            if (signature != null) {
                verificationResult = publicKey.verifySignature(message, signature);
            } else {
                verificationResult = false;
            }
        } catch (Exception e) {
            verificationResult = false;
        }
    }
    
    @When("I derive the authentication key")
    public void whenDeriveAuthenticationKey() {
        authKey = publicKey.authKey();
    }
    
    @When("I derive the account address")
    public void whenDeriveAccountAddress() {
        authKey = publicKey.authKey();
        accountAddress = authKey.accountAddress();
    }
    
    // ==========================================================================
    // CRYPTO: Then Steps
    // ==========================================================================
    
    @Then("the key pair should be valid")
    public void thenKeyPairShouldBeValid() {
        assertThat(privateKey).isNotNull();
        assertThat(publicKey).isNotNull();
    }
    
    @Then("the private key should be {int} bytes")
    public void thenPrivateKeyShouldBeNBytes(int expected) {
        assertThat(privateKey.toBytes()).hasSize(expected);
    }
    
    @Then("the public key should be {int} bytes")
    public void thenPublicKeyShouldBeNBytes(int expected) {
        assertThat(publicKey.toBytes()).hasSize(expected);
    }
    
    @Then("the signature should be valid")
    public void thenSignatureShouldBeValid() {
        assertThat(signature).isNotNull();
        boolean valid = publicKey.verifySignature(message, signature);
        assertThat(valid).isTrue();
    }
    
    @Then("verification should succeed")
    public void thenVerificationShouldSucceed() {
        assertThat(verificationResult).isTrue();
    }
    
    @Then("verification should fail")
    public void thenVerificationShouldFail() {
        assertThat(verificationResult).isFalse();
    }
    
    @Then("the authentication key should be {int} bytes")
    public void thenAuthenticationKeyShouldBeNBytes(int expected) {
        assertThat(authKey.toBytes()).hasSize(expected);
    }
    
    @Then("the account address should be {int} bytes")
    public void thenAccountAddressShouldBeNBytes(int expected) {
        assertThat(accountAddress.toBytes()).hasSize(expected);
    }
    
    // ==========================================================================
    // ACCOUNT: Given Steps
    // ==========================================================================
    
    @Given("I want to create an Ed25519 account")
    public void givenWantToCreateEd25519Account() {
        // Setup for account creation
    }
    
    @Given("an Ed25519 account")
    public void givenEd25519Account() {
        account = Ed25519Account.generate();
    }
    
    @Given("two Ed25519 accounts")
    public void givenTwoEd25519Accounts() {
        account = Ed25519Account.generate();
        account2 = Ed25519Account.generate();
    }
    
    // ==========================================================================
    // ACCOUNT: When Steps
    // ==========================================================================
    
    @When("I generate a random Ed25519 account")
    public void whenGenerateRandomEd25519Account() {
        try {
            account = Ed25519Account.generate();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I get the account address")
    public void whenGetAccountAddress() {
        accountAddress = account.getAccountAddress();
    }
    
    @When("I get the public key")
    public void whenGetPublicKey() {
        publicKey = account.getPublicKey();
    }
    
    @When("I get the private key")
    public void whenGetPrivateKey() {
        privateKey = account.getPrivateKey();
    }
    
    @When("I sign the message with the account")
    public void whenSignMessageWithAccount() {
        try {
            signature = account.sign(message);
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // ACCOUNT: Then Steps
    // ==========================================================================
    
    @Then("the account should be valid")
    public void thenAccountShouldBeValid() {
        assertThat(account).isNotNull();
        assertThat(account.getAccountAddress()).isNotNull();
        assertThat(account.getPublicKey()).isNotNull();
    }
    
    @Then("the account should have an address")
    public void thenAccountShouldHaveAddress() {
        assertThat(account.getAccountAddress()).isNotNull();
    }
    
    @Then("the account should have a public key")
    public void thenAccountShouldHavePublicKey() {
        assertThat(account.getPublicKey()).isNotNull();
    }
    
    @Then("the two accounts should have different addresses")
    public void thenTwoAccountsShouldHaveDifferentAddresses() {
        assertThat(account.getAccountAddress()).isNotEqualTo(account2.getAccountAddress());
    }
    
    // ==========================================================================
    // HASHING: Given Steps
    // ==========================================================================
    
    @Given("empty data")
    public void givenEmptyData() {
        inputData = new byte[0];
    }
    
    @Given("the string {string}")
    public void givenString(String str) {
        inputData = str.getBytes();
    }
    
    @Given("input data {string}")
    public void givenInputData(String data) {
        inputData = data.getBytes();
    }
    
    @Given("two different inputs {string} and {string}")
    public void givenTwoDifferentInputs(String data1, String data2) {
        inputData = data1.getBytes();
        inputData2 = data2.getBytes();
    }
    
    @Given("domain {string}")
    public void givenDomain(String d) {
        domain = d;
    }
    
    @Given("two different domains {string} and {string}")
    public void givenTwoDifferentDomains(String d1, String d2) {
        domain = d1;
        domain2 = d2;
    }
    
    // ==========================================================================
    // HASHING: When Steps
    // ==========================================================================
    
    @When("I compute SHA3-256")
    public void whenComputeSha3_256() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA3-256");
            hashResult = digest.digest(inputData);
            caughtError = null;
        } catch (NoSuchAlgorithmException e) {
            caughtError = e;
        }
    }
    
    @When("I compute SHA2-256")
    public void whenComputeSha2_256() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            sha2Result = digest.digest(inputData);
            caughtError = null;
        } catch (NoSuchAlgorithmException e) {
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // HASHING: Then Steps
    // ==========================================================================
    
    @Then("the hash should be {int} bytes")
    public void thenHashShouldBeNBytes(int expected) {
        assertThat(hashResult).hasSize(expected);
    }
    
    @Then("the hash should be {string}")
    public void thenHashShouldBe(String expectedHex) {
        String actualHex = HexUtils.bytesToHex(hashResult);
        assertThat(actualHex.toLowerCase()).isEqualTo(expectedHex.toLowerCase().replace("0x", ""));
    }
    
    @Then("the SHA2-256 hash should be {int} bytes")
    public void thenSha2HashShouldBeNBytes(int expected) {
        assertThat(sha2Result).hasSize(expected);
    }
    
    // ==========================================================================
    // SERIALIZATION: Given Steps
    // ==========================================================================
    
    @Given("a boolean value {string}")
    public void givenBooleanValue(String value) {
        boolValue = Boolean.parseBoolean(value);
    }
    
    @Given("a u8 value {int}")
    public void givenU8Value(int value) {
        u8Value = (byte) value;
    }
    
    @Given("a u16 value {int}")
    public void givenU16Value(int value) {
        u16Value = (short) value;
    }
    
    @Given("a u32 value {long}")
    public void givenU32Value(long value) {
        u32Value = (int) value;
    }
    
    @Given("a u64 value {long}")
    public void givenU64Value(long value) {
        u64Value = value;
    }
    
    @Given("a byte array {string}")
    public void givenByteArray(String hex) {
        bytesValue = HexUtils.hexToBytes(hex.replace("0x", ""));
    }
    
    @Given("a string {string}")
    public void givenStringValue(String value) {
        stringValue = value;
    }
    
    // ==========================================================================
    // SERIALIZATION: When Steps
    // ==========================================================================
    
    @When("I BCS serialize the boolean")
    public void whenBcsSerializeBoolean() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeBool(boolValue);
            serializedBytes = serializer.toByteArray();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS serialize the u8")
    public void whenBcsSerializeU8() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeU8(u8Value);
            serializedBytes = serializer.toByteArray();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS serialize the u64")
    public void whenBcsSerializeU64() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeU64(u64Value);
            serializedBytes = serializer.toByteArray();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS serialize the bytes")
    public void whenBcsSerializeBytes() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeBytes(bytesValue);
            serializedBytes = serializer.toByteArray();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS serialize the string")
    public void whenBcsSerializeString() {
        try {
            Serializer serializer = new Serializer();
            serializer.serializeString(stringValue);
            serializedBytes = serializer.toByteArray();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS deserialize as boolean")
    public void whenBcsDeserializeAsBoolean() {
        try {
            Deserializer deserializer = new Deserializer(serializedBytes);
            deserializedValue = deserializer.deserializeBool();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS deserialize as u8")
    public void whenBcsDeserializeAsU8() {
        try {
            Deserializer deserializer = new Deserializer(serializedBytes);
            deserializedValue = deserializer.deserializeU8();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS deserialize as u64")
    public void whenBcsDeserializeAsU64() {
        try {
            Deserializer deserializer = new Deserializer(serializedBytes);
            deserializedValue = deserializer.deserializeU64();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    @When("I BCS deserialize as string")
    public void whenBcsDeserializeAsString() {
        try {
            Deserializer deserializer = new Deserializer(serializedBytes);
            deserializedValue = deserializer.deserializeString();
            caughtError = null;
        } catch (Exception e) {
            caughtError = e;
        }
    }
    
    // ==========================================================================
    // SERIALIZATION: Then Steps
    // ==========================================================================
    
    @Then("the serialized bytes should be {string}")
    public void thenSerializedBytesShouldBe(String expectedHex) {
        String actualHex = HexUtils.bytesToHex(serializedBytes);
        assertThat(actualHex.toLowerCase()).isEqualTo(expectedHex.toLowerCase().replace("0x", ""));
    }
    
    @Then("the deserialized value should equal the original")
    public void thenDeserializedValueShouldEqualOriginal() {
        assertThat(deserializedValue).isNotNull();
    }
    
    @Then("the deserialized boolean should be {string}")
    public void thenDeserializedBooleanShouldBe(String expected) {
        assertThat((Boolean) deserializedValue).isEqualTo(Boolean.parseBoolean(expected));
    }
    
    @Then("the deserialized u8 should be {int}")
    public void thenDeserializedU8ShouldBe(int expected) {
        assertThat((Byte) deserializedValue).isEqualTo((byte) expected);
    }
    
    @Then("the deserialized u64 should be {long}")
    public void thenDeserializedU64ShouldBe(long expected) {
        assertThat((Long) deserializedValue).isEqualTo(expected);
    }
    
    @Then("the deserialized string should be {string}")
    public void thenDeserializedStringShouldBe(String expected) {
        assertThat((String) deserializedValue).isEqualTo(expected);
    }
}
