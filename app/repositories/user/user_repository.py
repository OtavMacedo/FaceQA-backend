from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_session
from app.models.user.user_model import User
from app.schemas.user.user_schemas import UserSchema


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user(self, user: UserSchema) -> User:
        db_user = User(email=user.email, hashed_password=user.password)

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user
