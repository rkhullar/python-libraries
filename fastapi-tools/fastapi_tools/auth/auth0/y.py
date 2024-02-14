from typing import Annotated
from fastapi import Security, Request, APIRouter


def build_helpers(auth_scheme, IdentityToken):

    ReadAccessToken = Annotated[str, Security(auth_scheme)]

    def require_auth():
        def dependency(request: Request, access_token: ReadAccessToken) -> str:
            request.state.auth_data = decode_jwt(access_token)
            return access_token
        return Security(dependency)

    def create_router() -> APIRouter:
        return APIRouter(dependencies=[require_auth()])

    async def read_identity_token(access_token: ReadAccessToken) -> IdentityToken:
        data = await auth_scheme.read_user_info(access_token)
        return IdentityToken.model_validate(data)

    ReadIdentityToken = Annotated[IdentityToken, Security(read_identity_token)]

    return ReadAccessToken, require_auth, create_router, ReadIdentityToken
