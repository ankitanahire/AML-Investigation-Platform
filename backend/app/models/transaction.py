from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    sender_account = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=True
    )

    receiver_account = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=True
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    transaction_type = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )