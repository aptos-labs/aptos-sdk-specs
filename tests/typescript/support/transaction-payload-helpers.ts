import {
  AccountAddress,
  EntryFunction,
  Serializer,
  TransactionPayloadEntryFunction,
} from "@aptos-labs/ts-sdk";

export function createEntryFunction(
  moduleAddress: AccountAddress,
  moduleName: string,
  functionName: string,
  typeArgs: any[] = [],
  args: any[] = [],
): EntryFunction {
  return EntryFunction.build(
    `${moduleAddress.toString()}::${moduleName}`,
    functionName,
    typeArgs,
    args,
  );
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
