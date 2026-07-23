from sqlalchemy.orm import Session

from app.models.accounts import Account
from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(db: Session, transaction: Transaction):
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_id(
        db: Session,
        transaction_id: int
    ):
        return (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

    @staticmethod
    def get_account_by_number(
        db: Session,
        account_number: str
    ):
        return (
            db.query(Account)
            .filter(Account.account_number == account_number)
            .first()
        )

    @staticmethod
    def get_sender_account(
        db: Session,
        account_number: str,
        user_id: int
    ):
        return (
            db.query(Account)
            .filter(
                Account.account_number == account_number,
                Account.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_transactions(
        db: Session,
        account_ids: list[int],
        page: int,
        limit: int,
        transaction_type: str | None = None
    ):

        query = db.query(Transaction).filter(
            (Transaction.sender_account.in_(account_ids)) |
            (Transaction.receiver_account.in_(account_ids))
        )

        if transaction_type:
            query = query.filter(
                Transaction.transaction_type == transaction_type
            )

        return (
            query
            .order_by(Transaction.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )