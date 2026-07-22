import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.accounts import Account
from app.models.transaction import Transaction

from app.schemas.accounts import (
    AccountCreate,
    DepositRequest,
    WithdrawRequest,
)


class AccountService:

    @staticmethod
    def generate_account_number():
        return str(random.randint(1000000000, 9999999999))

    @staticmethod
    def create_account(
        db: Session,
        user_id: int,
        account: AccountCreate
    ):
        account_number = AccountService.generate_account_number()

        while db.query(Account).filter(
            Account.account_number == account_number
        ).first():
            account_number = AccountService.generate_account_number()

        new_account = Account(
            account_number=account_number,
            account_type=account.account_type,
            balance=0,
            user_id=user_id
        )

        db.add(new_account)
        db.commit()
        db.refresh(new_account)

        return new_account

    @staticmethod
    def get_accounts(
        db: Session,
        user_id: int
    ):
        return db.query(Account).filter(
            Account.user_id == user_id
        ).all()

    @staticmethod
    def deposit_money(
        db: Session,
        user_id: int,
        deposit: DepositRequest
    ):
        account = db.query(Account).filter(
            Account.account_number == deposit.account_number,
            Account.user_id == user_id
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

    @staticmethod
    def withdraw_money(
        db: Session,
        user_id: int,
        withdraw: WithdrawRequest
    ):
        account = db.query(Account).filter(
            Account.account_number == withdraw.account_number,
            Account.user_id == user_id
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

    @staticmethod
    def check_balance(
        db: Session,
        user_id: int,
        account_number: str
    ):
        account = db.query(Account).filter(
            Account.account_number == account_number,
            Account.user_id == user_id
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