from typing import Self

from fastapi_tools.auth import AbstractUser
from fastapi_tools.auth.auth0 import Auth0IdentityToken


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
