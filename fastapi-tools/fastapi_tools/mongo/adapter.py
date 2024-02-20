from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache, cached_property
from typing import Generic, Type

from pymongo import MongoClient
from pymongo.database import Collection, Database

from .document import DocumentType


@dataclass(frozen=True)
class MongoAdapter(Generic[DocumentType]):
    model_type: Type[DocumentType]
    mongo_client: MongoClient
    collection_name: str
    database_name: str = 'default'

    @cached_property
    def database(self) -> Database:
        return self.mongo_client.get_database(self.database_name)

    @cached_property
    def collection(self) -> Collection:
        return self.database.get_collection(self.collection_name)

    def iter_docs(self, filter: dict = None) -> Iterator[DocumentType]:
        for doc in self.collection.find(filter=filter):
            yield self.model_type.from_pymongo(doc)

    def find_one(self, filter: dict) -> DocumentType | None:
        if doc := self.collection.find_one(filter):
            return self.model_type.from_pymongo(doc)


@dataclass(frozen=True)
class MongoAdapterCache:
    mongo_client: MongoClient
    default_database: str = 'default'

    @cache
    def database(self, name: str = None) -> Database:
        return self.mongo_client.get_database(name or self.default_database)

    @cache
    def collection(self, collection: str, database: str = None) -> Collection:
        return self.database(name=database or self.default_database).get_collection(collection)

    @cache
    def adapter(self, collection: str, database: str = None, model_type: Type[DocumentType] = None) -> MongoAdapter[DocumentType]:
        return MongoAdapter(model_type=model_type, mongo_client=self.mongo_client, collection_name=collection, database_name=database or self.default_database)
