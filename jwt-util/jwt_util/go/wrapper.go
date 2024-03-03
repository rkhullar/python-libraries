package main

import "C"

//export BuildKey
func BuildKey(size C.int, id *C.char) *C.char {
	_id := C.GoString(id)
	result := build_key(int(size), &_id)
	return C.CString(result)
}

//export BuildSignature
func BuildSignature() *C.char {
	return C.CString(build_signature())
}
