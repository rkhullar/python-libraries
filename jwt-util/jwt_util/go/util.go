package main

import "encoding/base64"

func b64enc(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

func strptr(data string) *string {
	return &data
}
