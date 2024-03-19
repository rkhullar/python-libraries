package main

import (
	lib "jwt-util/core"
	"unsafe"
)

// #include <stdlib.h>
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

//export Sign
func Sign(data *C.char) *C.char {
	result := lib.Sign(C.GoString(data))
	return C.CString(result)
}

//export FreeCString
func FreeCString(data *C.char) {
	C.free(unsafe.Pointer(data))
}

//export ExampleGo
func ExampleGo(n C.int) {
	lib.ExampleGo(int(n))
}
func main() {}
