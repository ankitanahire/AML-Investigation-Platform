import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.accounts import Account
from app.models.user import User
from app.models.transaction import Transaction

from app.schemas.accounts import (
    AccountCreate,
    AccountResponse,
    AccountList,
    DepositRequest,
    WithdrawRequest,
)

from app.auth.auth import verify_token

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


def generate_account_number():
    return str(random.randint(1000000000, 9999999999))


@router.post("/", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    account_number = generate_account_number()

    while db.query(Account).filter(
        Account.account_number == account_number
    ).first():
        account_number = generate_account_number()

    new_account = Account(
        account_number=account_number,
        account_type=account.account_type,
        balance=0,
        user_id=current_user.id
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


@router.get("/", response_model=AccountList)
def view_my_accounts(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    accounts = db.query(Account).filter(
        Account.user_id == current_user.id
    ).all()

    return {"accounts": accounts}


@router.post("/deposit", response_model=AccountResponse)
def deposit_money(
    deposit: DepositRequest,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.account_number == deposit.account_number,
        Account.user_id == current_user.id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    if deposit.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Deposit amount must be greater than zero"
        )

    account.balance += deposit.amount

    transaction = Transaction(
        sender_account=None,
        receiver_account=account.id,
        amount=deposit.amount,
        transaction_type="Deposit"
    )

    db.add(transaction)

    db.commit()

    db.refresh(account)

    return account


@router.post("/withdraw", response_model=AccountResponse)
def withdraw_money(
    withdraw: WithdrawRequest,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.account_number == withdraw.account_number,
        Account.user_id == current_user.id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    if withdraw.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Withdrawal amount must be greater than zero"
        )

    if account.balance < withdraw.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    account.balance -= withdraw.amount

    transaction = Transaction(
        sender_account=account.id,
        receiver_account=None,
        amount=withdraw.amount,
        transaction_type="Withdraw"
    )

    db.add(transaction)

    db.commit()

    db.refresh(account)

    return account


@router.get("/balance")
def check_balance(
    account_number: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.account_number == account_number,
        Account.user_id == current_user.id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "account_number": account.account_number,
        "balance": account.balance
    }