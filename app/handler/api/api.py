from fastapi import APIRouter

from app.handler.api.v1 import handler as v1_handler


api_router = APIRouter()
api_router.include_router(v1_handler.router, prefix="/v1", tags=["v1"])