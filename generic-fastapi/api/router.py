from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from .routes import debug, generic_data, generic_shared_data, profile
from .routes.admin import router as admin

router = APIRouter()
router.include_router(debug.router, prefix='/debug', tags=['debug'])
router.include_router(profile.router, prefix='/profile', tags=['profile'])
router.include_router(generic_data.router, prefix='/data', tags=['data'])
router.include_router(generic_shared_data.router, prefix='/shared-data', tags=['shared-data'])
router.include_router(admin.router, prefix='/admin', tags=['admin'])


@router.get('/', response_class=RedirectResponse, status_code=status.HTTP_302_FOUND, include_in_schema=False)
async def index():
    return 'docs'
