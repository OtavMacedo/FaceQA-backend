from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.user import UserRepository
from app.schemas.user import UserPublic, UserSchema

router = APIRouter()


@router.post(
    '/users', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
async def create_user(
    user: UserSchema, user_repository: UserRepository = Depends(UserRepository)
):
    db_user = await user_repository.read_by_email(user.email)

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists'
        )
    db_user = await user_repository.create(user)
    return db_user


# @router.post(
#     '/users', status_code=HTTPStatus.OK, response_model=UserPublic
# )
# async def update_user(

# )
