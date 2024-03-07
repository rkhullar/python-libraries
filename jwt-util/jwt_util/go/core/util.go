package x

import (
	"encoding/base64"
	"encoding/json"
	"math/big"
)

type ByteArray []byte
type StringMap map[string]any

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

func strptr(data string) *string {
	return &data
}

func strenc(data string) []byte {
	return ByteArray(data)
}

func MapToJSON(data StringMap) string {
	result, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	return string(result)
}

func ParseJSON(json_data string) StringMap {
	var data StringMap
	err := json.Unmarshal(strenc(json_data), &data)
	if err != nil {
		panic(err)
	}
	return data
}
