from typing import Annotated, Type
from collections.abc import Iterable
from fastapi import Request, Security, HTTPException, status
from pydantic import BaseModel

from ...util import decode_jwt
from .bearer import AbstractAuthCodeBearer
from .types import DynamicAuthDepends
from ...depends import read_request_state, build_access_decorator
from ...router import APIRouter


def build_auth_depends(auth_scheme: AbstractAuthCodeBearer, identity_token_type: Type[BaseModel],
                       with_scopes: bool = False, with_groups: bool = False) -> DynamicAuthDepends:

    ReadAccessToken = Annotated[str, Security(auth_scheme)]
    ReadAuthData = read_request_state(key='auth_data', _type=dict)

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

    def require_scopes(scopes: Iterable[str]):
        def dependency(auth_data: ReadAuthData) -> str:
            allowed_scopes: set[str] = set(scopes)
            granted_scopes: list[str] = auth_data.get('scope', '').split(' ') or auth_data.get('scp', [])
            if not allowed_scopes.intersection(granted_scopes):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return Annotated[None, Security(dependency)]

    return DynamicAuthDepends(
        require_auth=require_auth,
        create_router=create_router,
        ReadAccessToken=ReadAccessToken,
        ReadIdentityToken=ReadIdentityToken,
        ReadAuthData=ReadAuthData,
        require_scopes=require_scopes if with_scopes else None,
        allowed_scopes=build_access_decorator(require_scopes) if with_scopes else None,
    )
