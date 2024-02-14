from fastapi import Request, Depends
from typing import Type, Annotated


def read_request_state(key: str, _type: Type):
    def dependency(request: Request) -> _type:
        return getattr(request.state, key, None)
    return Annotated[_type, Depends(dependency)]


def load_extra(key: str, _type: Type):
    """load shared object from fastapi root"""
    def dependency(request: Request) -> _type:
        return request.app.extra[key]
    return Annotated[_type, Depends(dependency)]
