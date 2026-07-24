from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.aml_alert import AMLAlert

from app.repositories.aml_repository import AMLRepository


class AMLService:

    LARGE_TRANSFER_LIMIT = Decimal("50000")

    @staticmethod
    def check_large_transfer(
        db: Session,
        account_id: int,
        transaction_id: int | None,
        amount: Decimal
    ):

        if amount <= AMLService.LARGE_TRANSFER_LIMIT:
            return

        alert = AMLAlert(
            account_id=account_id,
            transaction_id=transaction_id,
            rule_triggered="Large Transfer",
            severity="HIGH",
            status="OPEN",
            remarks=f"Transfer of ₹{amount}"
        )

        AMLRepository.create_alert(
            db,
            alert
        )

    @staticmethod
    def check_round_amount(
        db: Session,
        account_id: int,
        transaction_id: int | None,
        amount: Decimal
    ):

        suspicious = [
            Decimal("100000"),
            Decimal("200000"),
            Decimal("500000"),
            Decimal("1000000")
        ]

        if amount not in suspicious:
            return

        alert = AMLAlert(
            account_id=account_id,
            transaction_id=transaction_id,
            rule_triggered="Round Amount Transfer",
            severity="MEDIUM",
            status="OPEN",
            remarks=f"Round amount ₹{amount}"
        )

        AMLRepository.create_alert(
            db,
            alert
        )

    @staticmethod
    def run_rules(
        db: Session,
        account_id: int,
        transaction_id: int | None,
        amount: Decimal
    ):

        AMLService.check_large_transfer(
            db,
            account_id,
            transaction_id,
            amount
        )

        AMLService.check_round_amount(
            db,
            account_id,
            transaction_id,
            amount
        )