from sqlalchemy.exc import SQLAlchemyError

from app.core.database.session import AsyncSessionLocal


async def get_session():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        print(f'Session error {e}')
