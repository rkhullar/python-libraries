from fastapi_tools.auth.auth0 import Auth0IdentityToken

from ..depends import ReadAuthData, ReadIdentityToken, create_router

router = create_router()


@router.get('/auth-state', response_model=dict)
async def debug_auth_state(auth_data: ReadAuthData):
    return {'auth_data': auth_data}


@router.get('/user-info', response_model=Auth0IdentityToken)
async def debug_user_info(token: ReadIdentityToken):
    return token
