from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.api_key import APIKey
from app.models.user import User
from app.services.api_key_service import get_api_key_hash


class APIKeyRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, api_key: str, user: User, suffix: str):
        db_key = APIKey(
            hashed_key=get_api_key_hash(api_key), user=user, suffix=suffix
        )
        self.session.add(db_key)
        await self.session.commit()
        await self.session.refresh(db_key)

        return db_key

    async def read_by_suffix(self, api_suffix):
        db_key: APIKey = await self.session.scalar(
            Select(APIKey).where(APIKey.suffix == api_suffix)
        )
        return db_key
