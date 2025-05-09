from datetime import timedelta, datetime, timezone
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.config import settings
from src.models import Client

import hashlib

from src.schemas.v1.client_schema import ClientCreate, ClientOut, ClientUpdate


async def get_client_by_email(session: AsyncSession, email: str) -> Client:
    stmt = (
        select(Client)
        .options(joinedload(Client.account))
        .where(Client.email == email)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_client_by_id(session: AsyncSession, client_id: int) -> Client:
    stmt = (
        select(Client)
        .options(joinedload(Client.account))
        .where(Client.id == client_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_client_data(session: AsyncSession, client: ClientUpdate) -> ClientOut:
    client_db = await get_client_by_id(session, client.id)
    client_db.full_name = client.full_name
    client_db.email = client.email
    client_db.phone_number = client.phone_number
    await session.commit()

    return ClientOut.model_validate(client_db)


async def create_client_db(db: AsyncSession, client: ClientCreate, password: str) -> ClientOut:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
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

async def delete_client_db(client_id: int, db: AsyncSession) -> None:
    client = await get_client_by_id(db, client_id)

    if client:
        await db.delete(client)
        await db.commit()

def verify_password(plain_password, hashed_password) -> bool:
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_token(data: dict, expires_delta: timedelta, key: bytes, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, key, algorithm=settings.ALGORITHM)
