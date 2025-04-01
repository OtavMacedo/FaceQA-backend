from datetime import datetime

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.registry import table_registry


@table_registry.mapped_as_dataclass
class CreditTransaction:
    __tablename__ = 'credit_transactions'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False, init=False
    )
    user: Mapped['User'] = relationship('User', back_populates='transactions')  # noqa: F821 # type: ignore
    amount: Mapped[int] = mapped_column(nullable=False)
    transaction_type: Mapped[str] = mapped_column(
        Enum('purchase', 'usage', 'adjustment', name='transaction_type_enum'),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
