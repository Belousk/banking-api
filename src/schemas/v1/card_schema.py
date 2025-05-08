from pydantic import Field
from typing import Optional
from datetime import date

from src.schemas.v1.base import BaseSchema



class CardCreate(BaseSchema):
    account_id: int
    card_number: str = Field(min_length=16, max_length=16)
    card_type: str = Field(pattern="^(debit|credit)$")

class CardOut(CardCreate):
    id: int
    expiration_date: Optional[date]


