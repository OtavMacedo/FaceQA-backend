from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.message import Message
from app.schemas.user import (
    UpdatePassword,
    UserPublic,
    UserSchema,
    UserUpdateMe,
)

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
    return await user_repository.create(user)


@router.patch(
    '/me/email', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def update_email_me(
    user_in: UserUpdateMe,
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_current_user),
):
    if user_in.email == current_user.email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='New email cannot be the same as the current one',
        )
    db_user = await user_repository.read_by_email(user_in.email)

    if db_user and db_user.id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User with this email already exists',
        )
    return await user_repository.update_email_me(current_user, user_in.email)


@router.patch(
    '/me/password', status_code=HTTPStatus.OK, response_model=Message
)
async def update_password_me(
    body: UpdatePassword,
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_current_user),
):
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='New password cannot be the same as the current one',
        )
    if not verify_password(
        body.current_password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect password'
        )

    await user_repository.update_password_me(current_user, body.new_password)

    return Message(message='Password updated successfully')


@router.delete('/me', status_code=HTTPStatus.OK, response_model=Message)
async def delete_me(
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_current_user),
):
    await user_repository.delete_me(current_user)

    return Message(message='User deleted successfully')
