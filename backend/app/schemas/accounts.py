from decimal import Decimal
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class AccountType(str, Enum):
    Savings = "Savings"
    Current = "Current"


class AccountCreate(BaseModel):
    account_type: AccountType


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: str
    balance: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccountList(BaseModel):
    accounts: list[AccountResponse]


class DepositRequest(BaseModel):
    account_number: str
    amount: Decimal = Field(gt=0)


class WithdrawRequest(BaseModel):
    account_number: str
    amount: Decimal = Field(gt=0)