from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.auth import verify_token

from app.models.user import User

from app.schemas.transaction import (
    TransferRequest,
    TransactionResponse,
)

from app.services.transaction_service import TransactionService

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

    return TransactionService.transfer_money(
        db,
        current_user.id,
        transfer
    )


@router.get("/", response_model=list[TransactionResponse])
def transaction_history(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return TransactionService.transaction_history(
        db,
        current_user.id
    )