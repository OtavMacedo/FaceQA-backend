from pydantic import BaseModel


class CreditPurchase(BaseModel):
    amount: int
