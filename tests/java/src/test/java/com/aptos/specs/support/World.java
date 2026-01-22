package com.aptos.specs.support;

import com.aptoslabs.japtos.account.Ed25519Account;
import com.aptoslabs.japtos.crypto.Ed25519PrivateKey;
import com.aptoslabs.japtos.crypto.Ed25519PublicKey;
import com.aptoslabs.japtos.crypto.Ed25519Signature;
import com.aptoslabs.japtos.types.AccountAddress;
import com.aptoslabs.japtos.types.AuthenticationKey;
import com.aptoslabs.japtos.types.HashValue;
import com.aptoslabs.japtos.client.AptosClient;
import com.aptoslabs.japtos.api.AptosConfig;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * World class holds test context/state between Cucumber steps.
 * Each scenario gets a fresh World instance via dependency injection.
 * 
 * Uses japtos SDK types for strong typing.
 */
public class World {
    
    // ==========================================================================
    // Configuration
    // ==========================================================================
    private String networkUrl = "https://fullnode.testnet.aptoslabs.com/v1";
    private AptosClient client;
    private AptosConfig config;
    
    // ==========================================================================
    // Addresses
    // ==========================================================================
    private AccountAddress address;
    private AccountAddress address2;
    private List<AccountAddress> addresses = new ArrayList<>();
    
    // ==========================================================================
    // Cryptography - Ed25519
    // ==========================================================================
    private Ed25519PrivateKey ed25519PrivateKey;
    private Ed25519PrivateKey ed25519PrivateKey2;
    private Ed25519PublicKey ed25519PublicKey;
    private Ed25519PublicKey ed25519PublicKey2;
    private Ed25519Signature ed25519Signature;
    private Ed25519Signature ed25519Signature2;
    
    // ==========================================================================
    // Accounts
    // ==========================================================================
    private Ed25519Account account;
    private Ed25519Account account2;
    private Map<String, Ed25519Account> namedAccounts = new HashMap<>();
    
    // ==========================================================================
    // Authentication
    // ==========================================================================
    private AuthenticationKey authenticationKey;
    
    // ==========================================================================
    // Hashing
    // ==========================================================================
    private HashValue hashValue;
    
    // ==========================================================================
    // Transactions
    // ==========================================================================
    private Object rawTransaction;
    private Object signedTransaction;
    private String transactionHash;
    private Object simulationResult;
    private Object entryFunctionPayload;
    
    // ==========================================================================
    // Type System
    // ==========================================================================
    private Object typeTag;
    private Object moduleId;
    private Object structTag;
    
    // ==========================================================================
    // Serialization
    // ==========================================================================
    private byte[] bytes;
    private byte[] serializedBytes;
    private String hexString;
    
    // ==========================================================================
    // Primitives for BCS testing
    // ==========================================================================
    private Boolean boolValue;
    private Integer u8Value;
    private Integer u16Value;
    private Long u32Value;
    private Long u64Value;
    private BigInteger u128Value;
    private BigInteger u256Value;
    private String stringValue;
    private List<?> vectorValue;
    private Optional<?> optionalValue;
    
    // ==========================================================================
    // General Purpose
    // ==========================================================================
    private Object result;
    private Exception error;
    private Map<String, Object> testVectors = new HashMap<>();
    
    // ==========================================================================
    // Getters and Setters
    // ==========================================================================
    
    public String getNetworkUrl() {
        return networkUrl;
    }
    
    public void setNetworkUrl(String networkUrl) {
        this.networkUrl = networkUrl;
    }
    
    public AptosClient getClient() {
        return client;
    }
    
    public void setClient(AptosClient client) {
        this.client = client;
    }
    
    public AptosConfig getConfig() {
        return config;
    }
    
    public void setConfig(AptosConfig config) {
        this.config = config;
    }
    
    public AccountAddress getAddress() {
        return address;
    }
    
    public void setAddress(AccountAddress address) {
        this.address = address;
    }
    
    // Generic setter for compatibility with placeholder code
    public void setAddress(Object address) {
        if (address instanceof AccountAddress) {
            this.address = (AccountAddress) address;
        }
    }
    
    public AccountAddress getAddress2() {
        return address2;
    }
    
    public void setAddress2(AccountAddress address2) {
        this.address2 = address2;
    }
    
    public void setAddress2(Object address2) {
        if (address2 instanceof AccountAddress) {
            this.address2 = (AccountAddress) address2;
        }
    }
    
    public List<AccountAddress> getAddresses() {
        return addresses;
    }
    
    public void setAddresses(List<AccountAddress> addresses) {
        this.addresses = addresses;
    }
    
    public Ed25519PrivateKey getEd25519PrivateKey() {
        return ed25519PrivateKey;
    }
    
    public void setEd25519PrivateKey(Ed25519PrivateKey ed25519PrivateKey) {
        this.ed25519PrivateKey = ed25519PrivateKey;
    }
    
    public Ed25519PublicKey getEd25519PublicKey() {
        return ed25519PublicKey;
    }
    
    public void setEd25519PublicKey(Ed25519PublicKey ed25519PublicKey) {
        this.ed25519PublicKey = ed25519PublicKey;
    }
    
    public Ed25519Signature getEd25519Signature() {
        return ed25519Signature;
    }
    
    public void setEd25519Signature(Ed25519Signature ed25519Signature) {
        this.ed25519Signature = ed25519Signature;
    }
    
    public Ed25519Account getAccount() {
        return account;
    }
    
    public void setAccount(Ed25519Account account) {
        this.account = account;
    }
    
    public Ed25519Account getAccount2() {
        return account2;
    }
    
    public void setAccount2(Ed25519Account account2) {
        this.account2 = account2;
    }
    
    public Map<String, Ed25519Account> getNamedAccounts() {
        return namedAccounts;
    }
    
    public AuthenticationKey getAuthenticationKey() {
        return authenticationKey;
    }
    
    public void setAuthenticationKey(AuthenticationKey authenticationKey) {
        this.authenticationKey = authenticationKey;
    }
    
    public HashValue getHashValue() {
        return hashValue;
    }
    
    public void setHashValue(HashValue hashValue) {
        this.hashValue = hashValue;
    }
    
    public Object getRawTransaction() {
        return rawTransaction;
    }
    
    public void setRawTransaction(Object rawTransaction) {
        this.rawTransaction = rawTransaction;
    }
    
    public Object getSignedTransaction() {
        return signedTransaction;
    }
    
    public void setSignedTransaction(Object signedTransaction) {
        this.signedTransaction = signedTransaction;
    }
    
    public String getTransactionHash() {
        return transactionHash;
    }
    
    public void setTransactionHash(String transactionHash) {
        this.transactionHash = transactionHash;
    }
    
    public Object getSimulationResult() {
        return simulationResult;
    }
    
    public void setSimulationResult(Object simulationResult) {
        this.simulationResult = simulationResult;
    }
    
    public Object getEntryFunctionPayload() {
        return entryFunctionPayload;
    }
    
    public void setEntryFunctionPayload(Object entryFunctionPayload) {
        this.entryFunctionPayload = entryFunctionPayload;
    }
    
    public Object getTypeTag() {
        return typeTag;
    }
    
    public void setTypeTag(Object typeTag) {
        this.typeTag = typeTag;
    }
    
    public Object getModuleId() {
        return moduleId;
    }
    
    public void setModuleId(Object moduleId) {
        this.moduleId = moduleId;
    }
    
    public Object getStructTag() {
        return structTag;
    }
    
    public void setStructTag(Object structTag) {
        this.structTag = structTag;
    }
    
    public byte[] getBytes() {
        return bytes;
    }
    
    public void setBytes(byte[] bytes) {
        this.bytes = bytes;
    }
    
    public byte[] getSerializedBytes() {
        return serializedBytes;
    }
    
    public void setSerializedBytes(byte[] serializedBytes) {
        this.serializedBytes = serializedBytes;
    }
    
    public String getHexString() {
        return hexString;
    }
    
    public void setHexString(String hexString) {
        this.hexString = hexString;
    }
    
    public Boolean getBoolValue() {
        return boolValue;
    }
    
    public void setBoolValue(Boolean boolValue) {
        this.boolValue = boolValue;
    }
    
    public Integer getU8Value() {
        return u8Value;
    }
    
    public void setU8Value(Integer u8Value) {
        this.u8Value = u8Value;
    }
    
    public Integer getU16Value() {
        return u16Value;
    }
    
    public void setU16Value(Integer u16Value) {
        this.u16Value = u16Value;
    }
    
    public Long getU32Value() {
        return u32Value;
    }
    
    public void setU32Value(Long u32Value) {
        this.u32Value = u32Value;
    }
    
    public Long getU64Value() {
        return u64Value;
    }
    
    public void setU64Value(Long u64Value) {
        this.u64Value = u64Value;
    }
    
    public BigInteger getU128Value() {
        return u128Value;
    }
    
    public void setU128Value(BigInteger u128Value) {
        this.u128Value = u128Value;
    }
    
    public BigInteger getU256Value() {
        return u256Value;
    }
    
    public void setU256Value(BigInteger u256Value) {
        this.u256Value = u256Value;
    }
    
    public String getStringValue() {
        return stringValue;
    }
    
    public void setStringValue(String stringValue) {
        this.stringValue = stringValue;
    }
    
    public List<?> getVectorValue() {
        return vectorValue;
    }
    
    public void setVectorValue(List<?> vectorValue) {
        this.vectorValue = vectorValue;
    }
    
    public Optional<?> getOptionalValue() {
        return optionalValue;
    }
    
    public void setOptionalValue(Optional<?> optionalValue) {
        this.optionalValue = optionalValue;
    }
    
    public Object getResult() {
        return result;
    }
    
    public void setResult(Object result) {
        this.result = result;
    }
    
    public Exception getError() {
        return error;
    }
    
    public void setError(Exception error) {
        this.error = error;
    }
    
    public void clearError() {
        this.error = null;
    }
    
    public Map<String, Object> getTestVectors() {
        return testVectors;
    }
    
    /**
     * Initialize the Aptos client for the current network.
     */
    public AptosClient initClient() {
        if (client == null) {
            config = AptosConfig.builder()
                .network(AptosConfig.Network.TESTNET)
                .build();
            client = new AptosClient(config);
        }
        return client;
    }
    
    /**
     * Reset all state. Called automatically before each scenario.
     */
    public void reset() {
        client = null;
        config = null;
        address = null;
        address2 = null;
        addresses = new ArrayList<>();
        ed25519PrivateKey = null;
        ed25519PrivateKey2 = null;
        ed25519PublicKey = null;
        ed25519PublicKey2 = null;
        ed25519Signature = null;
        ed25519Signature2 = null;
        account = null;
        account2 = null;
        namedAccounts = new HashMap<>();
        authenticationKey = null;
        hashValue = null;
        rawTransaction = null;
        signedTransaction = null;
        transactionHash = null;
        simulationResult = null;
        entryFunctionPayload = null;
        typeTag = null;
        moduleId = null;
        structTag = null;
        bytes = null;
        serializedBytes = null;
        hexString = null;
        boolValue = null;
        u8Value = null;
        u16Value = null;
        u32Value = null;
        u64Value = null;
        u128Value = null;
        u256Value = null;
        stringValue = null;
        vectorValue = null;
        optionalValue = null;
        result = null;
        error = null;
        testVectors = new HashMap<>();
    }
}
