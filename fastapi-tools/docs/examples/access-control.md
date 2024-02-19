### Example Access Control
```python
# schema/user.py

from fastapi_tools.auth import AbstractUser
from fastapi_tools.auth.auth0 import Auth0IdentityToken
from typing import Self

class User(AbstractUser):
    name: str
    email: str
    auth0_id: str
    
    @classmethod
    async def from_auth(cls, auth_data: dict, identity_token: Auth0IdentityToken, context: dict) -> Self:
        # NOTE: context would contain adapter to allow upsert into database
        return cls.model_validate({
            'name': identity_token.name,
            'email': identity_token.email,
            'auth0_id': auth_data['sub']
        })
```

```python
# depends.py

from fastapi_tools.auth import build_auth_depends
from fastapi_tools.auth.auth0 import Auth0CodeBearer, Auth0IdentityToken
from .schema.user import User

auth_scheme = Auth0CodeBearer(domain='your_auth0_domain')
auth_depends = build_auth_depends(auth_scheme=auth_scheme, identity_token_type=Auth0IdentityToken, user_type=User, with_scopes=True)
require_auth, create_router, require_scopes, allowed_scopes = auth_depends.methods
ReadAccessToken, ReadIdentityToken, ReadAuthData, GetUser = auth_depends.annotations
```

```python
# routes/example.py

from ..depends import create_router, allowed_scopes
from fastapi_tools.schema import NonBlankStr
from pydantic import BaseModel

router = create_router()

class CreateMessage(BaseModel):
    message: NonBlankStr

messages: list[str] = list()
    
@allowed_scopes('message:admin')
@router.post('')
async def create_message(create_object: CreateMessage):
    # NOTE: simplified example without database integration or response  model
    messages.append(create_object.message)
    return dict(message=messages[-1])
```
