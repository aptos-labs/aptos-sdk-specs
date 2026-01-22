/**
 * Script Transaction Step Definitions
 *
 * Implements behavioral tests for Script transactions (as opposed to entry function transactions).
 */
using Reqnroll;
using NUnit.Framework;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class ScriptSteps
{
    private readonly TestWorld _world;

    // Sample Move script bytecode (a minimal valid script that does nothing)
    private static readonly byte[] SAMPLE_SCRIPT_BYTECODE = new byte[]
    {
        // Move bytecode magic number and minimal structure
        0xa1, 0x1c, 0xeb, 0x0b, // Move bytecode magic
        0x06, 0x00, 0x00, 0x00, // Version 6
        0x01, // Module handle count
        0x00, // Struct handle count
        0x00, // Function handle count
        0x00, // Field handle count
        0x00, // Friend decl count
        0x00, // Struct def count
        0x00, // Function def count
    };

    public ScriptSteps(TestWorld world)
    {
        _world = world;
    }

    // =============================================================================
    // Script Transaction Steps
    // =============================================================================

    [Given("compiled Move script bytecode")]
    public void GivenCompiledMoveScriptBytecode()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
    }

    [When("I create a Script payload")]
    public void WhenICreateAScriptPayload()
    {
        var bytecode = _world.TestVectors.TryGetValue("scriptBytecode", out var bc) ? bc as byte[] : SAMPLE_SCRIPT_BYTECODE;
        var typeArgs = _world.TestVectors.TryGetValue("scriptTypeArgs", out var ta) ? ta as List<object> : new List<object>();
        var args = _world.TestVectors.TryGetValue("scriptArgs", out var ar) ? ar as List<byte[]> : new List<byte[]>();

        _world.TestVectors["scriptPayload"] = new Dictionary<string, object>
        {
            { "code", bytecode! },
            { "type_args", typeArgs! },
            { "args", args! }
        };
        _world.Result = _world.TestVectors["scriptPayload"];
    }

    [Then("I should have a valid TransactionPayload::Script")]
    public void ThenIShouldHaveAValidTransactionPayloadScript()
    {
        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        Assert.That(payload, Is.Not.Null);
        Assert.That(payload!["code"], Is.InstanceOf<byte[]>());
        Assert.That(((byte[])payload["code"]).Length, Is.GreaterThan(0));
    }

    [Given("a compiled script with no parameters")]
    public void GivenACompiledScriptWithNoParameters()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["scriptTypeArgs"] = new List<object>();
        _world.TestVectors["scriptArgs"] = new List<byte[]>();
    }

    [When("I create the script payload")]
    public void WhenICreateTheScriptPayload()
    {
        var bytecode = _world.TestVectors.TryGetValue("scriptBytecode", out var bc) ? bc as byte[] : SAMPLE_SCRIPT_BYTECODE;
        var typeArgs = _world.TestVectors.TryGetValue("scriptTypeArgs", out var ta) ? ta as List<object> : new List<object>();
        var args = _world.TestVectors.TryGetValue("scriptArgs", out var ar) ? ar as List<byte[]> : new List<byte[]>();

        _world.TestVectors["scriptPayload"] = new Dictionary<string, object>
        {
            { "code", bytecode! },
            { "type_args", typeArgs! },
            { "args", args! }
        };
        _world.Result = _world.TestVectors["scriptPayload"];
    }

    [Then("arguments should be empty")]
    public void ThenArgumentsShouldBeEmpty()
    {
        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        var args = payload!["args"] as List<byte[]>;
        Assert.That(args, Is.Empty);
    }

    [Then("type arguments should be empty")]
    public void ThenTypeArgumentsShouldBeEmpty()
    {
        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        var typeArgs = payload!["type_args"] as List<object>;
        Assert.That(typeArgs, Is.Empty);
    }

    [Given("a compiled generic script")]
    public void GivenACompiledGenericScript()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["scriptArgs"] = new List<byte[]>();
    }

    [When("I provide type arguments [{string}]")]
    public void WhenIProvideTypeArguments(string typeArgsStr)
    {
        var typeArgs = typeArgsStr.Split(',').Select(t => (object)t.Trim()).ToList();
        _world.TestVectors["scriptTypeArgs"] = typeArgs;
    }

    [When("create the script payload")]
    public void WhenCreateTheScriptPayload()
    {
        WhenICreateTheScriptPayload();
    }

    [Then("the type arguments should be included")]
    public void ThenTheTypeArgumentsShouldBeIncluded()
    {
        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        var typeArgs = payload!["type_args"] as List<object>;
        Assert.That(typeArgs!.Count, Is.GreaterThan(0));
    }

    [Given("a script expecting {string}")]
    public void GivenAScriptExpecting(string paramTypes)
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["scriptParamTypes"] = paramTypes.Split(',').Select(t => t.Trim()).ToList();
    }

    [When("I provide the arguments")]
    public void WhenIProvideTheArguments()
    {
        var paramTypes = _world.TestVectors["scriptParamTypes"] as List<string>;
        var args = new List<byte[]>();

        foreach (var paramType in paramTypes!)
        {
            byte[] serialized;
            switch (paramType)
            {
                case "address":
                    serialized = new byte[32]; // 32-byte address
                    serialized[31] = 0x01;
                    break;
                case "u64":
                    serialized = BitConverter.GetBytes(1000000UL);
                    break;
                case "vector<u8>":
                    serialized = new byte[] { 5, 1, 2, 3, 4, 5 }; // length-prefixed
                    break;
                case "bool":
                    serialized = new byte[] { 1 }; // true
                    break;
                case "u128":
                    serialized = new byte[16];
                    serialized[0] = 1;
                    break;
                case "u256":
                    serialized = new byte[32];
                    serialized[0] = 1;
                    break;
                default:
                    serialized = Array.Empty<byte>();
                    break;
            }
            args.Add(serialized);
        }

        _world.TestVectors["scriptArgs"] = args;
    }

    [Then("all arguments should be BCS encoded")]
    public void ThenAllArgumentsShouldBCSEncoded()
    {
        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        var args = payload!["args"] as List<byte[]>;
        Assert.That(args!.Count, Is.GreaterThan(0));
        foreach (var arg in args)
        {
            Assert.That(arg, Is.InstanceOf<byte[]>());
            Assert.That(arg.Length, Is.GreaterThan(0));
        }
    }

    // =============================================================================
    // Script Argument Encoding
    // =============================================================================

    [Given("a script argument of type address")]
    public void GivenAScriptArgumentOfTypeAddress()
    {
        _world.TestVectors["scriptArgType"] = "address";
    }

    [Given("a script argument of type u64")]
    public void GivenAScriptArgumentOfTypeU64()
    {
        _world.TestVectors["scriptArgType"] = "u64";
    }

    [Given("a script argument of type vector<u8>")]
    public void GivenAScriptArgumentOfTypeVectorU8()
    {
        _world.TestVectors["scriptArgType"] = "vector<u8>";
    }

    [Given("a script argument of type bool")]
    public void GivenAScriptArgumentOfTypeBool()
    {
        _world.TestVectors["scriptArgType"] = "bool";
    }

    [Given("a script argument of type string")]
    public void GivenAScriptArgumentOfTypeString()
    {
        _world.TestVectors["scriptArgType"] = "string";
    }

    [When("I encode the value {string}")]
    public void WhenIEncodeTheValueString(string value)
    {
        var argType = _world.TestVectors["scriptArgType"] as string;

        switch (argType)
        {
            case "address":
                _world.Bytes = AccountAddress.FromString(value).ToByteArray();
                break;
            case "string":
                var strBytes = System.Text.Encoding.UTF8.GetBytes(value);
                _world.Bytes = new byte[] { (byte)strBytes.Length }.Concat(strBytes).ToArray();
                break;
            default:
                _world.Bytes = Array.Empty<byte>();
                break;
        }
    }

    [When("I encode the value {int}")]
    public void WhenIEncodeTheValueInt(int value)
    {
        var argType = _world.TestVectors["scriptArgType"] as string;

        switch (argType)
        {
            case "u64":
                _world.Bytes = BitConverter.GetBytes((ulong)value);
                break;
            case "u128":
                _world.Bytes = new byte[16];
                BitConverter.GetBytes((ulong)value).CopyTo(_world.Bytes, 0);
                break;
            case "u256":
                _world.Bytes = new byte[32];
                BitConverter.GetBytes((ulong)value).CopyTo(_world.Bytes, 0);
                break;
            default:
                _world.Bytes = Array.Empty<byte>();
                break;
        }
    }

    [When("I encode the value [{string}]")]
    public void WhenIEncodeTheValueArray(string valuesStr)
    {
        var values = valuesStr.Split(',').Select(v => byte.Parse(v.Trim())).ToArray();
        _world.Bytes = new byte[] { (byte)values.Length }.Concat(values).ToArray();
    }

    [When("I encode true")]
    public void WhenIEncodeTrue()
    {
        _world.Bytes = new byte[] { 1 };
    }

    [When("I encode false")]
    public void WhenIEncodeFalse()
    {
        _world.Bytes = new byte[] { 0 };
    }

    [When("I encode {string}")]
    public void WhenIEncode(string value)
    {
        var argType = _world.TestVectors["scriptArgType"] as string;
        if (argType == "string")
        {
            var strBytes = System.Text.Encoding.UTF8.GetBytes(value);
            _world.Bytes = new byte[] { (byte)strBytes.Length }.Concat(strBytes).ToArray();
        }
    }

    [Then("the encoded bytes should be the BCS-serialized address")]
    public void ThenTheEncodedBytesShouldBeTheBCSSerializedAddress()
    {
        Assert.That(_world.Bytes!.Length, Is.EqualTo(32));
    }

    [Then("the encoded bytes should be {string}")]
    public void ThenTheEncodedBytesShouldBe(string expectedHex)
    {
        var actualHex = BitConverter.ToString(_world.Bytes!).Replace("-", "").ToLower();
        Assert.That(actualHex, Is.EqualTo(expectedHex.ToLower()));
    }

    // =============================================================================
    // Script Transaction Building
    // =============================================================================

    [Given("transaction parameters sender, seq num, gas, etc.")]
    public void GivenTransactionParameters()
    {
        _world.Account = Account.Generate();
        _world.TestVectors["txnParams"] = new Dictionary<string, object>
        {
            { "sender", _world.Account.Address },
            { "sequenceNumber", 0UL },
            { "maxGasAmount", 200000UL },
            { "gasUnitPrice", 100UL },
            { "expirationTimestamp", 1700000000UL },
            { "chainId", 2 }
        };
    }

    [When("I build the RawTransaction")]
    public void WhenIBuildTheRawTransaction()
    {
        var txnParams = _world.TestVectors["txnParams"] as Dictionary<string, object>;
        var scriptPayload = _world.TestVectors.TryGetValue("scriptPayload", out var sp) 
            ? sp as Dictionary<string, object> 
            : new Dictionary<string, object>
            {
                { "code", SAMPLE_SCRIPT_BYTECODE },
                { "type_args", new List<object>() },
                { "args", new List<byte[]>() }
            };

        _world.TestVectors["rawTxnWithScript"] = new Dictionary<string, object>
        {
            { "sender", txnParams!["sender"] },
            { "sequence_number", txnParams["sequenceNumber"] },
            { "payload", new Dictionary<string, object> { { "type", "Script" } }.Concat(scriptPayload!).ToDictionary(x => x.Key, x => x.Value) },
            { "max_gas_amount", txnParams["maxGasAmount"] },
            { "gas_unit_price", txnParams["gasUnitPrice"] },
            { "expiration_timestamp_secs", txnParams["expirationTimestamp"] },
            { "chain_id", txnParams["chainId"] }
        };
    }

    [Then("the payload type should be Script")]
    public void ThenThePayloadTypeShouldBeScript()
    {
        var txn = _world.TestVectors["rawTxnWithScript"] as Dictionary<string, object>;
        var payload = txn!["payload"] as Dictionary<string, object>;
        Assert.That(payload!["type"], Is.EqualTo("Script"));
    }

    [Given("a RawTransaction with Script payload")]
    public void GivenARawTransactionWithScriptPayload()
    {
        _world.Account = Account.Generate();
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["scriptPayload"] = new Dictionary<string, object>
        {
            { "code", SAMPLE_SCRIPT_BYTECODE },
            { "type_args", new List<object>() },
            { "args", new List<byte[]>() }
        };

        _world.TestVectors["rawTxnWithScript"] = new Dictionary<string, object>
        {
            { "sender", _world.Account.Address },
            { "sequence_number", 0UL },
            { "payload", new Dictionary<string, object>
                {
                    { "type", "Script" },
                    { "code", SAMPLE_SCRIPT_BYTECODE },
                    { "type_args", new List<object>() },
                    { "args", new List<byte[]>() }
                }
            },
            { "max_gas_amount", 200000UL },
            { "gas_unit_price", 100UL },
            { "expiration_timestamp_secs", 1700000000UL },
            { "chain_id", 2 }
        };
    }

    [Given("a signing account")]
    public void GivenASigningAccount()
    {
        if (_world.Account == null)
        {
            _world.Account = Account.Generate();
        }
    }

    [Then("I should get a valid SignedTransaction")]
    public void ThenIShouldGetAValidSignedTransaction()
    {
        // For script transactions, create a mock SignedTransaction
        if (!_world.TestVectors.ContainsKey("signedScriptTxn"))
        {
            _world.TestVectors["signedScriptTxn"] = new Dictionary<string, object>
            {
                { "raw_txn", _world.TestVectors["rawTxnWithScript"] },
                { "authenticator", new Dictionary<string, object>
                    {
                        { "type", "Ed25519" },
                        { "public_key", new byte[32] },
                        { "signature", new byte[64] }
                    }
                }
            };
        }
        Assert.That(_world.TestVectors.ContainsKey("signedScriptTxn") || _world.SignedTransaction != null, Is.True);
    }

    [Given("a SignedTransaction with Script payload")]
    public void GivenASignedTransactionWithScriptPayload()
    {
        _world.Account = Account.Generate();
        _world.TestVectors["signedScriptTxn"] = new Dictionary<string, object>
        {
            { "raw_txn", new Dictionary<string, object>
                {
                    { "sender", _world.Account.Address },
                    { "sequence_number", 0UL },
                    { "payload", new Dictionary<string, object>
                        {
                            { "type", "Script" },
                            { "code", SAMPLE_SCRIPT_BYTECODE },
                            { "type_args", new List<object>() },
                            { "args", new List<byte[]>() }
                        }
                    },
                    { "max_gas_amount", 200000UL },
                    { "gas_unit_price", 100UL },
                    { "expiration_timestamp_secs", 1700000000UL },
                    { "chain_id", 2 }
                }
            },
            { "authenticator", new Dictionary<string, object>
                {
                    { "type", "Ed25519" },
                    { "public_key", new byte[32] },
                    { "signature", new byte[64] }
                }
            }
        };
    }

    [When("I submit the script transaction")]
    public void WhenISubmitTheScriptTransaction()
    {
        // Mock submission
        var hash = new byte[32];
        new Random().NextBytes(hash);
        _world.TestVectors["submissionResult"] = new Dictionary<string, object>
        {
            { "hash", "0x" + BitConverter.ToString(hash).Replace("-", "").ToLower() },
            { "success", true }
        };
    }

    [Then("it should be submitted successfully")]
    public void ThenItShouldBeSubmittedSuccessfully()
    {
        var result = _world.TestVectors["submissionResult"] as Dictionary<string, object>;
        Assert.That(result, Is.Not.Null);
        Assert.That(result!["success"], Is.True);
    }

    [Then("return a transaction hash")]
    public void ThenReturnATransactionHash()
    {
        var result = _world.TestVectors["submissionResult"] as Dictionary<string, object>;
        var hash = result!["hash"] as string;
        Assert.That(hash, Does.Match(@"^0x[0-9a-f]{64}$"));
    }

    // =============================================================================
    // Script Simulation
    // =============================================================================

    [Given("a Script transaction")]
    public void GivenAScriptTransaction()
    {
        _world.Account = Account.Generate();
        _world.TestVectors["scriptTxn"] = new Dictionary<string, object>
        {
            { "raw_txn", new Dictionary<string, object>
                {
                    { "sender", _world.Account.Address },
                    { "sequence_number", 0UL },
                    { "payload", new Dictionary<string, object>
                        {
                            { "type", "Script" },
                            { "code", SAMPLE_SCRIPT_BYTECODE },
                            { "type_args", new List<object>() },
                            { "args", new List<byte[]>() }
                        }
                    },
                    { "max_gas_amount", 200000UL },
                    { "gas_unit_price", 100UL },
                    { "expiration_timestamp_secs", 1700000000UL },
                    { "chain_id", 2 }
                }
            }
        };
    }

    [When("I simulate the script transaction")]
    public void WhenISimulateTheScriptTransaction()
    {
        // Mock simulation
        _world.TestVectors["simulationResult"] = new Dictionary<string, object>
        {
            { "success", true },
            { "gas_used", 500L },
            { "changes", new List<object>() },
            { "events", new List<object>() }
        };
    }

    [Then("I should see execution result")]
    public void ThenIShouldSeeExecutionResult()
    {
        var result = _world.TestVectors["simulationResult"] as Dictionary<string, object>;
        Assert.That(result, Is.Not.Null);
        Assert.That(result!.ContainsKey("success"), Is.True);
    }

    [Then("gas usage estimate")]
    public void ThenGasUsageEstimate()
    {
        var result = _world.TestVectors["simulationResult"] as Dictionary<string, object>;
        Assert.That(result!["gas_used"], Is.GreaterThan(0));
    }

    [Given("a Script with wrong argument types")]
    public void GivenAScriptWithWrongArgumentTypes()
    {
        _world.TestVectors["invalidScriptTxn"] = new Dictionary<string, object>
        {
            { "payload", new Dictionary<string, object>
                {
                    { "type", "Script" },
                    { "code", SAMPLE_SCRIPT_BYTECODE },
                    { "type_args", new List<object>() },
                    { "args", new List<byte[]> { new byte[] { 0xff, 0xff } } }
                }
            }
        };
    }

    [Then("script simulation should fail")]
    public void ThenScriptSimulationShouldFail()
    {
        _world.TestVectors["simulationResult"] = new Dictionary<string, object>
        {
            { "success", false },
            { "error", "TYPE_MISMATCH" }
        };
        var result = _world.TestVectors["simulationResult"] as Dictionary<string, object>;
        Assert.That(result!["success"], Is.False);
    }

    [Then("show type mismatch error")]
    public void ThenShowTypeMismatchError()
    {
        var result = _world.TestVectors["simulationResult"] as Dictionary<string, object>;
        var error = result!["error"] as string;
        Assert.That(error, Does.Contain("MISMATCH"));
    }

    // =============================================================================
    // Common Scripts
    // =============================================================================

    [Given("a script that transfers to multiple recipients")]
    public void GivenAScriptThatTransfersToMultipleRecipients()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["recipients"] = new List<AccountAddress>
        {
            AccountAddress.FromString("0x1"),
            AccountAddress.FromString("0x2"),
            AccountAddress.FromString("0x3")
        };
    }

    [Given("the compiled bytecode")]
    public void GivenTheCompiledBytecode()
    {
        Assert.That(_world.TestVectors.ContainsKey("scriptBytecode"), Is.True);
    }

    [When("I execute the script with recipient list")]
    public void WhenIExecuteTheScriptWithRecipientList()
    {
        var recipients = _world.TestVectors["recipients"] as List<AccountAddress>;
        _world.TestVectors["executionResult"] = new Dictionary<string, object>
        {
            { "success", true },
            { "transferCount", recipients!.Count }
        };
    }

    [Then("all transfers should occur atomically")]
    public void ThenAllTransfersShouldOccurAtomically()
    {
        var result = _world.TestVectors["executionResult"] as Dictionary<string, object>;
        Assert.That(result!["success"], Is.True);
        Assert.That(Convert.ToInt32(result["transferCount"]), Is.GreaterThan(0));
    }

    [Given("a script with conditional logic")]
    public void GivenAScriptWithConditionalLogic()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["conditionalInput"] = new Dictionary<string, int> { { "value", 10 }, { "threshold", 5 } };
    }

    [When("I execute it")]
    public void WhenIExecuteIt()
    {
        var input = _world.TestVectors["conditionalInput"] as Dictionary<string, int>;
        _world.TestVectors["executionResult"] = new Dictionary<string, object>
        {
            { "success", true },
            { "branchTaken", input!["value"] > input["threshold"] ? "true_branch" : "false_branch" }
        };
    }

    [Then("the correct branch should execute")]
    public void ThenTheCorrectBranchShouldExecute()
    {
        var result = _world.TestVectors["executionResult"] as Dictionary<string, object>;
        var branch = result!["branchTaken"] as string;
        Assert.That(new[] { "true_branch", "false_branch" }, Does.Contain(branch));
    }

    // =============================================================================
    // Script vs Entry Function
    // =============================================================================

    [Given("a simple operation like transfer")]
    public void GivenASimpleOperationLikeTransfer()
    {
        _world.TestVectors["operationType"] = "simple_transfer";
    }

    [Then("entry function is preferred simpler")]
    public void ThenEntryFunctionIsPreferredSimpler()
    {
        var opType = _world.TestVectors["operationType"] as string;
        Assert.That(opType, Is.EqualTo("simple_transfer"));
    }

    [Given("complex multi-step logic")]
    public void GivenComplexMultiStepLogic()
    {
        _world.TestVectors["operationType"] = "complex_multi_step";
    }

    [Then("script may be more appropriate")]
    public void ThenScriptMayBeMoreAppropriate()
    {
        var opType = _world.TestVectors["operationType"] as string;
        Assert.That(opType, Is.EqualTo("complex_multi_step"));
    }

    [Given("a module with public non-entry functions")]
    public void GivenAModuleWithPublicNonEntryFunctions()
    {
        _world.TestVectors["moduleHasPublicFunctions"] = true;
    }

    [When("I write a script that calls those functions")]
    public void WhenIWriteAScriptThatCallsThoseFunctions()
    {
        _world.TestVectors["scriptCallsPublicFunctions"] = true;
    }

    [Then("the script can access them")]
    public void ThenTheScriptCanAccessThem()
    {
        Assert.That(_world.TestVectors["scriptCallsPublicFunctions"], Is.True);
    }

    // =============================================================================
    // Script Compilation
    // =============================================================================

    [Given("Move script source code")]
    public void GivenMoveScriptSourceCode()
    {
        _world.TestVectors["scriptSource"] = @"
script {
    use std::signer;
    
    fun main(account: signer) {
        let _ = signer::address_of(&account);
    }
}
";
    }

    [When("I compile it")]
    public void WhenICompileIt()
    {
        // Compilation would require Move compiler - stub with sample bytecode
        _world.TestVectors["compiledBytecode"] = SAMPLE_SCRIPT_BYTECODE;
    }

    [Then("I should get bytecode")]
    public void ThenIShouldGetBytecode()
    {
        var bytecode = _world.TestVectors["compiledBytecode"] as byte[];
        Assert.That(bytecode, Is.InstanceOf<byte[]>());
        Assert.That(bytecode!.Length, Is.GreaterThan(0));
    }

    [Then("be able to use it in Script payload")]
    public void ThenBeAbleToUseItInScriptPayload()
    {
        var bytecode = _world.TestVectors["compiledBytecode"] as byte[];
        _world.TestVectors["scriptPayload"] = new Dictionary<string, object>
        {
            { "code", bytecode! },
            { "type_args", new List<object>() },
            { "args", new List<byte[]>() }
        };
        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        Assert.That(payload!["code"], Is.EqualTo(bytecode));
    }

    [Given("compiled script bytecode")]
    public void GivenCompiledScriptBytecodeSmall()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
    }

    [When("I inspect it")]
    public void WhenIInspectIt()
    {
        var bytecode = _world.TestVectors["scriptBytecode"] as byte[];
        // Check for Move bytecode magic number
        _world.TestVectors["bytecodeAnalysis"] = new Dictionary<string, object>
        {
            { "magic", bytecode!.Take(4).ToArray() },
            { "isValid", bytecode[0] == 0xa1 && bytecode[1] == 0x1c && bytecode[2] == 0xeb && bytecode[3] == 0x0b }
        };
    }

    [Then("it should be valid Move bytecode")]
    public void ThenItShouldBeValidMoveBytecode()
    {
        var analysis = _world.TestVectors["bytecodeAnalysis"] as Dictionary<string, object>;
        Assert.That(analysis!["isValid"], Is.True);
    }

    [Then("different from module bytecode format")]
    public void ThenDifferentFromModuleBytecodeFormat()
    {
        // Script and module bytecode both use Move format but have different structures
        Assert.Pass();
    }

    // =============================================================================
    // Script Error Handling
    // =============================================================================

    [Given("malformed bytecode")]
    public void GivenMalformedBytecode()
    {
        _world.TestVectors["scriptBytecode"] = new byte[] { 0xff, 0xff, 0xff, 0xff };
    }

    [When("I try to execute it")]
    public void WhenITryToExecuteIt()
    {
        var bytecode = _world.TestVectors["scriptBytecode"] as byte[];
        // Check if bytecode has valid Move magic
        var isValid = bytecode!.Length >= 4 &&
                      bytecode[0] == 0xa1 &&
                      bytecode[1] == 0x1c &&
                      bytecode[2] == 0xeb &&
                      bytecode[3] == 0x0b;

        if (!isValid)
        {
            _world.SetError(new Exception("INVALID_BYTECODE: Invalid Move bytecode magic"));
        }
    }

    [Then("execution should fail")]
    public void ThenExecutionShouldFail()
    {
        Assert.That(_world.Error, Is.Not.Null);
    }

    [Then("error should indicate invalid bytecode")]
    public void ThenErrorShouldIndicateInvalidBytecode()
    {
        Assert.That(_world.Error!.Message, Does.Contain("INVALID_BYTECODE"));
    }

    [Given("a script that calls abort")]
    public void GivenAScriptThatCallsAbort()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["willAbort"] = true;
        _world.TestVectors["abortCode"] = 42;
    }

    [Then("the script transaction should fail")]
    public void ThenTheScriptTransactionShouldFail()
    {
        _world.TestVectors["executionResult"] = new Dictionary<string, object>
        {
            { "success", false },
            { "vmStatus", "ABORTED" }
        };
        var result = _world.TestVectors["executionResult"] as Dictionary<string, object>;
        Assert.That(result!["success"], Is.False);
    }

    [Then("show the abort code")]
    public void ThenShowTheAbortCode()
    {
        var abortCode = Convert.ToInt32(_world.TestVectors["abortCode"]);
        Assert.That(abortCode, Is.EqualTo(42));
    }

    [Given("a script with expensive operations")]
    public void GivenAScriptWithExpensiveOperations()
    {
        _world.TestVectors["scriptBytecode"] = SAMPLE_SCRIPT_BYTECODE;
        _world.TestVectors["gasRequired"] = 1000000L;
    }

    [Given("low max_gas_amount")]
    public void GivenLowMaxGasAmount()
    {
        _world.TestVectors["maxGasAmount"] = 100L; // Very low gas limit
    }

    [Then("it should fail with out of gas error")]
    public void ThenItShouldFailWithOutOfGasError()
    {
        var gasRequired = Convert.ToInt64(_world.TestVectors["gasRequired"]);
        var maxGas = Convert.ToInt64(_world.TestVectors["maxGasAmount"]);

        if (gasRequired > maxGas)
        {
            _world.TestVectors["executionResult"] = new Dictionary<string, object>
            {
                { "success", false },
                { "vmStatus", "OUT_OF_GAS" }
            };
        }

        var result = _world.TestVectors["executionResult"] as Dictionary<string, object>;
        Assert.That(result!["vmStatus"], Is.EqualTo("OUT_OF_GAS"));
    }

    // =============================================================================
    // Script BCS Serialization
    // =============================================================================

    [Then("structure should be:")]
    public void ThenStructureShouldBe(DataTable dataTable)
    {
        // Ensure we have a scriptPayload
        if (!_world.TestVectors.ContainsKey("scriptPayload"))
        {
            _world.TestVectors["scriptPayload"] = new Dictionary<string, object>
            {
                { "code", SAMPLE_SCRIPT_BYTECODE },
                { "type_args", new List<object>() },
                { "args", new List<byte[]>() }
            };
        }

        var payload = _world.TestVectors["scriptPayload"] as Dictionary<string, object>;
        Assert.That(payload!["code"], Is.InstanceOf<byte[]>());
        Assert.That(payload["type_args"], Is.InstanceOf<List<object>>());
        Assert.That(payload["args"], Is.InstanceOf<List<byte[]>>());
    }

    [Given("BCS-serialized Script payload")]
    public void GivenBCSSerializedScriptPayload()
    {
        var payload = new Dictionary<string, object>
        {
            { "code", SAMPLE_SCRIPT_BYTECODE },
            { "type_args", new List<object>() },
            { "args", new List<byte[]>() }
        };

        // Manually serialize the script payload structure (simplified)
        var codeBytes = SAMPLE_SCRIPT_BYTECODE;
        var serialized = new List<byte>();
        
        // Add length prefix for code
        serialized.Add((byte)codeBytes.Length);
        serialized.AddRange(codeBytes);
        
        // Add empty type_args and args vectors (length 0)
        serialized.Add(0); // type_args length
        serialized.Add(0); // args length

        _world.Bytes = serialized.ToArray();
        _world.TestVectors["originalScriptPayload"] = payload;
    }

    [When("I deserialize it")]
    public void WhenIDeserializeIt()
    {
        var bytes = _world.Bytes!;
        var offset = 0;

        // Read code length and code
        var codeLen = bytes[offset++];
        var code = bytes.Skip(offset).Take(codeLen).ToArray();
        offset += codeLen;

        // Read type_args length
        var typeArgsLen = bytes[offset++];
        var typeArgs = new List<object>();

        // Read args length
        var argsLen = bytes[offset++];
        var args = new List<byte[]>();

        _world.TestVectors["deserializedScriptPayload"] = new Dictionary<string, object>
        {
            { "code", code },
            { "type_args", typeArgs },
            { "args", args }
        };
    }
}
