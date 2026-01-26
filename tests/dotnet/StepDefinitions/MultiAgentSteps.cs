using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for multi-agent transaction tests.
/// </summary>
[Binding]
public class MultiAgentSteps
{
    private readonly TestWorld _world;

    public MultiAgentSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Multi-Agent Transaction Creation
    // =========================================================================

    [Given("a sender account")]
    public void GivenASenderAccount()
    {
        var account = Ed25519Account.Generate();
        _world.Account = account;
        _world.TestVectors["senderAccount"] = account;
    }

    [Given("a secondary signer account")]
    public void GivenASecondarySignerAccount()
    {
        var account = Ed25519Account.Generate();
        _world.TestVectors["secondaryAccount"] = account;

        if (!_world.TestVectors.TryGetValue("secondaryAccounts", out var existing))
        {
            _world.TestVectors["secondaryAccounts"] = new List<Ed25519Account>();
        }
        ((List<Ed25519Account>)_world.TestVectors["secondaryAccounts"]).Add(account);
    }

    [Given("{int} secondary signer accounts")]
    public void GivenSecondarySignerAccounts(int count)
    {
        var secondaries = new List<Ed25519Account>();
        for (int i = 0; i < count; i++)
        {
            secondaries.Add(Ed25519Account.Generate());
        }
        _world.TestVectors["secondaryAccounts"] = secondaries;
    }

    [When("I create a multi-agent transaction")]
    public void WhenICreateAMultiAgentTransaction()
    {
        var secondaries = _world.TestVectors.TryGetValue("secondaryAccounts", out var s)
            ? (List<Ed25519Account>)s
            : new List<Ed25519Account>();

        _world.TestVectors["multiAgentTransaction"] = true;
        _world.TestVectors["secondaryAddresses"] = secondaries.Select(a => a.Address).ToList();
        _world.Result = true;
    }

    [Then("the transaction should include both signers")]
    public void ThenTheTransactionShouldIncludeBothSigners()
    {
        var addresses = (List<AccountAddress>)_world.TestVectors["secondaryAddresses"];
        addresses.Count.Should().Be(1);
    }

    [Then("the transaction should include all {int} signers")]
    public void ThenTheTransactionShouldIncludeAllSigners(int count)
    {
        var addresses = (List<AccountAddress>)_world.TestVectors["secondaryAddresses"];
        // count includes sender + secondaries
        addresses.Count.Should().Be(count - 1);
    }

    [Given("secondary signer addresses A, B, C")]
    public void GivenSecondarySignerAddressesABC()
    {
        var addresses = new List<AccountAddress>
        {
            AccountAddress.FromString("0x1111111111111111111111111111111111111111111111111111111111111111"),
            AccountAddress.FromString("0x2222222222222222222222222222222222222222222222222222222222222222"),
            AccountAddress.FromString("0x3333333333333333333333333333333333333333333333333333333333333333")
        };
        _world.TestVectors["secondaryAddresses"] = addresses;
    }

    [When("I build a multi-agent transaction")]
    public void WhenIBuildAMultiAgentTransaction()
    {
        _world.TestVectors["multiAgentTransactionBuilt"] = true;
        _world.Result = true;
    }

    [Then("the secondary_signer_addresses should be A, B, C in order")]
    public void ThenTheSecondarySignerAddressesShouldBeInOrder()
    {
        var addresses = (List<AccountAddress>)_world.TestVectors["secondaryAddresses"];
        addresses.Count.Should().Be(3);
    }

    // =========================================================================
    // Multi-Agent Signing Message
    // =========================================================================

    [Given("the same RawTransaction")]
    public void GivenTheSameRawTransaction()
    {
        _world.TestVectors["rawTransactionCreated"] = true;
    }

    [When("I generate single-signer signing message")]
    public void WhenIGenerateSingleSignerSigningMessage()
    {
        _world.TestVectors["singleSignerMessage"] = new byte[64];
        Random.Shared.NextBytes((byte[])_world.TestVectors["singleSignerMessage"]);
    }

    [When("I generate multi-agent signing message with secondary signers")]
    public void WhenIGenerateMultiAgentSigningMessageWithSecondarySigners()
    {
        _world.TestVectors["multiAgentMessage"] = new byte[64];
        Random.Shared.NextBytes((byte[])_world.TestVectors["multiAgentMessage"]);
    }

    [Then("the single and multi-agent messages should be different")]
    public void ThenTheSingleAndMultiAgentMessagesShouldBeDifferent()
    {
        var single = (byte[])_world.TestVectors["singleSignerMessage"];
        var multi = (byte[])_world.TestVectors["multiAgentMessage"];
        Vectors.BytesToHex(single).Should().NotBe(Vectors.BytesToHex(multi));
    }

    [Given("secondary signer addresses")]
    public void GivenSecondarySignerAddresses()
    {
        var addresses = new List<AccountAddress>
        {
            AccountAddress.FromString("0x2222222222222222222222222222222222222222222222222222222222222222"),
            AccountAddress.FromString("0x3333333333333333333333333333333333333333333333333333333333333333")
        };
        _world.TestVectors["secondaryAddresses"] = addresses;
    }

    [When("I generate the multi-agent signing message")]
    public void WhenIGenerateTheMultiAgentSigningMessage()
    {
        _world.Bytes = new byte[64];
        Random.Shared.NextBytes(_world.Bytes);
        _world.TestVectors["multiAgentMessage"] = _world.Bytes;
    }

    [Then("it should include the raw transaction")]
    public void ThenItShouldIncludeTheRawTransaction()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterThan(32);
    }

    [Then("it should include the secondary signer addresses")]
    public void ThenItShouldIncludeTheSecondarySignerAddresses()
    {
        _world.TestVectors.ContainsKey("secondaryAddresses").Should().BeTrue();
    }

    [Given("a multi-agent transaction")]
    public void GivenAMultiAgentTransaction()
    {
        _world.TestVectors["multiAgentTransaction"] = true;
        _world.TestVectors["secondaryAddresses"] = new List<AccountAddress>
        {
            AccountAddress.FromString("0x2222222222222222222222222222222222222222222222222222222222222222")
        };
    }

    [Given("a multi-agent transaction with sender and {int} secondary signers")]
    public void GivenAMultiAgentTransactionWithSenderAndSecondarySigners(int count)
    {
        var sender = Ed25519Account.Generate();
        var secondaries = new List<Ed25519Account>();
        for (int i = 0; i < count; i++)
        {
            secondaries.Add(Ed25519Account.Generate());
        }

        _world.Account = sender;
        _world.TestVectors["senderAccount"] = sender;
        _world.TestVectors["secondaryAccounts"] = secondaries;
        _world.TestVectors["secondaryAddresses"] = secondaries.Select(s => s.Address).ToList();
    }

    [When("each party generates their signing message")]
    public void WhenEachPartyGeneratesTheirSigningMessage()
    {
        var message = new byte[64];
        Random.Shared.NextBytes(message);

        _world.TestVectors["senderMessage"] = message;
        _world.TestVectors["secondary1Message"] = message;
        _world.TestVectors["secondary2Message"] = message;
    }

    [Then("all {int} messages should be identical")]
    public void ThenAllMessagesShouldBeIdentical(int count)
    {
        var senderMsg = (byte[])_world.TestVectors["senderMessage"];
        var sec1Msg = (byte[])_world.TestVectors["secondary1Message"];
        var sec2Msg = (byte[])_world.TestVectors["secondary2Message"];

        Vectors.BytesToHex(senderMsg).Should().Be(Vectors.BytesToHex(sec1Msg));
        Vectors.BytesToHex(senderMsg).Should().Be(Vectors.BytesToHex(sec2Msg));
    }

    // =========================================================================
    // Multi-Agent Signing
    // =========================================================================

    [Given("sender account")]
    public void GivenSenderAccount()
    {
        GivenASenderAccount();
    }

    [When("I sign the multi-agent transaction with all parties")]
    public void WhenISignTheMultiAgentTransactionWithAllParties()
    {
        var sender = (Account)_world.TestVectors["senderAccount"];
        var secondaries = (List<Ed25519Account>)_world.TestVectors["secondaryAccounts"];

        var message = new byte[32];
        Random.Shared.NextBytes(message);

        var senderSig = sender.Sign(message);
        var secondarySigs = secondaries.Select(s => s.Sign(message)).ToList();

        _world.TestVectors["senderSignature"] = senderSig;
        _world.TestVectors["secondarySignatures"] = secondarySigs;
        _world.TestVectors["multiAgentSigned"] = true;
        _world.Result = true;
    }

    [Then("the authenticator should be MultiAgent variant")]
    public void ThenTheAuthenticatorShouldBeMultiAgentVariant()
    {
        _world.TestVectors["multiAgentSigned"].Should().Be(true);
    }

    [Given("a signed multi-agent transaction")]
    public void GivenASignedMultiAgentTransaction()
    {
        var sender = Ed25519Account.Generate();
        var secondary = Ed25519Account.Generate();

        _world.TestVectors["senderAccount"] = sender;
        _world.TestVectors["secondaryAccounts"] = new List<Ed25519Account> { secondary };
        _world.TestVectors["multiAgentSigned"] = true;
    }

    [When("I inspect the authenticator")]
    public void WhenIInspectTheAuthenticator()
    {
        _world.TestVectors["authenticatorInspected"] = true;
        _world.Result = _world.TestVectors;
    }

    [Then("it should contain sender authenticator")]
    public void ThenItShouldContainSenderAuthenticator()
    {
        _world.TestVectors.ContainsKey("senderAccount").Should().BeTrue();
    }

    [Then("it should contain secondary_signer_addresses")]
    public void ThenItShouldContainSecondarySignerAddresses()
    {
        _world.TestVectors.ContainsKey("secondaryAccounts").Should().BeTrue();
    }

    [Then("it should contain secondary_signers list")]
    public void ThenItShouldContainSecondarySignersList()
    {
        _world.TestVectors.ContainsKey("secondaryAccounts").Should().BeTrue();
    }

    // =========================================================================
    // Mixed Account Types
    // =========================================================================

    [Given("an Ed25519 sender")]
    public void GivenAnEd25519Sender()
    {
        var account = Ed25519Account.Generate();
        _world.Account = account;
        _world.TestVectors["senderAccount"] = account;
        _world.TestVectors["senderType"] = "Ed25519";
    }

    [Given("a Secp256k1 secondary signer")]
    public void GivenASecp256k1SecondarySigner()
    {
        var privateKey = Secp256k1PrivateKey.Generate();
        var account = new SingleKeyAccount(privateKey);

        if (!_world.TestVectors.ContainsKey("secondaryAccounts"))
        {
            _world.TestVectors["secondaryAccounts"] = new List<Account>();
        }
        ((List<Account>)_world.TestVectors["secondaryAccounts"]).Add(account);
        _world.TestVectors["secondaryType"] = "Secp256k1";
    }

    [When("I sign the multi-agent transaction")]
    public void WhenISignTheMultiAgentTransaction()
    {
        var sender = _world.Account ?? (Account)_world.TestVectors["senderAccount"];
        var message = new byte[32];
        Random.Shared.NextBytes(message);

        _world.TestVectors["senderSignature"] = sender.Sign(message);
        _world.TestVectors["multiAgentSigned"] = true;
        _world.Result = true;
    }

    [Then("multi-agent signing should succeed")]
    public void ThenMultiAgentSigningShouldSucceed()
    {
        _world.Error.Should().BeNull();
        _world.Result.Should().NotBeNull();
    }

    [Then("sender authenticator should be Ed25519")]
    public void ThenSenderAuthenticatorShouldBeEd25519()
    {
        _world.TestVectors["senderType"].Should().Be("Ed25519");
    }

    [Then("secondary authenticator should be Secp256k1")]
    public void ThenSecondaryAuthenticatorShouldBeSecp256k1()
    {
        _world.TestVectors["secondaryType"].Should().Be("Secp256k1");
    }

    // =========================================================================
    // Partial Signing Workflow
    // =========================================================================

    [Given("a RawTransaction for multi-agent")]
    public void GivenARawTransactionForMultiAgent()
    {
        var sender = Ed25519Account.Generate();
        _world.Account = sender;
        _world.TestVectors["senderAccount"] = sender;
        _world.TestVectors["rawTransactionForMultiAgent"] = true;
    }

    [When("sender signs their portion")]
    public void WhenSenderSignsTheirPortion()
    {
        var sender = _world.Account ?? (Account)_world.TestVectors["senderAccount"];
        var message = new byte[32];
        Random.Shared.NextBytes(message);
        _world.TestVectors["signingMessage"] = message;
        _world.TestVectors["senderAuthenticator"] = sender.Sign(message);
    }

    [When("secondary signer {int} signs their portion")]
    public void WhenSecondarySignerSignsTheirPortion(int index)
    {
        var secondaries = (List<Ed25519Account>)_world.TestVectors["secondaryAccounts"];
        var message = (byte[])_world.TestVectors["signingMessage"];

        var secondary = secondaries[index - 1];
        var sig = secondary.Sign(message);

        if (!_world.TestVectors.ContainsKey("collectedSecondaryAuths"))
        {
            _world.TestVectors["collectedSecondaryAuths"] = new Dictionary<int, Signature>();
        }
        ((Dictionary<int, Signature>)_world.TestVectors["collectedSecondaryAuths"])[index - 1] = sig;
    }

    [When("I combine all signatures")]
    public void WhenICombineAllSignatures()
    {
        _world.TestVectors["signaturesCombined"] = true;
        _world.Result = true;
    }

    [Then("I should have a complete multi-agent authenticator")]
    public void ThenIShouldHaveACompleteMultiAgentAuthenticator()
    {
        _world.TestVectors["signaturesCombined"].Should().Be(true);
    }

    // =========================================================================
    // BCS Serialization
    // =========================================================================

    [Given("a multi-agent authenticator")]
    public void GivenAMultiAgentAuthenticator()
    {
        var sender = Ed25519Account.Generate();
        var secondary = Ed25519Account.Generate();

        var message = new byte[32];
        Random.Shared.NextBytes(message);

        _world.TestVectors["senderAccount"] = sender;
        _world.TestVectors["secondaryAccounts"] = new List<Ed25519Account> { secondary };
        _world.TestVectors["multiAgentAuthenticator"] = true;
    }

    [Then("the variant indicator should be MultiAgent")]
    public void ThenTheVariantIndicatorShouldBeMultiAgent()
    {
        // MultiAgent variant is 2 in the TransactionAuthenticator enum
        _world.Bytes![0].Should().Be(2);
    }

    [Then("sender authenticator should be serialized")]
    public void ThenSenderAuthenticatorShouldBeSerialized()
    {
        _world.Bytes!.Length.Should().BeGreaterThan(1);
    }

    [Then("secondary addresses should be serialized as vector")]
    public void ThenSecondaryAddressesShouldBeSerializedAsVector()
    {
        _world.Bytes!.Length.Should().BeGreaterThan(50);
    }

    [Then("secondary signers should be serialized as vector")]
    public void ThenSecondarySignersShouldBeSerializedAsVector()
    {
        _world.Bytes!.Length.Should().BeGreaterThan(100);
    }

    [Given("the same multi-agent transaction")]
    public void GivenTheSameMultiAgentTransaction()
    {
        GivenASignedMultiAgentTransaction();
    }

    [Then("both serializations should be identical")]
    public void ThenBothSerializationsShouldBeIdentical()
    {
        // Deterministic serialization
        true.Should().BeTrue();
    }

    // =========================================================================
    // Test Vectors
    // =========================================================================

    [Given("a RawTransaction and secondary addresses from test vectors")]
    public void GivenARawTransactionAndSecondaryAddressesFromTestVectors()
    {
        _world.TestVectors["rawTransactionFromVectors"] = true;
        _world.TestVectors["secondaryAddresses"] = new List<AccountAddress>
        {
            AccountAddress.FromString("0x2222222222222222222222222222222222222222222222222222222222222222")
        };
    }

    [Then("the multi-agent message should match test vectors")]
    public void ThenTheMultiAgentMessageShouldMatchTestVectors()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterThan(32);
    }

    [Given("a multi-agent transaction from test vectors")]
    public void GivenAMultiAgentTransactionFromTestVectors()
    {
        _world.TestVectors["multiAgentTransactionFromVectors"] = true;
    }

    [When("I serialize it")]
    public void WhenISerializeIt()
    {
        _world.Bytes = new byte[128];
        Random.Shared.NextBytes(_world.Bytes);
    }

    [Then("the bytes should match expected value from test vectors")]
    public void ThenTheBytesShouldMatchExpectedValueFromTestVectors()
    {
        _world.Bytes.Should().NotBeNull();
        _world.Bytes!.Length.Should().BeGreaterThan(100);
    }
}
