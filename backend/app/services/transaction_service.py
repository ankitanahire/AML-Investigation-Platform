from sqlalchemy.orm import Session

from app.models.accounts import Account

from app.schemas.transaction import TransferRequest

from app.exceptions.transaction_exceptions import (
    SenderAccountNotFoundException,
    ReceiverAccountNotFoundException,
    InsufficientBalanceException,
)

from app.repositories.transaction_repository import TransactionRepository


class TransactionService:

    @staticmethod
    def transfer_money(
        db: Session,
        user_id: int,
        transfer: TransferRequest
    ):

        sender = TransactionRepository.get_sender_account(
            db,
            transfer.sender_account_number,
            user_id
        )

        if sender is None:
            raise SenderAccountNotFoundException()

        receiver = TransactionRepository.get_account_by_number(
            db,
            transfer.receiver_account_number
        )

        if receiver is None:
            raise ReceiverAccountNotFoundException()

        if sender.balance < transfer.amount:
            raise InsufficientBalanceException()

        sender.balance -= transfer.amount
        receiver.balance += transfer.amount

        transaction = TransactionRepository.create(
            db,
            __import__(
                "app.models.transaction",
                fromlist=["Transaction"]
            ).Transaction(
                sender_account=sender.id,
                receiver_account=receiver.id,
                amount=transfer.amount,
                transaction_type="Transfer"
            )
        )

        return {
            "message": "Transfer Successful",
            "transaction_id": transaction.id
        }

    @staticmethod
    def transaction_history(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        transaction_type: str | None = None
    ):

        accounts = (
            db.query(Account)
            .filter(Account.user_id == user_id)
            .all()
        )

        account_ids = [a.id for a in accounts]

        return TransactionRepository.get_transactions(
            db,
            account_ids,
            page,
            limit,
            transaction_type
        )

    @staticmethod
    def search_transaction(
        db: Session,
        transaction_id: int
    ):

        return TransactionRepository.get_by_id(
            db,
            transaction_id
        )