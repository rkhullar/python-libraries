from dataclasses import dataclass
from typing import Callable, Optional, Type, TypedDict


class FreeNamesDict(TypedDict, total=False):
    string: str
    string_with_error: str
    bool_with_error: str


def build_base_adapter(ffi, lib, error_type: Type[Exception], free_names: FreeNamesDict = None):

    def get_free_func(key: str) -> Optional[Callable]:
        if name := free_names.get(key):
            return getattr(lib, name)

    free_funcs = {key: get_free_func(key) for key in FreeNamesDict.__annotations__}

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
                free_funcs['string'](data)
            return output

        @classmethod
        def _handle_string_with_error(cls, obj, free: bool = True) -> str:
            if obj == ffi.NULL:
                raise error_type
            elif res := obj.data:
                output = cls._decode_string(res, free=False)
                free_funcs['string_with_error'](obj)
                return output
            elif err := obj.error:
                error_message = cls._decode_string(err, free=False)
                free_funcs['string_with_error'](obj)
                raise error_type(error_message)

        @classmethod
        def _handle_bool_with_error(cls, obj, free: bool = True) -> bool:
            if obj == ffi.NULL:
                raise error_type
            elif res := obj.data:
                output = res
                free_funcs['bool_with_error'](obj)
                return output
            elif err := obj.error:
                error_message = cls._decode_string(err, free=False)
                free_funcs['bool_with_error'](obj)
                raise error_type(error_message)

    return BaseExtensionAdapter
