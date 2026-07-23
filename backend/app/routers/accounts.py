from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.auth import verify_token

from app.models.user import User

from app.schemas.accounts import (
    AccountCreate,
    AccountResponse,
    AccountList,
    DepositRequest,
    WithdrawRequest,
)

from app.services.account_service import AccountService

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return AccountService.create_account(
        db,
        current_user.id,
        account
    )


@router.get("/", response_model=AccountList)
def view_my_accounts(
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    accounts = AccountService.get_accounts(
        db,
        current_user.id
    )

    return {"accounts": accounts}


# -----------------------------
# NEW - Search Account Number
# -----------------------------
@router.get("/search/{account_number}", response_model=AccountResponse)
def search_account(
    account_number: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return AccountService.search_account(
        db,
        current_user.id,
        account_number
    )


@router.post("/deposit", response_model=AccountResponse)
def deposit_money(
    deposit: DepositRequest,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return AccountService.deposit_money(
        db,
        current_user.id,
        deposit
    )


@router.post("/withdraw", response_model=AccountResponse)
def withdraw_money(
    withdraw: WithdrawRequest,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return AccountService.withdraw_money(
        db,
        current_user.id,
        withdraw
    )


@router.get("/balance")
def check_balance(
    account_number: str,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return AccountService.check_balance(
        db,
        current_user.id,
        account_number
    )