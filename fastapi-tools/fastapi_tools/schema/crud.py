from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, RootModel

T = TypeVar('T')


class CreateResponse(RootModel[T], Generic[T]):
    root: T


class ReadResponse(RootModel[T], Generic[T]):
    root: T


class UpdateResponse(RootModel[T], Generic[T]):
    root: T


class DeleteResponse(BaseModel, Generic[T]):
    data: T
    acknowledged: bool


# TODO: switch parent to typed dict; use NotRequired over Optional?
class Metadata(BaseModel):
    count: int
    extra: Optional[dict] = None


class ListResponse(BaseModel, Generic[T]):
    data: list[T]
    metadata: Optional[Metadata] = None


class PaginationMetadata(Metadata):
    count: Optional[int] = None
    total_count: int
    has_more: bool
    limit: int
    offset: int
    filter: Optional[dict] = None


class PaginationResponse(BaseModel, Generic[T]):
    data: list[T]
    metadata: PaginationMetadata
