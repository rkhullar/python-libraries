from typing import Self

from fastapi_tools.auth import AbstractUser
from fastapi_tools.auth.auth0 import Auth0IdentityToken
from fastapi_tools.mongo import PydanticObjectId


class User(AbstractUser):
    id: PydanticObjectId
    name: str
    email: str
    auth0_id: str

    @classmethod
    async def from_auth(cls, auth_data: dict, identity_token: Auth0IdentityToken, context: dict) -> Self:
        users = context['users']
        if doc := users.find_one({'email': identity_token.email}):
            # TODO: check user attributes for updates?
            data = doc.model_dump()
            data['id'] = doc.id
            return cls.model_validate(data)
        else:
            to_insert = {
                'name': identity_token.name,
                'email': identity_token.email,
                'auth0_id': auth_data['sub']
            }
            response = users.collection.insert_one(to_insert)
            return cls(id=response.inserted_id, **to_insert)
