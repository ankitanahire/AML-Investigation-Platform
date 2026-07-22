from fastapi import HTTPException


class SenderAccountNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Sender account not found"
        )


class ReceiverAccountNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Receiver account not found"
        )


class InvalidTransferAmountException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Amount must be greater than zero"
        )


class InsufficientBalanceException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Insufficient balance"
        )