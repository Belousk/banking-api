from datetime import date
from sqlalchemy import ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    loan_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    interest_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    client: Mapped["Client"] = relationship("Client", back_populates="loans")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="loan", cascade="all, delete")
