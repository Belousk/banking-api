from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="client", cascade="all, delete")
    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="client", cascade="all, delete")
