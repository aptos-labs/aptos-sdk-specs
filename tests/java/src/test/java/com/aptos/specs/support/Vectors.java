package com.aptos.specs.support;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Utility class for loading test vectors from JSON files. Test vectors are
 * stored in ../../test-vectors/ relative to the tests/java directory.
 */
public class Vectors {

	private static final String VECTORS_DIR = "../../test-vectors";
	private static final Gson gson = new Gson();

	/**
	 * Load a JSON test vector file.
	 *
	 * @param filename
	 *            The name of the file (e.g., "addresses.json")
	 * @return JsonObject containing the parsed JSON
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static JsonObject loadVectorFile(String filename) throws IOException {
		Path path = Paths.get(VECTORS_DIR, filename);
		String content = Files.readString(path, StandardCharsets.UTF_8);
		return gson.fromJson(content, JsonObject.class);
	}

	/**
	 * Load address parsing test vectors.
	 *
	 * @return List of AddressVector objects
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static List<AddressVector> getAddressParsingVectors() throws IOException {
		JsonObject data = loadVectorFile("addresses.json");
		JsonArray vectorsArray = data.getAsJsonArray("parsing_vectors");

		Type listType = new TypeToken<List<AddressVector>>() {
		}.getType();
		return gson.fromJson(vectorsArray, listType);
	}

	/**
	 * Load mnemonic derivation test vectors.
	 *
	 * @return List of MnemonicVector objects
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static List<MnemonicVector> getEd25519DerivationVectors() throws IOException {
		JsonObject data = loadVectorFile("mnemonics.json");
		JsonArray vectorsArray = data.getAsJsonArray("ed25519_derivation_vectors");

		Type listType = new TypeToken<List<MnemonicVector>>() {
		}.getType();
		return gson.fromJson(vectorsArray, listType);
	}

	/**
	 * Load signature test vectors.
	 *
	 * @return JsonObject containing signature test data
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static JsonObject getSignatureVectors() throws IOException {
		return loadVectorFile("signatures.json");
	}

	/**
	 * Load SHA3-256 hash test vectors.
	 *
	 * @return List of HashVector objects
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static List<HashVector> getSha3256Vectors() throws IOException {
		JsonObject data = getSignatureVectors();
		JsonObject hashing = data.getAsJsonObject("hashing");
		JsonArray vectorsArray = hashing.getAsJsonArray("sha3_256");

		Type listType = new TypeToken<List<HashVector>>() {
		}.getType();
		return gson.fromJson(vectorsArray, listType);
	}

	/**
	 * Load BCS encoding test vectors.
	 *
	 * @return JsonObject containing BCS test data
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static JsonObject getBcsVectors() throws IOException {
		return loadVectorFile("bcs.json");
	}

	/**
	 * Load transaction test vectors.
	 *
	 * @return JsonObject containing transaction test data
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static JsonObject getTransactionVectors() throws IOException {
		return loadVectorFile("transactions.json");
	}

	/**
	 * Load TypeTag test vectors.
	 *
	 * @return JsonObject containing TypeTag test data
	 * @throws IOException
	 *             if the file cannot be read
	 */
	public static JsonObject getTypeTagVectors() throws IOException {
		return loadVectorFile("type-tags.json");
	}

	// ==========================================================================
	// Utility Methods
	// ==========================================================================

	/**
	 * Convert a hex string to bytes.
	 *
	 * @param hexString
	 *            The hex string (with or without 0x prefix)
	 * @return byte array
	 */
	public static byte[] hexToBytes(String hexString) {
		String cleanHex = hexString.startsWith("0x") ? hexString.substring(2) : hexString;
		int len = cleanHex.length();
		byte[] bytes = new byte[len / 2];
		for (int i = 0; i < len; i += 2) {
			bytes[i / 2] = (byte) ((Character.digit(cleanHex.charAt(i), 16) << 4)
					+ Character.digit(cleanHex.charAt(i + 1), 16));
		}
		return bytes;
	}

	/**
	 * Convert bytes to a hex string with 0x prefix.
	 *
	 * @param bytes
	 *            The byte array
	 * @return Hex string with 0x prefix
	 */
	public static String bytesToHex(byte[] bytes) {
		StringBuilder sb = new StringBuilder("0x");
		for (byte b : bytes) {
			sb.append(String.format("%02x", b));
		}
		return sb.toString();
	}

	// ==========================================================================
	// Data Classes
	// ==========================================================================

	/**
	 * Address parsing test vector.
	 */
	public static class AddressVector {
		public String name;
		public String description;
		public String input;
		public Expected expected;

		public static class Expected {
			public String full_hex;
			public String short_string;
			public String bytes_hex;
			public int last_byte;
		}
	}

	/**
	 * Mnemonic derivation test vector.
	 */
	public static class MnemonicVector {
		public String name;
		public String description;
		public Input input;
		public Expected expected;

		public static class Input {
			public String mnemonic;
			public String passphrase;
			public String derivation_path;
		}

		public static class Expected {
			public String seed_hex;
			public String private_key_hex;
			public String public_key_hex;
			public String auth_key_hex;
			public String address;
		}
	}

	/**
	 * Hash test vector.
	 */
	public static class HashVector {
		public String name;
		public String input;
		public String input_hex;
		public String expected_hex;
	}

	/**
	 * BCS encoding test vector.
	 */
	public static class BcsVector {
		public String name;
		public String type;
		public Object value;
		public String bcs_hex;
	}
}
