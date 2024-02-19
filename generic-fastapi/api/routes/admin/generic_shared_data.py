import pymongo
from fastapi_tools.schema.crud import DeleteResponse, UpdateResponse

from ...depends import allowed_scopes, atlas, create_router
from ...model.generic_data import GenericSharedData
from ...schema.generic_data import GenericDataCreate, GenericDataUpdate
from ..generic_shared_data import read_data

router = create_router()
GenericSharedDataAdapter = atlas(name='generic_shared_data', model=GenericSharedData)


@allowed_scopes('shared-data:admin')
@router.post('', response_model=GenericSharedData)
async def create_data(adapter: GenericSharedDataAdapter, create_object: GenericDataCreate):
    to_insert = create_object.to_pymongo(shared=True, user_id=None)
    response = adapter.collection.insert_one(to_insert)
    return await read_data(adapter=adapter, _id=str(response.inserted_id))


@allowed_scopes('shared-data:admin')
@router.delete('/{_id}', response_model=DeleteResponse[GenericSharedData])
async def delete_data(adapter: GenericSharedDataAdapter, _id: str):
    model_object = await read_data(adapter=adapter, _id=_id)
    response = adapter.collection.delete_one({'_id': model_object.id})
    return DeleteResponse(data=model_object, acknowledged=response.acknowledged)


@allowed_scopes('shared-data:admin')
@router.put('/{_id}', response_model=UpdateResponse[GenericSharedData])
async def update_data(adapter: GenericSharedDataAdapter, _id: str, update_object: GenericDataUpdate):
    model_object = await read_data(adapter=adapter, _id=_id)

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
    return GenericSharedData(
        id=model_object.id,
        created=model_object.created,
        type=result['type'],
        data=result['data']
    )
