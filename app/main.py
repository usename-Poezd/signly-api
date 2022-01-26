import numpy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.core.models.sign import SignModel
from app.handler.api import api


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    # For cold start
    SignModel().predict(numpy.zeros((1, 30, 1662)))

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app
app = get_application()


app.include_router(api.api_router, prefix="/api")
