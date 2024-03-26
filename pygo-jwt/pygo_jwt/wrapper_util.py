from dataclasses import dataclass
from typing import Callable


def build_base_adapter(ffi, lib, free_string_name: str = 'FreeString'):

    @dataclass
    class BaseExtensionAdapter:

        @staticmethod
        def _encode_string(data: str):
            return ffi.new('char[]', data.encode())

        @staticmethod
        def _encode_int(data: int):
            return ffi.cast('int', data)

        @classmethod
        def _decode_string(cls, data) -> str:
            output = ffi.string(data).decode()
            cls._free_string_func(data)
            return output

        @staticmethod
        def _free_string_func() -> Callable:
            return getattr(lib, free_string_name)

    return BaseExtensionAdapter
