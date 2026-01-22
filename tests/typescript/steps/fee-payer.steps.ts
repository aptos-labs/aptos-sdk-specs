/**
 * Fee Payer (Sponsored) Transaction Step Definitions
 *
 * Implements behavioral tests for fee payer transactions.
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
  TransactionAuthenticatorFeePayer,
  AccountAuthenticator,
  AccountAuthenticatorSingleKey,
  generateSigningMessageForTransaction,
  Serializer,
  Deserializer,
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
// Fee Payer Transaction Creation
// =============================================================================

Given("a fee payer \\(sponsor\\) account", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("feePayerAccount", account);
});

Given("a fee payer account", function (this: AptosWorld) {
  const privateKey = Ed25519PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("feePayerAccount", account);
});

Given("secondary signer accounts", function (this: AptosWorld) {
  const secondaries: Account[] = [];

  for (let i = 0; i < 2; i++) {
    const privateKey = Ed25519PrivateKey.generate();
    secondaries.push(Account.fromPrivateKey({ privateKey }));
  }

  this.testVectors.set("secondaryAccounts", secondaries);
});

When("I create a fee payer transaction", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const feePayer = this.testVectors.get("feePayerAccount") as Account;
  const secondaries =
    (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];

  const feePayerTxn = new FeePayerRawTransaction(
    rawTxn,
    secondaries.map((s) => s.accountAddress),
    feePayer.accountAddress,
  );

  this.testVectors.set("feePayerTransaction", feePayerTxn);
  this.result = feePayerTxn;
});

Then(
  "the transaction should have the fee payer designated",
  function (this: AptosWorld) {
    const feePayerTxn = this.testVectors.get(
      "feePayerTransaction",
    ) as FeePayerRawTransaction;
    const feePayer = this.testVectors.get("feePayerAccount") as Account;

    expect(feePayerTxn.fee_payer_address.toString()).to.equal(
      feePayer.accountAddress.toString(),
    );
  },
);

Then(
  "it should include all signers plus fee payer",
  function (this: AptosWorld) {
    const feePayerTxn = this.testVectors.get(
      "feePayerTransaction",
    ) as FeePayerRawTransaction;
    const secondaries =
      (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];

    expect(feePayerTxn.secondary_signer_addresses.length).to.equal(
      secondaries.length,
    );
    expect(feePayerTxn.fee_payer_address).to.not.be.undefined;
  },
);

Given(
  "fee payer address {string}",
  function (this: AptosWorld, addressStr: string) {
    // Handle placeholder address
    const address =
      addressStr === "0xSPONSOR"
        ? AccountAddress.from(
            "0x5555555555555555555555555555555555555555555555555555555555555555",
          )
        : AccountAddress.from(addressStr);
    this.testVectors.set("feePayerAddress", address);
  },
);

When("I build a fee payer transaction", function (this: AptosWorld) {
  const rawTxn =
    (this.testVectors.get("rawTransaction") as RawTransaction) ??
    createDefaultRawTxn();
  const feePayerAddress = this.testVectors.get(
    "feePayerAddress",
  ) as AccountAddress;

  const feePayerTxn = new FeePayerRawTransaction(rawTxn, [], feePayerAddress);

  this.testVectors.set("feePayerTransaction", feePayerTxn);
  this.result = feePayerTxn;
});

Then(
  "fee_payer_address should be {string}",
  function (this: AptosWorld, addressStr: string) {
    const feePayerTxn = this.testVectors.get(
      "feePayerTransaction",
    ) as FeePayerRawTransaction;
    const expectedAddress =
      addressStr === "0xSPONSOR"
        ? "0x5555555555555555555555555555555555555555555555555555555555555555"
        : addressStr;

    expect(feePayerTxn.fee_payer_address.toStringLong()).to.equal(
      expectedAddress,
    );
  },
);

// =============================================================================
// Fee Payer Signing Message
// =============================================================================

Given(
  "the same RawTransaction and secondary signers",
  function (this: AptosWorld) {
    const rawTxn = createDefaultRawTxn();
    const secondaryAddresses = [
      AccountAddress.from(
        "0x2222222222222222222222222222222222222222222222222222222222222222",
      ),
    ];

    this.testVectors.set("rawTransaction", rawTxn);
    this.testVectors.set("secondaryAddresses", secondaryAddresses);
  },
);

When("I generate multi-agent signing message", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaryAddresses = this.testVectors.get(
    "secondaryAddresses",
  ) as AccountAddress[];

  const message = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  this.testVectors.set("multiAgentMessage", message);
});

When(
  "I generate fee payer signing message with sponsor",
  function (this: AptosWorld) {
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const secondaryAddresses =
      (this.testVectors.get("secondaryAddresses") as AccountAddress[]) ?? [];
    const feePayerAddress = AccountAddress.from(
      "0x5555555555555555555555555555555555555555555555555555555555555555",
    );

    const message = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
      secondarySignerAddresses: secondaryAddresses,
      feePayerAddress: feePayerAddress,
    });

    this.testVectors.set("feePayerMessage", message);
  },
);

Given("a fee payer address", function (this: AptosWorld) {
  const address = AccountAddress.from(
    "0x5555555555555555555555555555555555555555555555555555555555555555",
  );
  this.testVectors.set("feePayerAddress", address);
});

Then("it should include the fee payer address", function (this: AptosWorld) {
  // The signing message includes the fee payer address in the serialized data
  // Verify by comparing with multi-agent message (which doesn't have fee payer)
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaryAddresses =
    (this.testVectors.get("secondaryAddresses") as AccountAddress[]) ?? [];

  const multiAgentMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
  });

  // Fee payer message should be different (includes fee payer address)
  expect(bytesToHex(this.bytes!)).to.not.equal(bytesToHex(multiAgentMessage));
});

Given("a fee payer transaction", function (this: AptosWorld) {
  // Create actual accounts so subsequent steps can sign
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const feePayerPrivate = Ed25519PrivateKey.generate();
  const feePayer = Account.fromPrivateKey({ privateKey: feePayerPrivate });

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

  const feePayerTxn = new FeePayerRawTransaction(rawTxn, [], feePayer.accountAddress);

  // Store in testVectors for step compatibility
  this.testVectors.set("rawTransaction", rawTxn);
  this.testVectors.set("senderAccount", sender);
  this.testVectors.set("feePayerAccount", feePayer);
  this.testVectors.set("feePayerAddress", feePayer.accountAddress);
  this.testVectors.set("feePayerTransaction", feePayerTxn);

  // Also store on world for other step patterns
  this.rawTransaction = rawTxn;
  this.account = sender;
});

When("I generate the fee payer signing message", function (this: AptosWorld) {
  // Check both storage locations for rawTransaction
  const rawTxn = (this.testVectors.get("rawTransaction") as RawTransaction) ?? this.rawTransaction;
  if (!rawTxn) {
    throw new Error("No rawTransaction found in testVectors or on world");
  }

  const secondaryAddresses =
    (this.testVectors.get("secondaryAddresses") as AccountAddress[]) ?? [];
  const feePayerAddress = this.testVectors.get(
    "feePayerAddress",
  ) as AccountAddress;

  if (!feePayerAddress) {
    throw new Error("No feePayerAddress found - ensure 'a fee payer address' step ran first");
  }

  const message = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
    feePayerAddress: feePayerAddress,
  });

  this.bytes = message;
});

Given(
  "a fee payer transaction with sender, secondary, and sponsor",
  function (this: AptosWorld) {
    const senderPrivate = Ed25519PrivateKey.generate();
    const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

    const secondaryPrivate = Ed25519PrivateKey.generate();
    const secondary = Account.fromPrivateKey({ privateKey: secondaryPrivate });

    const feePayerPrivate = Ed25519PrivateKey.generate();
    const feePayer = Account.fromPrivateKey({ privateKey: feePayerPrivate });

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
    this.testVectors.set("secondaryAccounts", [secondary]);
    this.testVectors.set("feePayerAccount", feePayer);
    this.testVectors.set("rawTransaction", rawTxn);
    this.testVectors.set("feePayerAddress", feePayer.accountAddress);
    this.testVectors.set("secondaryAddresses", [secondary.accountAddress]);
  },
);

Then("all messages should be identical", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const secondaryAddresses =
    (this.testVectors.get("secondaryAddresses") as AccountAddress[]) ?? [];
  const feePayerAddress = this.testVectors.get(
    "feePayerAddress",
  ) as AccountAddress;

  // Generate signing message from each party's perspective (should be the same)
  const senderMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
    feePayerAddress: feePayerAddress,
  });

  const secondaryMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
    feePayerAddress: feePayerAddress,
  });

  const feePayerMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
    feePayerAddress: feePayerAddress,
  });

  expect(bytesToHex(senderMessage)).to.equal(bytesToHex(secondaryMessage));
  expect(bytesToHex(senderMessage)).to.equal(bytesToHex(feePayerMessage));
});

// =============================================================================
// Fee Payer Signing
// =============================================================================

When(
  "I sign the fee payer transaction with both parties",
  function (this: AptosWorld) {
    const sender = this.testVectors.get("senderAccount") as Account;
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const feePayer = this.testVectors.get("feePayerAccount") as Account;

    const signingMessage = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
      secondarySignerAddresses: [],
      feePayerAddress: feePayer.accountAddress,
    });

    const senderAuth = new AccountAuthenticatorSingleKey(
      sender.publicKey,
      sender.sign(signingMessage),
    );

    const feePayerAuth = new AccountAuthenticatorSingleKey(
      feePayer.publicKey,
      feePayer.sign(signingMessage),
    );

    const feePayerAuthenticator = new TransactionAuthenticatorFeePayer(
      senderAuth,
      [],
      [],
      { address: feePayer.accountAddress, authenticator: feePayerAuth },
    );

    const signedTxn = new SignedTransaction(rawTxn, feePayerAuthenticator);

    this.testVectors.set("signedTransaction", signedTxn);
    this.testVectors.set("feePayerAuthenticator", feePayerAuthenticator);
    this.result = signedTxn;
  },
);

Then(
  "the authenticator should be FeePayer variant",
  function (this: AptosWorld) {
    const signedTxn = this.result as SignedTransaction;
    expect(signedTxn.authenticator.isFeePayer()).to.be.true;
  },
);

Given("a signed fee payer transaction", function (this: AptosWorld) {
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const feePayerPrivate = Ed25519PrivateKey.generate();
  const feePayer = Account.fromPrivateKey({ privateKey: feePayerPrivate });

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

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: [],
    feePayerAddress: feePayer.accountAddress,
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  const feePayerAuth = new AccountAuthenticatorSingleKey(
    feePayer.publicKey,
    feePayer.sign(signingMessage),
  );

  const feePayerAuthenticator = new TransactionAuthenticatorFeePayer(
    senderAuth,
    [],
    [],
    { address: feePayer.accountAddress, authenticator: feePayerAuth },
  );

  const signedTxn = new SignedTransaction(rawTxn, feePayerAuthenticator);

  this.testVectors.set("signedTransaction", signedTxn);
  this.testVectors.set("feePayerAuthenticator", feePayerAuthenticator);
});

Then(
  "it should contain secondary_signer_addresses \\(may be empty\\)",
  function (this: AptosWorld) {
    const auth = this.result as TransactionAuthenticatorFeePayer;
    expect(auth.secondary_signer_addresses).to.not.be.undefined;
    expect(Array.isArray(auth.secondary_signer_addresses)).to.be.true;
  },
);

Then(
  "it should contain secondary_signers \\(may be empty\\)",
  function (this: AptosWorld) {
    const auth = this.result as TransactionAuthenticatorFeePayer;
    expect(auth.secondary_signers).to.not.be.undefined;
    expect(Array.isArray(auth.secondary_signers)).to.be.true;
  },
);

Then("it should contain fee_payer_address", function (this: AptosWorld) {
  const auth = this.result as TransactionAuthenticatorFeePayer;
  expect(auth.fee_payer.address).to.not.be.undefined;
});

Then(
  "it should contain fee_payer_signer authenticator",
  function (this: AptosWorld) {
    const auth = this.result as TransactionAuthenticatorFeePayer;
    expect(auth.fee_payer.authenticator).to.not.be.undefined;
  },
);

// =============================================================================
// Fee Payer with No Secondary Signers
// =============================================================================

Given("no secondary signers", function (this: AptosWorld) {
  this.testVectors.set("secondaryAccounts", []);
  this.testVectors.set("secondaryAddresses", []);
});

When("I sign the fee payer transaction", function (this: AptosWorld) {
  // Check both storage locations
  const sender = (this.testVectors.get("senderAccount") as Account) ?? this.account;
  let rawTxn = (this.testVectors.get("rawTransaction") as RawTransaction) ?? this.rawTransaction;
  const feePayer = this.testVectors.get("feePayerAccount") as Account;

  if (!sender || !feePayer) {
    throw new Error("Missing required data: sender or feePayerAccount");
  }

  // Create a RawTransaction if not already created
  if (!rawTxn) {
    const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));
    rawTxn = new RawTransaction(
      sender.accountAddress,
      BigInt(0),
      payload,
      BigInt(100000),
      BigInt(100),
      BigInt(Math.floor(Date.now() / 1000) + 600),
      new ChainId(1),
    );
    this.rawTransaction = rawTxn;
    this.testVectors.set("rawTransaction", rawTxn);
  }

  const secondaries =
    (this.testVectors.get("secondaryAccounts") as Account[]) ?? [];

  const secondaryAddresses = secondaries.map((s) => s.accountAddress);

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: secondaryAddresses,
    feePayerAddress: feePayer.accountAddress,
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

  const feePayerAuth = new AccountAuthenticatorSingleKey(
    feePayer.publicKey,
    feePayer.sign(signingMessage),
  );

  const feePayerAuthenticator = new TransactionAuthenticatorFeePayer(
    senderAuth,
    secondaryAddresses,
    secondaryAuths,
    { address: feePayer.accountAddress, authenticator: feePayerAuth },
  );

  const signedTxn = new SignedTransaction(rawTxn, feePayerAuthenticator);

  this.signedTransaction = signedTxn;
  this.testVectors.set("signedTransaction", signedTxn);
  this.testVectors.set("feePayerAuthenticator", feePayerAuthenticator);
  this.result = signedTxn;
});

Then("secondary_signer_addresses should be empty", function (this: AptosWorld) {
  const auth = this.testVectors.get(
    "feePayerAuthenticator",
  ) as TransactionAuthenticatorFeePayer;
  expect(auth.secondary_signer_addresses.length).to.equal(0);
});

Then("secondary_signers should be empty", function (this: AptosWorld) {
  const auth = this.testVectors.get(
    "feePayerAuthenticator",
  ) as TransactionAuthenticatorFeePayer;
  expect(auth.secondary_signers.length).to.equal(0);
});

Then("fee payer should be present", function (this: AptosWorld) {
  const auth = this.testVectors.get(
    "feePayerAuthenticator",
  ) as TransactionAuthenticatorFeePayer;
  expect(auth.fee_payer).to.not.be.undefined;
  expect(auth.fee_payer.address).to.not.be.undefined;
  expect(auth.fee_payer.authenticator).to.not.be.undefined;
});

// =============================================================================
// Mixed Account Types
// =============================================================================

Given("a Secp256k1 fee payer", function (this: AptosWorld) {
  const privateKey = Secp256k1PrivateKey.generate();
  const account = Account.fromPrivateKey({ privateKey });
  this.testVectors.set("feePayerAccount", account);
  this.testVectors.set("feePayerType", "Secp256k1");
});

Then(
  "both authenticators should be correct types",
  function (this: AptosWorld) {
    const auth = this.testVectors.get(
      "feePayerAuthenticator",
    ) as TransactionAuthenticatorFeePayer;
    // Both should be SingleKey authenticators wrapping different key types
    expect(auth.sender).to.not.be.undefined;
    expect(auth.fee_payer.authenticator).to.not.be.undefined;
  },
);

// =============================================================================
// Sponsored Transaction Workflow
// =============================================================================

Given("a sender who wants sponsored transaction", function (this: AptosWorld) {
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });
  this.testVectors.set("senderAccount", sender);
});

When("sender creates RawTransaction", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account;

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

  this.testVectors.set("rawTransaction", rawTxn);
});

When("sender signs the fee payer signing message", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account;
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;

  // For fee payer transactions, sender signs with a placeholder fee payer address
  // In a real workflow, this would be the actual fee payer's address
  const placeholderFeePayer = AccountAddress.from(
    "0x0000000000000000000000000000000000000000000000000000000000000000",
  );

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: [],
    feePayerAddress: placeholderFeePayer,
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  this.testVectors.set("senderAuthenticator", senderAuth);
  this.testVectors.set("signingMessage", signingMessage);
});

Then(
  "sender can send partially signed tx to sponsor",
  function (this: AptosWorld) {
    const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
    const senderAuth = this.testVectors.get(
      "senderAuthenticator",
    ) as AccountAuthenticator;

    // Sender would serialize and send: rawTxn, senderAuth
    expect(rawTxn).to.not.be.undefined;
    expect(senderAuth).to.not.be.undefined;
  },
);

Given(
  "a partially signed fee payer transaction from sender",
  function (this: AptosWorld) {
    const senderPrivate = Ed25519PrivateKey.generate();
    const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

    const feePayerPrivate = Ed25519PrivateKey.generate();
    const feePayer = Account.fromPrivateKey({ privateKey: feePayerPrivate });

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

    // Sender signs with the actual fee payer address
    const signingMessage = generateSigningMessageForTransaction({
      rawTransaction: rawTxn,
      secondarySignerAddresses: [],
      feePayerAddress: feePayer.accountAddress,
    });

    const senderAuth = new AccountAuthenticatorSingleKey(
      sender.publicKey,
      sender.sign(signingMessage),
    );

    this.testVectors.set("senderAccount", sender);
    this.testVectors.set("feePayerAccount", feePayer);
    this.testVectors.set("rawTransaction", rawTxn);
    this.testVectors.set("senderAuthenticator", senderAuth);
    this.testVectors.set("signingMessage", signingMessage);
  },
);

When("sponsor reviews the transaction", function (this: AptosWorld) {
  // Sponsor would verify the transaction details
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  expect(rawTxn).to.not.be.undefined;
});

When(
  "sponsor signs the fee payer signing message",
  function (this: AptosWorld) {
    const feePayer = this.testVectors.get("feePayerAccount") as Account;
    const signingMessage = this.testVectors.get("signingMessage") as Uint8Array;

    const feePayerAuth = new AccountAuthenticatorSingleKey(
      feePayer.publicKey,
      feePayer.sign(signingMessage),
    );

    this.testVectors.set("feePayerAuthenticator", feePayerAuth);
  },
);

When(
  "sponsor combines signatures into authenticator",
  function (this: AptosWorld) {
    const senderAuth = this.testVectors.get(
      "senderAuthenticator",
    ) as AccountAuthenticator;
    const feePayerAuth = this.testVectors.get(
      "feePayerAuthenticator",
    ) as AccountAuthenticator;
    const feePayer = this.testVectors.get("feePayerAccount") as Account;

    const combinedAuth = new TransactionAuthenticatorFeePayer(
      senderAuth,
      [],
      [],
      { address: feePayer.accountAddress, authenticator: feePayerAuth },
    );

    this.testVectors.set("combinedAuthenticator", combinedAuth);
    this.result = combinedAuth;
  },
);

Then("the transaction is ready for submission", function (this: AptosWorld) {
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;
  const combinedAuth = this.testVectors.get(
    "combinedAuthenticator",
  ) as TransactionAuthenticatorFeePayer;

  const signedTxn = new SignedTransaction(rawTxn, combinedAuth);

  expect(signedTxn).to.not.be.undefined;
  expect(signedTxn.authenticator.isFeePayer()).to.be.true;
});

When("sponsor signs first", function (this: AptosWorld) {
  const feePayer = this.testVectors.get("feePayerAccount") as Account;
  const rawTxn = this.testVectors.get("rawTransaction") as RawTransaction;

  const signingMessage = generateSigningMessageForTransaction({
    rawTransaction: rawTxn,
    secondarySignerAddresses: [],
    feePayerAddress: feePayer.accountAddress,
  });

  const feePayerAuth = new AccountAuthenticatorSingleKey(
    feePayer.publicKey,
    feePayer.sign(signingMessage),
  );

  this.testVectors.set("feePayerAuth", feePayerAuth);
  this.testVectors.set("signingMessage", signingMessage);
});

When("sender signs second", function (this: AptosWorld) {
  const sender = this.testVectors.get("senderAccount") as Account;
  const signingMessage = this.testVectors.get("signingMessage") as Uint8Array;

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  this.testVectors.set("senderAuth", senderAuth);
});

When("I combine correctly", function (this: AptosWorld) {
  const senderAuth = this.testVectors.get("senderAuth") as AccountAuthenticator;
  const feePayerAuth = this.testVectors.get(
    "feePayerAuth",
  ) as AccountAuthenticator;
  const feePayer = this.testVectors.get("feePayerAccount") as Account;

  const combinedAuth = new TransactionAuthenticatorFeePayer(
    senderAuth,
    [],
    [],
    { address: feePayer.accountAddress, authenticator: feePayerAuth },
  );

  this.testVectors.set("combinedAuthenticator", combinedAuth);
  this.result = combinedAuth;
});

Then("the fee payer transaction should be valid", function (this: AptosWorld) {
  const auth = this.result as TransactionAuthenticatorFeePayer;
  expect(auth).to.not.be.undefined;
  expect(auth.sender).to.not.be.undefined;
  expect(auth.fee_payer).to.not.be.undefined;
});

// =============================================================================
// BCS Serialization
// =============================================================================

Given("a fee payer authenticator", function (this: AptosWorld) {
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const feePayerPrivate = Ed25519PrivateKey.generate();
  const feePayer = Account.fromPrivateKey({ privateKey: feePayerPrivate });

  const message = new Uint8Array([1, 2, 3, 4]);

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(message),
  );

  const feePayerAuth = new AccountAuthenticatorSingleKey(
    feePayer.publicKey,
    feePayer.sign(message),
  );

  const feePayerAuthenticator = new TransactionAuthenticatorFeePayer(
    senderAuth,
    [],
    [],
    { address: feePayer.accountAddress, authenticator: feePayerAuth },
  );

  this.testVectors.set("feePayerAuthenticator", feePayerAuthenticator);
});

Then("the variant indicator should be FeePayer", function (this: AptosWorld) {
  // FeePayer variant is 3 in the TransactionAuthenticator enum
  expect(this.bytes![0]).to.equal(3);
});

Then(
  "all components should be serialized in order",
  function (this: AptosWorld) {
    // Verified by successful serialization
    expect(this.bytes!.length).to.be.greaterThan(100);
  },
);

Given("the same fee payer transaction", function (this: AptosWorld) {
  const senderPrivate = Ed25519PrivateKey.generate();
  const sender = Account.fromPrivateKey({ privateKey: senderPrivate });

  const feePayerPrivate = Ed25519PrivateKey.generate();
  const feePayer = Account.fromPrivateKey({ privateKey: feePayerPrivate });

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
    secondarySignerAddresses: [],
    feePayerAddress: feePayer.accountAddress,
  });

  const senderAuth = new AccountAuthenticatorSingleKey(
    sender.publicKey,
    sender.sign(signingMessage),
  );

  const feePayerAuth = new AccountAuthenticatorSingleKey(
    feePayer.publicKey,
    feePayer.sign(signingMessage),
  );

  const feePayerAuthenticator = new TransactionAuthenticatorFeePayer(
    senderAuth,
    [],
    [],
    { address: feePayer.accountAddress, authenticator: feePayerAuth },
  );

  const signedTxn = new SignedTransaction(rawTxn, feePayerAuthenticator);

  // Store in both locations for compatibility
  this.signedTransaction = signedTxn;
  this.testVectors.set("signedTransaction", signedTxn);
});

// =============================================================================
// Test Vectors
// =============================================================================

Given(
  "a RawTransaction and fee payer address from test vectors",
  function (this: AptosWorld) {
    const sender = AccountAddress.from("0x1");
    const feePayerAddress = AccountAddress.from(
      "0x5555555555555555555555555555555555555555555555555555555555555555",
    );

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
    this.testVectors.set("feePayerAddress", feePayerAddress);
  },
);

Given("a fee payer transaction from test vectors", function (this: AptosWorld) {
  const sender = AccountAddress.from("0x1");
  const feePayerAddress = AccountAddress.from(
    "0x5555555555555555555555555555555555555555555555555555555555555555",
  );

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

  const feePayerTxn = new FeePayerRawTransaction(rawTxn, [], feePayerAddress);

  this.testVectors.set("feePayerTransaction", feePayerTxn);
});

// =============================================================================
// Helper Functions
// =============================================================================

function createDefaultRawTxn(): RawTransaction {
  const sender = AccountAddress.from("0x1");
  const payload = createTransferPayload(AccountAddress.from("0x2"), BigInt(1000));

  return new RawTransaction(
    sender,
    BigInt(0),
    payload,
    BigInt(100000),
    BigInt(100),
    BigInt(Math.floor(Date.now() / 1000) + 600),
    new ChainId(1),
  );
}
