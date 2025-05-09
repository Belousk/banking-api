from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.config import settings
from src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Client


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    description="Используйте этот endpoint для получения access токена. А refresh используйте вручную через /auth/refresh"
)



async def get_current_client(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> Client:
    try:
        payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    stmt = (
        select(Client)
        .options(joinedload(Client.account))
        .where(Client.email == email)
    )
    result = await session.execute(stmt)
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=404, detail="User not found")
    return client


