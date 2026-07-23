from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.accounts import Account
from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(
        db: Session,
        transaction: Transaction
    ):
        """
        Add transaction to current DB session.
        Service layer will commit.
        """
        db.add(transaction)
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
        page: int = 1,
        limit: int = 10,
        transaction_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        sort: str = "newest"
    ):

        query = db.query(Transaction).filter(
            or_(
                Transaction.sender_account.in_(account_ids),
                Transaction.receiver_account.in_(account_ids)
            )
        )

        if transaction_type:
            query = query.filter(
                Transaction.transaction_type == transaction_type
            )

        if start_date:
            query = query.filter(
                Transaction.created_at >= start_date
            )

        if end_date:
            query = query.filter(
                Transaction.created_at <= end_date
            )

        if sort == "oldest":
            query = query.order_by(
                Transaction.created_at.asc()
            )

        elif sort == "amount_asc":
            query = query.order_by(
                Transaction.amount.asc()
            )

        elif sort == "amount_desc":
            query = query.order_by(
                Transaction.amount.desc()
            )

        else:
            query = query.order_by(
                Transaction.created_at.desc()
            )

        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_account_statement(
        db: Session,
        account_id: int
    ):
        return (
            db.query(Transaction)
            .filter(
                or_(
                    Transaction.sender_account == account_id,
                    Transaction.receiver_account == account_id
                )
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

    @staticmethod
    def get_daily_transfer_total(
        db: Session,
        account_id: int,
        start_of_day: datetime,
        end_of_day: datetime
    ):
        """
        Used later by AML Rule:
        Daily transfer limit.
        """

        return (
            db.query(Transaction)
            .filter(
                Transaction.sender_account == account_id,
                Transaction.transaction_type == "Transfer",
                Transaction.created_at >= start_of_day,
                Transaction.created_at <= end_of_day
            )
            .all()
        )

    @staticmethod
    def get_recent_transfers(
        db: Session,
        account_id: int,
        since: datetime
    ):
        """
        Used later by AML:
        Multiple transfers within 1 minute.
        """

        return (
            db.query(Transaction)
            .filter(
                Transaction.sender_account == account_id,
                Transaction.transaction_type == "Transfer",
                Transaction.created_at >= since
            )
            .all()
        )