from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.app_settings import settings


def create_db_engine() -> AsyncEngine:
    try:
        async_engine: AsyncEngine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI
        )
    except SQLAlchemyError:
        # Log the error
        pass

    return async_engine


async_engine = create_db_engine()
