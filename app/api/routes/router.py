from fastapi import APIRouter

from ..routes.user.user import router as user_router

router = APIRouter()

router.include_router(user_router)
