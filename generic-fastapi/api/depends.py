from .config import Settings
from fastapi_tools.depends import load_extra, read_request_state
from fastapi_tools.auth.auth0 import Auth0CodeBearer, build_depends, Auth0IdentityToken

LoadSettings = load_extra(key='settings', _type=Settings)
ReadAuthData = read_request_state(key='auth_data', _type=dict)

settings = Settings()
auth_scheme = Auth0CodeBearer(domain=settings.auth0_host)
auth_depends = build_depends(auth_scheme=auth_scheme, identity_token_type=Auth0IdentityToken)
require_auth, create_router, ReadAccessToken, ReadIdentityToken = auth_depends
