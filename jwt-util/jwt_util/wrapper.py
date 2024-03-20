from dataclasses import dataclass

from _jwt_util import ffi, lib

from .time_util import timed


@dataclass
class ExtensionAdapter:

    @staticmethod
    def _encode_string(data: str):
        return ffi.new('char[]', data.encode())

    @staticmethod
    def _encode_int(data: int):
        return ffi.cast('int', data)

    @staticmethod
    def _decode_string(data) -> str:
        output = ffi.string(data).decode()
        lib.FreeCString(data)
        return output

    @classmethod
    def new_jwk(cls, size: int = 2048, _id: str = None) -> str:
        params = [cls._encode_int(size)]
        if _id:
            params.append(cls._encode_string(_id))
        else:
            params.append(ffi.NULL)
        result = lib.NewJWK(*params)
        return cls._decode_string(result)

    @classmethod
    def jwk_to_pem(cls, jwk: str) -> str:
        param = cls._encode_string(jwk)
        result = lib.JWKToPEM(param)
        return cls._decode_string(result)

    @classmethod
    def pem_to_jwk(cls, pem: str) -> str:
        param = cls._encode_string(pem)
        result = lib.PEMToJWK(param)
        return cls._decode_string(result)

    @classmethod
    def parse_jwk_and_sign(cls, key: str, data: str) -> str:
        params = [cls._encode_string(key), cls._encode_string(data)]
        result = lib.ParseJWKAndSign(*params)
        return cls._decode_string(result)

    @classmethod
    def parse_pem_and_sign(cls, key: str, data: str) -> str:
        params = [cls._encode_string(key), cls._encode_string(data)]
        result = lib.ParsePEMAndSign(*params)
        return cls._decode_string(result)

    @classmethod
    @timed
    def example_go(cls, n: int) -> None:
        param = cls._encode_int(n)
        lib.ExampleGo(param)
