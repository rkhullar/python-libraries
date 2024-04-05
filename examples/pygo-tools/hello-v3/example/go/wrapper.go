package main

import "C"

//export Hello
func Hello(message *C.char, count C.int) *C.char {
	result := hello(C.GoString(message), int(count))
	return C.CString(result)
}

func main() {}
