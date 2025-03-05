from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_hash
from app.database.session import get_session
from app.models.refresh_token import RefreshToken
from app.models.user import User


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(
        self, token: str, expires_at: datetime, user: User
    ) -> RefreshToken:
        new_token = RefreshToken(
            token=get_hash(token), expires_at=expires_at, user=user
        )
        self.session.add(new_token)
        await self.session.commit()
        await self.session.refresh(new_token)
