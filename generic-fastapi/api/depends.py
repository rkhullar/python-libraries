from typing import Self

from fastapi_tools.auth import AbstractUser, build_auth_depends
from fastapi_tools.auth.auth0 import Auth0CodeBearer, Auth0IdentityToken
from fastapi_tools.depends import load_extra, read_request_state

from .config import Settings

LoadSettings = load_extra(key='settings', _type=Settings)


class User(AbstractUser):
    name: str
    email: str
    auth0_id: str

    @classmethod
    async def load(cls, auth_data: dict, identity_token: Auth0IdentityToken, context: dict) -> Self:
        return cls.model_validate({
            'name': identity_token.name,
            'email': identity_token.email,
            'auth0_id': auth_data['sub']
        })


settings = Settings()
auth_scheme = Auth0CodeBearer(domain=settings.auth0_host)
auth_depends = build_auth_depends(auth_scheme=auth_scheme, identity_token_type=Auth0IdentityToken, user_type=User, with_scopes=True)
require_auth, create_router, require_scopes, allowed_scopes = auth_depends.methods
ReadAccessToken, ReadIdentityToken, ReadAuthData, GetUser = auth_depends.annotations
