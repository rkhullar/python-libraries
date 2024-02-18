from fastapi_tools.auth.auth0 import Auth0IdentityToken

from ..depends import (GetUser, ReadAuthData, ReadIdentityToken, User,
                       create_router)

router = create_router()


@router.get('/auth-state', response_model=dict)
async def debug_auth_state(auth_data: ReadAuthData):
    return {'auth_data': auth_data}


@router.get('/user-info', response_model=Auth0IdentityToken)
async def debug_user_info(token: ReadIdentityToken):
    return token


@router.get('/test-user', response_model=User)
async def test_user(user: GetUser):
    return user
