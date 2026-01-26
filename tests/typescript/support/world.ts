import { setWorldConstructor, World, type IWorldOptions } from "@cucumber/cucumber";
import {
  Aptos,
  AptosConfig,
  Network,
  Account,
  Ed25519PrivateKey,
  Secp256k1PrivateKey,
  AccountAddress,
  type RawTransaction,
  type SignedTransaction,
  type PrivateKey,
  type Ed25519Signature,
} from "@aptos-labs/ts-sdk";

/**
 * Benchmark result statistics
 */
export interface BenchmarkResult {
  samples: number[];
  avg: number;
  p95: number;
  min: number;
  max: number;
  opsPerSecond: number;
}

/**
 * Custom World class that holds test context between steps.
 * Each scenario gets a fresh World instance.
 */
export class AptosWorld extends World {
  // Configuration
  public network: Network = Network.TESTNET;
  public config?: AptosConfig;
  public client?: Aptos;

  // Accounts
  public account?: Account;
  public accounts: Map<string, Account> = new Map();
  public privateKey?: PrivateKey;
  public publicKey?: Uint8Array;

  // Addresses
  public address?: AccountAddress;
  public addresses: AccountAddress[] = [];

  // Transactions
  public rawTransaction?: RawTransaction;
  public signedTransaction?: SignedTransaction;
  public transactionHash?: string;
  public simulationResult?: any;

  // General purpose storage
  public result?: any;
  public error?: Error;
  public bytes?: Uint8Array;
  public hexString?: string;

  // Test vectors
  public testVectors: Map<string, any> = new Map();

  // Performance benchmarks
  public benchmarkResult?: BenchmarkResult;
  public stepBreakdown?: Record<string, BenchmarkResult>;
  public message?: Uint8Array;
  public signature?: Ed25519Signature;

  constructor(options: IWorldOptions) {
    super(options);
  }

  /**
   * Initialize the Aptos client for the current network
   */
  initClient(): Aptos {
    if (!this.client) {
      this.config = new AptosConfig({ network: this.network });
      this.client = new Aptos(this.config);
    }
    return this.client;
  }

  /**
   * Get or create a named account
   */
  getOrCreateAccount(name: string): Account {
    let account = this.accounts.get(name);
    if (!account) {
      account = Account.generate();
      this.accounts.set(name, account);
    }
    return account;
  }

  /**
   * Store an error for later assertion
   */
  setError(error: Error): void {
    this.error = error;
  }

  /**
   * Clear error state
   */
  clearError(): void {
    this.error = undefined;
  }

  /**
   * Reset state between scenarios (handled automatically by Cucumber)
   */
  reset(): void {
    this.config = undefined;
    this.client = undefined;
    this.account = undefined;
    this.accounts.clear();
    this.privateKey = undefined;
    this.publicKey = undefined;
    this.address = undefined;
    this.addresses = [];
    this.rawTransaction = undefined;
    this.signedTransaction = undefined;
    this.transactionHash = undefined;
    this.simulationResult = undefined;
    this.result = undefined;
    this.error = undefined;
    this.bytes = undefined;
    this.hexString = undefined;
  }
}

setWorldConstructor(AptosWorld);

// Type alias for step definitions
export type TestWorld = AptosWorld;
