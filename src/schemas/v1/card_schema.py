from pydantic import Field
from typing import Optional
from datetime import date
from decimal import Decimal
from src.schemas.v1.base import BaseSchema



class CardCreate(BaseSchema):
    card_number: str = Field(min_length=16, max_length=16)
    card_type: str = Field(pattern="^(debit)$")

class CardShortOut(CardCreate):
    id: int
    account_id: int

class CardOut(CardShortOut):
    expiration_date: Optional[date]
    cvv: str = Field(min_length=3, max_length=5)
    balance: Decimal


