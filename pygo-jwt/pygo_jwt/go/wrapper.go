package main

import "C"
import (
	lib "github.com/rkhullar/python-libraries/pygo-jwt/pygo_jwt/go/core"
	"unsafe"
)

// #include <stdlib.h>
// #include <stdbool.h>
import "C"

//export NewJWK
func NewJWK(size C.int, id *C.char) *C.char {
	result := lib.NewJWK(int(size), TranslateStrPtr(id))
	return C.CString(result)
}

//export JWKToPEM
func JWKToPEM(json_data *C.char) *C.char {
	result := lib.JWKToPEM(C.GoString(json_data))
	return C.CString(result)
}

//export PEMToJWK
func PEMToJWK(pem *C.char, id *C.char) *C.char {
	result := lib.PEMToJWK(C.GoString(pem), TranslateStrPtr(id))
	return C.CString(result)
}

//export ParseJWKAndSign
func ParseJWKAndSign(key *C.char, data *C.char) *C.char {
	result := lib.ParseJWKAndSign(C.GoString(key), C.GoString(data))
	return C.CString(result)
}

//export ParsePEMAndSign
func ParsePEMAndSign(key *C.char, data *C.char) *C.char {
	result := lib.ParsePEMAndSign(C.GoString(key), C.GoString(data))
	return C.CString(result)
}

//export ExtractPublicJWK
func ExtractPublicJWK(key *C.char) *C.char {
	result := lib.ExtractPublicJWK(C.GoString(key))
	return C.CString(result)
}

//export ExtractPublicPEM
func ExtractPublicPEM(key *C.char) *C.char {
	result := lib.ExtractPublicPEM(C.GoString(key))
	return C.CString(result)
}

//export ParsePublicJWKAndVerify
func ParsePublicJWKAndVerify(key *C.char, data *C.char, signature *C.char) C.bool {
	result := lib.ParsePublicJWKAndVerify(C.GoString(key), C.GoString(data), C.GoString(signature))
	return C.bool(result)
}

//export ParsePublicPEMAndVerify
func ParsePublicPEMAndVerify(key *C.char, data *C.char, signature *C.char) C.bool {
	result := lib.ParsePublicPEMAndVerify(C.GoString(key), C.GoString(data), C.GoString(signature))
	return C.bool(result)
}

//export FreeCString
func FreeCString(data *C.char) {
	C.free(unsafe.Pointer(data))
}

//export ExampleGo
func ExampleGo(n C.int) {
	lib.ExampleGo(int(n))
}

func TranslateStrPtr(data *C.char) *string {
	if data != nil {
		result := C.GoString(data)
		return &result
	} else {
		return nil
	}
}

func main() {}
