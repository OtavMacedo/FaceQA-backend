from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.app_settings import settings

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,  # Desligar em prod
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:  # type: ignore
    async with AsyncSessionLocal() as session:
        yield session
