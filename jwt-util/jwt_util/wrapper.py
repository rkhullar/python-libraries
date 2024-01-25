from _jwt_util import ffi, lib
from dataclasses import dataclass


@dataclass
class ExtensionAdapter:

    @staticmethod
    def build_signature() -> str:
        result = lib.BuildSignature()
        return ffi.string(result).decode()
