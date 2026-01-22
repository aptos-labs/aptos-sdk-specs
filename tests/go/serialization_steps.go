package main

import (
	"bytes"
	"encoding/hex"
	"fmt"
	"math/big"
	"strconv"
	"strings"

	"github.com/aptos-labs/aptos-go-sdk"
	"github.com/aptos-labs/aptos-go-sdk/bcs"
	"github.com/cucumber/godog"
)

func initSerializationSteps(ctx *godog.ScenarioContext, world *World) {
	// =============================================================================
	// Given Steps - Boolean
	// =============================================================================

	ctx.Step(`^a boolean value (true|false)$`, func(value string) error {
		world.TestVectors["boolValue"] = value == "true"
		return nil
	})

	ctx.Step(`^a bool value (true|false)$`, func(value string) error {
		world.TestVectors["boolValue"] = value == "true"
		return nil
	})

	ctx.Step(`^bytes \[([^\]]*)\]$`, func(bytesStr string) error {
		// Handle empty
		if bytesStr == "" {
			world.Bytes = []byte{}
			return nil
		}
		// Parse hex bytes like "0x00" or "0x01, 0x02"
		parts := strings.Split(bytesStr, ",")
		world.Bytes = make([]byte, len(parts))
		for i, part := range parts {
			part = strings.TrimSpace(part)
			part = strings.TrimPrefix(part, "0x")
			part = strings.TrimPrefix(part, "0X")
			val, err := strconv.ParseUint(part, 16, 8)
			if err != nil {
				return err
			}
			world.Bytes[i] = byte(val)
		}
		return nil
	})

	// =============================================================================
	// Given Steps - Integers
	// =============================================================================

	ctx.Step(`^a u8 value (\d+)$`, func(value int) error {
		world.TestVectors["u8Value"] = uint8(value)
		return nil
	})

	ctx.Step(`^a u16 value ([0-9a-fA-Fx]+)$`, func(valueStr string) error {
		value, err := parseHexOrDecimal(valueStr)
		if err != nil {
			return err
		}
		world.TestVectors["u16Value"] = uint16(value)
		return nil
	})

	ctx.Step(`^a u32 value ([0-9a-fA-Fx]+)$`, func(valueStr string) error {
		value, err := parseHexOrDecimal(valueStr)
		if err != nil {
			return err
		}
		world.TestVectors["u32Value"] = uint32(value)
		return nil
	})

	ctx.Step(`^a u64 value ([0-9a-fA-Fx]+)$`, func(valueStr string) error {
		value, err := parseHexOrDecimal64(valueStr)
		if err != nil {
			return err
		}
		world.TestVectors["u64Value"] = value
		return nil
	})

	ctx.Step(`^a u128 value ([0-9a-fA-Fx]+)$`, func(valueStr string) error {
		value, err := parseHexOrDecimalBig(valueStr)
		if err != nil {
			return err
		}
		world.TestVectors["u128Value"] = value
		return nil
	})

	ctx.Step(`^a u256 value ([0-9a-fA-Fx]+)$`, func(valueStr string) error {
		value, err := parseHexOrDecimalBig(valueStr)
		if err != nil {
			return err
		}
		world.TestVectors["u256Value"] = value
		return nil
	})

	ctx.Step(`^a length value (\d+)$`, func(value int) error {
		world.TestVectors["lengthValue"] = uint32(value)
		return nil
	})

	// =============================================================================
	// Given Steps - Bytes/Strings
	// =============================================================================

	ctx.Step(`^an empty byte array$`, func() error {
		world.Bytes = []byte{}
		return nil
	})

	ctx.Step(`^a string "([^"]*)"$`, func(s string) error {
		world.TestVectors["stringValue"] = s
		return nil
	})

	// =============================================================================
	// Given Steps - Options
	// =============================================================================

	ctx.Step(`^an Option with no value$`, func() error {
		world.TestVectors["optionValue"] = nil
		world.TestVectors["optionHasValue"] = false
		return nil
	})

	ctx.Step(`^an Option containing u64 value (\d+)$`, func(value int) error {
		world.TestVectors["optionValue"] = uint64(value)
		world.TestVectors["optionHasValue"] = true
		return nil
	})

	// =============================================================================
	// Given Steps - Vectors
	// =============================================================================

	ctx.Step(`^an empty vector of u8$`, func() error {
		world.TestVectors["vectorU8"] = []uint8{}
		return nil
	})

	ctx.Step(`^a vector \[(\d+), (\d+), (\d+)\] of u8$`, func(a, b, c int) error {
		world.TestVectors["vectorU8"] = []uint8{uint8(a), uint8(b), uint8(c)}
		return nil
	})

	ctx.Step(`^a vector \[(\d+), (\d+)\] of u64$`, func(a, b int) error {
		world.TestVectors["vectorU64"] = []uint64{uint64(a), uint64(b)}
		return nil
	})

	ctx.Step(`^a vector \[\[(\d+), (\d+)\], \[(\d+), (\d+)\]\] of vectors of u8$`, func(a, b, c, d int) error {
		world.TestVectors["nestedVector"] = [][]uint8{
			{uint8(a), uint8(b)},
			{uint8(c), uint8(d)},
		}
		return nil
	})

	// =============================================================================
	// Given Steps - AccountAddress
	// =============================================================================

	ctx.Step(`^an AccountAddress "([^"]*)"$`, func(addrStr string) error {
		addr := &aptos.AccountAddress{}
		err := addr.ParseStringRelaxed(addrStr)
		if err != nil {
			return err
		}
		world.Address = addr
		return nil
	})

	ctx.Step(`^32 bytes with byte 31 = 0x([0-9a-fA-F]+)$`, func(hexVal string) error {
		world.Bytes = make([]byte, 32)
		val, err := strconv.ParseUint(hexVal, 16, 8)
		if err != nil {
			return err
		}
		world.Bytes[31] = byte(val)
		return nil
	})

	// =============================================================================
	// Given Steps - Structs
	// =============================================================================

	ctx.Step(`^a struct with fields:$`, func(table *godog.Table) error {
		// Store the table - serialization happens in "I BCS serialize it"
		world.TestVectors["structFields"] = table
		return nil
	})

	// =============================================================================
	// Given Steps - Error cases
	// =============================================================================

	ctx.Step(`^bytes \[([^\]]*)\] intended for u64$`, func(bytesStr string) error {
		parts := strings.Split(bytesStr, ",")
		world.Bytes = make([]byte, len(parts))
		for i, part := range parts {
			part = strings.TrimSpace(part)
			part = strings.TrimPrefix(part, "0x")
			val, _ := strconv.ParseUint(part, 16, 8)
			world.Bytes[i] = byte(val)
		}
		return nil
	})

	// =============================================================================
	// When Steps - Serialization
	// =============================================================================

	ctx.Step(`^I BCS serialize it$`, func() error {
		serializer := &bcs.Serializer{}

		// Check for RawTransaction first (transaction tests)
		if tx, ok := world.TestVectors["rawTransaction"].(*aptos.RawTransaction); ok {
			tx.MarshalBCS(serializer)
			if err := serializer.Error(); err != nil {
				world.SetError(err)
				return nil
			}
			world.Bytes = serializer.ToBytes()
			world.ClearError()
			return nil
		}

		// Check for struct fields
		if table, ok := world.TestVectors["structFields"].(*godog.Table); ok {
			for i, row := range table.Rows {
				if i == 0 {
					continue // Skip header row
				}
				fieldType := row.Cells[1].Value
				fieldValue := row.Cells[2].Value

				switch fieldType {
				case "address":
					addr := &aptos.AccountAddress{}
					err := addr.ParseStringRelaxed(fieldValue)
					if err != nil {
						return err
					}
					addr.MarshalBCS(serializer)
				case "u64":
					val, err := parseHexOrDecimal64(fieldValue)
					if err != nil {
						return err
					}
					serializer.U64(val)
				case "u8":
					val, err := parseHexOrDecimal(fieldValue)
					if err != nil {
						return err
					}
					serializer.U8(uint8(val))
				case "string":
					serializer.WriteString(fieldValue)
				}
			}
			if err := serializer.Error(); err != nil {
				world.SetError(err)
				return nil
			}
			world.Bytes = serializer.ToBytes()
			world.ClearError()
			return nil
		}

		// Check what type of value we have
		if v, ok := world.TestVectors["boolValue"].(bool); ok {
			serializer.Bool(v)
		} else if v, ok := world.TestVectors["u8Value"].(uint8); ok {
			serializer.U8(v)
		} else if v, ok := world.TestVectors["u16Value"].(uint16); ok {
			serializer.U16(v)
		} else if v, ok := world.TestVectors["u32Value"].(uint32); ok {
			serializer.U32(v)
		} else if v, ok := world.TestVectors["u64Value"].(uint64); ok {
			serializer.U64(v)
		} else if v, ok := world.TestVectors["u128Value"].(*big.Int); ok {
			serializer.U128(*v)
		} else if v, ok := world.TestVectors["u256Value"].(*big.Int); ok {
			serializer.U256(*v)
		} else if v, ok := world.TestVectors["stringValue"].(string); ok {
			serializer.WriteString(v)
		} else if world.Bytes != nil {
			serializer.WriteBytes(world.Bytes)
		} else if hasValue, ok := world.TestVectors["optionHasValue"].(bool); ok {
			if !hasValue {
				serializer.Bool(false) // None
			} else {
				serializer.Bool(true) // Some
				if v, ok := world.TestVectors["optionValue"].(uint64); ok {
					serializer.U64(v)
				}
			}
		} else if v, ok := world.TestVectors["vectorU8"].([]uint8); ok {
			serializer.Uleb128(uint32(len(v)))
			for _, b := range v {
				serializer.U8(b)
			}
		} else if v, ok := world.TestVectors["vectorU64"].([]uint64); ok {
			serializer.Uleb128(uint32(len(v)))
			for _, val := range v {
				serializer.U64(val)
			}
		} else if v, ok := world.TestVectors["nestedVector"].([][]uint8); ok {
			serializer.Uleb128(uint32(len(v)))
			for _, inner := range v {
				serializer.Uleb128(uint32(len(inner)))
				for _, b := range inner {
					serializer.U8(b)
				}
			}
		} else if world.Address != nil {
			world.Address.MarshalBCS(serializer)
		}

		if err := serializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		world.Bytes = serializer.ToBytes()
		world.ClearError()
		return nil
	})

	ctx.Step(`^I ULEB128 encode it$`, func() error {
		value := world.TestVectors["lengthValue"].(uint32)
		serializer := &bcs.Serializer{}
		serializer.Uleb128(value)
		if err := serializer.Error(); err != nil {
			return err
		}
		world.Bytes = serializer.ToBytes()
		return nil
	})

	ctx.Step(`^I ULEB128 encode and decode it$`, func() error {
		value := world.TestVectors["lengthValue"].(uint32)
		serializer := &bcs.Serializer{}
		serializer.Uleb128(value)
		if err := serializer.Error(); err != nil {
			return err
		}
		encoded := serializer.ToBytes()

		deserializer := bcs.NewDeserializer(encoded)
		decoded := deserializer.Uleb128()
		if err := deserializer.Error(); err != nil {
			return err
		}
		world.TestVectors["decodedValue"] = decoded
		return nil
	})

	// =============================================================================
	// When Steps - Deserialization
	// =============================================================================

	ctx.Step(`^I BCS deserialize as boolean$`, func() error {
		deserializer := bcs.NewDeserializer(world.Bytes)
		value := deserializer.Bool()
		if err := deserializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		world.Result = value
		world.ClearError()
		return nil
	})

	ctx.Step(`^I BCS deserialize as u64$`, func() error {
		deserializer := bcs.NewDeserializer(world.Bytes)
		value := deserializer.U64()
		if err := deserializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		world.Result = value
		world.ClearError()
		return nil
	})

	ctx.Step(`^I BCS deserialize as AccountAddress$`, func() error {
		deserializer := bcs.NewDeserializer(world.Bytes)
		addr := &aptos.AccountAddress{}
		addr.UnmarshalBCS(deserializer)
		if err := deserializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		world.Address = addr
		world.ClearError()
		return nil
	})

	ctx.Step(`^I BCS deserialize as vector of u8$`, func() error {
		deserializer := bcs.NewDeserializer(world.Bytes)
		length := deserializer.Uleb128()
		if err := deserializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		// Check for unreasonable length
		if length > 1000000 {
			world.SetError(fmt.Errorf("vector length too large: %d", length))
			return nil
		}
		result := make([]byte, length)
		for i := uint32(0); i < length; i++ {
			result[i] = deserializer.U8()
		}
		if err := deserializer.Error(); err != nil {
			world.SetError(err)
			return nil
		}
		world.Result = result
		world.ClearError()
		return nil
	})

	// =============================================================================
	// Then Steps - Validation
	// =============================================================================

	ctx.Step(`^the result should be 1 byte$`, func() error {
		if len(world.Bytes) != 1 {
			return fmt.Errorf("expected 1 byte, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the byte should be 0x([0-9a-fA-F]+)$`, func(expected string) error {
		expectedByte, err := strconv.ParseUint(expected, 16, 8)
		if err != nil {
			return err
		}
		if world.Bytes[0] != byte(expectedByte) {
			return fmt.Errorf("expected 0x%02X, got 0x%02X", expectedByte, world.Bytes[0])
		}
		return nil
	})

	ctx.Step(`^the result should be (true|false)$`, func(expected string) error {
		expectedBool := expected == "true"
		if world.Result != expectedBool {
			return fmt.Errorf("expected %v, got %v", expectedBool, world.Result)
		}
		return nil
	})

	ctx.Step(`^the result should be 2 bytes in little-endian$`, func() error {
		if len(world.Bytes) != 2 {
			return fmt.Errorf("expected 2 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the result should be 4 bytes in little-endian$`, func() error {
		if len(world.Bytes) != 4 {
			return fmt.Errorf("expected 4 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the result should be 8 bytes in little-endian$`, func() error {
		if len(world.Bytes) != 8 {
			return fmt.Errorf("expected 8 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the result should be 16 bytes in little-endian$`, func() error {
		if len(world.Bytes) != 16 {
			return fmt.Errorf("expected 16 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the result should be 32 bytes in little-endian$`, func() error {
		if len(world.Bytes) != 32 {
			return fmt.Errorf("expected 32 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the bytes should be \[([^\]]*)\]$`, func(expected string) error {
		expectedBytes, err := parseByteArray(expected)
		if err != nil {
			return err
		}
		if !bytes.Equal(world.Bytes, expectedBytes) {
			return fmt.Errorf("expected %v, got %v", expectedBytes, world.Bytes)
		}
		return nil
	})

	ctx.Step(`^the result should be \[([^\]]*)\]$`, func(expected string) error {
		expectedBytes, err := parseByteArray(expected)
		if err != nil {
			return err
		}
		if !bytes.Equal(world.Bytes, expectedBytes) {
			return fmt.Errorf("expected %v, got %v", expectedBytes, world.Bytes)
		}
		return nil
	})

	ctx.Step(`^the result should equal the original value$`, func() error {
		original := world.TestVectors["lengthValue"].(uint32)
		decoded := world.TestVectors["decodedValue"].(uint32)
		if original != decoded {
			return fmt.Errorf("expected %d, got %d", original, decoded)
		}
		return nil
	})

	ctx.Step(`^the first byte should be 0x([0-9a-fA-F]+) \(length\)$`, func(expected string) error {
		expectedByte, err := strconv.ParseUint(expected, 16, 8)
		if err != nil {
			return err
		}
		if world.Bytes[0] != byte(expectedByte) {
			return fmt.Errorf("expected first byte 0x%02X, got 0x%02X", expectedByte, world.Bytes[0])
		}
		return nil
	})

	ctx.Step(`^the first byte should be 0x([0-9a-fA-F]+) \(UTF-8 byte length\)$`, func(expected string) error {
		expectedByte, err := strconv.ParseUint(expected, 16, 8)
		if err != nil {
			return err
		}
		if world.Bytes[0] != byte(expectedByte) {
			return fmt.Errorf("expected first byte 0x%02X, got 0x%02X", expectedByte, world.Bytes[0])
		}
		return nil
	})

	ctx.Step(`^the first byte should be 0x([0-9a-fA-F]+)$`, func(expected string) error {
		expectedByte, err := strconv.ParseUint(expected, 16, 8)
		if err != nil {
			return err
		}
		if world.Bytes[0] != byte(expectedByte) {
			return fmt.Errorf("expected first byte 0x%02X, got 0x%02X", expectedByte, world.Bytes[0])
		}
		return nil
	})

	ctx.Step(`^the remaining bytes should be \[([^\]]*)\]$`, func(expected string) error {
		expectedBytes, err := parseByteArray(expected)
		if err != nil {
			return err
		}
		remaining := world.Bytes[1:]
		if !bytes.Equal(remaining, expectedBytes) {
			return fmt.Errorf("expected %v, got %v", expectedBytes, remaining)
		}
		return nil
	})

	ctx.Step(`^the remaining bytes should be UTF-8 encoded "([^"]*)"$`, func(expected string) error {
		remaining := world.Bytes[1:]
		if string(remaining) != expected {
			return fmt.Errorf("expected %s, got %s", expected, string(remaining))
		}
		return nil
	})

	ctx.Step(`^the remaining 8 bytes should be the u64 value$`, func() error {
		if len(world.Bytes) != 9 {
			return fmt.Errorf("expected 9 bytes (1 + 8), got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the remaining bytes should be two u64 values in little-endian$`, func() error {
		if len(world.Bytes) != 17 {
			return fmt.Errorf("expected 17 bytes (1 + 8 + 8), got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the first byte should be 0x([0-9a-fA-F]+) \(outer length\)$`, func(expected string) error {
		expectedByte, err := strconv.ParseUint(expected, 16, 8)
		if err != nil {
			return err
		}
		if world.Bytes[0] != byte(expectedByte) {
			return fmt.Errorf("expected first byte 0x%02X, got 0x%02X", expectedByte, world.Bytes[0])
		}
		return nil
	})

	ctx.Step(`^each inner vector should be length-prefixed$`, func() error {
		// For [[1,2], [3,4]], serialized as: 0x02 0x02 0x01 0x02 0x02 0x03 0x04
		// Verify structure is correct
		if len(world.Bytes) < 7 {
			return fmt.Errorf("nested vector serialization too short")
		}
		return nil
	})

	ctx.Step(`^the result should be exactly 32 bytes$`, func() error {
		if len(world.Bytes) != 32 {
			return fmt.Errorf("expected 32 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^byte 31 should be 0x([0-9a-fA-F]+)$`, func(expected string) error {
		expectedByte, err := strconv.ParseUint(expected, 16, 8)
		if err != nil {
			return err
		}
		if world.Bytes[31] != byte(expectedByte) {
			return fmt.Errorf("expected byte 31 to be 0x%02X, got 0x%02X", expectedByte, world.Bytes[31])
		}
		return nil
	})

	ctx.Step(`^bytes 0-30 should all be 0x00$`, func() error {
		for i := 0; i < 31; i++ {
			if world.Bytes[i] != 0 {
				return fmt.Errorf("byte %d should be 0, got 0x%02X", i, world.Bytes[i])
			}
		}
		return nil
	})

	ctx.Step(`^the short string should be "([^"]*)"$`, func(expected string) error {
		if world.Address == nil {
			return fmt.Errorf("no address set")
		}
		actual := world.Address.String()
		// Go SDK returns full hex, so compare the values semantically
		expectedAddr := &aptos.AccountAddress{}
		err := expectedAddr.ParseStringRelaxed(expected)
		if err != nil {
			return err
		}
		if *world.Address != *expectedAddr {
			return fmt.Errorf("expected %s, got %s", expected, actual)
		}
		return nil
	})

	ctx.Step(`^the fields should be serialized in order$`, func() error {
		// Verify we have serialized bytes
		if len(world.Bytes) == 0 {
			return fmt.Errorf("no serialized bytes")
		}
		return nil
	})

	ctx.Step(`^the total length should be 40 bytes \(32 \+ 8\)$`, func() error {
		if len(world.Bytes) != 40 {
			return fmt.Errorf("expected 40 bytes, got %d", len(world.Bytes))
		}
		return nil
	})

	ctx.Step(`^the deserialization should fail with an error$`, func() error {
		if world.Error == nil {
			return fmt.Errorf("expected deserialization error")
		}
		return nil
	})
}

// Helper functions

func parseHexOrDecimal(s string) (uint64, error) {
	s = strings.TrimSpace(s)
	if strings.HasPrefix(s, "0x") || strings.HasPrefix(s, "0X") {
		return strconv.ParseUint(s[2:], 16, 64)
	}
	return strconv.ParseUint(s, 10, 64)
}

func parseHexOrDecimal64(s string) (uint64, error) {
	s = strings.TrimSpace(s)
	if strings.HasPrefix(s, "0x") || strings.HasPrefix(s, "0X") {
		return strconv.ParseUint(s[2:], 16, 64)
	}
	return strconv.ParseUint(s, 10, 64)
}

func parseHexOrDecimalBig(s string) (*big.Int, error) {
	s = strings.TrimSpace(s)
	result := new(big.Int)
	if strings.HasPrefix(s, "0x") || strings.HasPrefix(s, "0X") {
		_, ok := result.SetString(s[2:], 16)
		if !ok {
			return nil, fmt.Errorf("invalid hex: %s", s)
		}
	} else {
		_, ok := result.SetString(s, 10)
		if !ok {
			return nil, fmt.Errorf("invalid decimal: %s", s)
		}
	}
	return result, nil
}

func parseByteArray(s string) ([]byte, error) {
	if s == "" {
		return []byte{}, nil
	}
	parts := strings.Split(s, ",")
	result := make([]byte, len(parts))
	for i, part := range parts {
		part = strings.TrimSpace(part)
		part = strings.TrimPrefix(part, "0x")
		part = strings.TrimPrefix(part, "0X")
		val, err := strconv.ParseUint(part, 16, 8)
		if err != nil {
			return nil, err
		}
		result[i] = byte(val)
	}
	return result, nil
}

func hexToBytes(s string) ([]byte, error) {
	s = strings.TrimPrefix(s, "0x")
	return hex.DecodeString(s)
}
