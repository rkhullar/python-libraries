import base64
import json


def b64_enc(data: str) -> str:
    return base64.b64encode(data.encode()).decode().rstrip('=')


def _padding_size(data: str, n: int) -> int:
    remainder = len(data) % n
    return (n - remainder) % n


def b64_dec(data: str) -> str:
    padding_size = _padding_size(data, n=4)
    data += padding_size * '='
    return base64.b64decode(data.encode()).decode()


def b64_json_dumps(data: dict, sort: bool = False) -> str:
    json_data = json.dumps(data, separators=(',', ':'), sort_keys=sort)
    return b64_enc(json_data)


def b64_json_loads(data: str):
    return json.loads(b64_dec(data))
