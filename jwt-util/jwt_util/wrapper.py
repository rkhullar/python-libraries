from dataclasses import dataclass

from _jwt_util import ffi, lib


@dataclass
class ExtensionAdapter:

    @staticmethod
    def _decode_string(data) -> str:
        output = ffi.string(data).decode()
        lib.FreeCString(data)
        return output

    @classmethod
    def new_jwk(cls, size: int = 2048, _id: str = None) -> str:
        params = [ffi.cast('int', size)]
        if _id:
            params.append(ffi.new('char[]', _id.encode()))
        else:
            params.append(ffi.NULL)
        result = lib.NewJWK(*params)
        return cls._decode_string(result)

    @classmethod
    def jwk_to_pem(cls, jwk: str) -> str:
        param = ffi.new('char[]', jwk.encode())
        result = lib.JWKToPEM(param)
        return cls._decode_string(result)

    @classmethod
    def build_signature(cls) -> str:
        result = lib.BuildSignature()
        return cls._decode_string(result)
