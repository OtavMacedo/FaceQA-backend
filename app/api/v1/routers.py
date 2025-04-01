from fastapi import APIRouter

from app.api.v1.endpoints import api_keys, auth, credits, face_qa, user

router = APIRouter()

router.include_router(api_keys.router)
router.include_router(auth.router)
router.include_router(credits.router)
router.include_router(face_qa.router)
router.include_router(user.router)
