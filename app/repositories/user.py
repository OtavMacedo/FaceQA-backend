from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.database.session import get_session
from app.models.user import User
from app.schemas.user import UserSchema


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, user: UserSchema) -> User:
        db_user = User(
            email=user.email, hashed_password=get_password_hash(user.password)
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user

    async def read_by_email(self, email: str) -> User:
        db_user = await self.session.scalar(
            Select(User).where(User.email == email)
        )
        return db_user
