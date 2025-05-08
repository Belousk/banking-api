from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.config import settings
from src.database import async_session_factory, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Client
from src.schemas.v1.client_schema import ClientOut
from src.services.client_service import get_client_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_client(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> ClientOut:
    try:
        payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


    client = await get_client_by_email(session, email)

    return client


