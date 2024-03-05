from dataclasses import dataclass

from _jwt_util import ffi, lib


@dataclass
class ExtensionAdapter:

    @staticmethod
    def new_jwk(size: int = 2048, _id: str = None) -> str:
        params = [ffi.cast('int', size)]
        if _id:
            params.append(ffi.new('char[]', _id.encode()))
        else:
            params.append(ffi.NULL)
        result = lib.NewJWK(*params)
        return ffi.string(result).decode()

    @staticmethod
    def jwk_to_pem(jwk: str) -> str:
        param = ffi.new('char[]', jwk.encode())
        result = lib.JWKToPEM(param)
        return ffi.string(result).decode()

    @staticmethod
    def build_signature() -> str:
        result = lib.BuildSignature()
        return ffi.string(result).decode()
