from typing import Callable, NamedTuple, Type


class DynamicAuthDepends(NamedTuple):
    require_auth: Callable
    create_router: Callable
    ReadAccessToken: Type
    ReadIdentityToken: Type
