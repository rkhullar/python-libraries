package util

import (
	"encoding/base64"
	"math/big"
)

func b64enc(data ByteArray) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func b64dec(data string) ByteArray {
	res, err := base64.RawURLEncoding.DecodeString(data)
	if err != nil {
		panic(err)
	}
	return res
}

func b64dec_bigint(data any) *big.Int {
	data_str, ok := data.(string)
	if !ok {
		panic("input data is not a string")
	}
	buffer := b64dec(data_str)
	output := new(big.Int)
	output.SetBytes(buffer)
	return output
}
