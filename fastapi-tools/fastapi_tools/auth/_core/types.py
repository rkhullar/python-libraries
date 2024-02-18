from typing import Callable, NamedTuple, Type, Optional
from collections.abc import Iterable


class DynamicAuthDepends(NamedTuple):
    require_auth: Callable
    create_router: Callable
    ReadAccessToken: Type
    ReadIdentityToken: Type
    ReadAuthData: Type
    require_scopes: Optional[Callable]
    allowed_scopes: Optional[Callable]

    def unpack(self, fields: Iterable[str]) -> tuple:
        return tuple(filter(None, (getattr(self, field) for field in fields)))

    @property
    def methods(self) -> tuple[Callable]:
        return self.unpack(fields=['require_auth', 'create_router', 'require_scopes', 'allowed_scopes'])

    @property
    def annotations(self) -> tuple[Type]:
        return self.unpack(fields=['ReadAccessToken', 'ReadIdentityToken', 'ReadAuthData'])
