from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    create_access_token,
    verify_hash,
)
from app.repositories.user import UserRepository
from app.schemas.tokens import LoginToken

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login', status_code=HTTPStatus.OK, response_model=LoginToken)
async def login(
    user_repository: UserRepository = Depends(UserRepository),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_repository.read_by_email(form_data.username)
    if not user or not verify_hash(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token({'sub': form_data.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}
