from pydantic import Field, EmailStr, validator
from datetime import datetime
import re

from src.schemas.v1.base import BaseSchema



class ClientGet(BaseSchema):
    id: int

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


class ClientUpdate(ClientCreate):
    pass


class ClientOut(ClientGet, ClientUpdate):
    hashed_password: str
    created_at: datetime
