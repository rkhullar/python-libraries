from collections.abc import Iterable
from typing import Annotated, Type

from fastapi import Depends, HTTPException, Request, Security, status
from pydantic import BaseModel

from ...depends import build_access_decorator, read_request_state
from ...router import APIRouter
from ...util import decode_jwt
from .bearer import AbstractAuthCodeBearer
from .types import AbstractUser, DynamicAuthDepends


def build_auth_depends(auth_scheme: AbstractAuthCodeBearer, identity_token_type: Type[BaseModel], user_type: Type[AbstractUser],
                       with_scopes: bool = False, with_groups: bool = False, groups_field: str = 'groups') -> DynamicAuthDepends:

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

    async def load_user(request: Request, auth_data: ReadAuthData, identity_token: ReadIdentityToken) -> user_type:
        return await user_type.from_auth(auth_data=auth_data, identity_token=identity_token, context=request.app.extra)

    GetUser = Annotated[user_type, Depends(load_user)]

    def require_scopes(scopes: Iterable[str]):
        def dependency(auth_data: ReadAuthData):
            allowed_scopes: set[str] = set(scopes)
            granted_scopes: list[str] = auth_data.get('scope', '').split(' ') or auth_data.get('scp', [])
            if not allowed_scopes.intersection(granted_scopes):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return Annotated[None, Security(dependency)]

    def require_groups(groups: Iterable[str]):
        def dependency(user: GetUser):
            allowed_groups: set[str] = set(groups)
            granted_groups: set[str] = getattr(user, groups_field)
            if not allowed_groups.intersection(granted_groups):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return Annotated[None, Security(dependency)]

    return DynamicAuthDepends(
        require_auth=require_auth,
        create_router=create_router,
        ReadAccessToken=ReadAccessToken,
        ReadIdentityToken=ReadIdentityToken,
        ReadAuthData=ReadAuthData,
        GetUser=GetUser,
        require_scopes=require_scopes if with_scopes else None,
        allowed_scopes=build_access_decorator(require_scopes) if with_scopes else None,
        require_groups=require_groups if with_groups else None,
        allowed_groups=build_access_decorator(require_groups) if with_groups else None
    )
