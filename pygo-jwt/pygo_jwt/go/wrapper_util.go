package main

// #include "wrapper_util.h"
import "C"
import "unsafe"

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
	C.free(unsafe.Pointer(data))
}

//export FreeStringWithError
func FreeStringWithError(data *C.StringWithError) {
	C.free(unsafe.Pointer(data))
}

//export FreeBoolWithError
func FreeBoolWithError(data *C.BoolWithError) {
	C.free(unsafe.Pointer(data))
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
