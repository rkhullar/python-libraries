package main

import (
	lib "github.com/rkhullar/python-libraries/jwt-util/core"
)
import "C"

//export NewJWK
func NewJWK(size C.int, id *C.char) *C.char {
	_id := C.GoString(id)
	result := lib.NewJWK(int(size), &_id)
	return C.CString(result)
}

//export JWKToPEM
func JWKToPem(json_data *C.char) *C.char {
	result := lib.JWKToPem(C.GoString(json_data))
	return C.Cstring(result)
}

//export BuildSignature
func BuildSignature() *C.char {
	return C.CString(lib.BuildSignature())
}

func main() {}
