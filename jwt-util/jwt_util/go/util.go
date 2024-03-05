package main

import (
	"encoding/base64"
	"encoding/json"
)

func b64enc(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func strptr(data string) *string {
	return &data
}

func to_json(data map[string]interface{}) string {
	result, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	return string(result)
}
