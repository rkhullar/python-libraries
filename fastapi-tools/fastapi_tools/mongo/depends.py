from fastapi import Request, Depends
from typing import Type, Annotated
from .document import DocumentType
from pymongo.database import Collection
from .adapter import MongoAdapterCache, MongoAdapter


def build_atlas_depends(mongo_adapter_key: str = 'atlas'):
    def atlas(name: str, database: str = 'default', model: Type[DocumentType] = None):
        # TODO: rename and split into helpers for loading adapter and collection?
        def dependency(request: Request) -> MongoAdapter[DocumentType] | Collection:
            mongo_adapter_cache: MongoAdapterCache = request.app.extra[mongo_adapter_key]
            if model:
                return mongo_adapter_cache.adapter(collection=name, database=database, model_type=model)
            else:
                return mongo_adapter_cache.collection(collection=name, database=database)
        return_type = MongoAdapter[DocumentType] if model else Collection
        return Annotated[return_type, Depends(dependency)]
    return atlas
