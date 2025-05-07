from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config import settings
from src.models.users import User
from src.schemas.v1.schemas import UserCreate
import hashlib


async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        client_id=user.client_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_token(data: dict, expires_delta: timedelta, key: bytes, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, key, algorithm=settings.ALGORITHM)
