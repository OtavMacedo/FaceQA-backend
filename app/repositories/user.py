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

    async def create(self, user: UserSchema):
        new_user = User(
            email=user.email, hashed_password=get_password_hash(user.password)
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def read_by_email(self, email: str):
        db_user = await self.session.scalar(
            Select(User).where(User.email == email)
        )
        return db_user

    async def read_by_id(self, user_id: int):
        db_user = await self.session.scalar(
            Select(User).where(User.id == user_id)
        )
        return db_user

    async def delete_me(self, current_user: User):
        await self.session.delete(current_user)
        await self.session.commit()

    async def update_password_me(self, current_user: User, new_password: str):
        current_user.hashed_password = get_password_hash(new_password)
        await self.session.commit()

    async def update_email_me(self, current_user: User, new_email: str):
        current_user.email = new_email
        await self.session.commit()
        await self.session.refresh(current_user)

        return current_user

    async def update_credits_me(self, current_user: User, amount: int):
        current_user.api_credits += amount
        await self.session.commit()
