from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    sender_account = Column(Integer, ForeignKey("accounts.id"))
    receiver_account = Column(Integer, ForeignKey("accounts.id"))

    amount = Column(Float, nullable=False)

    transaction_type = Column(String(20))