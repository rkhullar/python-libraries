package main

// #include "wrapper_util.h"
import "C"
import (
	"sync"
	"unsafe"
)

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

//export FreeCString
func FreeCString(data *C.char) {
	_FreeStringMutex.Lock()
	defer _FreeStringMutex.Unlock()
	C.free(unsafe.Pointer(data))
}

//export FreeStringWithError
func FreeStringWithError(object *C.StringWithError) {
	_FreeStringErrorMutex.Lock()
	defer _FreeStringErrorMutex.Unlock()
	if object.data != nil {
		FreeCString(object.data)
	}
	if object.error != nil {
		FreeCString(object.error)
	}
	C.free(unsafe.Pointer(object))
}

//export FreeBoolWithError
func FreeBoolWithError(object *C.BoolWithError) {
	_FreeBoolErrorMutex.Lock()
	defer _FreeBoolErrorMutex.Unlock()
	if object.error != nil {
		FreeCString(object.error)
	}
	C.free(unsafe.Pointer(object))
}

func HandleStringWithError(res string, err error) *C.StringWithError {
	if err != nil {
		return &C.StringWithError{nil, C.CString(err.Error())}
	} else {
		return &C.StringWithError{C.CString(res), nil}
	}
}

func HandleBoolWithError(res bool, err error) *C.BoolWithError {
	if err != nil {
		return &C.BoolWithError{false, C.CString(err.Error())}
	} else {
		return &C.BoolWithError{C.bool(res), nil}
	}
}

/*
 * TODO
 * - check thread safety and mutex usage; implement mutex map?
 * - check memory leaks; use C.malloc?
 */
