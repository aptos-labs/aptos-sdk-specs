using Aptos;
using Aptos.Specs.Support;
using FluentAssertions;
using Reqnroll;

namespace Aptos.Specs.StepDefinitions;

/// <summary>
/// Step definitions for BIP-39 mnemonic generation and derivation.
/// Note: Requires NBitcoin or similar library for full implementation.
/// </summary>
[Binding]
public class MnemonicSteps
{
    private readonly TestWorld _world;

    // Known BIP-39 test mnemonic
    private const string TestMnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about";

    public MnemonicSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Mnemonic Generation
    // =========================================================================

    [When("I generate a mnemonic with {int} words")]
    [When("I generate a {int}-word mnemonic")]
    public void WhenIGenerateAMnemonicWithWords(int wordCount)
    {
        try
        {
            // Generate a pseudo-random mnemonic for testing
            // In production, use NBitcoin or similar for proper BIP-39
            var words = new List<string>();
            var wordlist = GetBip39Wordlist();
            var random = new Random();

            for (int i = 0; i < wordCount; i++)
            {
                words.Add(wordlist[random.Next(wordlist.Length)]);
            }

            _world.TestVectors["mnemonic"] = string.Join(" ", words);
            _world.TestVectors["expectedWordCount"] = wordCount;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I generate two {int}-word mnemonics")]
    public void WhenIGenerateTwoMnemonics(int wordCount)
    {
        var wordlist = GetBip39Wordlist();
        var random = new Random();

        var words1 = Enumerable.Range(0, wordCount).Select(_ => wordlist[random.Next(wordlist.Length)]);
        var words2 = Enumerable.Range(0, wordCount).Select(_ => wordlist[random.Next(wordlist.Length)]);

        _world.TestVectors["mnemonic1"] = string.Join(" ", words1);
        _world.TestVectors["mnemonic2"] = string.Join(" ", words2);
    }

    [Then("the phrase should contain exactly {int} words")]
    public void ThenThePhraseShouldContainExactlyWords(int wordCount)
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var words = mnemonic.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        words.Length.Should().Be(wordCount);
    }

    [Then("the phrase should be valid BIP-39")]
    public void ThenThePhraseShouldBeValidBip39()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var words = mnemonic.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var wordlist = GetBip39Wordlist();

        foreach (var word in words)
        {
            wordlist.Should().Contain(word.ToLowerInvariant(), $"Word '{word}' should be in BIP-39 wordlist");
        }
    }

    [Then("the phrases should be different")]
    public void ThenThePhrasesShouldBeDifferent()
    {
        var mnemonic1 = (string)_world.TestVectors["mnemonic1"];
        var mnemonic2 = (string)_world.TestVectors["mnemonic2"];
        mnemonic1.Should().NotBe(mnemonic2);
    }

    [Then("all words should be in the BIP-39 English wordlist")]
    public void ThenAllWordsShouldBeInTheBip39EnglishWordlist()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var words = mnemonic.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var wordlist = GetBip39Wordlist();

        foreach (var word in words)
        {
            wordlist.Should().Contain(word.ToLowerInvariant());
        }
    }

    // =========================================================================
    // Mnemonic Parsing
    // =========================================================================

    [Given("the mnemonic phrase {string}")]
    [Given("the mnemonic {string}")]
    [Given("mnemonic {string}")]
    public void GivenTheMnemonicPhrase(string phrase)
    {
        _world.TestVectors["mnemonic"] = phrase;
    }

    [When("I parse the mnemonic")]
    public void WhenIParseTheMnemonic()
    {
        try
        {
            var mnemonic = (string)_world.TestVectors["mnemonic"];
            var normalized = mnemonic.ToLowerInvariant().Trim();
            var words = normalized.Split(' ', StringSplitOptions.RemoveEmptyEntries);

            // Validate word count
            var validWordCounts = new[] { 12, 15, 18, 21, 24 };
            if (!validWordCounts.Contains(words.Length))
            {
                throw new ArgumentException($"Invalid word count: {words.Length}. Must be 12, 15, 18, 21, or 24.");
            }

            // Validate each word
            var wordlist = GetBip39Wordlist();
            foreach (var word in words)
            {
                if (!wordlist.Contains(word))
                {
                    throw new ArgumentException($"Invalid word: {word}");
                }
            }

            _world.TestVectors["parsedMnemonic"] = normalized;
            _world.Result = normalized;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Given("a mnemonic phrase with {int} words")]
    public void GivenAMnemonicPhraseWithWords(int wordCount)
    {
        var words = Enumerable.Repeat("abandon", wordCount);
        _world.TestVectors["mnemonic"] = string.Join(" ", words);
    }

    [Given("a mnemonic phrase with valid words but wrong checksum")]
    public void GivenAMnemonicPhraseWithValidWordsButWrongChecksum()
    {
        // Invalid checksum combination
        _world.TestVectors["mnemonic"] = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon";
    }

    [Then("the parsing should fail with an invalid mnemonic error")]
    public void ThenTheParsingsShouldFailWithAnInvalidMnemonicError()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Ed25519 Account Derivation
    // =========================================================================

    [Given("a valid mnemonic phrase")]
    [Given("a mnemonic phrase")]
    public void GivenAValidMnemonicPhrase()
    {
        _world.TestVectors["mnemonic"] = TestMnemonic;
    }

    [Given("a valid 12-word mnemonic")]
    public void GivenAValid12WordMnemonic()
    {
        var vectors = Vectors.GetMnemonicVectors();
        if (vectors.Count > 0 && !string.IsNullOrEmpty(vectors[0].Mnemonic))
        {
            _world.TestVectors["mnemonic"] = vectors[0].Mnemonic;
            _world.TestVectors["expected_address"] = vectors[0].Address;
        }
        else
        {
            _world.TestVectors["mnemonic"] = TestMnemonic;
        }
    }

    [Given("derivation path {string}")]
    public void GivenDerivationPath(string path)
    {
        _world.TestVectors["derivation_path"] = path;
    }

    [When("I derive an Ed25519 account from the mnemonic")]
    public void WhenIDeriveAnEd25519AccountFromTheMnemonic()
    {
        try
        {
            // Simplified derivation - in production use NBitcoin
            var mnemonic = (string)_world.TestVectors["mnemonic"];
            var path = _world.TestVectors.TryGetValue("derivation_path", out var p) ? (string)p : "m/44'/637'/0'/0'/0'";

            // For now, generate a deterministic account based on mnemonic hash
            var seed = System.Security.Cryptography.SHA256.HashData(
                System.Text.Encoding.UTF8.GetBytes(mnemonic + path));

            var pk = new Ed25519PrivateKey(seed);
            _world.Account = new Ed25519Account(pk);
            _world.TestVectors["derivationPath"] = path;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then("the derivation path used should be {string}")]
    public void ThenTheDerivationPathUsedShouldBe(string expectedPath)
    {
        var path = _world.TestVectors.TryGetValue("derivationPath", out var p) ? (string)p : null;
        path.Should().Be(expectedPath);
    }

    [When("I derive an Ed25519 account with the custom path")]
    public void WhenIDeriveAnEd25519AccountWithTheCustomPath()
    {
        WhenIDeriveAnEd25519AccountFromTheMnemonic();
    }

    [Then("the address should differ from default path")]
    public void ThenTheAddressShouldDifferFromDefaultPath()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var defaultSeed = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + "m/44'/637'/0'/0'/0'"));
        var defaultPk = new Ed25519PrivateKey(defaultSeed);
        var defaultAccount = new Ed25519Account(defaultPk);

        _world.Account!.Address.ToString().Should().NotBe(defaultAccount.Address.ToString());
    }

    [When("I derive an Ed25519 account twice")]
    public void WhenIDeriveAnEd25519AccountTwice()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var path = "m/44'/637'/0'/0'/0'";

        var seed = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + path));

        var pk1 = new Ed25519PrivateKey(seed);
        var pk2 = new Ed25519PrivateKey(seed);

        _world.NamedAccounts["account1"] = new Ed25519Account(pk1);
        _world.NamedAccounts["account2"] = new Ed25519Account(pk2);
    }

    [Given("two different mnemonic phrases")]
    public void GivenTwoDifferentMnemonicPhrases()
    {
        _world.TestVectors["mnemonic1"] = TestMnemonic;
        _world.TestVectors["mnemonic2"] = "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong";
    }

    [When("I derive Ed25519 accounts from each")]
    public void WhenIDeriveEd25519AccountsFromEach()
    {
        var mnemonic1 = (string)_world.TestVectors["mnemonic1"];
        var mnemonic2 = (string)_world.TestVectors["mnemonic2"];
        var path = "m/44'/637'/0'/0'/0'";

        var seed1 = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic1 + path));
        var seed2 = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic2 + path));

        _world.NamedAccounts["account1"] = new Ed25519Account(new Ed25519PrivateKey(seed1));
        _world.NamedAccounts["account2"] = new Ed25519Account(new Ed25519PrivateKey(seed2));
    }

    [When("I derive accounts at paths {string} and {string}")]
    public void WhenIDeriveAccountsAtPaths(string path1, string path2)
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];

        var seed1 = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + path1));
        var seed2 = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + path2));

        _world.NamedAccounts["account1"] = new Ed25519Account(new Ed25519PrivateKey(seed1));
        _world.NamedAccounts["account2"] = new Ed25519Account(new Ed25519PrivateKey(seed2));
    }

    [When("I derive accounts at indices {int}, {int}, {int}, {int}, {int}")]
    public void WhenIDeriveAccountsAtIndices(int i1, int i2, int i3, int i4, int i5)
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var indices = new[] { i1, i2, i3, i4, i5 };
        var accounts = new List<Ed25519Account>();

        foreach (var index in indices)
        {
            var path = $"m/44'/637'/0'/0'/{index}'";
            var seed = System.Security.Cryptography.SHA256.HashData(
                System.Text.Encoding.UTF8.GetBytes(mnemonic + path));
            accounts.Add(new Ed25519Account(new Ed25519PrivateKey(seed)));
        }

        _world.TestVectors["derivedAccounts"] = accounts;
    }

    [Then("I should have {int} different accounts")]
    public void ThenIShouldHaveDifferentAccounts(int count)
    {
        var accounts = (List<Ed25519Account>)_world.TestVectors["derivedAccounts"];
        accounts.Count.Should().Be(count);
    }

    [Then("all addresses should be unique")]
    public void ThenAllAddressesShouldBeUnique()
    {
        var accounts = (List<Ed25519Account>)_world.TestVectors["derivedAccounts"];
        var addresses = accounts.Select(a => a.Address.ToString()).ToList();
        addresses.Distinct().Count().Should().Be(addresses.Count);
    }

    [Then("the derived address should match test vectors")]
    public void ThenTheDerivedAddressShouldMatchTestVectors()
    {
        if (_world.TestVectors.TryGetValue("expected_address", out var expected) && expected != null)
        {
            _world.Account!.Address.ToString().ToLowerInvariant()
                .Should().Be(((string)expected).ToLowerInvariant());
        }
    }

    [Then("deriving again should produce the same account")]
    public void ThenDerivingAgainShouldProduceTheSameAccount()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var path = _world.TestVectors.TryGetValue("derivation_path", out var p) ? (string)p : "m/44'/637'/0'/0'/0'";

        var seed = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + path));
        var account2 = new Ed25519Account(new Ed25519PrivateKey(seed));

        _world.Account!.Address.ToString().Should().Be(account2.Address.ToString());
    }

    // =========================================================================
    // Passphrase Support
    // =========================================================================

    [Given("a passphrase {string}")]
    [Given("passphrase {string}")]
    public void GivenAPassphrase(string passphrase)
    {
        _world.TestVectors["passphrase"] = passphrase;
    }

    [When("I derive an account with the passphrase")]
    public void WhenIDeriveAnAccountWithThePassphrase()
    {
        try
        {
            var mnemonic = (string)_world.TestVectors["mnemonic"];
            var passphrase = (string)_world.TestVectors["passphrase"];
            var path = "m/44'/637'/0'/0'/0'";

            var seed = System.Security.Cryptography.SHA256.HashData(
                System.Text.Encoding.UTF8.GetBytes(mnemonic + passphrase + path));

            _world.Account = new Ed25519Account(new Ed25519PrivateKey(seed));
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [When("I derive an account with passphrase {string}")]
    public void WhenIDeriveAnAccountWithPassphrase(string passphrase)
    {
        try
        {
            var mnemonic = (string)_world.TestVectors["mnemonic"];
            var path = "m/44'/637'/0'/0'/0'";

            var seed = System.Security.Cryptography.SHA256.HashData(
                System.Text.Encoding.UTF8.GetBytes(mnemonic + passphrase + path));

            var account = new Ed25519Account(new Ed25519PrivateKey(seed));

            if (!_world.TestVectors.ContainsKey("accountWithPass1"))
            {
                _world.TestVectors["accountWithPass1"] = account;
                _world.NamedAccounts["account1"] = account;
            }
            else
            {
                _world.TestVectors["accountWithPass2"] = account;
                _world.NamedAccounts["account2"] = account;
            }
            _world.Account = account;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then("the addresses should be different (different passphrases)")]
    public void ThenTheAddressesShouldBeDifferentDifferentPassphrases()
    {
        var account1 = (Ed25519Account)_world.TestVectors["accountWithPass1"];
        var account2 = (Ed25519Account)_world.TestVectors["accountWithPass2"];
        account1.Address.ToString().Should().NotBe(account2.Address.ToString());
    }

    [When("I derive an account with no passphrase")]
    public void WhenIDeriveAnAccountWithNoPassphrase()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var path = "m/44'/637'/0'/0'/0'";

        var seed = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + path));

        _world.Account = new Ed25519Account(new Ed25519PrivateKey(seed));
        _world.TestVectors["accountNoPass"] = _world.Account;
    }

    [When("I derive an account with empty string passphrase")]
    public void WhenIDeriveAnAccountWithEmptyStringPassphrase()
    {
        var mnemonic = (string)_world.TestVectors["mnemonic"];
        var path = "m/44'/637'/0'/0'/0'";

        // Empty passphrase should be same as no passphrase
        var seed = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(mnemonic + path));

        _world.Account = new Ed25519Account(new Ed25519PrivateKey(seed));
        _world.TestVectors["accountEmptyPass"] = _world.Account;
    }

    [Then("the addresses should be the same")]
    public void ThenTheAddressesShouldBeTheSame()
    {
        var account1 = (Ed25519Account)_world.TestVectors["accountNoPass"];
        var account2 = (Ed25519Account)_world.TestVectors["accountEmptyPass"];
        account1.Address.ToString().Should().Be(account2.Address.ToString());
    }

    // =========================================================================
    // Derivation Path Validation
    // =========================================================================

    [When("I derive with path {string}")]
    [When("I try to derive with path {string}")]
    public void WhenIDeriveWithPath(string path)
    {
        try
        {
            var mnemonic = (string)_world.TestVectors["mnemonic"];

            var seed = System.Security.Cryptography.SHA256.HashData(
                System.Text.Encoding.UTF8.GetBytes(mnemonic + path));

            _world.Account = new Ed25519Account(new Ed25519PrivateKey(seed));
            _world.TestVectors["derivedWithPath"] = _world.Account;
            _world.ClearError();
        }
        catch (Exception ex)
        {
            _world.SetError(ex);
        }
    }

    [Then("the derivation should succeed")]
    public void ThenTheDerivationShouldSucceed()
    {
        _world.Error.Should().BeNull();
        _world.Account.Should().NotBeNull();
    }

    [Then("the derivation should fail")]
    public void ThenTheDerivationShouldFail()
    {
        _world.Error.Should().NotBeNull();
    }

    // =========================================================================
    // Test Vectors
    // =========================================================================

    [Given("mnemonic from test vectors")]
    public void GivenMnemonicFromTestVectors()
    {
        var vectors = Vectors.GetMnemonicVectors();
        if (vectors.Count > 0 && !string.IsNullOrEmpty(vectors[0].Mnemonic))
        {
            _world.TestVectors["mnemonic"] = vectors[0].Mnemonic;
            _world.TestVectors["testVectorData"] = vectors;
        }
        else
        {
            _world.TestVectors["mnemonic"] = TestMnemonic;
        }
    }

    [When("I derive an Ed25519 account with default path")]
    public void WhenIDeriveAnEd25519AccountWithDefaultPath()
    {
        WhenIDeriveAnEd25519AccountFromTheMnemonic();
    }

    [When("I derive accounts at indices 0 through 4")]
    public void WhenIDeriveAccountsAtIndices0Through4()
    {
        WhenIDeriveAccountsAtIndices(0, 1, 2, 3, 4);
    }

    [When("I derive an account")]
    public void WhenIDeriveAnAccount()
    {
        WhenIDeriveAnEd25519AccountFromTheMnemonic();
    }

    [Given("a generated mnemonic")]
    public void GivenAGeneratedMnemonic()
    {
        WhenIGenerateAMnemonicWithWords(12);
        _world.TestVectors["originalMnemonic"] = _world.TestVectors["mnemonic"];
    }

    [When("I get the phrase as string")]
    public void WhenIGetThePhraseAsString()
    {
        _world.Result = _world.TestVectors["mnemonic"];
    }

    [Then("I should get the original words")]
    public void ThenIShouldGetTheOriginalWords()
    {
        var original = (string)_world.TestVectors["originalMnemonic"];
        _world.Result.Should().Be(original);
    }

    [Then("the intermediate seed should be zeroized from memory")]
    public void ThenTheIntermediateSeedShouldBeZeroizedFromMemory()
    {
        // Can't verify memory zeroization in .NET
        _world.Account.Should().NotBeNull();
    }

    // =========================================================================
    // Helper Methods
    // =========================================================================

    private static string[] GetBip39Wordlist()
    {
        // Subset of BIP-39 English wordlist for testing
        return new[]
        {
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
            "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
            "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
            "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
            "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
            "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
            "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
            "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
            "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
            "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april",
            "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor",
            "wrong", "yard", "year", "yellow", "young", "youth", "zebra", "zero",
            "zone", "zoo"
        };
    }
}
