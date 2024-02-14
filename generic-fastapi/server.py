from api.config import Settings
from api.factory import create_app
from fastapi import FastAPI

settings: Settings = Settings()
app: FastAPI = create_app(settings)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', host=settings.service_host, port=settings.service_port, reload=settings.reload_fastapi)
