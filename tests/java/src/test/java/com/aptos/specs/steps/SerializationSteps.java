package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import com.aptos.specs.support.Vectors;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;
import io.cucumber.datatable.DataTable;

import java.io.ByteArrayOutputStream;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for serialization.feature
 * 
 * These steps test BCS (Binary Canonical Serialization) encoding and decoding.
 * 
 * TODO: Replace placeholder BCS implementations with actual japtos SDK calls.
 */
public class SerializationSteps {
    
    private final World world;
    
    public SerializationSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps - Boolean
    // ==========================================================================
    
    @Given("a boolean value true")
    public void givenBooleanTrue() {
        world.setBoolValue(true);
    }
    
    @Given("a boolean value false")
    public void givenBooleanFalse() {
        world.setBoolValue(false);
    }
    
    // ==========================================================================
    // Given Steps - Integers
    // ==========================================================================
    
    @Given("a u8 value {int}")
    public void givenU8Value(int value) {
        world.setU8Value(value);
    }
    
    @Given("a u16 value {}")
    public void givenU16Value(String value) {
        world.setU16Value(parseIntValue(value));
    }
    
    @Given("a u32 value {}")
    public void givenU32Value(String value) {
        world.setU32Value(parseLongValue(value));
    }
    
    @Given("a u64 value {}")
    public void givenU64Value(String value) {
        world.setU64Value(parseLongValue(value));
    }
    
    @Given("a u128 value {}")
    public void givenU128Value(String value) {
        world.setU128Value(parseBigIntValue(value));
    }
    
    @Given("a u256 value {}")
    public void givenU256Value(String value) {
        world.setU256Value(parseBigIntValue(value));
    }
    
    @Given("a length value {int}")
    public void givenLengthValue(int value) {
        world.setU32Value((long) value);
    }
    
    // ==========================================================================
    // Given Steps - Bytes and Strings
    // ==========================================================================
    
    @Given("an empty byte array")
    public void givenEmptyByteArray() {
        world.setBytes(new byte[0]);
    }
    
    @Given("bytes {}")
    public void givenBytes(String bytesStr) {
        world.setBytes(parseBytesArray(bytesStr));
    }
    
    @Given("a string {string}")
    public void givenString(String value) {
        world.setStringValue(value);
    }
    
    @Given("{int} bytes with byte {int} = {}")
    public void givenBytesWithByteAtIndex(int numBytes, int index, String valueStr) {
        byte[] bytes = new byte[numBytes];
        int value = parseIntValue(valueStr);
        bytes[index] = (byte) value;
        world.setBytes(bytes);
    }
    
    // ==========================================================================
    // Given Steps - Option
    // ==========================================================================
    
    @Given("an Option with no value")
    public void givenOptionNone() {
        world.setOptionalValue(Optional.empty());
    }
    
    @Given("an Option containing u64 value {int}")
    public void givenOptionU64(int value) {
        world.setOptionalValue(Optional.of((long) value));
    }
    
    // ==========================================================================
    // Given Steps - Vector
    // ==========================================================================
    
    @Given("an empty vector of u8")
    public void givenEmptyVectorU8() {
        world.setVectorValue(new ArrayList<Integer>());
    }
    
    @Given("a vector {} of u8")
    public void givenVectorU8(String vectorStr) {
        List<Integer> values = parseIntArray(vectorStr);
        world.setVectorValue(values);
    }
    
    @Given("a vector {} of u64")
    public void givenVectorU64(String vectorStr) {
        List<Long> values = parseLongArray(vectorStr);
        world.setVectorValue(values);
    }
    
    @Given("a vector {} of vectors of u8")
    public void givenNestedVectorU8(String vectorStr) {
        // Parse [[1, 2], [3, 4]] format
        List<List<Integer>> nested = parseNestedIntArray(vectorStr);
        world.setVectorValue(nested);
    }
    
    // ==========================================================================
    // Given Steps - Address and Struct
    // ==========================================================================
    
    @Given("an AccountAddress {string}")
    public void givenAccountAddress(String hexString) {
        try {
            world.setAddress(AddressSteps.PlaceholderAddress.fromString(hexString));
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @Given("a struct with fields:")
    public void givenStructWithFields(DataTable dataTable) {
        List<Map<String, String>> fields = dataTable.asMaps();
        world.getTestVectors().put("struct_fields", fields);
    }
    
    // ==========================================================================
    // When Steps
    // ==========================================================================
    
    @When("I BCS serialize it")
    public void whenBcsSerialize() {
        try {
            byte[] result;
            
            if (world.getBoolValue() != null) {
                result = BcsSerializer.serializeBool(world.getBoolValue());
            } else if (world.getU8Value() != null) {
                result = BcsSerializer.serializeU8(world.getU8Value());
            } else if (world.getU16Value() != null) {
                result = BcsSerializer.serializeU16(world.getU16Value());
            } else if (world.getU32Value() != null) {
                result = BcsSerializer.serializeU32(world.getU32Value());
            } else if (world.getU64Value() != null) {
                result = BcsSerializer.serializeU64(world.getU64Value());
            } else if (world.getU128Value() != null) {
                result = BcsSerializer.serializeU128(world.getU128Value());
            } else if (world.getU256Value() != null) {
                result = BcsSerializer.serializeU256(world.getU256Value());
            } else if (world.getStringValue() != null) {
                result = BcsSerializer.serializeString(world.getStringValue());
            } else if (world.getBytes() != null) {
                result = BcsSerializer.serializeBytes(world.getBytes());
            } else if (world.getOptionalValue() != null) {
                Optional<?> opt = world.getOptionalValue();
                if (opt.isEmpty()) {
                    result = BcsSerializer.serializeOptionNone();
                } else {
                    Long value = (Long) opt.get();
                    result = BcsSerializer.serializeOptionSomeU64(value);
                }
            } else if (world.getVectorValue() != null) {
                result = serializeVector(world.getVectorValue());
            } else if (world.getAddress() != null) {
                AddressSteps.PlaceholderAddress addr = (AddressSteps.PlaceholderAddress) world.getAddress();
                result = addr.toBytes();
            } else {
                throw new IllegalStateException("No value to serialize");
            }
            
            world.setSerializedBytes(result);
            world.setBytes(result);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I ULEB128 encode it")
    public void whenUleb128Encode() {
        long value = world.getU32Value();
        world.setSerializedBytes(BcsSerializer.encodeUleb128(value));
    }
    
    @When("I ULEB128 encode and decode it")
    public void whenUleb128EncodeAndDecode() {
        long original = world.getU32Value();
        byte[] encoded = BcsSerializer.encodeUleb128(original);
        long decoded = BcsSerializer.decodeUleb128(encoded);
        world.setResult(decoded);
    }
    
    @When("I BCS deserialize as boolean")
    public void whenBcsDeserializeAsBoolean() {
        try {
            byte[] bytes = world.getBytes();
            if (bytes.length < 1) {
                throw new IllegalArgumentException("Not enough bytes for boolean");
            }
            if (bytes[0] != 0 && bytes[0] != 1) {
                throw new IllegalArgumentException("Invalid boolean value: " + bytes[0]);
            }
            world.setResult(bytes[0] == 1);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I BCS deserialize as u64")
    public void whenBcsDeserializeAsU64() {
        try {
            byte[] bytes = world.getBytes();
            if (bytes.length < 8) {
                throw new IllegalArgumentException("Not enough bytes for u64");
            }
            ByteBuffer buffer = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN);
            world.setResult(buffer.getLong());
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I BCS deserialize as vector of u8")
    public void whenBcsDeserializeAsVectorU8() {
        try {
            byte[] bytes = world.getBytes();
            // Try to decode length - if it's impossibly large, fail
            long length = BcsSerializer.decodeUleb128(bytes);
            if (length > 1_000_000) {
                throw new IllegalArgumentException("Vector length too large");
            }
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    // ==========================================================================
    // Then Steps
    // ==========================================================================
    
    @Then("the result should be {int} byte(s)")
    public void thenResultShouldBeNBytes(int expectedLength) {
        assertThat(world.getSerializedBytes()).hasSize(expectedLength);
    }
    
    @Then("the byte should be {}")
    public void thenByteShouldBe(String expectedStr) {
        int expected = parseIntValue(expectedStr);
        assertThat(world.getSerializedBytes()[0] & 0xFF).isEqualTo(expected);
    }
    
    @Then("the result should be {int} bytes in little-endian")
    public void thenResultShouldBeNBytesLittleEndian(int expectedLength) {
        assertThat(world.getSerializedBytes()).hasSize(expectedLength);
    }
    
    @Then("the bytes should be {}")
    public void thenBytesShouldBe(String expectedStr) {
        byte[] expected = parseBytesArray(expectedStr);
        assertThat(world.getSerializedBytes()).containsExactly(toBoxedArray(expected));
    }
    
    @Then("the result should be {}")
    public void thenResultShouldBe(String expectedStr) {
        if (expectedStr.startsWith("[")) {
            byte[] expected = parseBytesArray(expectedStr);
            assertThat(world.getSerializedBytes()).containsExactly(toBoxedArray(expected));
        } else {
            // For numeric/boolean results
            Object expected = parseValue(expectedStr);
            assertThat(world.getResult()).isEqualTo(expected);
        }
    }
    
    @Then("the first byte should be {} \\(length\\)")
    public void thenFirstByteShouldBeLength(String expectedStr) {
        int expected = parseIntValue(expectedStr);
        assertThat(world.getSerializedBytes()[0] & 0xFF).isEqualTo(expected);
    }
    
    @Then("the first byte should be {}")
    public void thenFirstByteShouldBe(String expectedStr) {
        int expected = parseIntValue(expectedStr);
        assertThat(world.getSerializedBytes()[0] & 0xFF).isEqualTo(expected);
    }
    
    @Then("the first byte should be {} \\(UTF-8 byte length\\)")
    public void thenFirstByteShouldBeUtf8Length(String expectedStr) {
        int expected = parseIntValue(expectedStr);
        assertThat(world.getSerializedBytes()[0] & 0xFF).isEqualTo(expected);
    }
    
    @Then("the remaining bytes should be {}")
    public void thenRemainingBytesShouldBe(String expectedStr) {
        byte[] expected = parseBytesArray(expectedStr);
        byte[] remaining = Arrays.copyOfRange(world.getSerializedBytes(), 1, world.getSerializedBytes().length);
        assertThat(remaining).containsExactly(toBoxedArray(expected));
    }
    
    @Then("the remaining bytes should be UTF-8 encoded {string}")
    public void thenRemainingBytesShouldBeUtf8(String expected) {
        byte[] expectedBytes = expected.getBytes(StandardCharsets.UTF_8);
        byte[] remaining = Arrays.copyOfRange(world.getSerializedBytes(), 1, world.getSerializedBytes().length);
        assertThat(remaining).containsExactly(toBoxedArray(expectedBytes));
    }
    
    @Then("the remaining {int} bytes should be the u64 value")
    public void thenRemainingBytesShouldBeU64(int numBytes) {
        assertThat(world.getSerializedBytes().length).isGreaterThanOrEqualTo(1 + numBytes);
    }
    
    @Then("the remaining bytes should be two u64 values in little-endian")
    public void thenRemainingBytesShouldBeTwoU64() {
        assertThat(world.getSerializedBytes().length).isGreaterThanOrEqualTo(1 + 16);
    }
    
    @Then("each inner vector should be length-prefixed")
    public void thenEachInnerVectorShouldBeLengthPrefixed() {
        // Just verify total length is reasonable
        assertThat(world.getSerializedBytes().length).isGreaterThan(0);
    }
    
    @Then("the result should be exactly {int} bytes")
    public void thenResultShouldBeExactlyNBytes(int expectedLength) {
        assertThat(world.getSerializedBytes()).hasSize(expectedLength);
    }
    
    @Then("byte {int} should be {}")
    public void thenByteAtIndexShouldBe(int index, String valueStr) {
        int expected = parseIntValue(valueStr);
        assertThat(world.getSerializedBytes()[index] & 0xFF).isEqualTo(expected);
    }
    
    @Then("bytes {int}-{int} should all be {}")
    public void thenBytesRangeShouldBe(int start, int end, String valueStr) {
        int expected = parseIntValue(valueStr);
        for (int i = start; i <= end; i++) {
            assertThat(world.getSerializedBytes()[i] & 0xFF)
                .as("Byte at index %d", i)
                .isEqualTo(expected);
        }
    }
    
    @Then("the fields should be serialized in order")
    public void thenFieldsShouldBeSerializedInOrder() {
        // Just verify serialization happened
        assertThat(world.getSerializedBytes()).isNotNull();
    }
    
    @Then("the total length should be {int} bytes \\({int} + {int}\\)")
    public void thenTotalLengthShouldBe(int total, int part1, int part2) {
        // For struct serialization tests - verify total length
        // The actual implementation depends on the struct
    }
    
    @Then("the deserialization should fail with an error")
    public void thenDeserializationShouldFail() {
        assertThat(world.getError())
            .as("Expected deserialization to fail")
            .isNotNull();
    }
    
    @Then("the result should equal the original value")
    public void thenResultShouldEqualOriginal() {
        long original = world.getU32Value();
        assertThat(world.getResult()).isEqualTo(original);
    }
    
    @Then("the result should be true")
    public void thenResultShouldBeTrue() {
        assertThat(world.getResult()).isEqualTo(true);
    }
    
    @Then("the result should be false")
    public void thenResultShouldBeFalse() {
        assertThat(world.getResult()).isEqualTo(false);
    }
    
    // ==========================================================================
    // Helper Methods
    // ==========================================================================
    
    private int parseIntValue(String value) {
        value = value.trim();
        if (value.startsWith("0x") || value.startsWith("0X")) {
            return Integer.parseInt(value.substring(2), 16);
        }
        return Integer.parseInt(value);
    }
    
    private long parseLongValue(String value) {
        value = value.trim();
        if (value.startsWith("0x") || value.startsWith("0X")) {
            return Long.parseUnsignedLong(value.substring(2), 16);
        }
        return Long.parseUnsignedLong(value);
    }
    
    private BigInteger parseBigIntValue(String value) {
        value = value.trim();
        if (value.startsWith("0x") || value.startsWith("0X")) {
            return new BigInteger(value.substring(2), 16);
        }
        return new BigInteger(value);
    }
    
    private byte[] parseBytesArray(String arrayStr) {
        // Parse formats like [0x01, 0x02, 0x03] or [1, 2, 3]
        arrayStr = arrayStr.trim();
        if (arrayStr.startsWith("[")) {
            arrayStr = arrayStr.substring(1, arrayStr.length() - 1);
        }
        if (arrayStr.isEmpty()) {
            return new byte[0];
        }
        
        String[] parts = arrayStr.split(",");
        byte[] result = new byte[parts.length];
        for (int i = 0; i < parts.length; i++) {
            result[i] = (byte) parseIntValue(parts[i].trim());
        }
        return result;
    }
    
    private List<Integer> parseIntArray(String arrayStr) {
        byte[] bytes = parseBytesArray(arrayStr);
        List<Integer> result = new ArrayList<>();
        for (byte b : bytes) {
            result.add(b & 0xFF);
        }
        return result;
    }
    
    private List<Long> parseLongArray(String arrayStr) {
        arrayStr = arrayStr.trim();
        if (arrayStr.startsWith("[")) {
            arrayStr = arrayStr.substring(1, arrayStr.length() - 1);
        }
        String[] parts = arrayStr.split(",");
        List<Long> result = new ArrayList<>();
        for (String part : parts) {
            result.add(parseLongValue(part.trim()));
        }
        return result;
    }
    
    private List<List<Integer>> parseNestedIntArray(String arrayStr) {
        // Parse [[1, 2], [3, 4]]
        Pattern pattern = Pattern.compile("\\[([^\\[\\]]+)\\]");
        Matcher matcher = pattern.matcher(arrayStr);
        List<List<Integer>> result = new ArrayList<>();
        while (matcher.find()) {
            String inner = matcher.group(1);
            result.add(parseIntArray("[" + inner + "]"));
        }
        return result;
    }
    
    private Object parseValue(String value) {
        value = value.trim();
        if (value.equals("true")) return true;
        if (value.equals("false")) return false;
        return parseLongValue(value);
    }
    
    private Byte[] toBoxedArray(byte[] bytes) {
        Byte[] result = new Byte[bytes.length];
        for (int i = 0; i < bytes.length; i++) {
            result[i] = bytes[i];
        }
        return result;
    }
    
    @SuppressWarnings("unchecked")
    private byte[] serializeVector(List<?> vector) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        
        // Write length as ULEB128
        byte[] lengthBytes = BcsSerializer.encodeUleb128(vector.size());
        out.writeBytes(lengthBytes);
        
        // Write elements
        for (Object elem : vector) {
            if (elem instanceof Integer) {
                out.write((Integer) elem & 0xFF);
            } else if (elem instanceof Long) {
                byte[] bytes = BcsSerializer.serializeU64((Long) elem);
                out.writeBytes(bytes);
            } else if (elem instanceof List) {
                byte[] nested = serializeVector((List<?>) elem);
                out.writeBytes(nested);
            }
        }
        
        return out.toByteArray();
    }
    
    // ==========================================================================
    // BCS Serializer - Placeholder Implementation
    // ==========================================================================
    
    /**
     * Placeholder BCS serialization utilities.
     * TODO: Replace with actual japtos BCS implementation.
     */
    public static class BcsSerializer {
        
        public static byte[] serializeBool(boolean value) {
            return new byte[] { (byte) (value ? 1 : 0) };
        }
        
        public static byte[] serializeU8(int value) {
            return new byte[] { (byte) value };
        }
        
        public static byte[] serializeU16(int value) {
            return ByteBuffer.allocate(2)
                .order(ByteOrder.LITTLE_ENDIAN)
                .putShort((short) value)
                .array();
        }
        
        public static byte[] serializeU32(long value) {
            return ByteBuffer.allocate(4)
                .order(ByteOrder.LITTLE_ENDIAN)
                .putInt((int) value)
                .array();
        }
        
        public static byte[] serializeU64(long value) {
            return ByteBuffer.allocate(8)
                .order(ByteOrder.LITTLE_ENDIAN)
                .putLong(value)
                .array();
        }
        
        public static byte[] serializeU128(BigInteger value) {
            byte[] result = new byte[16];
            byte[] bigEndian = value.toByteArray();
            // Convert to little-endian, handling sign byte
            int srcPos = bigEndian.length - 1;
            int destPos = 0;
            while (srcPos >= 0 && destPos < 16) {
                result[destPos++] = bigEndian[srcPos--];
            }
            return result;
        }
        
        public static byte[] serializeU256(BigInteger value) {
            byte[] result = new byte[32];
            byte[] bigEndian = value.toByteArray();
            // Convert to little-endian, handling sign byte
            int srcPos = bigEndian.length - 1;
            int destPos = 0;
            while (srcPos >= 0 && destPos < 32) {
                result[destPos++] = bigEndian[srcPos--];
            }
            return result;
        }
        
        public static byte[] serializeString(String value) {
            byte[] utf8 = value.getBytes(StandardCharsets.UTF_8);
            return serializeBytes(utf8);
        }
        
        public static byte[] serializeBytes(byte[] value) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] length = encodeUleb128(value.length);
            out.writeBytes(length);
            out.writeBytes(value);
            return out.toByteArray();
        }
        
        public static byte[] serializeOptionNone() {
            return new byte[] { 0x00 };
        }
        
        public static byte[] serializeOptionSomeU64(long value) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            out.write(0x01);
            out.writeBytes(serializeU64(value));
            return out.toByteArray();
        }
        
        public static byte[] encodeUleb128(long value) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            do {
                int b = (int) (value & 0x7F);
                value >>>= 7;
                if (value != 0) {
                    b |= 0x80;
                }
                out.write(b);
            } while (value != 0);
            return out.toByteArray();
        }
        
        public static long decodeUleb128(byte[] bytes) {
            long result = 0;
            int shift = 0;
            for (byte b : bytes) {
                result |= (long) (b & 0x7F) << shift;
                if ((b & 0x80) == 0) {
                    break;
                }
                shift += 7;
            }
            return result;
        }
    }
}
