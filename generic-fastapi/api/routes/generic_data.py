import json

import pymongo
from fastapi import HTTPException, status
from fastapi_tools.depends import int_query, read_query_param
from fastapi_tools.mongo import get_or_404
from fastapi_tools.schema.crud import (DeleteResponse, PaginationMetadata,
                                       PaginationResponse, UpdateResponse)

from ..depends import GetUser, atlas, create_router
from ..model.generic_data import GenericData
from ..schema.generic_data import GenericDataCreate, GenericDataUpdate
from ..util import build_filter_params

router = create_router()
GenericDataAdapter = atlas(name='generic_data', model=GenericData)


@router.post('', response_model=GenericData)
async def create_data(user: GetUser, adapter: GenericDataAdapter, create_object: GenericDataCreate):
    to_insert = create_object.to_pymongo(user_id=user.id)
    response = adapter.collection.insert_one(to_insert)
    return await read_data(user=user, adapter=adapter, _id=str(response.inserted_id))


@router.get('/{_id}', response_model=GenericData)
async def read_data(user: GetUser, adapter: GenericDataAdapter, _id: str):
    model_object = get_or_404(collection=adapter.collection, model_type=GenericData, _id=_id)
    if model_object.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return model_object


@router.get('', response_model=PaginationResponse[GenericData])
async def list_data(
        user: GetUser, adapter: GenericDataAdapter,
        limit: int_query(ge=1, le=100) = 100, offset: int_query(ge=0) = 0,
        _type: read_query_param(key='type', required=False, escape=False) = ...,
        _filter: read_query_param(key='filter', required=False, escape=False) = ...,
):
    filter_parts = [{'user_id': user.id}]
    if value := _type:
        filter_parts.append({'type': value})
    if value := _filter:
        try:
            value_data = json.loads(value)
        except json.JSONDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid json')
        filter_parts.append(value_data)
    filter_params = build_filter_params(filter_parts)

    total_count: int = adapter.collection.count_documents(filter_params)
    has_more: bool = offset + limit < total_count
    cursor = adapter.collection.find(filter_params).sort('created', pymongo.DESCENDING).skip(offset).limit(limit)
    result = [GenericData.from_pymongo(doc) for doc in cursor]
    return PaginationResponse(
        data=result,
        metadata=PaginationMetadata(
            count=len(result), total_count=total_count, has_more=has_more,
            limit=limit, offset=offset, extra={'filter': str(filter_params)}
        )
    )


@router.put('/{_id}', response_model=UpdateResponse[GenericData])
async def update_data(user: GetUser, adapter: GenericDataAdapter, _id: str, update_object: GenericDataUpdate):
    model_object = await read_data(user=user, adapter=adapter, _id=_id)

    to_update = dict()
    for key in ['type']:
        if value := getattr(update_object, key):
            to_update[key] = value

    if value := update_object.data:
        to_update['data'] = value.model_dump()

    update_params = dict(
        filter={'_id': model_object.id},
        update={'$set': to_update},
        return_document=pymongo.ReturnDocument.AFTER
    )

    result: dict = adapter.collection.find_one_and_update(**update_params)
    return GenericData(
        id=model_object.id,
        created=model_object.created,
        user_id=model_object.user_id,
        type=result['type'],
        data=result['data']
    )


@router.delete('/{_id}', response_model=DeleteResponse[GenericData])
async def delete_data(user: GetUser, adapter: GenericDataAdapter, _id: str):
    model_object = await read_data(user=user, adapter=adapter, _id=_id)
    response = adapter.collection.delete_one({'_id': model_object.id})
    return DeleteResponse(data=model_object, acknowledged=response.acknowledged)
