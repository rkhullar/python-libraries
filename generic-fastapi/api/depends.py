from .config import Settings
from fastapi_tools.depends.x import load_extra, read_request_state

LoadSettings = load_extra(key='settings', _type=Settings)
ReadAuthData = read_request_state(key='auth_data', _type=dict)
