from __future__ import annotations
import datetime as dt
from typing import Union
from pydantic import Field, RootModel
from fastapi_tools.mongo import PydanticObjectId, Document

primitive_types = None, bool, int, float, str, dt.date, dt.datetime
PrimitiveValue = Union[primitive_types]


class PrimitiveOrCollection(RootModel):
    root: dict[str, PrimitiveOrCollection] | list[PrimitiveOrCollection] | PrimitiveValue
    # TODO: revisit class name


class GenericData(Document):
    created: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    user_id: PydanticObjectId
    type: str
    data: PrimitiveOrCollection


class GenericSharedData(Document):
    created: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    type: str
    data: PrimitiveOrCollection
