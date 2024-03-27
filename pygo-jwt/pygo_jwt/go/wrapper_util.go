package main

import (
	"fmt"
	"sync"
	"unsafe"
)

// #include "wrapper_util.h"
import "C"

var _FreeStringMutex sync.Mutex
var _FreeStringErrorMutex sync.Mutex
var _FreeBoolErrorMutex sync.Mutex

func TranslateStrPtr(data *C.char) *string {
	if data != nil {
		result := C.GoString(data)
		return &result
	} else {
		return nil
	}
}

//export FreeString
func FreeString(data *C.char) {
	defer PreventPanic()
	_FreeStringMutex.Lock()
	defer _FreeStringMutex.Unlock()
	C.free(unsafe.Pointer(data))
}

//export FreeStringWithError
func FreeStringWithError(object *C.StringWithError) {
	defer PreventPanic()
	_FreeStringErrorMutex.Lock()
	defer _FreeStringErrorMutex.Unlock()
	if object.data != nil {
		FreeString(object.data)
	}
	if object.error != nil {
		FreeString(object.error)
	}
	C.free(unsafe.Pointer(object))
}

//export FreeBoolWithError
func FreeBoolWithError(object *C.BoolWithError) {
	defer PreventPanic()
	_FreeBoolErrorMutex.Lock()
	defer _FreeBoolErrorMutex.Unlock()
	if object.error != nil {
		FreeString(object.error)
	}
	C.free(unsafe.Pointer(object))
}

func NewStringWithError() *C.StringWithError {
	return (*C.StringWithError)(C.malloc(C.size_t(unsafe.Sizeof(C.StringWithError{}))))
}

func NewBoolWithError() *C.BoolWithError {
	return (*C.BoolWithError)(C.malloc(C.size_t(unsafe.Sizeof(C.BoolWithError{}))))
}

func HandleStringWithError(res string, err error) *C.StringWithError {
	object := NewStringWithError()
	if err != nil {
		object.data = nil
		object.error = C.CString(err.Error())
	} else {
		object.data = C.CString(res)
		object.error = nil
	}
	return object
}

func HandleBoolWithError(res bool, err error) *C.BoolWithError {
	object := NewBoolWithError()
	if err != nil {
		object.data = false
		object.error = C.CString(err.Error())
	} else {
		object.data = C.bool(res)
		object.error = nil
	}
	return object
}

func PreventPanic() {
	if r := recover(); r != nil {
		fmt.Println("recovered from panic: ", r)
	}
}

/*
 * TODO
 * - check thread safety and mutex usage; implement mutex map?
 * - check memory leaks; use reflection for C.malloc?; check double free?
 * - how to prevent memory errors? i.e: pointer being freed was not allocated
 * - would it be better to return entire struct for StringWithError instead of pointer?
 */
