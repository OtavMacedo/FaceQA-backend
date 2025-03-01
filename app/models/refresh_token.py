from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.registry import table_registry
from app.models.user import User


@table_registry.mapped_as_dataclass
class RefreshToken:
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), init=False)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    expires_at: Mapped[datetime]
    user: Mapped['User'] = relationship(
        'User', back_populates='refresh_tokens'
    )
    revoked: Mapped[bool] = mapped_column(default=False)
