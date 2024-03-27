from dataclasses import dataclass
from typing import Type


def build_base_adapter(ffi, lib, error_type: Type[Exception], free_string_name: str = 'FreeString',
                       free_string_with_error_name: str = 'FreeStringWithError',
                       free_bool_with_error_name: str = 'FreeBoolWithError'):

    free_string_func = getattr(lib, free_string_name)
    free_string_with_error_func = getattr(lib, free_string_with_error_name)
    free_bool_with_error_func = getattr(lib, free_bool_with_error_name)

    @dataclass
    class BaseExtensionAdapter:

        @staticmethod
        def _encode_string(data: str):
            return ffi.new('char[]', data.encode())

        @staticmethod
        def _encode_int(data: int):
            return ffi.cast('int', data)

        @classmethod
        def _decode_string(cls, data, free: bool = True) -> str:
            output = ffi.string(data).decode()
            if free:
                free_string_func(data)
            return output

        @classmethod
        def _handle_string_with_error(cls, obj) -> str:
            if obj == ffi.NULL:
                raise error_type
            elif res := obj.data:
                output = cls._decode_string(res, free=False)
                free_string_with_error_func(obj)
                return output
            elif err := obj.error:
                error_message = cls._decode_string(err, free=False)
                free_string_with_error_func(obj)
                raise error_type(error_message)

        @classmethod
        def _handle_bool_with_error(cls, obj) -> bool:
            if obj == ffi.NULL:
                raise error_type
            elif res := obj.data:
                output = res
                free_bool_with_error_func(obj)
                return output
            elif err := obj.error:
                error_message = cls._decode_string(err, free=False)
                free_bool_with_error_func(obj)
                raise error_type(error_message)

    return BaseExtensionAdapter
