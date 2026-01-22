package main

import (
	"fmt"
	"strings"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/cucumber/godog"
)

func initTypeTagSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Type String Setup
	// =============================================================================

	ctx.Step(`^a type string "([^"]*)"$`, func(typeStr string) error {
		world.TestVectors["typeString"] = typeStr
		return nil
	})

	ctx.Step(`^a TypeTag of variant U64$`, func() error {
		world.TestVectors["typeTag"] = &aptos.TypeTag{Value: &aptos.U64Tag{}}
		return nil
	})

	ctx.Step(`^a TypeTag of variant U8$`, func() error {
		world.TestVectors["typeTag"] = &aptos.TypeTag{Value: &aptos.U8Tag{}}
		return nil
	})

	ctx.Step(`^a TypeTag of Vector containing U8$`, func() error {
		inner := aptos.TypeTag{Value: &aptos.U8Tag{}}
		world.TestVectors["typeTag"] = &aptos.TypeTag{Value: &aptos.VectorTag{TypeParam: inner}}
		return nil
	})

	ctx.Step(`^a simple struct TypeTag "([^"]*)"$`, func(typeStr string) error {
		world.TestVectors["typeString"] = typeStr
		return nil
	})

	ctx.Step(`^a module string "([^"]*)"$`, func(moduleStr string) error {
		world.TestVectors["moduleString"] = moduleStr
		return nil
	})

	ctx.Step(`^a MoveModuleId with address "([^"]*)" and name "([^"]*)"$`, func(addrStr, name string) error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(addrStr)
		if err != nil {
			return err
		}
		world.TestVectors["moduleId"] = &aptos.ModuleId{
			Address: *addr,
			Name:    name,
		}
		return nil
	})

	// =============================================================================
	// When Steps - Parsing
	// =============================================================================

	ctx.Step(`^I parse it as a TypeTag$`, func() error {
		typeStr := world.TestVectors["typeString"].(string)
		tag, err := aptos.ParseTypeTag(typeStr)
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["typeTag"] = tag
		world.ClearError()
		return nil
	})

	ctx.Step(`^I format it as a string$`, func() error {
		// Check for moduleId first
		if moduleId, ok := world.TestVectors["moduleId"].(*aptos.ModuleId); ok {
			world.Result = moduleId.Address.StringShort() + "::" + moduleId.Name
			return nil
		}
		// Then check for typeTag
		if tag, ok := world.TestVectors["typeTag"].(*aptos.TypeTag); ok {
			world.Result = tag.String()
			return nil
		}
		return fmt.Errorf("no typeTag or moduleId set")
	})

	ctx.Step(`^I parse it as a MoveModuleId$`, func() error {
		moduleStr := world.TestVectors["moduleString"].(string)
		// Parse module ID format: "address::module"
		parts := strings.Split(moduleStr, "::")
		if len(parts) != 2 {
			world.SetError(fmt.Errorf("invalid module ID format: %s", moduleStr))
			return nil
		}
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(parts[0])
		if err != nil {
			world.SetError(err)
			return nil
		}
		world.TestVectors["moduleId"] = &aptos.ModuleId{
			Address: *addr,
			Name:    parts[1],
		}
		world.ClearError()
		return nil
	})

	// =============================================================================
	// Then Steps - Validation
	// =============================================================================

	ctx.Step(`^the parsing should succeed$`, func() error {
		if world.Error != nil {
			return fmt.Errorf("expected no error, got: %v", world.Error)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be Bool$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.BoolTag); !ok {
			return fmt.Errorf("expected Bool variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be U8$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.U8Tag); !ok {
			return fmt.Errorf("expected U8 variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be U16$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.U16Tag); !ok {
			return fmt.Errorf("expected U16 variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be U32$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.U32Tag); !ok {
			return fmt.Errorf("expected U32 variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be U64$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.U64Tag); !ok {
			return fmt.Errorf("expected U64 variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be U128$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.U128Tag); !ok {
			return fmt.Errorf("expected U128 variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be U256$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.U256Tag); !ok {
			return fmt.Errorf("expected U256 variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be Address$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.AddressTag); !ok {
			return fmt.Errorf("expected Address variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be Signer$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.SignerTag); !ok {
			return fmt.Errorf("expected Signer variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be Vector$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.VectorTag); !ok {
			return fmt.Errorf("expected Vector variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the TypeTag variant should be Struct$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.StructTag); !ok {
			return fmt.Errorf("expected Struct variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the inner type should be U8$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		vector, ok := tag.Value.(*aptos.VectorTag)
		if !ok {
			return fmt.Errorf("expected Vector variant, got %T", tag.Value)
		}
		if _, ok := vector.TypeParam.Value.(*aptos.U8Tag); !ok {
			return fmt.Errorf("expected inner type U8, got %T", vector.TypeParam.Value)
		}
		return nil
	})

	ctx.Step(`^the inner type should be a Vector of U8$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		vector, ok := tag.Value.(*aptos.VectorTag)
		if !ok {
			return fmt.Errorf("expected Vector variant, got %T", tag.Value)
		}
		inner, ok := vector.TypeParam.Value.(*aptos.VectorTag)
		if !ok {
			return fmt.Errorf("expected inner Vector, got %T", vector.TypeParam.Value)
		}
		if _, ok := inner.TypeParam.Value.(*aptos.U8Tag); !ok {
			return fmt.Errorf("expected inner inner type U8, got %T", inner.TypeParam.Value)
		}
		return nil
	})

	ctx.Step(`^the inner type should be a Struct$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		vector, ok := tag.Value.(*aptos.VectorTag)
		if !ok {
			return fmt.Errorf("expected Vector variant, got %T", tag.Value)
		}
		if _, ok := vector.TypeParam.Value.(*aptos.StructTag); !ok {
			return fmt.Errorf("expected inner type Struct, got %T", vector.TypeParam.Value)
		}
		return nil
	})

	ctx.Step(`^the struct address should be "([^"]*)"$`, func(expected string) error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		structTag, ok := tag.Value.(*aptos.StructTag)
		if !ok {
			return fmt.Errorf("expected Struct variant, got %T", tag.Value)
		}
		expectedAddr := &aptos.AccountAddress{}
		err := expectedAddr.ParseStringRelaxed(expected)
		if err != nil {
			return err
		}
		if structTag.Address != *expectedAddr {
			return fmt.Errorf("expected address %s, got %s", expected, structTag.Address.String())
		}
		return nil
	})

	ctx.Step(`^the struct module should be "([^"]*)"$`, func(expected string) error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		structTag, ok := tag.Value.(*aptos.StructTag)
		if !ok {
			return fmt.Errorf("expected Struct variant, got %T", tag.Value)
		}
		if structTag.Module != expected {
			return fmt.Errorf("expected module %s, got %s", expected, structTag.Module)
		}
		return nil
	})

	ctx.Step(`^the struct name should be "([^"]*)"$`, func(expected string) error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		structTag, ok := tag.Value.(*aptos.StructTag)
		if !ok {
			return fmt.Errorf("expected Struct variant, got %T", tag.Value)
		}
		if structTag.Name != expected {
			return fmt.Errorf("expected name %s, got %s", expected, structTag.Name)
		}
		return nil
	})

	ctx.Step(`^the struct should have (\d+) type arguments?$`, func(count int) error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		structTag, ok := tag.Value.(*aptos.StructTag)
		if !ok {
			return fmt.Errorf("expected Struct variant, got %T", tag.Value)
		}
		if len(structTag.TypeParams) != count {
			return fmt.Errorf("expected %d type arguments, got %d", count, len(structTag.TypeParams))
		}
		return nil
	})

	ctx.Step(`^the struct tag should be valid$`, func() error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		if _, ok := tag.Value.(*aptos.StructTag); !ok {
			return fmt.Errorf("expected Struct variant, got %T", tag.Value)
		}
		return nil
	})

	ctx.Step(`^the result should be "([^"]*)"$`, func(expected string) error {
		result, ok := world.Result.(string)
		if !ok {
			return fmt.Errorf("expected string result")
		}
		if result != expected {
			return fmt.Errorf("expected %s, got %s", expected, result)
		}
		return nil
	})

	ctx.Step(`^the string representation should be "([^"]*)"$`, func(expected string) error {
		tag := world.TestVectors["typeTag"].(*aptos.TypeTag)
		result := tag.String()
		if result != expected {
			return fmt.Errorf("expected %s, got %s", expected, result)
		}
		return nil
	})

	ctx.Step(`^the parsing should fail$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected parsing to fail")
		}
		return nil
	})

	ctx.Step(`^the result should equal the original TypeTag$`, func() error {
		original := world.TestVectors["typeTag"].(*aptos.TypeTag)
		deserialized := world.TestVectors["deserializedTypeTag"].(*aptos.TypeTag)
		// Compare string representations
		if original.String() != deserialized.String() {
			return fmt.Errorf("expected %s, got %s", original.String(), deserialized.String())
		}
		return nil
	})

	ctx.Step(`^the address should be "([^"]*)"$`, func(expected string) error {
		moduleId, ok := world.TestVectors["moduleId"].(*aptos.ModuleId)
		if !ok {
			return fmt.Errorf("no module ID set")
		}
		expectedAddr := &aptos.AccountAddress{}
		err := expectedAddr.ParseStringRelaxed(expected)
		if err != nil {
			return err
		}
		if moduleId.Address != *expectedAddr {
			return fmt.Errorf("expected address %s, got %s", expected, moduleId.Address.String())
		}
		return nil
	})

	ctx.Step(`^the module address should be "([^"]*)"$`, func(expected string) error {
		// Check for moduleId first (from type-tags)
		if moduleId, ok := world.TestVectors["moduleId"].(*aptos.ModuleId); ok {
			expectedAddr := &aptos.AccountAddress{}
			err := expectedAddr.ParseStringRelaxed(expected)
			if err != nil {
				return err
			}
			if moduleId.Address != *expectedAddr {
				return fmt.Errorf("expected address %s, got %s", expected, moduleId.Address.StringShort())
			}
			return nil
		}
		// Then check for entryFunction (from entry-function)
		if entryFunc, ok := world.TestVectors["entryFunction"].(*aptos.EntryFunction); ok {
			expectedAddr := &aptos.AccountAddress{}
			err := expectedAddr.ParseStringRelaxed(expected)
			if err != nil {
				return err
			}
			if entryFunc.Module.Address != *expectedAddr {
				return fmt.Errorf("expected address %s, got %s", expected, entryFunc.Module.Address.StringShort())
			}
			return nil
		}
		return fmt.Errorf("no module ID or entry function set")
	})

	ctx.Step(`^the module name should be "([^"]*)"$`, func(expected string) error {
		// Check for moduleId first (from type-tags)
		if moduleId, ok := world.TestVectors["moduleId"].(*aptos.ModuleId); ok {
			if moduleId.Name != expected {
				return fmt.Errorf("expected name %s, got %s", expected, moduleId.Name)
			}
			return nil
		}
		// Then check for entryFunction (from entry-function)
		if entryFunc, ok := world.TestVectors["entryFunction"].(*aptos.EntryFunction); ok {
			if entryFunc.Module.Name != expected {
				return fmt.Errorf("expected module name %s, got %s", expected, entryFunc.Module.Name)
			}
			return nil
		}
		return fmt.Errorf("no module ID or entry function set")
	})

	ctx.Step(`^the name should be "([^"]*)"$`, func(expected string) error {
		moduleId, ok := world.TestVectors["moduleId"].(*aptos.ModuleId)
		if !ok {
			return fmt.Errorf("no module ID set")
		}
		if moduleId.Name != expected {
			return fmt.Errorf("expected name %s, got %s", expected, moduleId.Name)
		}
		return nil
	})
}
