package main

import (
	"sync"
	"unsafe"
)

/*
#ifndef WRAPPER_UTIL_H
#define WRAPPER_UTIL_H

#include <stdlib.h>
#include <stdbool.h>

typedef struct string_with_error {char* data; char* error;} StringWithError;
typedef struct bool_with_error {bool data; char* error;} BoolWithError;

#endif
*/
import "C"

// TODO: change to `#include "wrapper_util.h"` once supported

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
	_FreeStringMutex.Lock()
	defer _FreeStringMutex.Unlock()
	C.free(unsafe.Pointer(data))
}

//export FreeStringWithError
func FreeStringWithError(object *C.StringWithError) {
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

/*
 * TODO
 * - check thread safety and mutex usage; implement mutex map?
 * - check memory leaks; use C.malloc?
 * - how to prevent potential panic?
 */
