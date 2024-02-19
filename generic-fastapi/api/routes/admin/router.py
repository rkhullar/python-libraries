from fastapi_tools import APIRouter

from . import generic_shared_data

router = APIRouter()
router.include_router(generic_shared_data.router, prefix='/shared-data', tags=['shared-data'])
