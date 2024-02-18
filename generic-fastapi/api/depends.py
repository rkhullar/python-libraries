from fastapi_tools.auth import build_auth_depends
from fastapi_tools.auth.auth0 import Auth0CodeBearer, Auth0IdentityToken
from fastapi_tools.depends import load_extra, read_request_state

from .config import Settings

LoadSettings = load_extra(key='settings', _type=Settings)

settings = Settings()
auth_scheme = Auth0CodeBearer(domain=settings.auth0_host)
auth_depends = build_auth_depends(auth_scheme=auth_scheme, identity_token_type=Auth0IdentityToken, with_scopes=True)
require_auth, create_router, require_scopes, allowed_scopes = auth_depends.methods
ReadAccessToken, ReadIdentityToken, ReadAuthData = auth_depends.annotations
