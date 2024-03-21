from typing import Literal

from .b64_util import b64_json_dumps, b64_json_loads
from .errors import InvalidSignatureError, TokenDecodeError
from .wrapper import ExtensionAdapter

KeyFormat = Literal['jwk', 'pem']


signers = {
    'jwk': ExtensionAdapter.parse_jwk_and_sign,
    'pem': ExtensionAdapter.parse_pem_and_sign
}

verifiers = {
    'jwk': ExtensionAdapter.parse_public_jwk_and_verify,
    'pem': ExtensionAdapter.parse_public_pem_and_verify
}


def new_jwk(size: int = 2048, _id: str = None) -> str:
    return ExtensionAdapter.new_jwk(size=size, _id=_id)


def jwk_to_pem(jwk: str) -> str:
    return ExtensionAdapter.jwk_to_pem(jwk)


def pem_to_jwk(pem: str) -> str:
    return ExtensionAdapter.pem_to_jwk(pem)


def extract_public_jwk(key: str) -> str:
    return ExtensionAdapter.extract_public_jwk(key)


def extract_public_pem(key: str) -> str:
    return ExtensionAdapter.extract_public_pem(key)


def encode(payload: dict, key: str, mode: KeyFormat, headers: dict = None) -> str:
    headers = dict(headers or dict())
    headers['alg'] = 'RS256'
    headers['typ'] = 'JWT'
    header_data = b64_json_dumps(headers, sort=True)
    payload_data = b64_json_dumps(payload)
    header_payload_data = f'{header_data}.{payload_data}'
    signature_data = signers[mode](key=key, data=header_payload_data)
    return f'{header_payload_data}.{signature_data}'


def decode(token: str, key: str, mode: KeyFormat, verify: bool = True) -> dict:
    parts = token.split('.')
    if len(parts) != 3:
        raise TokenDecodeError
    header, payload, signature = parts
    if verify:
        is_valid = verifiers[mode](key=key, data=f'{header}.{payload}', signature=signature)
        if not is_valid:
            raise InvalidSignatureError
    return b64_json_loads(payload)
