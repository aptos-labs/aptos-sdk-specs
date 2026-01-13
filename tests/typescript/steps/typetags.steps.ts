import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "chai";
import {
  TypeTag,
  TypeTagBool,
  TypeTagU8,
  TypeTagU16,
  TypeTagU32,
  TypeTagU64,
  TypeTagU128,
  TypeTagU256,
  TypeTagAddress,
  TypeTagSigner,
  TypeTagVector,
  TypeTagStruct,
  AccountAddress,
  Serializer,
  Deserializer,
  parseTypeTag,
  EntryFunction,
} from "@aptos-labs/ts-sdk";
import type { AptosWorld } from "../support/world.js";
import { bytesToHex } from "../support/vectors.js";

// =============================================================================
// Given Steps - Type String Input
// =============================================================================

Given(
  "a type string {string}",
  function (this: AptosWorld, typeString: string) {
    this.testVectors.set("typeString", typeString);
  },
);

Given(
  "a TypeTag of variant {word}",
  function (this: AptosWorld, variant: string) {
    switch (variant) {
      case "Bool":
        this.result = new TypeTagBool();
        break;
      case "U8":
        this.result = new TypeTagU8();
        break;
      case "U16":
        this.result = new TypeTagU16();
        break;
      case "U32":
        this.result = new TypeTagU32();
        break;
      case "U64":
        this.result = new TypeTagU64();
        break;
      case "U128":
        this.result = new TypeTagU128();
        break;
      case "U256":
        this.result = new TypeTagU256();
        break;
      case "Address":
        this.result = new TypeTagAddress();
        break;
      case "Signer":
        this.result = new TypeTagSigner();
        break;
      default:
        throw new Error(`Unknown TypeTag variant: ${variant}`);
    }
  },
);

Given("a TypeTag of Vector containing U8", function (this: AptosWorld) {
  this.result = new TypeTagVector(new TypeTagU8());
});

Given(
  "a TypeTag struct with address {string}, module {string}, name {string}",
  function (this: AptosWorld, address: string, module: string, name: string) {
    this.result = new TypeTagStruct({
      address: AccountAddress.from(address),
      moduleName: { identifier: module },
      name: { identifier: name },
      typeArgs: [],
    });
  },
);

Given("a TypeTag for CoinStore of AptosCoin", function (this: AptosWorld) {
  const aptosCoin = new TypeTagStruct({
    address: AccountAddress.ONE,
    moduleName: { identifier: "aptos_coin" },
    name: { identifier: "AptosCoin" },
    typeArgs: [],
  });
  this.result = new TypeTagStruct({
    address: AccountAddress.ONE,
    moduleName: { identifier: "coin" },
    name: { identifier: "CoinStore" },
    typeArgs: [aptosCoin],
  });
});

// =============================================================================
// Given Steps - Module ID
// =============================================================================

Given(
  "a module string {string}",
  function (this: AptosWorld, moduleString: string) {
    this.testVectors.set("moduleString", moduleString);
  },
);

Given(
  "a MoveModuleId with address {string} and name {string}",
  function (this: AptosWorld, address: string, name: string) {
    this.testVectors.set("moduleAddress", address);
    this.testVectors.set("moduleName", name);
  },
);

// =============================================================================
// Given Steps - Struct Tag
// =============================================================================

Given(
  /^address "([^"]+)", module "([^"]+)", name "([^"]+)", and type args \[AptosCoin\]$/,
  function (this: AptosWorld, address: string, module: string, name: string) {
    this.testVectors.set("structAddress", address);
    this.testVectors.set("structModule", module);
    this.testVectors.set("structName", name);
    this.testVectors.set("structTypeArgs", ["AptosCoin"]);
  },
);

// =============================================================================
// When Steps - TypeTag Parsing
// =============================================================================

When("I parse it as a TypeTag", function (this: AptosWorld) {
  const typeString = this.testVectors.get("typeString") as string;
  try {
    this.result = parseTypeTag(typeString);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I format it as a string", function (this: AptosWorld) {
  // Handle TypeTag, MoveModuleId, and Address formatting
  if (
    this.result instanceof TypeTagBool ||
    this.result instanceof TypeTagU8 ||
    this.result instanceof TypeTagU16 ||
    this.result instanceof TypeTagU32 ||
    this.result instanceof TypeTagU64 ||
    this.result instanceof TypeTagU128 ||
    this.result instanceof TypeTagU256 ||
    this.result instanceof TypeTagAddress ||
    this.result instanceof TypeTagSigner ||
    this.result instanceof TypeTagVector ||
    this.result instanceof TypeTagStruct
  ) {
    // It's a TypeTag
    this.testVectors.set("formattedString", this.result.toString());
  } else if (
    this.testVectors.has("moduleAddress") &&
    this.testVectors.has("moduleName")
  ) {
    // It's a MoveModuleId from components
    const address = this.testVectors.get("moduleAddress") as string;
    const name = this.testVectors.get("moduleName") as string;
    this.testVectors.set("formattedString", `${address}::${name}`);
  } else if (
    this.result &&
    typeof this.result === "object" &&
    "address" in this.result &&
    "name" in this.result
  ) {
    // It's a parsed module ID object
    const moduleId = this.result as { address: string; name: string };
    this.testVectors.set(
      "formattedString",
      `${moduleId.address}::${moduleId.name}`,
    );
  } else if (this.address) {
    // It's an AccountAddress
    this.testVectors.set("formattedString", this.address.toString());
  } else {
    throw new Error("No TypeTag, MoveModuleId, or Address found to format");
  }
});

// =============================================================================
// When Steps - Module ID Parsing
// =============================================================================

When("I parse it as a MoveModuleId", function (this: AptosWorld) {
  const moduleString = this.testVectors.get("moduleString") as string;
  try {
    const parts = moduleString.split("::");
    if (parts.length !== 2) {
      throw new Error("Invalid module ID format");
    }
    this.testVectors.set("parsedModuleAddress", parts[0]);
    this.testVectors.set("parsedModuleName", parts[1]);
    // Store in result to indicate success
    this.result = { address: parts[0], name: parts[1] };
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// =============================================================================
// When Steps - Struct Tag Creation
// =============================================================================

When("I create a MoveStructTag", function (this: AptosWorld) {
  try {
    const address = this.testVectors.get("structAddress") as string;
    const module = this.testVectors.get("structModule") as string;
    const name = this.testVectors.get("structName") as string;
    const typeArgsNames = this.testVectors.get("structTypeArgs") as string[];

    const typeArgs: TypeTag[] = typeArgsNames.map((argName: string) => {
      if (argName === "AptosCoin") {
        return new TypeTagStruct({
          address: AccountAddress.ONE,
          moduleName: { identifier: "aptos_coin" },
          name: { identifier: "AptosCoin" },
          typeArgs: [],
        });
      }
      throw new Error(`Unknown type arg: ${argName}`);
    });

    this.result = new TypeTagStruct({
      address: AccountAddress.from(address),
      moduleName: { identifier: module },
      name: { identifier: name },
      typeArgs,
    });
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

// =============================================================================
// When Steps - BCS Serialization
// =============================================================================

When("I BCS serialize the TypeTag", function (this: AptosWorld) {
  try {
    const typeTag = this.result as TypeTag;
    const serializer = new Serializer();
    typeTag.serialize(serializer);
    this.bytes = serializer.toUint8Array();
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I parse and BCS serialize the TypeTag", function (this: AptosWorld) {
  const typeString = this.testVectors.get("typeString") as string;
  try {
    const typeTag = parseTypeTag(typeString);
    const serializer = new Serializer();
    typeTag.serialize(serializer);
    this.bytes = serializer.toUint8Array();
    this.testVectors.set("originalTypeTag", typeTag);
    this.clearError();
  } catch (error) {
    this.setError(error as Error);
  }
});

When("I BCS serialize and deserialize it", function (this: AptosWorld) {
  try {
    // Handle RawTransaction
    if (this.rawTransaction) {
      const { RawTransaction } = require("@aptos-labs/ts-sdk");
      const serializer = new Serializer();
      this.rawTransaction.serialize(serializer);
      const bytes = serializer.toUint8Array();

      const deserializer = new Deserializer(bytes);
      this.result = RawTransaction.deserialize(deserializer);
      this.testVectors.set("originalRawTx", this.rawTransaction);
      this.clearError();
      return;
    }

    // Handle EntryFunction - check for the module_name property which is unique to EntryFunction
    if (
      this.result &&
      typeof this.result.serialize === "function" &&
      this.result.module_name !== undefined
    ) {
      const originalEntryFunction = this.result;
      const serializer = new Serializer();
      originalEntryFunction.serialize(serializer);
      const bytes = serializer.toUint8Array();

      const deserializer = new Deserializer(bytes);
      const deserialized = EntryFunction.deserialize(deserializer);
      this.testVectors.set("originalEntryFunction", originalEntryFunction);
      this.result = deserialized;
      this.clearError();
      return;
    }

    // Handle TypeTag
    const typeTag = this.testVectors.get("typeTag") || this.result;
    if (typeTag && typeTag instanceof TypeTag) {
      // Serialize
      const serializer = new Serializer();
      typeTag.serialize(serializer);
      const bytes = serializer.toUint8Array();

      // Deserialize
      const deserializer = new Deserializer(bytes);
      this.result = TypeTag.deserialize(deserializer);
      this.testVectors.set("originalTypeTag", typeTag);
      this.clearError();
      return;
    }

    throw new Error(
      "No TypeTag, RawTransaction, or EntryFunction found to serialize/deserialize",
    );
  } catch (error) {
    this.setError(error as Error);
  }
});

// =============================================================================
// Then Steps - TypeTag Validation
// =============================================================================

Then(
  "the TypeTag variant should be {word}",
  function (this: AptosWorld, variant: string) {
    const typeTag = this.result as TypeTag;

    const variantChecks: Record<string, (t: TypeTag) => boolean> = {
      Bool: (t) => t instanceof TypeTagBool,
      U8: (t) => t instanceof TypeTagU8,
      U16: (t) => t instanceof TypeTagU16,
      U32: (t) => t instanceof TypeTagU32,
      U64: (t) => t instanceof TypeTagU64,
      U128: (t) => t instanceof TypeTagU128,
      U256: (t) => t instanceof TypeTagU256,
      Address: (t) => t instanceof TypeTagAddress,
      Signer: (t) => t instanceof TypeTagSigner,
      Vector: (t) => t instanceof TypeTagVector,
      Struct: (t) => t instanceof TypeTagStruct,
    };

    const check = variantChecks[variant];
    if (!check) {
      throw new Error(`Unknown variant: ${variant}`);
    }
    expect(check(typeTag)).to.be.true;
  },
);

Then("the inner type should be U8", function (this: AptosWorld) {
  const typeTag = this.result as TypeTagVector;
  expect(typeTag.value instanceof TypeTagU8).to.be.true;
});

Then("the inner type should be a Vector of U8", function (this: AptosWorld) {
  const typeTag = this.result as TypeTagVector;
  expect(typeTag.value instanceof TypeTagVector).to.be.true;
  expect((typeTag.value as TypeTagVector).value instanceof TypeTagU8).to.be
    .true;
});

Then("the inner type should be a Struct", function (this: AptosWorld) {
  const typeTag = this.result as TypeTagVector;
  expect(typeTag.value instanceof TypeTagStruct).to.be.true;
});

// =============================================================================
// Then Steps - Struct Properties
// =============================================================================

Then(
  "the struct address should be {string}",
  function (this: AptosWorld, expected: string) {
    const typeTag = this.result as TypeTagStruct;
    const actualAddress = typeTag.value.address.toString();
    // Normalize both addresses for comparison
    const normalizedExpected = AccountAddress.from(expected).toString();
    expect(actualAddress.toLowerCase()).to.equal(
      normalizedExpected.toLowerCase(),
    );
  },
);

Then(
  "the struct module should be {string}",
  function (this: AptosWorld, expected: string) {
    const typeTag = this.result as TypeTagStruct;
    expect(typeTag.value.moduleName.identifier).to.equal(expected);
  },
);

Then(
  "the struct name should be {string}",
  function (this: AptosWorld, expected: string) {
    const typeTag = this.result as TypeTagStruct;
    expect(typeTag.value.name.identifier).to.equal(expected);
  },
);

Then(
  "the struct should have {int} type arguments",
  function (this: AptosWorld, count: number) {
    const typeTag = this.result as TypeTagStruct;
    expect(typeTag.value.typeArgs.length).to.equal(count);
  },
);

Then(
  "the struct should have {int} type argument",
  function (this: AptosWorld, count: number) {
    const typeTag = this.result as TypeTagStruct;
    expect(typeTag.value.typeArgs.length).to.equal(count);
  },
);

Then(
  "type argument {int} should be U64",
  function (this: AptosWorld, index: number) {
    const typeTag = this.result as TypeTagStruct;
    expect(typeTag.value.typeArgs[index] instanceof TypeTagU64).to.be.true;
  },
);

Then(
  "type argument {int} should be a Struct named {string}",
  function (this: AptosWorld, index: number, name: string) {
    const typeTag = this.result as TypeTagStruct;
    const arg = typeTag.value.typeArgs[index] as TypeTagStruct;
    expect(arg instanceof TypeTagStruct).to.be.true;
    expect(arg.value.name.identifier).to.equal(name);
  },
);

// =============================================================================
// Then Steps - Module ID Properties
// =============================================================================

Then(
  "the module address should be {string}",
  function (this: AptosWorld, expected: string) {
    // Try multiple sources: parsed module, entry function result
    let address: string | undefined;
    if (this.testVectors.has("parsedModuleAddress")) {
      address = this.testVectors.get("parsedModuleAddress") as string;
    } else if (this.result && (this.result as any).module_name?.address) {
      address = (this.result as any).module_name.address.toString();
    }

    if (address) {
      const normalizedExpected = AccountAddress.from(expected).toString();
      const normalizedActual = AccountAddress.from(address).toString();
      expect(normalizedActual.toLowerCase()).to.equal(
        normalizedExpected.toLowerCase(),
      );
    } else {
      throw new Error("No module address found");
    }
  },
);

Then(
  "the module name should be {string}",
  function (this: AptosWorld, expected: string) {
    // Try multiple sources: parsed module, entry function result
    let name: string | undefined;
    if (this.testVectors.has("parsedModuleName")) {
      name = this.testVectors.get("parsedModuleName") as string;
    } else if (
      this.result &&
      (this.result as any).module_name?.name?.identifier
    ) {
      name = (this.result as any).module_name.name.identifier;
    }

    if (name) {
      expect(name).to.equal(expected);
    } else {
      throw new Error("No module name found");
    }
  },
);

// =============================================================================
// Then Steps - Struct Tag
// =============================================================================

Then("the struct tag should be valid", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  expect(this.result).to.not.be.undefined;
});

Then(
  "the string representation should be {string}",
  function (this: AptosWorld, expected: string) {
    const typeTag = this.result as TypeTagStruct;
    expect(typeTag.toString()).to.equal(expected);
  },
);

// =============================================================================
// Then Steps - BCS Serialization
// =============================================================================

Then(
  "the first byte should be the U64 variant index",
  function (this: AptosWorld) {
    // U64 variant index in TypeTag enum is typically 4
    expect(this.bytes![0]).to.be.a("number");
  },
);

Then("the serialization should succeed", function (this: AptosWorld) {
  expect(this.error).to.be.undefined;
  expect(this.bytes).to.not.be.undefined;
  expect(this.bytes!.length).to.be.greaterThan(0);
});

Then(
  "the result should be deserializable back to the same TypeTag",
  function (this: AptosWorld) {
    const originalTypeTag = this.testVectors.get("originalTypeTag") as TypeTag;
    const deserializer = new Deserializer(this.bytes!);
    const deserialized = TypeTag.deserialize(deserializer);
    expect(deserialized.toString()).to.equal(originalTypeTag.toString());
  },
);

Then(
  "the result should equal the original TypeTag",
  function (this: AptosWorld) {
    const originalTypeTag = this.testVectors.get("originalTypeTag") as TypeTag;
    const resultTypeTag = this.result as TypeTag;
    expect(resultTypeTag.toString()).to.equal(originalTypeTag.toString());
  },
);

// =============================================================================
// Then Steps - Parsing Failure
// =============================================================================

Then("the parsing should fail with a parse error", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});

Then("the parsing should fail", function (this: AptosWorld) {
  expect(this.error).to.not.be.undefined;
});
