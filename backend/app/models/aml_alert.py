from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
)

from sqlalchemy.sql import func

from app.database import Base


class AMLAlert(Base):
    __tablename__ = "aml_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id"),
        nullable=True
    )

    rule_triggered = Column(
        String(100),
        nullable=False
    )

    severity = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(20),
        default="OPEN"
    )

    remarks = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )