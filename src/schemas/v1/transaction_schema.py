from decimal import Decimal

from pydantic import Field
from typing import Optional
from datetime import datetime

from src.schemas.v1.base import BaseSchema

class MoneyTransferRequest(BaseSchema):
    sender_card_id: int = Field(..., description="Sender account ID")
    receiver_card_id: int = Field(..., description="Receiver account ID")
    amount: Decimal = Field(..., gt=0, description="Amount to transfer (must be greater than 0)")


class TransactionCreate(MoneyTransferRequest):
    transaction_type: str = Field(pattern="^(debit|credit|transfer)$")
    description: Optional[str] = Field(default=None, max_length=500)

class TransactionOut(TransactionCreate):
    id: int
    transaction_date: datetime

class TransactionResponse(BaseSchema):
    message: str

