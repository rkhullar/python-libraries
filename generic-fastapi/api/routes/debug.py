from ..depends import create_router, ReadAuthData, ReadIdentityToken
from fastapi_tools.auth.auth0 import Auth0IdentityToken

router = create_router()


@router.get('/auth-state', response_model=dict)
def debug_auth_state(auth_data: ReadAuthData):
    return {'auth_data': auth_data}


@router.get('/user-info', response_model=Auth0IdentityToken)
def debug_user_info(token: ReadIdentityToken):
    return token
