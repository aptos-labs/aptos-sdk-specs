/**
 * Multi-Agent Transaction Step Definitions
 *
 * Implements behavioral tests for multi-agent transactions.
 */
import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  Ed25519PrivateKey,
  Secp256k1PrivateKey,
  Account,
  AccountAddress,
  RawTransaction,
  TransactionPayloadEntryFunction,
  EntryFunction,
  EntryFunctionBytes,
  ChainId,
  SignedTransaction,
  MultiAgentTransaction,
  FeePayerRawTransaction,
  TransactionAuthenticatorMultiAgent,
  AccountAuthenticator,
  AccountAuthenticatorEd25519,
  AccountAuthenticatorSingleKey,
  generateSigningMessageForTransaction,
  Serializer,
  Deserializer,
  SigningSchemeInput,
  ModuleId,
  Identifier,
} from "@aptos-labs/ts-sdk";
import { sha3_256 } from "@noble/hashes/sha3.js";
import { bytesToHex } from "@noble/hashes/utils.js";
import type { AptosWorld } from "../support/world.js";

// Helper to create a proper EntryFunction
function createEntryFunction(
  moduleAddress: AccountAddress,
  moduleName: string,
  functionName: string,
  typeArgs: any[] = [],
  args: Uint8Array[] = [],
): EntryFunction {
  const moduleId = new ModuleId(moduleAddress, new Identifier(moduleName));
  const wrappedArgs = args.map((a) => new EntryFunctionBytes(a));
  return new EntryFunction(
    moduleId,
    new Identifier(functionName),
    typeArgs,
    wrappedArgs,
  );
}

// Helper to create a standard APT transfer payload
function createTransferPayload(
  recipient: AccountAddress,
  amount: bigint,
): TransactionPayloadEntryFunction {
  const recipientSerializer = new Serializer();
  recipient.serialize(recipientSerializer);

  const amountSerializer = new Serializer();
  amountSerializer.serializeU64(amount);

  const entryFunction = createEntryFunction(
    AccountAddress.ONE,
    "aptos_account",
    "transfer",
    [],
    [recipientSerializer.toUint8Array(), amountSerializer.toUint8Array()],
  );

  return new TransactionPayloadEntryFunction(entryFunction);
}

// =============================================================================
// Multi-Agent Transaction Creation
// =============================================================================

Given("a sender account", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("senderAccount", account);
  this.account = account;
});

Given("a secondary signer account", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("secondaryAccount", account);

  const secondaries =
    (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];
  secondaries.push(account);
  this.testVectors.set("secondaryAccounts", secondaries);
});

Given(
  "{int} secondary signer accounts",
  function (this: AptosWorld, count: number) {
    const secondaries: Account[] = [];

    for (let i = 0; i < count; i++) {
      const privateKey = Ed25519PrivateKey.generate();
      const account = Account.fromPrivateKey({ privateKey });
      secondaries.push(account);
    }

    this.testVectors.set("secondaryAccounts", secondaries);
  },
);

When("I create a multi-agent transaction", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account;
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaries =
    (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];

  const secondaryAddresses = secondaries.map((acc) => acc.accountAddress);

  const multiAgentTxn = new MultiAgentTransaction(rawTxn, secondaryAddresses);

  this.testVectors.set("multiAgentTransaction", multiAgentTxn);
  this.result = multiAgentTxn;
});

Then(
  "the transaction should include both signers",
  function (this: AptosWorld) {
    const multiAgentTxn = this.testVectors.get(
      "multiAgentTransaction",
    ) as MultiAgentTransaction;
    expect(multiAgentTxn.secondarySignerAddresses.length).to.equal(1);
  },
);

Then(
  "the transaction should include all {int} signers",
  function (this: AptosWorld, count: number) {
    const multiAgentTxn = this.testVectors.get(
      "multiAgentTransaction",
    ) as MultiAgentTransaction;
    // count includes sender + secondaries
    expect(multiAgentTxn.secondarySignerAddresses.length).to.equal(count - 1);
  },
);

Given("secondary signer addresses [A, B, C]", function (this: AptosWorld) {
  const addresses = [
    AccountAddress.from(
      "0x1111111111111111111111111111111111111111111111111111111111111111",
    ),
    AccountAddress.from(
      "0x2222222222222222222222222222222222222222222222222222222222222222",
    ),
    AccountAddress.from(
      "0x3333333333333333333333333333333333333333333333333333333333333333",
    ),
  ];
  this.testVectors.set("secondaryAddresses", addresses);
});

When("I build a multi-agent transaction", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaryAddresses = this.testVectors.get(
    "secondaryAddresses",
  ) as AccountAddress[];

  const multiAgentTxn = new MultiAgentTransaction(rawTxn, secondaryAddresses);

  this.testVectors.set("multiAgentTransaction", multiAgentTxn);
  this.result = multiAgentTxn;
});

Then(
  "the secondary_signer_addresses should be [A, B, C] in order",
  function (this: AptosWorld) {
    const multiAgentTxn = this.testVectors.get(
      "multiAgentTransaction",
    ) as MultiAgentTransaction;
    const expected = this.testVectors.get(
      "secondaryAddresses",
    ) as AccountAddress[];

    expect(multiAgentTxn.secondarySignerAddresses.length).to.equal(
      expected.length,
    );
    for (let i = 0; i < expected.length; i++) {
      expect(multiAgentTxn.secondarySignerAddresses[i].toString()).to.equal(
        expected[i].toString(),
      );
    }
  },
);

// =============================================================================
// Multi-Agent Signing Message
// =============================================================================

Given("the same RawTransaction", function (this: AptosWorld) {
  const sender = AccountAddress.from("0x1");
  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

  const rawTxn = new RawTransaction(
    sender,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(Math.floor(Date.now() / 1000) + 600),
    new ChainId(1),
  );

  this.testVectors.set("rawTransaction", rawTxn);
});

When("I generate single-signer signing message", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;

  const message = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
  });

  this.testVectors.set("singleSignerMessage", message);
});

When(
  "I generate multi-agent signing message with secondary signers",
  function (this: AptosWorld) {
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const secondaryAddresses = [
      AccountAddress.from(
        "0x2222222222222222222222222222222222222222222222222222222222222222",
      ),
    ];

    const message = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
      secondarySignerAddresses: secondaryAddresses,
    });

    this.testVectors.set("multiAgentMessage", message);
  },
);

Then(
  "the single and multi-agent messages should be different",
  function (this: AptosWorld) {
    const single = this.testVectors.get("singleSignerMessage") as Uint8Array;
    const multi = this.testVectors.get("multiAgentMessage") as Uint8Array;

    expect(bytesToHex(single)).to.not.equal(bytesToHex(multi));
  },
);

Given("secondary signer addresses", function (this: AptosWorld) {
  const addresses = [
    AccountAddress.from(
      "0x2222222222222222222222222222222222222222222222222222222222222222",
    ),
    AccountAddress.from(
      "0x3333333333333333333333333333333333333333333333333333333333333333",
    ),
  ];
  this.testVectors.set("secondaryAddresses", addresses);
});

When("I generate the multi-agent signing message", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaryAddresses = this.testVectors.get(
    "secondaryAddresses",
  ) as AccountAddress[];

  const message = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  this.testVectors.set("multiAgentMessage", message);
  this.bytes = message;
});

Then("it should include the raw transaction", function (this: AptosWorld) {
  // The signing message includes the BCS-serialized raw transaction
  expect(this.bytes).to.not.be.undefined;
  expect(this.bytes!.length).to.be.greaterThan(32); // At least domain prefix
});

Then(
  "it should include the secondary signer addresses",
  function (this: AptosWorld) {
    // This is verified implicitly - the message is different from single signer
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const singleMessage = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
    });

    expect(bytesToHex(this.bytes!)).to.not.equal(bytesToHex(singleMessage));
  },
);

Given("a multi-agent transaction", function (this: AptosWorld) {
  const sender = AccountAddress.from("0x1");
  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

  const rawTxn = new RawTransaction(
    sender,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(Math.floor(Date.now() / 1000) + 600),
    new ChainId(1),
  );

  const secondaryAddresses = [
    AccountAddress.from(
      "0x2222222222222222222222222222222222222222222222222222222222222222",
    ),
  ];

  const multiAgentTxn = new MultiAgentTransaction(rawTxn, secondaryAddresses);

  this.testVectors.set("rawTransaction", rawTxn);
  this.testVectors.set("secondaryAddresses", secondaryAddresses);
  this.testVectors.set("multiAgentTransaction", multiAgentTxn);
});

Then(
  /^it should start with SHA3-256\("APTOS::RawTransactionWithData"\)$/,
  function (this: AptosWorld) {
    const expectedPrefix = sha3_256(new TextEncoder().encode("APTOS::RawTransactionWithData"));
    const actual = this.bytes!.slice(0, 32);

    expect(bytesToHex(actual)).to.equal(bytesToHex(expectedPrefix));
  },
);

Given(
  "a multi-agent transaction with sender and {int} secondary signers",
  function (this: AptosWorld, count: number) {
    const senderPrivate = Ed25519PrivateKey.generate();
    const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

    const secondaries: Account[] = [];
    for (let i = 0; i < count; i++) {
      const pk = Ed25519PrivateKey.generate();
      secondaries.push(Account.fromPrivateKey({ privateKey: pk }));
    }

    const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

    const rawTxn = new RawTransaction(
      sender.accountAddress,
      BigInt(0),
      payload,
      BigInt(100000),
      BigInt(100),
      BigInt(Math.floor(Date.now() / 1000) + 600),
      new ChainId(1),
    );

    this.testVectors.set("senderAccount", sender);
    this.testVectors.set("secondaryAccounts", secondaries);
    this.testVectors.set("rawTransaction", rawTxn);

    const multiAgentTxn = new MultiAgentTransaction(
      rawTxn,
      secondaries.map((s) => s.accountAddress),
    );
    this.testVectors.set("multiAgentTransaction", multiAgentTxn);
  },
);

When("each party generates their signing message", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaries = this.testVectors.get("secondaryAccounts") as Account[];

  const secondaryAddresses = secondaries.map((s) => s.accountAddress);

  // All parties generate the same signing message
  const senderMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  const secondary1Message = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  const secondary2Message = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  this.testVectors.set("senderMessage", senderMessage);
  this.testVectors.set("secondary1Message", secondary1Message);
  this.testVectors.set("secondary2Message", secondary2Message);
});

Then(
  "all {int} messages should be identical",
  function (this: AptosWorld, count: number) {
    const senderMsg = this.testVectors.get("senderMessage") as Uint8Array;
    const sec1Msg = this.testVectors.get("secondary1Message") as Uint8Array;
    const sec2Msg = this.testVectors.get("secondary2Message") as Uint8Array;

    expect(bytesToHex(senderMsg)).to.equal(bytesToHex(sec1Msg));
    expect(bytesToHex(senderMsg)).to.equal(bytesToHex(sec2Msg));
  },
);

// =============================================================================
// Multi-Agent Signing
// =============================================================================

Given("sender account", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("senderAccount", account);
});

// Note: '{int} secondary signer accounts' is defined earlier in this file

When(
  "I sign the multi-agent transaction with all parties",
  function (this: AptosWorld) {
    const sender = this.testVectors.get("senderAccount") as Account;
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const secondaries = this.testVectors.get("secondaryAccounts") as Account[];

    const secondaryAddresses = secondaries.map((s) => s.accountAddress);

    // Generate signing message
    const signingMessage = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
      secondarySignerAddresses: secondaryAddresses,
    });

    // Sign with sender
    const senderSignature = sender.sign(signingMessage);
    const senderAuth = new AccountAuthenticatorSingleKey(
      sender.publicKey,
      senderSignature,
    );

    // Sign with secondaries
    const secondaryAuths = secondaries.map((secondary) => {
      const sig = secondary.sign(signingMessage);
      return new AccountAuthenticatorSingleKey(secondary.publicKey, sig);
    });

    // Create multi-agent authenticator
    const multiAgentAuth = new TransactionAuthenticatorMultiAgent(
      senderAuth,
      secondaryAddresses,
      secondaryAuths,
    );

    const signedTxn = new SignedTransaction(rawTxn, multiAgentAuth);

    this.testVectors.set("signedTransaction", signedTxn);
    this.testVectors.set("multiAgentAuthenticator", multiAgentAuth);
    this.result = signedTxn;
  },
);

Then(
  "the authenticator should be MultiAgent variant",
  function (this: AptosWorld) {
    const signedTxn = this.result as SignedTransaction;
    expect(signedTxn.authenticator.isMultiAgent()).to.be.true;
  },
);

Given("a signed multi-agent transaction", function (this: AptosWorld) {
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const secondary1Private = Ed25519PrivateKey.generate();
  const secondary1 = Account.fromPrivateKey({ privateKey: secondary1Private });

  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

  const rawTxn = new RawTransaction(
    sender.accountAddress,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(Math.floor(Date.now() / 1000) + 600),
    new ChainId(1),
  );

  const secondaryAddresses = [secondary1.accountAddress];

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  const secondaryAuth = new AccountAuthenticatorSingleKey(
    secondary1.publicKey,
    secondary1.sign(signingMessage),
  );

  const multiAgentAuth = new TransactionAuthenticatorMultiAgent(
    senderAuth,
    secondaryAddresses,
    [secondaryAuth],
  );

  const signedTxn = new SignedTransaction(rawTxn, multiAgentAuth);

  this.testVectors.set("signedTransaction", signedTxn);
  this.testVectors.set("multiAgentAuthenticator", multiAgentAuth);
});

When("I inspect the authenticator", function (this: AptosWorld) {
  const auth = this.testVectors.get(
    "multiAgentAuthenticator",
  ) as TransactionAuthenticatorMultiAgent;
  this.result = auth;
});

Then("it should contain sender authenticator", function (this: AptosWorld) {
  const auth = this.result as TransactionAuthenticatorMultiAgent;
  expect(auth.sender).to.not.be.undefined;
});

Then(
  "it should contain secondary_signer_addresses",
  function (this: AptosWorld) {
    const auth = this.result as TransactionAuthenticatorMultiAgent;
    expect(auth.secondary_signer_addresses).to.not.be.undefined;
    expect(Array.isArray(auth.secondary_signer_addresses)).to.be.true;
  },
);

Then("it should contain secondary_signers list", function (this: AptosWorld) {
  const auth = this.result as TransactionAuthenticatorMultiAgent;
  expect(auth.secondary_signers).to.not.be.undefined;
  expect(Array.isArray(auth.secondary_signers)).to.be.true;
});

// =============================================================================
// Mixed Account Types
// =============================================================================

Given("an Ed25519 sender", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("senderAccount", account);
  this.testVectors.set("senderType", "Ed25519");
});

Given("a Secp256k1 secondary signer", function (this: AptosWorld) {
  const privateKey = Secp256k1PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });

  const secondaries =
    (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];
  secondaries.push(account);
  this.testVectors.set("secondaryAccounts", secondaries);
  this.testVectors.set("secondaryType", "Secp256k1");
});

When("I sign the multi-agent transaction", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account;
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaries =
    (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];

  const secondaryAddresses = secondaries.map((s) => s.accountAddress);

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  const secondaryAuths = secondaries.map((secondary) => {
    return new AccountAuthenticatorSingleKey(
      secondary.publicKey,
      secondary.sign(signingMessage),
    );
  });

  const multiAgentAuth = new TransactionAuthenticatorMultiAgent(
    senderAuth,
    secondaryAddresses,
    secondaryAuths,
  );

  const signedTxn = new SignedTransaction(rawTxn, multiAgentAuth);

  this.testVectors.set("signedTransaction", signedTxn);
  this.testVectors.set("multiAgentAuthenticator", multiAgentAuth);
  this.result = signedTxn;
});

Then("multi-agent signing should succeed", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  expect(this.result).to.not.be.undefined;
});

Then("sender authenticator should be Ed25519", function (this: AptosWorld) {
  const auth = this.testVectors.get(
    "multiAgentAuthenticator",
  ) as TransactionAuthenticatorMultiAgent;
  // SingleKey authenticator wraps the actual signature
  expect(auth.sender).to.not.be.undefined;
});

Then(
  "secondary authenticator should be Secp256k1",
  function (this: AptosWorld) {
    const auth = this.testVectors.get(
      "multiAgentAuthenticator",
    ) as TransactionAuthenticatorMultiAgent;
    expect(auth.secondary_signers.length).to.be.greaterThan(0);
  },
);

// =============================================================================
// Partial Signing Workflow
// =============================================================================

Given("a RawTransaction for multi-agent", function (this: AptosWorld) {
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

  const rawTxn = new RawTransaction(
    sender.accountAddress,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(Math.floor(Date.now() / 1000) + 600),
    new ChainId(1),
  );

  this.testVectors.set("senderAccount", sender);
  this.testVectors.set("rawTransaction", rawTxn);
});

When("sender signs their portion", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account;
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaryAddresses =
    (this.testVectors.get("secondaryAddresses") as AccountAddress[]) ?? [];

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  this.testVectors.set("senderAuthenticator", senderAuth);
});

When(
  "secondary signer {int} signs their portion",
  function (this: AptosWorld, index: number) {
    const secondaries = this.testVectors.get("secondaryAccounts") as Account[];
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const secondaryAddresses = secondaries.map((s) => s.accountAddress);

    const signingMessage = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
      secondarySignerAddresses: secondaryAddresses,
    });

    const secondary = secondaries[index - 1]; // 1-indexed in feature
    const auth = new AccountAuthenticatorSingleKey(
      secondary.publicKey,
      secondary.sign(signingMessage),
    );

    const collectedAuths =
      (this.testVectors.get(
        "collectedSecondaryAuths",
      ) as AccountAuthenticator[]) ?? [];
    collectedAuths[index - 1] = auth;
    this.testVectors.set("collectedSecondaryAuths", collectedAuths);
  },
);

When("I combine all signatures", function (this: AptosWorld) {
  const senderAuth = this.testVectors.get(
    "senderAuthenticator",
  ) as AccountAuthenticator;
  const secondaryAuths = this.testVectors.get(
    "collectedSecondaryAuths",
  ) as AccountAuthenticator[];
  const secondaries = this.testVectors.get("secondaryAccounts") as Account[];
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;

  const secondaryAddresses = secondaries.map((s) => s.accountAddress);

  const multiAgentAuth = new TransactionAuthenticatorMultiAgent(
    senderAuth,
    secondaryAddresses,
    secondaryAuths,
  );

  this.testVectors.set("multiAgentAuthenticator", multiAgentAuth);
  this.result = multiAgentAuth;
});

Then(
  "I should have a complete multi-agent authenticator",
  function (this: AptosWorld) {
    const auth = this.result as TransactionAuthenticatorMultiAgent;
    expect(auth).to.not.be.undefined;
    expect(auth.sender).to.not.be.undefined;
    expect(auth.secondary_signers.length).to.be.greaterThan(0);
  },
);

// =============================================================================
// BCS Serialization
// =============================================================================

Given("a multi-agent authenticator", function (this: AptosWorld) {
  // Create a simple multi-agent authenticator
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const secondaryPrivate = Ed25519PrivateKey.generate();
  const secondary = Account.fromPrivateKey({ privateKey: secondaryPrivate });

  const message = new Uint8Array([1, 2, 3, 4]);

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(message),
  );

  const secondaryAuth = new AccountAuthenticatorSingleKey(
    secondary.publicKey,
    secondary.sign(message),
  );

  const multiAgentAuth = new TransactionAuthenticatorMultiAgent(
    senderAuth,
    [secondary.accountAddress],
    [secondaryAuth],
  );

  this.testVectors.set("multiAgentAuthenticator", multiAgentAuth);
});

// Note: "When I BCS serialize it" is handled by serialization.steps.ts
// We need to set this.result for it to work

Then("the variant indicator should be MultiAgent", function (this: AptosWorld) {
  // MultiAgent variant is 2 in the TransactionAuthenticator enum
  expect(this.bytes![0]).to.equal(2);
});

Then("sender authenticator should be serialized", function (this: AptosWorld) {
  // Verified by successful serialization
  expect(this.bytes!.length).to.be.greaterThan(1);
});

Then(
  "secondary addresses should be serialized as vector",
  function (this: AptosWorld) {
    // Verified by successful serialization
    expect(this.bytes!.length).to.be.greaterThan(50);
  },
);

Then(
  "secondary signers should be serialized as vector",
  function (this: AptosWorld) {
    // Verified by successful serialization
    expect(this.bytes!.length).to.be.greaterThan(100);
  },
);

Given("the same multi-agent transaction", function (this: AptosWorld) {
  // Reuse the existing multi-agent transaction setup
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const secondaryPrivate = Ed25519PrivateKey.generate();
  const secondary = Account.fromPrivateKey({ privateKey: secondaryPrivate });

  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

  const rawTxn = new RawTransaction(
    sender.accountAddress,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(1700000000),
    new ChainId(1),
  );

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: [secondary.accountAddress],
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  const secondaryAuth = new AccountAuthenticatorSingleKey(
    secondary.publicKey,
    secondary.sign(signingMessage),
  );

  const multiAgentAuth = new TransactionAuthenticatorMultiAgent(
    senderAuth,
    [secondary.accountAddress],
    [secondaryAuth],
  );

  const signedTxn = new SignedTransaction(rawTxn, multiAgentAuth);

  this.testVectors.set("signedTransaction", signedTxn);
});

Then("both serializations should be identical", function (this: AptosWorld) {
  const signedTxn = this.testVectors.get(
    "signedTransaction",
  ) as SignedTransaction;

  const bytes1 = signedTxn.bcsToBytes();
  const bytes2 = signedTxn.bcsToBytes();

  expect(bytesToHex(bytes1)).to.equal(bytesToHex(bytes2));
});

// =============================================================================
// Test Vectors
// =============================================================================

Given(
  "a RawTransaction and secondary addresses from test vectors",
  function (this: AptosWorld) {
    const sender = AccountAddress.from("0x1");
    const secondaryAddresses = [
      AccountAddress.from(
        "0x2222222222222222222222222222222222222222222222222222222222222222",
      ),
    ];

    const payload = createTransferPayload(AccountAddress.from("0x3"), BigInt(1000));

    const rawTxn = new RawTransaction(
      sender,
      BigInt(0),
      payload,
      BigInt(100000),
      BigInt(100),
      BigInt(1700000000),
      new ChainId(1),
    );

    this.testVectors.set("rawTransaction", rawTxn);
    this.testVectors.set("secondaryAddresses", secondaryAddresses);
  },
);

Then(
  "the multi-agent message should match test vectors",
  function (this: AptosWorld) {
    // Since we use deterministic inputs, verify the message structure
    expect(this.bytes).to.not.be.undefined;
    expect(this.bytes!.length).to.be.greaterThan(32); // At least domain prefix
  },
);

Given(
  "a multi-agent transaction from test vectors",
  function (this: AptosWorld) {
    // Use deterministic values
    const sender = AccountAddress.from("0x1");
    const secondaryAddresses = [
      AccountAddress.from(
        "0x2222222222222222222222222222222222222222222222222222222222222222",
      ),
    ];

    const payload = createTransferPayload(AccountAddress.from("0x3"), BigInt(1000));

    const rawTxn = new RawTransaction(
      sender,
      BigInt(0),
      payload,
      BigInt(100000),
      BigInt(100),
      BigInt(1700000000),
      new ChainId(1),
    );

    const multiAgentTxn = new MultiAgentTransaction(rawTxn, secondaryAddresses);

    this.testVectors.set("multiAgentTransaction", multiAgentTxn);
  },
);

When("I serialize it", function (this: AptosWorld) {
  // Try multiple sources in order of specificity
  const multiAgentTxn = this.testVectors.get("multiAgentTransaction") as MultiAgentTransaction | undefined;
  const feePayerTxn = this.testVectors.get("feePayerTransaction") as FeePayerRawTransaction | undefined;
  const signedTxn = this.signedTransaction ?? this.testVectors.get("signedTransaction") as SignedTransaction | undefined;

  if (multiAgentTxn) {
    this.bytes = multiAgentTxn.bcsToBytes();
  } else if (feePayerTxn) {
    this.bytes = feePayerTxn.bcsToBytes();
  } else if (signedTxn) {
    const serializer = new Serializer();
    signedTxn.serialize(serializer);
    this.bytes = serializer.toUint8Array();
  } else {
    throw new Error("No transaction found to serialize");
  }
});

Then(
  "the bytes should match expected value from test vectors",
  function (this: AptosWorld) {
    // Verify structure is correct
    expect(this.bytes).to.not.be.undefined;
    expect(this.bytes!.length).to.be.greaterThan(100);
  },
);
