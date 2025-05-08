from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config import settings
from src.models import Client

import hashlib

from src.schemas.v1.client_schema import ClientCreate, ClientOut, ClientUpdate


async def get_client_by_email(session: AsyncSession, email: str) -> ClientOut:
    stmt = select(Client).where(Client.email == email)
    result = await session.execute(stmt)
    return ClientOut.model_validate(result.scalar_one_or_none(), from_attributes=True)



async def update_client_data(session: AsyncSession, client: ClientUpdate) -> ClientOut:
    client_db = await session.get(Client, client.id)
    client_db.full_name = client.full_name
    client_db.email = client.email
    client_db.phone_number = client.phone_number
    await session.refresh(client_db)
    await session.commit()

    return ClientOut.model_validate(client_db)


async def create_user(db: AsyncSession, client: ClientCreate) -> ClientOut:
    hashed_password = hashlib.sha256(client.password.encode()).hexdigest()
    db_user = Client(
        full_name = client.full_name,
        email = client.email,
        hashed_password = hashed_password,
        phone_number = client.phone_number,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return ClientOut.model_validate(db_user, from_attributes=True)

def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_token(data: dict, expires_delta: timedelta, key: bytes, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, key, algorithm=settings.ALGORITHM)
