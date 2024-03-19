import base64
from typing import Literal
from .wrapper import ExtensionAdapter
import json

KeyFormat = Literal['jwk', 'pem']


def _b64_json_dumps(data: dict, sort: bool = False) -> str:
    json_data = json.dumps(data, separators=(',', ':'), sort_keys=sort)
    return _b64_enc(json_data)


def _b64_enc(data: str) -> str:
    return base64.b64encode(data.encode()).decode().rstrip('=')


def encode(payload: dict, key: str, mode: KeyFormat = 'jwk', headers: dict = None) -> str:
    headers = dict(headers or dict())
    headers['alg'] = 'RS256'
    headers['typ'] = 'JWT'
    return _b64_json_dumps(headers, sort=True)
