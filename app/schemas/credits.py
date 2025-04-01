from pydantic import BaseModel


class CreditPurchaseAmount(BaseModel):
    amount: int


class CreditPurchaseTransaction(BaseModel):
    amount: int
    transaction_type: str
    user: str
