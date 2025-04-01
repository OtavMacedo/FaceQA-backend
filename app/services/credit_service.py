from http import HTTPStatus

from fastapi import Depends, HTTPException

from app.models.user import User
from app.repositories.credit_transaction import CreditTransactionRepository
from app.repositories.user import UserRepository
from app.schemas.credits import CreditPurchaseTransaction


class CreditService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        credit_repo: CreditTransactionRepository = Depends(),
    ):
        self.user_repo = user_repo
        self.credit_repo = credit_repo

    async def add_credits(self, amount: int, user: User):
        transaction_type = 'purchase'

        if amount < 1:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='The minimum purchase amount is 1 credit.',
            )

        await self.credit_repo.create_transaction(
            user=user, amount=amount, transaction_type=transaction_type
        )
        await self.user_repo.update_credits_me(user, amount)

        return CreditPurchaseTransaction(
            amount=amount,
            transaction_type=transaction_type,
            user=user.email
        )
