from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base



class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    account: Mapped["Account"] = relationship("Account", back_populates="client", uselist=False)
