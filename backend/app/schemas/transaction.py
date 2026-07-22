from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TransferRequest(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    amount: Decimal = Field(gt=0)


class TransactionResponse(BaseModel):
    id: int
    sender_account: int | None
    receiver_account: int |None
    amount: Decimal
    transaction_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionFilter(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    transaction_type: Optional[str] = None