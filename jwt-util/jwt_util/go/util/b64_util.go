package util

import (
	"encoding/base64"
	"math/big"
)

func B64Enc(data ByteArray) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func B64Dec(data string) ByteArray {
	res, err := base64.RawURLEncoding.DecodeString(data)
	if err != nil {
		panic(err)
	}
	return res
}

func B64DecBigInt(data any) *big.Int {
	data_str, ok := data.(string)
	if !ok {
		panic("input data is not a string")
	}
	buffer := B64Dec(data_str)
	output := new(big.Int)
	output.SetBytes(buffer)
	return output
}
