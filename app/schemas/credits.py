from pydantic import BaseModel


class CreditPurchaseAmount(BaseModel):
    amount: int


class CreditTransaction(BaseModel):
    amount: int
    transaction_type: str
    user: str
