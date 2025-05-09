#ifndef WRAPPER_UTIL_H
#define WRAPPER_UTIL_H

#include <stdlib.h>
#include <stdbool.h>

typedef struct string_with_error {char* data; char* error;} StringWithError;
typedef struct bool_with_error {bool data; char* error;} BoolWithError;

#endif