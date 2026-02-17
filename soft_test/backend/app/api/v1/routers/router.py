from fastapi import APIRouter
from .wordle import wordle_router

router = APIRouter()

router.include_router(wordle_router, prefix="/wordle", tags=["wordle"])