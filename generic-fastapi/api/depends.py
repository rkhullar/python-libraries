from .config import Settings
from fastapi_tools.depends import load_extra, read_request_state
from fastapi_tools.auth.auth0 import Auth0CodeBearer, build_depends, Auth0IdentityToken

LoadSettings = load_extra(key='settings', _type=Settings)
ReadAuthData = read_request_state(key='auth_data', _type=dict)

settings = Settings()
auth_scheme = Auth0CodeBearer(domain=settings.auth0_host)
depends = build_depends(auth_scheme=auth_scheme, identity_token_type=Auth0IdentityToken)

create_router = depends['create_router']
require_auth = depends['require_auth']
ReadAccessToken = depends['ReadAccessToken']
ReadIdentityToken = depends['ReadIdentityToken']
