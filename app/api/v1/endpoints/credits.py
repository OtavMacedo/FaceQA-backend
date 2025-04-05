from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.credits import CreditPurchaseAmount, CreditTransaction
from app.services.credit_service import CreditService

router = APIRouter(prefix='/credits', tags=['APICredits'])


@router.post(
    '/purchase',
    status_code=HTTPStatus.OK,
    response_model=CreditTransaction,
)
async def credit_purchase(
    body: CreditPurchaseAmount,
    current_user: User = Depends(get_current_user),
    credit_service: CreditService = Depends(),
):
    transaction = await credit_service.add_credits(
        amount=body.amount, user=current_user
    )
    return transaction
