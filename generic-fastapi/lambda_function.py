from api.config import Settings
from api.factory import create_app
from fastapi import FastAPI
from mangum import Mangum

settings: Settings = Settings()
app: FastAPI = create_app(settings)
lambda_handler: Mangum = Mangum(app)
