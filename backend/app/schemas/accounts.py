from decimal import Decimal
from typing import List

from pydantic import BaseModel


class AccountCreate(BaseModel):
    account_type: str


class DepositRequest(BaseModel):
    account_number: str
    amount: Decimal


class WithdrawRequest(BaseModel):
    account_number: str
    amount: Decimal


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: str
    balance: Decimal

    class Config:
        from_attributes = True


class AccountList(BaseModel):
    accounts: List[AccountResponse]