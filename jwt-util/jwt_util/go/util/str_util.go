package util

func StrPtr(data string) *string {
	return &data
}

func StrEnc(data string) ByteSlice {
	return ByteSlice(data)
}

func B64StrEnc(data string) string {
	return B64Enc(StrEnc(data))
}

func StringMap_GetStrPtr(data StringMap, key string) *string {
	value := data[key]
	if value != nil {
		value_str := value.(string)
		return &value_str
	}
	return nil
}
