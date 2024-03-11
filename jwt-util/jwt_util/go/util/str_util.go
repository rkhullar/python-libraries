package util

func strptr(data string) *string {
	return &data
}

func strenc(data string) []byte {
	return ByteArray(data)
}

func B64EncStr(data string) string {
	return b64enc(strenc(data))
}
