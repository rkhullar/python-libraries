package util

import (
	"crypto/sha256"
	"errors"
	"reflect"
)

func ByteArrayToSlice32(array [32]byte) ByteSlice {
	slice := make(ByteSlice, len(array))
	copy(slice, array[:])
	return slice
}

func ByteArrayToSlice(array any) (ByteSlice, error) {
	_type := reflect.TypeOf(array)
	if _type.Kind() != reflect.Array {
		return nil, errors.New("unexpected data type")
	}
	slice := make(ByteSlice, _type.Len())
	reflect.Copy(reflect.ValueOf(slice), reflect.ValueOf(array))
	return slice, nil
}

func SHA256Sum(data string) ByteSlice {
	return ByteArrayToSlice32(sha256.Sum256(StrEnc(data)))
}
