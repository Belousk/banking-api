from datetime import date
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    card_number: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date)
    cvv: Mapped[Optional[str]] = mapped_column(String(4))
    card_type: Mapped[str] = mapped_column(String(10))
    balance: Mapped[float] = mapped_column(Numeric(15, 2), default=0)

    sent_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="sender_card",
        foreign_keys="[Transaction.sender_card_id]"
    )
    received_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="receiver_card",
        foreign_keys="[Transaction.receiver_card_id]"
    )

    account: Mapped["Account"] = relationship("Account", back_populates="cards")
