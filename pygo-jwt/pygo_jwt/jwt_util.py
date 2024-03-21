from typing import Literal
from .wrapper import ExtensionAdapter
from .b64_util import b64_json_dumps, b64_json_loads


KeyFormat = Literal['jwk', 'pem']


signers = {
    'jwk': ExtensionAdapter.parse_jwk_and_sign,
    'pem': ExtensionAdapter.parse_pem_and_sign
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
    signature_data = signers[mode](key, header_payload_data)
    return f'{header_payload_data}.{signature_data}'


def decode(token: str) -> dict:
    pass
