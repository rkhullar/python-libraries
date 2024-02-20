from __future__ import annotations

from typing import Generic, Type, TypeVar

from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import BaseModel, RootModel
from pymongo.database import Collection

from .client import is_valid_object_id
from .object_id import PydanticObjectId


class Document(BaseModel):
    id: PydanticObjectId | str

    @classmethod
    def from_pymongo(cls, doc: dict) -> DocumentType:
        _id = doc.pop('_id')
        return cls(id=_id, **doc)

    @property
    def object_ref(self) -> ObjectRef[DocumentType]:
        return ObjectRef[DocumentType](__root__=self.id)


DocumentType = TypeVar('DocumentType', bound=Document)


class ObjectRef(RootModel[DocumentType], Generic[DocumentType]):
    root: PydanticObjectId | str

    @property
    def id(self):
        # TODO: try field alias
        return self.root


def get_or_404(collection: Collection, model_type: Type[DocumentType], _id: str, cast: bool = True) -> DocumentType:
    if cast and not is_valid_object_id(_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid object id')
    key = ObjectId(_id) if cast else _id
    if doc := collection.find_one({'_id': key}):
        return model_type.from_pymongo(doc)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
