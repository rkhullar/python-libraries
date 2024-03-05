package x

import (
	"encoding/base64"
	"encoding/json"
)

type StringMap map[string]string

func b64enc(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func b64dec(data string) []byte {
	res, err := base64.RawURLEncoding.DecodeString(data)
	if err != nil {
		panic(err)
	}
	return res
}

func strptr(data string) *string {
	return &data
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
	err := json.Unmarshal([]byte(json_data), &data)
	if err != nil {
		panic(err)
	}
	return data
}
