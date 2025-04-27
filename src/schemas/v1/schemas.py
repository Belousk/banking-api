from pydantic import Field, EmailStr, validator, BaseModel
from typing import Optional
from datetime import datetime, date
import re

from src.models.transactions import TransactionType
from src.schemas.v1.base import BaseSchema

# ------------ CLIENTS ------------

class ClientCreate(BaseSchema):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=20)

    @validator('phone_number')
    def validate_phone_number(cls, v):
        phone_pattern = re.compile(r'^\+?\d{10,15}$')
        if not phone_pattern.match(v):
            raise ValueError('Invalid phone number format. It must be digits, optional + at start.')
        return v

class ClientOut(ClientCreate):
    id: int
    created_at: datetime

# ------------ ACCOUNTS ------------

class AccountCreate(BaseSchema):
    client_id: int
    account_number: str = Field(min_length=5, max_length=20)

class AccountOut(AccountCreate):
    id: int
    balance: float
    created_at: datetime

# ------------ CARDS ------------

class CardCreate(BaseSchema):
    account_id: int
    card_number: str = Field(min_length=16, max_length=16)
    card_type: str = Field(pattern="^(debit|credit)$")

class CardOut(CardCreate):
    id: int
    expiration_date: Optional[date]

# ------------ TRANSACTIONS ------------
class MoneyTransferRequest(BaseModel):
    sender_account_id: int = Field(..., description="Sender account ID")
    receiver_account_id: int = Field(..., description="Receiver account ID")
    amount: float = Field(..., gt=0, description="Amount to transfer (must be greater than 0)")


class TransactionCreate(MoneyTransferRequest):
    transaction_type: str = Field(pattern="^(debit|credit|transfer)$")
    description: Optional[str] = Field(default=None, max_length=500)

class TransactionOut(TransactionCreate):
    id: int
    transaction_date: datetime


class MoneyTransferResponse(BaseModel):
    message: str

class TransactionHistoryOut(TransactionOut):
    pass


# ------------ LOANS ------------

class LoanCreate(BaseSchema):
    client_id: int
    loan_amount: float = Field(gt=0)
    interest_rate: float = Field(gt=0, lt=100)
    start_date: date
    end_date: date

class LoanOut(LoanCreate):
    id: int

# ------------ PAYMENTS ------------

class PaymentCreate(BaseSchema):
    loan_id: int
    payment_amount: float = Field(gt=0)

class PaymentOut(PaymentCreate):
    id: int
    payment_date: datetime

