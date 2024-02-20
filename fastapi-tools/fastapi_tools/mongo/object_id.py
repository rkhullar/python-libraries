from typing import Annotated

from bson.objectid import ObjectId as BsonObjectId
from pydantic import GetPydanticSchema, PlainSerializer, WithJsonSchema
from pydantic_core import core_schema

PydanticObjectId = Annotated[
    BsonObjectId,
    GetPydanticSchema(lambda source_type, handler: core_schema.is_instance_schema(BsonObjectId)),
    PlainSerializer(lambda data: str(data), return_type=str),
    WithJsonSchema({'type': 'string', 'example': 'ObjectId()'})
]