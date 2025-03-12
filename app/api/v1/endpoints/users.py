from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user, verify_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.message import Message
from app.schemas.user import UpdatePassword, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['User'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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


@router.delete('/me', status_code=HTTPStatus.OK, response_model=Message)
async def delete_me(
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_current_user),
):
    success = await user_repository.delete_me(current_user)

    if not success:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')

    return Message(message="User deleted successfully")


@router.patch(
    '/me/password', status_code=HTTPStatus.OK, response_model=Message
)
async def update_password_me(
    body: UpdatePassword,
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_current_user),
):
    if not verify_hash(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect password'
        )

    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='New password cannot be the same as the current one',
        )

    success = await user_repository.update_password_me(
        current_user, body.new_password
    )
    if not success:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')

    return Message(message='Password updated successfully')
