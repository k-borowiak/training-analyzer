from fastapi import APIRouter

from .health import router as health_router
from .me import router as me_router
from .strava import router as strava_router

router = APIRouter()
router.include_router(health_router)
router.include_router(me_router)
router.include_router(strava_router)