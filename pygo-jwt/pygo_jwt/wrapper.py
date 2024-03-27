from dataclasses import dataclass

from _rsa_util import ffi, lib

from pygo_tools_lib import FreeNamesDict, build_base_adapter

from .errors import CorePyGoJWTError
from .time_util import timed

BaseExtensionAdapter = build_base_adapter(ffi, lib, error_type=CorePyGoJWTError, free_names=FreeNamesDict(
    string='FreeString', string_with_error='FreeStringWithError', bool_with_error='FreeBoolWithError'
))


@dataclass
class ExtensionAdapter(BaseExtensionAdapter):

    @classmethod
    def new_jwk(cls, size: int = 2048, _id: str = None) -> str:
        params = [cls._encode_int(size)]
        if _id:
            params.append(cls._encode_string(_id))
        else:
            params.append(ffi.NULL)
        result = lib.NewJWK(*params)
        return cls._handle_string_with_error(result)

    @classmethod
    def jwk_to_pem(cls, jwk: str) -> str:
        param = cls._encode_string(jwk)
        result = lib.JWKToPEM(param)
        return cls._handle_string_with_error(result)

    @classmethod
    def pem_to_jwk(cls, pem: str, _id: str = None) -> str:
        params = [cls._encode_string(pem)]
        if _id:
            params.append(cls._encode_string(_id))
        else:
            params.append(ffi.NULL)
        result = lib.PEMToJWK(*params)
        return cls._handle_string_with_error(result)

    @classmethod
    def extract_public_jwk(cls, key: str) -> str:
        param = cls._encode_string(key)
        result = lib.ExtractPublicJWK(param)
        return cls._handle_string_with_error(result)

    @classmethod
    def extract_public_pem(cls, key: str) -> str:
        param = cls._encode_string(key)
        result = lib.ExtractPublicPEM(param)
        return cls._handle_string_with_error(result)

    @classmethod
    def parse_jwk_and_sign(cls, key: str, data: str) -> str:
        params = [cls._encode_string(key), cls._encode_string(data)]
        result = lib.ParseJWKAndSign(*params)
        return cls._handle_string_with_error(result)

    @classmethod
    def parse_pem_and_sign(cls, key: str, data: str) -> str:
        params = [cls._encode_string(key), cls._encode_string(data)]
        result = lib.ParsePEMAndSign(*params)
        return cls._handle_string_with_error(result)

    @classmethod
    def parse_public_jwk_and_verify(cls, key: str, data: str, signature: str) -> bool:
        params = [cls._encode_string(key), cls._encode_string(data), cls._encode_string(signature)]
        result = lib.ParsePublicJWKAndVerify(*params)
        return cls._handle_bool_with_error(result)

    @classmethod
    def parse_public_pem_and_verify(cls, key: str, data: str, signature: str) -> bool:
        params = [cls._encode_string(key), cls._encode_string(data), cls._encode_string(signature)]
        result = lib.ParsePublicPEMAndVerify(*params)
        return cls._handle_bool_with_error(result)

    @classmethod
    @timed
    def example_go(cls, n: int) -> None:
        param = cls._encode_int(n)
        lib.ExampleGo(param)

    @classmethod
    def maybe_error(cls, n: int) -> str:
        param = cls._encode_int(n)
        result = lib.MaybeError(param)
        return cls._handle_string_with_error(result)
