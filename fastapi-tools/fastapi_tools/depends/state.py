from typing import Annotated, Type

from fastapi import Depends, Request


def read_request_state(key: str, _type: Type):
    def dependency(request: Request) -> _type:
        return getattr(request.state, key, None)
    return Annotated[_type, Depends(dependency)]


def load_extra(key: str, _type: Type):
    """load shared object from fastapi root"""
    def dependency(request: Request) -> _type:
        return request.app.extra[key]
    return Annotated[_type, Depends(dependency)]


def load_extras(keys: list[str], types: list[Type]) -> tuple:
    # TODO: make params optional to allow ordered dict mapping
    # example 1: LoadSettings = load_extras(keys=['settings'], types=[Settings])
    # example 2: LoadSettings = load_extras(OrderedDict[('settings', Settings)])
    return tuple(load_extra(key, _type) for key, _type in zip(keys, types))
