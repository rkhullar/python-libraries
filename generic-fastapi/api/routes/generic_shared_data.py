import json

import pymongo
from fastapi import HTTPException, status
from fastapi_tools.depends import int_query, read_query_param
from fastapi_tools.schema.crud import PaginationMetadata, PaginationResponse
from fastapi_tools.mongo import get_or_404

from ..depends import atlas, create_router
from ..model.generic_data import GenericSharedData
from ..util import build_filter_params

router = create_router()
GenericSharedDataAdapter = atlas(name='generic_shared_data', model=GenericSharedData)


@router.get('/{_id}', response_model=GenericSharedData)
async def read_data(adapter: GenericSharedDataAdapter, _id: str):
    return get_or_404(collection=adapter.collection, model_type=GenericSharedData, _id=_id)


@router.get('', response_model=PaginationResponse[GenericSharedData])
async def list_data(
        adapter: GenericSharedDataAdapter,
        limit: int_query(ge=1, le=100) = 100, offset: int_query(ge=0) = 0,
        _type: read_query_param(key='type', required=False, escape=False) = ...,
        _filter: read_query_param(key='filter', required=False, escape=False) = ...,
):
    filter_parts = list()
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
    result = [GenericSharedData.from_pymongo(doc) for doc in cursor]
    return PaginationResponse(
        data=result,
        metadata=PaginationMetadata(
            count=len(result), total_count=total_count, has_more=has_more,
            limit=limit, offset=offset, extra={'filter': str(filter_params)}
        )
    )
