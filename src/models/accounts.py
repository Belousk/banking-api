from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, Numeric, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    account_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    sent_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="sender_account",
        foreign_keys="[Transaction.sender_account_id]"
    )

    received_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="receiver_account",
        foreign_keys="[Transaction.receiver_account_id]"
    )
    client: Mapped["Client"] = relationship(back_populates="accounts")

    cards: Mapped[List["Card"]] = relationship(
        "Card",
        back_populates="account",
        cascade="all, delete"
    )