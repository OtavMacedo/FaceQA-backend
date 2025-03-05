import secrets
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_settings import settings
from app.database.session import get_session
from app.models.user import User

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def get_hash(password: str):
    return pwd_context.hash(password)


def verify_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired'
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    payload = verify_access_token(token)

    email = payload.get('sub')
    if not email:
        raise credentials_exception

    user = await session.scalar(Select(User).where(User.email == email))
    if not user:
        raise credentials_exception

    return user


def create_refresh_token():
    token = secrets.token_hex(32)
    expire = datetime.now(tz=timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    return {'token': token, 'expires_at': expire}
