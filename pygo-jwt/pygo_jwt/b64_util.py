import base64
import json


def b64_enc(data: str) -> str:
    return base64.b64encode(data.encode()).decode().rstrip('=')


def b64_dec(data: str) -> str:
    pass


def b64_json_dumps(data: dict, sort: bool = False) -> str:
    json_data = json.dumps(data, separators=(',', ':'), sort_keys=sort)
    return b64_enc(json_data)


def b64_json_loads(data: str):
    pass
