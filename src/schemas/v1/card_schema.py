from pydantic import Field
from typing import Optional
from datetime import date

from src.schemas.v1.base import BaseSchema



class CardCreate(BaseSchema):
    card_number: str = Field(min_length=16, max_length=16)
    card_type: str = Field(pattern="^(debit)$")

class CardOut(CardCreate):
    # generate automatically
    id: int
    expiration_date: Optional[date]
    cvv: int = Field(min_length=3, max_length=5)
    # take from current_client.account.id
    account_id: int




