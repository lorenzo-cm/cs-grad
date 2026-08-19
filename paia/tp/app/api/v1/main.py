from fastapi import APIRouter

from app.api.v1.admin_buildings import router as admin_buildings_router
from app.api.v1.webhooks.chatwoot import router as chatwoot_router

router = APIRouter()

router.include_router(chatwoot_router, tags=["chatwoot"])
router.include_router(admin_buildings_router)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "Health Check: v1"}
