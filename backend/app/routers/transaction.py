from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.auth import verify_token

from app.models.user import User
from app.models.accounts import Account
from app.models.transaction import Transaction

from app.schemas.transaction import (
    TransferRequest,
    TransactionResponse,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/transfer")
def transfer_money(
    transfer: TransferRequest,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    sender = db.query(Account).filter(
        Account.account_number == transfer.sender_account_number,
        Account.user_id == current_user.id
    ).first()

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender account not found"
        )

    receiver = db.query(Account).filter(
        Account.account_number == transfer.receiver_account_number
    ).first()

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver account not found"
        )

    if transfer.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    if sender.balance < transfer.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

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


@router.get("/", response_model=list[TransactionResponse])
def transaction_history(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    accounts = db.query(Account).filter(
        Account.user_id == current_user.id
    ).all()

    account_ids = [account.id for account in accounts]

    transactions = db.query(Transaction).filter(
        (Transaction.sender_account.in_(account_ids)) |
        (Transaction.receiver_account.in_(account_ids))
    ).order_by(Transaction.created_at.desc()).all()

    return transactions