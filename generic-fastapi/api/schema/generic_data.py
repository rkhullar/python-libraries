import datetime as dt
from typing import Optional, Self

from bson import ObjectId
from fastapi_tools.schema import NonBlankStr, ensure_update
from pydantic import BaseModel, model_validator

from ..model.generic_data import PrimitiveOrCollection


class GenericDataCreate(BaseModel):
    type: NonBlankStr
    data: PrimitiveOrCollection

    def to_pymongo(self, user_id: Optional[ObjectId], shared: bool = False) -> dict:
        result = dict(created=dt.datetime.now(dt.UTC), type=self.type, data=self.data.model_dump())
        if not shared:
            result['user_id'] = user_id
        return result


class GenericDataUpdate(BaseModel):
    type: Optional[NonBlankStr] = None
    data: Optional[PrimitiveOrCollection] = None

    @model_validator(mode='after')
    def check_update(self) -> Self:
        ensure_update(update_object=self, fields=['type', 'data'])
        return self
