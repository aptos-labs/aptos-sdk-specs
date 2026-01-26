#!/usr/bin/env bun

/**
 * Standalone performance benchmark script for Aptos TypeScript SDK
 * Run with: bun benchmark.ts
 */

import {
  Aptos,
  AptosConfig,
  Network,
  Account,
} from "@aptos-labs/ts-sdk";
import { sha3_256 } from "@noble/hashes/sha3.js";

interface BenchmarkResult {
  name: string;
  avg: number;
  p95: number;
  min: number;
  max: number;
  ops: number;
  unit: string;
}

function calculateStats(samples: number[]): { avg: number; p95: number; min: number; max: number } {
  if (samples.length === 0) return { avg: 0, p95: 0, min: 0, max: 0 };
  
  const sorted = [...samples].sort((a, b) => a - b);
  const avg = samples.reduce((a, b) => a + b, 0) / samples.length;
  const p95Idx = Math.floor(samples.length * 0.95);
  const p95 = sorted[Math.min(p95Idx, sorted.length - 1)];
  const min = sorted[0];
  const max = sorted[sorted.length - 1];
  
  return { avg, p95, min, max };
}

async function measureAsync<T>(
  fn: () => Promise<T>,
  iterations: number,
  warmup: number = 3
): Promise<{ avg: number; p95: number; min: number; max: number }> {
  // Warmup
  for (let i = 0; i < warmup; i++) {
    await fn();
  }
  
  // Measure
  const samples: number[] = [];
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    await fn();
    const end = performance.now();
    samples.push(end - start);
  }
  
  return calculateStats(samples);
}

function measureSync<T>(
  fn: () => T,
  iterations: number,
  warmup: number = 100
): { avg: number; p95: number; min: number; max: number } {
  // Warmup
  for (let i = 0; i < warmup; i++) {
    fn();
  }
  
  // Measure
  const samples: number[] = [];
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    fn();
    const end = performance.now();
    samples.push(end - start);
  }
  
  return calculateStats(samples);
}

async function runBenchmarks() {
  console.log("=== Aptos TypeScript SDK Benchmarks ===\n");
  console.log(`Network: Devnet`);
  console.log(`Runtime: Bun ${Bun.version}`);
  console.log(`Date: ${new Date().toISOString()}\n`);
  
  const results: BenchmarkResult[] = [];
  
  // Initialize client
  const config = new AptosConfig({ network: Network.DEVNET });
  const aptos = new Aptos(config);
  
  // Get a known address for tests
  const knownAddress = "0x1";
  
  // =============================================================================
  // Cryptographic Operations (Local)
  // =============================================================================
  console.log("--- Cryptographic Operations ---\n");
  
  // Ed25519 Key Generation
  {
    const stats = measureSync(() => Account.generate(), 1000);
    const avgUs = stats.avg * 1000;
    const ops = 1000000 / avgUs;
    results.push({ name: "Ed25519 Key Gen", avg: avgUs, p95: stats.p95 * 1000, min: stats.min * 1000, max: stats.max * 1000, ops, unit: "μs" });
    console.log(`Ed25519 Key Gen: ${avgUs.toFixed(1)} μs avg, ${ops.toFixed(0)} ops/s`);
  }
  
  // Ed25519 Signing
  {
    const account = Account.generate();
    const message = new Uint8Array(256).fill(0x42);
    const stats = measureSync(() => account.sign(message), 1000);
    const avgUs = stats.avg * 1000;
    const ops = 1000000 / avgUs;
    results.push({ name: "Ed25519 Sign", avg: avgUs, p95: stats.p95 * 1000, min: stats.min * 1000, max: stats.max * 1000, ops, unit: "μs" });
    console.log(`Ed25519 Sign: ${avgUs.toFixed(1)} μs avg, ${ops.toFixed(0)} ops/s`);
  }
  
  // Ed25519 Verification
  {
    const account = Account.generate();
    const message = new Uint8Array(256).fill(0x42);
    const signature = account.sign(message);
    const publicKey = account.publicKey;
    const stats = measureSync(() => publicKey.verifySignature({ message, signature }), 1000);
    const avgUs = stats.avg * 1000;
    const ops = 1000000 / avgUs;
    results.push({ name: "Ed25519 Verify", avg: avgUs, p95: stats.p95 * 1000, min: stats.min * 1000, max: stats.max * 1000, ops, unit: "μs" });
    console.log(`Ed25519 Verify: ${avgUs.toFixed(1)} μs avg, ${ops.toFixed(0)} ops/s`);
  }
  
  // SHA3-256 Hashing
  {
    const message = new Uint8Array(256).fill(0x42);
    const stats = measureSync(() => sha3_256(message), 5000);
    const avgUs = stats.avg * 1000;
    const ops = 1000000 / avgUs;
    results.push({ name: "SHA3-256", avg: avgUs, p95: stats.p95 * 1000, min: stats.min * 1000, max: stats.max * 1000, ops, unit: "μs" });
    console.log(`SHA3-256 Hash: ${avgUs.toFixed(2)} μs avg, ${ops.toFixed(0)} ops/s`);
  }
  
  // =============================================================================
  // REST API Operations (Network)
  // =============================================================================
  console.log("\n--- REST API Operations ---\n");
  
  // Get Ledger Info
  {
    const stats = await measureAsync(() => aptos.getLedgerInfo(), 5, 1);
    results.push({ name: "Get Ledger Info", avg: stats.avg, p95: stats.p95, min: stats.min, max: stats.max, ops: 1000 / stats.avg, unit: "ms" });
    console.log(`Get Ledger Info: ${stats.avg.toFixed(1)} ms avg, ${(1000 / stats.avg).toFixed(1)} req/s`);
  }
  
  // Get Account Info
  {
    const stats = await measureAsync(() => aptos.getAccountInfo({ accountAddress: knownAddress }), 5, 1);
    results.push({ name: "Get Account Info", avg: stats.avg, p95: stats.p95, min: stats.min, max: stats.max, ops: 1000 / stats.avg, unit: "ms" });
    console.log(`Get Account Info: ${stats.avg.toFixed(1)} ms avg, ${(1000 / stats.avg).toFixed(1)} req/s`);
  }
  
  // Get Account Resources
  {
    const stats = await measureAsync(() => aptos.getAccountResources({ accountAddress: knownAddress }), 5, 1);
    results.push({ name: "Get Account Resources", avg: stats.avg, p95: stats.p95, min: stats.min, max: stats.max, ops: 1000 / stats.avg, unit: "ms" });
    console.log(`Get Account Resources: ${stats.avg.toFixed(1)} ms avg, ${(1000 / stats.avg).toFixed(1)} req/s`);
  }
  
  // Get Account Balance
  {
    const stats = await measureAsync(() => aptos.getAccountAPTAmount({ accountAddress: knownAddress }), 5, 1);
    results.push({ name: "Get Account Balance", avg: stats.avg, p95: stats.p95, min: stats.min, max: stats.max, ops: 1000 / stats.avg, unit: "ms" });
    console.log(`Get Account Balance: ${stats.avg.toFixed(1)} ms avg, ${(1000 / stats.avg).toFixed(1)} req/s`);
  }
  
  // =============================================================================
  // GraphQL/Indexer Operations (Network)
  // =============================================================================
  console.log("\n--- GraphQL/Indexer Operations ---\n");
  
  // Get Account Tokens
  {
    try {
      const stats = await measureAsync(() => aptos.getAccountOwnedTokens({ accountAddress: knownAddress }), 10);
      results.push({ name: "Get Account Tokens", avg: stats.avg, p95: stats.p95, min: stats.min, max: stats.max, ops: 1000 / stats.avg, unit: "ms" });
      console.log(`Get Account Tokens: ${stats.avg.toFixed(1)} ms avg, ${(1000 / stats.avg).toFixed(1)} req/s`);
    } catch (e) {
      console.log(`Get Account Tokens: SKIPPED (${e.message})`);
    }
  }
  
  // Get Account Transactions
  {
    try {
      const stats = await measureAsync(() => aptos.getAccountTransactions({ accountAddress: knownAddress, options: { limit: 10 } }), 10);
      results.push({ name: "Get Account Transactions", avg: stats.avg, p95: stats.p95, min: stats.min, max: stats.max, ops: 1000 / stats.avg, unit: "ms" });
      console.log(`Get Account Transactions: ${stats.avg.toFixed(1)} ms avg, ${(1000 / stats.avg).toFixed(1)} req/s`);
    } catch (e) {
      console.log(`Get Account Transactions: SKIPPED (${e.message})`);
    }
  }
  
  // =============================================================================
  // Summary JSON
  // =============================================================================
  console.log("\n=== Results JSON ===");
  console.log(JSON.stringify({
    sdk: "typescript",
    version: "5.2.0",
    runtime: `bun ${Bun.version}`,
    network: "devnet",
    timestamp: new Date().toISOString(),
    results: results.reduce((acc, r) => {
      acc[r.name] = { avg: r.avg, p95: r.p95, ops: r.ops, unit: r.unit };
      return acc;
    }, {} as Record<string, any>)
  }, null, 2));
}

runBenchmarks().catch(console.error);
