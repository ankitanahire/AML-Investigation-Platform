from fastapi import HTTPException


class AccountNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Account not found"
        )


class InvalidDepositAmountException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Deposit amount must be greater than zero"
        )


class InvalidWithdrawalAmountException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Withdrawal amount must be greater than zero"
        )


class InsufficientBalanceException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Insufficient balance"
        )