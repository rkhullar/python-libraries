package util

import (
	"encoding/base64"
	"errors"
	"fmt"
	"math/big"
)

func B64Enc(data ByteSlice) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func B64Dec(data string) (ByteSlice, error) {
	return base64.RawURLEncoding.DecodeString(data)
}

func B64DecBigInt(data any) (*big.Int, error) {
	data_str, ok := data.(string)
	if !ok {
		return nil, errors.New("input data is not a string")
	}
	buffer, err := B64Dec(data_str)
	if err != nil {
		return nil, err
	}
	output := new(big.Int)
	output.SetBytes(buffer)
	return output, nil
}

func B64DecBigIntMap(data StringMap, keys []string) (map[string]*big.Int, error) {
	result := make(map[string]*big.Int)
	for _, key := range keys {
		val, err := B64DecBigInt(data[key])
		if err != nil {
			return nil, fmt.Errorf("failed to decode %s: %w", key, err)
		} else {
			result[key] = val
		}
	}
	return result, nil
}
