from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.api_key import APIKey
from app.models.user import User
from app.services.api_key_service import get_api_key_hash


class APIKeyRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, api_key: str, user: User):
        db_key = APIKey(hashed_key=get_api_key_hash(api_key), user=user)
        self.session.add(db_key)
        await self.session.commit()
        await self.session.refresh(db_key)

        return db_key
