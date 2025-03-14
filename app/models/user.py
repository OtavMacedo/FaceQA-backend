from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.registry import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    api_keys: Mapped[list['APIKey']] = relationship(  # noqa: F821 # type: ignore
        'APIKey',
        back_populates='user',
        cascade='all, delete',
        default_factory=list,
    )
    # refresh_tokens: Mapped[list['RefreshToken']] = relationship(
    #     'RefreshToken',
    #     back_populates='user',
    #     default_factory=list,
    #     cascade='all, delete',
    # )
