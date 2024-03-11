package util

func StrPtr(data string) *string {
	return &data
}

func StrEnc(data string) []byte {
	return ByteArray(data)
}

func B64StrEnc(data string) string {
	return b64enc(StrEnc(data))
}
