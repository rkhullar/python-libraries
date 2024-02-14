from fastapi import FastAPI
from .config import Settings
# from .model.adapter import MongoAdapterCache
from .router import router as api_router
from fastapi_tools.metrics import add_process_time_header


def create_app(settings: Settings, test: bool = False) -> FastAPI:
    app = FastAPI(
        settings=settings,
        swagger_ui_init_oauth={
            'clientId': settings.auth0_client_id,
            'usePkceWithAuthorizationCodeGrant': True,
            'scopes': ' '.join(settings.auth0_scopes),
            'additionalQueryStringParams': {'audience': settings.auth0_audience}
        }
    )
    app.include_router(api_router)  # prefix='/api'
    # mongo_client = build_atlas_client(atlas_host=settings.atlas_host, local_mode=settings.local_mode)
    # app.extra['atlas'] = MongoAdapterCache(mongo_client=mongo_client)

    #app.add_middleware(add_process_time_header)
    app.middleware('http')(add_process_time_header)

    return app
