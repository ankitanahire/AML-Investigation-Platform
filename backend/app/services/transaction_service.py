from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.accounts import Account
from app.models.transaction import Transaction

from app.schemas.transaction import TransferRequest

from app.exceptions.transaction_exceptions import (
    SenderAccountNotFoundException,
    ReceiverAccountNotFoundException,
    InsufficientBalanceException,
)

from app.repositories.transaction_repository import TransactionRepository
from app.services.aml_service import AMLService


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

        # -----------------------------------
        # Account Freeze Checks
        # -----------------------------------

        if sender.is_frozen:
            raise HTTPException(
                status_code=403,
                detail="Sender account is frozen"
            )

        if receiver.is_frozen:
            raise HTTPException(
                status_code=403,
                detail="Receiver account is frozen"
            )

        # -----------------------------------
        # Balance Check
        # -----------------------------------

        if sender.balance < transfer.amount:
            raise InsufficientBalanceException()

        # -----------------------------------
        # Transfer
        # -----------------------------------

        sender.balance -= transfer.amount
        receiver.balance += transfer.amount

        transaction = Transaction(
            sender_account=sender.id,
            receiver_account=receiver.id,
            amount=transfer.amount,
            transaction_type="Transfer"
        )

        transaction = TransactionRepository.create(
            db,
            transaction
        )

        db.flush()

        # -----------------------------------
        # AML Rules
        # -----------------------------------

        AMLService.run_rules(
            db=db,
            account_id=sender.id,
            transaction_id=transaction.id,
            amount=transfer.amount
        )

        db.commit()

        db.refresh(transaction)
        db.refresh(sender)
        db.refresh(receiver)

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