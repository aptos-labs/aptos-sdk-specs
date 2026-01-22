/**
 * Keyless Accounts (OIDC Authentication) Step Definitions
 *
 * Keyless accounts are NOT currently supported by the Aptos .NET SDK.
 * These steps throw NotImplementedException to clearly indicate missing functionality.
 */
using Reqnroll;
using FluentAssertions;
using Aptos;
using Aptos.Specs.Support;

namespace Aptos.Specs.StepDefinitions;

[Binding]
public class KeylessSteps
{
    private readonly TestWorld _world;

    public KeylessSteps(TestWorld world)
    {
        _world = world;
    }

    // =========================================================================
    // Ephemeral Key Pair - NOT IMPLEMENTED
    // =========================================================================

    [When("I generate an ephemeral key pair with {int} second expiry")]
    public void WhenIGenerateAnEphemeralKeyPairWithSecondExpiry(int expirySeconds)
    {
        throw new NotImplementedException("Keyless accounts (ephemeral key pairs) are not supported by the Aptos .NET SDK");
    }

    [Then("the ephemeral key pair should be valid")]
    public void ThenTheEphemeralKeyPairShouldBeValid()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the ephemeral key pair should have an expiry date")]
    public void ThenTheEphemeralKeyPairShouldHaveAnExpiryDate()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the ephemeral key pair should have a nonce")]
    public void ThenTheEphemeralKeyPairShouldHaveANonce()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I check is_expired")]
    public void WhenICheckIsExpired()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I check is_valid")]
    public void WhenICheckIsValid()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I generate an expired ephemeral key pair")]
    public void WhenIGenerateAnExpiredEphemeralKeyPair()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("checking is_expired should return true")]
    public void ThenCheckingIsExpiredShouldReturnTrue()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // JWT/OIDC - NOT IMPLEMENTED
    // =========================================================================

    [Given("a valid JWT from Google with sub {string}")]
    public void GivenAValidJWTFromGoogleWithSub(string sub)
    {
        throw new NotImplementedException("Keyless accounts (JWT/OIDC) are not supported by the Aptos .NET SDK");
    }

    [Given("a valid JWT from Apple with sub {string}")]
    public void GivenAValidJWTFromAppleWithSub(string sub)
    {
        throw new NotImplementedException("Keyless accounts (JWT/OIDC) are not supported by the Aptos .NET SDK");
    }

    [Given("a valid JWT with nonce matching the ephemeral key pair")]
    public void GivenAValidJWTWithNonceMatchingTheEphemeralKeyPair()
    {
        throw new NotImplementedException("Keyless accounts (JWT/OIDC) are not supported by the Aptos .NET SDK");
    }

    [Given("a malformed JWT")]
    public void GivenAMalformedJWT()
    {
        throw new NotImplementedException("Keyless accounts (JWT/OIDC) are not supported by the Aptos .NET SDK");
    }

    [Given("a JWT with mismatched nonce")]
    public void GivenAJWTWithMismatchedNonce()
    {
        throw new NotImplementedException("Keyless accounts (JWT/OIDC) are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Pepper Service - NOT IMPLEMENTED
    // =========================================================================

    [Given("a pepper service response")]
    public void GivenAPepperServiceResponse()
    {
        throw new NotImplementedException("Keyless accounts (pepper service) are not supported by the Aptos .NET SDK");
    }

    [Given("a fetched pepper for the JWT")]
    public void GivenAFetchedPepperForTheJWT()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I fetch a pepper from the pepper service")]
    public void WhenIFetchAPepperFromThePepperService()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("I should receive a valid pepper")]
    public void ThenIShouldReceiveAValidPepper()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the pepper should be deterministic for the same JWT")]
    public void ThenThePepperShouldBeDeterministicForTheSameJWT()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Keyless Account Creation - NOT IMPLEMENTED
    // =========================================================================

    [When("I create a keyless account")]
    public void WhenICreateAKeylessAccount()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the keyless account should have a valid address")]
    public void ThenTheKeylessAccountShouldHaveAValidAddress()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the address should be derivable from the JWT claims and pepper")]
    public void ThenTheAddressShouldBeDerivableFromTheJWTClaimsAndPepper()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Given("the same JWT and pepper")]
    public void GivenTheSameJWTAndPepper()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I derive the address again")]
    public void WhenIDeriveTheAddressAgain()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should match the original address")]
    public void ThenItShouldMatchTheOriginalAddress()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Keyless Signing - NOT IMPLEMENTED
    // =========================================================================

    [Given("a valid ZK proof for the keyless account")]
    public void GivenAValidZKProofForTheKeylessAccount()
    {
        throw new NotImplementedException("Keyless accounts (ZK proofs) are not supported by the Aptos .NET SDK");
    }

    [When("I call sign with message")]
    public void WhenICallSignWithMessage()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I call address")]
    public void WhenICallAddress()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the signature should include the ZK proof")]
    public void ThenTheSignatureShouldIncludeTheZKProof()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the signature should include the ephemeral signature")]
    public void ThenTheSignatureShouldIncludeTheEphemeralSignature()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the signature should be verifiable on-chain")]
    public void ThenTheSignatureShouldBeVerifiableOnChain()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Prover Service - NOT IMPLEMENTED
    // =========================================================================

    [When("I submit a proof request to the prover")]
    public void WhenISubmitAProofRequestToTheProver()
    {
        throw new NotImplementedException("Keyless accounts (prover service) are not supported by the Aptos .NET SDK");
    }

    [Then("I should receive a valid ZK proof")]
    public void ThenIShouldReceiveAValidZKProof()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("the proof should be valid for a limited time")]
    public void ThenTheProofShouldBeValidForALimitedTime()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Given("an expired ZK proof")]
    public void GivenAnExpiredZKProof()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I try to sign with the expired proof")]
    public void WhenITryToSignWithTheExpiredProof()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should require refreshing the proof")]
    public void ThenItShouldRequireRefreshingTheProof()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Error Scenarios - NOT IMPLEMENTED
    // =========================================================================

    [When("I try to create a keyless account with the malformed JWT")]
    public void WhenITryToCreateAKeylessAccountWithTheMalformedJWT()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should fail with a JWT parsing error")]
    public void ThenItShouldFailWithAJWTParsingError()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I try to create a keyless account")]
    public void WhenITryToCreateAKeylessAccount()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should fail with a nonce mismatch error")]
    public void ThenItShouldFailWithANonceMismatchError()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I try to sign with the expired ephemeral key")]
    public void WhenITryToSignWithTheExpiredEphemeralKey()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should fail with an ephemeral key expired error")]
    public void ThenItShouldFailWithAnEphemeralKeyExpiredError()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    // =========================================================================
    // Security Properties - NOT IMPLEMENTED
    // =========================================================================

    [Given("a keyless account")]
    public void GivenAKeylessAccount()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [When("I try to access the pepper")]
    public void WhenITryToAccessThePepper()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should not be directly accessible")]
    public void ThenItShouldNotBeDirectlyAccessible()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Given("an ephemeral private key")]
    public void GivenAnEphemeralPrivateKey()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("it should not allow deriving the main account key")]
    public void ThenItShouldNotAllowDerivingTheMainAccountKey()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }

    [Then("without the ZK proof it should be unusable")]
    public void ThenWithoutTheZKProofItShouldBeUnusable()
    {
        throw new NotImplementedException("Keyless accounts are not supported by the Aptos .NET SDK");
    }
}
