from datetime import date
from typing import Optional
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    card_number: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date)
    cvv: Mapped[Optional[str]] = mapped_column(String(4))
    card_type: Mapped[str] = mapped_column(String(10))  # Например, "debit" или "credit"

    account: Mapped["Account"] = relationship("Account", back_populates="cards")
