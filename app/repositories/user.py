from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_hash
from app.database.session import get_session
from app.models.user import User
from app.schemas.user import UserSchema


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, user: UserSchema) -> User:
        new_user = User(
            email=user.email, hashed_password=get_hash(user.password)
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def read_by_email(self, email: str) -> User:
        db_user = await self.session.scalar(
            Select(User).where(User.email == email)
        )

        return db_user

    async def delete_me(self, current_user: User):
        db_user = self.read_by_email(current_user.email)
        if not db_user:
            return False

        await self.session.delete(current_user)
        await self.session.commit()

        return True

    async def update_password_me(self, current_user: User, new_password: str):
        db_user = self.read_by_email(current_user.email)
        if not db_user:
            return False

        current_user.hashed_password = get_hash(new_password)
        await self.session.commit()

        return True
