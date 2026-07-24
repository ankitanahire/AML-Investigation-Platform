from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.aml_alert import AMLAlert
from app.models.transaction import Transaction


class AMLRepository:

    @staticmethod
    def create_alert(
        db: Session,
        alert: AMLAlert
    ):
        db.add(alert)
        return alert

    @staticmethod
    def get_all_alerts(
        db: Session
    ):
        return (
            db.query(AMLAlert)
            .order_by(AMLAlert.created_at.desc())
            .all()
        )

    @staticmethod
    def get_alert_by_id(
        db: Session,
        alert_id: int
    ):
        return (
            db.query(AMLAlert)
            .filter(AMLAlert.id == alert_id)
            .first()
        )

    @staticmethod
    def update_status(
        db: Session,
        alert: AMLAlert,
        status: str
    ):
        alert.status = status
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_dashboard_statistics(
        db: Session
    ):

        total_alerts = db.query(AMLAlert).count()

        open_alerts = (
            db.query(AMLAlert)
            .filter(AMLAlert.status == "OPEN")
            .count()
        )

        resolved_alerts = (
            db.query(AMLAlert)
            .filter(AMLAlert.status == "RESOLVED")
            .count()
        )

        high_risk = (
            db.query(AMLAlert)
            .filter(AMLAlert.severity == "HIGH")
            .count()
        )

        critical = (
            db.query(AMLAlert)
            .filter(AMLAlert.severity == "CRITICAL")
            .count()
        )

        suspicious_accounts = (
            db.query(
                AMLAlert.account_id,
                func.count(AMLAlert.id).label("alerts")
            )
            .group_by(AMLAlert.account_id)
            .order_by(func.count(AMLAlert.id).desc())
            .limit(5)
            .all()
        )

        return {
            "total_alerts": total_alerts,
            "open_alerts": open_alerts,
            "resolved_alerts": resolved_alerts,
            "high_risk": high_risk,
            "critical": critical,
            "top_suspicious_accounts": [
                {
                    "account_id": row.account_id,
                    "alerts": row.alerts
                }
                for row in suspicious_accounts
            ]
        }