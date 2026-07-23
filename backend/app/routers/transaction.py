from fastapi import APIRouter, Depends, HTTPException, Query
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
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    transaction_type: str | None = None,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return TransactionService.transaction_history(
        db,
        current_user.id,
        page,
        limit,
        transaction_type
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def search_transaction(
    transaction_id: int,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    transaction = TransactionService.search_transaction(
        db,
        transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction