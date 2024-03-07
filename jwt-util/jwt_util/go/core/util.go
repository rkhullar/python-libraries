package x

import (
	"encoding/base64"
	"encoding/json"
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
