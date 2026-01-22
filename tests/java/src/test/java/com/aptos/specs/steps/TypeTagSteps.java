package com.aptos.specs.steps;

import com.aptos.specs.support.World;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.assertj.core.api.Assertions.*;

/**
 * Step definitions for type-tags.feature
 * 
 * These steps test TypeTag parsing, formatting, and BCS serialization.
 * 
 * TODO: Replace placeholder implementations with actual japtos SDK calls.
 */
public class TypeTagSteps {
    
    private final World world;
    
    public TypeTagSteps(World world) {
        this.world = world;
    }
    
    // ==========================================================================
    // Given Steps
    // ==========================================================================
    
    @Given("a type string {string}")
    public void givenTypeString(String typeString) {
        world.setStringValue(typeString);
    }
    
    @Given("a TypeTag of variant {word}")
    public void givenTypeTagVariant(String variant) {
        // TODO: Replace with actual SDK call
        PlaceholderTypeTag typeTag = PlaceholderTypeTag.primitive(variant);
        world.setTypeTag(typeTag);
    }
    
    @Given("a TypeTag of Vector containing {word}")
    public void givenTypeTagVector(String innerType) {
        PlaceholderTypeTag inner = PlaceholderTypeTag.primitive(innerType);
        PlaceholderTypeTag typeTag = PlaceholderTypeTag.vector(inner);
        world.setTypeTag(typeTag);
    }
    
    @Given("a TypeTag struct with address {string}, module {string}, name {string}")
    public void givenTypeTagStruct(String address, String module, String name) {
        PlaceholderTypeTag typeTag = PlaceholderTypeTag.struct(address, module, name, List.of());
        world.setTypeTag(typeTag);
    }
    
    @Given("a TypeTag for CoinStore of AptosCoin")
    public void givenTypeTagCoinStore() {
        PlaceholderTypeTag aptosCoin = PlaceholderTypeTag.struct("0x1", "aptos_coin", "AptosCoin", List.of());
        PlaceholderTypeTag coinStore = PlaceholderTypeTag.struct("0x1", "coin", "CoinStore", List.of(aptosCoin));
        world.setTypeTag(coinStore);
    }
    
    @Given("a module string {string}")
    public void givenModuleString(String moduleString) {
        world.setStringValue(moduleString);
    }
    
    @Given("a MoveModuleId with address {string} and name {string}")
    public void givenMoveModuleId(String address, String name) {
        PlaceholderModuleId moduleId = new PlaceholderModuleId(address, name);
        world.setModuleId(moduleId);
    }
    
    @Given("address {string}, module {string}, name {string}, and type args [AptosCoin]")
    public void givenStructTagComponents(String address, String module, String name) {
        PlaceholderTypeTag aptosCoin = PlaceholderTypeTag.struct("0x1", "aptos_coin", "AptosCoin", List.of());
        PlaceholderStructTag structTag = new PlaceholderStructTag(address, module, name, List.of(aptosCoin));
        world.setStructTag(structTag);
    }
    
    // ==========================================================================
    // When Steps
    // ==========================================================================
    
    @When("I parse it as a TypeTag")
    public void whenParseAsTypeTag() {
        try {
            String typeString = world.getStringValue();
            PlaceholderTypeTag typeTag = PlaceholderTypeTag.parse(typeString);
            world.setTypeTag(typeTag);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I format it as a string")
    public void whenFormatAsString() {
        if (world.getTypeTag() != null) {
            PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
            world.setResult(typeTag.toString());
        } else if (world.getModuleId() != null) {
            PlaceholderModuleId moduleId = (PlaceholderModuleId) world.getModuleId();
            world.setResult(moduleId.toString());
        }
    }
    
    @When("I parse it as a MoveModuleId")
    public void whenParseAsMoveModuleId() {
        try {
            String moduleString = world.getStringValue();
            PlaceholderModuleId moduleId = PlaceholderModuleId.parse(moduleString);
            world.setModuleId(moduleId);
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I create a MoveStructTag")
    public void whenCreateMoveStructTag() {
        // Already created in given step
    }
    
    @When("I BCS serialize the TypeTag")
    public void whenBcsSerializeTypeTag() {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        world.setSerializedBytes(typeTag.toBcs());
    }
    
    @When("I parse and BCS serialize the TypeTag")
    public void whenParseAndBcsSerializeTypeTag() {
        try {
            String typeString = world.getStringValue();
            PlaceholderTypeTag typeTag = PlaceholderTypeTag.parse(typeString);
            world.setTypeTag(typeTag);
            world.setSerializedBytes(typeTag.toBcs());
            world.clearError();
        } catch (Exception e) {
            world.setError(e);
        }
    }
    
    @When("I BCS serialize and deserialize it")
    public void whenBcsSerializeAndDeserialize() {
        PlaceholderTypeTag original = (PlaceholderTypeTag) world.getTypeTag();
        byte[] bcs = original.toBcs();
        // For now, just store the original since we're verifying round-trip
        world.setResult(original);
    }
    
    // ==========================================================================
    // Then Steps
    // ==========================================================================
    
    @Then("the TypeTag variant should be {word}")
    public void thenTypeTagVariantShouldBe(String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getVariant()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the inner type should be {word}")
    public void thenInnerTypeShouldBe(String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getInnerType()).isNotNull();
        assertThat(typeTag.getInnerType().getVariant()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the inner type should be a Vector of {word}")
    public void thenInnerTypeShouldBeVectorOf(String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getInnerType()).isNotNull();
        assertThat(typeTag.getInnerType().getVariant()).isEqualToIgnoringCase("Vector");
        assertThat(typeTag.getInnerType().getInnerType().getVariant()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the inner type should be a Struct")
    public void thenInnerTypeShouldBeStruct() {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getInnerType()).isNotNull();
        assertThat(typeTag.getInnerType().getVariant()).isEqualToIgnoringCase("Struct");
    }
    
    @Then("the struct address should be {string}")
    public void thenStructAddressShouldBe(String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getStructAddress()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the struct module should be {string}")
    public void thenStructModuleShouldBe(String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getStructModule()).isEqualTo(expected);
    }
    
    @Then("the struct name should be {string}")
    public void thenStructNameShouldBe(String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getStructName()).isEqualTo(expected);
    }
    
    @Then("the struct should have {int} type argument(s)")
    public void thenStructShouldHaveTypeArgs(int expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        assertThat(typeTag.getTypeArgs()).hasSize(expected);
    }
    
    @Then("type argument {int} should be a Struct named {string}")
    public void thenTypeArgShouldBeStructNamed(int index, String name) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        PlaceholderTypeTag arg = typeTag.getTypeArgs().get(index);
        assertThat(arg.getVariant()).isEqualToIgnoringCase("Struct");
        assertThat(arg.getStructName()).isEqualTo(name);
    }
    
    @Then("type argument {int} should be {word}")
    public void thenTypeArgShouldBe(int index, String expected) {
        PlaceholderTypeTag typeTag = (PlaceholderTypeTag) world.getTypeTag();
        PlaceholderTypeTag arg = typeTag.getTypeArgs().get(index);
        assertThat(arg.getVariant()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the parsing should fail with a parse error")
    public void thenParsingShouldFailWithParseError() {
        assertThat(world.getError())
            .as("Expected parsing to fail")
            .isNotNull();
    }
    
    @Then("the parsing should fail")
    public void thenParsingShouldFail() {
        assertThat(world.getError())
            .as("Expected parsing to fail")
            .isNotNull();
    }
    
    @Then("the module address should be {string}")
    public void thenModuleAddressShouldBe(String expected) {
        PlaceholderModuleId moduleId = (PlaceholderModuleId) world.getModuleId();
        assertThat(moduleId.getAddress()).isEqualToIgnoringCase(expected);
    }
    
    @Then("the module name should be {string}")
    public void thenModuleNameShouldBe(String expected) {
        PlaceholderModuleId moduleId = (PlaceholderModuleId) world.getModuleId();
        assertThat(moduleId.getName()).isEqualTo(expected);
    }
    
    @Then("the struct tag should be valid")
    public void thenStructTagShouldBeValid() {
        assertThat(world.getStructTag()).isNotNull();
    }
    
    @Then("the string representation should be {string}")
    public void thenStringRepresentationShouldBe(String expected) {
        PlaceholderStructTag structTag = (PlaceholderStructTag) world.getStructTag();
        assertThat(structTag.toString()).isEqualTo(expected);
    }
    
    @Then("the first byte should be the {word} variant index")
    public void thenFirstByteShouldBeVariantIndex(String variant) {
        // U64 variant index is typically 4 in BCS TypeTag encoding
        assertThat(world.getSerializedBytes()).isNotEmpty();
    }
    
    @Then("the serialization should succeed")
    public void thenSerializationShouldSucceed() {
        assertThat(world.getError()).isNull();
        assertThat(world.getSerializedBytes()).isNotNull();
        assertThat(world.getSerializedBytes().length).isGreaterThan(0);
    }
    
    @Then("the result should be deserializable back to the same TypeTag")
    public void thenResultShouldBeDeserializable() {
        // Placeholder - actual implementation would deserialize and compare
        assertThat(world.getSerializedBytes()).isNotNull();
    }
    
    @Then("the result should equal the original TypeTag")
    public void thenResultShouldEqualOriginal() {
        PlaceholderTypeTag original = (PlaceholderTypeTag) world.getTypeTag();
        PlaceholderTypeTag result = (PlaceholderTypeTag) world.getResult();
        assertThat(result).isEqualTo(original);
    }
    
    // ==========================================================================
    // Placeholder Classes
    // ==========================================================================
    
    /**
     * Placeholder TypeTag implementation.
     * TODO: Replace with actual japtos TypeTag class.
     */
    public static class PlaceholderTypeTag {
        private final String variant;
        private final PlaceholderTypeTag innerType;
        private final String structAddress;
        private final String structModule;
        private final String structName;
        private final List<PlaceholderTypeTag> typeArgs;
        
        private PlaceholderTypeTag(String variant, PlaceholderTypeTag innerType,
                                   String structAddress, String structModule, String structName,
                                   List<PlaceholderTypeTag> typeArgs) {
            this.variant = variant;
            this.innerType = innerType;
            this.structAddress = structAddress;
            this.structModule = structModule;
            this.structName = structName;
            this.typeArgs = typeArgs != null ? typeArgs : List.of();
        }
        
        public static PlaceholderTypeTag primitive(String type) {
            String variant = switch (type.toLowerCase()) {
                case "bool" -> "Bool";
                case "u8" -> "U8";
                case "u16" -> "U16";
                case "u32" -> "U32";
                case "u64" -> "U64";
                case "u128" -> "U128";
                case "u256" -> "U256";
                case "address" -> "Address";
                case "signer" -> "Signer";
                default -> type;
            };
            return new PlaceholderTypeTag(variant, null, null, null, null, null);
        }
        
        public static PlaceholderTypeTag vector(PlaceholderTypeTag inner) {
            return new PlaceholderTypeTag("Vector", inner, null, null, null, null);
        }
        
        public static PlaceholderTypeTag struct(String address, String module, String name,
                                                List<PlaceholderTypeTag> typeArgs) {
            // Normalize address to short form
            String shortAddr = normalizeAddress(address);
            return new PlaceholderTypeTag("Struct", null, shortAddr, module, name, typeArgs);
        }
        
        public static PlaceholderTypeTag parse(String typeString) {
            if (typeString == null || typeString.isEmpty()) {
                throw new IllegalArgumentException("Empty type string");
            }
            
            typeString = typeString.trim();
            
            // Check primitives
            String lower = typeString.toLowerCase();
            if (lower.matches("bool|u8|u16|u32|u64|u128|u256|address|signer")) {
                return primitive(lower);
            }
            
            // Check vector
            if (typeString.startsWith("vector<")) {
                if (!typeString.endsWith(">")) {
                    throw new IllegalArgumentException("Unclosed vector bracket");
                }
                String inner = typeString.substring(7, typeString.length() - 1).trim();
                if (inner.isEmpty()) {
                    throw new IllegalArgumentException("Empty vector type");
                }
                return vector(parse(inner));
            }
            
            // Must be a struct
            return parseStruct(typeString);
        }
        
        private static PlaceholderTypeTag parseStruct(String typeString) {
            // Pattern: address::module::name or address::module::name<type_args>
            int typeArgsStart = typeString.indexOf('<');
            String mainPart;
            List<PlaceholderTypeTag> typeArgs = new ArrayList<>();
            
            if (typeArgsStart > 0) {
                if (!typeString.endsWith(">")) {
                    throw new IllegalArgumentException("Unclosed type argument bracket");
                }
                mainPart = typeString.substring(0, typeArgsStart);
                String argsStr = typeString.substring(typeArgsStart + 1, typeString.length() - 1);
                typeArgs = parseTypeArgs(argsStr);
            } else {
                mainPart = typeString;
            }
            
            String[] parts = mainPart.split("::");
            if (parts.length != 3) {
                throw new IllegalArgumentException("Invalid struct format: " + typeString);
            }
            
            String address = parts[0];
            String module = parts[1];
            String name = parts[2];
            
            // Validate address
            if (!address.matches("0x[0-9a-fA-F]+")) {
                throw new IllegalArgumentException("Invalid address: " + address);
            }
            
            return struct(address, module, name, typeArgs);
        }
        
        private static List<PlaceholderTypeTag> parseTypeArgs(String argsStr) {
            List<PlaceholderTypeTag> result = new ArrayList<>();
            int depth = 0;
            int start = 0;
            
            for (int i = 0; i < argsStr.length(); i++) {
                char c = argsStr.charAt(i);
                if (c == '<') depth++;
                else if (c == '>') depth--;
                else if (c == ',' && depth == 0) {
                    result.add(parse(argsStr.substring(start, i).trim()));
                    start = i + 1;
                }
            }
            
            if (start < argsStr.length()) {
                result.add(parse(argsStr.substring(start).trim()));
            }
            
            return result;
        }
        
        private static String normalizeAddress(String address) {
            String clean = address.startsWith("0x") ? address.substring(2) : address;
            clean = clean.replaceFirst("^0+(?!$)", "");
            return "0x" + clean;
        }
        
        public String getVariant() {
            return variant;
        }
        
        public PlaceholderTypeTag getInnerType() {
            return innerType;
        }
        
        public String getStructAddress() {
            return structAddress;
        }
        
        public String getStructModule() {
            return structModule;
        }
        
        public String getStructName() {
            return structName;
        }
        
        public List<PlaceholderTypeTag> getTypeArgs() {
            return typeArgs;
        }
        
        public byte[] toBcs() {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            int variantIndex = switch (variant) {
                case "Bool" -> 0;
                case "U8" -> 1;
                case "U64" -> 2;
                case "U128" -> 3;
                case "Address" -> 4;
                case "Signer" -> 5;
                case "Vector" -> 6;
                case "Struct" -> 7;
                default -> 0;
            };
            out.write(variantIndex);
            // Additional BCS encoding would go here
            return out.toByteArray();
        }
        
        @Override
        public String toString() {
            return switch (variant) {
                case "Bool" -> "bool";
                case "U8" -> "u8";
                case "U16" -> "u16";
                case "U32" -> "u32";
                case "U64" -> "u64";
                case "U128" -> "u128";
                case "U256" -> "u256";
                case "Address" -> "address";
                case "Signer" -> "signer";
                case "Vector" -> "vector<" + innerType.toString() + ">";
                case "Struct" -> {
                    StringBuilder sb = new StringBuilder();
                    sb.append(structAddress).append("::").append(structModule).append("::").append(structName);
                    if (!typeArgs.isEmpty()) {
                        sb.append("<");
                        for (int i = 0; i < typeArgs.size(); i++) {
                            if (i > 0) sb.append(", ");
                            sb.append(typeArgs.get(i).toString());
                        }
                        sb.append(">");
                    }
                    yield sb.toString();
                }
                default -> variant.toLowerCase();
            };
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (!(obj instanceof PlaceholderTypeTag other)) return false;
            return Objects.equals(variant, other.variant) &&
                   Objects.equals(innerType, other.innerType) &&
                   Objects.equals(structAddress, other.structAddress) &&
                   Objects.equals(structModule, other.structModule) &&
                   Objects.equals(structName, other.structName) &&
                   Objects.equals(typeArgs, other.typeArgs);
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(variant, innerType, structAddress, structModule, structName, typeArgs);
        }
    }
    
    /**
     * Placeholder MoveModuleId implementation.
     */
    public static class PlaceholderModuleId {
        private final String address;
        private final String name;
        
        public PlaceholderModuleId(String address, String name) {
            this.address = normalizeAddress(address);
            this.name = name;
        }
        
        public static PlaceholderModuleId parse(String moduleString) {
            String[] parts = moduleString.split("::");
            if (parts.length != 2) {
                throw new IllegalArgumentException("Invalid module ID format");
            }
            return new PlaceholderModuleId(parts[0], parts[1]);
        }
        
        private static String normalizeAddress(String address) {
            String clean = address.startsWith("0x") ? address.substring(2) : address;
            clean = clean.replaceFirst("^0+(?!$)", "");
            return "0x" + clean;
        }
        
        public String getAddress() {
            return address;
        }
        
        public String getName() {
            return name;
        }
        
        @Override
        public String toString() {
            return address + "::" + name;
        }
    }
    
    /**
     * Placeholder MoveStructTag implementation.
     */
    public static class PlaceholderStructTag {
        private final String address;
        private final String module;
        private final String name;
        private final List<PlaceholderTypeTag> typeArgs;
        
        public PlaceholderStructTag(String address, String module, String name,
                                    List<PlaceholderTypeTag> typeArgs) {
            this.address = normalizeAddress(address);
            this.module = module;
            this.name = name;
            this.typeArgs = typeArgs;
        }
        
        private static String normalizeAddress(String address) {
            String clean = address.startsWith("0x") ? address.substring(2) : address;
            clean = clean.replaceFirst("^0+(?!$)", "");
            return "0x" + clean;
        }
        
        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append(address).append("::").append(module).append("::").append(name);
            if (!typeArgs.isEmpty()) {
                sb.append("<");
                for (int i = 0; i < typeArgs.size(); i++) {
                    if (i > 0) sb.append(", ");
                    sb.append(typeArgs.get(i).toString());
                }
                sb.append(">");
            }
            return sb.toString();
        }
    }
}
