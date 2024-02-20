package main

import "C"
import "fmt"

func hello(message string, count int) string {
	return fmt.Sprintf("hello %s %d", message, count)
}

//export Hello
func Hello(message *C.char, count C.int) *C.char {
	result := hello(C.GoString(message), int(count))
	return C.CString(result)
}

func main() {}
