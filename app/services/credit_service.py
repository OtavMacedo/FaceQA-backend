from http import HTTPStatus

from fastapi import Depends, HTTPException

from app.models.user import User
from app.repositories.credit_transaction import CreditTransactionRepository
from app.repositories.user import UserRepository
from app.schemas.credits import CreditTransaction


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
                detail='Minimum amount to purchase is 1 credit',
            )

        await self.credit_repo.create_transaction(
            user=user, amount=amount, transaction_type=transaction_type
        )
        await self.user_repo.update_credits_me(
            current_user=user, amount=amount
        )

        return CreditTransaction(
            amount=amount, transaction_type=transaction_type, user=user.email
        )

    async def consume_credits(self, amount: int, user: User):
        transaction_type = 'usage'

        if amount < 1:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Minimum amount to spend is 1 credit',
            )

        if user.api_credits < amount:
            raise HTTPException(
                status_code=HTTPStatus.PAYMENT_REQUIRED,
                detail='Insufficient credits',
            )
        to_spend = -amount

        await self.credit_repo.create_transaction(
            user=user, amount=amount, transaction_type=transaction_type
        )
        await self.user_repo.update_credits_me(
            current_user=user, amount=to_spend
        )

        return CreditTransaction(
            amount=amount, transaction_type=transaction_type, user=user.email
        )
