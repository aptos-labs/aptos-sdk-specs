import { Then } from "@cucumber/cucumber";
import { expect } from "chai";
import type { AptosWorld } from "../support/world.js";

Then("the result should be {int} byte", function (this: AptosWorld, count: number) {
  const result = (this.result as Uint8Array | undefined) ?? this.bytes;
  expect(result, "expected result bytes to be set").to.not.be.undefined;
  expect(result!.length).to.equal(count);
});

Then("the result should be {int} bytes", function (this: AptosWorld, count: number) {
  const result = (this.result as Uint8Array | undefined) ?? this.bytes;
  expect(result, "expected result bytes to be set").to.not.be.undefined;
  expect(result!.length).to.equal(count);
});

Then("the result should be {bool}", async function (this: AptosWorld, bool: boolean) {
  expect(this.result).to.equal(bool);
});

Then("the result should be [{bytes}]", async function (this: AptosWorld, bytes: number[]) {
  const result = (this.result as Uint8Array | undefined) ?? this.bytes;
  expect(result, "expected result bytes to be set").to.not.be.undefined;
  expect(result!.length).to.equal(bytes.length);
  expect(result!.every((value, index) => value === bytes[index])).to.be.true;
});

Then("the first byte should be 0x02 \\(outer length)", async function () {
  const result = (this.result as Uint8Array | undefined) ?? this.bytes;
  expect(result, "expected result bytes to be set").to.not.be.undefined;
  expect(result![0]).to.equal(0x02);
});
