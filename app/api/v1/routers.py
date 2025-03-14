from fastapi import APIRouter

from app.api.v1.endpoints import api_keys, auth, users

router = APIRouter()

router.include_router(api_keys.router)
router.include_router(auth.router)
router.include_router(users.router)
