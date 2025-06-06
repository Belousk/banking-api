import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Numeric, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy import Enum as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class TransactionType(enum.Enum):
    debit = 'debit'
    credit ='credit'
    transfer ='transfer'


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    sender_card_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cards.id", ondelete="SET NULL"), nullable=True
    )

    receiver_card_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cards.id", ondelete="SET NULL"), nullable=True
    )

    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)

    transaction_type: Mapped[TransactionType] = mapped_column(
        PgEnum(TransactionType, name="transaction_type_enum", create_constraint=True),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(Text)
    transaction_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )


    # Опциональные связи
    sender_card: Mapped[Optional["Card"]] = relationship(
        "Card",
        foreign_keys=[sender_card_id],
        back_populates="sent_transactions",
    )

    receiver_card: Mapped[Optional["Card"]] = relationship(
        "Card",
        foreign_keys=[receiver_card_id],
        back_populates="received_transactions",
    )

