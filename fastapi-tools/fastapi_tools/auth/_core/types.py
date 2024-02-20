from abc import abstractmethod
from collections.abc import Iterable
from typing import Callable, NamedTuple, Optional, Self, Type

from pydantic import BaseModel


class AbstractUser(BaseModel):

    @classmethod
    @abstractmethod
    async def from_auth(cls, auth_data: dict, identity_token: BaseModel, context: dict) -> Self:
        # NOTE: context is from request.app.extra
        pass


class DynamicAuthDepends(NamedTuple):
    require_auth: Callable
    create_router: Callable
    ReadAccessToken: Type
    ReadIdentityToken: Type
    ReadAuthData: Type
    GetUser: Type
    require_scopes: Optional[Callable]
    allowed_scopes: Optional[Callable]
    require_groups: Optional[Callable]
    allowed_groups: Optional[Callable]

    def unpack(self, fields: Iterable[str]) -> tuple:
        return tuple(filter(None, (getattr(self, field) for field in fields)))

    @property
    def methods(self) -> tuple[Callable]:
        return self.unpack(fields=['require_auth', 'create_router', 'require_scopes', 'allowed_scopes', 'require_groups', 'allowed_groups'])

    @property
    def annotations(self) -> tuple[Type]:
        return self.unpack(fields=['ReadAccessToken', 'ReadIdentityToken', 'ReadAuthData', 'GetUser'])
