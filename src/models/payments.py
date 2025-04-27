from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.id", ondelete="CASCADE"))
    payment_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    payment_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    loan: Mapped["Loan"] = relationship("Loan", back_populates="payments")
