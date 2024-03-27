import functools
from dataclasses import dataclass
from typing import Callable, Optional, Type, TypedDict


class FreeNamesDict(TypedDict, total=False):
    string: Optional[str]
    string_with_error: Optional[str]
    bool_with_error: Optional[str]


def build_with_free(ffi, error_type: Type[Exception], free_funcs: dict[str, Optional[Callable]]) -> Callable:
    def with_free(key: str):
        free_func = free_funcs[key]

        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(cls, pointer, *, free: bool = True):
                result, error = None, None
                if pointer == ffi.NULL:
                    raise error_type
                try:
                    result = fn(cls, pointer)
                except error_type as err:
                    error = err
                finally:
                    if free:
                        if free_func:
                            # TODO: add logger / logging
                            # print(f'{fn.__name__}: calling free {key} on {pointer}')
                            free_func(pointer)
                        else:
                            raise NotImplementedError(f'could not load free function for {key}')
                if error:
                    raise error from None
                return result
            return wrapper
        return decorator
    return with_free


def build_base_adapter(ffi, lib, error_type: Type[Exception], free_names: FreeNamesDict = None):

    def get_free_func(key: str) -> Optional[Callable]:
        if name := free_names.get(key):
            return getattr(lib, name)

    free_funcs = {key: get_free_func(key) for key in FreeNamesDict.__annotations__}
    with_free = build_with_free(ffi, error_type, free_funcs)

    @dataclass
    class BaseExtensionAdapter:

        @staticmethod
        def _encode_string(data: str):
            return ffi.new('char[]', data.encode())

        @staticmethod
        def _encode_int(data: int):
            return ffi.cast('int', data)

        @classmethod
        @with_free('string')
        def _decode_string(cls, data) -> str:
            return ffi.string(data).decode()

        @classmethod
        @with_free('string_with_error')
        def _handle_string_with_error(cls, pointer) -> str:
            if res := pointer.data:
                return cls._decode_string(res, free=False)
            elif err := pointer.error:
                error_message = cls._decode_string(err, free=False)
                raise error_type(error_message)

        @classmethod
        @with_free('bool_with_error')
        def _handle_bool_with_error(cls, ptr) -> bool:
            if res := ptr.data:
                return res
            elif err := ptr.error:
                error_message = cls._decode_string(err, free=False)
                raise error_type(error_message)

    return BaseExtensionAdapter
