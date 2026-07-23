import random
from sqlalchemy.orm import Session

from app.models.accounts import Account
from app.models.transaction import Transaction

from app.schemas.accounts import (
    AccountCreate,
    DepositRequest,
    WithdrawRequest,
)

from app.exceptions.account_exceptions import (
    AccountNotFoundException,
    InsufficientBalanceException,
)

from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository


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

        while AccountRepository.get_by_account_number(
            db,
            account_number
        ):
            account_number = AccountService.generate_account_number()

        new_account = Account(
            account_number=account_number,
            account_type=account.account_type,
            balance=0,
            user_id=user_id
        )

        return AccountRepository.create(
            db,
            new_account
        )

    @staticmethod
    def get_accounts(
        db: Session,
        user_id: int
    ):

        return AccountRepository.get_all_by_user(
            db,
            user_id
        )

    @staticmethod
    def search_account(
        db: Session,
        user_id: int,
        account_number: str
    ):

        account = AccountRepository.search_account(
            db,
            account_number,
            user_id
        )

        if account is None:
            raise AccountNotFoundException()

        return account

    @staticmethod
    def deposit_money(
        db: Session,
        user_id: int,
        deposit: DepositRequest
    ):

        account = AccountRepository.get_by_account_number_and_user(
            db,
            deposit.account_number,
            user_id
        )

        if account is None:
            raise AccountNotFoundException()

        account.balance += deposit.amount

        transaction = Transaction(
            sender_account=None,
            receiver_account=account.id,
            amount=deposit.amount,
            transaction_type="Deposit"
        )

        TransactionRepository.create(
            db,
            transaction
        )

        AccountRepository.refresh(db, account)

        return account

    @staticmethod
    def withdraw_money(
        db: Session,
        user_id: int,
        withdraw: WithdrawRequest
    ):

        account = AccountRepository.get_by_account_number_and_user(
            db,
            withdraw.account_number,
            user_id
        )

        if account is None:
            raise AccountNotFoundException()

        if account.balance < withdraw.amount:
            raise InsufficientBalanceException()

        account.balance -= withdraw.amount

        transaction = Transaction(
            sender_account=account.id,
            receiver_account=None,
            amount=withdraw.amount,
            transaction_type="Withdraw"
        )

        TransactionRepository.create(
            db,
            transaction
        )

        AccountRepository.refresh(db, account)

        return account

    @staticmethod
    def check_balance(
        db: Session,
        user_id: int,
        account_number: str
    ):

        account = AccountRepository.get_by_account_number_and_user(
            db,
            account_number,
            user_id
        )

        if account is None:
            raise AccountNotFoundException()

        return {
            "account_number": account.account_number,
            "balance": account.balance
        }