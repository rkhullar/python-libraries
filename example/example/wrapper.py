from _example import ffi, lib
from dataclasses import dataclass


@dataclass
class ExtensionAdapter:

    @staticmethod
    def hello(message: str, count: int = 1) -> str:
        params = ffi.new('char[]', message.encode()), ffi.cast('int', count)
        result = lib.Hello(*params)
        return ffi.string(result).decode()
