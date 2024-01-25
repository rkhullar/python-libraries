package main

import "C"

//export BuildSignature
func BuildSignature() *C.char {
	return C.CString(build_signature())
}
