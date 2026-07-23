from sqlalchemy.orm import Session

from app.models.accounts import Account


class AccountRepository:

    @staticmethod
    def create(
        db: Session,
        account: Account
    ):
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_by_account_number(
        db: Session,
        account_number: str
    ):
        return (
            db.query(Account)
            .filter(Account.account_number == account_number)
            .first()
        )

    @staticmethod
    def get_by_account_number_and_user(
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
    def get_all_by_user(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Account)
            .filter(Account.user_id == user_id)
            .all()
        )

    @staticmethod
    def search_account(
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
    def refresh(
        db: Session,
        account: Account
    ):
        db.refresh(account)