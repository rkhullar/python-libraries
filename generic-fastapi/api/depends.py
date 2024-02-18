from fastapi_tools.auth import AbstractUser, build_auth_depends
from fastapi_tools.auth.auth0 import Auth0CodeBearer, Auth0IdentityToken
from fastapi_tools.depends import load_extra, read_request_state
from fastapi_tools.mongo import build_atlas_depends

from .config import Auth0Settings, Settings
from .schema.user import User

LoadSettings = load_extra(key='settings', _type=Settings)
auth_settings = Auth0Settings()
auth_scheme = Auth0CodeBearer(domain=auth_settings.auth0_host)
auth_depends = build_auth_depends(auth_scheme=auth_scheme, identity_token_type=Auth0IdentityToken, user_type=User, with_scopes=True)
require_auth, create_router, require_scopes, allowed_scopes = auth_depends.methods
ReadAccessToken, ReadIdentityToken, ReadAuthData, GetUser = auth_depends.annotations
atlas = build_atlas_depends(mongo_adapter_key='atlas')
