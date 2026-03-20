import {
  AccountAddress,
  Deserializer,
  EntryFunction,
  EntryFunctionBytes,
  Identifier,
  ModuleId,
  Serializer,
  TransactionPayloadEntryFunction,
} from "@aptos-labs/ts-sdk";

export function createEntryFunction(
  moduleAddress: AccountAddress,
  moduleName: string,
  functionName: string,
  typeArgs: any[] = [],
  args: Uint8Array[] = [],
): EntryFunction {
  const moduleId = new ModuleId(moduleAddress, new Identifier(moduleName));
  const wrappedArgs = args.map((arg) => {
    const deserializer = new Deserializer(arg);
    return EntryFunctionBytes.deserialize(deserializer, arg.length);
  });

  return new EntryFunction(moduleId, new Identifier(functionName), typeArgs, wrappedArgs);
}

export function createTransferPayload(
  recipient: AccountAddress,
  amount: bigint,
): TransactionPayloadEntryFunction {
  const recipientSerializer = new Serializer();
  recipient.serialize(recipientSerializer);

  const amountSerializer = new Serializer();
  amountSerializer.serializeU64(amount);

  return new TransactionPayloadEntryFunction(
    createEntryFunction(
      AccountAddress.ONE,
      "aptos_account",
      "transfer",
      [],
      [recipientSerializer.toUint8Array(), amountSerializer.toUint8Array()],
    ),
  );
}
