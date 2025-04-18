from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.api_key import APIKey
from app.models.user import User


class ApiKeyRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, hashed_key: str, user: User, suffix: str):
        db_key = APIKey(hashed_key=hashed_key, user=user, suffix=suffix)
        self.session.add(db_key)
        await self.session.commit()

    async def read_by_suffix(self, api_suffix):
        db_key: APIKey = await self.session.scalar(
            Select(APIKey).where(APIKey.suffix == api_suffix)
        )
        return db_key
