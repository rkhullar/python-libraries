import base64
import json


def decode_jwt(token: str) -> dict:
    payload_b64 = token.split('.')[1]
    payload_json = base64.b64decode(payload_b64.encode() + b'==')
    return json.loads(payload_json)
