from decimal import Decimal

from pydantic import Field
from datetime import datetime

from src.schemas.v1.base import BaseSchema


class AccountCreate(BaseSchema):
    account_number: str = Field(min_length=5, max_length=20)

class AccountOut(AccountCreate):
    id: int
    client_id: int
    balance: Decimal
    created_at: datetime
