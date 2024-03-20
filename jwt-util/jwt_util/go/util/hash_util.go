package util

import (
	"crypto/sha256"
	"reflect"
)

func ByteArrayToSlice32(array [32]byte) []byte {
	slice := make([]byte, len(array))
	copy(slice, array[:])
	return slice
}

func ByteArrayToSlice(array any) []byte {
	_type := reflect.TypeOf(array)
	if _type.Kind() != reflect.Array {
		panic("unexpected data type")
	}
	slice := make([]byte, _type.Len())
	reflect.Copy(reflect.ValueOf(slice), reflect.ValueOf(array))
	return slice
}

func SHA256Sum(data string) ByteArray {
	return ByteArrayToSlice32(sha256.Sum256(StrEnc(data)))
}
