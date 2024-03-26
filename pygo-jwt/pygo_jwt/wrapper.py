from dataclasses import dataclass
from _rsa_util import ffi, lib
from .time_util import timed
from .errors import CorePyGoJWTError
from .wrapper_util import build_base_adapter


BaseExtensionAdapter = build_base_adapter(ffi, lib)


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
        return cls._decode_string(result)

    @classmethod
    def jwk_to_pem(cls, jwk: str) -> str:
        param = cls._encode_string(jwk)
        result = lib.JWKToPEM(param)
        return cls._decode_string(result)

    @classmethod
    def pem_to_jwk(cls, pem: str, _id: str = None) -> str:
        params = [cls._encode_string(pem)]
        if _id:
            params.append(cls._encode_string(_id))
        else:
            params.append(ffi.NULL)
        result = lib.PEMToJWK(*params)
        return cls._decode_string(result)

    @classmethod
    def extract_public_jwk(cls, key: str) -> str:
        param = cls._encode_string(key)
        result = lib.ExtractPublicJWK(param)
        return cls._decode_string(result)

    @classmethod
    def extract_public_pem(cls, key: str) -> str:
        param = cls._encode_string(key)
        result = lib.ExtractPublicPEM(param)
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
    def parse_public_jwk_and_verify(cls, key: str, data: str, signature: str) -> bool:
        params = [cls._encode_string(key), cls._encode_string(data), cls._encode_string(signature)]
        return lib.ParsePublicJWKAndVerify(*params)

    @classmethod
    def parse_public_pem_and_verify(cls, key: str, data: str, signature: str) -> bool:
        params = [cls._encode_string(key), cls._encode_string(data), cls._encode_string(signature)]
        return lib.ParsePublicPEMAndVerify(*params)

    @classmethod
    @timed
    def example_go(cls, n: int) -> None:
        param = cls._encode_int(n)
        lib.ExampleGo(param)

    @classmethod
    def maybe_error(cls, n: int):
        param = cls._encode_int(n)
        result = lib.MaybeError(param)
        # TODO: create helper; deallocate struct
        if res := result.data:
            output = ffi.string(res).decode()
            return output
        elif err := result.error:
            error_message = ffi.string(err).decode()
            raise CorePyGoJWTError(error_message)
