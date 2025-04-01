from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.credit_transaction import CreditTransaction
from app.models.user import User


class CreditTransactionRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_transaction(
        self,
        user: User,
        amount: int,
        transaction_type: str,  # Validar se tem como definir um conjunto especifico de transaction_type  # noqa: E501
    ):
        new_transaction = CreditTransaction(
            user=user, amount=amount, transaction_type=transaction_type
        )
        self.session.add(new_transaction)
        await self.session.commit()
