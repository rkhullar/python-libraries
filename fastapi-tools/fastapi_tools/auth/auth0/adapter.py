from typing import Annotated
from fastapi import Security, Request, APIRouter
from ...util import decode_jwt
from .bearer import Auth0CodeBearer
from typing import Type
from pydantic import BaseModel


def build_depends(auth_scheme: Auth0CodeBearer, identity_token_type: Type[BaseModel]) -> dict:

    ReadAccessToken = Annotated[str, Security(auth_scheme)]

    def require_auth():
        def dependency(request: Request, access_token: ReadAccessToken) -> str:
            request.state.auth_data = decode_jwt(access_token)
            return access_token
        return Security(dependency)

    def create_router() -> APIRouter:
        return APIRouter(dependencies=[require_auth()])

    async def read_identity_token(access_token: ReadAccessToken) -> identity_token_type:
        data = await auth_scheme.read_user_info(access_token)
        return identity_token_type.model_validate(data)

    ReadIdentityToken = Annotated[identity_token_type, Security(read_identity_token)]

    return dict(
        ReadAccessToken=ReadAccessToken,
        ReadIdentityToken=ReadIdentityToken,
        require_auth=require_auth,
        create_router=create_router
    )
