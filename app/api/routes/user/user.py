from fastapi import APIRouter, Depends

from app.repositories.user.user_repository import UserRepository
from app.schemas.user.user_schemas import UserSchema

router = APIRouter()


@router.post('/create_user')
async def create_user_route(
    user: UserSchema, user_repo: UserRepository = Depends()
):
    created_user = await user_repo.create_user(user)
    return created_user
