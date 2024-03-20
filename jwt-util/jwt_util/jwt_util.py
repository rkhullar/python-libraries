import base64
import json
from typing import Literal

from .wrapper import ExtensionAdapter

KeyFormat = Literal['jwk', 'pem']


def _b64_json_dumps(data: dict, sort: bool = False) -> str:
    json_data = json.dumps(data, separators=(',', ':'), sort_keys=sort)
    return _b64_enc(json_data)


def _b64_enc(data: str) -> str:
    return base64.b64encode(data.encode()).decode().rstrip('=')


signers = {
    'jwk': ExtensionAdapter.parse_jwk_and_sign,
    'pem': ExtensionAdapter.parse_pem_and_sign
}


def encode(payload: dict, key: str, mode: KeyFormat, headers: dict = None) -> str:
    headers = dict(headers or dict())
    headers['alg'] = 'RS256'
    headers['typ'] = 'JWT'
    header_data = _b64_json_dumps(headers, sort=True)
    payload_data = _b64_json_dumps(payload)
    header_payload_data = f'{header_data}.{payload_data}'
    signature_data = signers[mode](key, header_payload_data)
    return f'{header_payload_data}.{signature_data}'
