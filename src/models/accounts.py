from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, Numeric, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), unique=True)
    account_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


    client: Mapped["Client"] = relationship(back_populates="account", uselist=False)

    cards: Mapped[List["Card"]] = relationship(
        "Card",
        back_populates="account",
        cascade="all, delete"
    )