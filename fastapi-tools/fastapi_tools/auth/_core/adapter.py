from typing import Annotated, Type

from fastapi import APIRouter, Request, Security
from pydantic import BaseModel

from ...util import decode_jwt
from .types import DynamicAuthDepends
from .bearer import AbstractAuthCodeBearer


def build_auth_depends(auth_scheme: AbstractAuthCodeBearer, identity_token_type: Type[BaseModel]) -> DynamicAuthDepends:

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

    return DynamicAuthDepends(
        require_auth=require_auth,
        create_router=create_router,
        ReadAccessToken=ReadAccessToken,
        ReadIdentityToken=ReadIdentityToken
    )
