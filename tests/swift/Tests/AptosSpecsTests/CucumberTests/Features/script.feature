@transaction
@optional
Feature: Script Transactions
  As an SDK user
  I want to execute arbitrary Move scripts
  So that I can run custom logic without deploying modules

  # =============================================================================
  # Script Payload Construction
  # =============================================================================
  @optional
  Scenario: Create script payload from bytecode
    Given compiled Move script bytecode
    When I create a Script payload
    Then I should have a valid TransactionPayload::Script

  @optional
  Scenario: Script with no arguments
    Given a compiled script with no parameters
    When I create the script payload
    Then arguments should be empty
    And type arguments should be empty

  @optional
  Scenario: Script with type arguments
    Given a compiled generic script
    When I provide type arguments [0x1::aptos_coin::AptosCoin]
    And create the script payload
    Then the type arguments should be included

  @optional
  Scenario: Script with multiple arguments
    Given a script expecting (address, u64, vector<u8>)
    When I provide the arguments
    And create the script payload
    Then all arguments should be BCS encoded

  # =============================================================================
  # Script Argument Encoding
  # =============================================================================
  @optional
  Scenario: Encode address argument for script
    Given a script argument of type address
    When I encode the value "0x1"
    Then the encoded bytes should be the BCS-serialized address

  @optional
  Scenario: Encode u64 argument for script
    Given a script argument of type u64
    When I encode the value 1000000
    Then the encoded bytes should be "40420f0000000000"

  @optional
  Scenario: Encode vector<u8> argument for script
    Given a script argument of type vector<u8>
    When I encode the value [1, 2, 3]
    Then the encoded bytes should be "03010203"

  @optional
  Scenario: Encode bool argument for script
    Given a script argument of type bool
    When I encode true
    Then the encoded bytes should be "01"

  @optional
  Scenario: Encode string argument for script
    Given a script argument of type string
    When I encode "hello"
    Then the encoded bytes should be "0568656c6c6f"

  # =============================================================================
  # Script Transaction Building
  # =============================================================================
  @optional
  Scenario: Build transaction with script payload
    Given a Script payload
    And transaction parameters (sender, seq num, gas, etc.)
    When I build the RawTransaction
    Then the payload type should be Script

  @optional
  Scenario: Sign script transaction
    Given a RawTransaction with Script payload
    And a signing account
    When I sign the transaction
    Then I should get a valid SignedTransaction

  @optional
  Scenario: Submit script transaction
    Given a SignedTransaction with Script payload
    And a connected Aptos client
    When I submit the script transaction
    Then it should be submitted successfully
    And return a transaction hash

  # =============================================================================
  # Script Simulation
  # =============================================================================
  @optional
  Scenario: Simulate script execution
    Given a Script transaction
    When I simulate the script transaction
    Then I should see execution result
    And gas usage estimate

  @optional
  Scenario: Simulate script with invalid arguments
    Given a Script with wrong argument types
    When I simulate the script transaction
    Then script simulation should fail
    And show type mismatch error

  # =============================================================================
  # Common Scripts
  # =============================================================================
  @optional
  Scenario: Execute multi-transfer script
    Given a script that transfers to multiple recipients
    And the compiled bytecode
    When I execute the script with recipient list
    Then all transfers should occur atomically

  @optional
  Scenario: Execute conditional logic script
    Given a script with conditional logic
    When I execute it
    Then the correct branch should execute

  # =============================================================================
  # Script vs Entry Function
  # =============================================================================
  @optional
  Scenario: Choose between script and entry function
    Given a simple operation like transfer
    Then entry function is preferred (simpler)
    Given complex multi-step logic
    Then script may be more appropriate

  @optional
  Scenario: Scripts can call any public function
    Given a module with public (non-entry) functions
    When I write a script that calls those functions
    Then the script can access them

  # =============================================================================
  # Script Compilation
  # =============================================================================
  @optional
  Scenario: Compile Move script (if SDK provides)
    Given Move script source code
    When I compile it
    Then I should get bytecode
    And be able to use it in Script payload

  @optional
  Scenario: Script bytecode format
    Given compiled script bytecode
    When I inspect it
    Then it should be valid Move bytecode
    And different from module bytecode format

  # =============================================================================
  # Error Handling
  # =============================================================================
  @optional
  Scenario: Invalid script bytecode
    Given malformed bytecode
    When I try to execute it
    Then execution should fail
    And error should indicate invalid bytecode

  @optional
  Scenario: Script aborts
    Given a script that calls abort
    When I execute it
    Then the script transaction should fail
    And show the abort code

  @optional
  Scenario: Script runs out of gas
    Given a script with expensive operations
    And low max_gas_amount
    When I execute it
    Then it should fail with out of gas error

  # =============================================================================
  # BCS Serialization
  # =============================================================================
  @optional
  Scenario: Script payload BCS structure
    Given a Script payload
    When I BCS serialize it
    Then structure should be:
      | Field     | Type               |
      | code      | vector<u8>         |
      | type_args | vector<TypeTag>    |
      | args      | vector<vector<u8>> |

  @optional
  Scenario: Deserialize Script payload
    Given BCS-serialized Script payload
    When I deserialize it
    Then I should recover the original Script
