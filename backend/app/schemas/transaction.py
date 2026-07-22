from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class TransferRequest(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    amount: Decimal


class TransactionResponse(BaseModel):
    id: int
    sender_account: int | None
    receiver_account: int | None
    amount: Decimal
    transaction_type: str
    created_at: datetime

    class Config:
        from_attributes = True