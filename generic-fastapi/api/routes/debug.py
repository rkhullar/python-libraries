# from ..depends import ReadAuth0IdentityToken, ReadAuthData, create_router
# from ..schema.login import Auth0IdentityToken

# router = create_router()


# @router.get('/auth-state', response_model=dict)
# def debug_auth_state(auth_data: ReadAuthData):
#     return {'auth_data': auth_data}
#
#
# @router.get('/user-info', response_model=Auth0IdentityToken)
# def debug_user_info(token: ReadAuth0IdentityToken):
#     return token


from fastapi import APIRouter

router = APIRouter()


@router.get('/auth-state')
def debug_auth_state():
    return 'tbd'
