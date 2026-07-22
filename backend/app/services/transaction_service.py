from sqlalchemy.orm import Session

from app.models.accounts import Account
from app.models.transaction import Transaction

from app.schemas.transaction import TransferRequest

from app.exceptions.transaction_exceptions import (
    SenderAccountNotFoundException,
    ReceiverAccountNotFoundException,
    InsufficientBalanceException,
)


class TransactionService:

    @staticmethod
    def transfer_money(
        db: Session,
        user_id: int,
        transfer: TransferRequest
    ):

        sender = db.query(Account).filter(
            Account.account_number == transfer.sender_account_number,
            Account.user_id == user_id
        ).first()

        if sender is None:
            raise SenderAccountNotFoundException()

        receiver = db.query(Account).filter(
            Account.account_number == transfer.receiver_account_number
        ).first()

        if receiver is None:
            raise ReceiverAccountNotFoundException()

        if sender.balance < transfer.amount:
            raise InsufficientBalanceException()

        sender.balance -= transfer.amount
        receiver.balance += transfer.amount

        new_transaction = Transaction(
            sender_account=sender.id,
            receiver_account=receiver.id,
            amount=transfer.amount,
            transaction_type="Transfer"
        )

        db.add(new_transaction)

        db.commit()

        db.refresh(new_transaction)

        return {
            "message": "Transfer Successful",
            "transaction_id": new_transaction.id
        }

    @staticmethod
    def transaction_history(
        db: Session,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        transaction_type: str | None = None
    ):

        accounts = db.query(Account).filter(
            Account.user_id == user_id
        ).all()

        account_ids = [account.id for account in accounts]

        query = db.query(Transaction).filter(
            (Transaction.sender_account.in_(account_ids)) |
            (Transaction.receiver_account.in_(account_ids))
        )

        if transaction_type:
            query = query.filter(
                Transaction.transaction_type == transaction_type
            )

        transactions = (
            query
            .order_by(Transaction.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return transactions