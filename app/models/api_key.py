from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.registry import table_registry


@table_registry.mapped_as_dataclass
class APIKey:
    __tablename__ = 'api_keys'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False, init=False
    )
    user: Mapped['User'] = relationship('User', back_populates='api_keys')  # noqa: F821 # type: ignore
    hashed_key: Mapped[str] = mapped_column(unique=True, nullable=False)
    suffix: Mapped[str] = mapped_column(nullable=False)
    last_request: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, init=False, default=None
    )
    request_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
