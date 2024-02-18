import re
from typing import Annotated, TypeVar

from fastapi import Depends, HTTPException, Query, status

T = TypeVar('T')


def annotated_query(_type, **kwargs):
    return Annotated[_type, Query(**kwargs)]


def int_query(**kwargs):
    return annotated_query(int, **kwargs)


ReadQueryParamList = Annotated[set[T], Query()]


def read_query_param(key: str, required: bool = True, escape: bool = True, **kwargs):
    """read query param with regex escape"""
    kwargs['alias'] = key

    def dependency(value: Annotated[str, Query(**kwargs)] = None):
        if value:
            return re.escape(value) if escape else value
        elif required:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'missing query param: {key}')

    return Annotated[str, Depends(dependency)]
