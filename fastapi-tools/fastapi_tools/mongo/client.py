import os
from contextlib import contextmanager

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo import MongoClient


def build_atlas_client(atlas_host: str, local_mode: bool = False) -> MongoClient:
    # https://www.mongodb.com/docs/atlas/manage-connections-aws-lambda/
    # https://www.mongodb.com/docs/manual/reference/connection-string/#mongodb-atlas-cluster
    mongo_client_url = f'mongodb+srv://{atlas_host}/?authSource=%24external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority'
    if local_mode:
        assert 'AWS_PROFILE' in os.environ
    return MongoClient(mongo_client_url, connect=True)


def is_valid_object_id(_id: str) -> bool:
    try:
        ObjectId(_id)
        return True
    except InvalidId:
        return False


@contextmanager
def start_atlas_transaction(mongo_client: MongoClient):
    with mongo_client.start_session() as session:
        with session.start_transaction():
            yield session
