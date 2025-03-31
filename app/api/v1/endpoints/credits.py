from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.credits import CreditPurchase
from app.schemas.message import Message

router = APIRouter(prefix='/credits', tags=['APICredits'])


@router.post('/purchase', status_code=HTTPStatus.OK, response_model=Message)
async def credit_purchase(
    body: CreditPurchase, current_user: User = Depends(get_current_user)
):
    # Process payment
    amount = body.amount
    current_user.api_credits += amount

    return Message(message=f'{amount} credits added to your account.')
