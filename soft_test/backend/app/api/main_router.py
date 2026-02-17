from fastapi import APIRouter

from .v1.routers.router import router

main_router = APIRouter()

main_router.include_router(router, prefix="/v1")
