package core

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
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
	result, err := MarshalOrdered(data)
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

func MarshalOrdered(data StringMap) (ByteArray, error) {
	result := "{"
	count := 0
	var template string
	for key, value := range data {
		switch value.(type) {
		case string:
			template = `"%s":"%s"`
		default:
			template = `"%s":%v`
		}
		result += fmt.Sprintf(template, key, value) + ","
		count += 1
	}
	if count > 0 {
		result = result[:len(result)-1]
	}
	result += "}"
	return ByteArray(result), nil
}

func B64EncStr(data string) string {
	return b64enc(strenc(data))
}
