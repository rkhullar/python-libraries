package main

import (
	"encoding/base64"
	"encoding/json"
)

type StringMap map[string]string

func b64enc(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func strptr(data string) *string {
	return &data
}

func to_json(data StringMap) string {
	result, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	return string(result)
}
