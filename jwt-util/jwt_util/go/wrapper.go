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
func JWKToPEM(json_data *C.char) *C.char {
	result := lib.JWKToPEM(C.GoString(json_data))
	return C.CString(result)
}

//export PEMToJWK
func PEMToJWK(pem *C.char) *C.char {
	result := lib.PEMToJWK(C.GoString(pem))
	return C.CString(result)
}

//export BuildSignature
func BuildSignature() *C.char {
	return C.CString(lib.BuildSignature())
}

func main() {}
