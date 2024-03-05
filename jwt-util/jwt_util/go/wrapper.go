package main

import (
	"github.com/rkhullar/python-libraries/jwt-util/x"
)
import "C"

//export NewJWK
func NewJWK(size C.int, id *C.char) *C.char {
	_id := C.GoString(id)
	result := x.NewJWK(int(size), &_id)
	return C.CString(result)
}

//export BuildSignature
func BuildSignature() *C.char {
	return C.CString(x.BuildSignature())
}

func main() {}
