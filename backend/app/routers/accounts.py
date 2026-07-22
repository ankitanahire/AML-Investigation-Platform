import random

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.accounts import Account
from app.models.user import User
from app.schemas.accounts import (
    AccountCreate,
    AccountResponse
)
from app.auth.auth import verify_token

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


def generate_account_number():
    return str(random.randint(1000000000, 9999999999))


@router.post("/", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db)
):

    account_number = generate_account_number()

    while db.query(Account).filter(
        Account.account_number == account_number
    ).first():
        account_number = generate_account_number()

    new_account = Account(
        account_number=account_number,
        account_type=account.account_type,
        balance=0,
        user_id=current_user.id
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account